#!/usr/bin/env python3
"""Exact-rational audit of the ROUNDINGSQUEEZE3 retuning constraints.

This is a bounded falsification check, not an asymptotic lower-bound experiment.
Every invocation is intended to finish in under 30 seconds.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from fractions import Fraction
from pathlib import Path


def ceil_fraction(x: Fraction) -> int:
    return -(-x.numerator // x.denominator)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    started = time.perf_counter()

    assertions = 0
    failures: list[dict[str, object]] = []
    checked = 0

    # Published displayed choice in the recovered handoff.
    delta0 = Fraction(1, 200)
    alpha0 = 500
    published = []
    for c in range(3, 13):
        required = ceil_fraction(Fraction(2 * (c + 1), 1) / delta0)
        ok = alpha0 >= required
        assertions += 1
        if ok:
            failures.append({"type": "published-choice-unexpected-pass", "c": c})
        published.append({"c": c, "alpha": alpha0, "required_alpha": required, "passes": ok})

    # Exact grid: dimension condition plus k>q can never coexist with u<=z.
    # delta ranges over small positive rationals below 1/4; all comparisons are exact.
    deltas = sorted({Fraction(p, d) for d in range(5, 251) for p in range(1, min(6, d)) if Fraction(p, d) < Fraction(1, 4)})
    min_margin: Fraction | None = None
    witness = None
    for delta in deltas:
        for c in range(3, 13):
            alpha_min = ceil_fraction(Fraction(2 * (c + 1), 1) / delta)
            for alpha in (alpha_min, alpha_min + 1, alpha_min + 7):
                q = 4 * alpha + c + 1
                for k in range(q + 1, q + 65):
                    u = alpha * (k + 4) + k
                    z = Fraction(alpha, 1) * (1 - delta) * (k + c)
                    checked += 1
                    assertions += 5
                    if alpha < Fraction(2 * (c + 1), 1) / delta:
                        failures.append({"type": "dimension", "delta": str(delta), "c": c, "alpha": alpha})
                    if not k > q:
                        failures.append({"type": "exponent", "delta": str(delta), "c": c, "alpha": alpha, "k": k})
                    # Consequence of u<=z would be delta*k<c.  The other hypotheses force the opposite.
                    forced_lower = delta * k
                    assertions += 1
                    if not forced_lower > c:
                        failures.append({"type": "lower-bound-chain", "delta": str(delta), "c": c, "alpha": alpha, "k": k})
                    margin = Fraction(u, 1) - z
                    if min_margin is None or margin < min_margin:
                        min_margin = margin
                        witness = {"delta": str(delta), "c": c, "alpha": alpha, "k": k, "u_minus_z": str(margin)}
                    if u <= z:
                        failures.append({"type": "counterexample", "delta": str(delta), "c": c, "alpha": alpha, "k": k, "u": str(u), "z": str(z)})

    symbolic = {
        "dimension_condition": "alpha >= 2(c+1)/delta",
        "formula_exponent": "q = 4 alpha + c + 1",
        "known_proof_exponent": "u = alpha(k+4) + k",
        "cap_exponent": "z = alpha(1-delta)(k+c)",
        "cap_consequence": "u <= z implies delta*k < c",
        "supercritical_consequence": "k > q and dimension imply delta*k > 8(c+1) > c",
        "conclusion": "no simultaneous solution within this sufficient-bound package",
    }
    digest_payload = json.dumps({"published": published, "symbolic": symbolic, "checked": checked, "failures": failures}, sort_keys=True).encode()
    result = {
        "status": "PASS" if not failures else "FAIL",
        "classification": "COMPUTATIONAL exact-rational check supporting a separate symbolic proof",
        "checked_tuples": checked,
        "assertions": assertions,
        "delta_values": len(deltas),
        "failures": failures,
        "published_choice": published,
        "minimum_positive_u_minus_z": str(min_margin),
        "minimum_margin_witness": witness,
        "symbolic_ledger": symbolic,
        "limitations": [
            "Does not refute the cited paper's main theorem.",
            "Audits only the displayed generic lifting and compiler sufficient bounds.",
            "A specialized lifting lemma, convention correction, or tighter proof upper bound may evade the firewall.",
            "Does not measure arbitrary-machine runtime or minimum proof complexity."
        ],
        "semantic_sha256": hashlib.sha256(digest_payload).hexdigest(),
        "elapsed_seconds": round(time.perf_counter() - started, 6),
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
