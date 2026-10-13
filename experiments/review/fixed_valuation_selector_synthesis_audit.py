#!/usr/bin/env python3
"""Independent exponent-level audit for VALSUBCUBEFW1.

This script works in the exponent group of GF(2^d)^*.  It checks the exact
3-adic and correction identities used by the fixed-valuation selector.  It
does not replace the predecessor's polynomial-basis field and Tseitin audit.
"""

from __future__ import annotations

import hashlib
import json
import random
import time


SEED = 14102026


def v3(n: int) -> int:
    out = 0
    while n and n % 3 == 0:
        n //= 3
        out += 1
    return out


def order_of_exponent(exp: int, modulus: int) -> int:
    from math import gcd

    return modulus // gcd(exp % modulus, modulus)


def main() -> None:
    start = time.perf_counter()
    rng = random.Random(SEED)
    assertions = 0
    fixed_degrees = 0
    cube_targets = 0
    off_image_targets = 0
    selected_root_differs = 0
    square_cotree_cases = 0
    logarithmic_window_cases = 0
    max_candidates = 0

    def check(condition: bool, message: str) -> None:
        nonlocal assertions
        assertions += 1
        if not condition:
            raise AssertionError(message)

    for a in range(1, 5):
        r = 2 * (3**a)
        for d in range(2, 301, 2):
            if v3(d) != a:
                continue
            fixed_degrees += 1
            n = (1 << d) - 1
            n0 = (1 << r) - 1
            check(d % r == 0, f"subfield degree does not divide: a={a}, d={d}")
            check(n % n0 == 0, f"multiplicative subfield order failure: {d}")
            check(v3(n) == a + 1, f"ambient LTE failure: {d}")
            check(v3(n0) == a + 1, f"subfield LTE failure: {r}")
            cofactor = n // n0
            check(cofactor % 3 != 0, f"cofactor divisible by 3: {d}")

            # A generator of the unique subfield has ambient generator
            # exponent ``cofactor``.  Its nondivisibility by 3 proves that it
            # is not an ambient cube.
            c_exp = cofactor
            check(c_exp % 3 != 0, f"subfield generator became a cube: {d}")
            check(order_of_exponent(c_exp, n) == n0, f"wrong subfield order: {d}")

            m = n // (3 ** (a + 1))
            check(m % 3 != 0, f"m not coprime to 3: {d}")
            eta_exp = (c_exp * m) % n
            check(
                order_of_exponent(eta_exp, n) == 3 ** (a + 1),
                f"eta lacks full 3-primary order: {d}",
            )
            e = pow(3, -1, m)

            samples = range(n) if d <= 12 else [rng.randrange(n) for _ in range(64)]
            for w in samples:
                b_exp = (3 * w) % n
                y_exp = (b_exp * e) % n
                good = []
                for j in range(3**a):
                    x_exp = (y_exp + j * eta_exp) % n
                    if (3 * x_exp - b_exp) % n == 0:
                        good.append(x_exp)
                max_candidates = max(max_candidates, 3**a)
                check(len(good) == 1, f"correction transversal failure: a={a}, d={d}")
                x_exp = good[0]
                check((3 * x_exp - b_exp) % n == 0, f"root check failed: {d}")
                cube_targets += 1
                if x_exp != w % n:
                    selected_root_differs += 1

            for _ in range(24):
                b_exp = rng.randrange(n)
                while b_exp % 3 == 0:
                    b_exp = rng.randrange(n)
                y_exp = (b_exp * e) % n
                found = any(
                    (3 * ((y_exp + j * eta_exp) % n) - b_exp) % n == 0
                    for j in range(3**a)
                )
                check(not found, f"off-image exponent accepted: a={a}, d={d}")
                off_image_targets += 1

    # Genuine K_{s,s} cotree dimensions d=(s-1)^2.  Fixed valuation of
    # s-1 gives fixed valuation of d and therefore the same subfield repair.
    for s in range(3, 401, 2):
        base = s - 1
        h = v3(base)
        if h == 0:
            continue
        d = base * base
        a = v3(d)
        check(a == 2 * h, f"square valuation failure: s={s}")
        check(d % (2 * 3**a) == 0, f"square subfield divisibility failure: s={s}")
        square_cotree_cases += 1

    # Symbolic-size controls for a genuinely unbounded valuation sequence.
    # These checks intentionally avoid constructing GF(2^d): d itself is
    # already the field-vector dimension.  Choosing a large 3-coprime factor
    # shows that nu_3(d) may grow while r=2*3^a remains O(log d).
    for a in range(1, 9):
        u = (1 << (3**a)) + 1
        while u % 3 == 0:
            u += 1
        d = 2 * (3**a) * u
        r = 2 * (3**a)
        check(v3(d) == a, f"unbounded-window valuation failure: a={a}")
        check(r <= 2 * d.bit_length(), f"unbounded-window size failure: a={a}")
        logarithmic_window_cases += 1

    source = open(__file__, "rb").read()
    result = {
        "run_id": "VALSUBREVIEW1",
        "seed": SEED,
        "status": "COMPUTATIONAL",
        "audit_scope": "exponent-group identities; predecessor covers polynomial-basis fields and Tseitin reconstruction",
        "fixed_valuations": [1, 2, 3, 4],
        "fixed_degrees_checked": fixed_degrees,
        "cube_targets_checked": cube_targets,
        "off_image_targets_rejected": off_image_targets,
        "selected_root_differs_from_source": selected_root_differs,
        "square_cotree_cases_checked": square_cotree_cases,
        "logarithmic_window_cases_checked": logarithmic_window_cases,
        "largest_correction_transversal": max_candidates,
        "assertions": assertions,
        "failures": 0,
        "elapsed_seconds": round(time.perf_counter() - start, 6),
        "code_sha256": hashlib.sha256(source).hexdigest(),
        "limitations": [
            "finite arithmetic checks do not prove asymptotics",
            "the symbolic proof supplies the all-d fixed-valuation theorem",
            "the eight size controls do not prove the logarithmic-window theorem or unrestricted SAT time",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
