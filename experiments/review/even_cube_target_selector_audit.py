#!/usr/bin/env python3
"""CUBEROOTSEL1: target-only selector for an even-degree cube subfamily.

For even d not divisible by 6, the nonzero cube image in GF(2^d) has
order m=(2^d-1)/3 with gcd(3,m)=1.  If e=3^{-1} mod m, then y^e is a
cube root of every promised image point y.  This audit independently checks
that identity, affine input/output conjugates, and complete Tseitin forest
lifting without giving the selector the planted preimage.

Finite checks are computational evidence only.  The symbolic identity is
elementary and stated separately in the accompanying report.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import time
from collections import Counter, deque
from pathlib import Path


def poly_deg(a: int) -> int:
    return a.bit_length() - 1


def poly_mod(a: int, f: int) -> int:
    df = poly_deg(f)
    while poly_deg(a) >= df:
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


def prime_divisors(n: int) -> list[int]:
    out: list[int] = []
    p = 2
    while p * p <= n:
        if n % p == 0:
            out.append(p)
            while n % p == 0:
                n //= p
        p += 1
    if n > 1:
        out.append(n)
    return out


def is_irreducible(f: int, d: int) -> bool:
    if poly_deg(f) != d or not (f & 1):
        return False
    x = 2
    powers = [x]
    for _ in range(d):
        powers.append(gf_mul(powers[-1], powers[-1], f, d))
    if powers[d] != x:
        return False
    return all(poly_gcd(powers[d // q] ^ x, f) == 1
               for q in prime_divisors(d))


def first_irreducible(d: int) -> int:
    for middle in range(1 << (d - 1)):
        f = (1 << d) | (middle << 1) | 1
        if is_irreducible(f, d):
            return f
    raise AssertionError(f"no irreducible polynomial of degree {d}")


def cube_selector_exponent(d: int) -> int:
    if d < 4 or d % 2 or d % 6 == 0:
        raise ValueError("selector subtype requires even d >= 4 and 6 not dividing d")
    m = ((1 << d) - 1) // 3
    if math.gcd(3, m) != 1:
        raise ValueError("3 is not invertible modulo cube-image order")
    return pow(3, -1, m)


def cube_root_if_image(y: int, f: int, d: int) -> int | None:
    if y == 0:
        return 0
    e = cube_selector_exponent(d)
    z = gf_pow(y, e, f, d)
    return z if cube(z, f, d) == y else None


def unit_lower(d: int, salt: int) -> list[int]:
    rows: list[int] = []
    for i in range(d):
        row = 1 << i
        for j in range(i):
            if ((i + 1) * 5 + (j + 1) * 7 + salt) % 11 < 5:
                row |= 1 << j
        rows.append(row)
    return rows


def mat_vec(rows: list[int], x: int) -> int:
    out = 0
    for i, row in enumerate(rows):
        if (row & x).bit_count() & 1:
            out |= 1 << i
    return out


def invert_unit_lower(rows: list[int], y: int) -> int:
    x = 0
    for i, row in enumerate(rows):
        lower = row & ((1 << i) - 1)
        bit = ((y >> i) & 1) ^ ((lower & x).bit_count() & 1)
        x |= bit << i
    return x


def affine_cube(rows_in: list[int], phase_in: int, rows_out: list[int],
                phase_out: int, z: int, f: int, d: int) -> int:
    t = mat_vec(rows_in, z) ^ phase_in
    return mat_vec(rows_out, cube(t, f, d)) ^ phase_out


def affine_cube_root_if_image(rows_in: list[int], phase_in: int,
                              rows_out: list[int], phase_out: int,
                              target: int, f: int, d: int) -> int | None:
    y = invert_unit_lower(rows_out, target ^ phase_out)
    t = cube_root_if_image(y, f, d)
    if t is None:
        return None
    z = invert_unit_lower(rows_in, t ^ phase_in)
    return z if affine_cube(rows_in, phase_in, rows_out, phase_out,
                            z, f, d) == target else None


def kss(s: int) -> tuple[int, list[tuple[int, int]], list[int], list[int]]:
    edges = [(i, s + j) for i in range(s) for j in range(s)]
    tree = [i * s for i in range(1, s)] + list(range(s))
    cotree = [i * s + j for i in range(1, s) for j in range(1, s)]
    assert len(tree) == 2 * s - 1
    assert len(cotree) == (s - 1) ** 2
    assert set(tree).isdisjoint(cotree)
    assert set(tree) | set(cotree) == set(range(s * s))
    return 2 * s, edges, tree, cotree


def forest_lift(n: int, edges: list[tuple[int, int]], tree: list[int],
                cotree: list[int], charge: list[int], z: int) -> list[int]:
    if len(charge) != n or z >= (1 << len(cotree)):
        raise ValueError("malformed lift input")
    if set(tree).intersection(cotree) or set(tree) | set(cotree) != set(range(len(edges))):
        raise ValueError("tree/cotree do not partition edges")
    x = [0] * len(edges)
    residual = charge[:]
    for bit, ei in enumerate(cotree):
        val = (z >> bit) & 1
        x[ei] = val
        if val:
            a, b = edges[ei]
            residual[a] ^= 1
            residual[b] ^= 1

    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for ei in tree:
        a, b = edges[ei]
        if a == b or not (0 <= a < n and 0 <= b < n):
            raise ValueError("bad edge")
        adj[a].append((b, ei))
        adj[b].append((a, ei))

    seen = [False] * n
    for root in range(n):
        if seen[root]:
            continue
        parent = [-1] * n
        parent_edge = [-1] * n
        order: list[int] = []
        queue = deque([root])
        seen[root] = True
        while queue:
            v = queue.popleft()
            order.append(v)
            for w, ei in adj[v]:
                if w == parent[v]:
                    continue
                if seen[w]:
                    raise ValueError("declared forest has a cycle")
                seen[w] = True
                parent[w] = v
                parent_edge[w] = ei
                queue.append(w)
        for v in reversed(order[1:]):
            val = residual[v]
            ei = parent_edge[v]
            x[ei] = val
            if val:
                residual[parent[v]] ^= 1
            residual[v] = 0
        if residual[root]:
            raise ValueError("odd residual charge on a component")
    return x


def incidence(n: int, edges: list[tuple[int, int]], x: list[int]) -> list[int]:
    out = [0] * n
    for val, (a, b) in zip(x, edges):
        if val:
            out[a] ^= 1
            out[b] ^= 1
    return out


def source_sat(u: int) -> bool:
    bits = [(u >> i) & 1 for i in range(4)]
    return bool((bits[0] or bits[1] or bits[2]) and
                ((not bits[0]) or bits[1] or bits[3]))


def run() -> dict:
    started = time.perf_counter()
    assertions = 0
    failures: list[str] = []
    field_rows = []
    image_targets = 0
    off_image_targets = 0
    affine_targets = 0
    witness_reconstructions = 0
    erased_preimage_differences = 0
    source_yes = 0
    source_no = 0

    # Exhaustive target-only inversion on small selector dimensions.
    for d in (4, 8, 10, 14):
        f = first_irreducible(d)
        e = cube_selector_exponent(d)
        m = ((1 << d) - 1) // 3
        assertions += 2
        if (3 * e - 1) % m:
            failures.append(f"bad-exponent:{d}")
        fibers: dict[int, list[int]] = {}
        for z in range(1 << d):
            fibers.setdefault(cube(z, f, d), []).append(z)
        root_hist = Counter()
        for y, roots in fibers.items():
            recovered = cube_root_if_image(y, f, d)
            assertions += 2
            image_targets += 1
            if recovered is None or cube(recovered, f, d) != y:
                failures.append(f"image-root:{d}:{y}")
            if recovered not in roots:
                failures.append(f"wrong-fiber:{d}:{y}")
            root_hist[len(roots)] += 1
        image = set(fibers)
        for y in range(1 << d):
            if y not in image:
                assertions += 1
                off_image_targets += 1
                if cube_root_if_image(y, f, d) is not None:
                    failures.append(f"off-image-accepted:{d}:{y}")
        field_rows.append({
            "degree": d,
            "modulus": f,
            "image_order": m,
            "selector_exponent": e,
            "image_size": len(image),
            "fiber_histogram": dict(sorted(root_hist.items())),
        })

    # Exact control: d divisible by 6 has no power-map inverse on the image.
    blocked_dimensions = []
    for d in (6, 12, 18):
        m = ((1 << d) - 1) // 3
        assertions += 2
        if math.gcd(3, m) != 3:
            failures.append(f"blocked-gcd:{d}")
        try:
            cube_selector_exponent(d)
            failures.append(f"blocked-accepted:{d}")
        except ValueError:
            blocked_dimensions.append(d)

    # Affine input/output mixing and target-only selector.  The selector sees
    # only the target and public typed record, never the planted preimage.
    for d in (4, 8, 10):
        f = first_irreducible(d)
        ain, aout = unit_lower(d, 3), unit_lower(d, 8)
        pin = sum(1 << i for i in range(d) if (i * i + 1) % 5 < 2)
        pout = sum(1 << i for i in range(d) if (3 * i + 2) % 7 < 3)
        for planted in range(1 << d):
            target = affine_cube(ain, pin, aout, pout, planted, f, d)
            recovered = affine_cube_root_if_image(ain, pin, aout, pout,
                                                  target, f, d)
            assertions += 2
            affine_targets += 1
            if recovered is None or affine_cube(ain, pin, aout, pout,
                                                recovered, f, d) != target:
                failures.append(f"affine-root:{d}:{target}")
            if recovered != planted:
                erased_preimage_differences += 1

    # Full Tseitin lifts for the actual square cotree dimensions d=4,16.
    graph_rows = []
    for s in (3, 5):
        d = (s - 1) ** 2
        f = first_irreducible(d)
        ain, aout = unit_lower(d, 4), unit_lower(d, 9)
        pin = sum(1 << i for i in range(d) if i % 3 == 1)
        pout = sum(1 << i for i in range(d) if i % 4 == 2)
        n, edges, tree, cotree = kss(s)
        cases = range(1 << d) if d == 4 else range(512)
        completed = 0
        for raw in cases:
            planted = (raw * 0x9E37 + 0x53) & ((1 << d) - 1)
            target = affine_cube(ain, pin, aout, pout, planted, f, d)
            recovered = affine_cube_root_if_image(ain, pin, aout, pout,
                                                  target, f, d)
            charge = [((raw + 17 * i) >> (i % 7)) & 1 for i in range(n - 1)]
            charge.append(sum(charge) & 1)
            if recovered is None:
                failures.append(f"missing-recovered:{s}:{raw}")
                continue
            x = forest_lift(n, edges, tree, cotree, charge, recovered)
            assertions += 3
            witness_reconstructions += 1
            completed += 1
            if incidence(n, edges, x) != charge:
                failures.append(f"incidence:{s}:{raw}")
            z_back = sum(x[ei] << bit for bit, ei in enumerate(cotree))
            if z_back != recovered:
                failures.append(f"cotree:{s}:{raw}")
            if affine_cube(ain, pin, aout, pout, z_back, f, d) != target:
                failures.append(f"residual:{s}:{raw}")
        graph_rows.append({"s": s, "degree": d, "cases": len(cases),
                           "complete_witnesses": completed})

    # Literal source-conjunct controls: YES witnesses extend; NO assignments
    # are rejected before any residual witness can make the conjunction true.
    d = 4
    f = first_irreducible(d)
    ain, aout = unit_lower(d, 4), unit_lower(d, 9)
    pin, pout = 0b0110, 0b1001
    n, edges, tree, cotree = kss(3)
    for u in range(16):
        target = affine_cube(ain, pin, aout, pout, u, f, d)
        recovered = affine_cube_root_if_image(ain, pin, aout, pout,
                                              target, f, d)
        assertions += 1
        if source_sat(u):
            source_yes += 1
            if recovered is None:
                failures.append(f"source-yes-root:{u}")
                continue
            charge = [0] * n
            x = forest_lift(n, edges, tree, cotree, charge, recovered)
            assertions += 2
            witness_reconstructions += 1
            if incidence(n, edges, x) != charge:
                failures.append(f"source-yes-incidence:{u}")
            if affine_cube(ain, pin, aout, pout, recovered, f, d) != target:
                failures.append(f"source-yes-residual:{u}")
        else:
            source_no += 1
            if source_sat(u):
                failures.append(f"source-no-accepted:{u}")

    # Disconnected graph with an isolate: zero isolate charge lifts; odd does not.
    n, edges, tree, cotree = kss(3)
    n_iso = n + 1
    charge = [0] * n_iso
    z = 0b1010
    x = forest_lift(n_iso, edges, tree, cotree, charge, z)
    assertions += 2
    if incidence(n_iso, edges, x) != charge:
        failures.append("isolate-zero-charge")
    bad = charge[:]
    bad[-1] = 1
    try:
        forest_lift(n_iso, edges, tree, cotree, bad, z)
        failures.append("isolate-odd-charge-accepted")
    except ValueError:
        pass

    # Malformed and odd-degree controls.
    malformed_rejections = 0
    for d, f in ((4, 0b10001), (5, first_irreducible(5))):
        ok = d >= 4 and d % 2 == 0 and d % 6 != 0 and is_irreducible(f, d)
        assertions += 1
        if ok:
            failures.append(f"malformed-field:{d}:{f}")
        else:
            malformed_rejections += 1

    elapsed = time.perf_counter() - started
    result = {
        "run_id": "CUBEROOTSEL1",
        "status": "PASS" if not failures else "FAIL",
        "assertions": assertions,
        "failures": failures,
        "field_rows": field_rows,
        "blocked_power_selector_dimensions": blocked_dimensions,
        "graph_rows": graph_rows,
        "image_targets_checked": image_targets,
        "off_image_targets_checked": off_image_targets,
        "affine_targets_checked": affine_targets,
        "erased_preimage_differences": erased_preimage_differences,
        "witness_reconstructions": witness_reconstructions,
        "source_yes_controls": source_yes,
        "source_no_controls": source_no,
        "malformed_rejections": malformed_rejections,
        "elapsed_seconds": elapsed,
        "method": "deterministic exhaustive target-only root checks plus complete forest lifts",
        "limitations": [
            "finite checks support but do not prove the all-degree identity",
            "the power selector covers even d not divisible by 6; failure at d divisible by 6 is not hardness",
            "the selector solves the residual preimage problem, not the embedded source SAT instance",
            "no asymptotic conclusion is inferred from wall time",
        ],
    }
    if failures:
        raise AssertionError(failures[:10])
    return result


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    result = run()
    result["code_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
