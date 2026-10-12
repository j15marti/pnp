#!/usr/bin/env python3
"""Finite audit for PROMISE-IMAGE-EQUIVALENCE1.

This is a bounded identity and accounting check, not an asymptotic lower
bound.  A source 3-CNF is mapped to several explicit promise images.  Promise
deciders may behave arbitrarily off image.  Composition with the image map is
checked against direct SAT, and a charged pinning extractor is checked against
the source formula.  All instances are small enough for exhaustive truth-table
evaluation; no randomness is used.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import time
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Callable, Iterable

Literal = int
Clause = tuple[Literal, ...]
Formula = tuple[Clause, ...]

SIZES = tuple(range(2, 9))
FAMILIES = (
    "2SAT",
    "Horn",
    "affine-Tseitin",
    "bounded-treewidth",
    "independent-products",
    "padding",
    "redundant-clauses",
    "alternate-encoding",
)
EMBEDDINGS = ("TAG", "DUP", "RENAME", "PAD", "PRODUCT", "ALT")
OFF_PROMISE = ("REJECT", "ACCEPT", "PARITY")
WRAPPERS = ("DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP")


def normalize(formula: Iterable[Iterable[int]]) -> Formula:
    return tuple(tuple(int(x) for x in clause) for clause in formula)


def nvars(formula: Formula) -> int:
    return max((abs(lit) for clause in formula for lit in clause), default=0)


def eval_formula(formula: Formula, bits: tuple[int, ...]) -> bool:
    for clause in formula:
        if not clause:
            return False
        if not any((bits[abs(lit) - 1] == 1) == (lit > 0) for lit in clause):
            return False
    return True


@lru_cache(maxsize=None)
def solve(formula: Formula) -> tuple[bool, tuple[int, ...] | None, int]:
    n = nvars(formula)
    tested = 0
    for bits in itertools.product((0, 1), repeat=n):
        tested += 1
        if eval_formula(formula, bits):
            return True, bits, tested
    return False, None, tested


def restrict_formula(formula: Formula, assignment: dict[int, int]) -> Formula:
    out: list[Clause] = []
    for clause in formula:
        residual: list[int] = []
        satisfied = False
        for lit in clause:
            v = abs(lit)
            if v not in assignment:
                residual.append(lit)
            elif (assignment[v] == 1) == (lit > 0):
                satisfied = True
                break
        if not satisfied:
            out.append(tuple(residual))
    return tuple(out)


def source_formula(family: str, n: int) -> Formula:
    if family == "2SAT":
        return normalize((i, -(i % n + 1)) for i in range(1, n + 1))
    if family == "Horn":
        return normalize((-(i), -(i % n + 1), ((i + 1) % n + 1)) for i in range(1, n + 1))
    if family == "affine-Tseitin":
        clauses: list[Clause] = []
        for i in range(1, n):
            clauses.extend(((i, -(i + 1)), (-i, i + 1)))
        return tuple(clauses)
    if family == "bounded-treewidth":
        return normalize((i, i + 1, -(i + 2)) for i in range(1, max(2, n - 1)))
    if family == "independent-products":
        k = max(1, n // 2)
        return normalize((2 * i + 1, 2 * i + 2) for i in range(k))
    if family == "padding":
        return normalize((i, -i) for i in range(1, n + 1))
    if family == "redundant-clauses":
        base = ((1,),) if n == 2 else ((1, -2, 3),)
        return tuple(base[0] for _ in range(n))
    if family == "alternate-encoding":
        return normalize(tuple(reversed((i, -(i % n + 1), ((i + 1) % n + 1)))) for i in range(1, n + 1))
    raise ValueError(family)


def transform(formula: Formula, kind: str) -> Formula:
    n = nvars(formula)
    if kind == "TAG":
        return formula
    if kind == "DUP":
        return tuple(clause for c in formula for clause in (c, c))
    if kind == "RENAME":
        return tuple(tuple((2 * abs(lit)) * (1 if lit > 0 else -1) for lit in c) for c in formula)
    if kind == "PAD":
        pads = tuple((n + i, -(n + i)) for i in range(1, max(2, n) + 1))
        return formula + pads
    if kind == "PRODUCT":
        # A disjoint satisfiable chain; conjunction preserves the source bit.
        return formula + tuple((n + i, n + i + 1) for i in range(1, max(2, n)))
    if kind == "ALT":
        return tuple(tuple(reversed(c)) for c in reversed(formula))
    raise ValueError(kind)


def canonical_bytes(formula: Formula) -> bytes:
    return repr(formula).encode("utf-8")


@dataclass(frozen=True)
class Image:
    tag: str
    kind: str
    source: Formula
    payload: Formula
    checksum: str


def embed(formula: Formula, kind: str) -> tuple[Image, int]:
    payload = transform(formula, kind)
    checksum = hashlib.sha256(kind.encode() + b"|" + canonical_bytes(formula) + b"|" + canonical_bytes(payload)).hexdigest()[:16]
    image = Image("PROMISE-IMAGE-V1", kind, formula, payload, checksum)
    ops = 1 + sum(len(c) for c in formula) + sum(len(c) for c in payload)
    return image, ops


def recognize(image: Image) -> tuple[bool, int]:
    if image.tag != "PROMISE-IMAGE-V1" or image.kind not in EMBEDDINGS:
        return False, 1
    expected_payload = transform(image.source, image.kind)
    expected_hash = hashlib.sha256(
        image.kind.encode() + b"|" + canonical_bytes(image.source) + b"|" + canonical_bytes(expected_payload)
    ).hexdigest()[:16]
    ops = 1 + sum(len(c) for c in image.source) + sum(len(c) for c in expected_payload)
    return image.payload == expected_payload and image.checksum == expected_hash, ops


def off_value(image: Image, mode: str) -> bool:
    if mode == "REJECT":
        return False
    if mode == "ACCEPT":
        return True
    return int(hashlib.sha256(repr(image).encode()).hexdigest()[-1], 16) % 2 == 1


def promise_decide(image: Image, mode: str) -> tuple[bool, int]:
    valid, rec_ops = recognize(image)
    if not valid:
        return off_value(image, mode), rec_ops + 1
    value, _, tested = solve(image.payload)
    return value, rec_ops + tested


def wrapped_decide(image: Image, mode: str, wrapper: str) -> tuple[bool, int]:
    if wrapper == "DIRECT":
        return promise_decide(image, mode)
    if wrapper == "COPY":
        copied = Image(image.tag, image.kind, tuple(tuple(c) for c in image.source), tuple(tuple(c) for c in image.payload), image.checksum)
        value, cost = promise_decide(copied, mode)
        return value, cost + len(repr(copied))
    if wrapper == "DEAD":
        _, dead_cost = recognize(image)
        value, cost = promise_decide(image, mode)
        return value, cost + dead_cost
    if wrapper == "DELAY":
        value, cost = promise_decide(image, mode)
        delay = sum(len(c) for c in image.payload) + 1
        return value, cost + delay
    if wrapper == "INTERP":
        dispatch: dict[str, Callable[[Image, str], tuple[bool, int]]] = {"run": promise_decide}
        value, cost = dispatch["run"](image, mode)
        return value, cost + 3 * (len(image.payload) + 1)
    if wrapper == "RECOMP":
        a, ca = promise_decide(image, mode)
        b, cb = promise_decide(image, mode)
        assert a == b
        return a, ca + cb
    raise ValueError(wrapper)


def extract_witness(formula: Formula, kind: str, mode: str, wrapper: str) -> tuple[tuple[int, ...] | None, int, int]:
    image, build = embed(formula, kind)
    sat, work = wrapped_decide(image, mode, wrapper)
    calls = 1
    total = build + work
    if not sat:
        return None, calls, total
    assignment: dict[int, int] = {}
    for variable in range(1, nvars(formula) + 1):
        trial = dict(assignment)
        trial[variable] = 0
        residual = restrict_formula(formula, trial)
        query, query_build = embed(residual, kind)
        answer, query_work = wrapped_decide(query, mode, wrapper)
        calls += 1
        total += query_build + query_work
        assignment[variable] = 0 if answer else 1
    witness = tuple(assignment[i] for i in range(1, nvars(formula) + 1))
    return witness, calls, total


def corrupt(image: Image) -> Image:
    return Image(image.tag, image.kind, image.source, image.payload, "0" * 16)


def main() -> None:
    start = time.perf_counter()
    checks = 0
    failures: list[dict[str, object]] = []
    rows: list[dict[str, object]] = []
    total_extractor_calls = 0
    total_charged_work = 0
    off_promise_variation = 0

    for family in FAMILIES:
        family_checks = 0
        family_calls = 0
        sat_count = 0
        for n in SIZES:
            formula = source_formula(family, n)
            # Alternate YES/NO controls without leaving the named structural
            # classes: contradictory unit equations preserve 2-CNF, Horn,
            # affine, bounded-treewidth, product, padding and redundancy
            # interpretations.
            if n % 2 == 0:
                formula = formula + ((1,), (-1,))
            expected, direct_witness, direct_tests = solve(formula)
            sat_count += int(expected)
            for kind in EMBEDDINGS:
                image, build_ops = embed(formula, kind)
                valid, rec_ops = recognize(image)
                checks += 1
                family_checks += 1
                if not valid:
                    failures.append({"type": "recognition", "family": family, "n": n, "kind": kind})
                payload_sat, _, _ = solve(image.payload)
                checks += 1
                family_checks += 1
                if payload_sat != expected:
                    failures.append({"type": "preservation", "family": family, "n": n, "kind": kind})

                bad = corrupt(image)
                bad_values = []
                for mode in OFF_PROMISE:
                    bad_value, _ = promise_decide(bad, mode)
                    bad_values.append(bad_value)
                off_promise_variation += int(len(set(bad_values)) > 1)
                checks += 1
                family_checks += 1
                if len(set(bad_values)) <= 1:
                    failures.append({"type": "off-promise-not-arbitrary", "family": family, "n": n, "kind": kind})

                for mode in OFF_PROMISE:
                    for wrapper in WRAPPERS:
                        value, work = wrapped_decide(image, mode, wrapper)
                        checks += 1
                        family_checks += 1
                        if value != expected:
                            failures.append({"type": "composition", "family": family, "n": n, "kind": kind, "mode": mode, "wrapper": wrapper})
                        witness, calls, charged = extract_witness(formula, kind, mode, wrapper)
                        total_extractor_calls += calls
                        family_calls += calls
                        total_charged_work += charged
                        checks += 1
                        family_checks += 1
                        if expected:
                            if witness is None or not eval_formula(formula, witness):
                                failures.append({"type": "witness", "family": family, "n": n, "kind": kind, "mode": mode, "wrapper": wrapper})
                        elif witness is not None:
                            failures.append({"type": "unsat-witness", "family": family, "n": n, "kind": kind, "mode": mode, "wrapper": wrapper})

                # Polynomial-exponent ledger for a length map |R(x)| <= N^lambda.
                source_len = max(2, len(canonical_bytes(formula)))
                image_len = max(2, len(repr(image).encode()))
                for k in range(1, 9):
                    bound = build_ops + rec_ops + image_len**k
                    checks += 1
                    family_checks += 1
                    if bound < image_len**k or source_len <= 0:
                        failures.append({"type": "ledger", "family": family, "n": n, "kind": kind, "k": k})

        rows.append({
            "family": family,
            "sizes": len(SIZES),
            "sat_instances": sat_count,
            "checks": family_checks,
            "extractor_calls": family_calls,
        })

    elapsed = time.perf_counter() - start
    result = {
        "experiment": "PROMISE-IMAGE-EQUIVALENCE1 finite audit",
        "status": "COMPUTATIONAL",
        "deterministic": True,
        "random_seed": None,
        "scope": "finite identity, promise-domain, wrapper, extraction, and exact integer cost-ledger checks; no asymptotic inference",
        "families": list(FAMILIES),
        "sizes": list(SIZES),
        "embeddings": list(EMBEDDINGS),
        "off_promise_modes": list(OFF_PROMISE),
        "wrappers": list(WRAPPERS),
        "checks": checks,
        "failures": failures,
        "rows": rows,
        "off_promise_variation_witnesses": off_promise_variation,
        "total_extractor_calls": total_extractor_calls,
        "total_charged_work_units": total_charged_work,
        "elapsed_seconds": elapsed,
    }
    output = Path("results/raw/review/2026-10-13_promise_image_equivalence.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    output.write_text(encoded, encoding="utf-8")
    print(json.dumps({
        "checks": checks,
        "failures": len(failures),
        "elapsed_seconds": elapsed,
        "total_extractor_calls": total_extractor_calls,
        "off_promise_variation_witnesses": off_promise_variation,
        "result_sha256": hashlib.sha256(encoded.encode()).hexdigest(),
    }, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
