#!/usr/bin/env python3
"""Independent no-import verifier for REFEREE244."""
from __future__ import annotations

import copy
import hashlib
import itertools
import json
import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW = ROOT.parents[2] / "results/raw/arc/2026-10-31_0848_LSPV5_RENAME_INSTABILITY_REFEREE244_raw.json"
OUT = ROOT.parents[2] / "results/summaries/arc/2026-10-31_0848_LSPV5_RENAME_INSTABILITY_REFEREE244_verification.json"
SEED = 244031
MAX_B = 4


def generate(n, unsat):
    clauses = ([[1], [-1]] if unsat else []) + [[1, 2]] + [[i] for i in range(3, n + 1)]
    if unsat:
        clauses += [[n], [n]]
    return clauses


def permutation(n):
    q = n // 2
    p = {i: i for i in range(1, n + 1)}
    p[1], p[n] = n, 1
    p[2], p[q] = q, 2
    return p


def rename(clauses, p):
    return [[(1 if x > 0 else -1) * p[abs(x)] for x in c] for c in clauses]


def class_of(clauses):
    if all(len(c) <= 2 for c in clauses):
        return "KROM"
    if all(sum(x > 0 for x in c) <= 1 for c in clauses):
        return "HORN"
    if all(sum(x < 0 for x in c) <= 1 for c in clauses):
        return "DUAL_HORN"
    return None


