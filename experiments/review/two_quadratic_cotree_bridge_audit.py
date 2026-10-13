#!/usr/bin/env python3
"""TWOQCOLLAPSE1: audit two translated quadratic residual equations.

All arithmetic is over GF(2).  The canonical family uses K_{s,s}, its
deterministic star-of-stars spanning tree, free cotree coordinates y, and
two equations q(Ay+r)=b0 and q(Ay+r+e0)=b1.  Their difference fixes z_1
(zero-based coordinate 1), so an explicit selector plus a tree lift finds a
full witness.  This is a bounded audit of an exact upper-bound lemma, not an
asymptotic lower-bound experiment.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import random
import time

SEED = 202610132101
DEADLINE_SECONDS = 25.0


def parity(x: int) -> int:
    return x.bit_count() & 1


def mat_vec(rows: list[int], vector: int) -> int:
    return sum(parity(row & vector) << i for i, row in enumerate(rows))


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


def transpose(rows: list[int], d: int) -> list[int]:
    return [sum(((rows[i] >> j) & 1) << i for i in range(d)) for j in range(d)]


def multiply(left: list[int], right: list[int]) -> list[int]:
    out: list[int] = []
    for row in left:
        value = 0
        mask = row
        while mask:
            bit = (mask & -mask).bit_length() - 1
            value ^= right[bit]
            mask &= mask - 1
        out.append(value)
    return out


def structured_dense_involution(d: int) -> list[int]:
    """A=I+u v^T, with u all ones and v supported on the first half."""
    if d < 4 or d % 4:
        raise ValueError("dimension must be a positive multiple of four")
    v = (1 << (d // 2)) - 1
    return [(1 << i) ^ v for i in range(d)]


def paired_q(z: int, d: int) -> int:
    if d <= 0 or d % 2:
        raise ValueError("positive even dimension required")
    return sum(((z >> i) & 1) & ((z >> (i + 1)) & 1) for i in range(0, d, 2)) & 1


def j_rows(d: int) -> list[int]:
    return [1 << (i ^ 1) for i in range(d)]


def congruent_polar(a_rows: list[int]) -> list[int]:
    d = len(a_rows)
    return multiply(transpose(a_rows, d), multiply(j_rows(d), a_rows))


def select_z(d: int, b0: int, b1: int) -> int:
    """Solve q(z)=b0 and q(z+e0)=b1 for d>=4."""
    if d < 4 or d % 2 or b0 not in (0, 1) or b1 not in (0, 1):
        raise ValueError("valid d>=4 even and Boolean right sides required")
    delta = b0 ^ b1  # q(z+e0)+q(z)=z_1
    if delta:
        return (b0 << 0) | (1 << 1)
    if b0 == 0:
        return 0
    return (1 << 2) | (1 << 3)


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
    if len(charge) != n or any(bit not in (0, 1) for bit in charge) or (sum(charge) & 1):
        raise ValueError("charge must be a consistent n-bit vector")
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
        raise AssertionError("consistent root charge was not discharged")
    return x


def decode_record(payload: str) -> dict:
    record = json.loads(payload)
    expected = {"side", "charge", "phase", "b0", "b1", "transform", "shift"}
    if set(record) != expected:
        raise ValueError("record keys are not canonical")
    side = record["side"]
    if not isinstance(side, int) or isinstance(side, bool) or side < 3 or side % 2 == 0:
        raise ValueError("side must be odd and at least three")
    n, _, _, cotree = k_bipartite(side)
    d = len(cotree)
    if d % 4:
        raise ValueError("cotree dimension must be a multiple of four")
    charge = record["charge"]
    phase = record["phase"]
    if not isinstance(charge, list) or len(charge) != n or any(type(x) is not int or x not in (0, 1) for x in charge):
        raise ValueError("malformed charge")
    if sum(charge) & 1:
        raise ValueError("inconsistent charge")
    if not isinstance(phase, str) or len(phase) != d or any(x not in "01" for x in phase):
        raise ValueError("malformed phase")
    if type(record["b0"]) is not int or record["b0"] not in (0, 1) or type(record["b1"]) is not int or record["b1"] not in (0, 1):
        raise ValueError("right sides must be bits")
    if record["transform"] != "rank_one_half" or record["shift"] != "e0":
        raise ValueError("unknown transform or shift tag")
    record["phase_int"] = int(phase[::-1], 2)
    return record


def encode_record(side: int, charge: list[int], phase: int, b0: int, b1: int) -> str:
    d = (side - 1) ** 2
    return json.dumps({
        "side": side,
        "charge": charge,
        "phase": format(phase, f"0{d}b")[::-1],
        "b0": b0,
        "b1": b1,
        "transform": "rank_one_half",
        "shift": "e0",
    }, sort_keys=True, separators=(",", ":"))


@dataclass
class Counters:
    assertions: int = 0
    exhaustive_residual_assignments: int = 0
    witness_reconstructions: int = 0
    particular_solution_checks: int = 0
    kernel_basis_vector_checks: int = 0
    affine_decomposition_checks: int = 0
    malformed_rejections: int = 0
    no_controls: int = 0
    encoded_bytes: int = 0

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

    # Exhaust the canonical residual at d=4 for all phases and right sides.
    d = 4
    a_rows = structured_dense_involution(d)
    for phase in range(1 << d):
        for b0 in (0, 1):
            for b1 in (0, 1):
                solutions = []
                for y in range(1 << d):
                    z = mat_vec(a_rows, y) ^ phase
                    ok = paired_q(z, d) == b0 and paired_q(z ^ 1, d) == b1
                    if ok:
                        solutions.append(y)
                    c.exhaustive_residual_assignments += 1
                z_star = select_z(d, b0, b1)
                y_star = mat_vec(a_rows, z_star ^ phase)  # A=A^{-1}
                c.check(y_star in solutions)
                c.check(paired_q(z_star, d) == b0)
                c.check(paired_q(z_star ^ 1, d) == b1)
    # The omitted d=2 case exposes the exact dimension boundary.
    d2_solutions = [z for z in range(4) if paired_q(z, 2) == 1 and paired_q(z ^ 1, 2) == 1]
    c.check(d2_solutions == [])
    c.no_controls += 1

    for side in (3, 5, 7, 9, 17):
        n, edges, forest, cotree = k_bipartite(side)
        d = len(cotree)
        a_rows = structured_dense_involution(d)
        c.check(multiply(a_rows, a_rows) == [1 << i for i in range(d)])
        polar = congruent_polar(a_rows)
        c.check(gf2_rank(polar, d) == d)
        density = sum(row.bit_count() for row in polar) / (d * (d - 1))

        charge = [rng.randrange(2) for _ in range(n)]
        charge[-1] = sum(charge[:-1]) & 1
        phase = rng.randrange(1 << d)
        payload = encode_record(side, charge, phase, rng.randrange(2), rng.randrange(2))
        record = decode_record(payload)
        c.encoded_bytes += len(payload.encode())
        c.check(record["phase_int"] == phase)

        # Compute a and every column of L explicitly, as requested by the bridge.
        a_edge = lift_cotree(n, edges, forest, cotree, charge, 0)
        c.check(boundary(n, edges, a_edge) == charge)
        c.particular_solution_checks += 1
        basis: list[list[int]] = []
        zero_charge = [0] * n
        for j in range(d):
            column = lift_cotree(n, edges, forest, cotree, zero_charge, 1 << j)
            basis.append(column)
            c.check(boundary(n, edges, column) == zero_charge)
            projection = sum(column[edge_index] << k for k, edge_index in enumerate(cotree))
            c.check(projection == (1 << j))
            c.kernel_basis_vector_checks += 1

        for _ in range(10):
            b0, b1 = rng.randrange(2), rng.randrange(2)
            z_star = select_z(d, b0, b1)
            c.check(paired_q(z_star, d) == b0)
            c.check(paired_q(z_star ^ 1, d) == b1)
            y_star = mat_vec(a_rows, z_star ^ phase)
            x_direct = lift_cotree(n, edges, forest, cotree, charge, y_star)
            x_affine = list(a_edge)
            for j in range(d):
                if (y_star >> j) & 1:
                    x_affine = [u ^ v for u, v in zip(x_affine, basis[j])]
            c.check(x_affine == x_direct)
            c.check(boundary(n, edges, x_direct) == charge)
            recovered = sum(x_direct[edge_index] << j for j, edge_index in enumerate(cotree))
            c.check(recovered == y_star)
            z_recovered = mat_vec(a_rows, recovered) ^ phase
            c.check(paired_q(z_recovered, d) == b0)
            c.check(paired_q(z_recovered ^ 1, d) == b1)
            c.witness_reconstructions += 1
            c.affine_decomposition_checks += 1

        rows_out.append({
            "graph": f"K_{{{side},{side}}}",
            "vertices": n,
            "edges": len(edges),
            "cotree_dimension": d,
            "projected_rank": d,
            "polar_rank_equation_0": d,
            "polar_rank_equation_1": d,
            "polar_matrices_identical": True,
            "polar_offdiagonal_density": density,
            "explicit_kernel_basis_bits": d * len(edges),
            "encoded_record_bytes": len(payload.encode()),
        })
        deadline()

    # Malformed/off-image controls.  Every mutation must reject.
    base = json.loads(encode_record(3, [0] * 6, 0, 0, 1))
    mutations = []
    for key, value in [
        ("side", 4), ("charge", [0] * 5), ("charge", [1, 0, 0, 0, 0, 0]),
        ("phase", "0"), ("phase", "000x"), ("b0", 2),
        ("transform", "dense_table"), ("shift", "zero")]:
        item = dict(base)
        item[key] = value
        mutations.append(item)
    extra = dict(base)
    extra["advice"] = 1
    mutations.append(extra)
    for item in mutations:
        try:
            decode_record(json.dumps(item))
        except ValueError:
            c.malformed_rejections += 1
            c.assertions += 1
        else:
            raise AssertionError("malformed record accepted")

    elapsed = time.monotonic() - start
    deadline()
    semantic = {
        "claim": "two shared-variable dense full-rank quadratic phase translates can collapse to one quadratic equation plus one linear coordinate condition",
        "status": "COMPUTATIONAL checks supporting an exact symbolic upper-bound lemma; independent review pending",
        "difference_identity": "q(z XOR e0) XOR q(z) = z_1",
        "selector": "delta=b0 XOR b1; if delta=1 use z=(b0,1,0,...); if delta=0=b0 use z=0; if delta=0 and b0=1 use z=(0,0,1,1,0,...)",
        "counters": asdict(c),
        "family_rows": rows_out,
    }
    digest = hashlib.sha256(json.dumps(semantic, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return {
        "run_id": "TWOQCOLLAPSE1",
        "seed": SEED,
        "elapsed_seconds": round(elapsed, 6),
        "deadline_seconds": DEADLINE_SECONDS,
        "semantic_digest_sha256": digest,
        "semantic": semantic,
        "limitations": [
            "Finite checks do not prove an asymptotic lower bound.",
            "The exact lemma concerns two translates with the same polar form, not two genuinely independent polar forms.",
            "The family is an explicit polynomial-time upper-bound counterexample to a structural necessity claim, not an algorithm for arbitrary nonlinear residual systems.",
            "Materializing L costs O(d|E|) bits but is polynomial; the witness finder can stream/directly lift and need not materialize L.",
            "The family record is recognized exactly; malformed, inconsistent-charge, and off-image strings are rejected.",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
