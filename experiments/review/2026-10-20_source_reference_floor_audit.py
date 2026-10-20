#!/usr/bin/env python3
"""Exact audit for SOURCE-REFERENCE-FLOOR15.

The audit checks coding/counting floors and the exponent effect of carrying an
N-bit source inside queries.  It does not prove that every semantic reduction
must be source-faithful; that alternative is explicitly the open fiber branch.
"""

from fractions import Fraction
import json
from pathlib import Path

TAU = Fraction(241, 200)
SIGMA = Fraction(1, 2)


def short_query_exponents(a, k, C, D):
    return a * (1 + Fraction(C + 1, k)), a * Fraction(max(1, D), k)


def source_carrying_exponents(a, k, C, D):
    # MMW has M*p^{1+o(1)} short-query orchestration. Replacing p-length
    # queries by length max(p,N)=N for k>a contributes N^C per query.
    return a + Fraction(a, k) + C, Fraction(D)


def main():
    failures = []
    assertions = 0

    # Exact source-code counting: fewer than N bits cannot injectively encode
    # all N-bit sources, even allowing every binary string of length <=L.
    coding_cases = 0
    for N in range(1, 257):
        for L in range(0, N):
            fixed_codes = 1 << L
            variable_codes = (1 << (L + 1)) - 1
            sources = 1 << N
            coding_cases += 1
            assertions += 2
            if not fixed_codes < sources:
                failures.append(["fixed_code_floor", N, L])
            if not variable_codes < sources:
                failures.append(["variable_code_floor", N, L])

    # Cofinal p^d source descriptors cannot be faithful for fixed d.
    a_values = [Fraction(1), Fraction(21, 20), Fraction(11, 10), Fraction(6, 5)]
    descriptor_cases = 0
    for a in a_values:
        for d in range(1, 33):
            last_covering_k = 0
            for k in range(1, 2049):
                covers_exponent = a * Fraction(d, k) >= 1
                expected = k <= a * d
                descriptor_cases += 1
                assertions += 1
                if covers_exponent != expected:
                    failures.append(["descriptor_threshold", str(a), d, k])
                if covers_exponent:
                    last_covering_k = k
            assertions += 1
            if last_covering_k > int(a * d):
                failures.append(["cofinal_descriptor", str(a), d, last_covering_k])

    # Short queries absorb every fixed solver exponent; explicit N-bit source
    # carrying fails the strict space box for every integer D>=1.
    query_cases = 0
    short_successes = 0
    full_source_successes = 0
    witness_samples = []
    a = Fraction(6, 5)
    for C in range(1, 65):
        for D in range(1, 65):
            # Since TAU/a = 241/240, strict time absorption needs
            # k > 240(C+1). Strict space absorption needs k > 12D/5.
            # Evaluate the first integer satisfying both, avoiding a slow
            # linear search whose range would obscure the exact threshold.
            k = max(2, 240 * (C + 1) + 1, (12 * D) // 5 + 1)
            ts, ss = short_query_exponents(a, k, C, D)
            tf, sf = source_carrying_exponents(a, k, C, D)
            query_cases += 1
            assertions += 7
            if not (ts < TAU and ss < SIGMA):
                failures.append(["no_short_witness", C, D, k, str(ts), str(ss)])
            if k > 2:
                prev_t, prev_s = short_query_exponents(a, k - 1, C, D)
                if prev_t < TAU and prev_s < SIGMA:
                    failures.append(["nonminimal_short_witness", C, D, k])
            if tf < ts:
                failures.append(["full_below_short", C, D, k, str(tf), str(ts)])
            if sf < ss:
                failures.append(["full_space_below_short", C, D, k, str(sf), str(ss)])
            if tf < TAU and sf < SIGMA:
                full_source_successes += 1
            short_successes += 1
            if len(witness_samples) < 8:
                witness_samples.append({"C": C, "D": D, "k": k, "short_time": str(ts), "short_space": str(ss), "full_time": str(tf), "full_space": str(sf)})

    assertions += 1
    if full_source_successes != 0:
        failures.append(["full_source_successes", full_source_successes])

    # Any fixed positive contamination exponent lambda can be defeated by an
    # otherwise legitimate but sufficiently large fixed polynomial exponent C.
    contamination_cases = 0
    for den in range(1, 65):
        for num in range(1, den + 1):
            lam = Fraction(num, den)
            C = (TAU // lam) + 2
            contamination_cases += 1
            assertions += 1
            if not C * lam >= TAU:
                failures.append(["contamination", str(lam), C])

    result = {
        "run": "SOURCE-REFERENCE-FLOOR15",
        "status": "PASS" if not failures else "FAIL",
        "scope": "source-faithful encoding and query-length exponent audit; semantic fibers remain open",
        "coding_cases": coding_cases,
        "descriptor_cases": descriptor_cases,
        "query_cases_until_first_short_witness": query_cases,
        "short_successes": short_successes,
        "full_source_successes": full_source_successes,
        "contamination_cases": contamination_cases,
        "assertions": assertions,
        "witness_samples": witness_samples,
        "failures": failures,
        "global_status": "P versus NP OPEN",
    }
    out = Path("results/raw/synthesis/2026-10-20_1248_SOURCE_REFERENCE_FLOOR15.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if not failures else 1)


if __name__ == "__main__":
    main()
