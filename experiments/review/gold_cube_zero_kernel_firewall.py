"""CUBEPERMFW1: exact finite audit of the Gold cube residual firewall.

For odd d >= 3, Q(z)=z^3 on GF(2^d) is a quadratic permutation.  This
program checks its inverse, raw-ANF polar-output kernel, and a fully typed
Tseitin lift on a friendship graph.  Finite tests support, but do not replace,
the symbolic proof in the corresponding synthesis report.
"""

from __future__ import annotations

import hashlib
import json
import random
import time
from pathlib import Path


RUN_ID = "CUBEPERMFW1"
SEED = 22482026
DEGREES = (3, 5, 7, 9, 11)
OUT = Path("results/raw/review/2026-10-13_2248_gold_cube_zero_kernel.json")


def degree(p: int) -> int:
    return p.bit_length() - 1


def poly_mod(a: int, f: int) -> int:
    df = degree(f)
    while degree(a) >= df:
        a ^= f << (degree(a) - df)
    return a


def poly_gcd(a: int, b: int) -> int:
    while b:
        a, b = b, poly_mod(a, b)
    return a


def mul(a: int, b: int, f: int, d: int) -> int:
    ans = 0
    while b:
        if b & 1:
            ans ^= a
        b >>= 1
        a <<= 1
        if (a >> d) & 1:
            a ^= f
    return ans & ((1 << d) - 1)


def power(a: int, e: int, f: int, d: int) -> int:
    ans = 1
    while e:
        if e & 1:
            ans = mul(ans, a, f, d)
        a = mul(a, a, f, d)
        e >>= 1
    return ans


