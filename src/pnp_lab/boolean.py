"""Exact Boolean-function utilities for small-source experiments."""

from __future__ import annotations

from collections.abc import Callable, Sequence

from .gf2 import dependent_subset, rank_bitvectors


def truth_values_to_mask(values: Sequence[int]) -> int:
    mask = 0
    for i, value in enumerate(values):
        if value not in (0, 1, False, True):
            raise ValueError("truth values must be Boolean")
        if int(value):
            mask |= 1 << i
    return mask


def mask_to_truth_values(mask: int, size: int) -> list[int]:
    return [(mask >> i) & 1 for i in range(size)]


def mobius_anf(values: Sequence[int]) -> list[int]:
    """Return ANF coefficients from a truth table in binary index order."""
    n = len(values)
    if n == 0 or n & (n - 1):
        raise ValueError("truth-table length must be a positive power of two")
    coeffs = [int(v) & 1 for v in values]
    source_bits = n.bit_length() - 1
    for bit in range(source_bits):
        step = 1 << bit
        for mask in range(n):
            if mask & step:
                coeffs[mask] ^= coeffs[mask ^ step]
    return coeffs


def anf_degree(values: Sequence[int]) -> int:
    coeffs = mobius_anf(values)
    active = [mask.bit_count() for mask, c in enumerate(coeffs) if c]
    return max(active, default=-1)


def coordinate_truth_tables(
    encoder: Callable[[int], Sequence[int]],
    source_bits: int,
    output_bits: int,
) -> list[int]:
    """Return coordinate functions g_i as truth-table bitmasks."""
    if source_bits < 0 or output_bits < 0:
        raise ValueError("bit counts must be nonnegative")
    rows = []
    for u in range(1 << source_bits):
        out = list(encoder(u))
        if len(out) != output_bits:
            raise ValueError("encoder returned wrong output length")
        if any(v not in (0, 1, False, True) for v in out):
            raise ValueError("encoder outputs must be Boolean")
        rows.append([int(v) for v in out])

    coords: list[int] = []
    for i in range(output_bits):
        coords.append(truth_values_to_mask([row[i] for row in rows]))
    return coords


def product_feature_vectors(coords: Sequence[int], truth_table_size: int) -> tuple[list[str], list[int]]:
    """Vectors for {1, g_i, g_i g_j} with i<j.

    Squares are omitted because g_i^2=g_i for Boolean functions.
    """
    if truth_table_size <= 0:
        raise ValueError("truth_table_size must be positive")
    labels = ["1"]
    vectors = [(1 << truth_table_size) - 1]

    for i, g in enumerate(coords):
        labels.append(f"g_{i}")
        vectors.append(int(g))

    for i in range(len(coords)):
        for j in range(i + 1, len(coords)):
            labels.append(f"g_{i}g_{j}")
            vectors.append(int(coords[i]) & int(coords[j]))

    return labels, vectors


def quadratic_product_span_rank(coords: Sequence[int], truth_table_size: int) -> int:
    _, vectors = product_feature_vectors(coords, truth_table_size)
    return rank_bitvectors(vectors)


def sparse_quadratic_relation(
    coords: Sequence[int], truth_table_size: int
) -> list[str] | None:
    """Return one exact nonzero degree<=2 relation among output coordinates.

    If labels L are returned, XOR of their feature functions vanishes on every
    enumerated source point. This is a computational certificate for the
    enumerated range only.
    """
    labels, vectors = product_feature_vectors(coords, truth_table_size)
    relation = dependent_subset(vectors)
    if relation is None:
        return None
    return [labels[i] for i in relation]
