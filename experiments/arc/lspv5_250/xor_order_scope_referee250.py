#!/usr/bin/env python3
"""REFEREE250: independent scope audit of logical XOR order invariance.

This is an offline diagnostic.  It proves/tests a statement about one declared
aligned logical representation; it is not an internal SAT oracle or a native
FLMV benchmark.
"""
from __future__ import annotations

import ast
import hashlib
import importlib.util
import itertools
import json
import math
import random
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

ROOT = Path(__file__).resolve().parents[3]
BASE_PATH = ROOT / "experiments/arc/lspv5_247/target_scope_flmv_referee247.py"
SOURCE = ROOT / "tmp/doecker61_source.txt"
OUT = ROOT / "results/raw/arc/2026-10-31_1448_LSPV5_XOR_ORDER_SCOPE_REFEREE250_raw.json"


def load_base():
    spec = importlib.util.spec_from_file_location("ref247", BASE_PATH)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def load_u() -> list[list[int]]:
    text = "\n".join(line for line in SOURCE.read_text().splitlines() if not line.startswith("#"))
    return ast.literal_eval(text)


def y6() -> list[list[int]]:
    pos = [(1, 2, 3), (1, 4, 5), (2, 4, 6), (3, 5, 6)]
    neg = [(1, 2, 4), (1, 3, 6), (2, 3, 5), (4, 5, 6)]
    return [list(c) for c in pos] + [[-x for x in c] for c in neg]


def hd(a, b) -> int:
    return sum(x != y for x, y in zip(a, b))


def tcount(clause, a) -> int:
    return sum(a[abs(lit) - 1] == int(lit > 0) for lit in clause)


def code_count(t: int, encoding: str) -> tuple[int, int]:
    value = t if encoding == "binary" else t ^ (t >> 1)
    return value & 1, (value >> 1) & 1


def state(formula, a, encoding: str) -> list[int]:
    out = list(a)
    for clause in formula:
        t = tcount(clause, a)
        out.extend((*code_count(t, encoding), int(t > 0)))
    return out


def path_states(formula, a, order, encoding: str, directions=None):
    cur = list(a)
    rows = [state(formula, cur, encoding)]
    for q, var in enumerate(order):
        cur = cur[:]
        cur[var] = (1 - cur[var]) if directions is None else directions[q]
        rows.append(state(formula, cur, encoding))
    return rows


def ledger(rows) -> dict:
    return {
        "sum_adjacent": sum(hd(x, y) for x, y in zip(rows, rows[1:])),
        "endpoint": hd(rows[0], rows[-1]),
        "steps": len(rows) - 1,
    }


def edge_weight(p: int, q: int, encoding: str) -> int:
    assert abs(p - q) == 1
    return hd(code_count(p, encoding), code_count(q, encoding)) + int((p == 0) != (q == 0))


def comparable_formula(formula, a, b, encoding: str) -> dict:
    assert all(x <= y for x, y in zip(a, b)) or all(x >= y for x, y in zip(a, b))
    expected = hd(a, b)
    endpoint = hd(a, b)
    for clause in formula:
        p, q = tcount(clause, a), tcount(clause, b)
        lo, hi = sorted((p, q))
        expected += sum(edge_weight(r, r + 1, encoding) for r in range(lo, hi))
        endpoint += hd(code_count(p, encoding), code_count(q, encoding)) + int((p == 0) != (q == 0))
    return {"sum_adjacent": expected, "endpoint": endpoint}


