#!/usr/bin/env python3
"""Independent reconstruction of LSPV-5/425 canonical compression.

This verifier targets the preserved SOURCE/AND3/XOR packet/checker only.  It
does not authenticate the historical R_mix341 grammar.
"""

from __future__ import annotations
import copy, hashlib, json, subprocess, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACKET = ROOT / "replay/413/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json"
CHECKER = ROOT / "replay/413/lspv2_341_independent_verify.js"


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def js_key(value):
    if isinstance(value, bool):
        return ("bool", value)
    if isinstance(value, (int, float)):
        x = float(value)
        return ("number", 0.0 if x == 0 else x)
    return (type(value).__name__, value)


def canonicalize(data):
    out = []
    for f in data["fixtures"]:
        v, e = f["graph"]["n"], len(f["graph"]["edges"])
        keep = (1 << e) - 1
        ids = {}

        def put(old, new):
            k = js_key(old)
            if k in ids:
                raise ValueError("duplicate parsed identity")
            ids[k] = new
            return new

        def get(old):
            return ids[js_key(old)]

        clauses = [
            {"id": put(c["id"], f"s{i}"), "vertex": c["vertex"], "literals": list(c["literals"])}
            for i, c in enumerate(f["clauses"])
        ]

        def row(r):
            return {"mask": hex(int(r["mask"], 0) & keep), "rhs": r["rhs"]}

        proof = []
        for i, p in enumerate(f["proof"]):
            q = {"id": f"d{i}", "kind": p["kind"], "rule": p["rule"], "parents": [get(x) for x in p["parents"]]}
            put(p["id"], q["id"])
            if p["rule"] == "AND3":
                q.update(support=list(p["support"]), table=p["table"])
                if "row" in p:
                    q["row"] = row(p["row"])
            elif p["rule"] == "XOR":
                q["row"] = row(p["row"])
            else:
                raise ValueError("unknown rule")
            proof.append(q)
        out.append({
            "graph": {"name": "BRIDGE_K4x2" if f["graph"]["name"] == "BRIDGE_K4x2" else "G", "n": v, "edges": copy.deepcopy(f["graph"]["edges"])},
            "charges": list(f["charges"]), "clauses": clauses, "proof": proof,
            "deleted": [{"sourceId": get(d["sourceId"]), "assignment": d["assignment"]} for d in f["deleted"]],
            "evenWitness": f["evenWitness"], "properties": {"essential": f["properties"]["essential"]}
        })
    return {"fixtures": out, "summary": [None] * len(out)}


def encoded(data) -> bytes:
    return (json.dumps(data, separators=(",", ":")) + "\n").encode()


def accepted(raw: bytes) -> bool:
    with tempfile.NamedTemporaryFile(suffix=".json") as fh:
        fh.write(raw); fh.flush()
        return subprocess.run(["node", str(CHECKER), fh.name], capture_output=True).returncode == 0


def main():
    base = json.loads(PACKET.read_text())
    canon = canonicalize(base)
    raw = encoded(canon)
    assert accepted(raw)
    checks = 1

    # Independently exercise the projection homomorphism and ignored fields.
    ghost = copy.deepcopy(base)
    rows = [p for p in ghost["fixtures"][0]["proof"] if p["rule"] == "AND3" and "row" in p]
    for p in rows[:2]:
        p["row"]["mask"] = hex(int(p["row"]["mask"], 0) ^ (1 << 8192))
    assert encoded(canonicalize(ghost)) == raw
    checks += 1
    meta = copy.deepcopy(base)
    meta["version"] = "X" * (1 << 20); meta["definition"] = "Y" * (1 << 20); meta["unknown"] = "Z" * (1 << 20)
    assert encoded(canonicalize(meta)) == raw
    checks += 1

    for f in canon["fixtures"]:
        v, e, w = f["graph"]["n"], len(f["graph"]["edges"]), len(f["proof"])
        single = encoded({"fixtures": [f], "summary": [None]})
        assert len(single) <= 512 * (v + 1) * (e + w + 1)
        checks += 1

    for kind in ("sink", "literal", "table", "parent"):
        bad = copy.deepcopy(base)
        if kind == "sink": bad["fixtures"][0]["proof"][-1]["row"]["rhs"] ^= 1
        if kind == "literal": bad["fixtures"][0]["clauses"][0]["literals"][0] = 999
        if kind == "table": bad["fixtures"][0]["proof"][0]["table"] ^= 1
        if kind == "parent": bad["fixtures"][0]["proof"][0]["parents"][0] = "missing"
        try:
            out = encoded(canonicalize(bad))
            assert not accepted(out)
        except (KeyError, ValueError):
            pass
        checks += 1

    print(json.dumps({
        "status": "PASS independent Python reconstruction",
        "checks": checks,
        "canonical_bytes": len(raw),
        "canonical_sha256": digest(raw),
        "fixture_count": len(canon["fixtures"]),
        "scope": "recovered SOURCE/AND3/XOR parsed-object semantics only"
    }, indent=2))


if __name__ == "__main__":
    main()
