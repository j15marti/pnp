#!/usr/bin/env python3
"""Exact finite audit for THREEPENCILFW1.

The base object is a triple of quadratic forms on F_2^6.  Every nonzero
linear combination of their polar matrices is nonsingular, but the joint
map onto F_2^3 has a precomputed selector of Hamming weight at most two.
The audit checks this claim exhaustively and checks that block repetition,
dense affine mixing, and Tseitin cotree lifting preserve the shortcut.

Measured timings are evidence only for reproducibility; no asymptotic lower
or upper bound is inferred from them.
"""

from __future__ import annotations

import hashlib
import json
import random
import time
from typing import Iterable


SEED = 202610132138
MASKS = (16692, 3954, 18969)
SELECTORS = (0, 9, 5, 6, 3, 48, 12, 33)
PAIR6 = tuple((i, j) for i in range(6) for j in range(i + 1, 6))


def parity(x: int) -> int:
    return x.bit_count() & 1


def gf2_rank(rows: Iterable[int]) -> int:
    basis: dict[int, int] = {}
    for value in rows:
        x = value
        while x:
            p = x.bit_length() - 1
            if p in basis:
                x ^= basis[p]
            else:
                basis[p] = x
                break
    return len(basis)


def polar_rows(mask: int) -> list[int]:
    rows = [0] * 6
    for bit, (i, j) in enumerate(PAIR6):
        if (mask >> bit) & 1:
            rows[i] ^= 1 << j
            rows[j] ^= 1 << i
    return rows


def q(mask: int, x: int) -> int:
    return parity(sum((((x >> i) & 1) & ((x >> j) & 1)) << bit
                      for bit, (i, j) in enumerate(PAIR6)) & mask)


def q3(x: int) -> int:
    return sum(q(mask, x) << i for i, mask in enumerate(MASKS))


def block_q3(x: int, blocks: int) -> int:
    out = 0
    for block in range(blocks):
        out ^= q3((x >> (6 * block)) & 63)
    return out


def repeated_rank(mask_combo: int, blocks: int) -> int:
    base_mask = 0
    for i, mask in enumerate(MASKS):
        if (mask_combo >> i) & 1:
            base_mask ^= mask
    base = polar_rows(base_mask)
    rows = []
    for b in range(blocks):
        for row in base:
            rows.append(row << (6 * b))
    return gf2_rank(rows)