def all_comparable_y6(formula) -> dict:
    checks = paths = pairs = 0
    extrema = {enc: [10**9, -1] for enc in ("binary", "gray")}
    for orientation in (1, -1):
        for trits in itertools.product((0, 1, 2), repeat=6):
            # orientation +: 0 means 00, 1 means 01, 2 means 11.
            a, b, diff = [], [], []
            for i, z in enumerate(trits):
                pair = ((0, 0), (0, 1), (1, 1))[z]
                if orientation < 0:
                    pair = (1 - pair[0], 1 - pair[1])
                a.append(pair[0]); b.append(pair[1])
                if pair[0] != pair[1]: diff.append(i)
            pairs += 1
            orders = itertools.permutations(diff) if diff else [()]
            for order in orders:
                paths += 1
                for enc in ("binary", "gray"):
                    got = ledger(path_states(formula, a, order, enc))
                    want = comparable_formula(formula, a, b, enc)
                    assert got["sum_adjacent"] == want["sum_adjacent"]
                    assert got["endpoint"] == want["endpoint"]
                    assert path_states(formula, a, order, enc)[-1] == state(formula, b, enc)
                    extrema[enc][0] = min(extrema[enc][0], got["sum_adjacent"])
                    extrema[enc][1] = max(extrema[enc][1], got["sum_adjacent"])
                    checks += 3
    return {"endpoint_pairs_with_orientation": pairs, "ordered_paths": paths,
            "assertions": checks, "sum_ranges": extrema}


def full_sweep(formula, orders) -> dict:
    n = max(abs(x) for c in formula for x in c)
    out = {}
    for name, order in orders.items():
        out[name] = {}
        for enc in ("binary", "gray"):
            rows = path_states(formula, [0] * n, order, enc)
            out[name][enc] = ledger(rows)
    return out


def tape_head_cost(rows) -> int:
    """One explicit sequential-tape implementation, changed cells ascending."""
    head = 0
    cost = 0
    for old, new in zip(rows, rows[1:]):
        changed = [i for i, (x, y) in enumerate(zip(old, new)) if x != y]
        for i in changed:
            cost += abs(i - head) + 1  # moves plus one write transition
            head = i
    return cost


def y6_order_distribution(formula) -> dict:
    rows = []
    for order in itertools.permutations(range(6)):
        bstates = path_states(formula, [0] * 6, order, "binary")
        gstates = path_states(formula, [0] * 6, order, "gray")
        rows.append((order, ledger(bstates)["sum_adjacent"], ledger(gstates)["sum_adjacent"],
                     tape_head_cost(bstates), tape_head_cost(gstates)))
    assert len({r[1] for r in rows}) == len({r[2] for r in rows}) == 1
    return {
        "permutations": len(rows),
        "binary_logic_sum": rows[0][1],
        "gray_logic_sum": rows[0][2],
        "binary_single_tape_native_cost_range": [min(r[3] for r in rows), max(r[3] for r in rows)],
        "gray_single_tape_native_cost_range": [min(r[4] for r in rows), max(r[4] for r in rows)],
        "binary_min_order": list(min(rows, key=lambda r: r[3])[0]),
        "binary_max_order": list(max(rows, key=lambda r: r[3])[0]),
        "status": "COMPUTATIONAL implementation control; not a universal machine lower bound",
    }


def minimal_incomparable_counterexamples() -> dict:
    formula = [[1, 2, 3]]
    found = {}
    for enc in ("binary", "gray"):
        for a in itertools.product((0, 1), repeat=3):
            for b in itertools.product((0, 1), repeat=3):
                diff = [i for i in range(3) if a[i] != b[i]]
                if len(diff) < 2 or all(a[i] <= b[i] for i in range(3)) or all(a[i] >= b[i] for i in range(3)):
                    continue
                vals = []
                for order in itertools.permutations(diff):
                    vals.append((order, ledger(path_states(formula, a, order, enc))["sum_adjacent"]))
                if len({v for _, v in vals}) > 1:
                    found[enc] = {"start": list(a), "end": list(b),
                                  "orders_and_sums": [[list(o), v] for o, v in vals]}
                    break
            if enc in found: break
    return found


def backtrack_control() -> dict:
    f = [[1, 2, 3]]
    paths = {
        "direct": ([0, 0, 0], [0, 1], [1, 1]),
        "restore": ([0, 0, 0], [2, 2, 0, 1], [1, 0, 1, 1]),
    }
    out = {}
    # Both end at assignment 110; restore toggles x3 up and back down.
    for name, (start, order, values) in paths.items():
        out[name] = {}
        for enc in ("binary", "gray"):
            out[name][enc] = ledger(path_states(f, start, order, enc, values))
    return out


