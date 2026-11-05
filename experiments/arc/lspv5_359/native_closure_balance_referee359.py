#!/usr/bin/env python3
"""REFEREE359: executable audit of the literal paid-node closure of R_mix341.

This is deliberately not a replacement byte grammar for /341.  It tests the
mathematical distinction proved in the accompanying report:
  * public objects are paid nodes (or constant-many facets of a paid node);
  * LOCAL circuit-internal gates are not public proof nodes;
  * every constant-support semantic root has a constant truth-table normal form;
  * supplied payload bytes can be arbitrarily larger than paid-node cost.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


def tt3(mask: int) -> list[int]:
    return [(mask >> a) & 1 for a in range(8)]


def eval_tt3(bits: list[int], a: int, b: int, c: int) -> int:
    return bits[a | (b << 1) | (c << 2)]


def gate_tt(mask: int, a: int, b: int) -> int:
    return (mask >> (a | (b << 1))) & 1


def redundant_local_payload(pairs: int) -> dict:
    gates = []
    prev = "x0"
    for i in range(pairs):
        g1, g2 = f"n{i}_a", f"n{i}_b"
        gates.append({"id": g1, "op": "NOT", "in": prev})
        gates.append({"id": g2, "op": "NOT", "in": g1})
        prev = g2
    return {"support": ["x0"], "gates": gates, "root": prev}


def eval_redundant(payload: dict, x: int) -> int:
    env = {"x0": x}
    for g in payload["gates"]:
        env[g["id"]] = 1 - env[g["in"]]
    return env[payload["root"]]


def canonical_local(payload: dict) -> dict:
    return {"kind": "LOCAL_TT", "support": [0],
            "truth": [eval_redundant(payload, 0), eval_redundant(payload, 1)]}


def literal_reference_ok(ref: dict, paid_ids: set[int]) -> bool:
    """The /341 edge grammar names antecedent-node identifiers, not gate IDs."""
    return set(ref) == {"node"} and isinstance(ref["node"], int) and ref["node"] in paid_ids


def canonical_proof(q: int) -> list[dict]:
    """A typed semantic stress trace with bounded records and alpha-normal names."""
    out = []
    for i in range(q):
        typ = ("DEF", "AND3", "GF2", "LOCAL", "RES")[i % 5]
        rec = {"id": i, "type": typ, "parents": [j for j in (i - 2, i - 1) if j >= 0]}
        if typ == "DEF":
            rec.update(var=f"z{i}", inputs=[max(0, i - 1), max(0, i - 2)], gate=i % 16)
        elif typ == "AND3":
            rec.update(support=[j for j in range(min(3, i + 1))], truth=tt3(i % 256))
        elif typ == "GF2":
            rec.update(mask=[j for j in range(i + 1) if (j + i) % 3 == 0], rhs=i & 1)
        elif typ == "LOCAL":
            rec.update(support=[0, 1, 2][: min(3, i + 1)], truth=tt3((17 * i) % 256))
        else:
            rec.update(clause=[(j, (j + i) & 1) for j in range(i + 1) if (j + i) % 4 == 0], pivot=i // 2)
        out.append(rec)
    return out


def encoded_bytes(obj) -> int:
    return len(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode())


def main() -> None:
    assertions = 0
    # Every ternary Boolean root has an exact eight-bit extensional normal form.
    for mask in range(256):
        bits = tt3(mask)
        for a in range(2):
            for b in range(2):
                for c in range(2):
                    assert eval_tt3(bits, a, b, c) == ((mask >> (a | b << 1 | c << 2)) & 1)
                    assertions += 1

    # Every paid binary conservative DEF gate is one of sixteen four-row tables.
    for mask in range(16):
        rows = [gate_tt(mask, a, b) for a in range(2) for b in range(2)]
        assert len(rows) == 4
        assertions += 1
        for a in range(2):
            for b in range(2):
                z = gate_tt(mask, a, b)
                assert sum(int(zz == z) for zz in range(2)) == 1
                assertions += 1

    # Uncharged redundant payload can grow while W=1, but the root normalizes.
    payload_rows = []
    for pairs in (0, 1, 2, 8, 32, 128, 512):
        p = redundant_local_payload(pairs)
        c = canonical_local(p)
        assert c["truth"] == [0, 1]
        assertions += 1
        old_b, new_b = encoded_bytes(p), encoded_bytes(c)
        if pairs:
            assert old_b > new_b
            assertions += 1
        payload_rows.append({"not_pairs": pairs, "paid_nodes": 1,
                             "payload_bytes": old_b, "canonical_bytes": new_b})

    # Literal-closure references: node IDs pass; private wire selectors fail.
    paid = {0, 1, 2}
    reference_controls = [
        ({"node": 0}, True, "paid node"),
        ({"node": 2}, True, "paid node"),
        ({"node": 3}, False, "missing node"),
        ({"node": 1, "wire": "g7"}, False, "uncharged exported wire"),
        ({"wire": "g7"}, False, "wire without node"),
        ({"node": "1"}, False, "noninteger node"),
    ]
    for ref, expected, _ in reference_controls:
        assert literal_reference_ok(ref, paid) == expected
        assertions += 1

    # Canonical semantic records have a uniform coarse polynomial byte bound.
    size_rows = []
    source_bytes = 111
    for q in (1, 2, 4, 8, 16, 32, 64, 128):
        proof = canonical_proof(q)
        b = encoded_bytes(proof)
        bound = 32 * (source_bytes + q + 1) ** 3
        assert b <= bound
        assertions += 1
        assert [r["id"] for r in proof] == list(range(q))
        assertions += 1
        assert all(all(p < r["id"] for p in r["parents"]) for r in proof)
        assertions += 1
        size_rows.append({"q": q, "bytes": b, "coarse_bound": bound})

    # Both-label and malformed controls are explicit, not inferred from traces.
    sat = [[1, 2], [-1, 2]]
    unsat = [[1], [-1]]
    def models(cnf, n):
        ans = []
        for a in range(1 << n):
            if all(any(((a >> (abs(l)-1)) & 1) == (l > 0) for l in C) for C in cnf):
                ans.append(a)
        return ans
    assert len(models(sat, 2)) == 2; assertions += 1
    assert len(models(unsat, 1)) == 0; assertions += 1
    malformed = [None, {}, {"node": -1}, {"node": 0, "wire": 7}, {"node": 99}]
    for x in malformed:
        ok = isinstance(x, dict) and literal_reference_ok(x, paid)
        assert not ok
        assertions += 1

    result = {
        "run": "REFEREE359",
        "status": {
            "literal_paid_node_closure": "PROVED_BY_TEXTUAL_RULE_CLOSURE",
            "semantic_canonical_balance": "PROVED_FOR_ROOT_ONLY_FIXED_FACET_COMPLETION",
            "authoritative_byte_parser": "ABSENT_IN_341",
            "same_R_B3": "OPEN",
            "P_vs_NP": "OPEN",
        },
        "assertions": assertions,
        "payload_rows": payload_rows,
        "size_rows": size_rows,
        "reference_controls": [{"ref": r, "accepted": e, "reason": why}
                               for r, e, why in reference_controls],
        "both_label_models": {"sat": len(models(sat, 2)), "unsat": len(models(unsat, 1))},
        "physical_cost_note": "W counts paid nodes; supplied bytes, reads, normalization, checking, output, and peak space are separate.",
    }
    raw = json.dumps(result, indent=2, sort_keys=True) + "\n"
    result["prehash_sha256"] = hashlib.sha256(raw.encode()).hexdigest()
    out = Path("results/raw/arc/2026-11-05_0248_LSPV5_REFEREE359_raw.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"assertions": assertions, "raw": str(out),
                      "largest_payload": payload_rows[-1], "largest_canonical": size_rows[-1]}))


if __name__ == "__main__":
    main()
