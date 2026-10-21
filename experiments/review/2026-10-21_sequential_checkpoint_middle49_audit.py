#!/usr/bin/env python3
"""Finite controls for SEQUENTIAL-CHECKPOINT-MIDDLE49.

This checks the checkpoint/replay arithmetic and several exact toy generators.
It does not estimate arbitrary KT and does not address either open separation.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction


checks = 0


def require(condition: bool, message: str) -> None:
    global checks
    checks += 1
    if not condition:
        raise AssertionError(message)


def transition(state: int, width: int) -> int:
    mask = (1 << width) - 1
    return ((5 * state + 1) ^ (state >> 1)) & mask


def sequential_bits(seed: int, width: int, length: int) -> list[int]:
    state = seed
    out = []
    for _ in range(length):
        state = transition(state, width)
        out.append((state >> (width - 1)) & 1)
    return out


def checkpoints(seed: int, width: int, length: int, block: int) -> list[int]:
    state = seed
    saved = [state]
    for position in range(1, length + 1):
        state = transition(state, width)
        if position % block == 0 and position < length:
            saved.append(state)
    return saved


def checkpoint_bit(saved: list[int], width: int, block: int, index: int) -> int:
    state = saved[index // block]
    for _ in range(index % block + 1):
        state = transition(state, width)
    return (state >> (width - 1)) & 1


def source_transition(state: int, bit: int, width: int) -> int:
    mask = (1 << width) - 1
    return (((state << 1) | (state >> (width - 1))) ^ bit) & mask


def source_bits(source: list[int], width: int) -> list[int]:
    state = 0
    out = []
    for bit in source:
        state = source_transition(state, bit, width)
        out.append(state & 1)
    return out


# 1. Integer checkpoint ledger and AM-GM lower bound.
ledger_cases = 0
for length in range(2, 257):
    for state_bits in range(1, 17):
        for step_time in range(1, 17):
            values = []
            for block in range(1, length + 1):
                cost = math.ceil(length / block) * state_bits + block * step_time
                values.append(cost)
                require(cost * cost >= 4 * length * state_bits * step_time,
                        "integer checkpoint cost violated AM-GM")
                ledger_cases += 1
            optimum = min(values)
            root = math.sqrt(length * state_bits / step_time)
            balanced_block = max(1, min(length, math.ceil(root)))
            balanced_cost = (math.ceil(length / balanced_block) * state_bits
                             + balanced_block * step_time)
            require(optimum <= balanced_cost, "brute optimum exceeds balanced choice")
            require(balanced_cost <= 2 * math.sqrt(length * state_bits * step_time)
                    + state_bits + step_time + 1e-9,
                    "balanced checkpoint upper envelope failed")


# 2. Checkpoint replay reconstructs every target bit for a nonlinear toy stream.
replay_cases = 0
for width in range(2, 11):
    for length in (1, 2, 3, 7, 16, 31, 64, 127):
        for seed in (0, 1, (1 << width) - 1, (3 * width + 1) & ((1 << width) - 1)):
            truth = sequential_bits(seed, width, length)
            for block in sorted({1, 2, 3, 5, length, max(1, int(math.sqrt(length)))}):
                saved = checkpoints(seed, width, length, block)
                recovered = [checkpoint_bit(saved, width, block, i)
                             for i in range(length)]
                require(recovered == truth, "checkpoint replay mismatch")
                require(len(saved) == math.ceil(length / block),
                        "checkpoint count mismatch")
                replay_cases += 1


# 3. Source-free hypothesis is necessary: identical initial state, different
# source streams, different targets.
source_dependency_cases = 0
for width in range(2, 13):
    for length in range(1, 33):
        zero = [0] * length
        one = [0] * length
        one[-1] = 1
        require(source_bits(zero, width) != source_bits(one, width),
                "source-dependent stream unexpectedly identical")
        source_dependency_cases += 1


# 4. Fast-forwardable streams remain cheaply indexed despite the generic
# checkpoint ledger: modular increment is the compact-history control.
fast_forward_cases = 0
for width in range(2, 17):
    modulus = 1 << width
    for seed in (0, 1, modulus // 2, modulus - 1):
        state = seed
        for index in range(256):
            state = (state + 1) % modulus
            direct = (seed + index + 1) % modulus
            require(state == direct, "modular-increment fast forward mismatch")
            fast_forward_cases += 1


# 5. Exact exponent comparisons for k=241 and M=N^(6/5).
p_exp = Fraction(1, 241)
time_step_exp = Fraction(1, 240)
space_exp = Fraction(5, 12)
exponent_cases = {
    "constant_state_constant_step": (Fraction(0), Fraction(0)),
    "p_state_constant_step": (p_exp, Fraction(0)),
    "max_space_max_step": (space_exp, time_step_exp),
}
checkpoint_exponents = {}
for name, (state_exp, step_exp) in exponent_cases.items():
    optimum_exp = (1 + state_exp + step_exp) / 2
    checkpoint_exponents[name] = str(optimum_exp)
    require(optimum_exp > p_exp, "checkpoint exponent unexpectedly meets p")

threshold_cases = 0
for multiple in range(1, 13):
    # M=2^(241*multiple), hence p=M^(1/241)=2^multiple exactly.
    log2_m = 241 * multiple
    p = 1 << multiple
    require((1 << (log2_m + 2)) > p * p,
            "2*sqrt(M) should exceed the k=241 threshold")
    threshold_cases += 1


summary = {
    "run_id": "SEQUENTIAL-CHECKPOINT-MIDDLE49",
    "status": "PASS",
    "assertions": checks,
    "ledger_block_cases": ledger_cases,
    "checkpoint_replay_configurations": replay_cases,
    "source_dependency_cases": source_dependency_cases,
    "fast_forward_state_checks": fast_forward_cases,
    "threshold_cases": threshold_cases,
    "ordinary_KT_threshold_exponent_in_M": str(p_exp),
    "per_output_step_time_slack_exponent_in_M": str(time_step_exp),
    "peak_space_exponent_in_M": str(space_exp),
    "checkpoint_exponents": checkpoint_exponents,
    "scope": (
        "Finite controls for an exact checkpoint compiler and exponent ledger; "
        "not a KT lower bound, class separation, or arbitrary-source compiler."
    ),
}
print(json.dumps(summary, indent=2, sort_keys=True))
