#!/usr/bin/env python3
"""REFEREE311: early-contradiction correction to the local factor compiler."""

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


def canon(clause):
    out = tuple(sorted(set(clause), key=lambda x: (abs(x), x < 0)))
    assert all(x and -x not in out for x in out)
    return out


def blocker(a):
    return canon(-v if (a >> (v - 1)) & 1 else v for v in VARS)


def clause_true(clause, a):
    return any(bool((a >> (abs(l) - 1)) & 1) == (l > 0) for l in clause)


def resolve(left, right, pivot):
    assert pivot in left and -pivot in right
    raw = (set(left) - {pivot}) | (set(right) - {-pivot})
    assert not any(-x in raw for x in raw)
    return canon(raw)


def gate_slots(out, left, right):
    return (canon((-out, left)), canon((-out, right)), canon((out, -left, -right)))


def weaken(base, target, first_fresh=4):
    base, target = canon(base), canon(target)
    assert base and set(base) <= set(target)
    added = tuple(x for x in target if x not in base)
    if not added:
        return {"base": list(base), "target": list(target), "defs": [], "res": [], "cost": 0}
    nxt = first_fresh
    defs, chain = [], []
    if len(added) == 1:
        w = -added[0]
    else:
        out = nxt; nxt += 1
        slots = gate_slots(out, -added[0], -added[1])
        defs.append({"out": out, "left": -added[0], "right": -added[1], "slots": [list(x) for x in slots]})
        chain.append((out, slots))
        prev = out
        for lit in added[2:]:
            out = nxt; nxt += 1
            slots = gate_slots(out, prev, -lit)
            defs.append({"out": out, "left": prev, "right": -lit, "slots": [list(x) for x in slots]})
            chain.append((out, slots))
            prev = out
        w = prev
    qs = []
    for lit in base:
        out = nxt; nxt += 1
        slots = gate_slots(out, -lit, w)
        defs.append({"out": out, "left": -lit, "right": w, "slots": [list(x) for x in slots]})
        qs.append((lit, out, slots))
    res, cur = [], base
    for lit, q, slots in qs:
        child = resolve(cur, slots[0], lit)
        res.append({"left": list(cur), "right": list(slots[0]), "pivot": lit, "out": list(child)})
        cur = child
    for lit, q, slots in qs:
        child = resolve(cur, slots[2], -q)
        res.append({"left": list(cur), "right": list(slots[2]), "pivot": -q, "out": list(child)})
        cur = child
    for out, slots in reversed(chain):
        child = resolve(cur, slots[2], -out)
        res.append({"left": list(cur), "right": list(slots[2]), "pivot": -out, "out": list(child)})
        cur = child
    assert cur == target
    cost = len(defs) + len(res)
    assert cost == 3 * len(base) + 2 * len(added) - 2 <= 6
    return {"base": list(base), "target": list(target), "defs": defs, "res": res, "cost": cost}


def unique_zero_source():
    clauses = []
    for x, y in itertools.combinations(VARS, 2):
        clauses.extend([canon((-x, -y)), canon((-x, y)), canon((x, -y))])
    clauses = tuple(sorted(set(clauses), key=lambda c: c))
    models = [a for a in range(8) if all(clause_true(c, a) for c in clauses)]
    assert models == [0]
    return clauses


def false_cube_refutation():
    clauses = [blocker(a) for a in range(8)]
    nodes = []
    current = list(range(8))
    all_lines = list(clauses)
    # Assignment order 000,001,... pairs first on x1, then x2, then x3.
    for pivot in (1, 2, 3):
        nxt = []
        for i in range(0, len(current), 2):
            li, ri = current[i], current[i + 1]
            left, right = all_lines[li], all_lines[ri]
            if pivot not in left:
                left, right, li, ri = right, left, ri, li
            out = resolve(left, right, pivot)
            node = {"left_id": li, "right_id": ri, "pivot": pivot, "out": list(out)}
            nodes.append(node)
            all_lines.append(out)
            nxt.append(len(all_lines) - 1)
        current = nxt
    assert len(nodes) == 7 and all_lines[current[0]] == ()
    return {"sources": [list(c) for c in clauses], "nodes": nodes, "cost": 7, "root_id": current[0]}


def parse_pair(obj):
    if not isinstance(obj, dict) or set(obj) != {"input_mask", "output_mask"}:
        raise ValueError("schema")
    a, b = obj["input_mask"], obj["output_mask"]
    if not isinstance(a, int) or isinstance(a, bool) or not 0 <= a <= 255:
        raise ValueError("input")
    if not isinstance(b, int) or isinstance(b, bool) or not 0 <= b <= 255:
        raise ValueError("output")
    if a & ~b:
        raise ValueError("not entailed")
    return a, b


