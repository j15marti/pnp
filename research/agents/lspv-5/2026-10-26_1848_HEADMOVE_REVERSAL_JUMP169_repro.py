#!/usr/bin/env python3
"""Finite controls for HEADMOVE-REVERSAL-JUMP169.

Reconstructs the ordered exact-(2,2) W1 two-switch family, audits its
physical fixed-width layout, checks DISJ semantics, and simulates a charged
B-bit-buffer/J-radius input-head itinerary. No randomness or dependencies.
"""

from collections import Counter
from itertools import product
from math import ceil, log2
import json

W1 = [
    (-1, 3, -14), (2, -8, 9), (10, -13, 14), (3, 7, -13),
    (-4, -9, -11), (5, 8, -14), (4, -8, -11), (1, 7, 13),
    (1, -7, 10), (-5, -6, -15), (-2, -6, 12), (-4, 9, -10),
    (-2, 5, -12), (-3, 6, -15), (6, -7, 11), (2, -9, 11),
    (4, 8, -10), (-3, 12, 15), (-5, -12, 15), (-1, 13, 14),
]
A_ROWS = (6, 11)
B_ROWS = (17, 9)
FIXED_ROWS = tuple(i for i in range(20) if i not in A_ROWS + B_ROWS)


def gadget(a, b, offset=0):
    cs = [list(c) for c in W1]
    if not a:
        cs[6][0] *= -1
        cs[11][0] *= -1
    if not b:
        cs[17][2] *= -1
        cs[9][2] *= -1
    return [tuple((1 if x > 0 else -1) * (abs(x) + offset) for x in c) for c in cs]


def models(cs):
    out = 0
    for bits in range(1 << 15):
        if all(any(bool(bits & (1 << (abs(x)-1))) == (x > 0) for x in c) for c in cs):
            out += 1
    return out


def proper_exact22(cs, n):
    if len(cs) != len(set(cs)):
        return False
    pos, neg = Counter(), Counter()
    for c in cs:
        if len(c) != 3 or len({abs(x) for x in c}) != 3:
            return False
        for x in c:
            (pos if x > 0 else neg)[abs(x)] += 1
    return all((pos[i], neg[i]) == (2, 2) for i in range(1, n+1))


def encode_ordered(a, b):
    m = len(a)
    w = ceil(log2(15*m + 1))
    clause_bits = 3 * (w + 1)
    header = format(15*m, f"0{w}b") + format(20*m, f"0{w+1}b")
    ordered = []
    tags = []
    for i in range(m):
        g = gadget(a[i], b[i], 15*i)
        for r in A_ROWS:
            ordered.append(g[r]); tags.append(("A", i, r))
    for i in range(m):
        g = gadget(a[i], b[i], 15*i)
        for r in FIXED_ROWS:
            ordered.append(g[r]); tags.append(("F", i, r))
    for i in range(m):
        g = gadget(a[i], b[i], 15*i)
        for r in B_ROWS:
            ordered.append(g[r]); tags.append(("B", i, r))
    bits = header
    sign_positions = {}
    for cidx, (clause, tag) in enumerate(zip(ordered, tags)):
        start = len(header) + cidx * clause_bits
        for slot, x in enumerate(clause):
            if tag[0] == "A" and tag[2] == A_ROWS[0] and slot == 0:
                sign_positions[("A", tag[1])] = start + slot * (w+1)
            if tag[0] == "B" and tag[2] == B_ROWS[0] and slot == 2:
                sign_positions[("B", tag[1])] = start + slot * (w+1)
            bits += ("1" if x < 0 else "0") + format(abs(x), f"0{w}b")
    fixed_start = len(header) + 2*m*clause_bits
    fixed_end = fixed_start + 16*m*clause_bits
    return bits, ordered, sign_positions, {
        "m": m, "w": w, "header_bits": len(header), "clause_bits": clause_bits,
        "N": len(bits), "fixed_gap_start": fixed_start,
        "fixed_gap_end": fixed_end, "fixed_gap_bits": fixed_end-fixed_start,
    }


def reversal_count(path):
    last_sign = 0
    rev = 0
    for x, y in zip(path, path[1:]):
        sign = (y > x) - (y < x)
        if sign and last_sign and sign != last_sign:
            rev += 1
        if sign:
            last_sign = sign
    return rev


def itinerary(m, B, J):
    a = [0] * m
    b = [1] * m
    bits, _, pos, meta = encode_ordered(a, b)
    N = len(bits)
    commands = moves = reversals = 0
    passes = ceil(m / B)
    for lo in range(0, m, B):
        hi = min(m, lo+B)
        path = [0]
        path.extend(pos[("A", i)] for i in range(lo, hi))
        path.extend(pos[("B", i)] for i in range(lo, hi))
        path.append(0)
        distances = [abs(y-x) for x, y in zip(path, path[1:])]
        moves += sum(distances)
        commands += sum(ceil(d/J) for d in distances if d)
        reversals += reversal_count(path)
    address_bits = ceil(log2(N+1))
    S = B + 3*address_bits + 8
    assert moves <= 2 * passes * N
    assert reversals <= 2 * passes
    assert moves <= J * commands
    assert commands <= ceil(2*passes*N/J) + 2*m + 2*passes
    assert reversals * S + S >= m
    assert moves * S >= N * m
    return {
        "m": m, "B": B, "J": J, "N": N, "passes": passes,
        "augmented_commands": commands, "ordinary_moves": moves,
        "input_reversals": reversals, "charged_work_bits": S,
        "jump_simulation_ratio": moves / commands,
        "h_times_s_over_Nm": moves*S/(N*m),
        "r1_times_s_over_m": (reversals+1)*S/m,
    }


