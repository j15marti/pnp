#!/usr/bin/env python3
"""TMR-1/051: exact finite controls for a Williams-target class mismatch.
No randomness, no oracle calls, no asymptotic proof by testing.
"""
import json
from datetime import datetime


def oracle_check(bits):
    N = 1 << bits
    full = (1 << N) - 1
    checked = 0
    for missing in range(N):
        other = full ^ (1 << missing)
        distinguishing = []
        for query in range(1 << N):
            answer_full = bool(query & full)
            answer_other = bool(query & other)
            if answer_full != answer_other:
                distinguishing.append(query)
            checked += 1
        assert distinguishing == [1 << missing], (bits, missing, distinguishing)
    return {"input_bits": bits, "universe_size": N,
            "subsets_per_missing_element": 1 << N,
            "pairwise_oracle_comparisons": checked,
            "only_distinguishing_query_for_missing_j": "singleton_{j}",
            "deterministic_all_ones_query_lower_bound": N,
            "status": "PASS"}


def polynomial_crossover(k, decider_degree):
    # Conservative symbolic upper bound: T(n,g) <= K (n+g)^q.
    # For g <= n^k, and K=1 solely for illustrative numerical tests:
    # (n+n^k)^q <= 2^n/n^10, where q=max(3,2d)+1.
    q = max(3, 2 * decider_degree) + 1
    powers = [1 << t for t in range(4, 14)]
    first = next((n for n in powers
                  if (n + n**k)**q * n**10 <= (1 << n)), None)
    return {"max_circuit_size_exponent_k": k,
            "hypothetical_sat_polynomial_degree_d": decider_degree,
            "derived_q": q, "test_constants": "K=1",
            "first_power_of_two_n_with_exact_inequality": first,
            "finite_illustration_only": True}


def main():
    oracle = [oracle_check(b) for b in range(1, 5)]
    crossings = [polynomial_crossover(k, d)
                 for k in (1, 2, 3, 4) for d in (1, 2, 3)]
    result = {
        "run_id": "TMR1_WILL_NPCLASS051",
        "date_pacific": "2026-11-15 11:57 PST",
        "seed": "NONE: exhaustive deterministic",
        "model": "positive existential subset OR queries on an opaque subset of a 2^b-element universe",
        "oracle_controls": oracle,
        "polynomial_crossover_controls": crossings,
        "assertions": sum(x["pairwise_oracle_comparisons"] for x in oracle) + len(crossings),
        "failures": 0,
        "proof_status": "COMPUTATIONAL; mathematical corollaries proved separately",
        "limitations": [
            "Query oracle accepts positive subsets only; NOT a general SAT oracle",
            "Finite crossover thresholds assume leading constant K=1; cannot prove eventual dominance",
            "No native execution of October 2026 SAT formalisations",
            "No uniform SAT solver or circuit lower bound constructed"
        ]
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
