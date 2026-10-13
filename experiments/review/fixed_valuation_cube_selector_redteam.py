#!/usr/bin/env python3
"""VALSUBCUBEFW1: fixed-3-adic-valuation cube-selector firewall.

For K=GF(2^d), q-1=3^A m with gcd(3,m)=1.  If A is fixed, the
subfield GF(2^(2*3^(A-1))) has the same 3-primary multiplicative order.
It can therefore supply a cubic nonresidue by constant-size exhaustive
search.  An explicit AMM-style correction then selects a cube root from the
target alone.  This audit checks A=1,2, including the square cotree d=36 of
K_{7,7} (where v_3(s-1)=1).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import time
from collections import deque
from pathlib import Path


RUN_ID = "VALSUBCUBEFW1"
SEED = 38142026


def poly_deg(p: int) -> int:
    return p.bit_length() - 1


def poly_mod(a: int, f: int) -> int:
    df = poly_deg(f)
    while a and poly_deg(a) >= df:
        a ^= f << (poly_deg(a) - df)
    return a


def poly_gcd(a: int, b: int) -> int:
    while b:
        a, b = b, poly_mod(a, b)
    return a


def gf_mul(a: int, b: int, f: int, d: int) -> int:
    out = 0
    mask = (1 << d) - 1
    while b:
        if b & 1:
            out ^= a
        b >>= 1
        a <<= 1
        if a >> d:
            a ^= f
    return out & mask


def gf_pow(a: int, e: int, f: int, d: int) -> int:
    out = 1
    while e:
        if e & 1:
            out = gf_mul(out, a, f, d)
        a = gf_mul(a, a, f, d)
        e >>= 1
    return out


def cube(a: int, f: int, d: int) -> int:
    return gf_mul(gf_mul(a, a, f, d), a, f, d)


def gf_inv(a: int, f: int, d: int) -> int:
    if not a:
        raise ZeroDivisionError("zero has no inverse")
    return gf_pow(a, (1 << d) - 2, f, d)


def prime_divisors(n: int) -> list[int]:
    ans: list[int] = []
    p = 2
    while p * p <= n:
        if n % p == 0:
            ans.append(p)
            while n % p == 0:
                n //= p
        p += 1
    if n > 1:
        ans.append(n)
    return ans


def is_irreducible(f: int, d: int) -> bool:
    if poly_deg(f) != d or not (f & 1):
        return False
    x = 2
    powers = [x]
    for _ in range(d):
        powers.append(gf_mul(powers[-1], powers[-1], f, d))
    if powers[d] != x:
        return False
    return all(poly_gcd(powers[d // p] ^ x, f) == 1
               for p in prime_divisors(d))


def first_irreducible(d: int) -> int:
    for middle in range(1 << (d - 1)):
        f = (1 << d) | (middle << 1) | 1
        if is_irreducible(f, d):
            return f
    raise AssertionError(f"no irreducible polynomial of degree {d}")


def valuation(n: int, p: int) -> int:
    a = 0
    while n % p == 0:
        n //= p
        a += 1
    return a


def nullspace(rows: list[int], width: int) -> list[int]:
    a = [r for r in rows]
    pivot_cols: list[int] = []
    rank = 0
    for col in range(width):
        pivot = next((i for i in range(rank, len(a)) if (a[i] >> col) & 1), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        for i in range(len(a)):
            if i != rank and ((a[i] >> col) & 1):
                a[i] ^= a[rank]
        pivot_cols.append(col)
        rank += 1
    pivots = set(pivot_cols)
    basis: list[int] = []
    for free in range(width):
        if free in pivots:
            continue
        x = 1 << free
        for i, col in enumerate(pivot_cols):
            if (a[i] >> free) & 1:
                x |= 1 << col
        basis.append(x)
    return basis


def fixed_subfield_basis(f: int, d: int, r: int) -> list[int]:
    if d % r:
        raise ValueError("subfield degree must divide field degree")
    columns = []
    for j in range(d):
        x = 1 << j
        columns.append(gf_pow(x, 1 << r, f, d) ^ x)
    rows = [sum(((columns[j] >> i) & 1) << j for j in range(d))
            for i in range(d)]
    basis = nullspace(rows, d)
    if len(basis) != r:
        raise AssertionError(("wrong subfield dimension", d, r, len(basis)))
    if any(gf_pow(x, 1 << r, f, d) != x for x in basis):
        raise AssertionError("bad subfield basis")
    return basis


def span_element(basis: list[int], mask: int) -> int:
    x = 0
    for i, b in enumerate(basis):
        if (mask >> i) & 1:
            x ^= b
    return x


def derive_cubic_nonresidue(f: int, d: int, a: int) -> tuple[int, int, int]:
    """Return (nonresidue, trials, subfield_degree) for fixed valuation a=v3(d)."""
    r = 2 * (3 ** a)
    basis = fixed_subfield_basis(f, d, r)
    q = 1 << d
    for mask in range(1, 1 << r):
        c = span_element(basis, mask)
        if gf_pow(c, (q - 1) // 3, f, d) != 1:
            return c, mask, r
    raise AssertionError("fixed subfield contained no cubic nonresidue")


def target_cube_root(b: int, f: int, d: int, nonresidue: int) -> int | None:
    if b == 0:
        return 0
    q = 1 << d
    A = valuation(q - 1, 3)
    m = (q - 1) // (3 ** A)
    e = pow(3, -1, m)
    y = gf_pow(b, e, f, d)
    eta = gf_pow(nonresidue, m, f, d)
    if gf_pow(eta, 3 ** (A - 1), f, d) == 1:
        raise AssertionError("nonresidue has insufficient 3-primary order")
    correction = 1
    for _ in range(3 ** (A - 1)):
        x = gf_mul(y, correction, f, d)
        if cube(x, f, d) == b:
            return x
        correction = gf_mul(correction, eta, f, d)
    return None


def kss(s: int) -> tuple[int, list[tuple[int, int]], list[int], list[int]]:
    edges = [(i, s + j) for i in range(s) for j in range(s)]
    tree = [i * s for i in range(1, s)] + list(range(s))
    cotree = [i * s + j for i in range(1, s) for j in range(1, s)]
    assert len(tree) == 2 * s - 1
    assert len(cotree) == (s - 1) ** 2
    return 2 * s, edges, tree, cotree


def forest_lift(n: int, edges: list[tuple[int, int]], tree: list[int],
                cotree: list[int], charge: list[int], z: int) -> list[int]:
    x = [0] * len(edges)
    residual = charge[:]
    for bit, ei in enumerate(cotree):
        value = (z >> bit) & 1
        x[ei] = value
        if value:
            u, v = edges[ei]
            residual[u] ^= 1
            residual[v] ^= 1
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for ei in tree:
        u, v = edges[ei]
        adj[u].append((v, ei))
        adj[v].append((u, ei))
    parent = [-1] * n
    parent_edge = [-1] * n
    order: list[int] = []
    seen = [False] * n
    queue = deque([0])
    seen[0] = True
    while queue:
        u = queue.popleft()
        order.append(u)
        for v, ei in adj[u]:
            if not seen[v]:
                seen[v] = True
                parent[v] = u
                parent_edge[v] = ei
                queue.append(v)
    if not all(seen):
        raise ValueError("declared tree disconnected")
    for v in reversed(order[1:]):
        value = residual[v]
        x[parent_edge[v]] = value
        if value:
            residual[parent[v]] ^= 1
        residual[v] = 0
    if residual[0]:
        raise ValueError("odd total charge")
    return x


def incidence(n: int, edges: list[tuple[int, int]], x: list[int]) -> list[int]:
    out = [0] * n
    for value, (u, v) in zip(x, edges):
        if value:
            out[u] ^= 1
            out[v] ^= 1
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    rng = random.Random(SEED)
    assertions = 0
    records = []
    moduli: dict[int, int] = {}
    affine_targets_checked = 0

    for d in (6, 12, 18, 36):
        f = first_irreducible(d)
        moduli[d] = f
        assert is_irreducible(f, d)
        assertions += 1
        a = valuation(d, 3)
        A = valuation((1 << d) - 1, 3)
        assert A == a + 1
        assertions += 1
        c, trials, r = derive_cubic_nonresidue(f, d, a)
        assert r == 2 * (3 ** a) and d % r == 0
        assert gf_pow(c, ((1 << d) - 1) // 3, f, d) != 1
        assertions += 2

        image_checked = 0
        off_image_rejected = 0
        roots_different = 0
        samples = list(range(1 << d)) if d <= 12 else [rng.randrange(1 << d) for _ in range(512)]
        for z in samples:
            b = cube(z, f, d)
            root = target_cube_root(b, f, d, c)
            assert root is not None and cube(root, f, d) == b
            assertions += 1
            image_checked += 1
            roots_different += root != z
        for _ in range(512):
            y = rng.randrange(1, 1 << d)
            if gf_pow(y, ((1 << d) - 1) // 3, f, d) == 1:
                continue
            assert target_cube_root(y, f, d, c) is None
            assertions += 1
            off_image_rejected += 1

        # Public invertible scalar-affine conjugations: these change every
        # coordinate presentation but not the availability of a selector.
        if d >= 18:
            ain = rng.randrange(1, 1 << d)
            aout = rng.randrange(1, 1 << d)
            ainv = gf_inv(ain, f, d)
            aout_inv = gf_inv(aout, f, d)
            pin = rng.randrange(1 << d)
            pout = rng.randrange(1 << d)
            for _ in range(128):
                z0 = rng.randrange(1 << d)
                inner = gf_mul(ain, z0, f, d) ^ pin
                target = gf_mul(aout, cube(inner, f, d), f, d) ^ pout
                normalized = gf_mul(aout_inv, target ^ pout, f, d)
                root = target_cube_root(normalized, f, d, c)
                assert root is not None
                recovered = gf_mul(ainv, root ^ pin, f, d)
                check = gf_mul(aout, cube(gf_mul(ain, recovered, f, d) ^ pin, f, d), f, d) ^ pout
                assert check == target
                assertions += 2
                affine_targets_checked += 1
        records.append({
            "d": d,
            "v3_d": a,
            "v3_q_minus_1": A,
            "subfield_degree": r,
            "subfield_enumeration_cap": 1 << r,
            "nonresidue_trial_mask": trials,
            "modulus": f,
            "image_targets_checked": image_checked,
            "off_image_targets_rejected": off_image_rejected,
            "selected_root_differs_from_source": roots_different,
        })

    # Real square-cotree control: K_{7,7} has d=(7-1)^2=36 and v3(6)=1.
    d = 36
    f = moduli[d]
    c, _, _ = derive_cubic_nonresidue(f, d, valuation(d, 3))
    n, edges, tree, cotree = kss(7)
    assert len(cotree) == d
    assertions += 1
    witness_reconstructions = 0
    for _ in range(192):
        source = rng.randrange(1 << d)
        target = cube(source, f, d)
        selected = target_cube_root(target, f, d, c)
        assert selected is not None
        charge = [rng.randrange(2) for _ in range(n - 1)]
        charge.append(sum(charge) & 1)
        assignment = forest_lift(n, edges, tree, cotree, charge, selected)
        assert incidence(n, edges, assignment) == charge
        recovered = sum(assignment[ei] << bit for bit, ei in enumerate(cotree))
        assert recovered == selected and cube(recovered, f, d) == target
        assertions += 3
        witness_reconstructions += 1

    malformed_rejections = 0
    try:
        fixed_subfield_basis(moduli[12], 12, 18)
    except ValueError:
        malformed_rejections += 1
        assertions += 1
    try:
        forest_lift(n, edges, tree, cotree, [0] * (n - 1) + [1], 0)
    except ValueError:
        malformed_rejections += 1
        assertions += 1

    result = {
        "run_id": RUN_ID,
        "seed": SEED,
        "records": records,
        "assertions": assertions,
        "affine_targets_checked": affine_targets_checked,
        "witness_reconstructions": witness_reconstructions,
        "malformed_rejections": malformed_rejections,
        "elapsed_seconds": time.perf_counter() - started,
        "status": "PASS",
        "theorem_scope": "fixed v3(d); Kss control d=36 with v3(s-1)=1",
        "limitation": "Finite audit checks A=1,2. The symbolic fixed-valuation theorem is separate; unbounded v3(d) is not covered.",
    }
    payload = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["result_sha256_without_self_hash"] = hashlib.sha256(payload).hexdigest()
    result["code_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