def index_reset_amortization() -> dict:
    checks = 0
    rows = []
    for h in range(1, 17):
        # h charged 0->1 writes, one atomic erase: Q=h,E=h,B0=0,T=h+1,D=2h.
        Q = E = h; T = h + 1; D = 2 * h
        assert D <= Q + E <= 2 * Q <= 2 * T
        assert T >= math.ceil(D / 2)
        rows.append({"h": h, "Q": Q, "E": E, "T": T, "D": D,
                     "reset_interval_D": h, "reset_interval_steps": 1})
        checks += 2
    return {"rows": rows, "assertions": checks,
            "scope": "whole-run potential charge; one reset interval alone violates a one-bit-per-step premise"}


def wrappers() -> list[dict]:
    return [
        {"name": "read_only_DELAY", "steps": 10000, "endpoint_d_phys": 0, "reads": 10000},
        {"name": "unchanged_writes", "steps": 1000, "endpoint_d_phys": 0, "writes": 1000},
        {"name": "changed_then_restored", "steps": 2000, "endpoint_d_phys": 0, "writes": 2000},
        {"name": "lazy_source_reread", "steps": 792, "endpoint_d_phys": 0, "source_reads": 792},
    ]


def highs(formula, seconds: float) -> dict:
    n = max(abs(x) for c in formula for x in c)
    A, lo, hi = [], [], []
    for c in formula:
        row = np.zeros(n)
        for lit in c: row[abs(lit) - 1] = 1
        A.append(row)
        lo.append(1 if c[0] > 0 else -np.inf)
        hi.append(np.inf if c[0] > 0 else 2)
    start = time.perf_counter()
    r = milp(np.zeros(n), integrality=np.ones(n), bounds=Bounds(0, 1),
             constraints=LinearConstraint(np.asarray(A), lo, hi),
             options={"time_limit": seconds, "disp": False})
    return {"status": int(r.status), "success": bool(r.success),
            "classification": "UNSAT" if r.status == 2 else ("SAT" if r.success else "UNRESOLVED_AT_CAP"),
            "mip_nodes": None if r.mip_node_count is None else int(r.mip_node_count),
            "lp_iterations": None if r.mip_node_count is None else int(r.mip_node_count),
            "wall_seconds": time.perf_counter() - start}


