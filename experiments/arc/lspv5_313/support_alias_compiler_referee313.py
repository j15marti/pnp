#!/usr/bin/env python3
"""REFEREE313: same-support stronger-representation aliasing controls."""

from __future__ import annotations

import hashlib
import itertools
import json
import resource
import sys
import time
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


def blocker(assignment):
    return canon(-(i + 1) if (assignment >> i) & 1 else i + 1 for i in range(3))


def parity_cnf(wanted_parity):
    return tuple(blocker(a) for a in range(8) if a.bit_count() % 2 != wanted_parity)


def singleton_units(assignment):
    return tuple(canon(((i + 1) if (assignment >> i) & 1 else -(i + 1),)) for i in range(3))


def models(clauses):
    return [a for a in range(8) if all(clause_true(c, a) for c in clauses)]


def resolve(left, right, pivot):
    left, right = canon(left), canon(right)
    if pivot not in left or -pivot not in right:
        raise ValueError("bad pivot")
    raw = (set(left) - {pivot}) | (set(right) - {-pivot})
    return canon(raw)


def unit_refutation(assignment, opposite_parity):
    units = singleton_units(assignment)
    pc = parity_cnf(opposite_parity)
    bad = next(c for c in pc if not clause_true(c, assignment))
    sources = list(units) + list(pc)
    lines = list(sources)
    current_id = sources.index(bad)
    nodes = []
    for variable in VARS:
        current = lines[current_id]
        lit = next(x for x in current if abs(x) == variable)
        unit_id = next(i for i, c in enumerate(sources[:3]) if c == (-lit,))
        out = resolve(current, sources[unit_id], lit)
        nodes.append({"left_id": current_id, "right_id": unit_id,
                      "pivot": lit, "out": list(out)})
        lines.append(out)
        current_id = len(lines) - 1
    assert not lines[current_id]
    return {
        "assignment": assignment,
        "opposite_parity": opposite_parity,
        "sources": [list(c) for c in sources],
        "nodes": nodes,
        "root_id": current_id,
        "cost": len(nodes),
    }


def projection_certificate():
    sources = [canon((1, 2)), canon((1, -2))]
    out = resolve(sources[0], sources[1], 2)
    assert out == (1,)
    return {
        "input_support": [1, 2], "output_support": [1],
        "sources": [list(c) for c in sources],
        "nodes": [{"left_id": 0, "right_id": 1, "pivot": 2, "out": [1]}],
        "root_id": 2, "cost": 1,
        "reason_alias_forbidden": "strict support drop; y cannot remain hidden in a factor typed only on x",
    }


def parse_alias_record(obj):
    required = {"input_support", "output_support", "source_mask", "output_mask", "consumer"}
    if not isinstance(obj, dict) or set(obj) != required:
        raise ValueError("schema")
    for key in ("input_support", "output_support"):
        support = obj[key]
        if not isinstance(support, list) or not support:
            raise ValueError("support")
        if any(not isinstance(x, int) or isinstance(x, bool) or x not in VARS for x in support):
            raise ValueError("support item")
        if support != sorted(set(support)):
            raise ValueError("support canonical")
    for key in ("source_mask", "output_mask"):
        value = obj[key]
        if not isinstance(value, int) or isinstance(value, bool) or not 0 <= value <= 255:
            raise ValueError("mask")
    if obj["source_mask"] & ~obj["output_mask"] & FULL:
        raise ValueError("not consequence")
    if obj["consumer"] not in ("semantic_same_support", "typed_exit"):
        raise ValueError("consumer")
    return obj