def prime_divisors(n: int) -> list[int]:
    ans = []
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
    if degree(f) != d or not (f & 1):
        return False
    x = 0b10
    frob = x
    powers = {0: x}
    for k in range(1, d + 1):
        frob = mul(frob, frob, f, d)
        powers[k] = frob
    if powers[d] != x:
        return False
    return all(poly_gcd(powers[d // q] ^ x, f) == 1 for q in prime_divisors(d))


def first_irreducible(d: int) -> int:
    for low in range(1, 1 << d, 2):
        f = (1 << d) | low
        if is_irreducible(f, d):
            return f
    raise AssertionError(f"no irreducible polynomial of degree {d}")


def rank(columns: list[int], width: int) -> int:
    rows = [x for x in columns if x]
    r = 0
    for bit in range(width):
        pivot = next((i for i in range(r, len(rows)) if (rows[i] >> bit) & 1), None)
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        for i in range(len(rows)):
            if i != r and ((rows[i] >> bit) & 1):
                rows[i] ^= rows[r]
        r += 1
    return r


def pairs(d: int) -> list[tuple[int, int]]:
    return [(i, j) for i in range(d) for j in range(i + 1, d)]


def cube(x: int, f: int, d: int) -> int:
    return mul(mul(x, x, f, d), x, f, d)


def cube_anf(d: int, f: int) -> tuple[list[int], list[int]]:
    linear = [cube(1 << i, f, d) for i in range(d)]
    quadratic = [
        cube((1 << i) ^ (1 << j), f, d) ^ linear[i] ^ linear[j]
        for i, j in pairs(d)
    ]
    return linear, quadratic


def eval_anf(x: int, linear: list[int], quadratic: list[int], d: int) -> int:
    out = 0
    for i, col in enumerate(linear):
        if (x >> i) & 1:
            out ^= col
    for (i, j), col in zip(pairs(d), quadratic):
        if ((x >> i) & 1) and ((x >> j) & 1):
            out ^= col
    return out


def friendship_edges(d: int) -> list[tuple[int, int]]:
    edges = []
    for i in range(d):
        a, b = 2 * i + 1, 2 * i + 2
        edges.extend([(0, a), (a, b), (0, b)])
    return edges


def lift(charge: list[int], z: int, d: int) -> list[int]:
    witness = [0] * (3 * d)
    for i in range(d):
        a, b = 2 * i + 1, 2 * i + 2
        zi = (z >> i) & 1
        witness[3 * i] = charge[a] ^ zi
        witness[3 * i + 1] = zi
        witness[3 * i + 2] = charge[b] ^ zi
    return witness


def boundary(witness: list[int], d: int) -> list[int]:
    out = [0] * (2 * d + 1)
    for bit, (u, v) in zip(witness, friendship_edges(d)):
        out[u] ^= bit
        out[v] ^= bit
    return out


def kss_lift(charge: list[int], z: int, s: int) -> list[int]:
    """Lift cotree values on K_{s,s}; edges are ordered (i,j)."""
    witness = [0] * (s * s)
    k = 0
    for i in range(1, s):
        for j in range(1, s):
            witness[i * s + j] = (z >> k) & 1
            k += 1
    for i in range(1, s):
        witness[i * s] = charge[i] ^ sum(witness[i * s + j] for j in range(1, s)) % 2
    for j in range(1, s):
        witness[j] = charge[s + j] ^ sum(witness[i * s + j] for i in range(1, s)) % 2
    witness[0] = charge[0] ^ sum(witness[j] for j in range(1, s)) % 2
    return witness


def kss_boundary(witness: list[int], s: int) -> list[int]:
    out = [0] * (2 * s)
    for i in range(s):
        for j in range(s):
            bit = witness[i * s + j]
            out[i] ^= bit
            out[s + j] ^= bit
    return out


def valid_record(record: dict) -> tuple[bool, str]:
    expected = {"degree", "modulus", "charge", "target"}
    if set(record) != expected:
        return False, "key-set"
    d = record["degree"]
    if not isinstance(d, int) or d < 3 or d % 2 == 0:
        return False, "odd-degree"
    f = record["modulus"]
    if not isinstance(f, int) or not is_irreducible(f, d):
        return False, "irreducible-modulus"
    charge = record["charge"]
    if not isinstance(charge, list) or len(charge) != 2 * d + 1 or any(x not in (0, 1) for x in charge):
        return False, "charge-shape"
    if sum(charge) & 1:
        return False, "charge-parity"
    target = record["target"]
    if not isinstance(target, int) or not 0 <= target < (1 << d):
        return False, "target-range"
    return True, "ok"


def main() -> None:
    started = time.perf_counter()
    rng = random.Random(SEED)
    checks = 0
    failures: list[str] = []
    records = []

    def check(condition: bool, label: str) -> None:
        nonlocal checks
        checks += 1
        if not condition:
            failures.append(label)

    for d in DEGREES:
        f = first_irreducible(d)
        q = 1 << d
        inverse_exponent = ((1 << (d + 1)) - 1) // 3
        linear, quadratic = cube_anf(d, f)
        check(rank(quadratic, d) == d, f"zero-polar-kernel-d{d}")
        outputs = set()
        for x in range(q):
            y = cube(x, f, d)
            outputs.add(y)
            check(eval_anf(x, linear, quadratic, d) == y, f"quadratic-anf-d{d}-x{x}")
            inv = power(y, inverse_exponent, f, d)
            check(inv == x, f"inverse-d{d}-x{x}")
        check(len(outputs) == q, f"permutation-d{d}")

        targets_checked = 0
        witnesses_checked = 0
        for charge_index in range(4):
            charge = [rng.randrange(2) for _ in range(2 * d + 1)]
            charge[0] ^= sum(charge) & 1
            record = {"degree": d, "modulus": f, "charge": charge, "target": 0}
            ok, why = valid_record(record)
            check(ok and why == "ok", f"recognize-d{d}-c{charge_index}-{why}")
            for target in range(q):
                z = power(target, inverse_exponent, f, d)
                witness = lift(charge, z, d)
                check(boundary(witness, d) == charge, f"boundary-d{d}-c{charge_index}-b{target}")
                cotree = sum(witness[3 * i + 1] << i for i in range(d))
                check(cotree == z, f"cotree-d{d}-c{charge_index}-b{target}")
                check(cube(cotree, f, d) == target, f"residual-d{d}-c{charge_index}-b{target}")
                targets_checked += 1
                witnesses_checked += 1

        records.append({
            "degree": d,
            "field_size": q,
            "irreducible_modulus": f,
            "inverse_exponent": inverse_exponent,
            "quadratic_columns": len(quadratic),
            "quadratic_output_span_rank": rank(quadratic, d),
            "polar_output_kernel_dimension": d - rank(quadratic, d),
            "targets_checked": targets_checked,
            "complete_tseitin_witnesses_checked": witnesses_checked,
            "graph_vertices": 2 * d + 1,
            "graph_edges": 3 * d,
            "cycle_rank": d,
        })

    # Unbounded-treewidth typed control: even K_{s,s} has odd cotree dimension
    # d=(s-1)^2, so the same cube theorem applies.  Audit the smallest case.
    s = 4
    kss_d = (s - 1) ** 2
    f = first_irreducible(kss_d)
    inverse_exponent = ((1 << (kss_d + 1)) - 1) // 3
    kss_witnesses = 0
    for charge_index in range(4):
        charge = [rng.randrange(2) for _ in range(2 * s)]
        charge[0] ^= sum(charge) & 1
        for target in range(1 << kss_d):
            z = power(target, inverse_exponent, f, kss_d)
            witness = kss_lift(charge, z, s)
            check(kss_boundary(witness, s) == charge,
                  f"kss-boundary-s{s}-c{charge_index}-b{target}")
            cotree = 0
            k = 0
            for i in range(1, s):
                for j in range(1, s):
                    cotree |= witness[i * s + j] << k
                    k += 1
            check(cotree == z, f"kss-cotree-s{s}-c{charge_index}-b{target}")
            check(cube(cotree, f, kss_d) == target,
                  f"kss-residual-s{s}-c{charge_index}-b{target}")
            kss_witnesses += 1

    d = 5
    f = first_irreducible(d)
    valid_charge = [0] * (2 * d + 1)
    controls = [
        ({"degree": 4, "modulus": first_irreducible(4), "charge": [0] * 9, "target": 0}, "odd-degree"),
        ({"degree": d, "modulus": (1 << d) | 1, "charge": valid_charge, "target": 0}, "irreducible-modulus"),
        ({"degree": d, "modulus": f, "charge": [1] + [0] * (2 * d), "target": 0}, "charge-parity"),
        ({"degree": d, "modulus": f, "charge": valid_charge, "target": 1 << d}, "target-range"),
        ({"degree": d, "modulus": f, "charge": valid_charge}, "key-set"),
    ]
    control_results = []
    for record, expected in controls:
        ok, why = valid_record(record)
        check(not ok and why == expected, f"control-{expected}-{why}")
        control_results.append({"expected": expected, "accepted": ok, "reason": why})

    elapsed = time.perf_counter() - started
    result = {
        "run_id": RUN_ID,
        "status": "PASS" if not failures else "FAIL",
        "seed": SEED,
        "degrees": list(DEGREES),
        "checks": checks,
        "failures": failures,
        "elapsed_seconds": elapsed,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "records": records,
        "kss_control": {
            "s": s,
            "cycle_rank": kss_d,
            "treewidth": s,
            "targets_per_charge": 1 << kss_d,
            "complete_witnesses_checked": kss_witnesses,
        },
        "off_image_controls": control_results,
        "scope": "symbolic Gold-cube theorem plus bounded exhaustive audit; no arbitrary-MQ or runtime lower bound",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
