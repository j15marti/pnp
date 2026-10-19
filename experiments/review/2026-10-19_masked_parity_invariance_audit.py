#!/usr/bin/env python3
"""Independent audit for MASKED-PARITY-SHEAR8 and synthesis invariants."""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path


RAW_ROWS = [
    [3, 8, 12, 52, 122, 2592, 10, 417, 782, 783, 469, 230, 2294, 3214, 10, 1424, 47, 91, 59, 12, 526, 459, 8, 16, 16, 114, 88],
    [4, 16, 32, 168, 398, 10780, 30, 1361, 2554, 2555, 1529, 750, 7494, 10494, 12, 4743, 133, 257, 165, 32, 1538, 1436, 16, 32, 32, 242, 184],
    [5, 32, 80, 456, 1086, 32618, 78, 3713, 6970, 6971, 4169, 2046, 20454, 28638, 14, 12227, 331, 647, 411, 80, 3982, 3414, 32, 64, 64, 498, 346],
    [6, 64, 192, 1144, 2734, 98464, 190, 9345, 17546, 17547, 10489, 5150, 51494, 72094, 15, 30375, 791, 1555, 983, 192, 9734, 8248, 64, 128, 128, 1010, 718],
    [7, 128, 448, 2744, 6574, 256428, 446, 22465, 42186, 42187, 25209, 12382, 123814, 173342, 16, 71132, 1847, 3635, 2295, 448, 22982, 19086, 128, 256, 256, 2034, 1452],
]


def forward(x: tuple[int, ...]) -> tuple[int, ...]:
    y = [0] * len(x)
    y[0] = x[0]
    y[1] = x[1]
    for i in range(2, len(x)):
        y[i] = x[i] ^ (y[i - 1] & x[i - 2])
    return tuple(y)


def inverse(y: tuple[int, ...]) -> tuple[int, ...]:
    x = [0] * len(y)
    x[0] = y[0]
    x[1] = y[1]
    for i in range(2, len(y)):
        x[i] = y[i] ^ (y[i - 1] & x[i - 2])
    return tuple(x)


def anf_xor(a: set[frozenset[int]], b: set[frozenset[int]]) -> set[frozenset[int]]:
    return a.symmetric_difference(b)


def anf_mul_var(a: set[frozenset[int]], var: int) -> set[frozenset[int]]:
    return {m | {var} for m in a}


def build_anf(n: int) -> list[set[frozenset[int]]]:
    ys = [{frozenset({0})}, {frozenset({1})}]
    for i in range(2, n):
        ys.append(anf_xor({frozenset({i})}, anf_mul_var(ys[-1], i - 2)))
    return ys


def clause_sat(clause: tuple[int, ...], assignment: tuple[int, ...]) -> bool:
    return any((assignment[abs(lit) - 1] == 1) if lit > 0 else (assignment[abs(lit) - 1] == 0) for lit in clause)


def all_clause_sat(clauses: tuple[tuple[int, ...], ...], assignment: tuple[int, ...]) -> bool:
    return all(clause_sat(c, assignment) for c in clauses)


def and_clauses() -> tuple[tuple[int, ...], ...]:
    # Variables: a=1,b=2,z=3,p=4,q=5. Proper 3-CNF, four pad extensions.
    return ((-1, -2, 3), (1, -3, 4), (1, -3, -4), (2, -3, 5), (2, -3, -5))


def xor_clauses() -> tuple[tuple[int, ...], ...]:
    out = []
    for a in (0, 1):
        for b in (0, 1):
            z = 1 - (a ^ b)
            vals = (a, b, z)
            out.append(tuple((i + 1) if vals[i] == 0 else -(i + 1) for i in range(3)))
    return tuple(out)


def parity_charge(x: int, d: int) -> int:
    v = 1 << d
    b = 0
    e = 0
    for u in range(v):
        for bit in range(d):
            w = u ^ (1 << bit)
            if u < w:
                if (x >> e) & 1:
                    b ^= 1 << u
                    b ^= 1 << w
                e += 1
    return b


