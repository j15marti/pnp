#!/usr/bin/env python3
"""Independent adversarial audit of the published LSPV-3/508 compact checker.

The target is the separately declared R_CAST507(w) executable, not historical
R_mix341.  Every mutation is serialized to JSON and parsed back before replay,
so accepted cases are actual byte-level type/canonicalization aliases.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path

TARGET = Path(__file__).with_name("peer_lspv3_508_paid_cast_replay.py")


def load_target():
    spec = importlib.util.spec_from_file_location("peer508", TARGET)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def roundtrip(value):
    payload = json.dumps(value, separators=(",", ":"), allow_nan=False)
    return json.loads(payload), payload.encode()


def replay(module, sources, n, nodes, root, w):
    packed, raw = roundtrip(
        {"sources": sources, "n": n, "nodes": nodes, "root": root, "w": w}
    )
    # JSON changes source tuples to lists; restore only the separate trusted
    # source parameter exactly as an external parser would normalize clauses.
    packed["sources"] = [module.norm(c) for c in packed["sources"]]
    result = module.check(
        packed["sources"],
        packed["n"],
        packed["nodes"],
        packed["root"],
        packed["w"],
    )
    return result, raw


def strict_packet_check(module, packed):
    """Proposed canonical JSON-object layer before the peer semantic checker."""
    assert type(packed["n"]) is int and packed["n"] >= 0
    assert type(packed["root"]) is int and packed["root"] >= 0
    assert type(packed["w"]) is int and packed["w"] >= 1
    sources = packed["sources"]
    nodes = packed["nodes"]
    assert type(sources) is list and type(nodes) is list
    canonical_sources = []
    for clause in sources:
        assert type(clause) is list and clause
        assert all(type(lit) is int and lit != 0 for lit in clause)
        normalized = list(module.norm(clause))
        assert clause == normalized
        canonical_sources.append(tuple(clause))
    for idx, node in enumerate(nodes):
        assert type(node) is dict
        assert type(node.get("kind")) is str
        assert type(node.get("cost")) is int and node["cost"] >= 0
        if "parents" in node:
            assert type(node["parents"]) is list
            assert all(type(parent) is int and 0 <= parent < idx for parent in node["parents"])
        if "pivot" in node:
            assert type(node["pivot"]) is int and node["pivot"] > 0
        if "clause" in node:
            clause = node["clause"]
            assert type(clause) is list
            assert all(type(lit) is int and lit != 0 for lit in clause)
            assert clause == list(module.norm(clause))
        if node["kind"] == "SOURCE":
            assert idx < len(canonical_sources)
            assert node["clause"] == list(canonical_sources[idx])
    return module.check(
        canonical_sources,
        packed["n"],
        nodes,
        packed["root"],
        packed["w"],
    )


def first_source_literal(nodes, predicate):
    for i, node in enumerate(nodes):
        if node["kind"] != "SOURCE":
            continue
        for j, lit in enumerate(node["clause"]):
            if predicate(lit):
                return i, j, lit
    raise AssertionError("required source literal not found")


def run():
    m = load_target()
    sources, n, nodes, root = m.construct("K4", 0, 1)
    baseline, baseline_raw = replay(m, sources, n, nodes, root, 1)

    accepted = []
    accepted_packets = []

    def accepts(name, mutate):
        candidate = copy.deepcopy(nodes)
        mutate(candidate)
        result, raw = replay(m, sources, n, candidate, root, 1)
        assert result[:2] == baseline[:2]
        packed = json.loads(raw)
        accepted_packets.append(packed)
        accepted.append(
            {
                "name": name,
                "bytes": len(raw),
                "sha256": hashlib.sha256(raw).hexdigest(),
            }
        )

    i, j, lit = first_source_literal(nodes, lambda x: x > 0)
    accepts(
        "duplicate_source_literal",
        lambda p, i=i, lit=lit: p[i]["clause"].append(lit),
    )
    accepts(
        "reordered_source_literals",
        lambda p, i=i: p[i].__setitem__("clause", list(reversed(p[i]["clause"]))),
    )
    accepts(
        "integral_float_source_literal",
        lambda p, i=i, j=j, lit=lit: p[i]["clause"].__setitem__(j, float(lit)),
    )
    assert lit == 1, "K4 fixture expected a positive literal 1"
    accepts(
        "boolean_true_source_literal_for_integer_one",
        lambda p, i=i, j=j: p[i]["clause"].__setitem__(j, True),
    )

    first_and = next(k for k, node in enumerate(nodes) if node["kind"] == "AND3")
    assert nodes[first_and]["parents"] == [0, 1]
    accepts(
        "boolean_parent_ids_false_true",
        lambda p, k=first_and: p[k].__setitem__("parents", [False, True]),
    )
    accepts(
        "boolean_true_unit_cost",
        lambda p, k=first_and: p[k].__setitem__("cost", True),
    )
    accepts(
        "integral_float_unit_cost",
        lambda p, k=first_and: p[k].__setitem__("cost", 1.0),
    )

    rejected = []

    def rejects(name, mutate):
        candidate = copy.deepcopy(nodes)
        mutate(candidate)
        _, raw = roundtrip(
            {"sources": sources, "n": n, "nodes": candidate, "root": root, "w": 1}
        )
        try:
            replay(m, sources, n, candidate, root, 1)
        except (AssertionError, TypeError, ValueError, IndexError):
            rejected.append(
                {
                    "name": name,
                    "bytes": len(raw),
                    "sha256": hashlib.sha256(raw).hexdigest(),
                }
            )
            return
        raise AssertionError(f"hostile case accepted: {name}")

    rejects(
        "nonintegral_float_source_literal",
        lambda p, i=i, j=j: p[i]["clause"].__setitem__(j, 1.5),
    )
    rejects(
        "string_source_literal",
        lambda p, i=i, j=j: p[i]["clause"].__setitem__(j, "1"),
    )
    rejects(
        "false_unit_cost",
        lambda p, k=first_and: p[k].__setitem__("cost", False),
    )
    rejects(
        "float_parent_id",
        lambda p, k=first_and: p[k].__setitem__("parents", [0.0, 1]),
    )

    # The published compact replay covers prefixes j<k, not arbitrary subsets S.
    # This is a coverage fact, not a counterexample to the local mathematical
    # composition proof for an arbitrary positional S.
    prefix_positions = {}
    for k in (0, 1, 2, 4, 16):
        ss, _, _, _ = m.construct("K4", k, 1)
        prefix_positions[str(k)] = len(ss)

    baseline_packet = json.loads(baseline_raw)
    strict_baseline = strict_packet_check(m, baseline_packet)
    assert strict_baseline[:2] == baseline[:2]
    strict_alias_rejected = 0
    for packet in accepted_packets:
        try:
            strict_packet_check(m, packet)
        except (AssertionError, TypeError, ValueError, IndexError):
            strict_alias_rejected += 1
        else:
            raise AssertionError("strict layer accepted a known alias")

    return {
        "target_path": str(TARGET),
        "target_sha256": hashlib.sha256(TARGET.read_bytes()).hexdigest(),
        "baseline": {
            "work": baseline[0],
            "span": baseline[1],
            "serialized_bytes": len(baseline_raw),
            "sha256": hashlib.sha256(baseline_raw).hexdigest(),
        },
        "accepted_aliases": accepted,
        "rejected_controls": rejected,
        "accepted_count": len(accepted),
        "rejected_count": len(rejected),
        "strict_repair": {
            "baseline_accepted": True,
            "accepted_aliases_rejected": strict_alias_rejected,
        },
        "prefix_only_case_source_counts": prefix_positions,
        "scope": (
            "Published R_CAST507 compact JSON checker only; accepted aliases show "
            "raw-evidence canonical/type binding is absent. Logical construction "
            "and historical R_mix341 are not refuted."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
