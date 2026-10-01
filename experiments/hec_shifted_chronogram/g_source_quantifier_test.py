#!/usr/bin/env python3
"""Exact quantifier-order sanity checks for G-PPC-HEC."""
from fractions import Fraction

for m in [1,2,4,8,16,32,64]:
    pre = Fraction(1, 2**m)
    clairvoyant = Fraction(1,1)
    print({
        "future_bits": m,
        "precommit_success": str(pre),
        "ex_post_existential_success": str(clairvoyant),
        "unit_rate_ticks_required": m,
    })
