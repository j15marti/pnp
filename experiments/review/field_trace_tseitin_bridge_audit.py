#!/usr/bin/env python3
"""Bounded audit of a field-trace residual embedded in a Tseitin coset.

The program is deliberately self-contained.  It checks the exact recognizer,
the K_{s,s} cotree parametrization, affine mixing, the uniform selector for
Q(u,v)=uv, polar ranks, fiber counts, and malformed/off-image rejection.
All arithmetic is over GF(2), with GF(2^r) represented by a validated monic
irreducible polynomial.
"""

from __future__ import annotations

import hashlib
import json
import random
import time
from pathlib import Path

SEED = 22042026
OUT = Path("results/raw/review/2026-10-13_2204_field_trace_tseitin_bridge.json")
SCHEMA = "FIELDTRACE-TSEITIN-BRIDGE/v1"
KEYS = {"schema", "side", "modulus", "charge", "matrix", "phase", "target"}


def pdeg(p: int) -> int:
    return p.bit_length() - 1


def pmul(a: int, b: int) -> int:
    out = 0
    while b:
        if b & 1:
            out ^= a
        a <<= 1
        b >>= 1
    return out


def pmod(a: int, f: int) -> int:
    df = pdeg(f)
    while pdeg(a) >= df:
        a ^= f << (pdeg(a) - df)
    return a


def pgcd(a: int, b: int) -> int:
    while b:
        a, b = b, pmod(a, b)
    return a


def gf_mul(a: int, b: int, f: int, r: int) -> int:
    return pmod(pmul(a, b), f) & ((1 << r) - 1)


def gf_square(a: int, f: int, r: int) -> int:
    return gf_mul(a, a, f, r)


