#!/usr/bin/env python3
"""Exhaustive finite audit of selection-free semantic representative merging."""

import json
from pathlib import Path


def bit(word: int, position: int, length: int) -> int:
    return (word >> (length - 1 - position)) & 1


def run(length: int = 3) -> dict:
    words = list(range(1 << length))
    family_count = 0
    source_cases = 0
    prefix_steps = 0
    feasibility_checks = 0
    selector_disagreements = 0
    failures = []

    for mask in range(1 << len(words)):
        family = [w for w in words if (mask >> w) & 1]
        family_count += 1
        for source in words:
            source_cases += 1
            representative = family[-1] if family else None
            rejected = representative is None
            observed = []

            for position in range(length):
                prefix_steps += 1
                observed.append(bit(source, position, length))
                if rejected:
                    continue

                feasible = []
                for candidate in family:
                    feasibility_checks += 1
                    old_ok = all(
                        bit(candidate, j, length) == bit(representative, j, length)
                        for j in range(position)
                    )
                    new_ok = bit(candidate, position, length) == observed[position]
                    if old_ok and new_ok:
                        feasible.append(candidate)

                if not feasible:
                    rejected = True
                    representative = None
                else:
                    # Deliberately select the greatest feasible descriptor, not a
                    # minimum-size or lexicographically first representative.
                    chosen = feasible[-1]
                    if chosen != feasible[0]:
                        selector_disagreements += 1
                    representative = chosen

                if representative is not None:
                    represented_prefix = [
                        bit(representative, j, length) for j in range(position + 1)
                    ]
                    if represented_prefix != observed:
                        failures.append(
                            {
                                "kind": "prefix_invariant",
                                "mask": mask,
                                "source": source,
                                "position": position,
                            }
                        )

            expected_accept = source in family
            actual_accept = not rejected
            if actual_accept != expected_accept:
                failures.append(
                    {"kind": "final_decision", "mask": mask, "source": source}
                )
            if actual_accept and representative != source:
                failures.append(
                    {
                        "kind": "final_witness",
                        "mask": mask,
                        "source": source,
                        "representative": representative,
                    }
                )

    return {
        "run": "SELECTION_FREE_STREAM_MERGE6",
        "date_seoul": "2026-10-19 23:48",
        "finite_model": {
            "truth_table_bits": length,
            "witness_semantics": "all binary words of the same length",
            "selector": "greatest feasible witness (deliberately non-lexicographic-minimum)",
        },
        "family_count": family_count,
        "source_cases": source_cases,
        "prefix_steps": prefix_steps,
        "feasibility_checks": feasibility_checks,
        "selector_disagreements": selector_disagreements,
        "failed_assertions": len(failures),
        "failure_examples": failures[:10],
        "status": {
            "selection_free_induction": "PROVED_AND_COMPUTATIONALLY_AUDITED",
            "MMW_streaming_lower_bound": "OPEN",
            "P_vs_NP": "OPEN",
        },
    }


if __name__ == "__main__":
    result = run()
    assert result["failed_assertions"] == 0, result["failure_examples"]
    out = Path("results/raw/synthesis/2026-10-19_2348_SELECTION_FREE_STREAM_MERGE6.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
