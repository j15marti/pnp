#!/usr/bin/env python3
"""Finite audit for the PERMEXT1 unique-extension firewall.

The experiment is deliberately small and exact.  It checks that a source
assignment u has exactly one extension through

    B_X x = c(u),       cube(pi_C x) = b(u)

when cube(z)=z^3 is a permutation of GF(2^d), d odd.  Formula truth is then
preserved exactly.  This is an upper-bound/parsimonious-extension audit, not a
runtime lower bound and not an asymptotic inference from timing.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from dataclasses import dataclass
from pathlib import Path


SEED = 23002026


def degree(p: int) -> int:
    return p.bit_length() - 1


def poly_mod(a: int, modulus: int) -> int:
    md = degree(modulus)
    while a and degree(a) >= md:
        a ^= modulus << (degree(a) - md)
    return a


def poly_gcd(a: int, b: int) -> int:
    while b:
        a, b = b, poly_mod(a, b)
    return a


def gf_mul(a: int, b: int, modulus: int, d: int) -> int:
    out = 0
    x = a
    y = b
    for _ in range(d):
        if y & 1:
            out ^= x
        y >>= 1
        x <<= 1
        if x & (1 << d):
            x ^= modulus
    return out & ((1 << d) - 1)


def gf_pow(a: int, exponent: int, modulus: int, d: int) -> int:
    out = 1
    base = a
    while exponent:
        if exponent & 1:
            out = gf_mul(out, base, modulus, d)
        base = gf_mul(base, base, modulus, d)
        exponent >>= 1
    return out


def is_irreducible(modulus: int, d: int) -> bool:
    if degree(modulus) != d or not (modulus & 1):
        return False
    x = 0b10
    power = x
    for _ in range(1, d // 2 + 1):
        power = gf_mul(power, power, modulus, d)
        if poly_gcd(power ^ x, modulus) != 1:
            return False
    power = x
    for _ in range(d):
        power = gf_mul(power, power, modulus, d)
    return power == x


def first_irreducible(d: int) -> int:
    for low in range(1, 1 << d, 2):
        p = (1 << d) | low
        if is_irreducible(p, d):
            return p
    raise AssertionError(f"no irreducible polynomial found for degree {d}")


def bits(value: int, n: int) -> list[int]:
    return [(value >> i) & 1 for i in range(n)]


def source_target(u: list[int], d: int, phase: int) -> int:
    """A public quadratic source-to-target circuit b(u)."""
    n = len(u)
    out = 0
    for j in range(d):
        v = u[(3 * j + 1) % n]
        v ^= u[j % n] & u[(2 * j + 3) % n]
        v ^= (phase >> (j % max(1, phase.bit_length()))) & 1 if phase else 0
        out |= v << j
    return out


def source_charge(u: list[int], vertices: int, phase: int) -> list[int]:
    """A public even charge vector; the last bit is the parity check bit."""
    c = []
    for i in range(vertices - 1):
        c.append(u[(i + phase) % len(u)] ^ ((i + phase) & 1))
    c.append(sum(c) & 1)
    return c


def source_formula(kind: str, u: list[int]) -> bool:
    n = len(u)
    if kind == "yes":
        return True
    if kind == "no":
        return False
    if kind == "horn":
        return ((not u[0]) or (not u[1]) or u[2]) and ((not u[2]) or u[3])
    if kind == "krom":
        return (u[0] or u[1]) and ((not u[1]) or u[2]) and ((not u[2]) or u[3])
    if kind == "affine":
        return (u[0] ^ u[1] ^ u[2]) == 1 and (u[2] ^ u[3]) == 0
    if kind == "path":
        return all(u[i] or (not u[i + 1]) for i in range(n - 1))
    if kind == "product":
        left = (u[0] or u[1]) and ((not u[0]) or u[1])
        right = (u[n - 2] or u[n - 1]) and ((not u[n - 2]) or u[n - 1])
        return left and right
    if kind == "planted3":
        return (u[0] or u[1] or u[2]) and ((not u[0]) or u[2] or u[3])
    raise ValueError(kind)


@dataclass(frozen=True)
class Graph:
    vertices: int
    edges: tuple[tuple[int, int], ...]
    tree: tuple[int, ...]
    cotree: tuple[int, ...]

    @property
    def cycle_rank(self) -> int:
        return len(self.edges) - self.vertices + 1


def spanning_tree(vertices: int, edges: list[tuple[int, int]]) -> tuple[int, ...]:
    parent = list(range(vertices))

    def find(a: int) -> int:
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    chosen = []
    for i, (a, b) in enumerate(edges):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
            chosen.append(i)
    if len(chosen) != vertices - 1:
        raise ValueError("graph is disconnected")
    return tuple(chosen)


def k_bipartite(left: int, right: int) -> Graph:
    edges = [(i, left + j) for i in range(left) for j in range(right)]
    tree = spanning_tree(left + right, edges)
    tree_set = set(tree)
    cotree = tuple(i for i in range(len(edges)) if i not in tree_set)
    return Graph(left + right, tuple(edges), tree, cotree)


def graph_for_rank(d: int) -> Graph:
    if d == 9:
        g = k_bipartite(4, 4)
    else:
        g = k_bipartite(2, d + 1)
    assert g.cycle_rank == d
    return g


def recognize_record(d: int, modulus: int, g: Graph, target_bits: int) -> bool:
    """Syntactic promise recognizer used by the structured-family audit."""
    if d < 3 or d % 2 == 0 or target_bits != d:
        return False
    if not is_irreducible(modulus, d) or g.cycle_rank != d:
        return False
    try:
        return len(spanning_tree(g.vertices, list(g.edges))) == g.vertices - 1
    except ValueError:
        return False


def incidence_ok(g: Graph, x: list[int], charge: list[int]) -> bool:
    seen = [0] * g.vertices
    for bit, (a, b) in zip(x, g.edges):
        seen[a] ^= bit
        seen[b] ^= bit
    return seen == charge


def lift(g: Graph, charge: list[int], cotree_value: int) -> list[int]:
    if len(charge) != g.vertices or (sum(charge) & 1):
        raise ValueError("charge must have even parity and correct length")
    x = [0] * len(g.edges)
    residual = charge[:]
    for j, ei in enumerate(g.cotree):
        value = (cotree_value >> j) & 1
        x[ei] = value
        a, b = g.edges[ei]
        residual[a] ^= value
        residual[b] ^= value

    adjacency = [[] for _ in range(g.vertices)]
    for ei in g.tree:
        a, b = g.edges[ei]
        adjacency[a].append((b, ei))
        adjacency[b].append((a, ei))
    parent = [-1] * g.vertices
    parent_edge = [-1] * g.vertices
    order = [0]
    parent[0] = 0
    for v in order:
        for w, ei in adjacency[v]:
            if parent[w] == -1:
                parent[w] = v
                parent_edge[w] = ei
                order.append(w)
    if len(order) != g.vertices:
        raise ValueError("tree does not span")
    for v in reversed(order[1:]):
        value = residual[v]
        x[parent_edge[v]] = value
        residual[parent[v]] ^= value
    if residual[0] != 0 or not incidence_ok(g, x, charge):
        raise AssertionError("forest reconstruction failed")
    return x


def cotree_value(g: Graph, x: list[int]) -> int:
    return sum((x[ei] & 1) << j for j, ei in enumerate(g.cotree))


def gate_clause_unique_checks() -> int:
    """Exhaustively check definitional CNF clauses for AND, XOR, and NOT."""
    checks = 0
    for a in (0, 1):
        for b in (0, 1):
            satisfying_and = []
            satisfying_xor = []
            for y in (0, 1):
                and_clauses = [not y or a, not y or b, y or not a or not b]
                xor_clauses = [not a or not b or not y, a or b or not y,
                               a or not b or y, not a or b or y]
                if all(and_clauses):
                    satisfying_and.append(y)
                if all(xor_clauses):
                    satisfying_xor.append(y)
            assert satisfying_and == [a & b]
            assert satisfying_xor == [a ^ b]
            checks += 2
    for a in (0, 1):
        satisfying = []
        for y in (0, 1):
            clauses = [a or y, (not a) or (not y)]
            if all(clauses):
                satisfying.append(y)
        assert satisfying == [1 ^ a]
        checks += 1
    return checks


def run() -> dict:
    started = time.perf_counter()
    assertions = gate_clause_unique_checks()
    witness_count = 0
    accepted_count = 0
    rejected_count = 0
    field_rows = []
    control_rows = []
    kinds = ["yes", "no", "horn", "krom", "affine", "path", "product", "planted3"]

    for d in (3, 5, 7, 9):
        modulus = first_irreducible(d)
        g = graph_for_rank(d)
        inverse_exponent = ((1 << (d + 1)) - 1) // 3
        preimage = {}
        for z in range(1 << d):
            qz = gf_pow(z, 3, modulus, d)
            assert qz not in preimage
            preimage[qz] = z
            assert gf_pow(qz, inverse_exponent, modulus, d) == z
            assertions += 2
        assert len(preimage) == 1 << d
        assert recognize_record(d, modulus, g, d)
        assertions += 2

        n = min(8, d + 3)
        d_witnesses = 0
        for phase in (0, 1, 3):
            for kind in kinds:
                truth_count = 0
                for raw in range(1 << n):
                    u = bits(raw, n)
                    # Hostile-control wrapper: reverse and complement on phase 3.
                    if phase == 3:
                        u_eval = [1 ^ bit for bit in reversed(u)]
                    else:
                        u_eval = u
                    b = source_target(u_eval, d, phase)
                    z = gf_pow(b, inverse_exponent, modulus, d)
                    c = source_charge(u_eval, g.vertices, phase)
                    x = lift(g, c, z)
                    assert incidence_ok(g, x, c)
                    assert cotree_value(g, x) == z
                    assert gf_pow(cotree_value(g, x), 3, modulus, d) == b
                    assertions += 3
                    # Exhaustively confirm that z is the only residual preimage.
                    assert preimage[b] == z
                    assertions += 1
                    f_value = source_formula(kind, u_eval)
                    g_value = f_value and incidence_ok(g, x, c) and (
                        gf_pow(cotree_value(g, x), 3, modulus, d) == b
                    )
                    assert g_value == f_value
                    assertions += 1
                    truth_count += int(f_value)
                    witness_count += 1
                    d_witnesses += 1
                    accepted_count += int(g_value)
                control_rows.append({
                    "d": d,
                    "source_bits": n,
                    "phase": phase,
                    "control": kind,
                    "source_assignments": 1 << n,
                    "true_assignments": truth_count,
                })
        field_rows.append({
            "d": d,
            "modulus": modulus,
            "inverse_exponent": inverse_exponent,
            "graph_vertices": g.vertices,
            "graph_edges": len(g.edges),
            "cycle_rank": g.cycle_rank,
            "witnesses_checked": d_witnesses,
        })

    # Malformed/off-image record controls.
    disconnected = Graph(4, ((0, 1), (2, 3)), (0, 1), ())
    malformed = [
        ("even_degree", recognize_record(4, first_irreducible(4), graph_for_rank(4), 4)),
        ("reducible_modulus", recognize_record(5, (1 << 5) | 1, graph_for_rank(5), 5)),
        ("wrong_graph_rank", recognize_record(7, first_irreducible(7), graph_for_rank(5), 7)),
        ("dimension_mismatch", recognize_record(5, first_irreducible(5), graph_for_rank(5), 4)),
        ("disconnected_graph", recognize_record(3, first_irreducible(3), disconnected, 3)),
    ]
    for name, accepted in malformed:
        assert not accepted, name
        rejected_count += 1
        assertions += 1
    try:
        g = graph_for_rank(3)
        lift(g, [1] + [0] * (g.vertices - 1), 0)
        raise AssertionError("odd charge accepted")
    except ValueError:
        assertions += 1

    elapsed = time.perf_counter() - started
    return {
        "run_id": "PERMEXT1",
        "seed": SEED,
        "method": "exhaustive over declared small fields and all source assignments",
        "elapsed_seconds": elapsed,
        "assertions": assertions,
        "full_witnesses_checked": witness_count,
        "accepted_source_witnesses": accepted_count,
        "malformed_records_rejected": rejected_count,
        "field_rows": field_rows,
        "control_rows": control_rows,
        "limitations": [
            "Finite checks do not establish an asymptotic runtime lower bound.",
            "The symbolic unique-extension theorem is separate from these tests.",
            "The construction is a transparent subclass, not an algorithm for arbitrary MQ or SAT.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result = run()
    source_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result["code_sha256"] = source_hash
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
