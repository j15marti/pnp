#!/usr/bin/env python3
"""Independent bounded audit of the CONSTRUCTION-STRENGTHEN5 embedding.

This test authenticates the existing executable portfolio locally, adds the
proposed unit/pure prefix, and exhaustively checks the smallest nontrivial
source universe (all proper clauses on three densely occurring variables).
It deliberately does not treat finite testing as a complexity lower bound.
"""
from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import signal
import sys
import time

BUDGET = 25
signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError("25s")))
signal.alarm(BUDGET)
started = time.monotonic()

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[2] / "experiments/proof_spines/certified_partial_portfolio_test.py"
ARC2_SCANNER_SOURCE = HERE / "2026-10-08_2110_ARC-STRENGTHEN2-test.py"
spec = importlib.util.spec_from_file_location("authenticated_portfolio", SOURCE)
portfolio = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = portfolio
assert spec.loader is not None
spec.loader.exec_module(portfolio)


def parity0(x: int, y: int, z: int):
    """Four clauses accepting exactly x xor y xor z == 0."""
    ans = []
    for bits in itertools.product((0, 1), repeat=3):
        if sum(bits) % 2 == 1:
            ans.append(tuple(-v if bit else v for v, bit in zip((x, y, z), bits)))
    return tuple(ans)


def embed(source, n: int, extra_guards: bool = True):
    h, r = n + 1, n + 2
    out = list(source)
    out.extend(((h, -r), (-h, r)))
    next_var = n + 3
    if extra_guards:
        out.extend(parity0(h, next_var, next_var + 1))
        out.extend(parity0(h, next_var + 2, next_var + 3))
        next_var += 4
    for v in range(1, n + 1):
        out.extend(parity0(h, v, next_var))
        next_var += 1
    return portfolio.normalize(tuple(out))


def simplify_units_pures(formula):
    """Decision-preserving exhaustive prefix, with each rescan explicit."""
    cur = portfolio.normalize(formula)
    assignments = {}
    rescans = 0
    while True:
        rescans += 1
        if any(len(c) == 0 for c in cur):
            return cur, assignments, rescans
        unit = next((c[0] for c in cur if len(c) == 1), None)
        if unit is not None:
            v, value = abs(unit), unit > 0
            if v in assignments and assignments[v] != value:
                return ((),), assignments, rescans
            assignments[v] = value
            cur = portfolio.restrict(cur, {v: value})
            continue
        signs = {}
        for clause in cur:
            for lit in clause:
                signs.setdefault(abs(lit), set()).add(lit > 0)
        pure = next(((v, next(iter(ss))) for v, ss in signs.items() if len(ss) == 1), None)
        if pure is not None:
            v, value = pure
            assignments[v] = value
            cur = portfolio.restrict(cur, {v: value})
            continue
        return cur, assignments, rescans


def scanner_rejects(formula):
    # The authenticated ARC2 scanner starts with this exact width/distinctness guard.
    return any(len(c) != 3 or len(set(map(abs, c))) != 3 for c in formula)


def eval_int(formula, mask):
    return all(any(bool(mask & (1 << (abs(lit) - 1))) == (lit > 0) for lit in c) for c in formula)


def brute_int(formula):
    vs = portfolio.variables(formula)
    assert not vs or vs == tuple(range(1, max(vs) + 1))
    return any(eval_int(formula, mask) for mask in range(1 << len(vs)))


def min_strong_horn_backdoor(formula, cap=3):
    vs = portfolio.variables(formula)
    for width in range(cap + 1):
        for backdoor in itertools.combinations(vs, width):
            if all(
                portfolio.is_horn(portfolio.restrict(formula, dict(zip(backdoor, bits))))
                for bits in itertools.product((False, True), repeat=width)
            ):
                return width, backdoor
    return None, None


all_clauses = tuple(
    tuple(v if bit else -v for v, bit in zip((1, 2, 3), bits))
    for bits in itertools.product((0, 1), repeat=3)
)
semantic_checks = 0
dense_sources = 0
portfolio_checks = 0
prefix_checks = 0

for subset in range(1, 1 << len(all_clauses)):
    source = tuple(all_clauses[j] for j in range(8) if subset >> j & 1)
    if portfolio.variables(source) != (1, 2, 3):
        continue
    dense_sources += 1
    source_truth = brute_int(source)
    for guards in (False, True):
        target = embed(source, 3, guards)
        assert brute_int(target) == source_truth
        semantic_checks += 1
        reduced, chosen, rescans = simplify_units_pures(target)
        assert reduced == target and chosen == {} and rescans == 1
        prefix_checks += 1
        assert scanner_rejects(target)

# Exact portfolio and operational empty-clause semantics on representative
# satisfiable and unsatisfiable sources, for both stated and tightened forms.
representatives = (
    ((1, 2, 3),),
    all_clauses,
)
backdoor_rows = []
for source in representatives:
    for guards in (False, True):
        target = embed(source, 3, guards)
        winner, plan, metrics = portfolio.run_portfolio(target)
        assert winner is None and plan is None
        portfolio_checks += 1
        width, witness = min_strong_horn_backdoor(target, 2)
        assert width is None, (guards, width, witness)
        backdoor_rows.append({
            "extra_guards": guards,
            "source_clauses": len(source),
            "certified_strong_horn_backdoor_lower_bound": 3,
            "witness_at_most_two": witness,
            "old_candidate_restrictions": metrics["candidate_restrictions"],
        })

# Verify the special B={h,r}, h=r=1 branch does not trigger the portfolio's
# absorbing-empty-clause shortcut and leaves a positive binary clause.
for guards in (False, True):
    target = embed(((1, 2, 3),), 3, guards)
    h, r = 4, 5
    residual = portfolio.restrict(target, {h: True, r: True})
    assert residual != ((),)
    assert any(len(c) == 2 and sum(lit > 0 for lit in c) == 2 for c in residual)

signal.alarm(0)
result = {
    "status": "COMPUTATIONAL",
    "passed": True,
    "dense_three_variable_sources": dense_sources,
    "semantic_equivalence_checks": semantic_checks,
    "unit_pure_fixed_point_checks": prefix_checks,
    "exact_old_portfolio_failures_checked": portfolio_checks,
    "backdoor_rows": backdoor_rows,
    "seconds": time.monotonic() - started,
    "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "authenticated_portfolio_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    "authenticated_arc2_scanner_test_sha256": hashlib.sha256(ARC2_SCANNER_SOURCE.read_bytes()).hexdigest(),
    "conclusions": [
        "No counterexample was found in the complete n=3 source universe.",
        "The two extra guard parity blocks are redundant for dense proper width-3 sources.",
        "The local-access statement needs an explicit fixed-field encoding with n and m in the header.",
        "This is an NP-hardness-preserving embedding into the portfolio failure set, not a lower bound and not an all-input favorable wrapper.",
    ],
}
print(json.dumps(result, indent=2))
