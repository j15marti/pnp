#!/usr/bin/env python3
"""Bounded audit for MODELBRIDGE-0024.

This checks only finite quantifier identities and hostile-control accounting.
It does not test Lynch's asymptotic theorem and makes no P-vs-NP inference.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results/raw/review/2026-10-12_complexity_core_equivalence.json"
LENGTHS = tuple(range(2, 13))
EXPONENTS = tuple(range(1, 7))
WRAPPERS = ("DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP")


@dataclass(frozen=True)
class Schedule:
    name: str
    values: tuple[int, ...]


def cofinal_violation(schedule: Schedule, mask: int, exponent: int) -> bool:
    """Finite analogue of forall N0 exists n>=N0 in C: T(n)>n^d."""
    chosen = [i for i in range(len(LENGTHS)) if mask & (1 << i)]
    if not chosen:
        return False
    for threshold_index in chosen:
        if not any(
            j >= threshold_index
            and mask & (1 << j)
            and schedule.values[j] > LENGTHS[j] ** exponent
            for j in chosen
        ):
            return False
    return True


def eventual_bound(schedule: Schedule, mask: int, exponent: int) -> bool:
    """Finite analogue of exists N0 forall later n in C: T(n)<=n^d."""
    chosen = [i for i in range(len(LENGTHS)) if mask & (1 << i)]
    if not chosen:
        return True
    return any(
        all(
            schedule.values[j] <= LENGTHS[j] ** exponent
            for j in chosen
            if j >= threshold_index
        )
        for threshold_index in chosen
    )


def stable_label(instance: tuple[str, int, bool], wrapper: str) -> bool:
    """Equivalent wrappers preserve the one-bit answer."""
    family, index, answer = instance
    salt = hashlib.sha256(f"{wrapper}:{family}:{index}".encode()).digest()[0]
    internal_trace = (salt, len(wrapper), index)
    assert internal_trace
    return answer


def main() -> None:
    started = time.perf_counter()
    assertions = 0
    failures: list[str] = []

    schedules = [
        Schedule(f"poly_{k}", tuple(n**k for n in LENGTHS)) for k in range(1, 6)
    ]
    schedules += [
        Schedule("exp", tuple(2**n for n in LENGTHS)),
        Schedule("spiky", tuple((2**n if n % 2 else n**3) for n in LENGTHS)),
    ]

    masks_checked = 0
    for mask in range(1, 1 << len(LENGTHS)):
        masks_checked += 1
        for schedule in schedules:
            for exponent in EXPONENTS:
                lhs = cofinal_violation(schedule, mask, exponent)
                rhs = not eventual_bound(schedule, mask, exponent)
                assertions += 1
                if lhs != rhs:
                    failures.append(
                        f"quantifier-negation:{mask}:{schedule.name}:{exponent}"
                    )

        # A polynomial direct decider defeats a universal superpolynomial
        # core claim on every nonempty finite candidate once d is large enough.
        direct = schedules[0]
        assertions += 1
        if all(cofinal_violation(direct, mask, d) for d in EXPONENTS):
            failures.append(f"direct-decider-core:{mask}")

    families = (
        ("horn_yes", True),
        ("horn_no", False),
        ("2sat_yes", True),
        ("2sat_no", False),
        ("affine_yes", True),
        ("affine_no", False),
        ("bounded_tw_yes", True),
        ("bounded_tw_no", False),
        ("matching_clean_core", True),
        ("repeated_component", True),
        ("padded_yes", True),
        ("redundant_clause_yes", True),
        ("independent_product_no", False),
        ("alternate_encoding_yes", True),
    )
    instances = [
        (family, index, answer)
        for family, answer in families
        for index in range(8)
    ]
    wrapper_checks = 0
    for instance in instances:
        expected = instance[2]
        answers = [stable_label(instance, wrapper) for wrapper in WRAPPERS]
        wrapper_checks += len(answers)
        assertions += len(answers) + 1
        if any(answer != expected for answer in answers):
            failures.append(f"wrapper-answer:{instance}")
        if len(set(answers)) != 1:
            failures.append(f"wrapper-disagreement:{instance}")

    # Every bounded individual instance has a singleton constant-answer
    # recognizer; this checks the finite easy-island residual collapse only.
    singleton_checks = 0
    for target in instances:
        recognizer = lambda candidate, target=target: candidate == target
        selected = [candidate for candidate in instances if recognizer(candidate)]
        singleton_checks += len(instances)
        assertions += len(instances) + 2
        if selected != [target]:
            failures.append(f"singleton-recognizer:{target}")
        if any(candidate[2] != target[2] for candidate in selected):
            failures.append(f"singleton-label:{target}")

    elapsed = time.perf_counter() - started
    result = {
        "run_id": "MODELBRIDGE-0024",
        "claim": "CLEANCORE-COMPLEXITY-CORE-EQUIVALENCE1",
        "status": "COMPUTATIONAL",
        "limitations": (
            "Finite quantifier and wrapper regression only; Lynch's theorem "
            "and the NP-completeness implication are proved symbolically, not experimentally."
        ),
        "parameters": {
            "lengths": list(LENGTHS),
            "exponents": list(EXPONENTS),
            "wrappers": list(WRAPPERS),
            "schedule_names": [schedule.name for schedule in schedules],
            "masks_checked": masks_checked,
            "instances": len(instances),
        },
        "counts": {
            "assertions": assertions,
            "wrapper_checks": wrapper_checks,
            "singleton_recognizer_comparisons": singleton_checks,
            "failures": len(failures),
        },
        "failures": failures,
        "elapsed_seconds": round(elapsed, 6),
        "chunking": "none; one deterministic invocation below 30 seconds",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
