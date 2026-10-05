#!/usr/bin/env python3
"""INTERMEDIATE1 exact-layer 3-SAT experiment.

Status: COMPUTATIONAL.

Samples exact distinct-clause random proper 3-CNF at density 3.5, classifies
with an exact DPLL solver, evaluates the monotone pair statistic
    T(F)=sum_i d_i^+(F)d_i^-(F),
and extracts one deterministic deletion-minimal UNSAT core for every UNSAT
sample.

The DPLL implementation is self-checked against brute-force truth tables on
500 small random instances before the main run.
"""

from __future__ import annotations

from itertools import combinations, product
from math import comb
import random
import statistics

Q_VALUES = (20, 24, 28, 32)
N = 5000
DENSITY = 3.5
THRESHOLD_OFFSET = 0.5
BASE_SEED = 5252
VALIDATION_SEED = 99173
Clause = tuple[int, int, int]


def gen_clause(q: int, rng: random.Random) -> Clause:
    vs = rng.sample(range(q), 3)
    lits = []
    for v in vs:
        lits.append((v + 1) if rng.getrandbits(1) else -(v + 1))
    return tuple(sorted(lits, key=abs))


def gen_formula(q: int, t: int, rng: random.Random) -> tuple[Clause, ...]:
    clauses: set[Clause] = set()
    while len(clauses) < t:
        clauses.add(gen_clause(q, rng))
    return tuple(sorted(clauses))


def simplify(
    clauses: tuple[tuple[int, ...], ...], var: int, val: bool
) -> tuple[tuple[int, ...], ...] | None:
    true_lit = var if val else -var
    false_lit = -true_lit
    out = []
    for clause in clauses:
        if true_lit in clause:
            continue
        if false_lit in clause:
            new_clause = tuple(lit for lit in clause if lit != false_lit)
            if not new_clause:
                return None
            out.append(new_clause)
        else:
            out.append(clause)
    return tuple(out)


def dpll_sat(clauses: tuple[tuple[int, ...], ...]) -> bool:
    def rec(cs: tuple[tuple[int, ...], ...]) -> bool:
        while True:
            if not cs:
                return True
            if any(len(c) == 0 for c in cs):
                return False
            unit = next((c[0] for c in cs if len(c) == 1), None)
            if unit is None:
                break
            cs = simplify(cs, abs(unit), unit > 0)
            if cs is None:
                return False

        polarity: dict[int, int] = {}
        for clause in cs:
            for lit in clause:
                v = abs(lit)
                polarity[v] = polarity.get(v, 0) | (1 if lit > 0 else 2)
        for v, mask in polarity.items():
            if mask in (1, 2):
                reduced = simplify(cs, v, mask == 1)
                return False if reduced is None else rec(reduced)

        shortest = min(cs, key=len)
        lit = shortest[0]
        v = abs(lit)
        first = simplify(cs, v, lit > 0)
        if first is not None and rec(first):
            return True
        second = simplify(cs, v, lit < 0)
        return second is not None and rec(second)

    return rec(tuple(clauses))


def brute_sat(formula: tuple[Clause, ...], q: int) -> bool:
    for assignment in range(1 << q):
        good = True
        for clause in formula:
            if not any(
                ((assignment >> (abs(lit) - 1)) & 1) == (1 if lit > 0 else 0)
                for lit in clause
            ):
                good = False
                break
        if good:
            return True
    return False


def t_stat(formula: tuple[Clause, ...], q: int) -> int:
    pos = [0] * q
    neg = [0] * q
    for clause in formula:
        for lit in clause:
            if lit > 0:
                pos[lit - 1] += 1
            else:
                neg[-lit - 1] += 1
    return sum(a * b for a, b in zip(pos, neg))


def uniform_t_expectation(q: int, t: int) -> float:
    M = 8 * comb(q, 3)
    L = 4 * comb(q - 1, 2)
    return q * L * L * t * (t - 1) / (M * (M - 1))


def greedy_deletion_mus(formula: tuple[Clause, ...]) -> tuple[Clause, ...]:
    core = list(formula)
    i = 0
    while i < len(core):
        test = tuple(core[:i] + core[i + 1 :])
        if not dpll_sat(test):
            core.pop(i)
        else:
            i += 1
    return tuple(core)


def core_variable_count(core: tuple[Clause, ...]) -> int:
    return len({abs(lit) for clause in core for lit in clause})


def validate_solver() -> int:
    rng = random.Random(VALIDATION_SEED)
    checks = 0
    for q in range(4, 9):
        max_clauses = 8 * comb(q, 3)
        for _ in range(100):
            t = rng.randint(1, min(4 * q, max_clauses))
            formula = gen_formula(q, t, rng)
            assert dpll_sat(formula) == brute_sat(formula, q)
            checks += 1
    return checks


def run_q(q: int) -> None:
    t = round(DENSITY * q)
    rng = random.Random(BASE_SEED + q)
    E0 = uniform_t_expectation(q, t)
    threshold = E0 + THRESHOLD_OFFSET * q

    sat_t: list[int] = []
    unsat_t: list[int] = []
    unsat_formulas: list[tuple[Clause, ...]] = []

    for _ in range(N):
        formula = gen_formula(q, t, rng)
        T = t_stat(formula, q)
        if dpll_sat(formula):
            sat_t.append(T)
        else:
            unsat_t.append(T)
            unsat_formulas.append(formula)

    tpr = sum(T >= threshold for T in unsat_t) / len(unsat_t)
    tnr = sum(T < threshold for T in sat_t) / len(sat_t)
    balanced = (tpr + tnr) / 2

    core_pairs = []
    for formula in unsat_formulas:
        core = greedy_deletion_mus(formula)
        core_pairs.append((len(core), core_variable_count(core)))

    clause_sizes = [x for x, _ in core_pairs]
    variable_sizes = [y for _, y in core_pairs]

    print(
        "PAIR",
        f"q={q}",
        f"t={t}",
        f"N={N}",
        f"unsat={len(unsat_t)}",
        f"unsat_rate={len(unsat_t)/N:.6f}",
        f"E0_per_q={E0/q:.12f}",
        f"sat_T_per_q={statistics.mean(sat_t)/q:.12f}",
        f"unsat_T_per_q={statistics.mean(unsat_t)/q:.12f}",
        f"TPR={tpr:.12f}",
        f"TNR={tnr:.12f}",
        f"balanced_accuracy={balanced:.12f}",
    )
    print(
        "CORE",
        f"q={q}",
        f"count={len(core_pairs)}",
        f"clause_mean={statistics.mean(clause_sizes):.12f}",
        f"clause_min={min(clause_sizes)}",
        f"clause_max={max(clause_sizes)}",
        f"var_mean={statistics.mean(variable_sizes):.12f}",
        f"var_min={min(variable_sizes)}",
        f"var_max={max(variable_sizes)}",
    )


def main() -> None:
    print("INTERMEDIATE1")
    print(f"validation_checks={validate_solver()}")
    print(f"density={DENSITY}")
    print(f"samples_per_q={N}")
    print(f"threshold=E0+{THRESHOLD_OFFSET}q")
    for q in Q_VALUES:
        run_q(q)
    print("STATUS=PASS")


if __name__ == "__main__":
    main()
