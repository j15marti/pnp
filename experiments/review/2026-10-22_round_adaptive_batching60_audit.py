#!/usr/bin/env python3
"""Finite audit for ROUND-ADAPTIVE-BATCHING60.

Checks exact keyed-source membership queries exposed in adaptive rounds,
the pass inequality sum ceil(Q_r/B) <= Q/B + R, and the exponent phase
boundary.  This is not an unrestricted SAT or machine lower bound.
"""

from collections import defaultdict
import json
import math
import random


def answer_round(source_keys, queries, block_size):
    answers = [False] * len(queries)
    passes = 0
    visits = 0
    peak = 0
    for lo in range(0, len(queries), block_size):
        hi = min(len(queries), lo + block_size)
        positions = defaultdict(list)
        for pos in range(lo, hi):
            positions[queries[pos]].append(pos)
        peak = max(peak, hi - lo)
        passes += 1
        for key in source_keys:
            visits += 1
            for pos in positions.get(key, ()):
                answers[pos] = True
    return answers, passes, visits, peak


def adaptive_round_client(source_keys, universe, round_sizes, block_size, seed):
    """Each round's queries depend on the complete preceding transcript."""
    source_set = set(source_keys)
    state = seed
    total_queries = 0
    total_passes = 0
    total_visits = 0
    peak = 0
    transcript = []
    for round_index, count in enumerate(round_sizes):
        queries = []
        for j in range(count):
            state = (1103515245 * state + 12345 + 17 * round_index + j) & 0x7fffffff
            queries.append(state % universe)
        answers, passes, visits, local_peak = answer_round(
            source_keys, queries, block_size
        )
        expected = [q in source_set for q in queries]
        assert answers == expected
        transcript.extend(zip(queries, answers))
        # Make the next round genuinely answer-dependent.
        for q, answer in zip(queries, answers):
            state = ((state << 1) ^ (q * 257) ^ (1 if answer else 0)) & 0x7fffffff
        total_queries += count
        total_passes += passes
        total_visits += visits
        peak = max(peak, local_peak)
    return transcript, total_queries, total_passes, total_visits, peak


def main():
    rng = random.Random(600848)
    assertions = 0
    trials = 260
    query_checks = 0
    charged_visits = 0
    largest_rounds = 0

    for trial in range(trials):
        universe = 1 << rng.randint(7, 11)
        source_size = rng.randint(universe // 4, 3 * universe // 4)
        source_keys = rng.sample(range(universe), source_size)
        rng.shuffle(source_keys)
        rounds = rng.randint(1, 31)
        round_sizes = [rng.randint(1, max(1, universe // 3)) for _ in range(rounds)]
        block_size = rng.randint(1, max(1, int(math.sqrt(sum(round_sizes)))))
        transcript, q_total, passes, visits, peak = adaptive_round_client(
            source_keys, universe, round_sizes, block_size, 600848 + trial
        )
        expected_passes = sum(math.ceil(q / block_size) for q in round_sizes)
        assert len(transcript) == q_total == sum(round_sizes)
        assert passes == expected_passes
        assert passes <= q_total / block_size + rounds
        assert visits == source_size * passes
        assert peak <= block_size
        assertions += 5 + q_total
        query_checks += q_total
        charged_visits += visits
        largest_rounds = max(largest_rounds, rounds)

    # Exponent phase law: time exponent is 1+max(alpha-beta,rho),
    # aside from polylog factors, while output is alpha+lambda.
    phase_rows = []
    alpha = 0.6
    beta = 0.5
    child_exponent = 0.5
    for rho in (0.0, 0.05, 0.1, 0.11, 0.2, 0.6):
        scan_exponent = 1 + max(alpha - beta, rho)
        output_exponent = alpha + child_exponent
        fits_time = max(scan_exponent, output_exponent) <= 1.1 + 1e-12
        assert fits_time == (rho <= 0.1 + 1e-12)
        phase_rows.append({
            "query_exponent_alpha": alpha,
            "block_exponent_beta": beta,
            "round_exponent_rho": rho,
            "child_length_exponent_lambda": child_exponent,
            "scan_time_exponent": scan_exponent,
            "output_time_exponent": output_exponent,
            "fits_N_1_1_time": fits_time,
        })
        assertions += 1

    # Singleton-round hostile control: R=Q gives exactly Q passes.
    universe = 2048
    source_keys = rng.sample(range(universe), universe // 2)
    q_total = 513
    singleton_sizes = [1] * q_total
    transcript, checked_q, passes, visits, peak = adaptive_round_client(
        source_keys, universe, singleton_sizes, 64, 606060
    )
    assert len(transcript) == checked_q == q_total
    assert passes == q_total
    assert visits == q_total * len(source_keys)
    assert peak == 1
    assertions += 4 + q_total

    result = {
        "status": "FINITE_AUDIT_ONLY_NO_CLASS_SEPARATION",
        "restricted_lemma": {
            "model": "explicit keyed source; deterministic comparison dictionary; adaptive rounds",
            "pass_bound": "sum_r ceil(Q_r/B) <= Q/B + R",
            "time": "O(N*(Q/B+R)*log(B)+Q*log(B))",
            "space": "O(B*log(N)+parser_scratch)",
            "phase_law": "scan exponent 1+max(alpha-beta,rho)",
        },
        "random_audit": {
            "trials": trials,
            "membership_queries_checked": query_checks,
            "charged_source_record_visits": charged_visits,
            "largest_round_count": largest_rounds,
        },
        "phase_rows": phase_rows,
        "singleton_round_control": {
            "queries": q_total,
            "rounds": q_total,
            "passes": passes,
            "source_record_visits": visits,
        },
        "firewalls": [
            "all queries in a round must be fixed before that round's scans",
            "R must be at most N^(0.1+o(1)) at the target parameters",
            "source keys and query-key equality must be uniformly computable",
            "random-access dictionary simulation and child output must be charged on the target machine",
            "no arbitrary-SAT bounded-round exposure theorem is supplied",
        ],
        "assertions": assertions,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
