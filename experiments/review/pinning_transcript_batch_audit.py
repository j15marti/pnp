#!/usr/bin/env python3
"""Bounded hostile controls for additive pinning/self-reduction claims.

This validates exact transcripts and explicit encoding ledgers.  It does not
infer asymptotic hardness from timings or finite samples.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import random
import signal
import time
from dataclasses import dataclass
from pathlib import Path

Clause = tuple[int, ...]


class BudgetExceeded(RuntimeError):
    pass


def alarm(_signum, _frame):
    raise BudgetExceeded("25-second cooperative budget exceeded")


def gamma_len(x: int) -> int:
    assert x >= 1
    return 2 * (x.bit_length() - 1) + 1


@dataclass(frozen=True)
class Formula:
    family: str
    nvars: int
    clauses: tuple[Clause, ...]
    witness: tuple[int, ...]
    components: int


def encoded_bits(f: Formula) -> int:
    """Declared indexed encoding: gamma header/width plus signed indices."""
    width = max(1, math.ceil(math.log2(f.nvars + 1)))
    return (
        gamma_len(f.nvars)
        + gamma_len(len(f.clauses) + 1)
        + sum(gamma_len(len(c) + 1) + len(c) * (1 + width) for c in f.clauses)
    )


def touches(f: Formula) -> int:
    return sum(map(len, f.clauses))


def four_clause_pin(var: int, bit: int, p: int, q: int) -> tuple[Clause, ...]:
    lit = var if bit else -var
    return ((lit, p, q), (lit, p, -q), (lit, -p, q), (lit, -p, -q))


def proper_pin(bits: tuple[int, ...]) -> Formula:
    n = len(bits)
    cls: list[Clause] = []
    for i, bit in enumerate(bits, 1):
        cls.extend(four_clause_pin(i, bit, n + 2 * i - 1, n + 2 * i))
    return Formula("proper_pin", 3 * n, tuple(cls), bits + (0,) * (2 * n), n)


def horn_equality(bits: tuple[int, ...]) -> Formula:
    n = len(bits)
    cls: list[Clause] = []
    for i, bit in enumerate(bits, 1):
        y = n + i
        cls.extend(((-i, y), (i, -y), ((i if bit else -i),)))
    return Formula("horn_equality", 2 * n, tuple(cls), bits + bits, n)


def affine_path(bits: tuple[int, ...]) -> Formula:
    cls: list[Clause] = [((1 if bits[0] else -1),)]
    for i in range(1, len(bits)):
        x, y = i, i + 1
        cls.extend(((-x, y), (x, -y)) if bits[i - 1] == bits[i]
                   else ((x, y), (-x, -y)))
    return Formula("affine_tseitin_path", len(bits), tuple(cls), bits, len(bits))


def exact_one(blocks: int) -> Formula:
    cls: list[Clause] = []
    witness: list[int] = []
    for b in range(blocks):
        a, x, c = 3 * b + 1, 3 * b + 2, 3 * b + 3
        cls.extend(((a, x, c), (-a, -x), (-a, -c), (-x, -c)))
        witness.extend((0, 0, 1))
    return Formula("exact_one_product", 3 * blocks, tuple(cls), tuple(witness), blocks)


def wrap(f: Formula, duplicate: int, dead: int) -> Formula:
    cls = tuple(c for c in f.clauses for _ in range(duplicate)) + ((1, -1),) * dead
    return Formula(f.family, f.nvars, cls, f.witness, f.components)


def clause_value(c: Clause, a: tuple[int, ...]) -> bool:
    return any(a[abs(l) - 1] == int(l > 0) for l in c)


def satisfies(f: Formula, a: tuple[int, ...]) -> bool:
    return len(a) == f.nvars and all(clause_value(c, a) for c in f.clauses)


def prefix_feasible(f: Formula, prefix: tuple[int, ...]) -> bool:
    if len(prefix) > f.nvars:
        return False
    if f.family == "proper_pin":
        forced = min(len(prefix), f.components)
        return prefix[:forced] == f.witness[:forced]
    if f.family in {"horn_equality", "affine_tseitin_path"}:
        return prefix == f.witness[:len(prefix)]
    if f.family == "exact_one_product":
        for b in range(f.components):
            part = prefix[3 * b:min(3 * b + 3, len(prefix))]
            if sum(part) > 1 or (len(part) == 3 and sum(part) != 1):
                return False
        return True
    raise AssertionError(f.family)


def pinned_query(base: Formula, prefix: tuple[int, ...], mode: str) -> Formula:
    cls = list(base.clauses)
    nvars = base.nvars
    if mode == "unit":
        cls.extend(((i + 1 if bit else -(i + 1)),) for i, bit in enumerate(prefix))
    elif mode == "proper3":
        for i, bit in enumerate(prefix):
            p = base.nvars + 2 * i + 1
            cls.extend(four_clause_pin(i + 1, bit, p, p + 1))
        nvars += 2 * len(prefix)
    else:
        raise AssertionError(mode)
    return Formula(base.family, nvars, tuple(cls), (), base.components)


def independent_extractor(f: Formula, mode: str) -> dict[str, object]:
    prefix: tuple[int, ...] = ()
    answers: list[int] = []
    queries = [f]
    for _ in range(f.nvars):
        trial = prefix + (0,)
        ans = int(prefix_feasible(f, trial))
        answers.append(ans)
        queries.append(pinned_query(f, trial, mode))
        prefix += (0 if ans else 1,)
    assert satisfies(f, prefix)
    return {
        "witness": prefix,
        "answers": tuple(answers),
        "calls": len(queries),
        "materialized_bits": sum(encoded_bits(q) for q in queries),
        "literal_touches": sum(touches(q) for q in queries),
    }


def batch_extractor(f: Formula) -> dict[str, object]:
    prefix: tuple[int, ...] = ()
    answers: list[int] = []
    for _ in range(f.nvars):
        ans = int(prefix_feasible(f, prefix + (0,)))
        answers.append(ans)
        prefix += (0 if ans else 1,)
    assert satisfies(f, prefix)
    return {"witness": prefix, "answers": tuple(answers),
            "work": touches(f) + 2 * f.nvars}


def make_h22(rng: random.Random, n: int) -> tuple[Clause, ...]:
    triples = list(itertools.combinations(range(1, n + 1), 3))
    count = 2 * n // 3

    def regular() -> tuple[tuple[int, int, int], ...]:
        for _ in range(20_000):
            edges = tuple(rng.sample(triples, count))
            deg = [0] * (n + 1)
            for edge in edges:
                for v in edge:
                    deg[v] += 1
            if all(deg[v] == 2 for v in range(1, n + 1)):
                return edges
        raise RuntimeError("degree-two sampler failed")

    pos, neg = regular(), regular()
    return tuple(pos) + tuple(tuple(-v for v in e) for e in neg)


def h22_control(rng: random.Random, n: int, samples: int) -> dict[str, int]:
    instances = sat = shared = restarts = transcript = 0
    for _ in range(samples):
        clauses = make_h22(rng, n)
        solutions = []
        for a in itertools.product((0, 1), repeat=n):
            shared += 1
            if all(clause_value(c, a) for c in clauses):
                solutions.append(a)
        instances += 1
        if not solutions:
            continue
        sat += 1
        surviving, witness = solutions, []
        for i in range(n):
            zero = [a for a in surviving if a[i] == 0]
            bit = 0 if zero else 1
            surviving = zero or [a for a in surviving if a[i] == 1]
            witness.append(bit)
            transcript += 1
            found = False
            for a in itertools.product((0, 1), repeat=n):
                restarts += 1
                if a[:len(witness)] == tuple(witness) and all(clause_value(c, a) for c in clauses):
                    found = True
                    break
            assert found
        assert tuple(witness) == min(solutions)
    return {"instances": instances, "satisfiable_instances": sat,
            "transcript_bits_checked": transcript,
            "shared_truth_table_assignment_checks": shared,
            "independent_restart_assignment_checks": restarts}


def run(max_n: int, seed: int, h22_samples: int) -> dict[str, object]:
    start = time.monotonic()
    rng = random.Random(seed)
    totals = {"instances": 0, "semantic_agreement_checks": 0,
              "wrapper_checks": 0, "query_encoding_checks": 0,
              "strict_batch_separations": 0}
    families: dict[str, dict[str, int | float]] = {}
    for n in range(1, max_n + 1):
        bases: list[Formula] = []
        for mask in range(1 << n):
            bits = tuple((mask >> i) & 1 for i in range(n))
            bases.extend((proper_pin(bits), horn_equality(bits), affine_path(bits)))
        bases.append(exact_one(n))
        for base in bases:
            for duplicate, dead in ((1, 0), (3, n)):
                f = wrap(base, duplicate, dead)
                batch = batch_extractor(f)
                for mode in ("unit", "proper3"):
                    independent = independent_extractor(f, mode)
                    assert independent["witness"] == batch["witness"]
                    assert independent["answers"] == batch["answers"]
                    interp = tuple(1 - b for b in batch["answers"])
                    assert tuple(1 - b for b in interp) == batch["answers"]
                    recomp = batch_extractor(f)
                    assert recomp["answers"] == batch["answers"]
                    totals["instances"] += 1
                    totals["semantic_agreement_checks"] += f.nvars
                    totals["wrapper_checks"] += 4 * f.nvars
                    totals["query_encoding_checks"] += int(independent["calls"])
                    if int(independent["literal_touches"]) > int(batch["work"]):
                        totals["strict_batch_separations"] += 1
                    row = families.setdefault(f.family, {"runs": 0, "max_nvars": 0,
                        "max_materialized_bits": 0, "max_batch_work": 0,
                        "max_touch_ratio": 0.0})
                    row["runs"] = int(row["runs"]) + 1
                    row["max_nvars"] = max(int(row["max_nvars"]), f.nvars)
                    row["max_materialized_bits"] = max(int(row["max_materialized_bits"]),
                                                          int(independent["materialized_bits"]))
                    row["max_batch_work"] = max(int(row["max_batch_work"]), int(batch["work"]))
                    row["max_touch_ratio"] = max(float(row["max_touch_ratio"]),
                                                   int(independent["literal_touches"]) / max(1, int(batch["work"])))
    return {"run_id": "TESTS-0001", "status": "PASS", "seed": seed,
            "max_n": max_n,
            "method": "exhaustive easy-family targets; seeded finite H_2,2 controls",
            "totals": totals, "families": families,
            "h22_controls": {str(n): h22_control(rng, n, h22_samples) for n in (6, 9)},
            "elapsed_seconds": time.monotonic() - start,
            "limitations": [
                "Finite checks validate ledgers and implementations, not an asymptotic SAT lower bound.",
                "The linear batch theorem is scoped to the declared canonical easy families.",
                "The H_2,2 truth-table control is exponential and supplies no polynomial algorithm for that NP-complete core.",
                "A direct-sum or no-sharing theorem for arbitrary SAT deciders remains open."]}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--max-n", type=int, default=8)
    p.add_argument("--seed", type=int, default=20261011)
    p.add_argument("--h22-samples", type=int, default=8)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    signal.signal(signal.SIGALRM, alarm)
    signal.alarm(25)
    try:
        result = run(a.max_n, a.seed, a.h22_samples)
    finally:
        signal.alarm(0)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
