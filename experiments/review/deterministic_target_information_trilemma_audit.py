#!/usr/bin/env python3
"""Finite audit for MODELBRIDGE-0029.

Checks Shannon-information identities for deterministic targets H=g(X).
This is a bounded identity test, not an asymptotic lower bound.
"""

from __future__ import annotations

from collections import Counter, defaultdict
import itertools
import json
import math
from pathlib import Path


def entropy(values: list[object]) -> float:
    counts = Counter(values)
    total = len(values)
    return -sum((c / total) * math.log2(c / total) for c in counts.values())


def conditional_entropy(y: list[object], z: list[object]) -> float:
    groups: dict[object, list[object]] = defaultdict(list)
    for yi, zi in zip(y, z):
        groups[zi].append(yi)
    total = len(y)
    return sum((len(group) / total) * entropy(group) for group in groups.values())


def cmi(y: list[object], t: list[object], z: list[object]) -> float:
    # I(Y;T|Z)=H(Y|Z)-H(Y|T,Z)
    tz = list(zip(t, z))
    return conditional_entropy(y, z) - conditional_entropy(y, tz)


def prefix_parities(x: tuple[int, ...]) -> tuple[int, ...]:
    out = [0]
    for bit in x:
        out.append(out[-1] ^ bit)
    return tuple(out)


def reverse_bits(x: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(reversed(x))


def target_values(xs: list[tuple[int, ...]], name: str) -> list[object]:
    if name == "zero":
        return [0 for _ in xs]
    if name == "first":
        return [x[0] for x in xs]
    if name == "parity":
        return [sum(x) & 1 for x in xs]
    if name == "majority":
        return [int(sum(x) * 2 >= len(x)) for x in xs]
    if name == "weight":
        return [sum(x) for x in xs]
    if name == "identity":
        return list(xs)
    raise ValueError(name)


def answer_values(xs: list[tuple[int, ...]], mode: str) -> list[int]:
    if mode == "constant_yes":
        return [1 for _ in xs]
    if mode == "parity":
        return [sum(x) & 1 for x in xs]
    if mode == "first":
        return [x[0] for x in xs]
    raise ValueError(mode)


def main() -> None:
    tol = 1e-10
    identities = 0
    data_processing_checks = 0
    source_free_checks = 0
    copy_max_checks = 0
    hostile_control_checks = 0
    targets = ("zero", "first", "parity", "majority", "weight", "identity")
    answer_modes = ("constant_yes", "parity", "first")

    for n in range(1, 9):
        xs = list(itertools.product((0, 1), repeat=n))
        traces = {
            "dead": [0 for _ in xs],
            "answer_only": None,
            "copy": list(xs),
            "prefix": [prefix_parities(x) for x in xs],
            "reverse_encoding": [reverse_bits(x) for x in xs],
            "parity_projection": [sum(x) & 1 for x in xs],
            "weight_projection": [sum(x) for x in xs],
        }
        for answer_mode in answer_modes:
            answers = answer_values(xs, answer_mode)
            traces["answer_only"] = answers
            for target in targets:
                hs = target_values(xs, target)
                h_given_a = conditional_entropy(hs, answers)
                for trace_name, ts0 in traces.items():
                    ts = list(ts0)
                    # H is deterministic once X is fixed, so no trace has
                    # information surplus conditional on X (or X,A).
                    assert abs(cmi(hs, ts, list(xs))) < tol
                    assert abs(cmi(hs, ts, list(zip(xs, answers)))) < tol
                    identities += 2

                    # Conditional data processing: H=g(X).
                    ih = cmi(hs, ts, answers)
                    ix = cmi(list(xs), ts, answers)
                    assert ih <= ix + tol
                    data_processing_checks += 1
                    if abs(ix) < tol:
                        assert abs(ih) < tol
                        source_free_checks += 1

                # A raw source copy and any invertible transport attain the
                # maximum possible conditional target information.
                for name in ("copy", "prefix", "reverse_encoding"):
                    assert abs(cmi(hs, list(traces[name]), answers) - h_given_a) < tol
                    copy_max_checks += 1

    # Exact forced-assignment control: all formulas are YES, H is the unique
    # three-bit satisfying assignment.  Copy/prefix traces carry 3 bits about H
    # without an H-specific operation; parity carries exactly one bit.
    forced = list(itertools.product((0, 1), repeat=3))
    forced_h = list(forced)
    forced_a = [1] * len(forced)
    forced_prefix = [prefix_parities(x) for x in forced]
    forced_parity = [sum(x) & 1 for x in forced]
    forced_facts = {
        "H_H_given_answer": conditional_entropy(forced_h, forced_a),
        "I_H_copy_given_answer": cmi(forced_h, list(forced), forced_a),
        "I_H_prefix_given_answer": cmi(forced_h, forced_prefix, forced_a),
        "I_H_parity_given_answer": cmi(forced_h, forced_parity, forced_a),
        "I_H_prefix_given_source": cmi(forced_h, forced_prefix, list(forced)),
    }
    assert forced_facts == {
        "H_H_given_answer": 3.0,
        "I_H_copy_given_answer": 3.0,
        "I_H_prefix_given_answer": 3.0,
        "I_H_parity_given_answer": 1.0,
        "I_H_prefix_given_source": 0.0,
    }

    families = (
        "2SAT", "Horn", "affine_Tseitin", "bounded_treewidth",
        "independent_product", "padding", "redundant_clauses",
        "alternate_encoding", "signed_clean_core",
    )
    wrappers = ("DEAD", "COPY", "DELAY", "INTERP", "RECOMP")
    encodings = ("canonical", "reverse", "padded", "renamed")
    # These labels exercise invariance of the exact identities: none of the
    # names changes the deterministic relation H=g(X).
    for family, wrapper, encoding in itertools.product(families, wrappers, encodings):
        xs = forced
        ts = forced_prefix if wrapper in ("COPY", "DELAY", "INTERP", "RECOMP") else [0] * 8
        assert abs(cmi(forced_h, list(ts), list(xs))) < tol
        assert cmi(forced_h, list(ts), forced_a) <= cmi(list(xs), list(ts), forced_a) + tol
        hostile_control_checks += 2

    result = {
        "run_id": "INFONOGO1",
        "status": "COMPUTATIONAL finite Shannon-identity audit",
        "scope": "uniform source distributions on {0,1}^n for n=1..8; no asymptotic inference",
        "conditional_zero_identities": identities,
        "conditional_data_processing_checks": data_processing_checks,
        "source_free_implication_checks": source_free_checks,
        "copy_attains_maximum_checks": copy_max_checks,
        "hostile_control_checks": hostile_control_checks,
        "forced_assignment_information_bits": forced_facts,
        "conclusion": (
            "Unconditioned or answer-conditioned target information can be maximized by source copying; "
            "conditioning on the source makes deterministic-target information surplus identically zero."
        ),
        "p_vs_np": "OPEN",
    }
    out = Path("results/raw/review/2026-10-13_deterministic_target_information_trilemma.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