def discover(clauses, n):
    trials = []
    for b in range(1, min(MAX_B, n) + 1):
        r = math.isqrt(n - b)
        r += r * r < n - b
        last = -1
        current = []
        reason = None
        for j, clause in enumerate(clauses, 1):
            private = {(abs(x) - b - 1) // r for x in clause if abs(x) > b}
            if len(private) > 1:
                reason = "cross_private_blocks"
                break
            if not private:
                if last >= 0:
                    reason = "late_core"
                    break
                continue
            block = next(iter(private))
            if block < last:
                reason = "unsorted_source_blocks"
                break
            if block != last:
                if last >= 0 and class_of(current) is None:
                    reason = "hard_block"
                    break
                current = []
                last = block
            current.append(clause)
            if len(current) > r:
                reason = "block_overflow"
                break
        if reason is None and last >= 0 and class_of(current) is None:
            reason = "hard_last_block"
        trials.append((b, reason))
        if reason is None:
            return True, b, trials
    return False, None, trials


def sat_clause(clause, assignment):
    return any(assignment[abs(x)] == (x > 0) for x in clause)


def brute(clauses, n, base=None):
    base = {} if base is None else dict(base)
    rest = [i for i in range(1, n + 1) if i not in base and any(i == abs(x) for c in clauses for x in c)]
    for bits in itertools.product((False, True), repeat=len(rest)):
        a = {**base, **dict(zip(rest, bits))}
        if all(sat_clause(c, a) for c in clauses):
            return a
    return None


def count_true(clause, assignment):
    return sum(assignment[abs(x)] == (x > 0) for x in clause)


def check_diagnostics(clauses, n, d):
    checks = 0
    zero = {i: False for i in range(1, n + 1)}
    one = {i: True for i in range(1, n + 1)}
    assert len(d["occurrences"]) == len(clauses)
    for j, clause in enumerate(clauses):
        s = {str(abs(x)): int(x > 0) for x in clause}
        u = {k: 1 - v for k, v in s.items()}
        row = d["occurrences"][j]
        assert row["source_clause_index"] == j + 1
        assert row["signed_clause"] == clause
        assert row["S"] == s and row["U"] == u
        assert row["invert_S_U"] == u and row["invert_U_S"] == s
        checks += 6
    pair_map = {(x["j"], x["k"]): x for x in d["pairs"]}
    assert len(pair_map) == len(clauses) * (len(clauses) - 1) // 2
    for j, c in enumerate(clauses):
        for k in range(j + 1, len(clauses)):
            e = clauses[k]
            variables = sorted({abs(x) for x in c + e})
            row = pair_map[(j + 1, k + 1)]
            for states, field in [
                ((True, True), "SS"),
                ((True, False), "SU"),
                ((False, True), "US"),
                ((False, False), "UU"),
            ]:
                feasible = False
                for bits in itertools.product((False, True), repeat=len(variables)):
                    a = dict(zip(variables, bits))
                    if count_true(c, a) == (len(c) if states[0] else 0) and count_true(e, a) == (len(e) if states[1] else 0):
                        feasible = True
                        break
                assert row[field] == feasible
                checks += 1
    for assignment, row in zip((zero, one), d["endpoints"]):
        counts = [count_true(c, assignment) for c in clauses]
        assert row["counts"] == counts
        assert row["N"] == [counts.count(i) for i in range(4)]
        assert row["SAT"] == all(counts)
        checks += 3
    a = dict(zero)
    for row in d["flips"]:
        a[row["flip"]] = not a[row["flip"]]
        counts = [count_true(c, a) for c in clauses]
        assert row["counts"] == counts
        assert row["N"] == [counts.count(i) for i in range(4)]
        assert row["SAT"] == all(counts)
        checks += 3
    return checks


def verify(doc):
    assert doc["run"] == "LSPV5_RENAME_INSTABILITY_REFEREE244"
    assert len(doc["rows"]) == 16
    checks = 0
    for row in doc["rows"]:
        n = row["n"]
        unsat = "UNSAT" in row["name"]
        renamed = "RENAMED" in row["name"]
        clauses = generate(n, unsat)
        if renamed:
            clauses = rename(clauses, permutation(n))
        recognized, b, trials = discover(clauses, n)
        assert row["recognition"]["recognized"] == recognized
        assert recognized == (not renamed)
        if recognized:
            assert b == row["recognition"]["b"] == 1
        else:
            assert [x[1] for x in trials] == [
                x["reason"]["kind"] for x in row["recognition"]["trials"]
            ]
            assert all(x[1] == "cross_private_blocks" for x in trials)
        if n == 15:
            assert row["clauses"] == clauses
            witness = brute(clauses, n)
            assert (witness is None) == unsat
            checks += 2 ** n
            checks += check_diagnostics(clauses, n, row["diagnostics"])
        if renamed:
            p = permutation(n)
            assert row["prohibited_cube"]["variables"] == [p[1], p[2]]
        else:
            assert row["prohibited_cube"]["variables"] == [1, 2]
        assert row["prohibited_cube"]["values"] == [0, 0]
        if unsat:
            proof = row["unsat_resolution"]
            assert proof["parents"] == [[proof["pivot"]], [-proof["pivot"]]]
            assert proof["resolvent"] == []
        checks += 12
    for name, expected in (("H7_SAT", True), ("H8_UNSAT", False)):
        row = doc["controls"][name]
        assert (brute(row["clauses"], 3) is not None) == expected
        checks += 8
        checks += check_diagnostics(row["clauses"], 3, row["diagnostics"])
    rng = random.Random(SEED)
    source = generate(35, False)
    accepted = 0
    kinds = {}
    for _ in range(512):
        image = list(range(1, 36))
        rng.shuffle(image)
        p = {i + 1: image[i] for i in range(35)}
        ok, _, trials = discover(rename(source, p), 35)
        accepted += ok
        if not ok:
            kinds[trials[0][1]] = kinds.get(trials[0][1], 0) + 1
    rc = doc["random_renaming_control"]
    assert rc["recognized"] == accepted
    assert rc["rejected"] == 512 - accepted
    assert rc["first_trial_failure_kinds"] == kinds
    checks += 512
    return checks


def main():
    raw = RAW.read_bytes()
    doc = json.loads(raw)
    checks = verify(doc)
    rejected = 0
    for mode in range(4):
        x = copy.deepcopy(doc)
        if mode == 0:
            x["rows"][0]["recognition"]["recognized"] = False
        elif mode == 1:
            x["rows"][1]["prohibited_cube"]["values"] = [1, 1]
        elif mode == 2:
            x["rows"][0]["diagnostics"]["occurrences"][0]["S"]["1"] ^= 1
        else:
            x["controls"]["H8_UNSAT"]["diagnostics"]["pairs"][0]["SS"] ^= True
        try:
            verify(x)
        except AssertionError:
            rejected += 1
    assert rejected == 4
    out = {
        "status": "PASS",
        "independent_check_units": checks,
        "corruptions_rejected": rejected,
        "no_producer_import": True,
        "raw_sha256": hashlib.sha256(raw).hexdigest(),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
