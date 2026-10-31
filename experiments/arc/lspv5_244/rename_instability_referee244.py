#!/usr/bin/env python3
"""REFEREE244: variable-renaming hostile control for GATE277.

Standard library only.  The counters are reproducible Python event counters,
not FLMV machine steps.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import math
import random
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW = ROOT.parents[2] / "results/raw/arc/2026-10-31_0848_LSPV5_RENAME_INSTABILITY_REFEREE244_raw.json"
SUMMARY = ROOT.parents[2] / "results/summaries/arc/2026-10-31_0848_LSPV5_RENAME_INSTABILITY_REFEREE244_summary.json"
SEED = 244031
MAX_B = 4


class Ledger(dict):
    def bump(self, key, amount=1):
        self[key] = self.get(key, 0) + amount


def sat_lit(lit, assignment):
    return assignment[abs(lit)] == (lit > 0)


def sat_clause(clause, assignment):
    return any(sat_lit(lit, assignment) for lit in clause)


def count_true(clause, assignment):
    return sum(sat_lit(lit, assignment) for lit in clause)


def proper_source(clauses):
    return all(
        1 <= len(c) <= 3
        and len({abs(x) for x in c}) == len(c)
        and all(x != 0 for x in c)
        for c in clauses
    )


def class_of(clauses):
    if all(len(c) <= 2 for c in clauses):
        return "KROM"
    if all(sum(x > 0 for x in c) <= 1 for c in clauses):
        return "HORN"
    if all(sum(x < 0 for x in c) <= 1 for c in clauses):
        return "DUAL_HORN"
    return None


def discover(clauses, n, max_b=MAX_B):
    """Independent implementation of the declared GATE277 prefix recognizer."""
    ledger = Ledger()
    trials = []
    for b in range(1, min(max_b, n) + 1):
        ledger.bump("policy_trials")
        r = math.isqrt(n - b)
        if r * r < n - b:
            r += 1
        if r < 1:
            continue
        last = -1
        current = []
        types = {}
        reason = None
        for clause_index, clause in enumerate(clauses, 1):
            ledger.bump("source_clause_reads")
            ledger.bump("source_literal_reads", len(clause))
            private = {(abs(x) - b - 1) // r for x in clause if abs(x) > b}
            if len(private) > 1:
                reason = {
                    "kind": "cross_private_blocks",
                    "clause_index": clause_index,
                    "clause": clause,
                    "private_blocks": sorted(private),
                }
                break
            if not private:
                if last >= 0:
                    reason = {"kind": "late_core", "clause_index": clause_index}
                    break
                continue
            block = next(iter(private))
            if block < last:
                reason = {
                    "kind": "unsorted_source_blocks",
                    "clause_index": clause_index,
                    "block": block,
                    "last": last,
                }
                break
            if block != last:
                if last >= 0:
                    kind = class_of(current)
                    if kind is None:
                        reason = {"kind": "hard_block", "block": last}
                        break
                    types[str(last)] = kind
                current = []
                last = block
            current.append(clause)
            if len(current) > r:
                reason = {"kind": "block_overflow", "block": block}
                break
        if reason is None and last >= 0:
            kind = class_of(current)
            if kind is None:
                reason = {"kind": "hard_last_block", "block": last}
            else:
                types[str(last)] = kind
        trials.append({"b": b, "r": r, "reason": reason})
        if reason is None:
            return {
                "recognized": True,
                "b": b,
                "r": r,
                "types": types,
                "trials": trials,
                "ledger": dict(ledger),
            }
        ledger.bump("policy_rejected")
    return {
        "recognized": False,
        "trials": trials,
        "ledger": dict(ledger),
    }


def generate(n, unsat):
    # At b=1, r=ceil(sqrt(n-1)).  The first bin contains one coupling
    # clause and r-1 unit clauses; all later bins contain at most r units.
    clauses = ([[1], [-1]] if unsat else []) + [[1, 2]]
    clauses += [[i] for i in range(3, n + 1)]
    # Balance the two extra x_1 core occurrences with two extra x_n
    # occurrences.  This keeps native DIMACS length exactly invariant under
    # the adversarial 1<->n swap.  The chosen n=r^2-1 leaves two spare clause
    # slots in the final private bin, so recognition at b=1 remains valid.
    if unsat:
        clauses += [[n], [n]]
    assert proper_source(clauses)
    return clauses


def adversarial_permutation(n, max_b=MAX_B):
    # Move the true boundary variable to n and its coupled private variable
    # to q=max_b+1.  The two are in distinct private bins for every tested b.
    q = n // 2
    assert q not in (1, 2, n)
    pi = {i: i for i in range(1, n + 1)}
    pi[1], pi[n] = n, 1
    pi[2], pi[q] = q, 2
    return pi, q


def apply_permutation(clauses, pi):
    return [[(1 if x > 0 else -1) * pi[abs(x)] for x in c] for c in clauses]


def up(clauses, assignment, ledger):
    assignment = dict(assignment)
    while True:
        changed = False
        for clause in clauses:
            ledger.bump("literal_probes", len(clause))
            if any(
                abs(x) in assignment and assignment[abs(x)] == (x > 0)
                for x in clause
            ):
                continue
            unassigned = [x for x in clause if abs(x) not in assignment]
            if not unassigned:
                return None
            if len(unassigned) == 1:
                lit = unassigned[0]
                assignment[abs(lit)] = lit > 0
                ledger.bump("unit_assignments")
                changed = True
                break
        if not changed:
            return assignment


def dpll(clauses, n, base=None):
    ledger = Ledger()

    def rec(assignment):
        ledger.bump("nodes")
        assignment = up(clauses, assignment, ledger)
        if assignment is None:
            return None
        candidates = sorted(
            {abs(x) for c in clauses for x in c if abs(x) not in assignment}
        )
        if not candidates:
            return assignment
        variable = candidates[0]
        for value in (False, True):
            witness = rec({**assignment, variable: value})
            if witness is not None:
                return witness
        return None

    witness = rec({} if base is None else dict(base))
    return witness, dict(ledger)


def encode_clause_width3(clause, next_var):
    if len(clause) == 3:
        return [clause], next_var
    if len(clause) == 2:
        z = next_var
        return [clause + [z], clause + [-z]], z + 1
    if len(clause) == 1:
        u, v = next_var, next_var + 1
        return [
            [clause[0], su * u, sv * v]
            for su in (-1, 1)
            for sv in (-1, 1)
        ], next_var + 2
    raise AssertionError("only nonempty boundary clauses used")


def projected_child(clauses, n, b):
    blocked = []
    projection_work = Ledger()
    for bits in itertools.product((False, True), repeat=b):
        base = {i + 1: bits[i] for i in range(b)}
        witness, work = dpll(clauses, n, base)
        projection_work.bump("boundary_assignments")
        for key, value in work.items():
            projection_work.bump("dpll_" + key, value)
        if witness is None:
            blocked.append(list(map(int, bits)))
    child = []
    next_var = b + 1
    if not blocked:
        # Existentially true, while retaining a genuine proper ternary clause.
        child = [[b + 1, b + 2, b + 3]]
        next_var = b + 4
    else:
        for bits in blocked:
            forbid = [-(i + 1) if bits[i] else i + 1 for i in range(b)]
            encoded, next_var = encode_clause_width3(forbid, next_var)
            child.extend(encoded)
    return {
        "blocked": blocked,
        "child": child,
        "child_n": next_var - 1,
        "projection_work": dict(projection_work),
    }


def dimacs_bits(clauses, n):
    text = f"p cnf {n} {len(clauses)}\n" + "".join(
        " ".join(map(str, c)) + " 0\n" for c in clauses
    )
    return 8 * len(text)


def diagnostics(clauses, n):
    zero = {i: False for i in range(1, n + 1)}
    one = {i: True for i in range(1, n + 1)}
    occurrences = []
    pairs = []
    for j, clause in enumerate(clauses, 1):
        s = {str(abs(x)): int(x > 0) for x in clause}
        u = {key: 1 - value for key, value in s.items()}
        occurrences.append(
            {
                "source_clause_index": j,
                "signed_clause": clause,
                "S": s,
                "invert_S_U": u,
                "U": u,
                "invert_U_S": s,
            }
        )
    for j, clause in enumerate(clauses):
        a = {abs(x): x > 0 for x in clause}
        for k in range(j + 1, len(clauses)):
            d = {abs(x): x > 0 for x in clauses[k]}
            shared = a.keys() & d.keys()
            same = any(a[x] == d[x] for x in shared)
            opposite = any(a[x] != d[x] for x in shared)
            pairs.append(
                {
                    "j": j + 1,
                    "k": k + 1,
                    "SS": not opposite,
                    "SU": not same,
                    "US": not same,
                    "UU": not opposite,
                }
            )
    endpoints = []
    for name, assignment in (("zero", zero), ("one", one)):
        counts = [count_true(c, assignment) for c in clauses]
        endpoints.append(
            {
                "name": name,
                "counts": counts,
                "N": [counts.count(v) for v in range(4)],
                "SAT": all(counts),
            }
        )
    assignment = dict(zero)
    flips = []
    for variable in range(1, min(n, 10) + 1):
        assignment[variable] = not assignment[variable]
        counts = [count_true(c, assignment) for c in clauses]
        flips.append(
            {
                "flip": variable,
                "counts": counts,
                "N": [counts.count(v) for v in range(4)],
                "SAT": all(counts),
            }
        )
    assert all(
        count_true(c, zero) + count_true(c, one) == len(c) for c in clauses
    )
    return {
        "occurrences": occurrences,
        "pairs": pairs,
        "endpoints": endpoints,
        "flips": flips,
    }


def h7_h8():
    clauses = []
    for bits in itertools.product((False, True), repeat=3):
        clauses.append(
            [-(i + 1) if bits[i] else i + 1 for i in range(3)]
        )
    return clauses[:-1], clauses


def formula_row(n, unsat, renamed):
    source = generate(n, unsat)
    pi, q = adversarial_permutation(n)
    clauses = apply_permutation(source, pi) if renamed else source
    recognition = discover(clauses, n)
    witness, baseline = dpll(clauses, n)
    label = "SAT" if witness is not None else "UNSAT"
    assert label == ("UNSAT" if unsat else "SAT")
    child = None
    guest = None
    if recognition["recognized"]:
        child = projected_child(clauses, n, recognition["b"])
        child_witness, guest = dpll(child["child"], child["child_n"])
        assert (child_witness is not None) == (witness is not None)
    selected_work = sum(baseline.values()) + sum(recognition["ledger"].values())
    if child:
        selected_work += sum(child["projection_work"].values())
        selected_work += sum(guest.values())
    else:
        # Exact fallback is the baseline DPLL; charge it a second time as the
        # controller's selected fallback transaction.
        selected_work += sum(baseline.values())
    return {
        "name": f"N{n}_{'UNSAT' if unsat else 'SAT'}_{'RENAMED' if renamed else 'CANONICAL'}",
        "n": n,
        "q": q,
        "label": label,
        "clauses": clauses if n == 15 else None,
        "source_bits": dimacs_bits(clauses, n),
        "recognition": recognition,
        "baseline": baseline,
        "selected_work_proxy": selected_work,
        "child": child,
        "prohibited_cube": {
            "variables": [pi[1], pi[2]] if renamed else [1, 2],
            "values": [0, 0],
            "proof": "the coupling clause is false on exactly this partial cube",
        },
        "unsat_resolution": (
            {
                "pivot": pi[1] if renamed else 1,
                "parents": [
                    [pi[1] if renamed else 1],
                    [-(pi[1] if renamed else 1)],
                ],
                "resolvent": [],
            }
            if unsat
            else None
        ),
        "diagnostics": diagnostics(clauses, n) if n == 15 else None,
    }


def random_renaming_control(n=35, samples=512):
    source = generate(n, False)
    rng = random.Random(SEED)
    accepted = 0
    failure_kinds = {}
    for _ in range(samples):
        image = list(range(1, n + 1))
        rng.shuffle(image)
        pi = {i + 1: image[i] for i in range(n)}
        result = discover(apply_permutation(source, pi), n)
        accepted += int(result["recognized"])
        if not result["recognized"]:
            kind = result["trials"][0]["reason"]["kind"]
            failure_kinds[kind] = failure_kinds.get(kind, 0) + 1
    return {
        "n": n,
        "samples": samples,
        "recognized": accepted,
        "rejected": samples - accepted,
        "first_trial_failure_kinds": failure_kinds,
        "seed": SEED,
    }


def main():
    started = time.monotonic()
    rows = [
        formula_row(n, unsat, renamed)
        for n in (15, 24, 35, 63)
        for unsat in (False, True)
        for renamed in (False, True)
    ]
    for n in (15, 24, 35, 63):
        for unsat in (False, True):
            canonical = next(
                x for x in rows if x["n"] == n and x["label"] == ("UNSAT" if unsat else "SAT") and "CANONICAL" in x["name"]
            )
            renamed = next(
                x for x in rows if x["n"] == n and x["label"] == ("UNSAT" if unsat else "SAT") and "RENAMED" in x["name"]
            )
            assert canonical["recognition"]["recognized"]
            assert canonical["recognition"]["b"] == 1
            assert not renamed["recognition"]["recognized"]
    h7, h8 = h7_h8()
    controls = {
        "H7_SAT": {
            "clauses": h7,
            "label": "SAT",
            "diagnostics": diagnostics(h7, 3),
            "dpll": dpll(h7, 3)[1],
        },
        "H8_UNSAT": {
            "clauses": h8,
            "label": "UNSAT",
            "diagnostics": diagnostics(h8, 3),
            "dpll": dpll(h8, 3)[1],
        },
    }
    random_control = random_renaming_control()
    raw = {
        "run": "LSPV5_RENAME_INSTABILITY_REFEREE244",
        "timestamp": "2026-10-31T08:48:00-07:00",
        "status": "PROVED/EXACT restricted renaming-instability theorem; COMPUTATIONAL controls; ARC OPEN",
        "seed": SEED,
        "max_b": MAX_B,
        "rows": rows,
        "controls": controls,
        "random_renaming_control": random_control,
    }
    RAW.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY.parent.mkdir(parents=True, exist_ok=True)
    RAW.write_text(json.dumps(raw, sort_keys=True, separators=(",", ":")) + "\n")
    summary = {
        "run": raw["run"],
        "rows": len(rows),
        "canonical_recognized": sum(
            x["recognition"]["recognized"] and "CANONICAL" in x["name"]
            for x in rows
        ),
        "renamed_rejected": sum(
            (not x["recognition"]["recognized"]) and "RENAMED" in x["name"]
            for x in rows
        ),
        "sat_rows": sum(x["label"] == "SAT" for x in rows),
        "unsat_rows": sum(x["label"] == "UNSAT" for x in rows),
        "random_control": random_control,
        "raw_sha256": hashlib.sha256(RAW.read_bytes()).hexdigest(),
        "elapsed_seconds": round(time.monotonic() - started, 6),
    }
    SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