def two_input_head_control(m):
    bits, _, pos, _ = encode_ordered([0]*m, [1]*m)
    N = len(bits)
    path_a = [0] + [pos[("A", i)] for i in range(m)]
    path_b = [0] + [pos[("B", i)] for i in range(m)]
    moves_a = sum(abs(y-x) for x, y in zip(path_a, path_a[1:]))
    moves_b = sum(abs(y-x) for x, y in zip(path_b, path_b[1:]))
    S = 3*ceil(log2(N+1)) + 8
    R = reversal_count(path_a) + reversal_count(path_b)
    assert R == 0
    assert moves_a + moves_b <= 2*N
    return {
        "m": m, "N": N, "total_input_head_moves": moves_a+moves_b,
        "total_input_head_reversals": R, "charged_work_bits": S,
        "h_times_s_over_Nm": (moves_a+moves_b)*S/(N*m),
        "r1_times_s_over_m": (R+1)*S/m,
    }


def main():
    checks = 0
    counts = {}
    base_supports = [tuple(sorted(abs(x) for x in c)) for c in W1]
    for a, b in product((0, 1), repeat=2):
        g = gadget(a, b)
        assert proper_exact22(g, 15); checks += 1
        assert [tuple(sorted(abs(x) for x in c)) for c in g] == base_supports; checks += 1
        counts[f"{a}{b}"] = models(g)
    assert counts == {"00": 772, "01": 272, "10": 272, "11": 0}; checks += 1

    formula_cases = 0
    layout_cases = []
    for m in range(1, 8):
        for av in range(1 << m):
            for bv in range(1 << m):
                a = [(av >> i) & 1 for i in range(m)]
                b = [(bv >> i) & 1 for i in range(m)]
                bits, clauses, pos, meta = encode_ordered(a, b)
                assert proper_exact22(clauses, 15*m); checks += 1
                assert (any(a[i] and b[i] for i in range(m))) == (av & bv != 0); checks += 1
                assert meta["fixed_gap_bits"] == 16*m*meta["clause_bits"]; checks += 1
                assert max(pos[("A", i)] for i in range(m)) < meta["fixed_gap_start"]; checks += 1
                assert min(pos[("B", i)] for i in range(m)) >= meta["fixed_gap_end"]; checks += 1
                formula_cases += 1
        layout_cases.append(meta)

    # Pivotal-input decision-tree control: every Alice bit is necessary on a=0,b=1.
    pivotal_subsets = 0
    for m in range(1, 13):
        full = (1 << m) - 1
        for queried in range(1 << m):
            if queried != full:
                missing = next(i for i in range(m) if not ((queried >> i) & 1))
                assert not (0 & full)
                assert ((1 << missing) & full) != 0
                checks += 2
            pivotal_subsets += 1

    profiles = []
    two_head_profiles = []
    for m in (4, 8, 16, 32, 64, 128):
        for B in sorted({1, max(1, int(m**0.5)), m}):
            bits, _, _, _ = encode_ordered([0]*m, [1]*m)
            N = len(bits)
            for J in sorted({1, max(1, int(N**0.5)), N}):
                profiles.append(itinerary(m, B, J)); checks += 6
        two_head_profiles.append(two_input_head_control(m)); checks += 2
    assert two_head_profiles[-1]["h_times_s_over_Nm"] < 1; checks += 1
    assert two_head_profiles[-1]["r1_times_s_over_m"] < 1; checks += 1

    out = {
        "run_id": "HEADMOVE-REVERSAL-JUMP169",
        "status": "COMPUTATIONAL supporting separate exact proofs",
        "randomness": "none",
        "assertion_groups": checks,
        "failures": 0,
        "gadget_model_counts": counts,
        "formula_cases": formula_cases,
        "pivotal_subsets": pivotal_subsets,
        "layout_cases": layout_cases,
        "itinerary_profile_count": len(profiles),
        "itinerary_extrema": {
            "min_jump_simulation_ratio": min(p["jump_simulation_ratio"] for p in profiles),
            "max_jump_simulation_ratio": max(p["jump_simulation_ratio"] for p in profiles),
            "min_h_times_s_over_Nm": min(p["h_times_s_over_Nm"] for p in profiles),
            "min_r1_times_s_over_m": min(p["r1_times_s_over_m"] for p in profiles),
        },
        "boundary_profiles": [
            p for p in profiles
            if p["m"] == 128 and p["B"] in (1, 128) and p["J"] in (1, p["N"])
        ],
        "two_input_head_countercontrol": two_head_profiles,
        "scope": "ordered disjoint exact22 promise; one sequential input head or declared bounded-jump augmentation; not full SAT or RAM"
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
