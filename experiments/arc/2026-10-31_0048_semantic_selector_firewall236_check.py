#!/usr/bin/env python3
"""Independent checker for ARC-SEMANTIC-SELECTOR-FIREWALL236 raw output."""
import itertools
import json
from fractions import Fraction
from pathlib import Path

RAW = Path("results/raw/arc/2026-10-31_0048_LSPV5_SEMANTIC_SELECTOR_FIREWALL236_raw.json")


def clauses():
    return [tuple(-(i + 1) if a[i] else i + 1 for i in range(3))
            for a in itertools.product((0, 1), repeat=3)]


def sat(formula):
    for a in itertools.product((0, 1), repeat=3):
        if all(any((a[abs(l) - 1] == 1) == (l > 0) for l in c) for c in formula):
            return True
    return False


def main():
    data = json.loads(RAW.read_text(encoding="utf-8"))
    cs = clauses()
    checks = 0
    labels = []
    for row in data["exhaustive_family"]["rows"]:
        f = [cs[i] for i in range(8) if row["mask"] & (1 << i)]
        actual = "SAT" if sat(f) else "UNSAT"
        assert actual == row["label"]
        assert (row["child_kind"] == "T") == (actual == "SAT")
        labels.append(actual)
        checks += 2
    assert labels.count("SAT") == 255 and labels.count("UNSAT") == 1
    checks += 2
    T = [tuple(c) for c in data["fixed_children"]["T"]]
    U = [tuple(c) for c in data["fixed_children"]["U"]]
    assert sat(T) and not sat(U)
    checks += 2
    for row in data["delay_recurrence"]["rows"]:
        K = Fraction(row["K"])
        rhs = max(Fraction(11, 10), Fraction(3, 5) + Fraction(1, 2) * K)
        assert Fraction(row["claimed_rhs"]) == rhs
        assert row["violates_when_parent_call_mandatory"] == (K > rhs)
        checks += 2
    for name, control in data["same_support_controls"].items():
        diag = control["diagnostics"]
        for rec in diag["occurrences"]:
            s = {int(k): v for k, v in rec["S"].items()}
            u = {int(k): v for k, v in rec["U"].items()}
            assert all(u[v] == 1 - bit for v, bit in s.items())
            checks += 1
        for endpoint, rec in diag["endpoints"].items():
            assert sum(rec["N"]) == len(diag["occurrences"])
            assert rec["sat"] == (rec["N"][0] == 0)
            checks += 2
        assert (control["models"] > 0) == (name == "H7_SAT")
        checks += 1
    print(json.dumps({"run": data["run"], "independent_checks": checks,
                      "status": "PASS"}, sort_keys=True))


if __name__ == "__main__":
    main()
