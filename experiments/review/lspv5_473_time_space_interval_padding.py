#!/usr/bin/env python3
"""Exact controls for LSPV-5/473 time/space interval and native padding."""

from fractions import Fraction
from decimal import Decimal, getcontext
import json
import math

getcontext().prec = 50


def beta(c: Fraction) -> Fraction:
    return ((c + 2) / (c * c) - c) / 2


def high_address(n: int, r: Fraction) -> tuple[int, int]:
    """Address 2^floor(r log2 n), and bits appended to the index tape."""
    exponent = (r.numerator * (n.bit_length() - 1)) // r.denominator
    return 1 << exponent, exponent + 1


def dec_power(n_exp: int, exponent: Decimal) -> Decimal:
    return Decimal(10) ** (Decimal(n_exp) * exponent)


phi = (Decimal(5).sqrt() + 1) / 2
later_product = Decimal(2) * (Decimal(str(math.pi)) / Decimal(7)).cos() if hasattr(Decimal(1), "cos") else Decimal(str(2 * math.cos(math.pi / 7)))
# Decimal.cos is unavailable on some Python builds; overwrite with a stable literal.
later_product = Decimal("1.8019377358048382524722046390148901023318383242637")

assert beta(Fraction(6, 5)) == Fraction(23, 45)
assert beta(Fraction(6, 5)) - Fraction(1, 2) == Fraction(1, 90)

checks = 2
for den in range(2, 81):
    for num in range(den + 1, 2 * den + 1):
        c = Fraction(num, den)
        assert beta(c) < c
        checks += 1

wrapper_controls = []
for n in [2, 3, 7, 16, 31, 64, 1000, 10**6]:
    for r in [Fraction(1, 2), Fraction(1), Fraction(6, 5), Fraction(2), Fraction(5)]:
        address, index_bits = high_address(n, r)
        upper = Decimal(n) ** (Decimal(r.numerator) / Decimal(r.denominator))
        assert Decimal(address) <= upper
        # floor(r floor(log2 n)) can lose at most r+1 binary exponent units.
        assert Decimal(address) * (Decimal(2) ** (Decimal(r.numerator) / Decimal(r.denominator) + 1)) >= upper
        assert index_bits == address.bit_length()
        checks += 3
        wrapper_controls.append({
            "N": n,
            "r": f"{r.numerator}/{r.denominator}",
            "native_highwater": str(address),
            "index_build_steps": index_bits,
            "touched_far_cells": 1,
            "sparse_dummy_record_bits_upper": 2 * index_bits + 3,
        })

cs = [Decimal("1.01"), Decimal("1.1"), Decimal("1.2"), Decimal("1.4"),
      Decimal("1.5"), Decimal("1.5213797068"), Decimal("1.618"),
      later_product, Decimal("2"), Decimal("5"), Decimal("10"), Decimal("100")]
intervals = []
for c in cs:
    b = ((c + 2) / (c * c) - c) / 2
    flmv = max(Decimal(0), b)
    later = max(Decimal(0), later_product - c)
    lower = max(flmv, later)
    assert lower <= c
    checks += 1
    intervals.append({
        "c": str(c),
        "flmv_beta_positive_part": str(flmv),
        "later_product_lower_positive_part": str(later),
        "combined_known_lower_exponent": str(lower),
        "sparse_normalized_upper_exponent": str(c),
        "unclosed_exponent_gap": str(c - lower),
    })

scales = []
c = Decimal("1.2")
b = Decimal(23) / Decimal(45)
later = later_product - c
lower = max(b, later)
for e in [6, 12, 24, 60]:
    scales.append({
        "N": f"1e{e}",
        "N_pow_beta_23_over_45": str(dec_power(e, b)),
        "N_pow_later_lower": str(dec_power(e, lower)),
        "N_pow_sparse_upper_c": str(dec_power(e, c)),
        "note": "growth-law values only; not bytes",
    })

result = {
    "node": "P2-L5-473",
    "status": "PASS",
    "assertions": checks,
    "exact": {"beta_6_over_5": "23/45", "gap_over_half": "1/90"},
    "later_product_exponent": str(later_product),
    "intervals": intervals,
    "illustrative_scales": scales,
    "wrapper_sample_count": len(wrapper_controls),
    "wrapper_controls": wrapper_controls,
    "conclusions": {
        "original_native_space_from_time": "NOT_UPPER_BOUNDED_BY_T_DUE_TO_HIGH_ADDRESS_PADDING",
        "normalized_equivalent_space": "O(T_POLYLOG_T)",
        "exact_space_from_time_and_lower_bounds": "NOT_IDENTIFIED",
        "required_next_step": "STRICT_SPACE_CONTRACTION_BELOW_KNOWN_LOWER_ENVELOPE",
        "p_vs_np": "OPEN",
    },
}
print(json.dumps(result, indent=2, sort_keys=True))

