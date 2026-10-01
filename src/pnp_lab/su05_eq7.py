"""Exact SU05 Eq.(7) orbit controls for product-span experiments.

Scope guard
-----------
This module transcribes and tests the *q-ary orbit formula* of Shaltiel--Umans
(JACM 2005, Eq. (7)) together with a canonical Hadamard bit projection.

It is NOT an exact implementation of the local extractor E used abstractly in
van Melkebeek--Mocelin Sdroievski (CCC 2023, Lemma 21).  In particular, their
statement uses a uniform fixed-length binary seed over an odd prime field but
does not expose the exact sampler/field-label implementation.  Functions in
this module that use integer modulo p are therefore labeled controls, not
claims about the authors' exact bit-seed realization.

The natural-domain experiments are exact over F_p and are useful for:
  * checking the SU05 orbit/product-span algebra;
  * constructing explicit full-rank quadratic-feature minors;
  * testing Boolean-grid low-degree interpolants;
  * stress-testing ANF degree after one explicit, labeled bit wrapper.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Sequence
import hashlib

from .boolean import anf_degree
from .gf2 import rank_bitvectors


def _prime_factors(n: int) -> list[int]:
    if n < 1:
        raise ValueError("n must be positive")
    factors: list[int] = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            factors.append(d)
            while n % d == 0:
                n //= d
        d = 3 if d == 2 else d + 2
    if n > 1:
        factors.append(n)
    return factors


def primitive_root_prime(p: int) -> int:
    """Return the least primitive root modulo an odd prime p.

    This routine is intended only for the small exact controls in this module.
    """
    if p < 3:
        raise ValueError("p must be an odd prime for these controls")
    phi = p - 1
    factors = _prime_factors(phi)
    for g in range(2, p):
        if all(pow(g, phi // q, p) != 1 for q in factors):
            return g
    raise ValueError("no primitive root found; p may not be prime")


def poly_eval(coefficients: Sequence[int], x: int, p: int) -> int:
    y = 0
    for coefficient in reversed(coefficients):
        y = (y * x + coefficient) % p
    return y


def _trim(coefficients: list[int], p: int) -> list[int]:
    while len(coefficients) > 1 and coefficients[-1] % p == 0:
        coefficients.pop()
    return [x % p for x in coefficients]


def _poly_add(a: Sequence[int], b: Sequence[int], p: int) -> list[int]:
    out = [0] * max(len(a), len(b))
    for i in range(len(out)):
        out[i] = (
            (a[i] if i < len(a) else 0)
            + (b[i] if i < len(b) else 0)
        ) % p
    return _trim(out, p)


def _poly_mul(a: Sequence[int], b: Sequence[int], p: int) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] = (out[i + j] + x * y) % p
    return _trim(out, p)


def _poly_scale(a: Sequence[int], scalar: int, p: int) -> list[int]:
    return _trim([(scalar * x) % p for x in a], p)


def lagrange_interpolate(
    xs: Sequence[int], ys: Sequence[int], p: int
) -> list[int]:
    """Interpolate the unique degree < len(xs) polynomial over F_p."""
    if len(xs) != len(ys) or not xs:
        raise ValueError("xs and ys must be nonempty and have equal length")
    xs_mod = [x % p for x in xs]
    if len(set(xs_mod)) != len(xs_mod):
        raise ValueError("interpolation points must be distinct modulo p")

    result = [0]
    for i, (xi, yi) in enumerate(zip(xs_mod, ys)):
        basis = [1]
        denominator = 1
        for j, xj in enumerate(xs_mod):
            if i == j:
                continue
            basis = _poly_mul(basis, [(-xj) % p, 1], p)
            denominator = denominator * (xi - xj) % p
        inverse = pow(denominator, p - 2, p)
        result = _poly_add(
            result, _poly_scale(basis, int(yi) * inverse, p), p
        )
    return _trim(result, p)


def canonical_hadamard_bit(value: int, coordinate: int) -> int:
    """Hadamard bit <binary(value), coordinate> over F_2."""
    return ((int(value) & int(coordinate)).bit_count() & 1)


def su05_eq7_univariate_output(
    coefficients: Sequence[int],
    p: int,
    primitive_root: int,
    seed_v: int,
    code_coordinate: int,
    output_bits: int,
) -> list[int]:
    """SU05 Eq.(7) at d=1 followed by one Hadamard code coordinate.

    The q-ary orbit is f(alpha^i v), i=1,...,m.  The same Hadamard
    coordinate is applied to every q-ary output symbol, exactly as in the
    binary conversion of SU05 Lemma 4.16.
    """
    return [
        canonical_hadamard_bit(
            poly_eval(
                coefficients,
                (pow(primitive_root, i, p) * seed_v) % p,
                p,
            ),
            code_coordinate,
        )
        for i in range(1, output_bits + 1)
    ]


def quadratic_feature_mask(bits: Sequence[int]) -> int:
    """Pack (1, g_i, g_i g_j) into one integer row over F_2."""
    pos = 0
    row = 1
    pos += 1
    for bit in bits:
        if bit:
            row |= 1 << pos
        pos += 1
    for i in range(len(bits)):
        for j in range(i + 1, len(bits)):
            if bits[i] and bits[j]:
                row |= 1 << pos
            pos += 1
    return row


def degree_two_separating_rows(m: int) -> list[list[int]]:
    """Return 0, e_i, and e_i+e_j.

    Their degree<=2 Boolean feature rows form a square nonsingular matrix.
    """
    rows: list[list[int]] = [[0] * m]
    for i in range(m):
        rows.append([int(j == i) for j in range(m)])
    for i in range(m):
        for j in range(i + 1, m):
            rows.append([int(k == i or k == j) for k in range(m)])
    return rows


def construct_maximal_orbit_minor(m: int, p: int) -> dict[str, object]:
    """Construct an exact maximal quadratic-feature minor.

    Let M = 1+m+binom(m,2).  We choose M disjoint length-m windows on one
    multiplicative orbit and interpolate a polynomial whose Hadamard
    coordinate j=1 realizes, window-by-window, 0, e_i, and e_i+e_j.
    Hence the M degree<=2 feature rows are independent.

    This is an exact finite certificate for the SU05 Eq.(7) natural seed
    domain.  To fit a degree bound Delta one additionally needs
    Delta >= M*m-1.
    """
    if m < 1:
        raise ValueError("m must be positive")
    alpha = primitive_root_prime(p)
    rows = degree_two_separating_rows(m)
    feature_count = len(rows)
    stride = m + 1
    if p - 1 < feature_count * stride:
        raise ValueError("p is too small for disjoint orbit windows")

    xs: list[int] = []
    ys: list[int] = []
    for r, target in enumerate(rows):
        seed_v = pow(alpha, r * stride, p)
        for i, bit in enumerate(target, start=1):
            xs.append((pow(alpha, i, p) * seed_v) % p)
            ys.append(bit)

    if len(set(xs)) != len(xs):
        raise AssertionError("orbit-window construction unexpectedly collided")

    coefficients = lagrange_interpolate(xs, ys, p)
    feature_rows: list[int] = []
    for r, target in enumerate(rows):
        seed_v = pow(alpha, r * stride, p)
        observed = su05_eq7_univariate_output(
            coefficients, p, alpha, seed_v, 1, m
        )
        if observed != target:
            raise AssertionError("interpolated orbit window mismatch")
        feature_rows.append(quadratic_feature_mask(observed))

    rank = rank_bitvectors(feature_rows)
    coefficient_payload = ",".join(str(x) for x in coefficients).encode()
    return {
        "status": "COMPUTATIONAL",
        "model": "SU05-Eq7-natural-seed-Hadamard-control",
        "m": m,
        "p": p,
        "primitive_root": alpha,
        "feature_count": feature_count,
        "query_points": len(xs),
        "polynomial_degree": len(coefficients) - 1,
        "rank": rank,
        "is_maximal_rank": rank == feature_count,
        "coefficient_sha256": hashlib.sha256(coefficient_payload).hexdigest(),
    }


def natural_domain_product_span_rank(
    coefficients: Sequence[int], p: int, output_bits: int
) -> int:
    """Exact rho over all natural field seeds v and Hadamard coordinates j."""
    alpha = primitive_root_prime(p)
    width = (p - 1).bit_length()
    feature_rows: list[int] = []
    for seed_v in range(p):
        values = [
            poly_eval(
                coefficients,
                (pow(alpha, i, p) * seed_v) % p,
                p,
            )
            for i in range(1, output_bits + 1)
        ]
        for code_coordinate in range(1 << width):
            bits = [
                canonical_hadamard_bit(value, code_coordinate)
                for value in values
            ]
            feature_rows.append(quadratic_feature_mask(bits))
    return rank_bitvectors(feature_rows)


def scan_boolean_grid_interpolants(
    p: int, h: int, output_bits: int
) -> dict[str, object]:
    """Exhaustively scan all {0,1}-valued messages on grid 0,...,h-1.

    These are exact univariate low-degree extensions on the grid.  The scan
    uses the natural SU05 field seed and canonical Hadamard projection.
    """
    if h < 1 or h >= p:
        raise ValueError("require 1 <= h < p")
    feature_count = 1 + output_bits + output_bits * (output_bits - 1) // 2
    rank_distribution: Counter[int] = Counter()
    degree_distribution: Counter[int] = Counter()
    all_nonconstant_maximal = True

    for message_mask in range(1 << h):
        values = [(message_mask >> i) & 1 for i in range(h)]
        coefficients = lagrange_interpolate(list(range(h)), values, p)
        degree = len(coefficients) - 1
        rank = natural_domain_product_span_rank(
            coefficients, p, output_bits
        )
        rank_distribution[rank] += 1
        degree_distribution[degree] += 1

        is_constant = message_mask in (0, (1 << h) - 1)
        if not is_constant and rank != feature_count:
            all_nonconstant_maximal = False

    return {
        "status": "COMPUTATIONAL",
        "model": "Boolean-grid-LDE-on-SU05-Eq7-natural-seed-control",
        "p": p,
        "h": h,
        "m": output_bits,
        "feature_count": feature_count,
        "rank_distribution": dict(sorted(rank_distribution.items())),
        "polynomial_degree_distribution": dict(
            sorted(degree_distribution.items())
        ),
        "all_nonconstant_messages_maximal_rank": all_nonconstant_maximal,
    }


def modulo_seed_coordinate_anf_degrees(
    p: int,
    h: int,
    output_bits: int,
    message: Sequence[int],
) -> dict[str, object]:
    """Bit-blast one explicit modulo-p wrapper and return exact ANF degrees.

    This is a stress control only.  It uses width=ceil(log2 p) bits z and
    v=z mod p.  That fixed-width sampler is generally biased and is NOT
    asserted to be the binary sampler underlying vMS Lemma 21.
    """
    if len(message) != h or any(bit not in (0, 1) for bit in message):
        raise ValueError("message must contain h Boolean values")
    coefficients = lagrange_interpolate(list(range(h)), message, p)
    alpha = primitive_root_prime(p)
    width = (p - 1).bit_length()
    source_bits = 2 * width
    table_size = 1 << source_bits
    tables: list[list[int]] = [[] for _ in range(output_bits)]

    for source in range(table_size):
        z = source & ((1 << width) - 1)
        code_coordinate = (source >> width) & ((1 << width) - 1)
        seed_v = z % p
        bits = su05_eq7_univariate_output(
            coefficients,
            p,
            alpha,
            seed_v,
            code_coordinate,
            output_bits,
        )
        for i, bit in enumerate(bits):
            tables[i].append(bit)

    return {
        "status": "COMPUTATIONAL",
        "model": "biased-modulo-p-bit-wrapper-stress-control-not-vMS",
        "p": p,
        "h": h,
        "m": output_bits,
        "source_bits": source_bits,
        "message": list(message),
        "coordinate_anf_degrees": [anf_degree(table) for table in tables],
    }


def default_control_suite() -> dict[str, object]:
    """Run the deterministic control battery used by the LSPV-1 report."""
    maximal_minor_cases = [
        construct_maximal_orbit_minor(m, p)
        for m, p in [
            (2, 17),
            (3, 31),
            (4, 59),
            (5, 101),
            (6, 157),
            (8, 397),
        ]
    ]
    boolean_grid_scans = [
        scan_boolean_grid_interpolants(p, h, m)
        for p, h, m in [
            (7, 4, 4),
            (11, 4, 4),
            (11, 5, 6),
            (13, 5, 6),
            (17, 6, 8),
        ]
    ]
    modulo_seed_anf_controls = [
        modulo_seed_coordinate_anf_degrees(7, 4, 4, [0, 0, 0, 1]),
        modulo_seed_coordinate_anf_degrees(11, 5, 6, [0, 0, 0, 0, 1]),
        modulo_seed_coordinate_anf_degrees(
            17, 6, 8, [0, 0, 0, 0, 0, 1]
        ),
    ]
    return {
        "status": "COMPUTATIONAL",
        "scope_guard": (
            "Exact SU05 Eq.(7) natural-seed controls; no claim that the "
            "odd-prime fixed-bit seed sampler of vMS Lemma 21 has been "
            "recovered."
        ),
        "maximal_minor_cases": maximal_minor_cases,
        "boolean_grid_scans": boolean_grid_scans,
        "modulo_seed_anf_controls": modulo_seed_anf_controls,
    }
