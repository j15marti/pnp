#!/usr/bin/env python3
"""Independent checker for ARC-SOURCE-BLOCKER-COMPRESSION-FIREWALL232."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def eval_clause(clause, mask):
    return any((((mask >> (abs(lit) - 1)) & 1) == 1) == (lit > 0)
               for lit in clause)


def eval_formula(formula, mask):
    return all(eval_clause(c, mask) for c in formula)


def restrict(formula, cube):
    out = []
    for clause in formula:
        residual = []
        satisfied = False
        for lit in clause:
            v = abs(lit)
            if v not in cube:
                residual.append(lit)
            elif cube[v] == int(lit > 0):
                satisfied = True
                break
        if not satisfied:
            out.append(tuple(residual))
    return out


def brute_sat(formula, n):
    return any(eval_formula(formula, mask) for mask in range(1 << n))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("raw", type=Path)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    data = json.loads(args.raw.read_text(encoding="utf-8"))
    checks = 0

    assert data["id"] == "ARC-SOURCE-BLOCKER-COMPRESSION-FIREWALL232"; checks += 1
    assert data["status"]["P_vs_NP"] == "OPEN"; checks += 1

    for pair in data["matched_same_support_cases"]:
        blocks = pair["blocks"]
        n = 3 * blocks
        sat = pair["SAT"]
        unsat = pair["UNSAT"]
        fs = [tuple(c) for c in sat["source_formula"]]
        fu = [tuple(c) for c in unsat["source_formula"]]
        support_s = Counter(tuple(sorted(abs(l) for l in c)) for c in fs)
        support_u = Counter(tuple(sorted(abs(l) for l in c)) for c in fu)
        assert support_s == support_u; checks += 1
        assert len(fs) == len(fu) == 8 * blocks; checks += 1

        models_s = [m for m in range(1 << n) if eval_formula(fs, m)]
        models_u = [m for m in range(1 << n) if eval_formula(fu, m)]
        assert models_s == sat["models"] == [(1 << n) - 1]; checks += 1
        assert models_u == unsat["models"] == []; checks += 1

        blockers_s = [tuple(c) for c in sat["common_source_blockers"]]
        blockers_u = [tuple(c) for c in unsat["common_source_blockers"]]
        assert blockers_s == blockers_u == [(i,) for i in range(1, n + 1)]; checks += 1
        assert brute_sat(blockers_s, n); checks += 1
        for m in models_s:
            assert eval_formula(blockers_s, m); checks += 1
        # UNSAT entails every blocker vacuously, but the blocker conjunction is SAT.
        assert not models_u and brute_sat(blockers_u, n); checks += 1

        for row_s, row_u in zip(sat["residuals"], unsat["residuals"]):
            i = int(next(iter(row_s["cube"])))
            assert row_s["cube"] == row_u["cube"] == {str(i): 0}; checks += 1
            assert row_s["learned_source_blocker"] == row_u["learned_source_blocker"] == [i]; checks += 1
            assert not brute_sat(restrict(fs, {i: 0}), n); checks += 1
            assert not brute_sat(restrict(fu, {i: 0}), n); checks += 1

        source_pres_s = fs + blockers_s
        source_pres_u = fu + blockers_u
        assert brute_sat(source_pres_s, n); checks += 1
        assert not brute_sat(source_pres_u, n); checks += 1
        assert sat["source_preserving_clause_count"] >= sat["source_clause_count"]; checks += 1
        assert unsat["source_preserving_clause_count"] >= unsat["source_clause_count"]; checks += 1
        assert sat["source_preserving_literal_tokens"] >= sat["source_literal_tokens"]; checks += 1
        assert unsat["source_preserving_literal_tokens"] >= unsat["source_literal_tokens"]; checks += 1

        if blocks == 1:
            for row in (sat, unsat):
                formula = [tuple(c) for c in row["source_formula"]]
                for target in row["local_clause_targets"]:
                    clause = formula[target["clause_index"]]
                    occ = target["occurrences"]
                    assert [o["literal"] for o in occ] == list(clause); checks += 1
                    assert all(o["S_local_all_literals_true"] == int(o["literal"] > 0)
                               for o in occ); checks += 1
                    assert all(o["U_local_all_literals_false"] != int(o["literal"] > 0)
                               for o in occ); checks += 1
                    assert all(o["invert_S_is_U"] == o["U_local_all_literals_false"]
                               and o["invert_U_is_S"] == o["S_local_all_literals_true"]
                               for o in occ); checks += 1
                for mode in row["source_clause_pair_extremes"]:
                    assert set(mode["modes"]) == {"SS", "SU", "US", "UU"}; checks += 1
                    for key, entry in mode["modes"].items():
                        assert key in {"SS", "SU", "US", "UU"}; checks += 1
                        assert entry["feasible"] == bool(entry["coherent_witness_count"]); checks += 1
                assert len(row["global_endpoints"]["0^n"]["N0_N1_N2_N3"]) == 4; checks += 1

    out = {
        "id": data["id"],
        "independent_checks": checks,
        "status": "PASS",
    }
    text = json.dumps(out, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
