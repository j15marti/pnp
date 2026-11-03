#!/usr/bin/env python3
"""REFEREE314: source-aware three-variable factor-exit compiler."""

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


def canon(clause):
    out = tuple(sorted(set(clause), key=lambda x: (abs(x), x < 0)))
    if any(not isinstance(x, int) or isinstance(x, bool) or x == 0 or -x in out for x in out):
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


def unique_binary_source(assignment):
    result = []
    for x, y in itertools.combinations(VARS, 2):
        for sx, sy in itertools.product((-1, 1), repeat=2):
            clause = canon((sx * x, sy * y))
            if clause_true(clause, assignment):
                result.append(clause)
    result = tuple(sorted(set(result), key=lambda c: (len(c), c)))
    assert len(result) == 9
    assert [a for a in range(8) if all(clause_true(c, a) for c in result)] == [assignment]
    return result


def parity_basis(parity):
    result = []
    for a in range(8):
        if a.bit_count() % 2 == parity:
            continue
        result.append(canon(-(i + 1) if (a >> i) & 1 else i + 1 for i in range(3)))
    return tuple(sorted(result))


def resolve(left, right, pivot):
    left, right = canon(left), canon(right)
    if pivot not in left or -pivot not in right:
        raise ValueError("bad pivot")
    return canon((set(left) - {pivot}) | (set(right) - {-pivot}))


def gate_slots(out, left, right):
    return canon((-out, left)), canon((-out, right)), canon((out, -left, -right))


def weaken_one(base, target, fresh):
    base, target = canon(base), canon(target)
    if len(base) != 2 or len(target) != 3 or not set(base) < set(target):
        raise ValueError("expected binary-to-ternary weakening")
    added = next(x for x in target if x not in base)
    chosen = base[0]
    slots = gate_slots(fresh, -chosen, -added)
    first = resolve(base, slots[0], chosen)
    second = resolve(first, slots[2], -fresh)
    assert second == target
    return {
        "base": list(base), "target": list(target),
        "definition": {"out": fresh, "left": -chosen, "right": -added,
                       "slots": [list(c) for c in slots]},
        "resolutions": [
            {"left": list(base), "right": list(slots[0]), "pivot": chosen, "out": list(first)},
            {"left": list(first), "right": list(slots[2]), "pivot": -fresh, "out": list(second)},
        ],
        "cost": 3,
    }


def derive_unit(source, assignment, variable):
    literal = variable if (assignment >> (variable - 1)) & 1 else -variable
    other = next(v for v in VARS if v != variable)
    left, right = canon((literal, other)), canon((literal, -other))
    assert left in source and right in source
    out = resolve(left, right, other)
    assert out == (literal,)
    return {"sources": [list(left), list(right)], "pivot": other, "out": [literal], "cost": 1}


def strict_drop_basis(assignment):
    bit1, bit2 = assignment & 1, (assignment >> 1) & 1
    if bit1 == bit2:
        basis = (canon((-1, 2)), canon((1, -2)))
        relation = "x1_eq_x2"
    else:
        basis = (canon((1, 2)), canon((-1, -2)))
        relation = "x1_neq_x2"
    source = unique_binary_source(assignment)
    assert all(c in source for c in basis)
    expected = [a for a in range(8) if (((a & 1) ^ ((a >> 1) & 1)) == (bit1 ^ bit2))]
    actual = [a for a in range(8) if all(clause_true(c, a) for c in basis)]
    assert actual == expected
    return {"input_support": [1, 2, 3], "output_support": [1, 2],
            "relation": relation, "basis": [list(c) for c in basis],
            "models": actual, "paid_cost": 0}


def source_clause_charge(clause, assignment, source):
    clause = canon(clause)
    if not clause_true(clause, assignment):
        raise ValueError("not entailed by singleton source")
    if len(clause) == 2:
        assert clause in source
        return 0
    if len(clause) == 1:
        return 1
    assert len(clause) == 3
    assert any(set(base) < set(clause) for base in source)
    return 3


