#!/usr/bin/env python3
"""REFEREE373: actual CANON2R replay of the LSPV-3/434 AND3 firewall.

This authenticates a proposed frozen byte language, not the unresolved historical
R_mix341 serialization.  It changes no rule or weight.
"""
from __future__ import annotations

import copy
import importlib.util
import json
import resource
import time
from itertools import product
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


C2 = load("ref373_canon2", ROOT / "experiments/arc/lspv5_361/rmix341_canon2_repair_referee361.py")
R2 = load("ref373_canon2r", ROOT / "experiments/arc/lspv5_362/rmix341_raw_affine_firewall_referee362.py")

PADDED = [
    [1, 3, 4], [1, 3, -4], [1, -3, 4], [1, -3, -4],
    [-1, 2, 5], [-1, 2, -5], [-1, -2, 6], [-1, -2, -6],
]
ORIGINAL = [[1], [-1, 2], [-1, -2]]

RAW_PADDED = (
    b"c REFEREE373 exact LSPV3-434 padded source\n"
    b"p cnf 6 8\n"
    + b"".join((" ".join(map(str, c)) + " 0\n").encode("ascii") for c in PADDED)
)
RAW_ORIGINAL = (
    b"c REFEREE373 exact unpadded source\n"
    b"p cnf 2 3\n1 0\n-1 2 0\n-1 -2 0\n"
)


def srci(i: int) -> dict:
    return {"src": i, "view": "clause"}


def nodei(i: int, view: str = "clause") -> dict:
    return {"node": i, "view": view}


def res(i: int, left: dict, right: dict, pivot: int, clause: list[int]) -> dict:
    return {"id": i, "rule": "RES", "left": left, "right": right,
            "pivot": pivot, "clause": clause}


def factor_truth(left: list[int], right: list[int], nvars: int):
    support = sorted({abs(x) for x in left + right})
    truth = []
    for bits in range(1 << len(support)):
        env = {v: (bits >> j) & 1 for j, v in enumerate(support)}
        truth.append(C2.eval_clause(tuple(left), env) & C2.eval_clause(tuple(right), env))
    return {"support": support, "truth": truth}


def mixed_13_doc() -> dict:
    s = {"nvars": 6, "clauses": copy.deepcopy(PADDED)}
    ns = [
        res(0, srci(0), srci(1), 4, [1, 3]),
        res(1, srci(2), srci(3), 4, [1, -3]),
        res(2, srci(4), srci(5), 5, [-1, 2]),
        res(3, srci(6), srci(7), 6, [-1, -2]),
        res(4, nodei(1), nodei(2), 1, [2, -3]),
        res(5, nodei(0), nodei(4), 3, [1, 2]),
        {"id": 6, "rule": "AND3", "left": nodei(5), "right": nodei(3),
         "factor": {"support": [1, 2], "truth": [0, 1, 1, 0]},
         "affine": {"mask": [1, 2], "rhs": 1}},
        res(7, nodei(0), nodei(1), 3, [1]),
        res(8, nodei(7), nodei(2), 1, [2]),
        {"id": 9, "rule": "AND3", "left": nodei(7), "right": srci(0),
         "factor": {"support": [1, 3, 4], "truth": [0, 1, 0, 1, 0, 1, 0, 1]},
         "affine": {"mask": [1], "rhs": 1}},
        {"id": 10, "rule": "AND3", "left": nodei(8), "right": nodei(2),
         "factor": {"support": [1, 2], "truth": [0, 0, 1, 1]},
         "affine": {"mask": [2], "rhs": 1}},
        {"id": 11, "rule": "GF2", "left": nodei(9, "affine"),
         "right": nodei(10, "affine"), "affine": {"mask": [1, 2], "rhs": 0}},
        {"id": 12, "rule": "GF2", "left": nodei(11, "affine"),
         "right": nodei(6, "affine"), "affine": {"mask": [], "rhs": 1}},
    ]
    return C2.doc(s, ns, nodei(12, "affine"))


def optimal_7_doc() -> dict:
    s = {"nvars": 6, "clauses": copy.deepcopy(PADDED)}
    ns = [
        res(0, srci(0), srci(1), 4, [1, 3]),
        res(1, srci(2), srci(3), 4, [1, -3]),
        res(2, srci(4), srci(5), 5, [-1, 2]),
        res(3, srci(6), srci(7), 6, [-1, -2]),
        res(4, nodei(0), nodei(1), 3, [1]),
        res(5, nodei(2), nodei(3), 2, [-1]),
        res(6, nodei(4), nodei(5), 1, []),
    ]
    return C2.doc(s, ns, nodei(6))