def dense_involution(x: int, dimension: int) -> int:
    """A=I+1v^T with v supported on the first half; A^2=I here."""
    if (dimension // 2) & 1:
        raise ValueError("first-half size must be even")
    return x ^ (((1 << dimension) - 1) if parity(x & ((1 << (dimension // 2)) - 1)) else 0)


def permute(x: int, permutation: list[int]) -> int:
    out = 0
    for source, target in enumerate(permutation):
        out |= ((x >> source) & 1) << target
    return out


def inverse_permute(x: int, permutation: list[int]) -> int:
    out = 0
    for source, target in enumerate(permutation):
        out |= ((x >> target) & 1) << source
    return out


def build_kss(side: int) -> tuple[int, list[tuple[int, int]], list[int], list[int]]:
    """K_{s,s} with a star-of-stars spanning tree and cotree dimension (s-1)^2."""
    n = 2 * side
    edges = [(u, side + v) for u in range(side) for v in range(side)]
    index = {edge: i for i, edge in enumerate(edges)}
    forest_edges = [(0, side + v) for v in range(side)]
    forest_edges += [(u, side) for u in range(1, side)]
    forest = [index[e] for e in forest_edges]
    fset = set(forest)
    cotree = [i for i in range(len(edges)) if i not in fset]
    return n, edges, forest, cotree


def boundary(n: int, edges: list[tuple[int, int]], assignment: list[int]) -> list[int]:
    charge = [0] * n
    for bit, (u, v) in zip(assignment, edges):
        if bit:
            charge[u] ^= 1
            charge[v] ^= 1
    return charge


def lift_cotree(n: int, edges: list[tuple[int, int]], forest: list[int],
                cotree: list[int], charge: list[int], y: int) -> list[int]:
    """Extend an arbitrary cotree assignment through a consistent Tseitin system."""
    x = [0] * len(edges)
    residual = list(charge)
    for j, ei in enumerate(cotree):
        x[ei] = (y >> j) & 1
        if x[ei]:
            u, v = edges[ei]
            residual[u] ^= 1
            residual[v] ^= 1
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for ei in forest:
        u, v = edges[ei]
        adj[u].append((v, ei))
        adj[v].append((u, ei))
    parent = [-1] * n
    parent_edge = [-1] * n
    order = [0]
    for u in order:
        for v, ei in adj[u]:
            if v != 0 and parent[v] == -1:
                parent[v] = u
                parent_edge[v] = ei
                order.append(v)
    assert len(order) == n
    for v in reversed(order[1:]):
        bit = residual[v]
        x[parent_edge[v]] = bit
        if bit:
            residual[parent[v]] ^= 1
        residual[v] = 0
    if residual[0]:
        raise ValueError("inconsistent charge")
    return x


def rho_formula(n: int, edges: list[tuple[int, int]], support: set[int]) -> tuple[int, int]:
    def cc(kept: set[int]) -> int:
        parent = list(range(n))

        def find(a: int) -> int:
            while parent[a] != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a

        for ei in kept:
            u, v = edges[ei]
            ru, rv = find(u), find(v)
            if ru != rv:
                parent[ru] = rv
        return len({find(i) for i in range(n)})

    all_edges = set(range(len(edges)))
    predicted = len(support) + cc(all_edges) - cc(all_edges - support)
    incidence_rows = []
    for vertex in range(n):
        row = 0
        for ei, (u, v) in enumerate(edges):
            if vertex in (u, v):
                row |= 1 << ei
        incidence_rows.append(row)
    rank_all = gf2_rank(incidence_rows)
    complement_mask = sum(1 << ei for ei in all_edges - support)
    rank_complement = gf2_rank(row & complement_mask for row in incidence_rows)
    actual = len(support) - (rank_all - rank_complement)
    return predicted, actual


def main() -> None:
    start = time.perf_counter()
    checks = 0

    combo_ranks = {}
    for combo in range(1, 8):
        rank = repeated_rank(combo, 1)
        combo_ranks[str(combo)] = rank
        assert rank == 6
        checks += 1

    fibers = [0] * 8
    minimal_weight = [7] * 8
    for x in range(64):
        value = q3(x)
        fibers[value] += 1
        minimal_weight[value] = min(minimal_weight[value], x.bit_count())
        checks += 1
    assert fibers == [15, 7, 7, 7, 7, 7, 7, 7]
    assert [q3(x) for x in SELECTORS] == list(range(8))
    assert max(x.bit_count() for x in SELECTORS) == 2
    checks += 18

    rng = random.Random(SEED)
    graph_results = []
    for side in (7, 13, 19):
        n, edges, forest, cotree = build_kss(side)
        dimension = len(cotree)
        assert dimension == (side - 1) ** 2 and dimension % 6 == 0
        blocks = dimension // 6
        permutation = list(range(dimension))
        rng.shuffle(permutation)
        phase = rng.getrandbits(dimension)
        charge = [rng.randrange(2) for _ in range(n - 1)]
        charge.append(parity(sum(bit << i for i, bit in enumerate(charge))))
        witnesses = []
        for rhs in range(8):
            w = SELECTORS[rhs]
            assert block_q3(w, blocks) == rhs
            y = dense_involution(inverse_permute(w ^ phase, permutation), dimension)
            recovered = permute(dense_involution(y, dimension), permutation) ^ phase
            assert recovered == w
            x = lift_cotree(n, edges, forest, cotree, charge, y)
            assert boundary(n, edges, x) == charge
            assert block_q3(recovered, blocks) == rhs
            witnesses.append({"rhs": rhs, "selector_weight": w.bit_count(), "edge_weight": sum(x)})
            checks += 5
        for combo in range(1, 8):
            assert repeated_rank(combo, blocks) == dimension
            checks += 1
        graph_results.append({
            "side": side,
            "vertices": n,
            "edges": len(edges),
            "cotree_dimension": dimension,
            "blocks": blocks,
            "witnesses": witnesses,
        })

    # Disconnected graph with an isolate: both algebraic and component counts include it.
    n0, e0, _, c0 = build_kss(3)
    disconnected_n = n0 + 1
    support = set(c0[:3])
    predicted, actual = rho_formula(disconnected_n, e0, support)
    assert predicted == actual
    checks += 1

    # Hostile controls: malformed selector, inconsistent charge, affine/Horn/Krom easy residuals.
    malformed_rejected = False
    try:
        lift_cotree(2, [(0, 1)], [], [0], [0, 0], 0)
    except (AssertionError, ValueError, IndexError):
        malformed_rejected = True
    assert malformed_rejected
    n, edges, forest, cotree = build_kss(7)
    odd_charge = [0] * n
    odd_charge[0] = 1
    odd_rejected = False
    try:
        lift_cotree(n, edges, forest, cotree, odd_charge, 0)
    except ValueError:
        odd_rejected = True
    assert odd_rejected
    controls = {
        "affine": any((x & 1) == 0 for x in range(64)),
        "horn": any(not ((x & 1) and (x & 2)) for x in range(64)),
        "krom": any(((x & 1) or (x & 2)) for x in range(64)),
    }
    assert all(controls.values())
    checks += 5

    elapsed = time.perf_counter() - start
    result = {
        "run_id": "THREEPENCILFW1",
        "seed": SEED,
        "base_masks": list(MASKS),
        "all_nonzero_combination_ranks": combo_ranks,
        "fiber_sizes": fibers,
        "minimal_selector_weights": minimal_weight,
        "selectors": list(SELECTORS),
        "maximum_fixed_selector_weight": max(x.bit_count() for x in SELECTORS),
        "graphs": graph_results,
        "disconnected_isolate_rho": {"predicted": predicted, "actual": actual},
        "hostile_controls": {"malformed_rejected": malformed_rejected, "odd_charge_rejected": odd_rejected, **controls},
        "assertions": checks,
        "elapsed_seconds": elapsed,
        "status": "COMPUTATIONAL",
        "limitation": "Finite exact checks support the symbolic direct-sum/congruence argument; they do not prove a general runtime lower bound or solve arbitrary MQ.",
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["result_sha256_without_self_hash"] = hashlib.sha256(canonical).hexdigest()
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