def minimum_recipe_basis(mask, assignment, clauses, masks, source):
    candidates = []
    for i, clause in enumerate(clauses):
        if clause_true(clause, assignment) and not (mask & ~masks[i] & FULL):
            candidates.append((i, source_clause_charge(clause, assignment, source)))
    dp = {FULL: (0, ())}
    for i, charge in candidates:
        nxt = dict(dp)
        for current, (cost, basis) in dp.items():
            new_mask = current & masks[i]
            candidate = (cost + charge, basis + (i,))
            if new_mask not in nxt or candidate < nxt[new_mask]:
                nxt[new_mask] = candidate
        dp = nxt
    if mask not in dp:
        raise AssertionError("no exact basis")
    return dp[mask]


def parse_record(obj):
    required = {"assignment", "source", "output_mask", "basis"}
    if not isinstance(obj, dict) or set(obj) != required:
        raise ValueError("schema")
    if not isinstance(obj["assignment"], int) or isinstance(obj["assignment"], bool) or not 0 <= obj["assignment"] < 8:
        raise ValueError("assignment")
    if not isinstance(obj["output_mask"], int) or isinstance(obj["output_mask"], bool) or not 0 <= obj["output_mask"] <= 255:
        raise ValueError("mask")
    for key in ("source", "basis"):
        if not isinstance(obj[key], list):
            raise ValueError("clauses")
        parsed = []
        for raw in obj[key]:
            if not isinstance(raw, list) or not raw:
                raise ValueError("clause")
            if any(not isinstance(x, int) or isinstance(x, bool) or not 1 <= abs(x) <= 3 for x in raw):
                raise ValueError("literal")
            clause = canon(raw)
            if list(clause) != raw:
                raise ValueError("canonical")
            parsed.append(clause)
        if len(set(parsed)) != len(parsed):
            raise ValueError("duplicate")
    return obj