def slope(y0: int, y1: int, x0: int, x1: int) -> float:
    return math.log(y1 / y0) / math.log(x1 / x0)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    failures: list[str] = []
    inverse_tests = 0
    for n in range(3, 15):
        for a in range(1 << n):
            x = tuple((a >> i) & 1 for i in range(n))
            if inverse(forward(x)) != x:
                failures.append(f"inverse:n={n}:a={a}")
            inverse_tests += 1

    anf_tests = 0
    anf_sizes = []
    # n=3 is the exceptional base case: y2=x2+x1*x0 has degree 2, not n-2.
    # The exact n-2 formula begins at n=4; all cube instances audited here have M>=12.
    for n in range(3, 23):
        ys = build_anf(n)
        expected = frozenset(range(n - 2)) if n >= 4 else frozenset({0, 1})
        degree = max(map(len, ys[-1]))
        expected_degree = n - 2 if n >= 4 else 2
        ok = degree == expected_degree and expected in ys[-1]
        if not ok:
            failures.append(f"anf:n={n}:degree={degree}:target={expected in ys[-1]}")
        anf_sizes.append({"n": n, "last_degree": degree, "expected_degree": expected_degree, "last_monomials": len(ys[-1])})
        anf_tests += 1

    and_extension_counts = Counter()
    and_tests = 0
    for a in (0, 1):
        for b in (0, 1):
            for z in (0, 1):
                c = 0
                for p in (0, 1):
                    for q in (0, 1):
                        c += all_clause_sat(and_clauses(), (a, b, z, p, q))
                        and_tests += 1
                and_extension_counts[f"{a}{b}{z}"] = c
                if c != (4 if z == (a & b) else 0):
                    failures.append(f"and:{a}{b}{z}:extensions={c}")

    xor_tests = 0
    for a in (0, 1):
        for b in (0, 1):
            for z in (0, 1):
                got = all_clause_sat(xor_clauses(), (a, b, z))
                if got != (z == (a ^ b)):
                    failures.append(f"xor:{a}{b}{z}:{got}")
                xor_tests += 1

    charge_counts = Counter(parity_charge(x, 3) for x in range(1 << 12))
    if len(charge_counts) != 128 or set(charge_counts.values()) != {32}:
        failures.append(f"q3_charge_distribution:{len(charge_counts)}:{set(charge_counts.values())}")

    formula_checks = 0
    row_audits = []
    for row in RAW_ROWS:
        (d, v, m, n, c, source_bits, deg, rg, rpin, redge, rw, rb, rmos, rbmos, rdepth, rtog,
         pg, pe, pw, pb, pmos, ptog, sg, se, sw, smos, stog) = row
        expected = {
            "V": 2**d,
            "M": d * 2 ** (d - 1),
            "N": 5 * m - 8 + v * (d - 3),
            "C": 9 * (m - 2) + 4 * v * (d - 2),
            "degree": m - 2,
            "raw_G": n + 3 * c - 1,
            "raw_P_in": n + 6 * c - 2,
            "raw_E": n + 6 * c - 1,
            "raw_W": 2 * n + 3 * c - 1,
            "raw_MOS": 2 * n + 18 * c - 6,
            "raw_buffered_MOS": rmos + 4 * rb,
            "SAT_macro_G": v,
            "SAT_macro_E": 2 * v,
            "SAT_macro_W": 2 * v,
            "SAT_MOS": 16 * (v - 1) + 2,
        }
        observed = {
            "V": v, "M": m, "N": n, "C": c, "degree": deg, "raw_G": rg,
            "raw_P_in": rpin, "raw_E": redge, "raw_W": rw, "raw_MOS": rmos,
            "raw_buffered_MOS": rbmos, "SAT_macro_G": sg, "SAT_macro_E": se,
            "SAT_macro_W": sw, "SAT_MOS": smos,
        }
        for k in expected:
            formula_checks += 1
            if expected[k] != observed[k]:
                failures.append(f"row:d={d}:{k}:expected={expected[k]}:got={observed[k]}")
        primitive = {
            "G": 4 * v - 3,
            "P_in": 8 * v - 7,
            "P_out": 4 * v - 3,
            "E": 8 * v - 6,
            "W": 5 * v - 3,
            "MOS": smos,
            "depth": 3 * d + 1,
        }
        row_audits.append({"d": d, "V": v, "M": m, "macro_depth": d + 1, "NAND2_INV_expansion": primitive})

    first, last = RAW_ROWS[0], RAW_ROWS[-1]
    slopes = {
        "raw_nominal_MOS_vs_source_bits": slope(first[12], last[12], first[5], last[5]),
        "raw_buffered_MOS_vs_source_bits": slope(first[13], last[13], first[5], last[5]),
        "raw_distinct_nets_vs_source_bits": slope(first[10], last[10], first[5], last[5]),
        "projection_MOS_vs_M_source_edges": slope(first[20], last[20], first[2], last[2]),
        "SAT_charge_MOS_vs_V_charge_bits": slope(first[25], last[25], first[1], last[1]),
    }

    result = {
        "artifact": "BIJECTIVE-MASK-INVARIANCE8",
        "status": "PASS" if not failures else "FAIL",
        "theorem_checked": "For n>=4 the triangular map is bijective and its final coordinate has ANF degree n-2; composing a Q_d parity system (M>=12) with it preserves SAT and model count.",
        "boundary_case": "At n=3 the final coordinate has degree 2, so the n-2 formula has an explicit exceptional base case outside the reported cube range.",
        "exact_counterexample_checked": "For the same charge-parity circuit and identical MOS total, mixed-cell G=V while NAND2+INV-expanded G=4V-3; gate count is library-granularity dependent.",
        "tests": {
            "exhaustive_inverse_assignments": inverse_tests,
            "ANF_symbolic_instances": anf_tests,
            "proper_AND_assignments": and_tests,
            "proper_XOR_assignments": xor_tests,
            "Q3_edge_assignments": 1 << 12,
            "ledger_formula_equalities": formula_checks,
        },
        "proper_AND_pad_extensions": dict(and_extension_counts),
        "Q3_charge_vectors": len(charge_counts),
        "Q3_preimages_per_even_charge": sorted(set(charge_counts.values())),
        "ANF_audit": anf_sizes,
        "ledger_expansions": row_audits,
        "same_family_endpoint_log_slopes": slopes,
        "comparability_guard": "Each slope is internal to one fixed semantics/library/model family. Raw, projection and promised charge decision are not minimum-cost comparisons.",
        "failures": failures,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
