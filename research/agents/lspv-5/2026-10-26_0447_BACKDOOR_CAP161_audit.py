#!/usr/bin/env python3
"""Finite audit for BACKDOOR-CAP161.

The companion report contains the symbolic theorem.  This zero-dependency
program checks finite verifier relations, the exact-cap decision identity,
safe/unsafe fixed-length encodings, and the clock arithmetic used in the
backdoor/SCC specialization.  It uses no randomness.
"""

from __future__ import annotations

import json
from fractions import Fraction
from itertools import product


ASSERTIONS = 0


def check(condition: bool, message: str) -> None:
    global ASSERTIONS
    ASSERTIONS += 1
    if not condition:
        raise AssertionError(message)


def relation_audit() -> dict:
    # Four variable-length proof records; their listed order is the canonical
    # search order used to define the exact minimum accepted index.
    proofs = ("", "0", "1", "00")
    inputs = range(3)
    relations = 0
    yes_points = 0
    for mask in range(1 << (len(proofs) * len(tuple(inputs)))):
        relations += 1
        for x in inputs:
            accepted = [j for j in range(len(proofs))
                        if (mask >> (x * len(proofs) + j)) & 1]
            member = bool(accepted)
            k_star = min(accepted) if accepted else None
            check(member == (k_star is not None), "minimum-cap label mismatch")
            # Enumerating exactly through k_star decides the same membership
            # bit.  On NO inputs the distinguished infinity symbol is required.
            decided = False if k_star is None else any(
                (mask >> (x * len(proofs) + j)) & 1
                for j in range(k_star + 1)
            )
            check(decided == member, "exact cap failed to decide relation")
            yes_points += int(member)
    return {
        "inputs": 3,
        "proof_records": list(proofs),
        "relations_exhausted": relations,
        "yes_points_seen": yes_points,
    }


def padding_audit() -> dict:
    # V accepts exactly the one-bit record '1'.  Replacing a variable-length
    # record by raw zero padding to length two changes its semantics.
    def verifier(pi: str) -> bool:
        return pi == "1"

    raw = "1"
    naive = raw.ljust(2, "0")
    check(verifier(raw), "base proof must accept")
    check(not verifier(naive), "naive padding should be the counterexample")

    # A length-tagged fixed record preserves every proof in Sigma^{<=2}.
    universe = ("", "0", "1", "00", "01", "10", "11")

    def encode(pi: str) -> str:
        # Unary length, delimiter, payload, and zeros to a common width 5.
        return ("1" * len(pi) + "0" + pi).ljust(5, "0")

    def decode(word: str) -> str | None:
        try:
            ell = word.index("0")
        except ValueError:
            return None
        start = ell + 1
        if ell > 2 or start + ell > len(word):
            return None
        pi = word[start:start + ell]
        canonical = ("1" * ell + "0" + pi).ljust(5, "0")
        return pi if canonical == word else None

    encodings = set()
    for pi in universe:
        word = encode(pi)
        check(len(word) == 5, "non-fixed tagged width")
        check(word not in encodings, "tagged encoding collision")
        encodings.add(word)
        check(decode(word) == pi, "tagged round trip failed")
        check(verifier(decode(word) or "") == verifier(pi),
              "tagged verification semantics changed")
    return {
        "naive_counterexample": {"proof": raw, "zero_padded": naive},
        "tagged_records_checked": len(universe),
        "tagged_width": 5,
    }


def clock_audit() -> dict:
    # A short accepting branch coexists with a slow invalid branch.  The
    # best-accepting cost is linear, while nondeterministic time is governed
    # by the worst branch.  We use exact integer costs through N=24.
    rows = []
    for n in range(1, 25):
        best_accept = n + 1
        slow_invalid = 1 << n
        worst_branch = max(best_accept, slow_invalid)
        check(worst_branch == slow_invalid or n == 1,
              "unexpected worst-branch cost")
        check(best_accept <= worst_branch, "minimum exceeded maximum")
        rows.append({"N": n, "best_accept": best_accept,
                     "worst_branch": worst_branch})
    return {"rows": rows, "largest_ratio": rows[-1]["worst_branch"] /
            rows[-1]["best_accept"]}


def backdoor_exponent_audit() -> dict:
    d = Fraction(901, 500)
    c_threshold = Fraction(651000, 361301)
    alpha_threshold = c_threshold - 1
    check(alpha_threshold == Fraction(289699, 361301),
          "alpha threshold arithmetic mismatch")
    check(c_threshold < d, "strict FLMV threshold must lie below d")

    # If r(N)=floor(alpha log_2 N), the reported explicit residual verifier
    # has upper exponent 1+alpha (before additional overhead).  Test exact
    # powers of two so no floating-point logarithm enters the calculation.
    alpha_good = Fraction(4, 5)
    alpha_bad = Fraction(81, 100)
    check(1 + alpha_good < c_threshold, "good alpha lost strict slack")
    check(1 + alpha_bad > c_threshold, "bad alpha unexpectedly inside")
    rows = []
    for j in range(4, 17):
        n = 1 << j
        r_good = (alpha_good.numerator * j) // alpha_good.denominator
        leaves = 1 << r_good
        charged = n * leaves
        check(leaves == 2 ** r_good, "leaf count mismatch")
        check(charged == 2 ** (j + r_good), "charged work mismatch")
        rows.append({"N": n, "log2_N": j, "r_good": r_good,
                     "leaves": leaves, "N_times_leaves": charged})
    return {
        "d": str(d),
        "c_threshold": str(c_threshold),
        "c_threshold_decimal": float(c_threshold),
        "alpha_threshold": str(alpha_threshold),
        "alpha_threshold_decimal": float(alpha_threshold),
        "alpha_good": str(alpha_good),
        "alpha_bad": str(alpha_bad),
        "power_of_two_rows": rows,
    }


def main() -> None:
    result = {
        "run_id": "BACKDOOR-CAP161",
        "deterministic": True,
        "seed": None,
        "relation": relation_audit(),
        "padding": padding_audit(),
        "clock": clock_audit(),
        "backdoor_exponent": backdoor_exponent_audit(),
    }
    result["assertions"] = ASSERTIONS
    result["failures"] = 0
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
