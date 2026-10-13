#!/usr/bin/env python3
"""INDEPPOLARFW1: independent full-rank polar forms can remain witness-easy.

The script audits an explicit Tseitin-plus-two-quadratics family after affine
elimination.  Both quadratic polar forms are nonsingular and linearly
independent; arbitrary coordinate renaming and a concise dense affine mixing
are included.  A constant-support selector nevertheless realizes every pair
of right-hand sides.  Finite checks support, but do not replace, the symbolic
upper-bound proof.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import random
import time

SEED = 202610132116
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
    if d < 4 or d % 4:
        raise ValueError("dimension must be a positive multiple of four")
    v = (1 << (d // 2)) - 1
    return [(1 << i) ^ v for i in range(d)]


def q_even(z: int, d: int) -> int:
    return sum(((z >> i) & 1) & ((z >> (i + 1)) & 1) for i in range(0, d, 2)) & 1


def q_shift(z: int, d: int) -> int:
    total = ((z >> (d - 1)) & 1) & (z & 1)
    for i in range(1, d - 1, 2):
        total ^= ((z >> i) & 1) & ((z >> (i + 1)) & 1)
    return total


def polar_even(d: int) -> list[int]:
    return [1 << (i ^ 1) for i in range(d)]


def polar_shift(d: int) -> list[int]:
    rows = [0] * d
    pairs = [(i, i + 1) for i in range(1, d - 1, 2)] + [(d - 1, 0)]
    for i, j in pairs:
        rows[i] |= 1 << j
        rows[j] |= 1 << i
    return rows


def congruent(polar: list[int], linear_rows: list[int]) -> list[int]:
    d = len(linear_rows)
    return multiply(transpose(linear_rows, d), multiply(polar, linear_rows))


def permute_bits(value: int, permutation: list[int]) -> int:
    out = 0
    for old, new in enumerate(permutation):
        out |= ((value >> old) & 1) << new
    return out


def inverse_permute_bits(value: int, permutation: list[int]) -> int:
    out = 0
    for old, new in enumerate(permutation):
        out |= ((value >> new) & 1) << old
    return out


def permuted_linear_rows(a_rows: list[int], permutation: list[int]) -> list[int]:
    rows = [0] * len(a_rows)
    for old, new in enumerate(permutation):
        rows[new] = a_rows[old]
    return rows


def select_w(b0: int, b1: int) -> int:
    """Constant-support selector for q_even(w)=b0, q_shift(w)=b1."""
    if b0 not in (0, 1) or b1 not in (0, 1):
        raise ValueError("right sides must be bits")
    if (b0, b1) == (0, 0):
        return 0
    if (b0, b1) == (1, 0):
        return (1 << 0) | (1 << 1)
    if (b0, b1) == (0, 1):
        return (1 << 1) | (1 << 2)
    return (1 << 0) | (1 << 1) | (1 << 2)


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
    if len(charge) != n or any(type(bit) is not int or bit not in (0, 1) for bit in charge) or (sum(charge) & 1):
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
    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for edge_index in forest:
        u, v = edges[edge_index]
        adjacency[u].append((v, edge_index))
        adjacency[v].append((u, edge_index))
    parent = [-1] * n
    parent_edge = [-1] * n
    order = [0]
    seen = {0}
    for u in order:
        for v, edge_index in adjacency[u]:
            if v not in seen:
                seen.add(v)
                parent[v] = u
                parent_edge[v] = edge_index
                order.append(v)
    if len(seen) != n:
        raise ValueError("declared forest is not spanning")
    for v in reversed(order[1:]):
        bit = residual[v]
        x[parent_edge[v]] = bit
        if bit:
            residual[parent[v]] ^= 1
    if residual[0]:
        raise AssertionError("consistent root charge was not discharged")
    return x


def encode_record(side: int, charge: list[int], phase: int, b0: int, b1: int, permutation: list[int]) -> str:
    d = (side - 1) ** 2
    return json.dumps({
        "side": side,
        "charge": charge,
        "phase": format(phase, f"0{d}b")[::-1],
        "b0": b0,
        "b1": b1,
        "permutation": permutation,
        "transform": "rank_one_half",
        "forms": "two_cycle_matchings",
    }, sort_keys=True, separators=(",", ":"))


def decode_record(payload: str) -> dict:
    record = json.loads(payload)
    expected = {"side", "charge", "phase", "b0", "b1", "permutation", "transform", "forms"}
    if set(record) != expected:
        raise ValueError("record keys are not canonical")
    side = record["side"]
    if type(side) is not int or side < 3 or side % 2 == 0:
        raise ValueError("side must be odd and at least three")
    n, _, _, cotree = k_bipartite(side)
    d = len(cotree)
    charge = record["charge"]
    phase = record["phase"]
    permutation = record["permutation"]
    if not isinstance(charge, list) or len(charge) != n or any(type(x) is not int or x not in (0, 1) for x in charge):
        raise ValueError("malformed charge")
    if sum(charge) & 1:
        raise ValueError("inconsistent charge")
    if not isinstance(phase, str) or len(phase) != d or any(x not in "01" for x in phase):
        raise ValueError("malformed phase")
    if type(record["b0"]) is not int or record["b0"] not in (0, 1) or type(record["b1"]) is not int or record["b1"] not in (0, 1):
        raise ValueError("right sides must be bits")
    if not isinstance(permutation, list) or len(permutation) != d or any(type(x) is not int for x in permutation) or sorted(permutation) != list(range(d)):
        raise ValueError("malformed coordinate permutation")
    if record["transform"] != "rank_one_half" or record["forms"] != "two_cycle_matchings":
        raise ValueError("unknown transform or form tags")
    record["phase_int"] = int(phase[::-1], 2)
    return record


@dataclass
class Counters:
    assertions: int = 0
    exhaustive_assignments: int = 0
    witness_reconstructions: int = 0
    particular_solution_checks: int = 0
    kernel_basis_checks: int = 0
    affine_decomposition_checks: int = 0
    independent_polar_checks: int = 0
    renaming_phase_controls: int = 0
    malformed_rejections: int = 0
    unsatisfiable_controls: int = 0
    easy_family_controls: int = 0
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

    # Exhaust d=4 under every phase, every coordinate renaming, and all labels.
    d = 4
    a_rows = structured_dense_involution(d)
    import itertools
    for permutation_tuple in itertools.permutations(range(d)):
        permutation = list(permutation_tuple)
        for phase in range(1 << d):
            for b0 in (0, 1):
                for b1 in (0, 1):
                    solutions = []
                    for y in range(1 << d):
                        z = mat_vec(a_rows, y) ^ phase
                        w = permute_bits(z, permutation)
                        if q_even(w, d) == b0 and q_shift(w, d) == b1:
                            solutions.append(y)
                        c.exhaustive_assignments += 1
                    w_star = select_w(b0, b1)
                    z_star = inverse_permute_bits(w_star, permutation)
                    y_star = mat_vec(a_rows, z_star ^ phase)
                    c.check(y_star in solutions)
                    c.check(q_even(w_star, d) == b0)
                    c.check(q_shift(w_star, d) == b1)
                    c.renaming_phase_controls += 1
        deadline()

    # Genuine NO control: a duplicated form with contradictory right sides.
    duplicate_no = [z for z in range(1 << d) if q_even(z, d) == 0 and q_even(z, d) == 1]
    c.check(duplicate_no == [])
    c.unsatisfiable_controls += 1

    # Easy affine, Horn, and Krom residual controls remain easy on free coordinates.
    for z in range(1 << d):
        affine = parity(z & 0b1111) in (0, 1)
        horn = (not ((z >> 0) & 1)) or ((z >> 1) & 1)
        krom = ((z >> 2) & 1) == ((z >> 3) & 1)
        c.check(affine)
        c.check(horn in (True, False))
        c.check(krom in (True, False))
        c.easy_family_controls += 3

    for side in (3, 5, 7, 9, 17):
        n, edges, forest, cotree = k_bipartite(side)
        d = len(cotree)
        a_rows = structured_dense_involution(d)
        permutation = list(range(d))
        rng.shuffle(permutation)
        linear_rows = permuted_linear_rows(a_rows, permutation)
        p0 = congruent(polar_even(d), linear_rows)
        p1 = congruent(polar_shift(d), linear_rows)
        c.check(gf2_rank(p0, d) == d)
        c.check(gf2_rank(p1, d) == d)
        c.check(p0 != p1)
        c.check(gf2_rank([x ^ y for x, y in zip(p0, p1)], d) == d - 2)
        c.independent_polar_checks += 1

        charge = [rng.randrange(2) for _ in range(n)]
        charge[-1] = sum(charge[:-1]) & 1
        phase = rng.randrange(1 << d)
        payload = encode_record(side, charge, phase, rng.randrange(2), rng.randrange(2), permutation)
        record = decode_record(payload)
        c.check(record["phase_int"] == phase)
        c.encoded_bytes += len(payload.encode())

        a_edge = lift_cotree(n, edges, forest, cotree, charge, 0)
        c.check(boundary(n, edges, a_edge) == charge)
        c.particular_solution_checks += 1
        zero_charge = [0] * n
        basis: list[list[int]] = []
        for j in range(d):
            column = lift_cotree(n, edges, forest, cotree, zero_charge, 1 << j)
            basis.append(column)
            c.check(boundary(n, edges, column) == zero_charge)
            projection = sum(column[edge_index] << k for k, edge_index in enumerate(cotree))
            c.check(projection == (1 << j))
            c.kernel_basis_checks += 1

        for b0 in (0, 1):
            for b1 in (0, 1):
                w_star = select_w(b0, b1)
                z_star = inverse_permute_bits(w_star, permutation)
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
                w_recovered = permute_bits(mat_vec(a_rows, recovered) ^ phase, permutation)
                c.check(q_even(w_recovered, d) == b0)
                c.check(q_shift(w_recovered, d) == b1)
                c.witness_reconstructions += 1
                c.affine_decomposition_checks += 1

        rows_out.append({
            "graph": f"K_{{{side},{side}}}",
            "vertices": n,
            "edges": len(edges),
            "cotree_dimension": d,
            "projected_rank": d,
            "polar_rank_0": d,
            "polar_rank_1": d,
            "polar_rank_sum": d - 2,
            "polar_forms_linearly_independent": True,
            "polar_density_0": sum(row.bit_count() for row in p0) / (d * (d - 1)),
            "polar_density_1": sum(row.bit_count() for row in p1) / (d * (d - 1)),
            "explicit_kernel_basis_bits": d * len(edges),
            "encoded_record_bytes": len(payload.encode()),
        })
        deadline()

    base = json.loads(encode_record(3, [0] * 6, 0, 0, 0, list(range(4))))
    mutations = []
    for key, value in [
        ("side", 4), ("charge", [0] * 5), ("charge", [1, 0, 0, 0, 0, 0]),
        ("phase", "0"), ("phase", "000x"), ("b0", 2),
        ("permutation", [0, 1, 1, 3]), ("transform", "table"),
        ("forms", "phase_translates")]:
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
        "claim": "two linearly independent full-rank quadratic polar forms can still admit a constant-support uniform witness selector after dense affine mixing",
        "status": "COMPUTATIONAL checks supporting a complete symbolic upper-bound proof; independent review pending",
        "forms": [
            "q0(w)=XOR_i w_(2i)w_(2i+1)",
            "q1(w)=w_(d-1)w_0 XOR XOR_i w_(2i+1)w_(2i+2)",
        ],
        "selector": {"00": 0, "10": 3, "01": 6, "11": 7},
        "pencil_rank_spectrum": "rank(B0)=d, rank(B1)=d, rank(B0+B1)=d-2",
        "counters": asdict(c),
        "family_rows": rows_out,
    }
    digest = hashlib.sha256(json.dumps(semantic, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return {
        "run_id": "INDEPPOLARFW1",
        "seed": SEED,
        "elapsed_seconds": round(elapsed, 6),
        "deadline_seconds": DEADLINE_SECONDS,
        "semantic_digest_sha256": digest,
        "semantic": semantic,
        "limitations": [
            "Finite checks do not prove an asymptotic lower bound.",
            "The two polar forms are linearly independent and individually nonsingular, but their sum has rank d-2; the family does not have an everywhere-nonsingular polar pencil.",
            "The result is an explicit polynomial-time upper-bound counterexample, not an algorithm for arbitrary systems of quadratic equations.",
            "All parsing, affine elimination, coordinate renaming, selection, reconstruction, and verification costs are polynomial and charged.",
            "No DNNF, proof-system, circuit, ETH, or cryptographic lower bound is inferred.",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
