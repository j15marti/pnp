#!/usr/bin/env python3
"""Finite audit for the CYCLOROOTFW1 cyclotomic cube selector.

For a >= 0 put d=2*3^a and

    f_a(X)=X^d+X^(d/2)+1 = Phi_{3^(a+1)}(X).

The symbolic proof shows f_a is irreducible over GF(2), and the residue of X
has exact order 3^(a+1).  This script checks that representation-exposed
noncube, target-only cube-root selection, strict canonical recognition, and
complete Tseitin tree lifting on bounded instances.  Timings are not used as
asymptotic evidence.
"""

from __future__ import annotations

import hashlib
import json
import random
import time
from dataclasses import dataclass
from pathlib import Path


RUN_ID = "CYCLOROOTFW1"
SEED = 141020260107
OUT = Path("results/raw/review/2026-10-14_0107_cyclotomic_cube_selector.json")


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
    while y:
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


def irreducible(modulus: int, d: int) -> bool:
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


def v3(n: int) -> int:
    a = 0
    while n % 3 == 0:
        n //= 3
        a += 1
    return a


def canonical_degree(a: int) -> int:
    return 2 * (3**a)


def canonical_modulus(a: int) -> int:
    d = canonical_degree(a)
    return (1 << d) | (1 << (d // 2)) | 1


def recognize_field(a: int, d: int, modulus: int) -> bool:
    return (
        type(a) is int
        and 0 <= a <= 30
        and d == canonical_degree(a)
        and modulus == canonical_modulus(a)
        and degree(modulus) == d
    )


def cube_image_member(b: int, modulus: int, d: int) -> bool:
    if b == 0:
        return True
    return gf_pow(b, ((1 << d) - 1) // 3, modulus, d) == 1


def select_cube_root(a: int, d: int, modulus: int, b: int) -> int | None:
    """Select a cube root, rejecting malformed and off-image targets."""
    if not recognize_field(a, d, modulus) or type(b) is not int or not (0 <= b < (1 << d)):
        raise ValueError("malformed")
    if b == 0:
        return 0
    n = (1 << d) - 1
    if gf_pow(b, n // 3, modulus, d) != 1:
        return None
    m = n // (3 ** (a + 1))
    e = pow(3, -1, m)
    y = gf_pow(b, e, modulus, d)
    # The residue eta=X has exact order 3^(a+1) for the canonical modulus.
    eta = 0b10
    eta_power = 1
    for _j in range(3**a):
        x = gf_mul(y, eta_power, modulus, d)
        if gf_pow(x, 3, modulus, d) == b:
            return x
        eta_power = gf_mul(eta_power, eta, modulus, d)
    raise AssertionError("cube target had no correction candidate")


@dataclass(frozen=True)
class Graph:
    vertices: int
    edges: tuple[tuple[int, int], ...]
    tree: tuple[int, ...]
    cotree: tuple[int, ...]


def spanning_tree(vertices: int, edges: list[tuple[int, int]]) -> tuple[int, ...]:
    parent = list(range(vertices))

    def find(v: int) -> int:
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    chosen = []
    for i, (u, v) in enumerate(edges):
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
            chosen.append(i)
    if len(chosen) != vertices - 1:
        raise ValueError("disconnected")
    return tuple(chosen)


def graph_for_rank(d: int) -> Graph:
    edges = [(i, 2 + j) for i in range(2) for j in range(d + 1)]
    tree = spanning_tree(d + 3, edges)
    tree_set = set(tree)
    cotree = tuple(i for i in range(len(edges)) if i not in tree_set)
    assert len(cotree) == d
    return Graph(d + 3, tuple(edges), tree, cotree)


def boundary(graph: Graph, x: list[int]) -> list[int]:
    out = [0] * graph.vertices
    for bit, (u, v) in zip(x, graph.edges):
        out[u] ^= bit
        out[v] ^= bit
    return out


def lift(graph: Graph, charge: list[int], cotree_value: int) -> list[int]:
    if len(charge) != graph.vertices or sum(charge) % 2:
        raise ValueError("charge")
    if not (0 <= cotree_value < (1 << len(graph.cotree))):
        raise ValueError("cotree")
    x = [0] * len(graph.edges)
    residual = charge[:]
    for j, edge_id in enumerate(graph.cotree):
        bit = (cotree_value >> j) & 1
        x[edge_id] = bit
        u, v = graph.edges[edge_id]
        residual[u] ^= bit
        residual[v] ^= bit

    adjacency = [[] for _ in range(graph.vertices)]
    for edge_id in graph.tree:
        u, v = graph.edges[edge_id]
        adjacency[u].append((v, edge_id))
        adjacency[v].append((u, edge_id))
    parent = [-1] * graph.vertices
    parent_edge = [-1] * graph.vertices
    order = [0]
    parent[0] = 0
    for v in order:
        for w, edge_id in adjacency[v]:
            if parent[w] < 0:
                parent[w] = v
                parent_edge[w] = edge_id
                order.append(w)
    if len(order) != graph.vertices:
        raise ValueError("tree")
    for v in reversed(order[1:]):
        bit = residual[v]
        x[parent_edge[v]] = bit
        residual[parent[v]] ^= bit
    if residual[0] or boundary(graph, x) != charge:
        raise AssertionError("reconstruction")
    return x


def project(graph: Graph, x: list[int]) -> int:
    return sum((x[edge_id] & 1) << j for j, edge_id in enumerate(graph.cotree))


def main() -> None:
    start = time.perf_counter()
    rng = random.Random(SEED)
    assertions = 0
    degrees = []
    irreducibility_checks = 0
    exact_targets = 0
    sampled_cube_targets = 0
    off_image_targets = 0
    reconstructions = 0
    malformed_rejections = 0
    maximum_correction_width = 0

    def check(condition: bool, message: str) -> None:
        nonlocal assertions
        assertions += 1
        if not condition:
            raise AssertionError(message)

    for a in range(0, 5):
        d = canonical_degree(a)
        modulus = canonical_modulus(a)
        degrees.append(d)
        check(recognize_field(a, d, modulus), f"canonical recognition a={a}")
        check(v3(d) == a, f"valuation a={a}")
        check(irreducible(modulus, d), f"irreducibility a={a}")
        irreducibility_checks += 1

        n = (1 << d) - 1
        eta = 0b10
        check(gf_pow(eta, 3 ** (a + 1), modulus, d) == 1, f"eta order upper a={a}")
        check(gf_pow(eta, 3**a, modulus, d) != 1, f"eta order exact a={a}")
        check(gf_pow(eta, n // 3, modulus, d) != 1, f"eta noncube a={a}")
        maximum_correction_width = max(maximum_correction_width, 3**a)

        graph = graph_for_rank(d)
        charge = [rng.randrange(2) for _ in range(graph.vertices - 1)]
        charge.append(sum(charge) & 1)

        if d <= 6:
            targets = list(range(1 << d))
        else:
            targets = [0]
            targets += [gf_pow(rng.randrange(1, 1 << d), 3, modulus, d) for _ in range(64)]
            while len(targets) < 129:
                b = rng.randrange(1, 1 << d)
                if not cube_image_member(b, modulus, d):
                    targets.append(b)

        for b in targets:
            member = cube_image_member(b, modulus, d)
            root = select_cube_root(a, d, modulus, b)
            check((root is not None) == member, f"image mismatch a={a}")
            if d <= 6:
                brute = any(gf_pow(z, 3, modulus, d) == b for z in range(1 << d))
                check(brute == member, f"truth table a={a}, b={b}")
                exact_targets += 1
            if root is None:
                off_image_targets += 1
                continue
            sampled_cube_targets += 1
            check(gf_pow(root, 3, modulus, d) == b, f"root check a={a}")
            x = lift(graph, charge, root)
            check(boundary(graph, x) == charge, f"boundary a={a}")
            check(project(graph, x) == root, f"cotree a={a}")
            reconstructions += 1

        # Malformed canonical-type controls.
        bad_inputs = [
            (a, d, modulus ^ 0b10, 0),
            (a, d + 1, modulus, 0),
            (a + 1, d, modulus, 0),
            (a, d, modulus, 1 << d),
        ]
        for aa, dd, ff, bb in bad_inputs:
            try:
                select_cube_root(aa, dd, ff, bb)
            except ValueError:
                malformed_rejections += 1
            else:
                raise AssertionError(f"malformed accepted a={a}")

        # Odd charges are rejected independently of the root selector.
        odd_charge = charge[:]
        odd_charge[0] ^= 1
        try:
            lift(graph, odd_charge, 0)
        except ValueError:
            malformed_rejections += 1
        else:
            raise AssertionError(f"odd charge accepted a={a}")

    source = Path(__file__).read_bytes()
    result = {
        "run_id": RUN_ID,
        "seed": SEED,
        "status": "COMPUTATIONAL",
        "a_values": list(range(5)),
        "degrees": degrees,
        "irreducibility_checks": irreducibility_checks,
        "exact_truth_table_targets": exact_targets,
        "sampled_cube_targets": sampled_cube_targets,
        "off_image_targets_rejected": off_image_targets,
        "complete_tseitin_reconstructions": reconstructions,
        "malformed_or_odd_charge_rejections": malformed_rejections,
        "maximum_correction_width": maximum_correction_width,
        "assertions": assertions,
        "failures": 0,
        "elapsed_seconds": round(time.perf_counter() - start, 6),
        "code_sha256": hashlib.sha256(source).hexdigest(),
        "limitations": [
            "finite checks do not prove the cyclotomic irreducibility theorem",
            "degrees 18, 54, and 162 use sampled targets rather than exhaustive fields",
            "this upper-bound firewall does not prove an unrestricted SAT lower bound",
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
