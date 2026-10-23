#!/usr/bin/env python3
"""Independent finite audit for KROM-PROJECTION-CEILING99 (stdlib only)."""
from __future__ import annotations

import itertools
import json
import random
from pathlib import Path


def relation_p(p, mask):
    any_a = any((mask >> i) & 1 for i in range(p))
    any_b = any((mask >> (p + j)) & 1 for j in range(p))
    return not (any_a and any_b)


def mediator_exists(p, mask):
    for u in (0, 1):
        if all(not ((mask >> i) & 1) or u for i in range(p)) and \
           all(not u or not ((mask >> (p + j)) & 1) for j in range(p)):
            return True
    return False


def literal_true(lit, mask):
    var, positive = lit
    return bool((mask >> var) & 1) == positive


def clause_true(clause, mask):
    return any(literal_true(lit, mask) for lit in clause)


def all_clauses(s):
    # Per variable: absent, negative, positive. Complementary literals never occur.
    for state in itertools.product((-1, 0, 1), repeat=s):
        if all(x == -1 for x in state):
            continue
        yield tuple((i, x == 1) for i, x in enumerate(state) if x != -1)


def core_clause_audit(p):
    s = 2 * p
    good = [x for x in range(1 << s) if relation_p(p, x)]
    forbidden = [(1 << i) | (1 << (p + j)) for i in range(p) for j in range(p)]
    entailed = 0
    coverage = set()
    max_cover = 0
    for clause in all_clauses(s):
        if all(clause_true(clause, x) for x in good):
            entailed += 1
            hit = tuple(k for k, x in enumerate(forbidden) if not clause_true(clause, x))
            max_cover = max(max_cover, len(hit))
            coverage.update(hit)
    return {
        "p": p,
        "boundary_variables_s": s,
        "entailed_nonempty_clauses": entailed,
        "forbidden_minimal_assignments": p * p,
        "max_forbidden_assignments_falsified_by_one_entailed_clause": max_cover,
        "all_forbidden_assignments_clause_covered": len(coverage) == p * p,
        "minimum_cnf_clauses": p * p,
    }


def random_clause(rng, n):
    width = rng.choice((1, 2))
    vars_ = rng.sample(range(n), width)
    return tuple((v, bool(rng.getrandbits(1))) for v in vars_)


def eval_cnf(clauses, mask):
    return all(clause_true(c, mask) for c in clauses)


def projection_table(clauses, n, s):
    table = []
    for xmask in range(1 << s):
        ok = False
        for ymask in range(1 << (n - s)):
            mask = xmask | (ymask << s)
            if eval_cnf(clauses, mask):
                ok = True
                break
        table.append(ok)
    return table


def canonical_krom(table, s):
    clauses = []
    candidates = [((i, sign),) for i in range(s) for sign in (False, True)]
    for i in range(s):
        for j in range(i + 1, s):
            for si in (False, True):
                for sj in (False, True):
                    candidates.append(((i, si), (j, sj)))
    for clause in candidates:
        if all((not table[mask]) or clause_true(clause, mask)
               for mask in range(1 << s)):
            clauses.append(clause)
    return clauses


def weighted_source_count(p, positive_lambda):
    total = 0
    for a in range(1 << p):
        for b in range(1 << p):
            for u in (0, 1):
                if not all(not ((a >> i) & 1) or u for i in range(p)):
                    continue
                if not all(not u or not ((b >> j) & 1) for j in range(p)):
                    continue
                if not (a & 1):
                    continue
                b1 = bool(b & 1)
                if (b1 if positive_lambda else not b1) is False:
                    continue
                weight = 16  # four blocker r variables; blockers themselves are forced 0.
                for z in itertools.chain(((a >> i) & 1 for i in range(p)),
                                         ((b >> j) & 1 for j in range(p))):
                    weight *= 4 if z else 3
                total += weight
    return total


def h_p1_clauses(positive_lambda):
    # Variable order: a,b,u,s,t,v,w, rs,rt,rv,rw, then f,g,hf,hg for a and b.
    a, b, u, s, t, v, w, rs, rt, rv, rw = range(11)
    clauses = [
        ((a, False), (u, True)), ((u, False), (b, False)),
        ((s, False), (rs, True)), ((s, False), (rs, False)),
        ((t, False), (rt, True)), ((t, False), (rt, False)),
        ((v, False), (rv, True)), ((v, False), (rv, False)),
        ((w, False), (rw, True)), ((w, False), (rw, False)),
    ]
    nxt = 11
    for z in (a, b):
        f, g, hf, hg = range(nxt, nxt + 4)
        nxt += 4
        clauses.append(((z, True), (f, True), (g, True)))
        clauses.extend([
            ((f, False), (hf, True)), ((f, True), (hf, False)),
            ((g, False), (hg, True)), ((g, True), (hg, False)),
        ])
    clauses.append(((a, True), (s, True), (t, True)))
    clauses.append(((b, positive_lambda), (v, True), (w, True)))
    assert nxt == 19 and len(clauses) == 22
    return clauses


def main():
    assertions = 0
    boundary_assignments = 0
    rows = []
    for p in range(1, 5):
        for mask in range(1 << (2 * p)):
            assert relation_p(p, mask) == mediator_exists(p, mask)
            assertions += 1
            boundary_assignments += 1
        row = core_clause_audit(p)
        assert row["max_forbidden_assignments_falsified_by_one_entailed_clause"] == 1
        assert row["all_forbidden_assignments_clause_covered"]
        assertions += 2
        rows.append(row)

    rng = random.Random(2026102399)
    projection_instances = 0
    projection_assignments = 0
    for _ in range(320):
        n = rng.randint(2, 8)
        s = rng.randint(1, min(5, n))
        clauses = [random_clause(rng, n) for _ in range(rng.randint(0, 3 * n))]
        table = projection_table(clauses, n, s)
        out = canonical_krom(table, s)
        assert len(out) <= 2 * s * s
        assertions += 1
        for mask in range(1 << s):
            assert table[mask] == eval_cnf(out, mask)
            assertions += 1
            projection_assignments += 1
        projection_instances += 1

    source_rows = []
    for p in range(1, 9):
        sat = weighted_source_count(p, positive_lambda=False)
        unsat = weighted_source_count(p, positive_lambda=True)
        expected = 64 * (7 ** (p - 1)) * (3 ** p)
        assert sat == expected and unsat == 0
        assertions += 2
        source_rows.append({"p": p, "sat_models": sat, "unsat_models": unsat})

    full_source_assignments = 0
    for positive_lambda, expected in ((False, 192), (True, 0)):
        clauses = h_p1_clauses(positive_lambda)
        models = 0
        for mask in range(1 << 19):
            models += eval_cnf(clauses, mask)
            full_source_assignments += 1
        assert models == expected
        assertions += 1

    out = {
        "artifact": "KROM_PROJECTION_CEILING99",
        "status": "COMPUTATIONAL finite verification; symbolic theorem separate",
        "core_rows": rows,
        "random_2cnf_projection_instances": projection_instances,
        "random_projection_boundary_assignments": projection_assignments,
        "role4_source_count_rows": source_rows,
        "full_p1_source_assignments": full_source_assignments,
        "boundary_core_assignments": boundary_assignments,
        "assertions": assertions,
        "failures": 0,
        "proved_scope": "existential projections of 2-CNF have auxiliary-free 2-CNF of at most 2s^2 clauses; Role4 family requires Theta(s^2)",
    }
    path = Path(__file__).resolve().parents[2] / "results/raw/review/KROM_PROJECTION_CEILING99_raw.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
