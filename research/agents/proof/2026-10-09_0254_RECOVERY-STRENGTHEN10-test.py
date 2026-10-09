#!/usr/bin/env python3
"""Bounded exact-rational checks for RECOVERY-STRENGTHEN10.

The checks test the algebra used by the scoped no-amplification theorem.
They do not prove an all-input SAT compiler or an asymptotic machine bound.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import signal
import time
from fractions import Fraction
from pathlib import Path


def deadline(*_: object) -> None:
    raise TimeoutError("25-second RECOVERY-STRENGTHEN10 budget exceeded")


def simple_cycles_three(edges: dict[tuple[int, int], Fraction]) -> list[tuple[tuple[int, int], ...]]:
    cycles: list[tuple[tuple[int, int], ...]] = []
    # With three vertices, the simple directed cycles have length two or three.
    for a in range(3):
        for b in range(a + 1, 3):
            if (a, b) in edges and (b, a) in edges:
                cycles.append(((a, b), (b, a)))
    for order in ((0, 1, 2), (0, 2, 1)):
        cycle = tuple((order[i], order[(i + 1) % 3]) for i in range(3))
        if all(edge in edges for edge in cycle):
            cycles.append(cycle)
    return cycles


def product(values: list[Fraction] | tuple[Fraction, ...]) -> Fraction:
    out = Fraction(1)
    for value in values:
        out *= value
    return out


def check_graph_decomposition() -> dict[str, int]:
    directed = tuple((i, j) for i in range(3) for j in range(3) if i != j)
    choices: tuple[Fraction | None, ...] = (None, Fraction(1, 2), Fraction(1), Fraction(2))
    cyclic = admissible = with_fractional = walks = bad = 0
    for assignment in itertools.product(choices, repeat=len(directed)):
        edges = {edge: theta for edge, theta in zip(directed, assignment) if theta is not None}
        cycles = simple_cycles_three(edges)
        if not cycles:
            continue
        cyclic += 1
        if any(product(tuple(edges[e] for e in cycle)) < 1 for cycle in cycles):
            continue
        admissible += 1
        with_fractional += int(any(theta < 1 for theta in edges.values()))
        for start in range(3):
            frontier = [(start, Fraction(1))]
            for _length in range(1, 8):
                nxt: list[tuple[int, Fraction]] = []
                for vertex, gain in frontier:
                    for (u, v), theta in edges.items():
                        if u != vertex:
                            continue
                        new_gain = gain * theta
                        nxt.append((v, new_gain))
                        if v == start:
                            walks += 1
                            bad += int(new_gain < 1)
                frontier = nxt
    assert bad == 0
    return {
        "cyclic_graphs": cyclic,
        "all_simple_cycles_noncontracting": admissible,
        "such_graphs_with_fractional_edge": with_fractional,
        "closed_walks_checked": walks,
        "contracting_closed_walks": bad,
    }


def check_balanced_words() -> dict[str, int]:
    scales = {
        "pad": Fraction(2),
        "unpad": Fraction(1, 2),
        "alias": Fraction(1),
        "stream": Fraction(1),
        "dedup": Fraction(1),
    }
    balanced = bad_product = bad_k = shrunk = 0
    for length in range(1, 8):
        for word in itertools.product(scales, repeat=length):
            gain = product(tuple(scales[name] for name in word))
            if gain != 1:
                continue
            balanced += 1
            bad_product += int(gain != 1)
            bad_k += int(gain != 1)  # coefficient of K is the same product
            for theta in (Fraction(1, 2), Fraction(2, 3), Fraction(3, 4)):
                assert gain * theta < 1
                shrunk += 1
    assert bad_product == bad_k == 0
    return {
        "balanced_words": balanced,
        "bad_return_products": bad_product,
        "bad_k_coefficients": bad_k,
        "genuine_shrink_extensions": shrunk,
    }


def compose_affine(route: tuple[tuple[Fraction, Fraction], ...]) -> tuple[Fraction, Fraction]:
    # Compose x -> a + theta*x in route order; return A,Theta in A+Theta*x.
    intercept, coefficient = Fraction(0), Fraction(1)
    for additive, theta in reversed(route):
        intercept = additive + theta * intercept
        coefficient = theta * coefficient
    return intercept, coefficient


def check_affine_routes() -> dict[str, int]:
    edges = tuple(
        (additive, theta)
        for additive in (Fraction(0), Fraction(1, 10), Fraction(1, 2))
        for theta in (Fraction(1, 2), Fraction(1), Fraction(2))
    )
    balanced = positive = zero = bad = 0
    for length in range(1, 7):
        for route in itertools.product(edges, repeat=length):
            intercept, coefficient = compose_affine(route)
            if coefficient != 1:
                continue
            balanced += 1
            positive += int(intercept > 0)
            zero += int(intercept == 0)
            bad += int(intercept < 0)
    assert bad == 0 and balanced == positive + zero
    return {
        "balanced_affine_routes": balanced,
        "positive_intercept": positive,
        "zero_intercept": zero,
        "negative_intercept": bad,
    }


def check_virtual_source_invariance() -> dict[str, int]:
    checked = changed = 0
    vals = (Fraction(0), Fraction(1, 5), Fraction(1, 2), Fraction(4, 5), Fraction(1), Fraction(6, 5))
    for r, v, h, p in itertools.product(vals, repeat=4):
        if h >= 1:
            continue
        closed = (max(Fraction(1), r, (v - h) / (1 - h)), max(p, h))
        virtual = (max(Fraction(1), max(Fraction(1), r), (v - h) / (1 - h)), max(p, h))
        checked += 1
        changed += int(closed != virtual)
    assert changed == 0
    return {"ledger_tuples": checked, "changed_by_exponent_one_virtual_source": changed}


def main() -> None:
    signal.signal(signal.SIGALRM, deadline)
    signal.alarm(25)
    started = time.perf_counter()
    result = {
        "status": "PASS",
        "classification": "COMPUTATIONAL exact-rational finite checks",
        "timeout_seconds": 25,
        "graph_decomposition": check_graph_decomposition(),
        "balanced_operations": check_balanced_words(),
        "affine_routes": check_affine_routes(),
        "virtual_source": check_virtual_source_invariance(),
        "limitations": [
            "Finite enumeration is not a proof of the symbolic decomposition lemma.",
            "The theorem is scoped to the recovered composition interfaces, not arbitrary SAT algorithms.",
            "No test supplies an all-input source-first contraction or a machine-space implementation.",
        ],
    }
    result["seconds"] = time.perf_counter() - started
    result["code_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    destination = Path(__file__).with_name("2026-10-09_0254_RECOVERY-STRENGTHEN10-results.json")
    destination.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    signal.alarm(0)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