def optimal_2_doc(source=None) -> dict:
    s = source or {"nvars": 2, "clauses": copy.deepcopy(ORIGINAL)}
    ns = [
        res(0, srci(1), srci(2), 2, [-1]),
        res(1, srci(0), nodei(0), 1, []),
    ]
    return C2.doc(s, ns, nodei(1))


def naive_replay_doc(correct_factor: bool, affine: dict | None = None) -> dict:
    s = {"nvars": 2, "clauses": copy.deepcopy(ORIGINAL)}
    got = factor_truth([1], [-1, -2], 2)
    f = got if correct_factor else {"support": [1, 2], "truth": [0, 1, 1, 0]}
    n = {"id": 0, "rule": "AND3", "left": srci(0), "right": srci(2), "factor": f}
    if affine is not None:
        n["affine"] = affine
    return C2.doc(s, [n], nodei(0, "affine" if affine is not None else "factor"))


def expect_reject(fn, needle: str | None = None) -> str:
    try:
        fn()
    except (C2.Reject, R2.RawReject) as exc:
        msg = str(exc)
        if needle is not None:
            assert needle in msg, (needle, msg)
        return msg
    raise AssertionError("unexpected acceptance")


def sat_clause(clause, assignment):
    return any(assignment[abs(x)] == int(x > 0) for x in clause)


def deletion_witnesses():
    out = []
    for gone in range(len(PADDED)):
        witness = None
        for bits in product((0, 1), repeat=6):
            env = {i + 1: bits[i] for i in range(6)}
            if all(i == gone or sat_clause(c, env) for i, c in enumerate(PADDED)):
                witness = [env[i] for i in range(1, 7)]
                break
        assert witness is not None
        out.append(witness)
    return out


def original_deletion_witnesses():
    out = []
    for gone in range(len(ORIGINAL)):
        witness = None
        for bits in product((0, 1), repeat=2):
            env = {i + 1: bits[i] for i in range(2)}
            if all(i == gone or sat_clause(c, env) for i, c in enumerate(ORIGINAL)):
                witness = [env[1], env[2]]
                break
        assert witness is not None
        out.append(witness)
    return out


def span(nodes):
    depths = []
    for n in nodes:
        parents = []
        for key in ("left", "right", "parent"):
            r = n.get(key)
            if isinstance(r, dict) and "node" in r:
                parents.append(r["node"])
        depths.append(1 + max((depths[p] for p in parents), default=0))
    return max(depths, default=0)


