#!/usr/bin/env python3
"""Audit the MUS split-normalization hypotheses for the bridge core.

This script does not search the 36-leaf proof space.  It authenticates the
finite premises used by the symbolic theorem and imports the independently
replayed REFEREE388 side-closure result by exact SHA-256.
"""

from __future__ import annotations

import hashlib
import json
import resource
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
R386 = ROOT / "results/raw/review/2026-11-06_0548_LSPV5_BRIDGE_CUT_TOPOLOGY386.json"
R388 = ROOT / "results/raw/review/2026-11-06_0748_LSPV5_READONCE_RESOLUTION388.json"
V388 = ROOT / "results/raw/review/2026-11-06_0748_LSPV5_READONCE_RESOLUTION388_verification.json"
C389 = ROOT / "results/raw/review/2026-11-06_0848_LSPV5_SPLIT_ROR_COUNTEREXAMPLE389.json"
S389 = ROOT / "results/raw/review/2026-11-06_0848_LSPV5_SPLIT_ROR_MUS389_w3_s6.json"
G389 = ROOT / "results/raw/review/2026-11-06_0848_LSPV5_SPLIT_ROR_MUS_GADGET389.json"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clause_sat(c, mask):
    return any(((mask >> (abs(l) - 1)) & 1) == (l > 0) for l in c)


def models(clauses, variables=15):
    return [m for m in range(1 << variables) if all(clause_sat(c, m) for c in clauses)]


def main():
    start = time.perf_counter()
    r386 = json.loads(R386.read_text())
    r388 = json.loads(R388.read_text())
    v388 = json.loads(V388.read_text())
    c389 = json.loads(C389.read_text())
    s389 = json.loads(S389.read_text())
    g389 = json.loads(G389.read_text())

    clauses = r386["source"]["clauses"]
    core_ids = r386["core"]
    core = [clauses[i] for i in core_ids]
    left_ids = r388["left_source_ids"]
    right_ids = r388["right_source_ids"]
    left = [clauses[i] for i in left_ids]
    right = [clauses[i] for i in right_ids]

    core_models = models(core)
    deletion_models = []
    for i in range(len(core)):
        ms = models(core[:i] + core[i + 1 :])
        deletion_models.append(len(ms))
        if not ms:
            raise AssertionError(f"core deletion {i} remained UNSAT")
    if core_models:
        raise AssertionError("core unexpectedly SAT")

    left_models = models(left)
    right_models = models(right)
    if not left_models or not right_models:
        raise AssertionError("a split side is not satisfiable")
    if any(((m >> 14) & 1) == 0 for m in left_models):
        raise AssertionError("left does not force +15")
    if any(((m >> 14) & 1) == 1 for m in right_models):
        raise AssertionError("right does not force -15")

    lvars = {abs(l) for c in left for l in c}
    rvars = {abs(l) for c in right for l in c}
    shared = sorted(lvars & rvars)
    if shared != [15]:
        raise AssertionError(f"unexpected shared variables {shared}")
    if any(-15 in c for c in left):
        raise AssertionError("wrong-polarity -15 occurs on left")
    if any(15 in c for c in right):
        raise AssertionError("wrong-polarity +15 occurs on right")

    if sha256(R388) != "051f0c0596b788c3b14116d1acfaf35ca1a2325c22d55ec8e756f4ef1cf2e470":
        raise AssertionError("REF388 raw hash mismatch")
    if sha256(V388) != "db9ec0acd0390cfa75a4e4f91e016fd15c469b036faa0a2b5bac84ad7f16487c":
        raise AssertionError("REF388 verification hash mismatch")
    if not v388["pass"] or v388["left_target_found"] or v388["right_target_found"]:
        raise AssertionError("REF388 verification status mismatch")

    unrestricted = c389["unrestricted_counterexample"]
    if unrestricted["total_sources"] != 5 or unrestricted["right_target_present"]:
        raise AssertionError("five-source falsifier record mismatch")
    if s389["counterexample"] is not None or g389["counterexample"] is not None:
        raise AssertionError("finite MUS control unexpectedly found a counterexample")

    record = {
        "run": "LSPV-5/REFEREE389",
        "timestamp_pst": "2026-11-06 08:48 PST",
        "status": "PROVED_RESTRICTED_PLUS_COMPUTATIONAL",
        "theorem": {
            "name": "MUS one-cut source-once Resolution normalization",
            "scope": "pure strict oriented binary Resolution; split CNF L(X,b) and R(Y,b); X,Y disjoint; both sides satisfiable; union minimally UNSAT",
            "conclusion": "a global source-once refutation exists iff both side-unit source-once derivations exist (opposite forced b values), followed by one final RES",
            "proof_steps": [
                "semantic one-bit separation forces opposite values of b",
                "minimality forbids the wrong b polarity on each side",
                "restrict a global tree by a satisfying assignment of the opposite side",
                "source-once restriction normalization plus minimality preserves every local source",
                "lift the restricted private-variable tree; the only restored shared literal has one polarity, so the root is the forced unit",
            ],
            "necessary_hypothesis_falsifier": "five-source non-MUS split 2-CNF has an interleaved global ROR but no full-source right-unit ROR",
        },
        "bridge": {
            "source_dimacs_sha256": r386["source"]["dimacs_sha256"],
            "variables": r386["source"]["variables"],
            "source_clauses": len(clauses),
            "core_clauses": len(core),
            "core_models": len(core_models),
            "core_deletion_model_counts": deletion_models,
            "left_source_ids": left_ids,
            "right_source_ids": right_ids,
            "shared_variables": shared,
            "left_models": len(left_models),
            "right_models": len(right_models),
            "left_forces_positive_15": True,
            "right_forces_negative_15": True,
            "wrong_polarity_absent": True,
            "ref388_full_outcomes_each": v388["full_outcomes_each"],
            "ref388_pair_tests_each": v388["pair_tests_each"],
            "ref388_targets_absent": True,
            "new_consequence": "no pure-Resolution 35-node bridge refutation, including interleaved trees",
            "remaining_interval_full_mixed": [35, 37],
        },
        "finite_controls": {
            "five_source_unrestricted_falsifier": unrestricted,
            "small_mus_width3_two_private_each": {
                "candidate_universe": s389["candidate_universe"],
                "minimal_entailing_pool": s389["minimal_entailing_pool"],
                "counterexample": s389["counterexample"],
            },
            "non_ror_mus_weakened_gadget_pairs": len(g389["tested"]),
            "non_ror_mus_gadget_counterexample": g389["counterexample"],
        },
        "imported_sha256": {str(p.relative_to(ROOT)): sha256(p) for p in (R386, R388, V388, C389, S389, G389)},
        "limits": [
            "does not exclude mixed AND3/XOR/RES 35-node trees",
            "does not address any 36-node topology",
            "does not authenticate an unavailable historical byte checker",
            "does not prove superpolynomial mixed work or B1/B2/B3",
        ],
        "producer_wall_seconds": time.perf_counter() - start,
        "producer_max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }
    out = ROOT / "results/raw/review/2026-11-06_0848_LSPV5_BRIDGE_MUS_NORMALIZATION389.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    print(json.dumps(record, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
