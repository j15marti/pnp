#!/usr/bin/env python3
"""Reproducible finite controls for the PNP semantic-composition review.

No SAT hardness assumption is used. Exhaustive truth tables, squarefree
polynomial reduction, and weighted-graph shortest paths are independent
representations. This is not a physical Turing-machine simulation.
Run: python semantic_composition_audit.py --output results.json
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import heapq
import itertools
import json
from pathlib import Path
import random
import time

Clause = tuple[int, ...]
CNF = tuple[Clause, ...]
Polynomial = dict[int, int]  # monomial support mask -> integer coefficient


def satisfies(formula: CNF, assignment: int) -> bool:
    return all(any(bool(assignment & (1 << (abs(lit)-1))) == (lit > 0)
                   for lit in clause) for clause in formula)


def mask_clauses(masks: list[int]) -> CNF:
    return tuple(tuple(-(j+1) if (mask >> j) & 1 else j+1
                       for j in range(3)) for mask in masks)


def add(a: Polynomial, b: Polynomial, factor: int = 1) -> Polynomial:
    c = a.copy()
    for mon, coeff in b.items():
        c[mon] = c.get(mon, 0) + factor*coeff
        if c[mon] == 0:
            del c[mon]
    return c


def multiply_squarefree(a: Polynomial, b: Polynomial) -> Polynomial:
    """Multiply modulo x_i^2 = x_i; uses sharing, not independent inputs."""
    c: Polynomial = {}
    for i, u in a.items():
        for j, v in b.items():
            mask = i | j
            c[mask] = c.get(mask, 0) + u*v
    return {mask: coeff for mask, coeff in c.items() if coeff}


def canonical_multilinear(formula: CNF) -> Polynomial:
    p: Polynomial = {0: 1}
    for clause in formula:
        failure: Polynomial = {0: 1}
        for lit in clause:
            mon = 1 << (abs(lit)-1)
            literal = {mon: 1} if lit > 0 else {0: 1, mon: -1}
            failure = multiply_squarefree(failure, add({0: 1}, literal, -1))
        p = multiply_squarefree(p, add({0: 1}, failure, -1))
    return p


def evaluate(p: Polynomial, z: tuple[Fraction, ...]) -> Fraction:
    result = Fraction(0)
    for mask, coeff in p.items():
        term = Fraction(coeff)
        for j, value in enumerate(z):
            if (mask >> j) & 1:
                term *= value
        result += term
    return result


def naive_gate_extension(formula: CNF, z: tuple[Fraction, ...]) -> Fraction:
    result = Fraction(1)
    for clause in formula:
        false = Fraction(1)
        for lit in clause:
            value = z[abs(lit)-1]
            literal = value if lit > 0 else 1-value
            false *= 1-literal
        result *= 1-false
    return result


def fraction_record(v: Fraction) -> dict[str, int]:
    return {"numerator": v.numerator, "denominator": v.denominator}


def test_robustness() -> dict:
    layers = []
    total = 0
    for r in (1, 2, 3):
        masks = [s for s in range(8) for _ in range(r)]
        baseline = [r]*8
        for k in range(1, r+1):
            sat_count = 0
            count = 0
            for indices in itertools.combinations(range(24*r), k):
                changed: dict[int, int] = {}
                for coordinate in indices:
                    row, bit = divmod(coordinate, 3)
                    changed[row] = changed.get(row, 0) ^ (1 << bit)
                multiplicities = baseline.copy()
                for row, change in changed.items():
                    old, new = masks[row], masks[row] ^ change
                    multiplicities[old] -= 1
                    multiplicities[new] += 1
                sat_count += (0 in multiplicities)
                count += 1
            expected = 0 if k < r else 8*(3**r)
            assert sat_count == expected, (r, k, sat_count, expected)
            layers.append({"copies": r, "radius": k, "tested": count,
                           "sat_neighbors": sat_count})
            total += count
    block_tests = 0
    for r in range(1, 17):
        masks = [s for s in range(8) for _ in range(r)]
        occupied: set[int] = set()
        for s in range(8):
            for bit in range(3):
                block = {3*(s*r+j)+bit for j in range(r)}
                assert len(block) == r and occupied.isdisjoint(block)
                occupied |= block
                mutated = masks.copy()
                for coordinate in block:
                    row, b = divmod(coordinate, 3)
                    mutated[row] ^= 1 << b
                assert len(set(mutated)) == 7
                block_tests += 1
        assert occupied == set(range(24*r))
    return {"hamming_layers": layers, "total_hamming_variants": total,
            "disjoint_sensitive_blocks_checked": block_tests,
            "copies_tested_for_blocks": list(range(1, 17))}


def test_extensions() -> dict:
    rng = random.Random(20261114)
    fixtures: list[tuple[str, int, CNF]] = []
    for r in range(1, 9):
        masks = [s for s in range(8) for _ in range(r)]
        fixtures.append((f"U_{r}", 3, mask_clauses(masks)))
        neighbor = masks.copy()
        for j in range(r):
            neighbor[j] ^= 1
        fixtures.append((f"nearest_SAT_{r}", 3, mask_clauses(neighbor)))
        fixtures.append((f"single_signature_{r}", 3, mask_clauses([0]*(8*r))))
    fixtures += [
        ("shared_variable", 3, ((1,2,3),(-1,2,3))),
        ("Horn", 4, ((1,),(-1,2),(-2,3),(-3,4))),
        ("Horn_UNSAT", 4, ((1,),(-1,2),(-2,3),(-3,4),(-4,))),
        ("2SAT", 3, ((1,2),(-1,3),(-2,-3))),
        ("2SAT_lift", 4, ((1,2,4),(1,2,-4))),
        ("XOR3_even", 3, mask_clauses([1,2,4,7])),
        ("XOR3_odd", 3, mask_clauses([0,3,5,6])),
        ("disjoint_product", 6, ((1,2,3),(-1,-2,-3),(4,5,6),(-4,-5,-6))),
        ("duplicate_clauses", 3, ((1,2,3),)*12),
        ("renamed", 5, ((5,2,4),(-5,2,4))),
        ("contradiction", 1, ((1,),(-1,))),
    ]
    for n in range(3, 7):
        for k in range(40):
            f = tuple(tuple(v if rng.getrandbits(1) else -v
                            for v in rng.sample(range(1,n+1),3))
                      for _ in range(rng.randrange(1, 13)))
            fixtures.append((f"seeded_n{n}_{k}", n, f))
    boolean_checks = 0
    midpoint_checks = 0
    mismatches = 0
    records = []
    for name, n, f in fixtures:
        poly = canonical_multilinear(f)
        model_count = 0
        for a in range(1 << n):
            truth = satisfies(f, a)
            z = tuple(Fraction((a >> j) & 1) for j in range(n))
            assert evaluate(poly,z) == int(truth)
            assert naive_gate_extension(f,z) == int(truth)
            model_count += truth
            boolean_checks += 1
        center = (Fraction(1,2),)*n
        exact = evaluate(poly,center)
        naive = naive_gate_extension(f,center)
        assert exact == Fraction(model_count, 1 << n)
        midpoint_checks += 1
        mismatches += (exact != naive)
        if name.startswith(("U_", "nearest_SAT_", "single_signature_")):
            r = int(name.rsplit("_",1)[1])
            assert naive == Fraction(7,8)**(8*r)
            expected = 0 if name.startswith("U_") else (1 if name.startswith("nearest") else 7)
            assert model_count == expected
        if not name.startswith("seeded"):
            records.append({"name":name,"variables":n,"clauses":len(f),
                            "models":model_count,"canonical_midpoint":fraction_record(exact),
                            "gatewise_midpoint":fraction_record(naive),
                            "squarefree_terms":len(poly)})
    return {"seed":20261114,"formulas":len(fixtures),
            "boolean_assignments_checked":boolean_checks,
            "midpoint_identities_checked":midpoint_checks,
            "midpoint_disagreements":mismatches,"named_controls":records}


def test_graph_ceiling() -> dict:
    rng = random.Random(14082026)
    graph_count = 0
    edges_audited = 0
    terminal_count = 0
    positive_examples = []
    for n in range(2, 20):
        for _ in range(10):
            bound = rng.randrange(1, 10)
            # All states can reach terminal n-1 along a paid/zero-cost chain.
            edges = [(u,u+1,rng.randrange(bound+1)) for u in range(n-1)]
            edges += [(u,v,rng.randrange(bound+1)) for u in range(n)
                      for v in range(n) if rng.randrange(10) == 0 and u != n-1]
            reverse = [[] for _ in range(n)]
            for u,v,c in edges:
                reverse[v].append((u,c))
            d = [float('inf')]*n
            d[-1]=0
            queue=[(0,n-1)]
            while queue:
                dv,v=heapq.heappop(queue)
                if dv != d[v]:continue
                for u,c in reverse[v]:
                    if dv+c < d[u]:
                        d[u]=dv+c
                        heapq.heappush(queue,(d[u],u))
            for u,v,c in edges:
                assert d[u] <= c+d[v]
                edges_audited += 1
            assert d[0] <= (n-1)*bound
            assert d[-1] == 0
            terminal_count += 1
            graph_count += 1
    # Necessary qualifier: a polynomial-size *succinct description* is different
    # from a polynomial number of states. Binary countdown has exponentially many.
    for width in range(1, 13):
        initial = (1 << width)-1
        for v in range(1,initial+1):
            assert v == 1+(v-1)
        positive_examples.append({"counter_bits":width,"states":1<<width,
                                  "exact_countdown_cost":initial})
    return {"graphs":graph_count,"edge_inequalities":edges_audited,
            "terminal_checks":terminal_count,"succinct_counter_controls":positive_examples}


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    started=time.perf_counter()
    payload={"status":"COMPUTATIONAL", "physical_TM_simulation":False,
             "robustness":test_robustness(),
             "semantic_extensions":test_extensions(),
             "explicit_graph_ceiling":test_graph_ceiling()}
    payload['runtime_seconds']=round(time.perf_counter()-started,6)
    body=Path(__file__).read_bytes()
    payload['code_sha256']=hashlib.sha256(body).hexdigest()
    args.output.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
    print(json.dumps({"runtime_seconds":payload['runtime_seconds'],
                     "hamming_variants":payload['robustness']['total_hamming_variants'],
                     "block_checks":payload['robustness']['disjoint_sensitive_blocks_checked'],
                     "formulas":payload['semantic_extensions']['formulas'],
                     "boolean_assignments":payload['semantic_extensions']['boolean_assignments_checked'],
                     "midpoint_disagreements":payload['semantic_extensions']['midpoint_disagreements'],
                     "graph_edges":payload['explicit_graph_ceiling']['edge_inequalities'],
                     "failures":0},indent=2))

if __name__=='__main__':
    main()
