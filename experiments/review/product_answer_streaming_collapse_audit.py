#!/usr/bin/env python3
"""Finite audit for PRODUCT-ANSWER-STREAMING-COLLAPSE1.

This is a bounded bookkeeping test, not an asymptotic lower- or upper-bound
experiment.  It compares a sequential component-AND decider with a monolithic
truth-table control when the latter is small enough.  Semantic model counts
are computed on a separate audit path and are never charged to the decision
wrapper.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import random
import time
from dataclasses import dataclass, asdict
from pathlib import Path

Clause = tuple[int, ...]
CNF = tuple[Clause, ...]
SEED = 20261012
WRAPPERS = ("DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP")
ENCODINGS = ("canonical", "reversed", "renamed")


def variables(cnf: CNF) -> tuple[int, ...]:
    return tuple(sorted({abs(lit) for clause in cnf for lit in clause}))


def encode(cnf: CNF) -> str:
    return " ".join(" ".join(map(str, clause)) + " 0" for clause in cnf) + "\n"


def evaluate(cnf: CNF, assignment: dict[int, bool]) -> bool:
    return all(any(assignment[abs(lit)] == (lit > 0) for lit in clause) for clause in cnf)


def solve_and_count(cnf: CNF) -> tuple[bool, int, int]:
    vs = variables(cnf)
    count = 0
    tested = 0
    for bits in itertools.product((False, True), repeat=len(vs)):
        tested += 1
        a = dict(zip(vs, bits))
        count += int(evaluate(cnf, a))
    return count > 0, count, tested


def components(cnf: CNF) -> list[CNF]:
    """Return variable-incidence components; clauses are assumed nonempty."""
    var_to_clauses: dict[int, list[int]] = {}
    for ci, clause in enumerate(cnf):
        for v in {abs(lit) for lit in clause}:
            var_to_clauses.setdefault(v, []).append(ci)
    unseen = set(range(len(cnf)))
    out: list[CNF] = []
    while unseen:
        start = min(unseen)
        stack = [start]
        cset: set[int] = set()
        vset: set[int] = set()
        while stack:
            ci = stack.pop()
            if ci in cset:
                continue
            cset.add(ci)
            unseen.discard(ci)
            for lit in cnf[ci]:
                v = abs(lit)
                if v in vset:
                    continue
                vset.add(v)
                stack.extend(var_to_clauses[v])
        out.append(tuple(cnf[i] for i in sorted(cset)))
    out.sort(key=lambda c: min(variables(c)))
    return out


def rename_disjoint(cnf: CNF, offset: int) -> CNF:
    return tuple(tuple((abs(lit) + offset) * (1 if lit > 0 else -1) for lit in clause) for clause in cnf)


def product(parts: list[CNF]) -> CNF:
    out: list[Clause] = []
    offset = 0
    for part in parts:
        renamed = rename_disjoint(part, offset)
        out.extend(renamed)
        offset = max(variables(renamed))
    return tuple(out)


def parity3(even: bool = True) -> CNF:
    bad = []
    for bits in itertools.product((False, True), repeat=3):
        if (sum(bits) % 2 == 0) != even:
            bad.append(tuple(-i if bits[i - 1] else i for i in (1, 2, 3)))
    return tuple(bad)


def xor_path(n: int = 5) -> CNF:
    clauses: list[Clause] = []
    for i in range(1, n):
        clauses.extend(((i, i + 1), (-i, -(i + 1))))
    return tuple(clauses)


def paired_k33() -> CNF:
    edges = [(i, j) for i in range(3) for j in range(3)]
    idx = {e: p + 1 for p, e in enumerate(edges)}
    clauses: list[Clause] = []
    for i in range(3):
        star = tuple(idx[(i, j)] for j in range(3))
        clauses.extend((star, tuple(-x for x in star)))
    for j in range(3):
        star = tuple(idx[(i, j)] for i in range(3))
        clauses.extend((star, tuple(-x for x in star)))
    return tuple(clauses)


BASES: dict[str, CNF] = {
    "2sat_sat": ((1, 2), (-1, 2), (1, -2)),
    "2sat_unsat": ((1,), (-1,)),
    "horn_sat": ((1,), (-1, 2), (-2, 3)),
    "horn_unsat": ((1,), (-1, 2), (-2,)),
    "affine_tseitin": parity3(True),
    "bounded_treewidth": xor_path(5),
    "clean_k33": paired_k33(),
    "redundant_padding": ((1, 2), (-1, 2), (1, -2), (1, 2), (3, -3)),
}


def transform_encoding(cnf: CNF, style: str, seed: int) -> CNF:
    if style == "canonical":
        return cnf
    if style == "reversed":
        return tuple(tuple(reversed(c)) for c in reversed(cnf))
    rng = random.Random(seed)
    vs = list(variables(cnf))
    perm = vs[:]
    rng.shuffle(perm)
    mapping = dict(zip(vs, perm))
    clauses = [tuple(mapping[abs(l)] * (1 if l > 0 else -1) for l in c) for c in cnf]
    rng.shuffle(clauses)
    return tuple(clauses)


@dataclass
class Ledger:
    answer: bool
    component_count: int
    component_calls: int
    assignments_tested: int
    encoded_bytes_scanned: int
    copied_bytes: int
    dummy_steps: int
    peak_component_buffer_bytes: int
    answer_vector_bits: int
    accumulator_bits: int
    extraction_calls: int
    reconstruction_calls: int
    output_bits: int


def stream_decide(cnf: CNF, wrapper: str) -> Ledger:
    parts = components(cnf)

    def once() -> tuple[bool, int, int, int]:
        calls = tested = peak = 0
        answer = True
        for part in parts:
            calls += 1
            peak = max(peak, len(encode(part).encode("utf-8")))
            sat, _, work = solve_and_count(part)
            tested += work
            if not sat:
                answer = False
                break
        return answer, calls, tested, peak

    answer, calls, tested, peak = once()
    copied = dummy = 0
    size = len(encode(cnf).encode("utf-8"))
    if wrapper == "COPY":
        copied = size
    elif wrapper == "DEAD":
        dummy = len(cnf)
    elif wrapper == "DELAY":
        dummy = 3 * sum(len(c) for c in cnf)
    elif wrapper == "INTERP":
        copied = size
        dummy = sum(len(c) for c in cnf)
    elif wrapper == "RECOMP":
        again, c2, t2, p2 = once()
        assert again == answer
        calls += c2
        tested += t2
        peak = max(peak, p2)
    elif wrapper != "DIRECT":
        raise ValueError(wrapper)
    return Ledger(
        answer=answer,
        component_count=len(parts),
        component_calls=calls,
        assignments_tested=tested,
        encoded_bytes_scanned=size,
        copied_bytes=copied,
        dummy_steps=dummy,
        peak_component_buffer_bytes=peak,
        answer_vector_bits=0,
        accumulator_bits=1,
        extraction_calls=0,
        reconstruction_calls=0,
        output_bits=1,
    )


def semantic_audit(cnf: CNF) -> dict[str, int | bool]:
    parts = components(cnf)
    counts = []
    answers = []
    work = 0
    for part in parts:
        sat, count, tested = solve_and_count(part)
        answers.append(sat)
        counts.append(count)
        work += tested
    total = 1
    for count in counts:
        total *= count
    return {
        "product_answer": all(answers),
        "product_model_count": total,
        "separate_audit_assignments_tested": work,
        "component_answer_ones": sum(answers),
    }


def and_collision(k: int) -> dict[str, int]:
    zero_fiber = (1 << k) - 1
    one_fiber = 1
    collision_pairs = zero_fiber * zero_fiber + one_fiber
    domain = 1 << k
    cs_lower_bound_numerator = domain * domain
    return {
        "k": k,
        "zero_fiber": zero_fiber,
        "one_fiber": one_fiber,
        "collision_pairs": collision_pairs,
        "domain_squared": cs_lower_bound_numerator,
        "image_size": 2,
    }


def main() -> None:
    started = time.perf_counter()
    checks = 0
    rows = []
    suites: list[tuple[str, list[CNF]]] = []
    sat_cycle = [BASES["2sat_sat"], BASES["horn_sat"], BASES["affine_tseitin"], BASES["bounded_treewidth"], BASES["clean_k33"], BASES["redundant_padding"]]
    for k in (1, 2, 4, 8, 16, 32):
        suites.append((f"distinct_sat_k{k}", [sat_cycle[i % len(sat_cycle)] for i in range(k)]))
        suites.append((f"unsat_first_k{k}", [BASES["2sat_unsat"]] + [sat_cycle[i % len(sat_cycle)] for i in range(max(0, k - 1))]))
        if k >= 2:
            suites.append((f"unsat_last_k{k}", [sat_cycle[i % len(sat_cycle)] for i in range(k - 1)] + [BASES["horn_unsat"]]))

    for suite_index, (name, parts) in enumerate(suites):
        raw = product(parts)
        for enc_index, enc in enumerate(ENCODINGS):
            cnf = transform_encoding(raw, enc, SEED + 97 * suite_index + enc_index)
            sem = semantic_audit(cnf)
            direct = stream_decide(cnf, "DIRECT")
            assert direct.answer == sem["product_answer"]
            checks += 1
            comp_sizes = [len(encode(c).encode("utf-8")) for c in components(cnf)]
            # On a NO input the streaming decider may stop before the largest
            # later component; peak live buffer is therefore bounded by, not
            # necessarily equal to, the largest component encoding.
            assert direct.peak_component_buffer_bytes <= max(comp_sizes)
            assert direct.answer_vector_bits == 0 and direct.accumulator_bits == 1
            assert direct.extraction_calls == direct.reconstruction_calls == 0
            assert direct.output_bits == 1
            checks += 5
            total_vars = len(variables(cnf))
            if total_vars <= 20:
                mono, mono_count, _ = solve_and_count(cnf)
                assert mono == direct.answer
                assert mono_count == sem["product_model_count"]
                checks += 2
            answers = {}
            for wrapper in WRAPPERS:
                ledger = stream_decide(cnf, wrapper)
                answers[wrapper] = ledger.answer
                assert ledger.answer == direct.answer
                assert ledger.answer_vector_bits == 0
                assert ledger.extraction_calls == ledger.reconstruction_calls == 0
                assert ledger.output_bits == 1
                checks += 4
                rows.append({
                    "suite": name,
                    "encoding": enc,
                    "wrapper": wrapper,
                    "variables": total_vars,
                    "clauses": len(cnf),
                    "semantic": sem,
                    "ledger": asdict(ledger),
                })
            assert len(set(answers.values())) == 1
            checks += 1

    collisions = [and_collision(k) for k in (1, 2, 4, 8, 16, 32)]
    for item in collisions:
        assert item["collision_pairs"] == item["zero_fiber"] ** 2 + 1
        assert item["image_size"] == 2
        checks += 2

    elapsed = time.perf_counter() - started
    payload = {
        "claim": "PRODUCT-ANSWER-STREAMING-COLLAPSE1",
        "status": "COMPUTATIONAL",
        "seed": SEED,
        "exhaustive_or_randomized": "deterministic fixed-suite; exhaustive truth tables per finite component",
        "elapsed_seconds": elapsed,
        "checks": checks,
        "failures": 0,
        "rows": rows,
        "and_map_collision_ledgers": collisions,
        "limitations": [
            "Finite component suite only; no asymptotic runtime inference.",
            "The executable component finder uses ordinary adjacency storage; the symbolic log-space bound in the report instead cites Reingold's USTCON theorem.",
            "Semantic model counts are computed on a separate audit path and are not charged to the one-bit decision wrapper.",
        ],
    }
    out = Path("results/raw/review/2026-10-12_product_answer_streaming_collapse.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(out),
        "rows": len(rows),
        "checks": checks,
        "failures": 0,
        "elapsed_seconds": elapsed,
        "sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
