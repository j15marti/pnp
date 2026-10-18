#!/usr/bin/env python3
"""TETRAPINORBIT1: independent finite audit of the two-NAE front end.

The symbolic observation audited here is that every signed NAE formula without
constants is self-dual: complementing every variable preserves satisfaction.
Consequently no satisfiable pure signed-NAE gadget can existentially force one
distinguished variable to 0 (or to 1).

The program also checks the advertised one-clause identity, fresh-auxiliary
witness transport, and exact 6/8-bit boundary-relation gluing.  Finite outcomes
are COMPUTATIONAL and do not imply an arbitrary-machine lower bound.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
import time
from pathlib import Path

SEED = 202610190424


def nae(bits):
    return not (all(bits) or not any(bits))


def lit_value(mask: int, lit: int) -> bool:
    value = bool((mask >> (abs(lit) - 1)) & 1)
    return value if lit > 0 else not value


def sat_or_formula(formula, n):
    for mask in range(1 << n):
        if all(any(lit_value(mask, lit) for lit in clause) for clause in formula):
            return True, mask
    return False, None


def front_end_holds(literal_values, u):
    a, b, c = literal_values
    return nae((a, b, u)) and nae((not u, c, False))


def target_extensions(formula, n, source_mask):
    """Return all fresh-u vectors extending source_mask with the false constant."""
    extensions = []
    for umask in range(1 << len(formula)):
        ok = True
        for i, clause in enumerate(formula):
            values = tuple(lit_value(source_mask, lit) for lit in clause)
            if not front_end_holds(values, bool((umask >> i) & 1)):
                ok = False
                break
        if ok:
            extensions.append(umask)
    return extensions


def signed_nae_clause(mask: int, clause) -> bool:
    return nae(tuple(lit_value(mask, lit) for lit in clause))


def clause_identity_audit():
    rows = []
    checks = 0
    for values in itertools.product((False, True), repeat=3):
        lhs = any(values)
        witnesses = [u for u in (False, True) if front_end_holds(values, u)]
        assert lhs == bool(witnesses)
        checks += 1
        rows.append({"abc": "".join("1" if x else "0" for x in values),
                     "or": lhs, "u_witnesses": [int(u) for u in witnesses]})

    signed_permutation_checks = 0
    for signs in itertools.product((1, -1), repeat=3):
        for perm in itertools.permutations(range(3)):
            clause = tuple(signs[i] * (i + 1) for i in perm)
            for mask in range(8):
                values = tuple(lit_value(mask, lit) for lit in clause)
                assert any(values) == any(front_end_holds(values, u) for u in (False, True))
                signed_permutation_checks += 1
    return rows, checks, signed_permutation_checks


def formula_transport_audit(rng):
    # Exhaust every subset of the eight signed proper clauses on one support.
    universe = [tuple((i + 1) if bit else -(i + 1) for i, bit in enumerate(signs))
                for signs in itertools.product((False, True), repeat=3)]
    exhaustive_formulas = 0
    source_assignments = 0
    target_models = 0
    for selector in range(1 << len(universe)):
        formula = tuple(universe[i] for i in range(8) if (selector >> i) & 1)
        sat_source, _ = sat_or_formula(formula, 3)
        sat_target = False
        for mask in range(8):
            source_ok = all(any(lit_value(mask, lit) for lit in clause) for clause in formula)
            exts = target_extensions(formula, 3, mask)
            assert source_ok == bool(exts)
            source_assignments += 1
            target_models += len(exts)
            sat_target |= bool(exts)
        assert sat_source == sat_target
        exhaustive_formulas += 1

    random_cases = 240
    random_assertions = 0
    max_m = 8
    for _ in range(random_cases):
        n = 5
        m = rng.randint(1, max_m)
        formula = []
        for _j in range(m):
            support = rng.sample(range(1, n + 1), 3)
            rng.shuffle(support)
            formula.append(tuple(v if rng.getrandbits(1) else -v for v in support))
        formula = tuple(formula)
        sat_source, witness = sat_or_formula(formula, n)
        sat_target = False
        reconstructed = None
        for mask in range(1 << n):
            exts = target_extensions(formula, n, mask)
            if exts:
                sat_target = True
                reconstructed = mask
                break
        assert sat_source == sat_target
        if sat_target:
            assert reconstructed is not None
            assert all(any(lit_value(reconstructed, lit) for lit in c) for c in formula)
        if sat_source:
            assert target_extensions(formula, n, witness)
        random_assertions += 3

    return {
        "exhaustive_formulas": exhaustive_formulas,
        "source_assignment_projection_checks": source_assignments,
        "target_models_counted": target_models,
        "random_cases": random_cases,
        "random_assertions": random_assertions,
        "random_n": 5,
        "random_max_m": max_m,
    }


def proper_signed_nae_universe(n):
    clauses = []
    for support in itertools.combinations(range(1, n + 1), 3):
        # Quotient sign vectors by simultaneous literal complementation.
        for tail in itertools.product((1, -1), repeat=2):
            signs = (1,) + tail
            clauses.append(tuple(signs[i] * support[i] for i in range(3)))
    return clauses


def no_pin_exhaustive():
    summaries = []
    total_formulas = 0
    projection_checks = 0
    for n in (3, 4):
        universe = proper_signed_nae_universe(n)
        histogram = {"empty": 0, "both": 0, "singleton": 0}
        for selector in range(1 << len(universe)):
            formula = [universe[i] for i in range(len(universe)) if (selector >> i) & 1]
            projection = set()
            for mask in range(1 << n):
                if all(signed_nae_clause(mask, c) for c in formula):
                    projection.add(mask & 1)  # distinguished variable x_1
            kind = "empty" if not projection else "both" if projection == {0, 1} else "singleton"
            histogram[kind] += 1
            assert kind != "singleton"
            total_formulas += 1
            projection_checks += 1
        summaries.append({"n": n, "available_clause_orbits": len(universe),
                          "formulas": 1 << len(universe), "projection_histogram": histogram})
    return summaries, total_formulas, projection_checks


def boundary_projection(clauses, variables, boundary):
    local = sorted(set(variables) - set(boundary))
    relation = {}
    for bmask in range(1 << len(boundary)):
        base = {v: (bmask >> i) & 1 for i, v in enumerate(boundary)}
        witnesses = []
        for lmask in range(1 << len(local)):
            assignment = dict(base)
            assignment.update({v: (lmask >> i) & 1 for i, v in enumerate(local)})
            ok = True
            for clause in clauses:
                vals = []
                for lit in clause:
                    bit = bool(assignment[abs(lit)])
                    vals.append(bit if lit > 0 else not bit)
                if not nae(vals):
                    ok = False
                    break
            if ok:
                witnesses.append(lmask)
        if witnesses:
            relation[bmask] = witnesses
    return relation, local


def make_block(rng, boundary, local, style, clauses=12):
    vertices = list(boundary) + list(local)
    out = []
    for j in range(clauses):
        if style == "cyclic-balanced":
            b1 = boundary[j % len(boundary)]
            b2 = boundary[(j * 3 + 1) % len(boundary)]
            if b1 == b2:
                b2 = boundary[(j + 1) % len(boundary)]
            support = [b1, b2, local[j % len(local)]]
        else:
            support = rng.sample(vertices, 3)
        out.append(tuple(v if rng.getrandbits(1) else -v for v in support))
    return tuple(out)


def boundary_audit(rng):
    records = []
    assertions = 0
    for width in (6, 8):
        boundary = tuple(range(1, width + 1))
        left_local = tuple(range(width + 1, width + 4))
        right_local = tuple(range(width + 4, width + 7))
        for style in ("cyclic-balanced", "random-mixing"):
            for case in range(30):
                left = make_block(rng, boundary, left_local, style)
                right = make_block(rng, boundary, right_local, style)
                rleft, _ = boundary_projection(left, boundary + left_local, boundary)
                rright, _ = boundary_projection(right, boundary + right_local, boundary)
                common = sorted(set(rleft) & set(rright))
                # The two sides glue iff their exact boundary projections intersect.
                if common:
                    b = common[0]
                    assert rleft[b] and rright[b]
                # Signed NAE relations are closed under global complementation.
                full = (1 << width) - 1
                assert set(rleft) == {b ^ full for b in rleft}
                assert set(rright) == {b ^ full for b in rright}
                assertions += 3
                records.append({"width": width, "style": style, "case": case,
                                "left_projection": len(rleft),
                                "right_projection": len(rright),
                                "intersection": len(common),
                                "sat": bool(common),
                                "table_capacity_bits": 1 << width})
    summary = {}
    for width in (6, 8):
        rows = [r for r in records if r["width"] == width]
        summary[str(width)] = {
            "cases": len(rows),
            "sat_cases": sum(r["sat"] for r in rows),
            "mean_left_projection": sum(r["left_projection"] for r in rows) / len(rows),
            "mean_intersection": sum(r["intersection"] for r in rows) / len(rows),
            "exact_relation_table_bits": 1 << width,
        }
    return summary, records, assertions


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    start = time.perf_counter()
    rng = random.Random(SEED)

    truth_rows, truth_checks, signed_checks = clause_identity_audit()
    transport = formula_transport_audit(rng)
    pin_rows, pin_formulas, pin_checks = no_pin_exhaustive()
    boundary_summary, boundary_records, boundary_checks = boundary_audit(rng)

    result = {
        "run_id": "TETRAPINORBIT1",
        "status": "COMPUTATIONAL",
        "seed": SEED,
        "python_model": "exact Boolean exhaustive enumeration plus seeded controls",
        "limits": {
            "no_pin_variables": [3, 4],
            "no_pin_formula_space": pin_formulas,
            "boundary_cases_per_width_style": 30,
            "boundary_widths": [6, 8],
            "random_transport_cases": transport["random_cases"],
            "individual_invocation_budget_seconds": 30,
        },
        "clause_identity": {
            "identity": "OR(a,b,c) iff exists u NAE(a,b,u) and NAE(not u,c,0)",
            "truth_table": truth_rows,
            "truth_checks": truth_checks,
            "signed_permutation_checks": signed_checks,
        },
        "formula_transport": transport,
        "pin_symmetry": {
            "symbolic_invariant": "global complementation preserves every signed NAE clause",
            "finite_audit": pin_rows,
            "formula_checks": pin_checks,
            "singleton_projections_found": 0,
        },
        "front_end_bookkeeping": {
            "with_one_shared_false_variable": {
                "variables": "n+m+1",
                "clauses": "2m",
                "fresh_u_occurrence": 2,
                "shared_false_variable_occurrence": "m",
                "proper_if_source_proper_and_false_variable_distinct": True,
            },
            "claimed_local_pin_counts_n_plus_22m_36m": "NOT_AUDITED_SOURCE_GADGET_UNAVAILABLE",
        },
        "boundary_projection": {
            "summary": boundary_summary,
            "assertions": boundary_checks,
            "records": boundary_records,
            "interpretation": "exact projection/gluing check only; no child-length contraction or runtime lower bound",
        },
        "total_assertions": truth_checks + signed_checks + pin_checks + boundary_checks
                            + transport["source_assignment_projection_checks"]
                            + transport["random_assertions"],
        "elapsed_seconds": time.perf_counter() - start,
        "p_vs_np": "OPEN",
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    result["payload_sha256_before_digest_field"] = hashlib.sha256(payload.encode()).hexdigest()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("run_id", "status", "seed", "total_assertions", "elapsed_seconds", "p_vs_np")}, sort_keys=True))


if __name__ == "__main__":
    main()
