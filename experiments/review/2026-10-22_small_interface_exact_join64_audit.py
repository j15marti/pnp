#!/usr/bin/env python3
"""Finite audit for SMALL-INTERFACE-EXACT-JOIN64.

The theorem is symbolic.  This audit checks exact parent/join agreement,
restriction heredity, the omitted-source hostile control, and the exponent
ledger on deterministic small fixtures.
"""

from __future__ import annotations

import itertools
import json
import math
import random


def clause_value(clause, a):
    return any(a[abs(lit)] == (lit > 0) for lit in clause)


def sat(formula, variables, fixed=None):
    fixed = dict(fixed or {})
    free = sorted(set(variables) - set(fixed))
    for bits in itertools.product((False, True), repeat=len(free)):
        a = dict(fixed)
        a.update(zip(free, bits))
        if all(clause_value(c, a) for c in formula):
            return True
    return False


def restrict_formula(formula, fixed):
    out = []
    for clause in formula:
        reduced = []
        satisfied = False
        for lit in clause:
            v = abs(lit)
            if v not in fixed:
                reduced.append(lit)
            elif fixed[v] == (lit > 0):
                satisfied = True
                break
        if not satisfied:
            out.append(tuple(reduced))
    return out


def join_sat(blocks, separator, all_variables):
    internal = [set(abs(lit) for c in block for lit in c) - set(separator)
                for block in blocks]
    for i in range(len(internal)):
        for j in range(i):
            assert not (internal[i] & internal[j])
    for bits in itertools.product((False, True), repeat=len(separator)):
        fixed = dict(zip(separator, bits))
        if all(sat(block, all_variables, fixed) for block in blocks):
            return True
    return False


def make_fixture(seed, blocks_count, separator_size, internal_per_block):
    rng = random.Random(seed)
    separator = list(range(1, separator_size + 1))
    next_var = separator_size + 1
    blocks = []
    for _ in range(blocks_count):
        internal = list(range(next_var, next_var + internal_per_block))
        next_var += internal_per_block
        available = separator + internal
        block = []
        for _ in range(1 + internal_per_block):
            width = min(3, len(available))
            vars_ = rng.sample(available, width)
            block.append(tuple(v if rng.getrandbits(1) else -v for v in vars_))
        blocks.append(block)
    return blocks, separator, set(range(1, next_var))


def main():
    checks = 0
    fixtures = 0
    restrictions = 0
    for blocks_count in (2, 3, 4):
        for separator_size in (0, 1, 2):
            for seed in range(40):
                blocks, separator, variables = make_fixture(
                    10000 * blocks_count + 100 * separator_size + seed,
                    blocks_count, separator_size, 2)
                formula = [c for block in blocks for c in block]
                assert sat(formula, variables) == join_sat(
                    blocks, separator, variables)
                checks += 1
                fixtures += 1

                # Partial assignments preserve conditional block separation.
                for v in sorted(variables)[:min(3, len(variables))]:
                    for bit in (False, True):
                        fixed = {v: bit}
                        rblocks = [restrict_formula(block, fixed) for block in blocks]
                        rsep = [x for x in separator if x != v]
                        rformula = [c for block in rblocks for c in block]
                        assert sat(rformula, variables, fixed) == join_sat(
                            rblocks, rsep, variables)
                        checks += 1
                        restrictions += 1

    # Hostile control: z is a hidden cross-block source.  Omitting it from the
    # separator makes both blocks SAT while their conjunction is UNSAT.
    hidden_blocks = [[(1,)], [(-1,)]]
    assert sat([(1,), (-1,)], {1}) is False
    assert all(sat(block, {1}) for block in hidden_blocks)
    assert join_sat(hidden_blocks, [1], {1}) is False
    checks += 3

    # Exact exponent ledger for powers of two.  Floors make the inequalities
    # literal rather than asymptotic.
    ledger = []
    for e in range(20, 101, 5):
        N = 2 ** e
        J = 2 ** (e // 2)
        k = e // 10
        L = 2 ** (e // 2)
        Q = J * (2 ** k)
        log2_j = e // 2
        log2_q = log2_j + k
        log2_output = log2_q + e // 2
        assert 2 * log2_j <= e
        assert 10 * log2_q <= 6 * e
        assert 10 * log2_output <= 11 * e
        checks += 3
        ledger.append({"log2_N": e, "J": J, "k": k,
                       "log2_Q": log2_q,
                       "log2_output": log2_output})

    print(json.dumps({
        "status": "finite_audit_only_no_class_separation",
        "fixtures": fixtures,
        "restriction_tests": restrictions,
        "checks": checks,
        "failures": 0,
        "hostile_control": "(z) and (!z) false-joins if z is omitted from S",
        "ledger_samples": ledger,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
