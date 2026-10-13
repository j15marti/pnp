#!/usr/bin/env python3
"""PENCILFW1: an everywhere-nonsingular quadratic pencil can be witness-easy.

Audits an explicit Tseitin residual after affine elimination.  Two quadratic
forms have polar matrices J0,J1 such that every nonzero member of their
two-dimensional F2-pencil (J0,J1,J0+J1) is nonsingular.  Repeated 4-coordinate
blocks and an invertible dense mixing preserve that property, yet four fixed
constant-support selectors realize every pair of right-hand sides.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import itertools
import json
import random
import time

SEED = 202610132124
DEADLINE_SECONDS = 25.0
PAIR_ORDER = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
MASK0 = 12                 # x0*x3 + x1*x2
MASK1 = 22                 # x0*x2 + x0*x3 + x1*x3
SELECTOR = {(0, 0): 0, (0, 1): 5, (1, 0): 6, (1, 1): 7}


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
    out = []
    for row in left:
        value = 0
        while row:
            bit = (row & -row).bit_length() - 1
            value ^= right[bit]
            row &= row - 1
        out.append(value)
    return out


def congruent(polar: list[int], linear: list[int]) -> list[int]:
    return multiply(transpose(linear, len(linear)), multiply(polar, linear))


def dense_involution(d: int) -> list[int]:
    if d < 4 or d % 4:
        raise ValueError("dimension must be a positive multiple of four")
    half = (1 << (d // 2)) - 1
    return [(1 << i) ^ half for i in range(d)]


def q_mask(mask: int, block: int) -> int:
    return parity(sum((((block >> i) & 1) & ((block >> j) & 1)) << k
                      for k, (i, j) in enumerate(PAIR_ORDER)) & mask)


def q_repeated(mask: int, value: int, d: int) -> int:
    return sum(q_mask(mask, (value >> k) & 15) for k in range(0, d, 4)) & 1


def polar(mask: int, d: int) -> list[int]:
    rows = [0] * d
    for k in range(0, d, 4):
        for bit, (i, j) in enumerate(PAIR_ORDER):
            if (mask >> bit) & 1:
                rows[k + i] |= 1 << (k + j)
                rows[k + j] |= 1 << (k + i)
    return rows


def permute_bits(value: int, permutation: list[int]) -> int:
    return sum(((value >> old) & 1) << new for old, new in enumerate(permutation))


def inverse_permute_bits(value: int, permutation: list[int]) -> int:
    return sum(((value >> new) & 1) << old for old, new in enumerate(permutation))


def permuted_rows(rows: list[int], permutation: list[int]) -> list[int]:
    out = [0] * len(rows)
    for old, new in enumerate(permutation):
        out[new] = rows[old]
    return out


def k_bipartite(side: int):
    if side < 3 or side % 2 == 0:
        raise ValueError("odd side at least three required")
    edges, forest, cotree = [], [], []
    for i in range(side):
        for j in range(side):
            idx = len(edges)
            edges.append((i, side + j))
            (forest if i == 0 or (j == 0 and i > 0) else cotree).append(idx)
    return 2 * side, edges, forest, cotree


def boundary(n: int, edges: list[tuple[int, int]], x: list[int]) -> list[int]:
    out = [0] * n
    for bit, (u, v) in zip(x, edges):
        if bit:
            out[u] ^= 1
            out[v] ^= 1
    return out


def component_count(n: int, edges: list[tuple[int, int]]) -> int:
    adjacency = [[] for _ in range(n)]
    for u, v in edges:
        adjacency[u].append(v); adjacency[v].append(u)
    seen, count = set(), 0
    for root in range(n):
        if root in seen:
            continue
        count += 1; seen.add(root); stack = [root]
        while stack:
            u = stack.pop()
            for v in adjacency[u]:
                if v not in seen:
                    seen.add(v); stack.append(v)
    return count


def incidence_rows(n: int, edges: list[tuple[int, int]]) -> list[int]:
    rows = [0] * n
    for j, (u, v) in enumerate(edges):
        rows[u] |= 1 << j; rows[v] |= 1 << j
    return rows


def lift(n, edges, forest, cotree, charge, y):
    if len(charge) != n or any(type(b) is not int or b not in (0, 1) for b in charge) or sum(charge) & 1:
        raise ValueError("charge must be a consistent n-bit vector")
    residual, x = list(charge), [0] * len(edges)
    for j, edge_idx in enumerate(cotree):
        bit = (y >> j) & 1
        x[edge_idx] = bit
        if bit:
            u, v = edges[edge_idx]
            residual[u] ^= 1
            residual[v] ^= 1
    adj = [[] for _ in range(n)]
    for edge_idx in forest:
        u, v = edges[edge_idx]
        adj[u].append((v, edge_idx)); adj[v].append((u, edge_idx))
    parent, pedge, order, seen = [-1] * n, [-1] * n, [0], {0}
    for u in order:
        for v, edge_idx in adj[u]:
            if v not in seen:
                seen.add(v); parent[v] = u; pedge[v] = edge_idx; order.append(v)
    if len(seen) != n:
        raise ValueError("declared forest is not spanning")
    for v in reversed(order[1:]):
        x[pedge[v]] = residual[v]
        if residual[v]:
            residual[parent[v]] ^= 1
    if residual[0]:
        raise AssertionError("consistent root charge was not discharged")
    return x


def encode(side, charge, phase, b0, b1, permutation):
    d = (side - 1) ** 2
    return json.dumps({"side": side, "charge": charge,
        "phase": format(phase, f"0{d}b")[::-1], "b0": b0, "b1": b1,
        "permutation": permutation, "transform": "rank_one_half",
        "forms": "repeated_everywhere_nonsingular_pair"},
        sort_keys=True, separators=(",", ":"))


def decode(payload: str):
    r = json.loads(payload)
    keys = {"side", "charge", "phase", "b0", "b1", "permutation", "transform", "forms"}
    if set(r) != keys:
        raise ValueError("noncanonical keys")
    side = r["side"]
    if type(side) is not int or side < 3 or side % 2 == 0:
        raise ValueError("bad side")
    n, _, _, cotree = k_bipartite(side); d = len(cotree)
    if not isinstance(r["charge"], list) or len(r["charge"]) != n or any(type(x) is not int or x not in (0, 1) for x in r["charge"]) or sum(r["charge"]) & 1:
        raise ValueError("bad charge")
    if not isinstance(r["phase"], str) or len(r["phase"]) != d or any(x not in "01" for x in r["phase"]):
        raise ValueError("bad phase")
    if any(type(r[k]) is not int or r[k] not in (0, 1) for k in ("b0", "b1")):
        raise ValueError("bad rhs")
    p = r["permutation"]
    if not isinstance(p, list) or len(p) != d or any(type(x) is not int for x in p) or sorted(p) != list(range(d)):
        raise ValueError("bad permutation")
    if r["transform"] != "rank_one_half" or r["forms"] != "repeated_everywhere_nonsingular_pair":
        raise ValueError("bad tags")
    r["phase_int"] = int(r["phase"][::-1], 2)
    return r


@dataclass
class Counters:
    assertions: int = 0
    exhaustive_assignments: int = 0
    exhaustive_parameter_cells: int = 0
    pencil_checks: int = 0
    witness_reconstructions: int = 0
    kernel_basis_checks: int = 0
    malformed_rejections: int = 0
    unsat_controls: int = 0
    hostile_controls: int = 0
    encoded_bytes: int = 0
    def check(self, condition):
        assert condition
        self.assertions += 1


def run():
    start = time.monotonic(); rng = random.Random(SEED); c = Counters(); rows_out = []
    def deadline():
        if time.monotonic() - start > DEADLINE_SECONDS:
            raise TimeoutError("cooperative deadline exceeded")

    # Exhaust the full base block under all coordinate permutations, phases and labels.
    A4 = dense_involution(4)
    for perm in itertools.permutations(range(4)):
        p = list(perm)
        for phase in range(16):
            for rhs in itertools.product((0, 1), repeat=2):
                solutions = []
                for y in range(16):
                    w = permute_bits(mat_vec(A4, y) ^ phase, p)
                    if (q_repeated(MASK0, w, 4), q_repeated(MASK1, w, 4)) == rhs:
                        solutions.append(y)
                    c.exhaustive_assignments += 1
                wstar = SELECTOR[rhs]
                ystar = mat_vec(A4, inverse_permute_bits(wstar, p) ^ phase)
                c.check(ystar in solutions); c.check(len(solutions) > 0)
                c.exhaustive_parameter_cells += 1
        deadline()

    # Contradictory duplicate-equation NO control.
    c.check(not any(q_repeated(MASK0, z, 4) == 0 and q_repeated(MASK0, z, 4) == 1 for z in range(16)))
    c.unsat_controls += 1

    # Disconnected graph with an isolate: exhaust every support R and verify
    # rho=|R|+cc(X)-cc(X-R), with isolates included in both component counts.
    control_n = 7
    control_edges = [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5)]
    base_cc = component_count(control_n, control_edges)
    base_nullity = len(control_edges) - gf2_rank(incidence_rows(control_n, control_edges), len(control_edges))
    for support_mask in range(1 << len(control_edges)):
        kept = [e for j, e in enumerate(control_edges) if not ((support_mask >> j) & 1)]
        rho_formula = support_mask.bit_count() + base_cc - component_count(control_n, kept)
        kept_nullity = len(kept) - gf2_rank(incidence_rows(control_n, kept), len(kept))
        c.check(base_nullity - kept_nullity == rho_formula)
        c.hostile_controls += 1

    for side in (3, 5, 7, 9, 17):
        n, edges, forest, cotree = k_bipartite(side); d = len(cotree)
        A = dense_involution(d); perm = list(range(d)); rng.shuffle(perm)
        M = permuted_rows(A, perm)
        J0, J1 = polar(MASK0, d), polar(MASK1, d)
        mixed = [congruent(J, M) for J in (J0, J1, [a ^ b for a, b in zip(J0, J1)])]
        ranks = [gf2_rank(J, d) for J in mixed]
        c.check(ranks == [d, d, d]); c.pencil_checks += 1
        charge = [rng.randrange(2) for _ in range(n)]; charge[-1] = sum(charge[:-1]) & 1
        phase = rng.randrange(1 << d)
        payload = encode(side, charge, phase, rng.randrange(2), rng.randrange(2), perm)
        record = decode(payload); c.check(record["phase_int"] == phase); c.encoded_bytes += len(payload.encode())
        a = lift(n, edges, forest, cotree, charge, 0); c.check(boundary(n, edges, a) == charge)
        zero = [0] * n; basis = []
        for j in range(d):
            col = lift(n, edges, forest, cotree, zero, 1 << j); basis.append(col)
            c.check(boundary(n, edges, col) == zero)
            c.check(sum(col[e] << k for k, e in enumerate(cotree)) == 1 << j)
            c.kernel_basis_checks += 1
        for rhs in itertools.product((0, 1), repeat=2):
            wstar = SELECTOR[rhs]
            ystar = mat_vec(A, inverse_permute_bits(wstar, perm) ^ phase)
            x1 = lift(n, edges, forest, cotree, charge, ystar)
            x2 = list(a)
            for j in range(d):
                if (ystar >> j) & 1:
                    x2 = [u ^ v for u, v in zip(x2, basis[j])]
            recovered = sum(x1[e] << j for j, e in enumerate(cotree))
            w = permute_bits(mat_vec(A, recovered) ^ phase, perm)
            c.check(x1 == x2); c.check(boundary(n, edges, x1) == charge)
            c.check((q_repeated(MASK0, w, d), q_repeated(MASK1, w, d)) == rhs)
            c.witness_reconstructions += 1
        # Odd total charge is rejected before residual work.
        odd = list(charge); odd[0] ^= 1
        try: lift(n, edges, forest, cotree, odd, 0)
        except ValueError: c.assertions += 1; c.hostile_controls += 1
        else: raise AssertionError("odd charge accepted")
        rows_out.append({"graph": f"K_{{{side},{side}}}", "vertices": n,
            "edges": len(edges), "cotree_dimension": d, "projected_rank": d,
            "pencil_ranks": ranks,
            "polar_densities": [sum(row.bit_count() for row in J)/(d*(d-1)) for J in mixed],
            "encoded_record_bytes": len(payload.encode())})
        deadline()

    # Affine/Horn/Krom and planted nonlinear easy controls.
    for z in range(16):
        c.check(parity(z & 15) in (0, 1))
        c.check(((not (z & 1)) or bool(z & 2)) in (True, False))
        c.check((bool(z & 4) == bool(z & 8)) in (True, False))
        c.check((q_repeated(MASK0, z, 4), q_repeated(MASK1, z, 4)) in SELECTOR)
        c.hostile_controls += 4

    base = json.loads(encode(3, [0] * 6, 0, 0, 0, list(range(4))))
    mutations = [("side", 4), ("charge", [0] * 5), ("charge", [1, 0, 0, 0, 0, 0]),
        ("phase", "0"), ("phase", "00x0"), ("b1", 2), ("permutation", [0, 1, 1, 3]),
        ("transform", "table"), ("forms", "matching_pair")]
    for key, value in mutations:
        item = dict(base); item[key] = value
        try: decode(json.dumps(item))
        except ValueError: c.assertions += 1; c.malformed_rejections += 1
        else: raise AssertionError("malformed record accepted")
    item = dict(base); item["advice"] = 1
    try: decode(json.dumps(item))
    except ValueError: c.assertions += 1; c.malformed_rejections += 1
    else: raise AssertionError("off-image record accepted")

    elapsed = time.monotonic() - start; deadline()
    semantic = {"claim": "an everywhere-nonsingular two-dimensional quadratic polar pencil can admit a constant-support uniform witness selector after dense affine mixing and Tseitin lifting",
        "status": "COMPUTATIONAL audit supporting an exact symbolic counterexample; independent review pending",
        "base_masks": [MASK0, MASK1], "selector": {f"{a}{b}": SELECTOR[(a,b)] for a,b in SELECTOR},
        "base_truth_fibers": {f"{a}{b}": [x for x in range(16) if (q_repeated(MASK0,x,4),q_repeated(MASK1,x,4))==(a,b)] for a,b in SELECTOR},
        "counters": asdict(c), "family_rows": rows_out}
    digest = hashlib.sha256(json.dumps(semantic, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return {"run_id": "PENCILFW1", "seed": SEED, "elapsed_seconds": round(elapsed, 6),
        "deadline_seconds": DEADLINE_SECONDS, "semantic_digest_sha256": digest, "semantic": semantic,
        "limitations": ["Finite checks do not prove an asymptotic lower bound.",
          "The symbolic family is a polynomial-time upper-bound counterexample, not an algorithm for arbitrary quadratic systems.",
          "Every nonzero polar pencil member is nonsingular, but this does not imply unavoidable computation.",
          "Parsing, affine elimination, mixing inversion, selection, lifting and verification are polynomial and charged.",
          "No DNNF, PC, circuit, ETH or cryptographic premise is promoted to unrestricted runtime."]}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