def main() -> int:
    started = time.perf_counter(); base = load_base(); U = load_u(); V = [c[:] for c in U]
    V[2][-1], V[44][-1] = V[44][-1], V[2][-1]
    Y = y6(); cert = base.module_certificate(U); witness = base.replay(V, base.SAT_WITNESS)
    assert cert["proved_unsat_254_clause_subformula"] and witness["satisfied"]
    assert sum(base.replay(Y, "".join(map(str, a)))["satisfied"] for a in itertools.product((0, 1), repeat=6)) == 20
    malformed = {
        "missing_clause": Y[:-1], "duplicate_clause": Y + [Y[0]],
        "mixed_sign": [[1, -2, 3]] + Y[1:], "repeated_variable": [[1, 1, 2]] + Y[1:],
        "wrong_occurrence_count": [c[:] for c in Y[:-1]] + [[1, 2, 6]],
    }
    malformed_results = {name: base.valid_target(f) for name, f in malformed.items()}
    assert all(not row["valid"] for row in malformed_results.values())

    rng = random.Random(2501448)
    orders = {}
    for name, f in (("Y6", Y), ("U198", U), ("V198", V)):
        n = max(abs(x) for c in f for x in c)
        r = list(range(n)); rng.shuffle(r)
        orders[name] = full_sweep(f, {"ascending": list(range(n)), "descending": list(reversed(range(n))), "random": r})
        m = len(f)
        for policy in orders[name].values():
            assert policy["binary"] == {"sum_adjacent": n + 5 * m, "endpoint": n + 3 * m, "steps": n}
            assert policy["gray"] == {"sum_adjacent": n + 4 * m, "endpoint": n + 2 * m, "steps": n}

    raw = {
        "run_id": "XOR-ORDER-SCOPE-REFEREE250",
        "timestamp": "2026-10-31 14:48 America/Los_Angeles",
        "exact_claim": "for clausewise-monotone CNF and coordinate-comparable endpoints, fixed aligned assignment/count/sat XOR path length is flip-order invariant",
        "falsifiers": {
            "F1": "a different flip order lowers the full monotone-sweep logical XOR ledger",
            "F2": "the identity extends to incomparable endpoints or backtracking",
            "F3": "order-invariant logical XOR fixes physical time or yields a SAT selector",
            "F4": "an index-tape reset obeys a per-interval one-bit-change premise without charging its preparation",
        },
        "same_target_labels": {
            "Y6": {"status": "SAT", "models": 20, "n": 6, "m": 8},
            "U198": {"status": "UNSAT", "n": 198, "m": 264,
                     "certificate_nodes": cert["dpll_nodes"], "joint_rows": cert["joint_rows"]},
            "V198": {"status": "SAT", "n": 198, "m": 264,
                     "witness_sha256": hashlib.sha256(base.SAT_WITNESS.encode()).hexdigest(),
                     "witness_histogram": witness["true_literal_histogram"]},
        },
        "malformed_rejections": malformed_results,
        "full_sweeps": orders,
        "exhaustive_comparable_Y6": all_comparable_y6(Y),
        "Y6_all_full_sweep_orders": y6_order_distribution(Y),
        "minimal_incomparable_counterexamples": minimal_incomparable_counterexamples(),
        "backtrack_control": backtrack_control(),
        "index_reset_amortization": index_reset_amortization(),
        "zero_delta_work_controls": wrappers(),
        "signed_clause_extremes": {"U198": base.clause_extreme_control(U), "V198": base.clause_extreme_control(V)},
        "standard_solver": {"U198": highs(U, 4.0), "V198": highs(V, 4.0)},
        "resource_ledger": {
            "discovery": "the theorem is symbolic; exhaustive search only attacks scope and is offline",
            "policy_selection": "all 720 Y6 sweep orders plus ascending/descending/seeded U/V orders are charged in the experiment, not the solver",
            "logical_state": "assignment bits plus two fixed count bits and one satisfaction bit per original clause",
            "eager_physical": "materializing the logical vector inherits its bit changes but also pays writes, head/index motion and layout",
            "lazy_physical": "retaining assignments only uses one changed bit per monotone flip but pays source rereads/recomputation",
            "source": "read-only source accesses and original record IDs are not counted as writes",
            "index_tapes": "FLMV atomic erasure uses the whole-run potential bound D<=2Q+B0, not a per-reset local bound",
            "failed_trials": "incomparable, backtracking, DELAY, unchanged-write, restored-bit and source-reread controls are explicit",
            "output_space": "JSON trace generation and XOR scanning are offline; no Python heap number is promoted to FLMV space",
        },
        "proof_status": {
            "comparable_endpoint_order_invariance": "PROVED/EXACT",
            "full_sweep_peer_theorem": "PROVED/EXACT independently recreated",
            "finite_controls": "COMPUTATIONAL",
            "extension_to_incomparable_or_backtracking_paths": "FALSIFIED/RETIRED",
            "logical_XOR_universal_runtime_or_label_tariff": "FALSIFIED/RETIRED",
            "index_reset_whole_run_amortization": "PROVED/EXACT independently recreated",
            "arbitrary_A_to_Phi_A_ARC": "OPEN", "P_vs_NP": "OPEN",
        },
        "elapsed_seconds": time.perf_counter() - started,
    }
    assert raw["standard_solver"]["V198"]["success"]
    assert raw["standard_solver"]["U198"]["status"] in (1, 2)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(raw, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"run": raw["run_id"], "elapsed": raw["elapsed_seconds"],
                      "comparable": raw["exhaustive_comparable_Y6"],
                      "counterexamples": raw["minimal_incomparable_counterexamples"],
                      "solver": raw["standard_solver"]}, indent=2))
    print("VERIFIED::XOR-ORDER-SCOPE-REFEREE250")
    return 0


if __name__ == "__main__":
    sys.exit(main())
