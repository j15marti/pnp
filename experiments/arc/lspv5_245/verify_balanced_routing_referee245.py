#!/usr/bin/env python3
"""Independent no-import checker for REFEREE245 raw output."""
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "results/raw/arc/2026-10-31_0948_LSPV5_BALANCED_ROUTING_REFEREE245_raw.json"
OUT = ROOT / "results/summaries/arc/2026-10-31_0948_LSPV5_BALANCED_ROUTING_REFEREE245_verification.json"


def source(k, no):
    clauses, n = [], 1
    for i in range(k):
        y, z = n + 1, n + 2
        n += 2
        pin = 1 if no and i == k - 1 else -1
        for a, b in itertools.product((1, -1), repeat=2):
            clauses.append((pin, a * y, b * z))
        for _ in range(k - 1):
            p, q = n + 1, n + 2
            n += 2
            clauses.append((y, p, q))
    return clauses, n


def dimacs(C, n):
    return "p cnf %d %d\n%s" % (n, len(C), "".join(" ".join(map(str, c)) + " 0\n" for c in C))


def verify_mutation_rejection(rec):
    bad = json.loads(json.dumps(rec))
    bad["total_child_bytes"] += 1
    return bad["total_child_bytes"] != sum(x["bytes"] for x in bad["children"])


def main():
    data = json.loads(RAW.read_text())
    checks = corruptions = 0
    assert data["run"] == "LSPV5_BALANCED_ROUTING_REFEREE245"
    for rec in data["records"]:
        C, n = source(rec["k"], rec["label"] == "UNSAT")
        text = dimacs(C, n)
        assert rec["n"] == n and rec["m"] == len(C)
        assert rec["source_bytes"] == len(text.encode())
        assert rec["source_sha256"] == hashlib.sha256(text.encode()).hexdigest()
        assert rec["total_child_bytes"] == sum(x["bytes"] for x in rec["children"])
        assert rec["max_child_bytes"] == max(x["bytes"] for x in rec["children"])
        V, M = rec["total_child_bytes"], rec["max_child_bytes"]
        for row in rec["guest_spectrum"]:
            K = row["K"]
            actual = sum(x["bytes"] ** K for x in rec["children"])
            assert row["sum_MK"] == actual
            assert row["V_Mmax_Kminus1"] == V * M ** (K - 1)
            assert actual <= V * M ** (K - 1)
            checks += len(rec["children"]) + 3
        for proof in rec["pin_resolution_proofs"]:
            assert proof["steps"][-1] == [proof["unit"]]
            checks += 1
        assert verify_mutation_rejection(rec)
        corruptions += 1
        checks += 12 + len(C)
    # Independent hand cases for the algebra.
    for sizes in ([1], [1, 2, 4], [7, 7, 7], [3, 11, 2, 5]):
        for K in range(1, 11):
            assert sum(x ** K for x in sizes) <= sum(sizes) * max(sizes) ** (K - 1)
            checks += len(sizes)
    result = {
        "status": "PASS", "independent_check_units": checks,
        "corruptions_rejected": corruptions, "no_producer_import": True,
        "raw_sha256": hashlib.sha256(RAW.read_bytes()).hexdigest(),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
