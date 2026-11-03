#!/usr/bin/env python3
"""REFEREE312: exact weighted CNF bases for all three-variable factors."""

from __future__ import annotations

import hashlib
import itertools
import json
import resource
import sys
import time
from collections import Counter
from pathlib import Path

VARS = (1, 2, 3)
FULL = 255
WEIGHT = {1: 3, 2: 4, 3: 6}


def canon(clause):
    out = tuple(sorted(set(clause), key=lambda x: (abs(x), x < 0)))
    if any(x == 0 or -x in out for x in out):
        raise ValueError("noncanonical clause")
    return out


def clause_true(clause, assignment):
    return any(bool((assignment >> (abs(lit) - 1)) & 1) == (lit > 0) for lit in clause)


def clause_mask(clause):
    return sum(1 << a for a in range(8) if clause_true(clause, a))


def all_clauses():
    result = []
    for digits in itertools.product((0, 1, -1), repeat=3):
        if not any(digits):
            continue
        result.append(canon(d * (i + 1) for i, d in enumerate(digits) if d))
    result = sorted(set(result), key=lambda c: (len(c), c))
    assert len(result) == 26
    return result


def minimum_basis(mask, clauses, masks):
    if mask == 0:
        return 7, (), "early_contradiction"
    dp = {FULL: (0, ())}
    for i, clause in enumerate(clauses):
        if mask & ~masks[i]:
            continue
        nxt = dict(dp)
        for current, (cost, basis) in dp.items():
            new_mask = current & masks[i]
            new_cost = cost + WEIGHT[len(clause)]
            old = nxt.get(new_mask)
            candidate = basis + (i,)
            if old is None or (new_cost, candidate) < old:
                nxt[new_mask] = (new_cost, candidate)
        dp = nxt
    cost, basis = dp[mask]
    return cost, basis, "exact_cnf_basis"


def resolve(left, right, pivot):
    left, right = canon(left), canon(right)
    if pivot not in left or -pivot not in right:
        raise ValueError("bad pivot")
    raw = (set(left) - {pivot}) | (set(right) - {-pivot})
    return canon(raw)


def gate_slots(out, left, right):
    return canon((-out, left)), canon((-out, right)), canon((out, -left, -right))


def weaken_one_literal(base, target, first_fresh):
    base, target = canon(base), canon(target)
    if len(base) != 2 or len(target) != 3 or not set(base) < set(target):
        raise ValueError("expected binary-to-ternary weakening")
    added = next(x for x in target if x not in base)
    w = -added
    defs, res = [], []
    q_entries = []
    fresh = first_fresh
    for lit in base:
        q = fresh
        fresh += 1
        slots = gate_slots(q, -lit, w)
        defs.append({"out": q, "left": -lit, "right": w,
                     "slots": [list(c) for c in slots]})
        q_entries.append((lit, q, slots))
    current = base
    for lit, q, slots in q_entries:
        child = resolve(current, slots[0], lit)
        res.append({"left": list(current), "right": list(slots[0]),
                    "pivot": lit, "out": list(child)})
        current = child
    for lit, q, slots in q_entries:
        child = resolve(current, slots[2], -q)
        res.append({"left": list(current), "right": list(slots[2]),
                    "pivot": -q, "out": list(child)})
        current = child
    assert current == target and len(defs) + len(res) == 6
    return {"base": list(base), "target": list(target), "defs": defs, "res": res, "cost": 6}


def unique_zero_source():
    source = []
    for x, y in itertools.combinations(VARS, 2):
        source.extend((canon((-x, -y)), canon((-x, y)), canon((x, -y))))
    source = tuple(sorted(set(source)))
    models = [a for a in range(8) if all(clause_true(c, a) for c in source)]
    assert models == [0]
    return source


def parse_record(obj):
    if not isinstance(obj, dict) or set(obj) != {"mask", "basis"}:
        raise ValueError("schema")
    mask, basis = obj["mask"], obj["basis"]
    if not isinstance(mask, int) or isinstance(mask, bool) or not 0 <= mask <= 255:
        raise ValueError("mask")
    if not isinstance(basis, list):
        raise ValueError("basis")
    parsed = []
    for clause in basis:
        if not isinstance(clause, list) or not clause:
            raise ValueError("clause")
        if not all(isinstance(x, int) and not isinstance(x, bool) and 1 <= abs(x) <= 3 for x in clause):
            raise ValueError("literal")
        c = canon(clause)
        if list(c) != clause:
            raise ValueError("order/duplicate")
        parsed.append(c)
    if len(set(parsed)) != len(parsed):
        raise ValueError("duplicate clause")
    return mask, tuple(parsed)


