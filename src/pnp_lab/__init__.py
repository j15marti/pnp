"""Reusable exact-computation utilities for the P vs NP research lab."""

from .gf2 import dependent_subset, rank_bitvectors
from .boolean import (
    anf_degree,
    coordinate_truth_tables,
    quadratic_product_span_rank,
    sparse_quadratic_relation,
)

__all__ = [
    "rank_bitvectors",
    "dependent_subset",
    "anf_degree",
    "coordinate_truth_tables",
    "quadratic_product_span_rank",
    "sparse_quadratic_relation",
]
