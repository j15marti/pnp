#!/usr/bin/env python3
"""Independent structural verifier for the REFEREE247 raw record."""
from __future__ import annotations

import json
import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "results/raw/arc/2026-10-31_1148_LSPV5_TARGET_SCOPE_FLMV_REFEREE247_raw.json"
SOURCE = ROOT / "tmp/doecker61_source.txt"


def load_source():
    text = "\n".join(x for x in SOURCE.read_text().splitlines() if not x.startswith("#"))
    return ast.literal_eval(text)


def sat_first_literal(clauses, seed):
    """Second implementation: immutable sets and first-literal branching."""
    def reduce(cs, lit):
        out = []
        for c in cs:
            if lit in c:
                continue
            nc = c - {-lit}
            if not nc:
                return None
            out.append(nc)
        return out

    cs = [frozenset(c) for c in clauses]
    for v, value in seed.items():
        cs = reduce(cs, v if value else -v)
        if cs is None:
            return False

    def rec(state):
        if not state:
            return True
        unit = next((next(iter(c)) for c in state if len(c) == 1), None)
        if unit is not None:
            nxt = reduce(state, unit)
            return False if nxt is None else rec(nxt)
        lit = next(iter(state[0]))
        for choice in (lit, -lit):
            nxt = reduce(state, choice)
            if nxt is not None and rec(nxt):
                return True
        return False

    return rec(cs)


def independent_boundary_certificate():
    u = load_source()
    allowed = []
    for i in range(6):
        module = u[2 + 42 * i:2 + 42 * (i + 1)]
        rows = []
        for mask in range(64):
            seed = {v: bool((mask >> (v - 193)) & 1) for v in range(193, 199)}
            if sat_first_literal(module, seed):
                rows.append(mask)
        allowed.append(rows)
    globals_ok = []
    for mask in range(64):
        seed = {v: bool((mask >> (v - 193)) & 1) for v in range(193, 199)}
        if all(any(seed[abs(l)] == (l > 0) for l in c) for c in u[:2]):
            globals_ok.append(mask)
    return [len(x) for x in allowed], sorted(set(globals_ok).intersection(*map(set, allowed)))


def main() -> int:
    d = json.loads(RAW.read_text())
    f = d["fixtures"]
    allowed_counts, joint_rows = independent_boundary_certificate()
    checks = {
        "U_valid_target": f["U"]["syntax"]["valid"],
        "V_valid_target": f["V"]["syntax"]["valid"],
        "U_shape_198_264": (f["U"]["syntax"]["variables"], f["U"]["syntax"]["clauses"]) == (198, 264),
        "V_shape_198_264": (f["V"]["syntax"]["variables"], f["V"]["syntax"]["clauses"]) == (198, 264),
        "U_exact_occurrences": f["U"]["extreme_control"]["occurrence_count"] == 792,
        "U_all_pairs_covered_once": f["U"]["extreme_control"]["pair_count"] == 264 * 263 // 2,
        "U_independent_unsat": f["U"]["independent_unsat_certificate"]["proved_unsat_254_clause_subformula"],
        "U_no_boundary_row_survives": f["U"]["independent_unsat_certificate"]["joint_rows"] == [],
        "V_witness_satisfies_all": f["V"]["witness_replay"]["satisfied"],
        "V_no_false_clause": f["V"]["witness_replay"]["false_clause_indices"] == [],
        "both_baselines_capped_unknown": all(f[x]["baseline_cap_5000"]["status"] == "UNKNOWN" for x in ("U", "V")),
        "independent_DPLL_allowed_counts_match": allowed_counts == [48, 56, 56, 48, 56, 48],
        "independent_DPLL_no_joint_row": joint_rows == [],
    }
    print(json.dumps(checks, indent=2, sort_keys=True))
    if not all(checks.values()):
        return 1
    print("VERIFIED::TARGET-SCOPE-FLMV-REFEREE247")
    return 0


if __name__ == "__main__":
    sys.exit(main())