def main() -> None:
    started = time.perf_counter()
    parsed_padded = R2.parse_strict_dimacs(RAW_PADDED)
    parsed_original = R2.parse_strict_dimacs(RAW_ORIGINAL)
    assert parsed_padded == {"nvars": 6, "clauses": PADDED}
    assert parsed_original == {"nvars": 2, "clauses": ORIGINAL}
    assert all(len(c) == 3 and len({abs(x) for x in c}) == 3 for c in PADDED)

    mixed = mixed_13_doc()
    opt7 = optimal_7_doc()
    opt2 = optimal_2_doc()
    mixed_stats = C2.Checker(mixed, parsed_padded).run()
    opt7_stats = C2.Checker(opt7, parsed_padded).run()
    opt2_stats = C2.Checker(opt2, parsed_original).run()
    mixed_wrapped = R2.wrap(RAW_PADDED, mixed)
    opt7_wrapped = R2.wrap(RAW_PADDED, opt7)
    opt2_wrapped = R2.wrap(RAW_ORIGINAL, opt2)
    mixed_wrap_stats = R2.check_wrapper(mixed_wrapped)
    opt7_wrap_stats = R2.check_wrapper(opt7_wrapped)
    opt2_wrap_stats = R2.check_wrapper(opt2_wrapped)

    naive_wrong = expect_reject(
        lambda: C2.Checker(naive_replay_doc(False, {"mask": [1, 2], "rhs": 1}), parsed_original).run(),
        "wrong AND3 table")

    correct_factor = factor_truth([1], [-1, -2], 2)
    assert correct_factor == {"support": [1, 2], "truth": [0, 1, 0, 0]}
    affine_rejections = []
    for mask in ([], [1], [2], [1, 2]):
        for rhs in (0, 1):
            a = {"mask": mask, "rhs": rhs}
            reason = expect_reject(lambda a=a: C2.Checker(naive_replay_doc(True, a), parsed_original).run(),
                                   "false affine annotation")
            affine_rejections.append({"affine": a, "reason": reason})

    witnesses = deletion_witnesses()
    assert len(witnesses) == 8
    original_witnesses = original_deletion_witnesses()
    assert len(original_witnesses) == 3

    # Both-label and corruption controls.
    sat_source = {"nvars": 2, "clauses": [[1], [-1, 2], [-1, 2]]}
    sat_reason = expect_reject(lambda: C2.Checker(optimal_2_doc(sat_source), sat_source).run(),
                               "not an oriented resolvent")
    bad_mixed = copy.deepcopy(mixed)
    bad_mixed["nodes"][6]["affine"]["rhs"] = 0
    corrupt_affine = expect_reject(lambda: C2.Checker(bad_mixed, parsed_padded).run(),
                                   "false affine annotation")
    bad_hash = R2.wrap(RAW_PADDED, opt7)
    bad_hash["source_raw_sha256"] = "0" * 64
    hash_reason = expect_reject(lambda: R2.check_wrapper(bad_hash), "raw hash mismatch")
    malformed_raw = RAW_PADDED.replace(b"p cnf 6 8", b"p cnf 6 9")
    malformed_reason = expect_reject(lambda: R2.parse_strict_dimacs(malformed_raw), "clause count mismatch")

    elapsed = time.perf_counter() - started
    result = {
        "artifact": "REFEREE373",
        "status": "PASS",
        "scope": "actual frozen proposed CANON2/CANON2R bytes; not historical /341 authority",
        "sources": {
            "padded": {"nvars": 6, "clauses": 8, "proper_strict_3cnf": True,
                       "raw_sha256": R2.raw_sha(RAW_PADDED)},
            "original": {"nvars": 2, "clauses": 3, "raw_sha256": R2.raw_sha(RAW_ORIGINAL)},
        },
        "accepted": {
            "mixed_13": {"checker": mixed_stats, "wrapper": mixed_wrap_stats,
                         "distinct_nodes": 13, "span": span(mixed["nodes"])},
            "padded_optimal_7": {"checker": opt7_stats, "wrapper": opt7_wrap_stats,
                                 "distinct_nodes": 7, "span": span(opt7["nodes"])},
            "original_optimal_2": {"checker": opt2_stats, "wrapper": opt2_wrap_stats,
                                   "distinct_nodes": 2, "span": span(opt2["nodes"])},
        },
        "strengthening_firewall": {
            "old_exact_factor_canon2_truth_order": [0, 1, 1, 0],
            "strengthened_factor_canon2_truth_order": correct_factor["truth"],
            "semantic_00011011_order_used_by_peer": [0, 0, 1, 0],
            "discriminator": {"u": 0, "v": 1},
            "naive_exact_replay": naive_wrong,
            "all_affine_annotations_rejected": affine_rejections,
            "conclusion": "proper-subclause replacement is not a transparent exact AND3/GF2 port",
        },
        "minimum_certificate": {
            "padded_all_sources_indispensable": True,
            "deletion_witnesses": witnesses,
            "binary_ancestry_lower_bound": 7,
            "accepted_matching_upper_bound": 7,
            "original_all_sources_indispensable": True,
            "original_deletion_witnesses": original_witnesses,
            "original_binary_ancestry_lower_bound": 2,
            "accepted_original_upper_bound": 2,
        },
        "hostile_controls": {
            "sat_same_sign_source": sat_reason,
            "corrupt_affine": corrupt_affine,
            "raw_hash_mismatch": hash_reason,
            "malformed_clause_count": malformed_reason,
        },
        "status_ledger": {
            "verbatim_strengthening_to_exact_AND3_GF2": "FALSIFIED_BY_ACTUAL_CHECKER",
            "typed_global_polynomial_repair": "OPEN; finite fixture has accepted 2-node alternative",
            "historical_rmix341_bytes": "OPEN",
            "same_R_B3": "OPEN",
            "P_vs_NP": "OPEN",
        },
        "resource_ledger": {
            "producer_seconds": elapsed,
            "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "logical_xor_trace": "not used",
            "proof_search": "not charged to W; construction and exhaustive controls charged here",
        },
    }
    out_dir = ROOT / "results/raw/arc"
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_path = out_dir / "2026-11-05_1648_LSPV5_REFEREE373_raw.json"
    cert_path = out_dir / "2026-11-05_1648_LSPV5_REFEREE373_certificates.json"
    raw_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    cert_path.write_text(json.dumps({
        "mixed_13_canon2r": mixed_wrapped,
        "padded_optimal_7_canon2r": opt7_wrapped,
        "original_optimal_2_canon2r": opt2_wrapped,
    }, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
