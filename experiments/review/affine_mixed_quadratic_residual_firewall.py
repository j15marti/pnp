#!/usr/bin/env python3
"""AFFINEMIXQFW1: dense affine mixing does not make an easy quadratic residual hard.

All arithmetic is over GF(2).  The script checks the exact symbolic construction
q(Ay+r)=b on free cotree coordinates of a Tseitin system and reconstructs full
edge witnesses by a spanning-tree pass.  It is a bounded audit, not an
asymptotic lower-bound experiment.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import random
import time

SEED = 202610132048
DEADLINE_SECONDS = 25.0


def parity(x: int) -> int:
    return x.bit_count() & 1


def mat_vec(rows: list[int], vector: int) -> int:
    out = 0
    for i, row in enumerate(rows):
        out |= parity(row & vector) << i
    return out


def gf2_rank(rows: list[int], width: int) -> int:
    work = list(rows)
    rank = 0
    for col in range(width):
        pivot = next((i for i in range(rank, len(work)) if (work[i] >> col) & 1), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        for i in range(len(work)):
            if i != rank and ((work[i] >> col) & 1):
                work[i] ^= work[rank]
        rank += 1
    return rank


def solve_square(rows: list[int], rhs: int) -> int:
    """Solve A x = rhs for an invertible square bit matrix."""
    d = len(rows)
    aug = [rows[i] | (((rhs >> i) & 1) << d) for i in range(d)]
    for col in range(d):
        pivot = next((i for i in range(col, d) if (aug[i] >> col) & 1), None)
        if pivot is None:
            raise ValueError("singular matrix")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        for i in range(d):
            if i != col and ((aug[i] >> col) & 1):
                aug[i] ^= aug[col]
    return sum(((aug[i] >> d) & 1) << i for i in range(d))


def random_invertible(d: int, rng: random.Random) -> list[int]:
    rows = [1 << i for i in range(d)]
    rounds = max(8 * d, 32)
    for _ in range(rounds):
        i = rng.randrange(d)
        j = rng.randrange(d - 1)
        if j >= i:
            j += 1
        if rng.randrange(4) == 0:
            rows[i], rows[j] = rows[j], rows[i]
        else:
            rows[i] ^= rows[j]
    assert gf2_rank(rows, d) == d
    return rows


def structured_dense_involution(d: int) -> list[int]:
    """A=I+u v^T, u=all-ones, v=1 on the first half.

    For d divisible by four, v^T u=0, so A^2=I.  The transform has a
    uniform O(d)-bit description (indeed, just d) although its rows are dense.
    """
    if d <= 0 or d % 4:
        raise ValueError("dimension must be a positive multiple of four")
    v = (1 << (d // 2)) - 1
    return [(1 << i) ^ v for i in range(d)]


def paired_q(z: int, d: int) -> int:
    if d <= 0 or d % 2:
        raise ValueError("positive even dimension required")
    return sum(((z >> i) & 1) & ((z >> (i + 1)) & 1) for i in range(0, d, 2)) & 1


def j_rows(d: int) -> list[int]:
    return [1 << (i ^ 1) for i in range(d)]


def transpose(rows: list[int], d: int) -> list[int]:
    return [sum(((rows[i] >> j) & 1) << i for i in range(d)) for j in range(d)]


def multiply(left: list[int], right: list[int], d: int) -> list[int]:
    # Row i of the product is XOR of right rows selected by left row i.
    out = []
    for row in left:
        value = 0
        mask = row
        while mask:
            bit = (mask & -mask).bit_length() - 1
            value ^= right[bit]
            mask &= mask - 1
        out.append(value)
    return out


def congruent_polar(a_rows: list[int]) -> list[int]:
    d = len(a_rows)
    return multiply(transpose(a_rows, d), multiply(j_rows(d), a_rows, d), d)


def polar_by_queries(a_rows: list[int], phase: int) -> list[int]:
    d = len(a_rows)
    def f(y: int) -> int:
        return paired_q(mat_vec(a_rows, y) ^ phase, d)
    f0 = f(0)
    rows = [0] * d
    for i in range(d):
        ei = 1 << i
        for j in range(d):
            ej = 1 << j
            bit = f(ei ^ ej) ^ f(ei) ^ f(ej) ^ f0
            rows[i] |= bit << j
    return rows


def k_bipartite(side: int) -> tuple[int, list[tuple[int, int]], list[int], list[int]]:
    if side < 3 or side % 2 == 0:
        raise ValueError("odd side at least three required")
    n = 2 * side
    edges: list[tuple[int, int]] = []
    forest: list[int] = []
    cotree: list[int] = []
    for i in range(side):
        for j in range(side):
            idx = len(edges)
            edges.append((i, side + j))
            if i == 0 or (j == 0 and i > 0):
                forest.append(idx)
            else:
                cotree.append(idx)
    return n, edges, forest, cotree


def boundary(n: int, edges: list[tuple[int, int]], x: list[int]) -> list[int]:
    out = [0] * n
    for bit, (u, v) in zip(x, edges):
        if bit:
            out[u] ^= 1
            out[v] ^= 1
    return out


def lift_cotree(n: int, edges: list[tuple[int, int]], forest: list[int], cotree: list[int], charge: list[int], y: int) -> list[int]:
    if sum(charge) & 1:
        raise ValueError("inconsistent charge")
    residual = list(charge)
    x = [0] * len(edges)
    for j, edge_index in enumerate(cotree):
        bit = (y >> j) & 1
        x[edge_index] = bit
        if bit:
            u, v = edges[edge_index]
            residual[u] ^= 1
            residual[v] ^= 1
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for edge_index in forest:
        u, v = edges[edge_index]
        adj[u].append((v, edge_index))
        adj[v].append((u, edge_index))
    parent = [-1] * n
    parent_edge = [-1] * n
    order = [0]
    seen = {0}
    for u in order:
        for v, edge_index in adj[u]:
            if v not in seen:
                seen.add(v)
                parent[v] = u
                parent_edge[v] = edge_index
                order.append(v)
    if len(seen) != n:
        raise ValueError("forest is not spanning")
    for v in reversed(order[1:]):
        bit = residual[v]
        x[parent_edge[v]] = bit
        if bit:
            residual[parent[v]] ^= 1
    if residual[0]:
        raise AssertionError("root charge not discharged")
    return x


@dataclass
class Counters:
    assertions: int = 0
    matrices: int = 0
    exhaustive_assignments: int = 0
    polar_query_checks: int = 0
    witness_reconstructions: int = 0
    renaming_phase_controls: int = 0
    inconsistent_rejections: int = 0
    singular_rejections: int = 0
    parsed_bytes: int = 0

    def check(self, condition: bool) -> None:
        assert condition
        self.assertions += 1


def run() -> dict:
    start = time.monotonic()
    rng = random.Random(SEED)
    c = Counters()
    rows_out = []

    def deadline() -> None:
        if time.monotonic() - start > DEADLINE_SECONDS:
            raise TimeoutError("cooperative deadline exceeded")

    # Exact truth-table and polar-identity checks in small dimensions.
    for d in (2, 4, 6, 8):
        for _ in range(12):
            a = random_invertible(d, rng)
            phase = rng.randrange(1 << d)
            polar = congruent_polar(a)
            queried = polar_by_queries(a, phase)
            c.check(polar == queried)
            c.check(gf2_rank(polar, d) == d)
            c.check(all(((polar[i] >> i) & 1) == 0 for i in range(d)))
            c.matrices += 1
            c.polar_query_checks += d * d
            for y in range(1 << d):
                direct = paired_q(mat_vec(a, y) ^ phase, d)
                c.check(direct in (0, 1))
                c.exhaustive_assignments += 1
            for b in (0, 1):
                z_star = 0 if b == 0 else 3
                y_star = solve_square(a, z_star ^ phase)
                c.check(paired_q(mat_vec(a, y_star) ^ phase, d) == b)
        deadline()

    # Large free-cotree instances, arbitrary consistent charges, phases, and dense mixes.
    for side in (3, 5, 7, 9, 17):
        n, edges, forest, cotree = k_bipartite(side)
        d = len(cotree)
        densities = []
        structured = structured_dense_involution(d)
        c.check(gf2_rank(structured, d) == d)
        c.check(multiply(structured, structured, d) == [1 << i for i in range(d)])
        structured_polar = congruent_polar(structured)
        c.check(gf2_rank(structured_polar, d) == d)
        structured_density = sum(row.bit_count() for row in structured_polar) / (d * (d - 1))
        c.matrices += 1
        for _ in range(8):
            a = random_invertible(d, rng)
            phase = rng.randrange(1 << d)
            polar = congruent_polar(a)
            c.check(gf2_rank(polar, d) == d)
            offdiag = sum(row.bit_count() for row in polar)
            densities.append(offdiag / (d * (d - 1)))
            charge = [rng.randrange(2) for _ in range(n)]
            charge[-1] = sum(charge[:-1]) & 1
            payload = {"side": side, "A": a, "phase": phase, "charge": charge}
            c.parsed_bytes += len(json.dumps(payload, sort_keys=True, separators=(",", ":")))
            for b in (0, 1):
                z_star = 0 if b == 0 else 3
                y_star = solve_square(a, z_star ^ phase)
                x = lift_cotree(n, edges, forest, cotree, charge, y_star)
                c.check(boundary(n, edges, x) == charge)
                recovered = sum(x[edge_index] << j for j, edge_index in enumerate(cotree))
                c.check(recovered == y_star)
                c.check(paired_q(mat_vec(a, recovered) ^ phase, d) == b)
                c.witness_reconstructions += 1
            c.renaming_phase_controls += 1
        # The same reconstruction with the concise deterministic dense transform.
        phase = (1 << d) - 1
        charge = [rng.randrange(2) for _ in range(n)]
        charge[-1] = sum(charge[:-1]) & 1
        for b in (0, 1):
            z_star = 0 if b == 0 else 3
            # A is its own inverse.
            y_star = mat_vec(structured, z_star ^ phase)
            c.check(mat_vec(structured, y_star) == (z_star ^ phase))
            x = lift_cotree(n, edges, forest, cotree, charge, y_star)
            c.check(boundary(n, edges, x) == charge)
            recovered = sum(x[edge_index] << j for j, edge_index in enumerate(cotree))
            c.check(paired_q(mat_vec(structured, recovered) ^ phase, d) == b)
            c.witness_reconstructions += 1
        rows_out.append({
            "graph": f"K_{{{side},{side}}}",
            "vertices": n,
            "edges": len(edges),
            "cotree_dimension": d,
            "projected_rank": d,
            "polar_rank": d,
            "minimum_polar_offdiagonal_density": min(densities),
            "maximum_polar_offdiagonal_density": max(densities),
            "structured_polar_offdiagonal_density": structured_density,
            "structured_transform": "A=I+u v^T, u=all ones, v=first-half indicator; A^2=I",
            "structured_compact_gate_upper_bound": 3 * d,
            "compact_gate_upper_bound": d * d + d,
        })
        deadline()

    # Invalid controls.
    a = random_invertible(16, rng)
    singular = list(a)
    singular[-1] = singular[0]
    try:
        solve_square(singular, 0)
    except ValueError:
        c.singular_rejections += 1
        c.assertions += 1
    else:
        raise AssertionError("singular matrix accepted")
    n, edges, forest, cotree = k_bipartite(3)
    bad_charge = [0] * n
    bad_charge[0] = 1
    try:
        lift_cotree(n, edges, forest, cotree, bad_charge, 0)
    except ValueError:
        c.inconsistent_rejections += 1
        c.assertions += 1
    else:
        raise AssertionError("inconsistent charge accepted")

    elapsed = time.monotonic() - start
    deadline()
    semantic = {
        "claim": "dense invertible affine mixing preserves an explicit polynomial witness algorithm despite maximal projected and polar ranks",
        "status": "COMPUTATIONAL checks supporting a PROVED/EXACT symbolic firewall",
        "witness_rule": "choose z=0 for b=0 or z=e0+e1 for b=1; solve Ay=z+phase; lift cotree coordinates through the spanning tree",
        "counters": asdict(c),
        "family_rows": rows_out,
    }
    digest = hashlib.sha256(json.dumps(semantic, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return {
        "run_id": "AFFINEMIXQFW1",
        "seed": SEED,
        "elapsed_seconds": round(elapsed, 6),
        "deadline_seconds": DEADLINE_SECONDS,
        "semantic_digest_sha256": digest,
        "semantic": semantic,
        "limitations": [
            "Finite tests do not prove an asymptotic lower bound.",
            "The exact firewall concerns one affine-equivalence class of quadratic residuals, not arbitrary systems of quadratic equations or arbitrary nonlinear Q.",
            "The matrix A, phase, graph, charges, and spanning forest are explicit input data and all parsing, solving, and lifting costs are charged polynomially.",
            "Dense expanded ANF syntax is not a general-computation lower bound.",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
