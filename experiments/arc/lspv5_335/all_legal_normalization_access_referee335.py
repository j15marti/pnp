#!/usr/bin/env python3
"""REFEREE335 finite controls for all-legal LOCAL-CONVERT payload sensitivity."""

import itertools
import json
import math
import sys


checks = 0


def check(cond, msg):
    global checks
    checks += 1
    if not cond:
        raise AssertionError(msg)


def parse_cnf(obj):
    if not isinstance(obj, dict) or set(obj) != {"nvars", "clauses"}:
        return None
    n = obj["nvars"]
    cs = obj["clauses"]
    if not isinstance(n, int) or isinstance(n, bool) or n < 0 or not isinstance(cs, list):
        return None
    out = []
    for c in cs:
        if not isinstance(c, list) or not c:
            return None
        seen = set()
        row = []
        for lit in c:
            if not isinstance(lit, int) or isinstance(lit, bool) or lit == 0 or abs(lit) > n:
                return None
            if lit in seen or -lit in seen:
                return None
            seen.add(lit)
            row.append(lit)
        out.append(row)
    return out


def sat_count(n, clauses):
    total = 0
    for bits in itertools.product((False, True), repeat=n):
        if all(any(bits[abs(l)-1] == (l > 0) for l in c) for c in clauses):
            total += 1
    return total


def condition_table(payload):
    """C_b(x)=x OR NOT(AND_i b_i), returned at x=0,1."""
    t = all(payload)
    return [not t, True]


def entailed_by_x(table):
    return bool(table[1])


def streaming_normalize(payload):
    reads = 0
    t = True
    for bit in payload:
        reads += 1
        t = t and bit
    return [not t, True], reads, max(1, math.ceil(math.log2(len(payload) + 1)))


def main():
    unsat = {"nvars": 1, "clauses": [[1], [-1]]}
    sat = {"nvars": 2, "clauses": [[1], [1, 2]]}
    check(sat_count(1, parse_cnf(unsat)) == 0, "UNSAT control")
    check(sat_count(2, parse_cnf(sat)) == 2, "SAT local-factor control")

    malformed = [
        None, {}, {"nvars": True, "clauses": [[1]]},
        {"nvars": 1, "clauses": "not-a-list"}, {"nvars": 1, "clauses": [[]]},
        {"nvars": 1, "clauses": [[0]]}, {"nvars": 1, "clauses": [[2]]},
        {"nvars": 1, "clauses": [[1, -1]]}, {"nvars": 1, "clauses": [[1, 1]]},
    ]
    for i, obj in enumerate(malformed):
        check(parse_cnf(obj) is None, f"malformed {i}")

    cases = []
    exhaustive_assignments = 0
    for k in range(1, 13):
        ones = (True,) * k
        table = condition_table(ones)
        check(table == [False, True], f"all-one root x k={k}")
        check(entailed_by_x(table), f"legal all-one k={k}")

        for i in range(k):
            flipped = list(ones)
            flipped[i] = False
            ft = condition_table(flipped)
            check(ft == [True, True], f"single flip is true k={k} i={i}")
            check(entailed_by_x(ft), f"single flip remains legal k={k} i={i}")
            check(ft != table, f"single bit extensional sensitivity k={k} i={i}")

        for payload in itertools.product((False, True), repeat=k):
            exhaustive_assignments += 1
            tab = condition_table(payload)
            check(entailed_by_x(tab), f"every record legal k={k}")
            expected = [False, True] if all(payload) else [True, True]
            check(tab == expected, f"canonical quotient k={k}")

        normalized, reads, peak_counter_bits = streaming_normalize(ones)
        check(normalized == table, f"stream output k={k}")
        check(reads == k, f"stream reads k={k}")
        check(peak_counter_bits == max(1, math.ceil(math.log2(k + 1))), f"counter k={k}")
        cases.append({
            "payload_bits": k,
            "paid_prefix_nodes": 2,
            "all_ones_condition": table,
            "single_flip_condition": [True, True],
            "sensitive_positions": k,
            "deterministic_worst_case_reads": k,
            "normalized_truth_bits": 2,
            "stream_counter_bits": peak_counter_bits,
            "materialized_payload_bits": k,
        })

    result = {
        "id": "LSPV5_ALL_LEGAL_NORMALIZATION_ACCESS_REFEREE335",
        "date": "2026-11-04_0348_PST",
        "model": "explicit private-root bounded-support LOCAL-CONVERT payload; all records legal consequences of S=x",
        "theorem": "on b=1^k, every exact deterministic extensional normalizer reads all k payload bits although the canonical output has two truth bits",
        "source_controls": {"unsat_models": 0, "sat_models": 2, "malformed_rejections": len(malformed)},
        "cases": cases,
        "exhaustive_payloads": exhaustive_assignments,
        "producer_assertions": checks,
        "classification": {
            "abstract_node_to_bit_normalization": "PROVED/RESTRICTED for literal R_mix341 semantics",
            "normalization_work": "Omega(M) bit access under explicit payload syntax",
            "peak_space": "O(log M) streaming upper bound; no linear lower bound",
            "B1_B2_B3": "OPEN",
            "P_vs_NP": "OPEN",
        },
    }
    json.dump(result, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
