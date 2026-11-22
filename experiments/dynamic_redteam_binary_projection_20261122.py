"""Exhaustive independent truth-table audit of the pinned reduction."""
from collections import Counter
from itertools import combinations, combinations_with_replacement
import inspect
import json
import hashlib
import dynamic_discovery_mixed_to_binary_20261122 as peer

FACTORS = [(0, 1, 2), (3, 4, 5)]


def truth_mask(rows, exact_one=False):
    result = 0
    for assignment in range(256):
        totals = [sum((assignment >> v) & 1 for v in row) for row in rows]
        if all(total == 1 if exact_one else total % 2 == 0 for total in totals):
            result |= 1 << assignment
    return result


def main():
    pool = list(combinations(range(8), 3))
    base = truth_mask(FACTORS, True)
    masks = [truth_mask([row]) for row in pool]
    outcomes = Counter()
    order_changes = 0
    corrected_changes = 0
    corrected_outcomes = Counter()
    first_declines = {}
    for size in range(4):
        for indices in combinations_with_replacement(range(len(pool)), size):
            rows = [pool[i] for i in indices]
            models = base
            for i in indices:
                models &= masks[i]
            label = "SAT" if models else "UNSAT"
            answer = peer.reduce_source(FACTORS, rows)
            reversed_answer = peer.reduce_source(FACTORS, list(reversed(rows)))
            assert answer in ("UNKNOWN", label)
            assert reversed_answer in ("UNKNOWN", label)
            order_changes += answer != reversed_answer
            outcomes[answer + "/" + label] += 1
            contradiction = any(set(row) in [set(f) for f in FACTORS] for row in rows)
            corrected = "UNSAT" if contradiction else answer
            corrected_reverse = "UNSAT" if contradiction else reversed_answer
            assert corrected in ("UNKNOWN", label)
            corrected_changes += corrected != corrected_reverse
            corrected_outcomes[corrected + "/" + label] += 1
            if answer == "UNKNOWN":
                first_declines.setdefault(label, rows)
    print(json.dumps({
        "peer_source_sha256": hashlib.sha256(inspect.getsource(peer).encode()).hexdigest(),
        "universe": "all multisets of 0 through 3 ternary parity rows over 8 names",
        "factors": FACTORS, "cases": sum(outcomes.values()),
        "outcomes": dict(outcomes), "reversal_changes": order_changes,
        "first_declines": first_declines, "wrong_decisions": 0,
        "contradiction_prescan_outcomes": dict(corrected_outcomes),
        "contradiction_prescan_reversal_changes": corrected_changes
    }, indent=2))


if __name__ == "__main__":
    main()
