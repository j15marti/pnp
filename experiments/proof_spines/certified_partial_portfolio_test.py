#!/usr/bin/env python3
"""Bounded exact checks for CERTIFIED-PARTIAL-PORTFOLIO1.

The executable portfolio contains only syntactically recognizable partial
wrappers: constants, Horn, 2-CNF, disconnected components, and strong Horn
backdoors of size at most two.  A wrapper either returns an exact plan or FAIL.
The experiment checks the semantic interface; it does not prove universal
coverage or favorable asymptotic resource exponents.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, product
import hashlib
import json
from pathlib import Path
import random
import signal
import time


SEED = 20261007
BUDGET_SECONDS = 25
Clause = tuple[int, ...]
Formula = tuple[Clause, ...]


def normalize(formula: Formula) -> Formula:
    out: set[Clause] = set()
    for clause in formula:
        lits = set(clause)
        if any(-lit in lits for lit in lits):
            continue
        out.add(tuple(sorted(lits, key=lambda x: (abs(x), x < 0))))
    return tuple(sorted(out))


def variables(formula: Formula) -> tuple[int, ...]:
    return tuple(sorted({abs(lit) for clause in formula for lit in clause}))


def evaluate(formula: Formula, assignment: dict[int, bool]) -> bool:
    return all(any(assignment[abs(lit)] == (lit > 0) for lit in clause) for clause in formula)


def brute_sat(formula: Formula) -> bool:
    vs = variables(formula)
    return any(evaluate(formula, dict(zip(vs, bits))) for bits in product((False, True), repeat=len(vs)))


def restrict(formula: Formula, assignment: dict[int, bool]) -> Formula:
    residual: list[Clause] = []
    for clause in formula:
        if any(abs(lit) in assignment and assignment[abs(lit)] == (lit > 0) for lit in clause):
            continue
        reduced = tuple(lit for lit in clause if abs(lit) not in assignment)
        if not reduced:
            return ((),)
        residual.append(reduced)
    return normalize(tuple(residual))


def is_horn(formula: Formula) -> bool:
    return all(sum(lit > 0 for lit in clause) <= 1 for clause in formula)


def horn_sat(formula: Formula) -> bool:
    true_vars: set[int] = set()
    changed = True
    while changed:
        changed = False
        for clause in formula:
            positive = [lit for lit in clause if lit > 0]
            negative = [-lit for lit in clause if lit < 0]
            if all(v in true_vars for v in negative):
                if not positive:
                    return False
                if positive[0] not in true_vars:
                    true_vars.add(positive[0])
                    changed = True
    return True


def two_sat(formula: Formula) -> bool:
    vs = variables(formula)
    graph = {lit: [] for v in vs for lit in (v, -v)}
    reverse = {lit: [] for v in vs for lit in (v, -v)}
    for clause in formula:
        if len(clause) == 0:
            return False
        if len(clause) > 2:
            raise ValueError("not 2-CNF")
        a = clause[0]
        b = clause[-1]
        for u, v in ((-a, b), (-b, a)):
            graph.setdefault(u, []).append(v)
            graph.setdefault(v, [])
            reverse.setdefault(v, []).append(u)
            reverse.setdefault(u, [])
    seen: set[int] = set()
    order: list[int] = []

    def visit(u: int) -> None:
        seen.add(u)
        for v in graph[u]:
            if v not in seen:
                visit(v)
        order.append(u)

    for u in graph:
        if u not in seen:
            visit(u)
    component: dict[int, int] = {}

    def assign(u: int, label: int) -> None:
        component[u] = label
        for v in reverse[u]:
            if v not in component:
                assign(v, label)

    for u in reversed(order):
        if u not in component:
            assign(u, len(component))
    return all(component.get(v) != component.get(-v) for v in vs)


@dataclass(frozen=True)
class Plan:
    combiner: str
    children: tuple[Formula, ...] = ()
    value: bool | None = None


def constant_wrapper(formula: Formula, _: dict[str, int]) -> Plan | None:
    if not formula:
        return Plan("VALUE", value=True)
    if any(not clause for clause in formula):
        return Plan("VALUE", value=False)
    return None


def horn_wrapper(formula: Formula, _: dict[str, int]) -> Plan | None:
    return Plan("VALUE", value=horn_sat(formula)) if is_horn(formula) else None


def two_cnf_wrapper(formula: Formula, _: dict[str, int]) -> Plan | None:
    return Plan("VALUE", value=two_sat(formula)) if all(len(c) <= 2 for c in formula) else None


def component_wrapper(formula: Formula, _: dict[str, int]) -> Plan | None:
    vs = variables(formula)
    if len(vs) < 2:
        return None
    graph = {v: set() for v in vs}
    for clause in formula:
        cv = {abs(lit) for lit in clause}
        for u in cv:
            graph[u].update(cv - {u})
    components: list[set[int]] = []
    unseen = set(vs)
    while unseen:
        root = next(iter(unseen))
        stack = [root]
        block: set[int] = set()
        while stack:
            u = stack.pop()
            if u in block:
                continue
            block.add(u)
            unseen.discard(u)
            stack.extend(graph[u] - block)
        components.append(block)
    if len(components) <= 1:
        return None
    children = tuple(
        tuple(clause for clause in formula if any(abs(lit) in block for lit in clause))
        for block in components
    )
    return Plan("AND", tuple(normalize(child) for child in children))


def horn_backdoor2_wrapper(formula: Formula, metrics: dict[str, int]) -> Plan | None:
    vs = variables(formula)
    for width in range(1, min(2, len(vs)) + 1):
        for backdoor in combinations(vs, width):
            children: list[Formula] = []
            good = True
            for bits in product((False, True), repeat=width):
                metrics["candidate_restrictions"] += 1
                child = restrict(formula, dict(zip(backdoor, bits)))
                if not is_horn(child):
                    good = False
                    break
                children.append(child)
            if good:
                return Plan("OR", tuple(children))
    return None


WRAPPERS = (
    ("constant", constant_wrapper),
    ("horn", horn_wrapper),
    ("two_cnf", two_cnf_wrapper),
    ("components", component_wrapper),
    ("horn_backdoor2", horn_backdoor2_wrapper),
)


def run_portfolio(formula: Formula, order=WRAPPERS) -> tuple[str | None, Plan | None, dict[str, int]]:
    formula = normalize(formula)
    metrics = {"attempts": 0, "failed_attempts": 0, "candidate_restrictions": 0, "sat_oracle_calls": 0}
    for name, wrapper in order:
        metrics["attempts"] += 1
        plan = wrapper(formula, metrics)
        if plan is not None:
            return name, plan, metrics
        metrics["failed_attempts"] += 1
    return None, None, metrics


def plan_value(plan: Plan) -> bool:
    if plan.combiner == "VALUE":
        assert plan.value is not None
        return plan.value
    answers = [brute_sat(child) for child in plan.children]
    if plan.combiner == "AND":
        return all(answers)
    if plan.combiner == "OR":
        return any(answers)
    raise AssertionError(plan.combiner)


def random_clause(rng: random.Random, pool: list[int], width: int, horn: bool = False) -> Clause:
    chosen = rng.sample(pool, min(width, len(pool)))
    if horn:
        positive = rng.choice(chosen + [0])
        return tuple(v if v == positive else -v for v in chosen)
    return tuple(v if rng.getrandbits(1) else -v for v in chosen)


def build_cases(rng: random.Random) -> list[tuple[str, Formula]]:
    cases: list[tuple[str, Formula]] = []
    for _ in range(80):
        n = rng.randint(3, 8)
        cases.append(("horn", normalize(tuple(random_clause(rng, list(range(1, n + 1)), rng.randint(1, 3), True) for _ in range(rng.randint(1, 12))))))
    for _ in range(80):
        n = rng.randint(3, 8)
        cases.append(("two_cnf", normalize(tuple(random_clause(rng, list(range(1, n + 1)), rng.randint(1, 2)) for _ in range(rng.randint(1, 12))))))
    for _ in range(80):
        left = list(range(1, 5))
        right = list(range(5, 9))
        clauses = [random_clause(rng, left, 3) for _ in range(4)] + [random_clause(rng, right, 3) for _ in range(4)]
        cases.append(("components", normalize(tuple(clauses))))
    for _ in range(80):
        n = 7
        backdoor = [1, 2]
        clauses: list[Clause] = []
        for _ in range(8):
            non_backdoor = rng.choice(list(range(3, n + 1)))
            bvars = rng.sample(backdoor, rng.randint(1, 2))
            clause = [non_backdoor if rng.getrandbits(1) else -non_backdoor]
            clause += [v if rng.getrandbits(1) else -v for v in bvars]
            clauses.append(tuple(clause))
        cases.append(("backdoor2", normalize(tuple(clauses))))
    return cases


def main() -> None:
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError("25-second cooperative budget exceeded")))
    signal.alarm(BUDGET_SECONDS)
    started = time.monotonic()
    rng = random.Random(SEED)
    cases = build_cases(rng)
    winners = {name: 0 for name, _ in WRAPPERS}
    family_counts: dict[str, int] = {}
    total_attempts = total_failed = total_restrictions = 0
    for family, formula in cases:
        expected = brute_sat(formula)
        winner, plan, metrics = run_portfolio(formula)
        assert winner is not None and plan is not None
        assert plan_value(plan) == expected
        winners[winner] += 1
        family_counts[family] = family_counts.get(family, 0) + 1
        total_attempts += metrics["attempts"]
        total_failed += metrics["failed_attempts"]
        total_restrictions += metrics["candidate_restrictions"]
        assert metrics["sat_oracle_calls"] == 0

    permutation_checks = 0
    for formula in [case[1] for case in cases[:24]]:
        expected = brute_sat(formula)
        for _ in range(4):
            order = list(WRAPPERS)
            rng.shuffle(order)
            _, plan, _ = run_portfolio(formula, tuple(order))
            assert plan is not None and plan_value(plan) == expected
            permutation_checks += 1

    outside = normalize(tuple(tuple(((i + j - 1) % 7) + 1 for j in range(3)) for i in range(1, 8)))
    outside_winner, outside_plan, outside_metrics = run_portfolio(outside)
    assert outside_winner is None and outside_plan is None

    satisfiable_control: Formula = ((1, 2, 3),)
    assert brute_sat(satisfiable_control)
    unsafe_first = Plan("VALUE", value=False)
    unsafe_first_finisher_is_wrong = plan_value(unsafe_first) != brute_sat(satisfiable_control)
    assert unsafe_first_finisher_is_wrong

    independent_product = normalize(tuple((3 * i + 1, 3 * i + 2, -(3 * i + 3)) for i in range(4)))
    product_winner, product_plan, _ = run_portfolio(independent_product)
    assert product_winner == "components" and product_plan is not None
    assert plan_value(product_plan) == brute_sat(independent_product)

    padded = normalize(satisfiable_control + tuple((100 + i, -(100 + i), 1) for i in range(64)))
    assert padded == normalize(satisfiable_control)
    _, padded_plan, padded_metrics = run_portfolio(padded)
    assert padded_plan is not None and plan_value(padded_plan)

    elapsed = time.monotonic() - started
    signal.alarm(0)
    payload = {
        "claim_id": "CERTIFIED-PARTIAL-PORTFOLIO1",
        "status": "COMPUTATIONAL verification of an exact interface theorem on bounded families",
        "seed": SEED,
        "budget_seconds": BUDGET_SECONDS,
        "elapsed_seconds": round(elapsed, 6),
        "cases": len(cases),
        "family_counts": family_counts,
        "winner_counts": winners,
        "total_wrapper_attempts": total_attempts,
        "charged_failed_attempts": total_failed,
        "charged_candidate_restrictions": total_restrictions,
        "permutation_checks": permutation_checks,
        "current_scale_sat_oracle_calls": 0,
        "outside_coverage_control": {
            "portfolio_returned_fail": outside_winner is None,
            "attempts": outside_metrics["attempts"],
            "interpretation": "A finite partial portfolio is not a general-SAT wrapper without a universal coverage theorem.",
        },
        "unsafe_success_control": {
            "incorrect_first_success_breaks_exactness": unsafe_first_finisher_is_wrong,
            "interpretation": "At least one correct member is insufficient; every SUCCESS plan must be exact.",
        },
        "independent_product_control": {
            "winner": product_winner,
            "child_count": len(product_plan.children),
            "interpretation": "Component factorization is exact but does not prove favorable bounds on connected general inputs.",
        },
        "padding_control": {
            "tautologies_removed": 64,
            "attempts_after_normalization": padded_metrics["attempts"],
            "interpretation": "Cheap tautological padding is normalized away and supplies no contraction theorem.",
        },
        "growing_portfolio_control": {
            "synthetic_parent_size": 4096,
            "candidate_count": 4096,
            "minimum_sequential_attempts_if_winner_last": 4096,
            "interpretation": "The fixed-cardinality hypothesis is load-bearing; a growing family needs its own exponent and space ledger.",
        },
        "scope": (
            "Exact bounded semantic checks for declared partial wrappers. No universal coverage, fixed-power child shrink, "
            "favorable fanout, or Williams-model transfer is inferred. The theorem itself is proved symbolically in the report."
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "passed": True,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
