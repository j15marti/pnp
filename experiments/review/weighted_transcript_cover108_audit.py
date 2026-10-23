#!/usr/bin/env python3
"""Independent audit for WEIGHTED-TRANSCRIPT-COVER108.

No SAT oracle and no third-party packages are used.  The tested promise family
has an equality 2-CNF backbone and q disjoint all-positive/all-negative
ternaries.  It is SAT exactly when the q orientation bits are uniform.
"""

from itertools import product, combinations
import json


def label(bits):
    return len(set(bits)) == 1


def diff(x, y):
    return frozenset(i for i, (a, b) in enumerate(zip(x, y)) if a != b)


def weighted_cover(edges, costs):
    if not edges:
        return 0
    q = len(costs)
    best = sum(costs) + 1
    for mask in range(1 << q):
        chosen = {i for i in range(q) if (mask >> i) & 1}
        if all(chosen & edge for edge in edges):
            best = min(best, sum(costs[i] for i in chosen))
    return best


def transcript_edges(x, queried):
    q = len(x)
    out = []
    for y in product((0, 1), repeat=q):
        if label(y) == label(x):
            continue
        if all(y[i] == x[i] for i in queried):
            out.append(diff(x, y))
    return out


def expected_tau(x, costs):
    if label(x):
        return sum(costs)
    pos = [costs[i] for i, b in enumerate(x) if b]
    neg = [costs[i] for i, b in enumerate(x) if not b]
    return min(pos) + min(neg)


def family_counts(q):
    return {
        "variables": 3 * q,
        "binary_clauses": 6 * q - 2,
        "ternary_clauses": q,
        "clauses": 7 * q - 2,
        "literal_reads_full_parse": 15 * q - 4,
        "fixed_record_words": 28 * q - 6,
        "raw_strong_2cnf_backdoor": q,
    }


def audit():
    checks = 0
    failures = []
    summaries = []
    for q in range(2, 9):
        costs = tuple(1 + ((3 * i + q) % 5) for i in range(q))
        sat = unsat = 0
        for x in product((0, 1), repeat=q):
            sat += int(label(x))
            unsat += int(not label(x))
            edges = transcript_edges(x, frozenset())
            tau = weighted_cover(edges, costs)
            want = expected_tau(x, costs)
            checks += 1
            if tau != want:
                failures.append(("tau_formula", q, x, tau, want))

            # Verify the weighted one-step Lipschitz/telescoping inequality
            # on every prefix of the natural query order.
            previous = tau
            queried = set()
            spent = 0
            for i in range(q):
                queried.add(i)
                spent += costs[i]
                now = weighted_cover(transcript_edges(x, queried), costs)
                checks += 2
                if not (0 <= previous - now <= costs[i]):
                    failures.append(("drop", q, x, i, previous, now, costs[i]))
                if tau > spent + now:
                    failures.append(("telescoping", q, x, i, tau, spent, now))
                previous = now

            checks += 1
            if previous != 0:
                failures.append(("terminal", q, x, previous))

            # Restricted adaptive promise policy: stop when both signs have
            # been observed; otherwise exhaust the q orientations.
            seen = set()
            reads = 0
            for b in x:
                reads += 1
                seen.add(b)
                if len(seen) == 2:
                    break
            answer = len(seen) == 1
            checks += 1
            if answer != label(x):
                failures.append(("policy", q, x, reads, answer))

        checks += 2
        if sat != 2 or unsat != (1 << q) - 2:
            failures.append(("label_counts", q, sat, unsat))
        summaries.append({
            "q": q,
            "costs": costs,
            "sat_inputs": sat,
            "unsat_inputs": unsat,
            "uniform_tau": sum(costs),
            "family": family_counts(q),
        })

    # Explicit SAT/UNSAT state-switching controls at scale.
    q = 1024
    controls = {
        "sat_all_one": tuple([1] * q),
        "sat_all_zero": tuple([0] * q),
        "unsat_early_switch": tuple([1, 0] + [1] * (q - 2)),
        "unsat_late_switch": tuple([1] * (q - 1) + [0]),
    }
    control_rows = []
    for name, x in controls.items():
        seen = set()
        reads = 0
        for b in x:
            reads += 1
            seen.add(b)
            if len(seen) == 2:
                break
        got = len(seen) == 1
        checks += 1
        if got != label(x):
            failures.append(("large_control", name, reads, got))
        control_rows.append({
            "name": name,
            "label": "SAT" if got else "UNSAT",
            "orientation_reads_in_promise_policy": reads,
            "full_language_recognition_requires_full_source_validation": True,
            "counts": family_counts(q),
        })

    result = {
        "run": "WEIGHTED-TRANSCRIPT-COVER108",
        "status": "COMPUTATIONAL",
        "scope": "exhaustive q=2..8 plus four q=1024 switching controls",
        "random_seed": None,
        "checks": checks,
        "failures": failures,
        "summary": summaries,
        "controls": control_rows,
        "limitations": [
            "Finite tests do not prove asymptotic lower bounds.",
            "Promise-policy early stopping is not all-decider coverage.",
            "Event and record counts are not physical CPU instructions.",
            "Peak Python RSS was not measured.",
        ],
    }
    return result


if __name__ == "__main__":
    result = audit()
    payload = json.dumps(result, indent=2, sort_keys=True)
    print(payload)
    raise SystemExit(1 if result["failures"] else 0)
