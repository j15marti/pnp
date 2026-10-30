#!/usr/bin/env python3
"""Exact small controls for LSPV-5 generalized-support frontier run212."""
from __future__ import annotations

import itertools
import json
import math
import time
from functools import lru_cache


def parity(x: int) -> int:
    return x.bit_count() & 1


def span(rows):
    out = {0}
    for r in rows:
        out |= {x ^ r for x in tuple(out)}
    return frozenset(out)


def rank(rows):
    a = list(rows)
    out = 0
    while a:
        p = max(a)
        if p == 0:
            break
        out += 1
        bit = 1 << (p.bit_length() - 1)
        a = [x ^ p if x & bit else x for x in a if x != p]
    return out


def all_subspaces(b: int, r: int):
    seen = set()
    for rows in itertools.combinations(range(1, 1 << b), r):
        c = span(rows)
        if len(c) == 1 << r:
            seen.add(c)
    return sorted(seen, key=lambda c: tuple(sorted(c)))


def subspaces_of(code, k: int):
    nonzero = sorted(set(code) - {0})
    seen = set()
    if k == 0:
        return [frozenset({0})]
    for rows in itertools.combinations(nonzero, k):
        d = span(rows)
        if len(d) == 1 << k and d.issubset(code):
            seen.add(d)
    return list(seen)


def support_size(code):
    u = 0
    for c in code:
        u |= c
    return u.bit_count()


def generalized_weights(code):
    r = int(math.log2(len(code)))
    return {k: min(support_size(d) for d in subspaces_of(code, k))
            for k in range(1, r + 1)}


def basis(code):
    out = []
    for x in sorted(code, reverse=True):
        if rank(out + [x]) > len(out):
            out.append(x)
    return out


def output_table(code, b):
    rows = basis(code)
    return [sum(parity(row & a) << i for i, row in enumerate(rows))
            for a in range(1 << b)]


def optimal_nonlinear_one_bit_summary(code, b):
    """Exhaust every one-bit summary for b<=4; continuation is adaptive."""
    values = output_table(code, b)
    full = (1 << (1 << b)) - 1

    @lru_cache(None)
    def depth(fiber):
        if fiber == 0:
            return 0
        vals = {values[a] for a in range(1 << b) if fiber >> a & 1}
        if len(vals) <= 1:
            return 0
        best = b + 1
        for j in range(b):
            f0 = f1 = 0
            for a in range(1 << b):
                if fiber >> a & 1:
                    if a >> j & 1:
                        f1 |= 1 << a
                    else:
                        f0 |= 1 << a
            if not f0 or not f1:
                continue
            best = min(best, 1 + max(depth(f0), depth(f1)))
        return best

    optimum = b + 1
    witness = None
    checked = 0
    # Complementing a summary gives the same pair of fibers; fix source 0 in fiber 0.
    for f1 in range(0, full + 1, 2):
        f0 = full ^ f1
        q = max(depth(f0), depth(f1))
        checked += 1
        if q < optimum:
            optimum, witness = q, f1
    return optimum, witness, checked, depth.cache_info().currsize


def verify_linear_frontier(code, b):
    """Enumerate linear summaries U and fixed coordinate sets J."""
    r = int(math.log2(len(code)))
    weights = generalized_weights(code)
    rows_all = list(range(1 << b))
    checks = 0
    results = []
    for ell in range(r + 1):
        target = 0 if ell == r else weights[r - ell]
        best = b + 1
        witness = None
        # It suffices to enumerate subspaces U of the ambient dual space.
        for u in all_subspaces(b, ell) if ell else [frozenset({0})]:
            for q in range(b + 1):
                for js in itertools.combinations(range(b), q):
                    ej = span([1 << j for j in js])
                    checks += 1
                    if all(any((c ^ x) in ej for x in u) for c in code):
                        best = q
                        witness = (tuple(sorted(u)), js)
                        break
                if best == q:
                    break
            if best == target:
                break
        assert best == target, (b, code, ell, best, target)
        results.append({"L": ell, "Q": best, "d_r_minus_L": target,
                        "witness_summary": witness[0] if witness else (),
                        "witness_coordinates": witness[1] if witness else ()})
    return results, checks