def main():
    started = time.perf_counter()
    clauses = all_clauses()
    masks = [clause_mask(c) for c in clauses]
    records, cost_hist, clause_count_hist = [], Counter(), Counter()
    maxima = []
    max_cost = -1
    for mask in range(256):
        cost, basis_ids, mode = minimum_basis(mask, clauses, masks)
        basis = [clauses[i] for i in basis_ids]
        if mask:
            represented = FULL
            for i in basis_ids:
                assert not (mask & ~masks[i])
                represented &= masks[i]
            assert represented == mask
        cost_hist[cost] += 1
        clause_count_hist[len(basis)] += 1
        record = {"mask": mask, "models": mask.bit_count(), "mode": mode,
                  "cost": cost, "basis": [list(c) for c in basis]}
        records.append(record)
        if cost > max_cost:
            max_cost, maxima = cost, [mask]
        elif cost == max_cost:
            maxima.append(mask)
    assert max_cost == 24 and maxima == [105, 150]
    assert max(len(r["basis"]) for r in records) == 4

    pair_hist = Counter()
    pair_count = pair_max_count = 0
    for source_mask in range(256):
        for output_mask in range(256):
            if source_mask & ~output_mask:
                continue
            pair_count += 1
            cost = 7 if source_mask == 0 else records[output_mask]["cost"]
            pair_hist[cost] += 1
            if cost == 24:
                pair_max_count += 1
    assert pair_count == 6561 and pair_max_count == 30

    even_mask = sum(1 << a for a in range(8) if a.bit_count() % 2 == 0)
    odd_mask = FULL ^ even_mask
    assert (even_mask, odd_mask) == (105, 150)
    assert records[even_mask]["cost"] == records[odd_mask]["cost"] == 24

    source = unique_zero_source()
    even_basis = [tuple(c) for c in records[even_mask]["basis"]]
    certs = []
    fresh = 4
    for target in even_basis:
        falsifier = next(a for a in range(8) if not clause_true(target, a))
        candidates = [c for c in source if not clause_true(c, falsifier) and set(c) < set(target)]
        assert candidates
        cert = weaken_one_literal(candidates[0], target, fresh)
        fresh += 2
        certs.append({"falsifying_assignment": falsifier, **cert})
    assert sum(c["cost"] for c in certs) == 24

    false_proof = {"sources": [[1], [-1]], "nodes": [
        {"left_id": 0, "right_id": 1, "pivot": 1, "out": []}
    ], "root_id": 2, "cost": 1}

    malformed = [
        None, {}, {"mask": -1, "basis": []}, {"mask": 256, "basis": []},
        {"mask": True, "basis": []}, {"mask": 1.0, "basis": []},
        {"mask": 1, "basis": None}, {"mask": 1, "basis": [[]]},
        {"mask": 1, "basis": [[0]]}, {"mask": 1, "basis": [[1, -1]]},
        {"mask": 1, "basis": [[2, 1]]}, {"mask": 1, "basis": [[1], [1]]},
    ]
    rejected = 0
    for obj in malformed:
        try:
            parse_record(obj)
        except ValueError:
            rejected += 1
    assert rejected == 12
    assert parse_record({"mask": even_mask, "basis": records[even_mask]["basis"]})[0] == even_mask

    elapsed = time.perf_counter() - started
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    result = {
        "run_id": "SEMANTIC-CNF-BASIS-COMPILER-REFEREE312",
        "date_pst": "2026-11-03 04:48 PST",
        "calculus": "unchanged Rmix341; E=strict RES plus paid source-independent signed two-input VARDEF; L3 explicit factors on at most three common names",
        "status": {
            "proved_restricted": [
                "Every nonfalse three-variable Boolean relation has an exact auxiliary-free CNF basis of weighted clause-compilation cost at most 24.",
                "Only the even and odd parity relations attain weighted basis cost 24.",
                "Replacing every explicit L3 factor label by its exact basis improves the restricted simulation coefficient from 42 to 24."
            ],
            "computational": "Complete dynamic program over all 256 relations and all 26 nonempty nontautological clauses.",
            "open": ["cross-clause proof sharing below 24", "global XOR/circuit LOCAL-CONVERT", "B1", "B2", "B3", "superpolynomial Wbar", "P versus NP"]
        },
        "weights": {"width_1": 3, "width_2": 4, "width_3": 6, "false_factor_early_contradiction": 7},
        "theorem": {"prior_coefficient": 42, "new_coefficient": 24,
                    "formula": "W_L3(F) <= W_E(F) <= 24 W_L3(F) + O(1)"},
        "clause_catalog": [{"id": i, "clause": list(c), "mask": masks[i], "weight": WEIGHT[len(c)]}
                           for i, c in enumerate(clauses)],
        "relations": records,
        "summary": {
            "relation_count": 256,
            "cost_histogram": dict(sorted(cost_hist.items())),
            "basis_clause_count_histogram": dict(sorted(clause_count_hist.items())),
            "max_cost": max_cost,
            "max_cost_masks": maxima,
            "entailed_relation_pairs": pair_count,
            "max_cost_pair_count": pair_max_count,
            "pair_cost_histogram": dict(sorted(pair_hist.items()))
        },
        "explicit_24_node_control": {
            "source": [list(c) for c in source], "source_models": [0],
            "output_mask": even_mask, "basis": [list(c) for c in even_basis],
            "certificates": certs, "total_cost": 24
        },
        "false_factor_control": false_proof,
        "both_label_controls": {
            "even_parity_mask": even_mask, "odd_parity_mask": odd_mask,
            "even_models": even_mask.bit_count(), "odd_models": odd_mask.bit_count(),
            "even_entails_odd": False, "odd_entails_even": False,
            "both_weighted_basis_cost": 24
        },
        "malformed": {"rejected": rejected, "valid": 1},
        "work_ledger": {
            "producer_wall_seconds": elapsed, "producer_peak_rss_kib_linux": rss,
            "logical_cost": "basis clause bounds and paid DAG nodes; optimal-path/basis discovery excluded from W",
            "machine_warning": "DP, semantic table access, parsing, serialization, checking, scheduling and host memory are separately charged machine resources."
        }
    }
    out = Path("results/raw/arc/lspv5_312/semantic_cnf_basis_compiler_referee312.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    out.write_text(payload, encoding="utf-8")
    digest = hashlib.sha256(payload.encode()).hexdigest()
    print(json.dumps({"status": "PASS", "relations": 256, "pairs": pair_count,
                      "max_cost": max_cost, "max_masks": maxima,
                      "explicit_cost": 24, "malformed_rejected": rejected,
                      "raw_sha256": digest, "wall_seconds": elapsed,
                      "peak_rss_kib": rss}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "error": repr(exc)}), file=sys.stderr)
        raise
