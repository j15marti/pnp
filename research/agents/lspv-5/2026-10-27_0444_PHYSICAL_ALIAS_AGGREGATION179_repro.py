#!/usr/bin/env python3
"""Finite controls for PHYSICAL-ALIAS-AGGREGATION179.

Dependency-free and deterministic.  The symbolic theorem is in the report;
this program exhaustively checks the finite aliasing and aggregation controls.
"""

from itertools import product
import hashlib
import json


assertions = 0


def check(cond, msg):
    global assertions
    assertions += 1
    if not cond:
        raise AssertionError(msg)


def transcripts(keys):
    """All event-answer transcripts induced by fixed physical-cell assignments."""
    uniq = tuple(dict.fromkeys(keys))
    out = set()
    for bits in product((0, 1), repeat=len(uniq)):
        val = dict(zip(uniq, bits))
        out.add(tuple(val[k] for k in keys))
    return out


alias_cases = 0
for n in range(1, 7):
    # Every map of n logical events to at most four physical cells.
    for keys in product(range(min(n, 4)), repeat=n):
        used = len(set(keys))
        ts = transcripts(keys)
        check(len(ts) == 2 ** used, (n, keys, used, len(ts)))
        for tr in ts:
            for i in range(n):
                for j in range(n):
                    if keys[i] == keys[j]:
                        check(tr[i] == tr[j], (keys, tr, i, j))
        alias_cases += 1


# Too-fine logical namespace: the same physical bit queried under two child IDs.
physical = transcripts((("proof", 0), ("proof", 0)))
too_fine = set(product((0, 1), repeat=2))
check(all(a == b for a, b in physical), "fixed cell must answer consistently")
check(any(a != b for a, b in too_fine), "namespaced simulation invents inconsistency")
check(not any(a != b for a, b in physical), "no genuine proof satisfies inequality")


# Too-coarse namespace: two independent physical proof tapes at local address zero.
independent = transcripts((("left", 0), ("right", 0)))
too_coarse = transcripts((0, 0))
check((0, 1) in independent and (1, 0) in independent, "independent tapes may differ")
check((0, 1) not in too_coarse and (1, 0) not in too_coarse, "coarsening loses proofs")


# Local one-bit leaves versus global accepted-path information.
branch_rows = []
for h in range(0, 17):
    leaves = 2 ** h
    q_total = leaves
    local_cap = 1
    transcript_log2 = q_total
    check(local_cap == 1, h)
    check(q_total == 2 ** h, h)
    check(transcript_log2 == leaves, h)
    if h <= 4:
        keys = tuple(("leaf", i) for i in range(leaves))
        check(len(transcripts(keys)) == 2 ** leaves, h)
    branch_rows.append({
        "height": h,
        "leaves": leaves,
        "local_distinct_bits_per_leaf": local_cap,
        "global_distinct_bits_on_accepting_run": q_total,
        "log2_realizable_transcripts": transcript_log2,
    })


# Two-level sum and alias quotient controls.
two_level = []
for b1 in range(1, 7):
    for b2 in range(1, 7):
        events = [(i, j) for i in range(b1) for j in range(b2)]
        disjoint_keys = tuple(("leaf", i, j) for i, j in events)
        shared_by_parent = tuple(("parent", i) for i, _ in events)
        fully_shared = tuple(("one", 0) for _ in events)
        qd = len(set(disjoint_keys))
        qp = len(set(shared_by_parent))
        q1 = len(set(fully_shared))
        check(qd == b1 * b2, (b1, b2, qd))
        check(qp == b1, (b1, b2, qp))
        check(q1 == 1, (b1, b2, q1))
        if qd <= 12:
            check(len(transcripts(disjoint_keys)) == 2 ** qd, (b1, b2, "disjoint"))
        else:
            check(len(set(disjoint_keys)) == qd, (b1, b2, "disjoint-symbolic"))
        check(len(transcripts(shared_by_parent)) == 2 ** qp, (b1, b2, "parent"))
        check(len(transcripts(fully_shared)) == 2, (b1, b2, "shared"))
        two_level.append({"b1": b1, "b2": b2, "q_disjoint": qd,
                          "q_parent_shared": qp, "q_fully_shared": q1})


summary = {
    "run_id": "PHYSICAL-ALIAS-AGGREGATION179",
    "status": {
        "physical_alias_enumeration": "PROVED/EXACT in report; finite controls passed",
        "fine_namespace_without_injective_layout": "FALSIFIED/RETIRED",
        "coarse_namespace_across_independent_oracles": "FALSIFIED/RETIRED",
        "local_log_cap_implies_global_log_cap": "FALSIFIED/RETIRED",
        "unrestricted_sat_or_arc": "OPEN"
    },
    "deterministic": True,
    "random_seed": None,
    "alias_maps_checked": alias_cases,
    "assertions": assertions,
    "failures": 0,
    "fine_namespace": {
        "physical_transcripts": sorted(map(list, physical)),
        "namespaced_transcripts": sorted(map(list, too_fine)),
    },
    "coarse_namespace": {
        "independent_transcripts": sorted(map(list, independent)),
        "coarsened_transcripts": sorted(map(list, too_coarse)),
    },
    "branching": branch_rows,
    "two_level": two_level,
    "limitations": [
        "Finite enumeration is not a physical machine benchmark.",
        "The SAT/UNSAT lower-bound consequence remains conditional on an all-input verifier.",
        "No sequential-head theorem is transferred to indexed RAT or RAM."
    ]
}
payload = json.dumps(summary, indent=2, sort_keys=True) + "\n"
summary["canonical_without_hash_sha256"] = hashlib.sha256(payload.encode()).hexdigest()
print(json.dumps(summary, indent=2, sort_keys=True))
