#!/usr/bin/env python3
"""Independent truth-table comparisons and explicitly limited finite controls.

Run each stage separately.  Each is sized to finish in under 30 seconds.
Results contain the complete generated CNFs, reproducible seeds, source hashes,
and operation counts.  No finite result is promoted to an asymptotic claim.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import random
import time
from affine_table import Interface, Work, normalize, join, project, compile_cnf


def dense_mask(rel):
    return sum(int(rel.accepts(x)) << x for x in range(1 << rel.n))


def independent_rank(vectors):
    # Row-space cardinality calculation, independent of producer elimination.
    space = {0}
    for v in vectors:
        if v not in space:
            space |= {u ^ v for u in list(space)}
    return len(space).bit_length() - 1


def intrinsic_width(mask, n):
    accepted = [x for x in range(1 << n) if (mask >> x) & 1]
    if not accepted:
        return 0
    d = independent_rank([x ^ accepted[0] for x in accepted])
    periods = [t for t in range(1 << n)
               if all(((mask >> x) & 1) == ((mask >> (x ^ t)) & 1)
                      for x in range(1 << n))]
    return d - (len(periods).bit_length() - 1)


def literal_truth(lit, assignment):
    val = bool((assignment >> (abs(lit) - 1)) & 1)
    return val if lit > 0 else not val


def cnf_truth(clauses, assignment):
    return all(any(literal_truth(lit, assignment) for lit in c) for c in clauses)


def algebra(seed):
    rng = random.Random(seed)
    assertions = 0
    relations = []
    w = Work(cap=12)
    for mask in range(256):
        rel = Interface(3, (), (1, 2, 4), tuple(bool((mask >> x) & 1) for x in range(8)))
        canon = normalize(rel, w)
        assert dense_mask(canon) == mask
        assert canon.width == intrinsic_width(mask, 3)
        assertions += 2
        relations.append(canon)
        for private_mask in range(8):
            private = [j for j in range(3) if (private_mask >> j) & 1]
            result = project(canon, private, w)
            expected = 0
            for x in range(8):
                feasible = any((mask >> z) & 1 for z in range(8)
                               if ((x ^ z) & (7 ^ private_mask)) == 0)
                expected |= int(feasible) << x
            assert dense_mask(result) == expected
            assert result.width <= canon.width
            assert result.width == intrinsic_width(expected, 3)
            assertions += 3
    for _ in range(512):
        a, b = rng.randrange(256), rng.randrange(256)
        result = join(relations[a], relations[b], w)
        assert dense_mask(result) == (a & b)
        assert result.width <= relations[a].width + relations[b].width
        assertions += 2
    random_cases = []
    for case in range(300):
        n = rng.randrange(1, 8)
        k = rng.randrange(0, 5)
        eqs = tuple((rng.randrange(1 << n), rng.randrange(2))
                    for _ in range(rng.randrange(n + 2)))
        forms = tuple(rng.randrange(1 << n) for _ in range(k))
        table = tuple(bool(rng.randrange(2)) for _ in range(1 << k))
        original = Interface(n, eqs, forms, table)
        canon = normalize(original, w)
        before = dense_mask(original)
        assert dense_mask(canon) == before
        assert canon.width == intrinsic_width(before, n)
        private = [j for j in range(n) if rng.randrange(2)]
        private_mask = sum(1 << j for j in private)
        result = project(canon, private, w)
        expected = 0
        for x in range(1 << n):
            feasible = any((before >> z) & 1 for z in range(1 << n)
                           if ((x ^ z) & (((1 << n) - 1) ^ private_mask)) == 0)
            expected |= int(feasible) << x
        assert dense_mask(result) == expected
        assert result.width == intrinsic_width(expected, n)
        assertions += 4
        random_cases.append({"n": n, "equations": eqs, "forms": forms,
                             "table": table, "private": private,
                             "input_support_hex": hex(before),
                             "projected_support_hex": hex(expected),
                             "normalized_width": canon.width,
                             "projected_width": result.width})
    return {"stage": "algebra", "assertions": assertions, "failures": 0,
            "all_three_variable_functions": 256, "exhaustive_projections": 2048,
            "sampled_joins": 512, "random_interfaces": random_cases,
            "work": {k: v for k, v in vars(w).items() if k != "trace"}}


def sat_tests(seed):
    rng = random.Random(seed)
    cases = []
    assertions = 0
    for n in range(3, 11):
        for trial in range(18):
            m = rng.randrange(0, 6 * n + 1)
            clauses = [tuple(v if rng.randrange(2) else -v
                             for v in rng.sample(range(1, n + 1), 3)) for _ in range(m)]
            expected = any(cnf_truth(clauses, x) for x in range(1 << n))
            answer, work = compile_cnf(n, clauses, cap=12)
            assert answer is expected
            assertions += 1
            cases.append({"n": n, "clauses": clauses, "truth_table_answer": expected,
                          "compiler_answer": answer, "max_table_width": work.max_width,
                          "table_evaluations": work.table_evaluations,
                          "fourier_butterflies": work.fourier_butterflies,
                          "trace": work.trace})
    return {"stage": "sat", "assertions": assertions, "failures": 0,
            "sat_cases": sum(c["compiler_answer"] for c in cases),
            "unsat_cases": sum(not c["compiler_answer"] for c in cases),
            "cases": cases}


def or_chain(n):
    if n < 3:
        raise ValueError("n>=3")
    if n == 3:
        return [(1, 2, 3)]
    zs = list(range(n + 1, 2 * n - 2))
    clauses = [(1, 2, zs[0])]
    for i in range(len(zs) - 1):
        clauses.append((-zs[i], i + 3, zs[i + 1]))
    clauses.append((-zs[-1], n - 1, n))
    return clauses


def controls(seed):
    assertions = 0
    w = Work(cap=14)
    rows = []
    # Compact proper-3CNF source projecting to OR_n on n boundary variables.
    for n in range(3, 9):
        total = 2 * n - 3
        clauses = or_chain(n)
        from affine_table import clause_interface
        factors = [clause_interface(total, [c], w) for c in clauses]
        acc = factors[0]
        for f in factors[1:]:
            acc = join(acc, f, w)
        result = project(acc, range(n, total), w)
        assert result.width == n
        for x in range(1 << n):
            assert result.accepts(x) == bool(x)
            assertions += 1
        assertions += 1
        answer, ww = compile_cnf(total, clauses, cap=14)
        assert answer is True
        assertions += 1
        rows.append({"family": "OR_boundary", "boundary_variables": n,
                     "private_variables": n - 3, "clauses": clauses,
                     "normalized_projected_width": result.width,
                     "table_entries": len(result.table),
                     "decision_elimination_max_width": ww.max_width})
    # Disjoint clauses: direct global width grows, early elimination stays small.
    for m in range(1, 5):
        n = 3 * m
        clauses = [tuple(range(3 * j + 1, 3 * j + 4)) for j in range(m)]
        answer, ww = compile_cnf(n, clauses, cap=4)
        assert answer is True and ww.max_width == 3
        assertions += 1
        rows.append({"family": "independent_OR3", "m": m,
                     "mathematically_proved_global_width": 3 * m,
                     "decision_elimination_max_width": ww.max_width})
    # An unbounded physical boundary with no nonlinear table directions.
    n = 4096
    equations = tuple((sum(1 << j for j in range(256 * i, 256 * (i + 1))), i % 2)
                      for i in range(16))
    parity = normalize(Interface(n, equations, (), (True,)), w)
    projected = project(parity, [256 * i for i in range(16)], w)
    assert parity.width == 0 and projected.width == 0
    assert projected.equations == ()
    assertions += 3
    rows.append({"family": "large_affine_boundary", "variables": n,
                 "equations": 16, "table_width_before": 0,
                 "table_width_after": 0, "remaining_equations": 0})
    # Contradictory source parity packets: all four clauses of each sign.
    for rhs in (0, 1):
        clauses = []
        for assignment in range(8):
            if assignment.bit_count() % 2 != rhs:
                clauses.append(tuple(-(i + 1) if (assignment >> i) & 1 else i + 1
                                     for i in range(3)))
        answer, ww = compile_cnf(3, clauses, cap=4)
        assert answer is True
        bad, bw = compile_cnf(3, clauses + [(1,), (2,), ((3,) if rhs == 0 else (-3,))], cap=4)
        assert bad is False
        assertions += 2
        rows.append({"family": "source_XOR", "rhs": rhs, "clauses": clauses,
                     "sat": answer, "contradictory_pins_sat": bad})
    # A budget overflow must remain UNRESOLVED.
    answer, ww = compile_cnf(3, [(1, 2, 3)], cap=2)
    assert answer is None
    assertions += 1
    # Binary-encoded sparse identifiers cannot trigger enormous bit masks.
    answer, ww = compile_cnf(10**9, [(1, 800000001, -1000000000)], cap=4)
    assert answer is True and ww.max_width == 3
    assertions += 1
    # Every certified one-pattern exclusion compresses OR3 from width3 to2.
    for a in range(1, 8):
        table = tuple(z not in (0, a) for z in range(8))
        rel = normalize(Interface(3, (), (1, 2, 4), table), w)
        assert rel.width == 2
        assert dense_mask(rel) == sum(int(z not in (0, a)) << z for z in range(8))
        assertions += 2
        rows.append({"family": "one_pattern_pruned", "excluded": a,
                     "width": rel.width, "forms": rel.forms, "table": rel.table})
    return {"stage": "controls", "assertions": assertions, "failures": 0, "cases": rows}


def selector_test(seed):
    # Exhaust all literal signs, original assignments, and selector triples.
    assertions = 0
    cases = []
    for signs in itertools.product((-1, 1), repeat=3):
        clause = tuple(signs[i] * (i + 1) for i in range(3))
        p, q, r = 4, 5, 6
        horn = [(-p, -q), (-p, -r), (-q, -r),
                (-p, clause[0]), (-q, clause[1]), (-r, clause[2])]
        for x in range(8):
            projected = any(cnf_truth(horn, x | (s << 3)) and s.bit_count() % 2 == 1
                            for s in range(8))
            assert projected == cnf_truth([clause], x)
            assert cnf_truth(horn, x)  # all selectors zero
            assertions += 2
        assert all(sum(l > 0 for l in c) <= 1 for c in horn)
        assertions += 1
        cases.append({"clause": clause, "horn_2cnf": horn,
                     "xor_variables": [p, q, r], "xor_rhs": 1})
    return {"stage": "selector", "assertions": assertions, "failures": 0,
            "cases": cases}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("algebra", "sat", "controls", "selector"))
    parser.add_argument("--seed", type=int, default=20261111)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    start = time.perf_counter()
    result = {"algebra": algebra, "sat": sat_tests, "controls": controls,
              "selector": selector_test}[args.stage](args.seed)
    result.update(seed=args.seed, status="COMPUTATIONAL",
                  elapsed_seconds=time.perf_counter() - start,
                  limitation="Finite exact comparisons; no universal width or polynomial SAT bound.",
                  source_sha256={p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in (Path(__file__), Path(__file__).with_name("affine_table.py"))})
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items()
                      if k not in ("cases", "random_interfaces")}, indent=2))
