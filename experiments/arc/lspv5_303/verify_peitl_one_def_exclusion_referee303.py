#!/usr/bin/env python3
"""Independent no-import recomputation of REFEREE303's one-DEF exclusion."""

from __future__ import annotations

import hashlib
import itertools
import json
import resource
import time
from pathlib import Path


SOURCE = Path("results/raw/arc/lspv5_300_peitl/rsmu_5_7_1.cnf")
RAW = Path("results/raw/arc/2026-11-02_2048_LSPV5_PEITL_ONE_DEF_EXCLUSION_REFEREE303_raw.json")
OUT = Path("results/raw/arc/2026-11-02_2048_LSPV5_PEITL_ONE_DEF_EXCLUSION_REFEREE303_verify.json")


def parse(text):
    rows = [x.split() for x in text.splitlines() if x.strip() and not x.lstrip().startswith("c")]
    if not rows or len(rows[0]) != 4 or rows[0][:2] != ["p", "cnf"]:
        raise ValueError("header")
    n, promised = map(int, rows[0][2:])
    if n < 0 or promised < 0:
        raise ValueError("dimensions")
    clauses = []
    for row in rows[1:]:
        if not row or row[-1] != "0" or row.count("0") != 1:
            raise ValueError("terminator")
        clause = tuple(int(x) for x in row[:-1])
        if len(set(clause)) != len(clause) or any(x == 0 or abs(x) > n or -x in clause for x in clause):
            raise ValueError("literal")
        clauses.append(clause)
    if len(clauses) != promised:
        raise ValueError("count")
    return n, clauses


def tt(clause, n):
    table = 0
    for assignment in range(1 << n):
        okay = False
        for lit in clause:
            bit = (assignment >> (abs(lit) - 1)) & 1
            okay |= bit == (lit > 0)
        table |= int(okay) << assignment
    return table


def support(table, n):
    return sum(any(((table >> a) ^ (table >> (a ^ (1 << v)))) & 1 for a in range(1 << n)) for v in range(n))


def affine(mask, rhs, n):
    return sum((((a & mask).bit_count() & 1) == rhs) << a for a in range(1 << n))


def make_aliases(n):
    clause = {}
    for choice in itertools.product((0, 1, -1), repeat=n):
        c = tuple((i + 1) * sign for i, sign in enumerate(choice) if sign)
        clause[tt(c, n)] = c
    linear = {affine(mask, rhs, n): (mask, rhs) for mask in range(1 << n) for rhs in (0, 1)}
    return clause, linear


def operations(a, b, n, clause, linear):
    outputs = set()
    conjunction = a & b
    if support(conjunction, n) <= 3:
        outputs.add(conjunction)
    if a in linear and b in linear:
        ma, ra = linear[a]
        mb, rb = linear[b]
        outputs.add(affine(ma ^ mb, ra ^ rb, n))
    if a in clause and b in clause:
        for left, right in ((clause[a], clause[b]), (clause[b], clause[a])):
            for pivot in left:
                if -pivot not in right:
                    continue
                candidate = (set(left) | set(right)) - {pivot, -pivot}
                if not any(-x in candidate for x in candidate):
                    outputs.add(tt(tuple(candidate), n))
    return outputs


def slots():
    answer = set()
    for y in (6, -6):
        for amount in range(3):
            for variables in itertools.combinations(range(1, 6), amount):
                for signs in itertools.product((-1, 1), repeat=amount):
                    answer.add(tuple(sorted((y,) + tuple(s * v for s, v in zip(signs, variables)), key=lambda x: (abs(x), x < 0))))
    return sorted(answer, key=lambda x: (len(x), x))


def search(source, slot, clause, linear, cache):
    leaves = source + [slot]
    bank = [set() for _ in range(256)]
    for i, leaf in enumerate(leaves):
        bank[1 << i].add(tt(leaf, 6))
    pair_tests = generated = 0
    for whole in range(1, 256):
        if whole.bit_count() < 2:
            continue
        sub = (whole - 1) & whole
        while sub:
            other = whole ^ sub
            if sub < other:
                for a in bank[sub]:
                    for b in bank[other]:
                        pair_tests += 1
                        key = (min(a, b), max(a, b))
                        if key not in cache:
                            cache[key] = operations(a, b, 6, clause, linear)
                        made = cache[key]
                        generated += len(made)
                        bank[whole].update(made)
            sub = (sub - 1) & whole
    return 0 in bank[-1], len(bank[-1]), pair_tests, generated, sum(map(len, bank))


def main():
    began = time.perf_counter()
    source_bytes = SOURCE.read_bytes()
    raw_bytes = RAW.read_bytes()
    raw = json.loads(raw_bytes)
    n, source = parse(source_bytes.decode())
    clause, linear = make_aliases(6)
    cache = {}
    recomputed = []
    totals = [0, 0, 0]
    for slot in slots():
        found, terminal, pairs, generated, states = search(source, slot, clause, linear, cache)
        recomputed.append((slot, found, terminal, pairs, generated, states))
        totals[0] += pairs
        totals[1] += generated
        totals[2] += states
    published = [(tuple(x["slot"]), x["contains_false"], x["terminal_functions"], x["pair_tests"], x["generated_outputs"], x["states_total"]) for x in raw["cases"]]

    bad = [
        "1 0\n",
        "p sat 1 1\n1 0\n",
        "p cnf 1 2\n1 0\n",
        "p cnf 1 1\n2 0\n",
        "p cnf 1 1\n1\n",
        "p cnf 1 1\n1 1 0\n",
        "p cnf 1 1\n1 -1 0\n",
        "p cnf -1 0\n",
    ]
    rejects = 0
    for item in bad:
        try:
            parse(item)
        except ValueError:
            rejects += 1

    assertions = {
        "source_sha": hashlib.sha256(source_bytes).hexdigest() == "6ca65edf800525363d4153b266cd4f4d207bd3a8977064c74996bc363ee8f6d6",
        "source_shape": n == 5 and len(source) == 7,
        "slot_count": len(recomputed) == 102,
        "no_relaxed_def_slot_refutes": not any(x[1] for x in recomputed),
        "case_by_case_agreement": recomputed == published,
        "aggregate_agreement": totals == [raw["aggregate_search"]["pair_tests"], raw["aggregate_search"]["generated_outputs"], raw["aggregate_search"]["states_total"]],
        "cache_count_agreement": len(cache) == raw["aggregate_search"]["combine_cache_entries"],
        "all_malformed_rejected": rejects == len(bad),
        "published_assertions_true": all(raw["assertions"].values()),
    }
    if not all(assertions.values()):
        raise AssertionError(assertions)
    result = {
        "claim_id": "PEITL-ONE-DEF-EXCLUSION-REFEREE303-INDEPENDENT-VERIFY",
        "raw_sha256": hashlib.sha256(raw_bytes).hexdigest(),
        "assertions": assertions,
        "independent_totals": {"pair_tests": totals[0], "generated_outputs": totals[1], "states_total": totals[2], "combine_cache_entries": len(cache)},
        "elapsed_seconds": time.perf_counter() - began,
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