def continuation_potential(code, summary_space, b):
    """Psi(S): minimum fixed raw-coordinate set after linear summary space S."""
    for q in range(b + 1):
        for js in itertools.combinations(range(b), q):
            ej = span([1 << j for j in js])
            if all(any((c ^ x) in ej for x in summary_space) for c in code):
                return q, js
    raise AssertionError("unreachable")


def main():
    started = time.perf_counter()
    linear_cases = []
    nonlinear_cases = []
    total_linear_checks = 0
    total_summaries = 0
    total_depth_states = 0
    nonlinear_advantages = []

    for b in range(2, 5):
        for r in range(1, b + 1):
            for code in all_subspaces(b, r):
                weights = generalized_weights(code)
                frontier, checks = verify_linear_frontier(code, b)
                total_linear_checks += checks
                linear_cases.append({"b": b, "r": r,
                                     "basis": basis(code),
                                     "weights": weights,
                                     "frontier": frontier})
                if r >= 2:
                    q_nonlin, witness, checked, states = optimal_nonlinear_one_bit_summary(code, b)
                    q_linear = weights[r - 1]
                    total_summaries += checked
                    total_depth_states += states
                    row = {"b": b, "r": r, "basis": basis(code),
                           "weights": weights, "L": 1,
                           "Q_linear_GHW": q_linear,
                           "Q_nonlinear_exact": q_nonlin,
                           "summary_fiber1_mask": witness,
                           "summary_maps_checked": checked,
                           "depth_states": states}
                    nonlinear_cases.append(row)
                    if q_nonlin < q_linear:
                        nonlinear_advantages.append(row)

    # Named controls.
    even4 = span([0b0011, 0b0101, 0b1001])
    rep4 = span([0b1111])
    controls = {
        "even_weight_4_3": generalized_weights(even4),
        "repetition_4_1": generalized_weights(rep4),
        "coordinate_4_3": generalized_weights(span([1, 2, 4])),
    }
    # XOR-share contextual-value control: target a0, facts a1 and a0+a1.
    target = span([0b01])
    psi0 = continuation_potential(target, span([]), 2)[0]
    psi_u = continuation_potential(target, span([0b10]), 2)[0]
    psi_v = continuation_potential(target, span([0b11]), 2)[0]
    psi_uv = continuation_potential(target, span([0b10, 0b11]), 2)[0]
    assert (psi0, psi_u, psi_v, psi_uv) == (1, 1, 1, 0)
    # Costly high-value control: acquiring the length-b repetition parity removes b probes.
    costly = {}
    for b in (4, 8, 16, 32):
        # The one-dimensional repetition code has d_1=b exactly.
        before, after = b, 0
        costly[str(b)] = {"Psi_before": before, "Psi_after": after,
                          "value": before - after,
                          "direct_acquisition_source_reads": b}

    elapsed = time.perf_counter() - started
    result = {
        "run_id": "GENERALIZED-SUPPORT-FRONTIER-REFEREE212",
        "status": "PROVED/EXACT restricted linear theorem; COMPUTATIONAL nonlinear search",
        "elapsed_seconds": elapsed,
        "linear_code_cases": len(linear_cases),
        "linear_feasibility_checks": total_linear_checks,
        "nonlinear_code_cases": len(nonlinear_cases),
        "one_bit_summary_maps_checked": total_summaries,
        "decision_subproblems_cached": total_depth_states,
        "nonlinear_advantage_count": len(nonlinear_advantages),
        "nonlinear_advantages": nonlinear_advantages,
        "named_controls": controls,
        "xor_share_contextual_control": {
            "target": "a0", "u": "a1", "v": "a0+a1",
            "Psi_empty": psi0, "Psi_u": psi_u,
            "Psi_v": psi_v, "Psi_uv": psi_uv,
            "initial_values": [psi0 - psi_u, psi0 - psi_v],
            "joint_value": psi0 - psi_uv,
        },
        "costly_high_value_controls": costly,
        "linear_cases": linear_cases,
        "nonlinear_cases": nonlinear_cases,
        "limitations": [
            "Nonlinear exhaustive search is only b<=4 and one persisted bit.",
            "No finite search proves the arbitrary nonlinear frontier.",
            "The theorem concerns parity batches, not SAT hardness.",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