def main():
    started = time.perf_counter()
    clauses = all_clauses()
    masks = [clause_mask(c) for c in clauses]
    parity_masks = {
        p: sum(1 << a for a in range(8) if a.bit_count() % 2 == p)
        for p in (0, 1)
    }
    assert parity_masks == {0: 105, 1: 150}

    records, global_hist, maxima = [], Counter(), []
    max_cost = -1
    exact_pairs = 0
    for assignment in range(8):
        source = unique_binary_source(assignment)
        relation_records = []
        for mask in range(256):
            if not (mask & (1 << assignment)):
                continue
            cost, ids = minimum_recipe_basis(mask, assignment, clauses, masks, source)
            basis = [clauses[i] for i in ids]
            represented = FULL
            paid = 0
            for clause in basis:
                represented &= clause_mask(clause)
                paid += source_clause_charge(clause, assignment, source)
            assert represented == mask and paid == cost
            exact_pairs += 1
            global_hist[cost] += 1
            relation_records.append([mask, cost])
            if cost > max_cost:
                max_cost, maxima = cost, [(assignment, mask)]
            elif cost == max_cost:
                maxima.append((assignment, mask))

        parity = assignment.bit_count() % 2
        targets = parity_basis(parity)
        certificates = []
        fresh = 4
        for target in targets:
            bases = [c for c in source if set(c) < set(target)]
            assert bases
            certificates.append(weaken_one(bases[0], target, fresh))
            fresh += 1
        assert sum(c["cost"] for c in certificates) == 12

        records.append({
            "assignment": assignment,
            "source": [list(c) for c in source],
            "source_models": [assignment],
            "matching_parity": parity,
            "matching_parity_mask": parity_masks[parity],
            "opposite_parity_mask": parity_masks[1 - parity],
            "matching_models_with_source": [assignment],
            "opposite_models_with_source": [],
            "relation_costs": relation_records,
            "parity_basis": [list(c) for c in targets],
            "parity_certificates": certificates,
            "parity_paid_cost": 12,
            "strict_support_drop": strict_drop_basis(assignment),
            "unit_demand": derive_unit(source, assignment, 1),
        })

    expected_maxima = [(a, parity_masks[a.bit_count() % 2]) for a in range(8)]
    assert exact_pairs == 1024
    assert max_cost == 12 and maxima == expected_maxima
    assert global_hist == Counter({0: 584, 3: 296, 6: 96, 9: 40, 12: 8})

    valid = {"assignment": 0, "source": records[0]["source"],
             "output_mask": 105, "basis": records[0]["parity_basis"]}
    assert parse_record(valid) == valid
    malformed = [
        None, {}, {**valid, "extra": 1}, {**valid, "assignment": -1},
        {**valid, "assignment": 8}, {**valid, "assignment": True},
        {**valid, "output_mask": 256}, {**valid, "source": None},
        {**valid, "source": [[]]}, {**valid, "source": [[0]]},
        {**valid, "basis": [[1, -1]]}, {**valid, "basis": [[1], [1]]},
    ]
    rejected = 0
    for obj in malformed:
        try:
            parse_record(obj)
        except ValueError:
            rejected += 1
    assert rejected == 12

    elapsed = time.perf_counter() - started
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    result = {
        "run_id": "SOURCE-AWARE-EXIT-COMPILER-REFEREE314",
        "date_pst": "2026-11-03 06:48 PST",
        "calculus": "unchanged Rmix341; E=strict binary RES plus unit-cost source-independent signed two-input AND VARDEF",
        "status": {
            "proved_restricted": [
                "For each polarity-renamed nine-binary-clause singleton source U_a and every three-variable relation Q containing a, an exact auxiliary-free Q basis is source-authenticated with recipe cost at most 12.",
                "The 12 bound is attained in the declared source-aware independent-clause recipe only by the parity relation containing a.",
                "A strict support drop from U_a to the matching x1/x2 equality-or-disequality factor reuses two original source clauses and costs zero paid nodes."
            ],
            "falsified": [
                "The REFEREE312 unique-000 parity control needs 24 paid nodes under legal E derivations; explicit source-aware proofs use 12.",
                "Every strict support drop necessarily incurs a paid inference node."
            ],
            "open": ["full-E minimum of the parity exit", "global L3 minimum-to-minimum coefficient below 24", "B1", "B2", "B3", "superpolynomial Wbar", "P versus NP"]
        },
        "theorem": {
            "source_family": "U_a contains all nine non-tautological binary clauses satisfied by assignment a",
            "per_clause_recipe_cost": {"source_binary": 0, "entailed_unit": 1, "entailed_ternary": 3},
            "maximum_exact_basis_recipe_cost": max_cost,
            "maximizers": [{"assignment": a, "mask": m} for a, m in maxima],
            "firewall": "The DP optimum is exact only for the declared independently compiled source-aware basis recipe, not for unrestricted shared E DAGs."
        },
        "summary": {
            "assignments": 8, "relations_per_assignment": 128,
            "exact_source_output_pairs": exact_pairs,
            "cost_histogram": dict(sorted(global_hist.items())),
            "prior_control_cost": 24, "new_explicit_control_cost": 12,
            "strict_support_drop_paid_cost": 0,
        },
        "records": records,
        "malformed": {"rejected": rejected, "valid": 1},
        "work_ledger": {
            "producer_wall_seconds": elapsed,
            "producer_peak_rss_kib_linux": rss,
            "logical_cost": "VARDEF/RES nodes in explicit certificates; optimizer and basis discovery excluded from W",
            "machine_warning": "Parsing, source scans, relation DP, basis selection, proof emission, fresh-name management, checking, serialization and scheduling remain separately charged machine resources."
        }
    }
    out = Path("results/raw/arc/lspv5_314/source_aware_exit_compiler_referee314.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    out.write_text(payload, encoding="utf-8")
    digest = hashlib.sha256(payload.encode()).hexdigest()
    print(json.dumps({
        "status": "PASS", "pairs": exact_pairs, "max_cost": max_cost,
        "maximizers": maxima, "histogram": dict(sorted(global_hist.items())),
        "explicit_parity_certificates": 32, "explicit_paid_nodes": 96,
        "support_drop_cost": 0, "malformed_rejected": rejected,
        "raw_sha256": digest, "wall_seconds": elapsed, "peak_rss_kib": rss,
    }, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "error": repr(exc)}), file=sys.stderr)
        raise