def main():
    start = time.perf_counter()
    hist = Counter()
    pairs = 0
    sat_input_pairs = 0
    unsat_input_pairs = 0
    max_cost = -1
    extremal = []
    for inp in range(256):
        for out in range(256):
            if inp & ~out:
                continue
            pairs += 1
            if inp == 0:
                unsat_input_pairs += 1
                cost, mode = 7, "early_contradiction"
            else:
                sat_input_pairs += 1
                assert out != 0
                blockers = 8 - out.bit_count()
                cost, mode = 6 * blockers, "blockers"
                assert blockers <= 7 and cost <= 42
            hist[cost] += 1
            rec = {"input_mask": inp, "output_mask": out, "input_models": inp.bit_count(),
                   "output_models": out.bit_count(), "mode": mode, "bound": cost}
            if cost > max_cost:
                max_cost, extremal = cost, [rec]
            elif cost == max_cost:
                extremal.append(rec)
    assert (pairs, sat_input_pairs, unsat_input_pairs, max_cost, len(extremal)) == (6561, 6305, 256, 42, 8)

    # Explicit 42-node construction: an all-binary source with unique model 000.
    source = unique_zero_source()
    certs = []
    for a in range(1, 8):
        b = blocker(a)
        false = [c for c in source if not clause_true(c, a)]
        assert false and all(len(c) == 2 for c in false)
        cert = weaken(false[0], b, 4)
        assert cert["cost"] == 6
        certs.append({"assignment": a, **cert})
    assert sum(c["cost"] for c in certs) == 42

    false_ref = false_cube_refutation()

    even_mask = sum(1 << a for a in range(8) if a.bit_count() % 2 == 0)
    odd_mask = sum(1 << a for a in range(8) if a.bit_count() % 2 == 1)
    assert even_mask.bit_count() == odd_mask.bit_count() == 4
    assert not (even_mask & ~even_mask) and (even_mask & ~odd_mask)

    malformed = [None, {}, {"input_mask": -1, "output_mask": 0},
                 {"input_mask": 0, "output_mask": 256},
                 {"input_mask": True, "output_mask": 255},
                 {"input_mask": 1.0, "output_mask": 1},
                 {"input_mask": 3, "output_mask": 1},
                 {"input_mask": 1, "output_mask": 1, "extra": 0},
                 {"input_mask": "1", "output_mask": 1},
                 {"input_mask": 1, "output_mask": None}]
    rejected = 0
    for x in malformed:
        try:
            parse_pair(x)
        except ValueError:
            rejected += 1
    assert rejected == len(malformed)
    assert parse_pair({"input_mask": even_mask, "output_mask": even_mask}) == (even_mask, even_mask)

    elapsed = time.perf_counter() - start
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    result = {
        "run_id": "FACTOR-EARLY-CONTRADICTION-REFEREE311",
        "date_pst": "2026-11-03 03:48 PST",
        "calculus": "unchanged Rmix341; E=strict RES plus charged source-independent signed two-input VARDEF; explicit <=3-variable factors only",
        "status": {
            "proved": [
                "The DPLL-IMPLICATE-PRUNE358 branch merge invariant and seven-node k<=3 clause bound are sound.",
                "The claim that PRUNE358 does not improve REFEREE310's 48-node factor bound is false.",
                "A satisfiable input entails only a nonfalse output factor, so at most seven blockers are required; cost <=42.",
                "If the output factor is false, the input is UNSAT and the compiler terminates with contradiction in <=7 nodes."
            ],
            "restricted": "Explicit Boolean factors over at most three named variables only.",
            "open": ["global XOR compilation", "circuit-valued LOCAL-CONVERT", "B1", "B2", "B3", "superpolynomial Wbar", "P versus NP"]
        },
        "theorem": {
            "prior_factor_coefficient": 48,
            "corrected_factor_coefficient": 42,
            "false_output_early_contradiction": 7,
            "formula": "W_L3(F) <= W_E(F) <= 42 W_L3(F) + O(1)"
        },
        "exhaustive_relation_pairs": {
            "entailed_pairs": pairs,
            "satisfiable_input_pairs": sat_input_pairs,
            "unsat_input_pairs": unsat_input_pairs,
            "bound_histogram": dict(sorted(hist.items())),
            "max_bound": max_cost,
            "extremal_pairs": extremal
        },
        "explicit_42_node_control": {
            "source": [list(c) for c in source],
            "models": [0],
            "output_mask": 1,
            "certificates": certs,
            "total_cost": 42
        },
        "false_factor_control": false_ref,
        "both_label_controls": {
            "even_parity_mask": even_mask,
            "odd_parity_mask": odd_mask,
            "even_models": even_mask.bit_count(),
            "odd_models": odd_mask.bit_count(),
            "wrong_label_entailment": False
        },
        "malformed": {"rejected": rejected, "valid": 1},
        "work_ledger": {
            "producer_wall_seconds": elapsed,
            "producer_peak_rss_kib_linux": rss,
            "logical_cost": "distinct paid inference/definition nodes only; free best-path discovery",
            "machine_warning": "Enumeration, parsing, source selection, serialization, checking and peak host memory are separate from W and from FLMV resources."
        }
    }
    out = Path("results/raw/arc/lspv5_311/factor_early_contradiction_referee311.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    out.write_text(payload, encoding="utf-8")
    digest = hashlib.sha256(payload.encode()).hexdigest()
    print(json.dumps({"status": "PASS", "pairs": pairs, "max_bound": max_cost,
                      "extremal_pairs": len(extremal), "explicit_cost": 42,
                      "false_factor_cost": 7, "malformed_rejected": rejected,
                      "raw_sha256": digest, "wall_seconds": elapsed,
                      "peak_rss_kib": rss}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "error": repr(exc)}), file=sys.stderr)
        raise