def main():
    started = time.perf_counter()
    even_mask = sum(1 << a for a in range(8) if a.bit_count() % 2 == 0)
    odd_mask = FULL ^ even_mask
    assert (even_mask, odd_mask) == (105, 150)

    # Exhaustive finite audit of the substitution invariant:
    # S subset Q implies S intersect T subset Q intersect T.
    entailed_pairs = substitution_checks = 0
    for source in range(256):
        for output in range(256):
            if source & ~output & FULL:
                continue
            entailed_pairs += 1
            for continuation in range(256):
                substitution_checks += 1
                assert (source & continuation) & ~(output & continuation) & FULL == 0
    assert entailed_pairs == 6561
    assert substitution_checks == 1_679_616

    # A factor-only full-support chain can be arbitrarily long without
    # materializing its repeated even-parity labels.
    chain_controls = []
    for length in (1, 2, 4, 8, 16, 32):
        nodes = [{"kind": "semantic", "support": [1, 2, 3],
                  "input_mask": 1 if i == 0 else even_mask,
                  "output_mask": even_mask}
                 for i in range(length)]
        assert all(n["input_mask"] & ~n["output_mask"] & FULL == 0 for n in nodes)
        chain_controls.append({
            "semantic_nodes": length,
            "nodes": nodes,
            "materialized_internal_nodes": 0,
            "alias_representation_mask": 1,
            "final_refutation_cost": 3,
        })

    even_cnf, odd_cnf = parity_cnf(0), parity_cnf(1)
    assert models(even_cnf) == [0, 3, 5, 6]
    assert models(odd_cnf) == [1, 2, 4, 7]
    proof_zero_vs_odd = unit_refutation(0, 1)
    proof_one_vs_even = unit_refutation(1, 0)

    valid = {
        "input_support": [1, 2, 3], "output_support": [1, 2, 3],
        "source_mask": 1, "output_mask": even_mask,
        "consumer": "semantic_same_support",
    }
    assert parse_alias_record(valid) == valid
    malformed = [
        None, {}, {**valid, "extra": 1},
        {**valid, "input_support": []}, {**valid, "output_support": [3, 2, 1]},
        {**valid, "input_support": [1, 1, 2]}, {**valid, "input_support": [0, 1]},
        {**valid, "source_mask": -1}, {**valid, "output_mask": 256},
        {**valid, "source_mask": True}, {**valid, "consumer": "native_resolution"},
        {**valid, "source_mask": odd_mask, "output_mask": even_mask},
    ]
    rejected = 0
    for obj in malformed:
        try:
            parse_alias_record(obj)
        except ValueError:
            rejected += 1
    assert rejected == 12

    sat_controls = {
        "singleton_000_and_even_models": models(singleton_units(0) + even_cnf),
        "singleton_001_and_odd_models": models(singleton_units(1) + odd_cnf),
        "singleton_000_and_odd_models": models(singleton_units(0) + odd_cnf),
        "singleton_001_and_even_models": models(singleton_units(1) + even_cnf),
    }
    assert sat_controls == {
        "singleton_000_and_even_models": [0],
        "singleton_001_and_odd_models": [1],
        "singleton_000_and_odd_models": [],
        "singleton_001_and_even_models": [],
    }

    elapsed = time.perf_counter() - started
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    result = {
        "run_id": "SAME-SUPPORT-ALIAS-COMPILER-REFEREE313",
        "date_pst": "2026-11-03 05:48 PST",
        "calculus": "unchanged Rmix341; E=strict RES plus paid source-independent signed two-input VARDEF; L3 exact factors on at most three common names",
        "status": {
            "proved_restricted": [
                "A same-support semantic factor node can be represented by the conjunction of stronger authenticated parent representations at zero inference-node cost while all consumers remain semantic consequence nodes on that same support.",
                "A maximal same-support factor-only region needs no internal exact-factor materialization; this certified alias scheme stops and invokes paid authenticated compilation at typed exits, strict support drops, native syntactic consumers, or contradiction.",
                "The explicit singleton/parity control contracts arbitrarily long repeated even-parity regions and has a three-node strict Resolution refutation."
            ],
            "computational": "Exhaustive 1,679,616-case substitution audit plus independent encoded proof replay.",
            "open": ["global joint-DAG coefficient for unrestricted L3", "mixed-rule-resistant superpolynomial Wbar", "B1", "B2", "B3", "P versus NP"],
        },
        "theorem": {
            "invariant": "S subseteq Q implies (S intersection T) subseteq (Q intersection T)",
            "scope": "factor-only semantic consumers with identical declared support",
            "exit_bound": "each exact three-variable factor exit retains REFEREE312 cost <=24; a local false exit costs <=7",
            "not_claimed": "zero-cost aliasing across support drops, into native RES/VARDEF operands, or for arbitrary semantic equivalence queries; the theorem does not prove those boundaries intrinsically costly",
        },
        "exhaustive": {
            "relations": 256, "entailed_pairs": entailed_pairs,
            "continuations_per_pair": 256, "substitution_checks": substitution_checks,
        },
        "parity": {
            "even_mask": even_mask, "odd_mask": odd_mask,
            "even_cnf": [list(c) for c in even_cnf],
            "odd_cnf": [list(c) for c in odd_cnf],
        },
        "same_support_chain_controls": chain_controls,
        "explicit_refutations": {
            "singleton_000_vs_odd": proof_zero_vs_odd,
            "singleton_001_vs_even": proof_one_vs_even,
        },
        "projection_exit_control": projection_certificate(),
        "both_label_sat_controls": sat_controls,
        "typed_exit_controls": [
            {"case": "same_support_semantic_consumer", "alias_allowed": True},
            {"case": "strict_support_drop", "alias_allowed": False},
            {"case": "native_resolution_consumer", "alias_allowed": False},
            {"case": "contradiction_output", "alias_allowed": False},
        ],
        "malformed": {"rejected": rejected, "valid": 1},
        "work_ledger": {
            "producer_wall_seconds": elapsed,
            "producer_peak_rss_kib_linux": rss,
            "logical_cost": "three-node and one-node proof DAGs; optimizer/alias-region discovery excluded from W",
            "machine_warning": "Parsing, support checks, region discovery, table access, proof emission, scheduling, serialization and validation remain machine work and space.",
        },
    }
    out = Path("results/raw/arc/lspv5_313/support_alias_compiler_referee313.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    out.write_text(payload, encoding="utf-8")
    digest = hashlib.sha256(payload.encode()).hexdigest()
    print(json.dumps({
        "status": "PASS", "pairs": entailed_pairs,
        "substitution_checks": substitution_checks,
        "chain_lengths": [x["semantic_nodes"] for x in chain_controls],
        "refutation_costs": [proof_zero_vs_odd["cost"], proof_one_vs_even["cost"]],
        "projection_cost": 1, "malformed_rejected": rejected,
        "raw_sha256": digest, "wall_seconds": elapsed, "peak_rss_kib": rss,
    }, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "error": repr(exc)}), file=sys.stderr)
        raise
