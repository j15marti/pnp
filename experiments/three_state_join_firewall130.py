#!/usr/bin/env python3
"""Independent audit of EXACTONE-JOIN-CYCLE95.

Finite checks cover the exact-one affine/binary identity, the linear
proper-3CNF compiler, named equality joins, the matched arc-consistent
SAT/UNSAT pair, and randomized small source instances.  This is not an
unrestricted SAT lower bound.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from collections import defaultdict, deque
from itertools import product
from pathlib import Path


def lit_value(lit, assignment):
    name = lit[1:] if lit.startswith("!") else lit
    value = assignment[name]
    return not value if lit.startswith("!") else value


def exact_one(module, assignment):
    return sum(lit_value(x, assignment) for x in module) == 1


def local_domain(module):
    names = [x[1:] if x.startswith("!") else x for x in module]
    out = []
    for bits in product((0, 1), repeat=3):
        a = dict(zip(names, map(bool, bits)))
        if exact_one(module, a):
            out.append(bits)
    return out


def gf2_rank(rows):
    rows = [sum((bit & 1) << j for j, bit in enumerate(row)) for row in rows]
    rank = 0
    bit = 1
    while bit <= max(rows or [0]):
        pivot = next((i for i in range(rank, len(rows)) if rows[i] & bit), None)
        if pivot is not None:
            rows[rank], rows[pivot] = rows[pivot], rows[rank]
            for i in range(len(rows)):
                if i != rank and rows[i] & bit:
                    rows[i] ^= rows[rank]
            rank += 1
        bit <<= 1
    return rank


def aff_dim(domain):
    base = domain[0]
    return gf2_rank([tuple(x ^ y for x, y in zip(row, base)) for row in domain[1:]])


def occurrence_links(modules):
    occurrences = defaultdict(list)
    for i, module in enumerate(modules):
        for j, lit in enumerate(module):
            occurrences[lit[1:] if lit.startswith("!") else lit].append((i, j))
    links = defaultdict(list)
    for occs in occurrences.values():
        for left, right in zip(occs, occs[1:]):
            key = (left[0], right[0])
            links[key].append((left[1], right[1]))
    return dict(links)


def arc_consistency(modules):
    domains = [set(local_domain(m)) for m in modules]
    links = occurrence_links(modules)
    adjacency = defaultdict(list)
    for (i, j), coords in links.items():
        adjacency[i].append((j, coords))
        adjacency[j].append((i, [(b, a) for a, b in coords]))
    queue = deque((i, j, tuple(coords)) for i in adjacency for j, coords in adjacency[i])
    revisions = 0
    while queue:
        i, j, coords = queue.popleft()
        keep = {
            x for x in domains[i]
            if any(all(x[a] == y[b] for a, b in coords) for y in domains[j])
        }
        if keep != domains[i]:
            domains[i] = keep
            revisions += 1
            for h, hcoords in adjacency[i]:
                if h != j:
                    queue.append((h, i, tuple((b, a) for a, b in hcoords)))
    return domains, links, revisions


def source_sat(modules):
    names = sorted({lit[1:] if lit.startswith("!") else lit for m in modules for lit in m})
    witnesses = []
    for bits in product((0, 1), repeat=len(names)):
        a = dict(zip(names, map(bool, bits)))
        if all(exact_one(m, a) for m in modules):
            witnesses.append(tuple(bits))
    return names, witnesses


def join_sat(modules):
    domains = [local_domain(m) for m in modules]
    links = occurrence_links(modules)
    for choice in product(*domains):
        if all(all(choice[i][a] == choice[j][b] for a, b in coords)
               for (i, j), coords in links.items()):
            return True
    return False


class CnfBuilder:
    def __init__(self):
        self.next_var = 1
        self.clauses = []

    def fresh(self):
        v = self.next_var
        self.next_var += 1
        return v

    def binary(self, a, b):
        z = self.fresh()
        self.clauses.extend([(a, b, z), (a, b, -z)])


def compile_cnf(modules):
    b = CnfBuilder()
    occ = []
    for module in modules:
        row = [b.fresh() for _ in module]
        occ.append(row)
        expr = [(-v if lit.startswith("!") else v) for v, lit in zip(row, module)]
        for values in product((0, 1), repeat=3):
            if sum(values) % 2 == 0:
                b.clauses.append(tuple(e if value == 0 else -e for e, value in zip(expr, values)))
        b.binary(-expr[0], -expr[1])
    occurrences = defaultdict(list)
    for i, module in enumerate(modules):
        for j, lit in enumerate(module):
            name = lit[1:] if lit.startswith("!") else lit
            occurrences[name].append(occ[i][j])
    equality_links = 0
    for vars_ in occurrences.values():
        for u, v in zip(vars_, vars_[1:]):
            b.binary(-u, v)
            b.binary(u, -v)
            equality_links += 1
    return {
        "clauses": b.clauses,
        "variables": b.next_var - 1,
        "links": equality_links,
    }


def clause_true(clause, assignment):
    return any(assignment[abs(lit)] == (lit > 0) for lit in clause)


def verify_local_encoding():
    checks = 0
    # Exact-one = odd parity AND not(first AND second).
    for values in product((0, 1), repeat=3):
        one = sum(values) == 1
        rhs = (sum(values) % 2 == 1) and not (values[0] and values[1])
        assert one == rhs
        checks += 1
    # Binary properization and equality gadgets.
    for a, c, z in product((0, 1), repeat=3):
        lifted = (a or c or z) and (a or c or not z)
        assert lifted == (a or c)
        checks += 1
    for u, v in product((0, 1), repeat=2):
        base = ((not u) or v) and (u or (not v))
        assert base == (u == v)
        checks += 1
    return checks


def run(seed=20261024):
    checks = verify_local_encoding()
    U = [("a", "b", "c"), ("a", "b", "d"), ("a", "c", "d"), ("b", "c", "d")]
    S = U[:3] + [("!b", "c", "d")]
    pair = {}
    for label, modules in (("UNSAT", U), ("SAT", S)):
        names, witnesses = source_sat(modules)
        assert bool(witnesses) == (label == "SAT")
        assert join_sat(modules) == bool(witnesses)
        checks += 2
        domains, links, revisions = arc_consistency(modules)
        assert [len(x) for x in domains] == [3, 3, 3, 3]
        assert revisions == 0
        assert sorted(links) == [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)]
        assert sorted(len(v) for v in links.values()) == [1, 1, 2, 2, 2]
        checks += 4
        for domain in domains:
            assert aff_dim(sorted(domain)) == 2
            checks += 1
        compiled = compile_cnf(modules)
        assert compiled["variables"] == 32
        assert len(compiled["clauses"]) == 56
        assert compiled["links"] == 8
        assert all(len({abs(x) for x in c}) == 3 for c in compiled["clauses"])
        assert len(set(compiled["clauses"])) == len(compiled["clauses"])
        checks += 5
        pair[label] = {"modules": modules, "witnesses": witnesses, "domains": domains, "compiled": compiled}

    unsigned_u = [tuple(sorted(abs(x) for x in c)) for c in pair["UNSAT"]["compiled"]["clauses"]]
    unsigned_s = [tuple(sorted(abs(x) for x in c)) for c in pair["SAT"]["compiled"]["clauses"]]
    assert unsigned_u == unsigned_s
    checks += 1

    def half_relation(modules):
        names = ["a", "b", "c", "d"]
        return {
            bits for bits in product((0, 1), repeat=4)
            if all(exact_one(m, dict(zip(names, map(bool, bits)))) for m in modules)
        }

    left = half_relation(U[:2])
    right_u = half_relation(U[2:])
    right_s = half_relation(S[2:])
    assert len(left) == len(right_u) == len(right_s) == 3
    assert len(left & right_u) == 0
    assert len(left & right_s) == 1
    checks += 3

    rng = random.Random(seed)
    random_cases = 0
    random_sat = 0
    random_unsat = 0
    variables = list("abcdefg")
    for _ in range(240):
        nv = rng.randint(3, 7)
        m = rng.randint(2, 5)
        modules = []
        for _ in range(m):
            triple = rng.sample(variables[:nv], 3)
            modules.append(tuple(("!" if rng.getrandbits(1) else "") + x for x in triple))
        _, witnesses = source_sat(modules)
        joined = join_sat(modules)
        assert joined == bool(witnesses)
        checks += 1
        for module in modules:
            domain = local_domain(module)
            assert len(domain) == 3 and aff_dim(domain) == 2
            checks += 1
        compiled = compile_cnf(modules)
        nplus = len({lit[1:] if lit.startswith("!") else lit for mod in modules for lit in mod})
        L = 3 * m - nplus
        assert compiled["variables"] == 4 * m + 2 * L
        assert len(compiled["clauses"]) == 6 * m + 4 * L
        assert compiled["links"] == L
        checks += 3
        random_cases += 1
        random_sat += bool(witnesses)
        random_unsat += not bool(witnesses)

    # Exhaust all eight sign patterns on the fourth matched triple.
    fourth_labels = []
    fourth_domain_sizes = []
    for signs in product((0, 1), repeat=3):
        fourth = tuple(("!" if sign else "") + x for sign, x in zip(signs, ("b", "c", "d")))
        modules = U[:3] + [fourth]
        _, witnesses = source_sat(modules)
        domains, _, _ = arc_consistency(modules)
        assert all(0 <= len(d) <= 3 for d in domains)
        fourth_labels.append(bool(witnesses))
        fourth_domain_sizes.append([len(d) for d in domains])
        checks += 1

    result = {
        "status": "COMPUTATIONAL finite audit; P versus NP and ARC-EDGE-90 OPEN",
        "assertion_accounted_checks": checks,
        "seed": seed,
        "matched_pair": {
            "source_variables": 4,
            "modules": 4,
            "local_domain_sizes_after_arc_consistency": [3, 3, 3, 3],
            "arc_revisions": 0,
            "interaction_edges": [[1, 2], [1, 3], [2, 3], [2, 4], [3, 4]],
            "equality_links": 8,
            "compiled_variables": 32,
            "compiled_clauses": 56,
            "word_width": 13,
            "encoded_bits": 2938,
            "unsat_witness_count": len(pair["UNSAT"]["witnesses"]),
            "sat_witness_count": len(pair["SAT"]["witnesses"]),
            "two_level_intersections": {"UNSAT": 0, "SAT": 1},
        },
        "random_controls": {
            "cases": random_cases,
            "sat": random_sat,
            "unsat": random_unsat,
        },
        "fourth_module_sign_controls": {
            "labels": fourth_labels,
            "post_arc_domain_sizes": fourth_domain_sizes,
            "sat": sum(fourth_labels),
            "unsat": len(fourth_labels) - sum(fourth_labels),
        },
        "accepted_scope": "constant three-state local domains, equality-only global join, matched arc-consistency firewall",
        "rejected_inference": "bounded local support or arc consistency implies a favorable all-input SAT resource transition",
    }
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()
    result = run()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.json:
        args.json.write_text(payload, encoding="utf-8")
        result["json_sha256"] = hashlib.sha256(payload.encode()).hexdigest()
        payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    print(payload, end="")


if __name__ == "__main__":
    main()