def irreducible(f: int, r: int) -> bool:
    if pdeg(f) != r or not (f & 1):
        return False
    x = pmod(2, f)
    y = x
    for _ in range(1, r // 2 + 1):
        y = gf_square(y, f, r)
        if pgcd(y ^ x, f) != 1:
            return False
    y = x
    for _ in range(r):
        y = gf_square(y, f, r)
    return y == x


def find_irreducible(r: int) -> int:
    for low in range(1, 1 << r, 2):
        f = (1 << r) | low
        if irreducible(f, r):
            return f
    raise AssertionError("no irreducible polynomial found")


def gf_trace(a: int, f: int, r: int) -> int:
    acc = 0
    cur = a
    for _ in range(r):
        acc ^= cur
        cur = gf_square(cur, f, r)
    assert acc in (0, 1)
    return acc


def parity(x: int) -> int:
    return x.bit_count() & 1


def mat_vec(rows: list[int], x: int) -> int:
    out = 0
    for i, row in enumerate(rows):
        out |= parity(row & x) << i
    return out


def rank(rows: list[int], ncols: int) -> int:
    a = rows[:]
    rr = 0
    for col in range(ncols):
        pivot = next((i for i in range(rr, len(a)) if (a[i] >> col) & 1), None)
        if pivot is None:
            continue
        a[rr], a[pivot] = a[pivot], a[rr]
        for i in range(len(a)):
            if i != rr and ((a[i] >> col) & 1):
                a[i] ^= a[rr]
        rr += 1
    return rr


def invert(rows: list[int], n: int) -> list[int]:
    a = [rows[i] | (1 << (n + i)) for i in range(n)]
    rr = 0
    for col in range(n):
        pivot = next((i for i in range(rr, n) if (a[i] >> col) & 1), None)
        if pivot is None:
            raise ValueError("singular matrix")
        a[rr], a[pivot] = a[pivot], a[rr]
        for i in range(n):
            if i != rr and ((a[i] >> col) & 1):
                a[i] ^= a[rr]
        rr += 1
    return [(a[i] >> n) & ((1 << n) - 1) for i in range(n)]


def random_invertible(n: int, rng: random.Random) -> list[int]:
    rows = [1 << i for i in range(n)]
    for _ in range(8 * n):
        i, j = rng.sample(range(n), 2)
        if rng.randrange(2):
            rows[i] ^= rows[j]
        else:
            rows[i], rows[j] = rows[j], rows[i]
    assert rank(rows, n) == n
    return rows


def edge_index(s: int, i: int, j: int) -> int:
    return i * s + j


def boundary(s: int, edge_bits: int) -> int:
    out = 0
    for i in range(s):
        for j in range(s):
            if (edge_bits >> edge_index(s, i, j)) & 1:
                out ^= 1 << i
                out ^= 1 << (s + j)
    return out


def cotree_edges(s: int) -> list[int]:
    return [edge_index(s, i, j) for i in range(1, s) for j in range(1, s)]


def lift(s: int, charge: int, cotree: int) -> int:
    """Unique lift with prescribed cotree values on the star-of-stars tree."""
    x = 0
    for k, e in enumerate(cotree_edges(s)):
        if (cotree >> k) & 1:
            x |= 1 << e
    rem = charge ^ boundary(s, x)
    for i in range(1, s):
        if (rem >> i) & 1:
            e = edge_index(s, i, 0)
            x |= 1 << e
            rem ^= (1 << i) | (1 << s)
    for j in range(1, s):
        if (rem >> (s + j)) & 1:
            e = edge_index(s, 0, j)
            x |= 1 << e
            rem ^= 1 | (1 << (s + j))
    if (rem >> s) & 1:
        x |= 1 << edge_index(s, 0, 0)
        rem ^= 1 | (1 << s)
    if rem:
        raise ValueError("inconsistent charge")
    assert boundary(s, x) == charge
    return x


def project_cotree(s: int, x: int) -> int:
    out = 0
    for k, e in enumerate(cotree_edges(s)):
        out |= ((x >> e) & 1) << k
    return out


def recognize(obj: object) -> tuple[bool, str]:
    if not isinstance(obj, dict) or set(obj) != KEYS:
        return False, "schema-keys"
    if obj["schema"] != SCHEMA:
        return False, "schema-tag"
    vals = [obj[k] for k in ("side", "modulus", "charge", "phase", "target")]
    if any(type(v) is not int for v in vals):
        return False, "integer-fields"
    s = obj["side"]
    if s < 3 or s % 2 == 0:
        return False, "side"
    d = (s - 1) ** 2
    if d % 2:
        return False, "cotree-parity"
    r = d // 2
    if not irreducible(obj["modulus"], r):
        return False, "modulus"
    if obj["charge"] < 0 or obj["charge"] >= (1 << (2 * s)) or parity(obj["charge"]):
        return False, "charge"
    if obj["phase"] < 0 or obj["phase"] >= (1 << d):
        return False, "phase"
    if obj["target"] < 0 or obj["target"] >= (1 << r):
        return False, "target"
    rows = obj["matrix"]
    if not isinstance(rows, list) or len(rows) != d or any(type(v) is not int for v in rows):
        return False, "matrix-shape"
    if any(v < 0 or v >= (1 << d) for v in rows) or rank(rows, d) != d:
        return False, "matrix-rank"
    return True, "ok"


def solve_record(obj: dict) -> int:
    ok, why = recognize(obj)
    if not ok:
        raise ValueError(why)
    s = obj["side"]
    d = (s - 1) ** 2
    r = d // 2
    z = 1 | (obj["target"] << r)  # (u,v)=(1,b), little-endian blocks
    inv = invert(obj["matrix"], d)
    y = mat_vec(inv, z ^ obj["phase"])
    return lift(s, obj["charge"], y)


def residual_value(obj: dict, x: int) -> int:
    s = obj["side"]
    d = (s - 1) ** 2
    r = d // 2
    y = project_cotree(s, x)
    z = mat_vec(obj["matrix"], y) ^ obj["phase"]
    u = z & ((1 << r) - 1)
    v = z >> r
    return gf_mul(u, v, obj["modulus"], r)


def polar_rows(lam: int, f: int, r: int) -> list[int]:
    n = 2 * r
    rows = []
    for i in range(n):
        row = 0
        xi = 1 << i
        x, y = xi & ((1 << r) - 1), xi >> r
        for j in range(n):
            xj = 1 << j
            xp, yp = xj & ((1 << r) - 1), xj >> r
            val = gf_trace(gf_mul(lam, gf_mul(x, yp, f, r) ^ gf_mul(xp, y, f, r), f, r), f, r)
            row |= val << j
        rows.append(row)
    return rows


def congruence(rows_a: list[int], rows_m: list[int], n: int) -> list[int]:
    """Rows of A^T M A, with matrices stored by rows over GF(2)."""
    cols_a = [mat_vec(rows_a, 1 << j) for j in range(n)]
    out = []
    for i in range(n):
        row = 0
        mi = mat_vec(rows_m, cols_a[i])
        for j in range(n):
            row |= parity(mi & cols_a[j]) << j
        out.append(row)
    return out


def exact_fibers(f: int, r: int) -> list[int]:
    counts = [0] * (1 << r)
    for u in range(1 << r):
        for v in range(1 << r):
            counts[gf_mul(u, v, f, r)] += 1
    return counts


def main() -> None:
    started = time.perf_counter()
    rng = random.Random(SEED)
    checks = 0
    failures: list[str] = []
    cases = []

    def check(cond: bool, label: str) -> None:
        nonlocal checks
        checks += 1
        if not cond:
            failures.append(label)

    # Field theorem: exhaustive nonzero polar pencil and exact fibers to r=8.
    field_rows = []
    for r in range(1, 9):
        f = find_irreducible(r)
        check(irreducible(f, r), f"irreducible-r{r}")
        min_rank = 2 * r
        for lam in range(1, 1 << r):
            rr = rank(polar_rows(lam, f, r), 2 * r)
            min_rank = min(min_rank, rr)
            check(rr == 2 * r, f"polar-r{r}-lam{lam}")
        fibers = exact_fibers(f, r)
        check(fibers[0] == (1 << (r + 1)) - 1, f"fiber-zero-r{r}")
        for b in range(1, 1 << r):
            check(fibers[b] == (1 << r) - 1, f"fiber-nonzero-r{r}-b{b}")
        collision = sum(v * v for v in fibers)
        formula_collision = ((1 << (r + 1)) - 1) ** 2 + ((1 << r) - 1) ** 3
        check(collision == formula_collision, f"collision-r{r}")
        field_rows.append({"r": r, "modulus": f, "min_polar_rank": min_rank,
                           "fiber_zero": fibers[0], "fiber_nonzero": fibers[1] if r else None,
                           "collision": collision})

    # Fully typed K_{s,s} embeddings for the two bounded exhaustive sizes.
    for s in (3, 5):
        d = (s - 1) ** 2
        r = d // 2
        f = find_irreducible(r)
        rows = random_invertible(d, rng)
        inv = invert(rows, d)
        check(all(mat_vec(rows, mat_vec(inv, 1 << j)) == (1 << j) for j in range(d)), f"inverse-s{s}")
        phase = rng.randrange(1 << d)
        charge = rng.randrange(1 << (2 * s))
        if parity(charge):
            charge ^= 1
        # Explicit a and L checks.
        a = lift(s, charge, 0)
        check(boundary(s, a) == charge, f"a-boundary-s{s}")
        check(project_cotree(s, a) == 0, f"a-projection-s{s}")
        for j in range(d):
            col = lift(s, 0, 1 << j)
            check(boundary(s, col) == 0, f"L-kernel-s{s}-j{j}")
            check(project_cotree(s, col) == (1 << j), f"L-project-s{s}-j{j}")
        for trial in range(16):
            y = rng.randrange(1 << d)
            via_basis = a
            for j in range(d):
                if (y >> j) & 1:
                    via_basis ^= lift(s, 0, 1 << j)
            check(via_basis == lift(s, charge, y), f"aL-identity-s{s}-t{trial}")
        for lam in range(1, 1 << r):
            transformed = congruence(rows, polar_rows(lam, f, r), d)
            check(rank(transformed, d) == d, f"affine-polar-s{s}-lam{lam}")
        targets = range(1 << r)
        for b in targets:
            obj = {"schema": SCHEMA, "side": s, "modulus": f, "charge": charge,
                   "matrix": rows, "phase": phase, "target": b}
            ok, why = recognize(obj)
            check(ok and why == "ok", f"recognize-s{s}-b{b}")
            x = solve_record(obj)
            check(boundary(s, x) == charge, f"witness-boundary-s{s}-b{b}")
            check(residual_value(obj, x) == b, f"witness-residual-s{s}-b{b}")
        encoded = len(json.dumps(obj, separators=(",", ":")).encode())
        cases.append({"side": s, "vertices": 2 * s, "edges": s * s, "cotree_dim": d,
                      "field_degree": r, "targets_checked": 1 << r,
                      "encoded_json_bytes": encoded})

    # Exact malformed/off-image semantics: deterministic rejection.
    base = {"schema": SCHEMA, "side": 3, "modulus": find_irreducible(2), "charge": 0,
            "matrix": [1 << i for i in range(4)], "phase": 0, "target": 0}
    bad = []
    for label, mutate in [
        ("missing-key", lambda q: q.pop("target")),
        ("schema-tag", lambda q: q.__setitem__("schema", "wrong")),
        ("even-side", lambda q: q.__setitem__("side", 4)),
        ("reducible-modulus", lambda q: q.__setitem__("modulus", 5)),
        ("odd-charge", lambda q: q.__setitem__("charge", 1)),
        ("phase-range", lambda q: q.__setitem__("phase", 16)),
        ("target-range", lambda q: q.__setitem__("target", 4)),
        ("matrix-shape", lambda q: q.__setitem__("matrix", [1, 2, 4])),
        ("matrix-singular", lambda q: q.__setitem__("matrix", [1, 2, 4, 4])),
    ]:
        q = dict(base)
        mutate(q)
        ok, why = recognize(q)
        check(not ok, f"malformed-{label}")
        bad.append({"case": label, "reason": why})

    elapsed = time.perf_counter() - started
    script_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result = {
        "run_id": "FIELDTRACELIFT1",
        "status": "PASS" if not failures else "FAIL",
        "seed": SEED,
        "checks": checks,
        "failures": failures,
        "elapsed_seconds": elapsed,
        "script_sha256": script_hash,
        "field_audit": field_rows,
        "tseitin_cases": cases,
        "malformed_controls": bad,
        "scope": "bounded exact audit; no asymptotic runtime inference",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
