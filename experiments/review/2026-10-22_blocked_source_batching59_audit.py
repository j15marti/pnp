#!/usr/bin/env python3
"""Finite audit for BLOCKED-SOURCE-BATCHING59.

Checks an exact batching algorithm for an explicit keyed source stream,
its exponent ledger, streamed child-output charge, and an adaptive-query
control.  This is a restricted algorithmic audit, not a complexity-class
claim or a lower bound for unrestricted algorithms.
"""

from collections import defaultdict
import json
import math
import random


def blocked_membership(source_keys, queries, block_size):
    """Answer a nonadaptive query list by one source pass per query block."""
    answers = [False] * len(queries)
    scans = 0
    visits = 0
    peak_records = 0
    for lo in range(0, len(queries), block_size):
        hi = min(len(queries), lo + block_size)
        positions = defaultdict(list)
        for pos in range(lo, hi):
            positions[queries[pos]].append(pos)
        peak_records = max(peak_records, hi - lo)
        scans += 1
        for key in source_keys:
            visits += 1
            for pos in positions.get(key, ()):
                answers[pos] = True
    return answers, scans, visits, peak_records


def adaptive_rescan(source_set, source_order, start, rounds, modulus):
    """A deliberately sequential client: q_(i+1) depends on answer i."""
    query = start
    transcript = []
    visits = 0
    for step in range(rounds):
        found = False
        for key in source_order:
            visits += 1
            if key == query:
                found = True
        transcript.append((query, found))
        # Both branches are injective affine maps modulo a power of two.
        query = ((5 if found else 3) * query + 2 * step + (1 if found else 0)) % modulus
    assert all(found == (query in source_set) for query, found in transcript)
    return transcript, visits


def main():
    rng = random.Random(590748)
    assertions = 0
    trials = 240
    total_queries = 0
    total_source_visits = 0
    maximum_peak = 0

    for _ in range(trials):
        universe = 1 << rng.randint(7, 11)
        source_size = rng.randint(universe // 5, 4 * universe // 5)
        source_keys = rng.sample(range(universe), source_size)
        source_set = set(source_keys)
        rng.shuffle(source_keys)
        query_count = rng.randint(1, 3 * universe)
        queries = [rng.randrange(universe) for _ in range(query_count)]
        block_size = rng.randint(1, max(1, int(math.sqrt(query_count))))
        answers, scans, visits, peak = blocked_membership(
            source_keys, queries, block_size
        )
        expected = [q in source_set for q in queries]
        assert answers == expected
        assert scans == math.ceil(query_count / block_size)
        assert visits == source_size * scans
        assert peak <= block_size
        assertions += 4 + query_count
        total_queries += query_count
        total_source_visits += visits
        maximum_peak = max(maximum_peak, peak)

    # Symbolic exponent audit for Q=N^0.6, B=L=N^0.5.
    exponent_rows = []
    for log2_n in (20, 40, 80, 160, 320, 640):
        q_log = 0.6 * log2_n
        b_log = 0.5 * log2_n
        scans_log = q_log - b_log
        scan_time_log = log2_n + scans_log
        output_time_log = q_log + b_log
        assert math.isclose(scan_time_log / log2_n, 1.1)
        assert math.isclose(output_time_log / log2_n, 1.1)
        assert math.isclose(b_log / log2_n, 0.5)
        exponent_rows.append({
            "log2_N": log2_n,
            "Q_exponent": 0.6,
            "B_exponent": 0.5,
            "passes_exponent": 0.1,
            "source_scan_time_exponent": 1.1,
            "streamed_output_time_exponent": 1.1,
            "peak_record_exponent": 0.5,
        })
        assertions += 3

    # Adaptive control: in this rescan architecture, only the next query is
    # exposed after the previous answer, so Q source scans are performed.
    modulus = 4096
    source_set = set(rng.sample(range(modulus), modulus // 2))
    source_order = list(source_set)
    rng.shuffle(source_order)
    rounds = 257
    transcript, adaptive_visits = adaptive_rescan(
        source_set, source_order, 17, rounds, modulus
    )
    assert len(transcript) == rounds
    assert adaptive_visits == rounds * len(source_order)
    assertions += 2 + rounds

    result = {
        "status": "FINITE_AUDIT_ONLY_NO_CLASS_SEPARATION",
        "restricted_lemma": {
            "source_model": "explicit keyed stream",
            "query_model": "nonadaptive exact membership queries known before batching",
            "time": "O(N*ceil(Q/B)*log(B)+Q) on a comparison dictionary; expected O(N*ceil(Q/B)+Q) with hashing",
            "space": "O(B*log(N)+parser_scratch) bits",
            "duplicates": "supported",
        },
        "finite_random_audit": {
            "trials": trials,
            "queries_checked": total_queries,
            "source_record_visits": total_source_visits,
            "maximum_query_records_resident": maximum_peak,
        },
        "exponent_ledger": exponent_rows,
        "streamed_child_output": {
            "Q": "N^0.6",
            "child_length": "N^0.5",
            "total_write_time": "N^1.1",
            "peak_child_buffer": "N^0.5",
        },
        "adaptive_control": {
            "rounds": rounds,
            "source_size": len(source_order),
            "record_visits": adaptive_visits,
            "scope": "lower bound only for the explicit sequential-rescan architecture",
        },
        "firewalls": [
            "queries must be exposed nonadaptively before their block is scanned",
            "source records must reveal uniformly computable keys",
            "per-record dictionary update must be polylogarithmic rather than linear in B",
            "all source acquisition, parser/index tapes, failed queries, and output are charged",
            "the lemma does not supply an arbitrary-SAT hereditary ARC contractor",
        ],
        "assertions": assertions,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
