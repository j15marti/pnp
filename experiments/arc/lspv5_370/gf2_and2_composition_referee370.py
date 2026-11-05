#!/usr/bin/env python3
"""REFEREE370: strict GF(2) row composition and degenerate AND2 elimination.

This is an independent finite audit of the restricted X(K) compiler used by
LSPV-1/425.  It is not the authoritative historical R_mix341 checker.

Part A exhausts every ordered pair of signed GF(2) rows on five variables and
constructs the advertised strict-Resolution tree for every output blocker.
Part B exhausts strict Resolution inferences over four variables and checks
that eliminating z <-> (a AND b) remains locally simulable when a,b are equal
or complementary signed literals, as well as when they are distinct.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import resource
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "results/raw/arc/2026-11-05_1348_LSPV5_REFEREE370_raw.json"


def canon_clause(lits):
    out = set(int(x) for x in lits)
    if 0 in out:
        raise ValueError("zero literal")
    if any(-x in out for x in out):
        return None
    return tuple(sorted(out, key=lambda x: (abs(x), x < 0)))


def strict_resolve(left, right, pivot):
    if pivot not in left or -pivot not in right:
        raise ValueError("oriented pivot absent")
    a = set(left) - {pivot}
    b = set(right) - {-pivot}
    if any(-x in b for x in a):
        raise ValueError("nonpivot complementary pair")
    return canon_clause(a | b)


def assignments(variables):
    variables = tuple(variables)
    for bits in itertools.product((0, 1), repeat=len(variables)):
        yield dict(zip(variables, bits))


def blocker(support, assignment):
    return canon_clause(v if assignment[v] == 0 else -v for v in support)


def violates(mask, rhs, assignment):
    parity = 0
    for v in range(1, 6):
        if mask & (1 << (v - 1)):
            parity ^= assignment[v]
    return parity != rhs


def support(mask):
    return tuple(v for v in range(1, 6) if mask & (1 << (v - 1)))


def compile_output_blocker(mask_a, rhs_a, mask_b, rhs_b, tau):
    sa, sb = set(support(mask_a)), set(support(mask_b))
    inter = tuple(sorted(sa & sb))
    diff = tuple(sorted(sa ^ sb))
    target = blocker(diff, tau)
    level = {}
    leaf_sources = {"A": 0, "B": 0}
    for u in assignments(inter):
        full = dict(tau)
        full.update(u)
        af = violates(mask_a, rhs_a, full)
        bf = violates(mask_b, rhs_b, full)
        if af == bf:
            raise AssertionError("sum violation must falsify exactly one parent row")
        tag, mask, rhs = ("A", mask_a, rhs_a) if af else ("B", mask_b, rhs_b)
        leaf_sources[tag] += 1
        level[tuple(u[v] for v in inter)] = blocker(support(mask), full)

    steps = []
    keys_vars = list(inter)
    while keys_vars:
        pivot = keys_vars[-1]
        next_level = {}
        prefixes = sorted({key[:-1] for key in level})
        for pre in prefixes:
            c0, c1 = level[pre + (0,)], level[pre + (1,)]
            got = strict_resolve(c0, c1, pivot)
            steps.append({"pivot": pivot, "left": c0, "right": c1, "out": got})
            next_level[pre] = got
        level = next_level
        keys_vars.pop()
    final = level[()]
    if not set(final).issubset(target):
        raise AssertionError("compiled clause is not a target subclause")
    if len(steps) > (1 << len(inter)) - 1:
        raise AssertionError("strict tree exceeds 2^t-1")
    return final, target, steps, leaf_sources


def gf2_audit():
    ordered_pairs = output_blockers = strict_steps = 0
    max_steps = max_t = max_r = 0
    exact_outputs = proper_subclauses = 0
    leaf_source_counts = {"A": 0, "B": 0}
    example = None
    for mask_a in range(32):
        for rhs_a in (0, 1):
            for mask_b in range(32):
                for rhs_b in (0, 1):
                    ordered_pairs += 1
                    out_mask, out_rhs = mask_a ^ mask_b, rhs_a ^ rhs_b
                    out_support = support(out_mask)
                    t = (mask_a & mask_b).bit_count()
                    r = out_mask.bit_count()
                    max_t, max_r = max(max_t, t), max(max_r, r)
                    for tau in assignments(out_support):
                        if not violates(out_mask, out_rhs, tau):
                            continue
                        final, target, steps, leaves = compile_output_blocker(
                            mask_a, rhs_a, mask_b, rhs_b, tau
                        )
                        output_blockers += 1
                        strict_steps += len(steps)
                        max_steps = max(max_steps, len(steps))
                        for k in leaf_source_counts:
                            leaf_source_counts[k] += leaves[k]
                        if final == target:
                            exact_outputs += 1
                        else:
                            proper_subclauses += 1
                        if example is None and t == 2 and r == 2 and steps:
                            example = {
                                "mask_a": mask_a,
                                "rhs_a": rhs_a,
                                "mask_b": mask_b,
                                "rhs_b": rhs_b,
                                "intersection": sorted(set(support(mask_a)) & set(support(mask_b))),
                                "difference": list(out_support),
                                "target": list(target),
                                "final": list(final),
                                "strict_steps": len(steps),
                            }
    return {
        "variables": 5,
        "signed_rows": 64,
        "ordered_pairs": ordered_pairs,
        "output_blockers": output_blockers,
        "strict_resolution_steps_constructed": strict_steps,
        "maximum_intersection_t": max_t,
        "maximum_difference_r": max_r,
        "maximum_steps_for_one_blocker": max_steps,
        "bound_at_maximum_t": (1 << max_t) - 1,
        "exact_output_blockers": exact_outputs,
        "proper_subclause_outputs": proper_subclauses,
        "leaf_source_counts": leaf_source_counts,
        "example": example,
    }


def all_clauses(variables):
    for choices in itertools.product((-1, 0, 1), repeat=len(variables)):
        # -1 = negative literal, 0 = absent, 1 = positive literal.
        yield canon_clause(s * v for s, v in zip(choices, variables) if s)


def substitute_and2(clause, a, b, z=3):
    if clause is None:
        return ()
    if abs(a) == z or abs(b) == z:
        raise ValueError("output cannot be its own input")
    if z in clause:
        rest = set(clause) - {z}
        candidates = [canon_clause(rest | {a}), canon_clause(rest | {b})]
    elif -z in clause:
        rest = set(clause) - {-z}
        candidates = [canon_clause(rest | {-a, -b})]
    else:
        candidates = [clause]
    return tuple(sorted({c for c in candidates if c is not None}, key=lambda c: (len(c), c)))


def closure_with_depth(initial, variables=(1, 2, 4)):
    depth = {c: 0 for c in initial}
    changed = True
    while changed:
        changed = False
        clauses = list(depth)
        for left in clauses:
            for right in clauses:
                for p in variables:
                    if p not in left or -p not in right:
                        continue
                    try:
                        out = strict_resolve(left, right, p)
                    except ValueError:
                        continue
                    d = 1 + max(depth[left], depth[right])
                    if out not in depth or d < depth[out]:
                        depth[out] = d
                        changed = True
    return depth


def gate_audit():
    variables = (1, 2, 3, 4)
    clauses = tuple(all_clauses(variables))
    signed_inputs = (1, -1, 2, -2)
    pair_classes = {"identical": 0, "complementary": 0, "distinct": 0}
    inferences_by_class = {k: 0 for k in pair_classes}
    target_obligations = {k: 0 for k in pair_classes}
    max_depth = {k: 0 for k in pair_classes}
    failures = []
    facet_checks = 0

    original_inferences = []
    for pivot in variables:
        for left in clauses:
            if pivot not in left:
                continue
            for right in clauses:
                if -pivot not in right:
                    continue
                try:
                    out = strict_resolve(left, right, pivot)
                except ValueError:
                    continue
                original_inferences.append((left, right, pivot, out))

    for a in signed_inputs:
        for b in signed_inputs:
            cls = "identical" if a == b else "complementary" if a == -b else "distinct"
            pair_classes[cls] += 1
            facets = ((-3, a), (-3, b), (3, -a, -b))
            for f in facets:
                facet_checks += 1
                if substitute_and2(canon_clause(f), a, b):
                    failures.append({"kind": "definition facet survived", "a": a, "b": b, "facet": f})
            for left, right, pivot, out in original_inferences:
                initial = set(substitute_and2(left, a, b)) | set(substitute_and2(right, a, b))
                goals = substitute_and2(out, a, b)
                closure = closure_with_depth(initial)
                inferences_by_class[cls] += 1
                for goal in goals:
                    target_obligations[cls] += 1
                    candidates = [(d, c) for c, d in closure.items() if set(c).issubset(goal)]
                    if not candidates:
                        failures.append({
                            "kind": "unreachable transformed resolvent",
                            "a": a, "b": b, "left": left, "right": right,
                            "pivot": pivot, "out": out, "goal": goal,
                        })
                    else:
                        max_depth[cls] = max(max_depth[cls], min(d for d, _ in candidates))

    # Focused malformed/corrupt controls.
    controls = {}
    try:
        strict_resolve((1, 2), (-1, -2), 1)
        controls["nonpivot_complement"] = "ACCEPTED"
    except ValueError:
        controls["nonpivot_complement"] = "REJECTED"
    try:
        substitute_and2((3,), 3, 1)
        controls["self_input"] = "ACCEPTED"
    except ValueError:
        controls["self_input"] = "REJECTED"
    forged_closure = closure_with_depth({(1, 4), (-1, 4)})
    controls["forged_negative_x4"] = "REJECTED" if not any(set(c).issubset({-4}) for c in forged_closure) else "ACCEPTED"

    if failures:
        raise AssertionError(f"gate audit failures: {failures[:3]}")
    return {
        "signed_input_pairs": 16,
        "pair_classes": pair_classes,
        "original_strict_inferences": len(original_inferences),
        "inferences_checked_by_class": inferences_by_class,
        "target_clause_obligations": target_obligations,
        "maximum_local_resolution_depth": max_depth,
        "definition_facets_eliminated_as_tautologies": facet_checks,
        "failures": 0,
        "controls": controls,
    }


def canonical_bytes(obj):
    return (json.dumps(obj, sort_keys=True, separators=(",", ":")) + "\n").encode()


def main():
    started = time.perf_counter()
    gf2 = gf2_audit()
    gate = gate_audit()
    payload = {
        "artifact": "REFEREE370",
        "status": "PASS",
        "scope": "restricted X(K) compiler audit; not authoritative R_mix341",
        "gf2": gf2,
        "and2_elimination": gate,
        "resource_ledger": {
            "construction_search_seconds": round(time.perf_counter() - started, 6),
            "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "logical_xor_trace": "not used",
            "offline_diagnostic": True,
        },
    }
    payload["content_sha256"] = hashlib.sha256(canonical_bytes(payload)).hexdigest()
    RAW.parent.mkdir(parents=True, exist_ok=True)
    RAW.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
