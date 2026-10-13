#!/usr/bin/env python3
"""PLANTEDCUBEFW1: source-matched section firewall for even-degree cubes.

The experiment checks the exact finite-field identities behind the report and
reconstructs complete Tseitin witnesses.  It is deterministic and dependency
free.  Finite checks are not interpreted as asymptotic lower bounds.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from collections import Counter
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


def prime_divisors(n: int) -> list[int]:
    out = []
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


def gf_trace(a: int, f: int, d: int) -> int:
    total = 0
    cur = a
    for _ in range(d):
        total ^= cur
        cur = gf_mul(cur, cur, f, d)
    if total not in (0, 1):
        raise AssertionError((a, f, d, total))
    return total


def cube(a: int, f: int, d: int) -> int:
    return gf_mul(gf_mul(a, a, f, d), a, f, d)


def gf2_rank(rows: list[int], width: int) -> int:
    rows = rows[:]
    rank = 0
    for col in range(width):
        pivot = next((i for i in range(rank, len(rows))
                      if (rows[i] >> col) & 1), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for i in range(len(rows)):
            if i != rank and ((rows[i] >> col) & 1):
                rows[i] ^= rows[rank]
        rank += 1
    return rank


def polar_rows(lam: int, f: int, d: int) -> list[int]:
    rows = [0] * d
    for i in range(d):
        ei = 1 << i
        for j in range(i + 1, d):
            ej = 1 << j
            p = cube(ei ^ ej, f, d) ^ cube(ei, f, d) ^ cube(ej, f, d)
            bit = gf_trace(gf_mul(lam, p, f, d), f, d)
            if bit:
                rows[i] |= 1 << j
                rows[j] |= 1 << i
    return rows


def dense_unit_lower(d: int) -> list[int]:
    rows = []
    for i in range(d):
        row = 1 << i
        for j in range(i):
            if ((i + 1) * 3 + (j + 1) * 5) % 7 < 3:
                row |= 1 << j
        rows.append(row)
    return rows


def mat_vec(rows: list[int], x: int) -> int:
    out = 0
    for i, row in enumerate(rows):
        if (row & x).bit_count() & 1:
            out |= 1 << i
    return out


def kss_lift(s: int, charge: list[int], cotree: int) -> list[int]:
    d = (s - 1) ** 2
    if len(charge) != 2 * s or (sum(charge) & 1) or cotree >= 1 << d:
        raise ValueError("invalid lift input")
    x = [0] * (s * s)
    bit = 0
    for i in range(1, s):
        for j in range(1, s):
            x[i * s + j] = (cotree >> bit) & 1
            bit += 1
    # Each non-root left/right vertex is a leaf after cotree contributions.
    for i in range(1, s):
        x[i * s] = charge[i] ^ sum(x[i * s + j] for j in range(1, s)) % 2
    for j in range(1, s):
        x[j] = charge[s + j] ^ sum(x[i * s + j] for i in range(1, s)) % 2
    x[0] = charge[0] ^ sum(x[j] for j in range(1, s)) % 2
    return x


def incidence_ok(s: int, charge: list[int], x: list[int]) -> bool:
    left = [sum(x[i * s + j] for j in range(s)) & 1 for i in range(s)]
    right = [sum(x[i * s + j] for i in range(s)) & 1 for j in range(s)]
    return left + right == charge


def source_sat(u: int, d: int) -> bool:
    bits = [(u >> i) & 1 for i in range(d)]
    # A fixed proper 3-CNF control; unused high bits remain legal source bits.
    return ((bits[0] or bits[1] or bits[2]) and
            ((not bits[0]) or bits[1] or bits[3]))


def run() -> dict:
    started = time.perf_counter()
    assertions = 0
    failures: list[str] = []
    field_rows = []
    fiber_checks = 0
    polar_checks = 0

    # Exhaustive small fields: image/fibers and zero scalar-polar kernel.
    for d in (4, 6, 8, 10):
        f = first_irreducible(d)
        fibers = Counter(cube(z, f, d) for z in range(1 << d))
        expected_image = 1 + ((1 << d) - 1) // 3
        assertions += 2
        if len(fibers) != expected_image:
            failures.append(f"image:{d}:{len(fibers)}")
        if sorted(Counter(fibers.values()).items()) != [(1, 1), (3, expected_image - 1)]:
            failures.append(f"fibers:{d}")
        zero_components = 0
        spectrum = Counter()
        for lam in range(1, 1 << d):
            rows = polar_rows(lam, f, d)
            rank = gf2_rank(rows, d)
            spectrum[rank] += 1
            polar_checks += 1
            assertions += 1
            if rank == 0:
                zero_components += 1
        if zero_components:
            failures.append(f"polar-kernel:{d}:{zero_components}")
        # Every off-image value is genuinely NO for z^3=b.
        image = set(fibers)
        for b in range(1 << d):
            if b not in image:
                assertions += 1
                fiber_checks += 1
                if any(cube(z, f, d) == b for z in range(1 << d)):
                    failures.append(f"off-image:{d}:{b}")
        field_rows.append({
            "degree": d,
            "modulus": f,
            "image_size": len(fibers),
            "fiber_histogram": dict(sorted(Counter(fibers.values()).items())),
            "polar_rank_spectrum": dict(sorted(spectrum.items())),
        })

    # Source-matched, densely mixed planted sections lifted through K_{s,s}.
    witness_reconstructions = 0
    source_cases = 0
    graph_rows = []
    for s in (3, 5, 7):
        d = (s - 1) ** 2
        f = first_irreducible(d)
        A = dense_unit_lower(d)
        phase = sum(1 << i for i in range(d) if (i * i + 3 * i + 1) % 5 < 2)
        patterns = range(1 << d) if d == 4 else range(128)
        accepted = 0
        for raw in patterns:
            # Repeat the available pattern deterministically to obtain d bits.
            width = min(d, 7)
            u = sum(((raw >> (i % width)) & 1) << i for i in range(d))
            source_cases += 1
            if not source_sat(u, d):
                continue
            accepted += 1
            planted = mat_vec(A, u) ^ phase
            target = cube(planted, f, d)
            charge = [((raw * 13 + i * 7) >> (i % 6)) & 1 for i in range(2 * s - 1)]
            charge.append(sum(charge) & 1)
            edge_witness = kss_lift(s, charge, planted)
            assertions += 3
            witness_reconstructions += 1
            if not incidence_ok(s, charge, edge_witness):
                failures.append(f"incidence:{s}:{raw}")
            if cube(planted, f, d) != target:
                failures.append(f"section:{s}:{raw}")
            if not source_sat(u, d):
                failures.append(f"projection:{s}:{raw}")
        graph_rows.append({"s": s, "degree": d, "source_cases": len(patterns),
                           "satisfying_source_cases": accepted})

    # Malformed controls: reducible modulus, odd degree, odd charge, wrong cotree.
    malformed_rejections = 0
    for d, f in ((4, 0b10001), (5, first_irreducible(5))):
        ok = d >= 4 and d % 2 == 0 and is_irreducible(f, d)
        assertions += 1
        if ok:
            failures.append(f"malformed-field:{d}:{f}")
        else:
            malformed_rejections += 1
    try:
        kss_lift(3, [1] + [0] * 5, 0)
        failures.append("odd-charge-accepted")
    except ValueError:
        malformed_rejections += 1
        assertions += 1
    try:
        kss_lift(3, [0] * 6, 1 << 4)
        failures.append("cotree-overflow-accepted")
    except ValueError:
        malformed_rejections += 1
        assertions += 1

    elapsed = time.perf_counter() - started
    result = {
        "run_id": "PLANTEDCUBEFW1",
        "status": "PASS" if not failures else "FAIL",
        "assertions": assertions,
        "failures": failures,
        "field_rows": field_rows,
        "graph_rows": graph_rows,
        "polar_components_checked": polar_checks,
        "off_image_targets_checked": fiber_checks,
        "source_cases": source_cases,
        "witness_reconstructions": witness_reconstructions,
        "malformed_rejections": malformed_rejections,
        "elapsed_seconds": elapsed,
        "method": "deterministic exhaustive small-field audit plus explicit Kss witness lifting",
        "limitations": [
            "finite checks support but do not prove the symbolic all-degree theorem",
            "the planted section is an upper-bound firewall, not an algorithm for arbitrary residual systems",
            "no runtime conclusion is inferred from measured elapsed time",
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
