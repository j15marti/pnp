#!/usr/bin/env python3
"""Finite controls for CHECKPOINT-REPLAY-FRONTIER-REFEREE208.

The symbolic checkpoint/replay theorem is proved in the accompanying report.
This dependency-free script compares four exact reconstruction schedules on a
deterministic state chain.  It is intentionally small enough for one <30 s run.
"""

from __future__ import annotations

import json
import math
import time


MASK = (1 << 64) - 1


def transition(i: int, x: int) -> int:
    """Deterministic, deliberately not assumed invertible."""
    y = (x * 6364136223846793005 + 1442695040888963407 + i) & MASK
    return (y ^ (y >> 23) ^ ((x << 17) & MASK)) & MASK


def reference(m: int, x0: int) -> tuple[list[int], int, int]:
    states = [x0]
    calls = 0
    for i in range(m):
        states.append(transition(i, states[-1]))
        calls += 1
    return list(reversed(states)), calls, len(states)


def block_checkpoint(m: int, x0: int, length: int) -> tuple[list[int], int, int]:
    """Store every length-th state, then replay each block once backward."""
    checkpoints: dict[int, int] = {0: x0}
    x = x0
    calls = 0
    for i in range(m):
        x = transition(i, x)
        calls += 1
        if (i + 1) % length == 0 or i + 1 == m:
            checkpoints[i + 1] = x

    out: list[int] = []
    peak_states = len(checkpoints)
    ends = sorted(checkpoints)
    for j in range(len(ends) - 1, 0, -1):
        lo, hi = ends[j - 1], ends[j]
        local = [checkpoints[lo]]
        for i in range(lo, hi):
            local.append(transition(i, local[-1]))
            calls += 1
        peak_states = max(peak_states, len(checkpoints) + len(local))
        if not out:
            out.extend(reversed(local))
        else:
            out.extend(reversed(local[:-1]))
    return out, calls, peak_states


def divide_replay(m: int, x0: int) -> tuple[list[int], int, int]:
    """Binary recursive replay; emits every chain state in reverse order."""
    out: list[int] = []
    calls = 0
    peak_states = 0

    def emit(lo: int, hi: int, x_lo: int, depth: int) -> None:
        nonlocal calls, peak_states
        peak_states = max(peak_states, depth + 1)
        if hi == lo:
            out.append(x_lo)
            return
        if hi == lo + 1:
            x_hi = transition(lo, x_lo)
            calls += 1
            out.extend((x_hi, x_lo))
            return
        mid = (lo + hi) // 2
        x_mid = x_lo
        for i in range(lo, mid):
            x_mid = transition(i, x_mid)
            calls += 1
        right_before = len(out)
        emit(mid, hi, x_mid, depth + 1)
        # The midpoint was emitted by the right half; suppress its duplicate.
        right = out[right_before:]
        del out[right_before:]
        emit(lo, mid, x_lo, depth + 1)
        left = out[right_before:]
        del out[right_before:]
        out.extend(right)
        out.extend(left[1:])

    emit(0, m, x0, 0)
    return out, calls, peak_states


def pure_replay(m: int, x0: int) -> tuple[list[int], int, int]:
    out: list[int] = []
    calls = 0
    for hi in range(m, -1, -1):
        x = x0
        for i in range(hi):
            x = transition(i, x)
            calls += 1
        out.append(x)
    return out, calls, 2


def xor_inverse_control(m: int, x0: int) -> tuple[list[int], int, int]:
    constants = [transition(i, i + 1) for i in range(m)]
    x = x0
    calls = 0
    for c in constants:
        x ^= c
        calls += 1
    out = [x]
    for c in reversed(constants):
        x ^= c
        calls += 1
        out.append(x)
    return out, calls, 2


def xor_reference(m: int, x0: int) -> list[int]:
    constants = [transition(i, i + 1) for i in range(m)]
    states = [x0]
    for c in constants:
        states.append(states[-1] ^ c)
    return list(reversed(states))


def symbolic_frontier(mu: float, beta: float, gamma: float) -> dict:
    output_floor = mu + beta
    base_time = max(mu + gamma, output_floor)
    return {
        "parameters": {"mu": mu, "beta": beta, "gamma": gamma},
        "materialize_all": {"time": base_time, "space": mu + beta},
        "sqrt_block": {"time": base_time, "space": beta + mu / 2},
        "divide_replay": {"time": base_time, "space": beta},
        "pure_replay": {"time": max(2 * mu + gamma, output_floor), "space": beta},
        "invertible_chain": {"time": base_time, "space": beta},
        "output_is_write_only": True,
    }


def main() -> None:
    started = time.perf_counter()
    rows = []
    x0 = 0x123456789ABCDEF0
    for h in range(2, 12):
        m = 1 << h
        expected, material_calls, material_peak = reference(m, x0)
        length = max(1, round(math.sqrt(m)))
        got_b, calls_b, peak_b = block_checkpoint(m, x0, length)
        got_d, calls_d, peak_d = divide_replay(m, x0)
        got_p, calls_p, peak_p = pure_replay(m, x0)
        assert got_b == expected
        assert got_d == expected
        assert got_p == expected
        assert calls_b == 2 * m
        assert calls_p == m * (m + 1) // 2
        assert peak_d <= 2 + math.ceil(math.log2(m))
        rows.append({
            "m": m,
            "sqrt_block_length": length,
            "transition_calls": {
                "materialize": material_calls,
                "sqrt_block": calls_b,
                "divide_replay": calls_d,
                "pure_replay": calls_p,
            },
            "peak_live_states_upper_or_measured": {
                "materialize": material_peak,
                "sqrt_block": peak_b,
                "divide_replay": peak_d,
                "pure_replay": peak_p,
            },
            "divide_calls_over_m_log2m": calls_d / (m * math.log2(m)),
        })

    for m in (4, 16, 64, 256, 1024):
        got, calls, peak = xor_inverse_control(m, x0)
        assert got == xor_reference(m, x0)
        assert calls == 2 * m and peak == 2

    out = {
        "run_id": "CHECKPOINT-REPLAY-FRONTIER-REFEREE208",
        "status": {
            "symbolic": "PROVED/EXACT in accompanying report",
            "finite": "COMPUTATIONAL",
            "P_vs_NP": "OPEN",
        },
        "rows": rows,
        "symbolic_examples": [
            symbolic_frontier(0.4, 0.2, 0.3),
            symbolic_frontier(1.0, 0.0, 1.0),
        ],
        "checks": {
            "all_exact_outputs_match": True,
            "largest_m": rows[-1]["m"],
            "xor_invertible_controls": 5,
            "elapsed_seconds": time.perf_counter() - started,
            "dependencies": [],
        },
        "limitations": [
            "The replay theorem is for an authenticated deterministic path recurrence.",
            "It is an upper-bound schedule, not a lower bound or an optimality theorem.",
            "The test counts abstract transitions and live states, not native TM cells.",
            "No arbitrary-SAT decomposition or P-versus-NP implication is proved.",
        ],
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
