"""Small exact GF(2) linear-algebra helpers.

Vectors are represented as nonnegative Python integers; bit k is coordinate k.
This keeps the finite experiments dependency-free and exact.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence


def rank_bitvectors(vectors: Iterable[int]) -> int:
    """Return the GF(2) rank of integer bit-vectors."""
    basis: dict[int, int] = {}
    for value in vectors:
        x = int(value)
        if x < 0:
            raise ValueError("bit-vectors must be nonnegative")
        while x:
            pivot = x.bit_length() - 1
            if pivot in basis:
                x ^= basis[pivot]
            else:
                basis[pivot] = x
                break
    return len(basis)


def dependent_subset(vectors: Sequence[int]) -> list[int] | None:
    """Return indices of a nonempty XOR-zero subset, or None if independent.

    The returned relation is exact over GF(2). It is not guaranteed to be
    minimum weight.
    """
    basis: dict[int, tuple[int, int]] = {}
    for index, value in enumerate(vectors):
        x = int(value)
        if x < 0:
            raise ValueError("bit-vectors must be nonnegative")
        combination = 1 << index
        while x:
            pivot = x.bit_length() - 1
            if pivot in basis:
                bvec, bcomb = basis[pivot]
                x ^= bvec
                combination ^= bcomb
            else:
                basis[pivot] = (x, combination)
                break
        if x == 0:
            return [i for i in range(len(vectors)) if (combination >> i) & 1]
    return None
