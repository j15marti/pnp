#!/usr/bin/env python3
"""Audit quadratic payload shears after affine Tseitin elimination.

For any explicit Boolean quadratic payload P, the map

    S_P(u,v) = (u, v + P(u))

is an involution.  This is a hostile control for attempts to infer witness
search time from many nonlinear coordinates, dense quadratic relation spaces,
singleton fibers, or full projected affine rank.  The audit uses exact small
truth tables and complete K_{s,s} Tseitin witness reconstruction.
"""

from __future__ import annotations

import hashlib
import json
import random
import time
from pathlib import Path


SEED = 22242026
SCHEMA = "QUADRATIC-PAYLOAD-SHEAR-TSEITIN/v1"
OUT = Path("results/raw/review/2026-10-13_2224_quadratic_payload_shear.json")
KEYS = {
    "schema", "side", "charge", "split", "quadratic_masks",
    "linear_masks", "constants", "input_matrix", "output_matrix",
    "input_phase", "output_phase", "target",
}


def parity(x: int) -> int:
    return x.bit_count() & 1


def mat_vec(rows: list[int], x: int) -> int:
    out = 0
    for i, row in enumerate(rows):
        out |= parity(row & x) << i
    return out


def rank(rows: list[int], width: int) -> int:
    a = list(rows)
    r = 0
    for col in range(width):
        pivot = next((i for i in range(r, len(a)) if (a[i] >> col) & 1), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        for i in range(len(a)):
            if i != r and ((a[i] >> col) & 1):
                a[i] ^= a[r]
        r += 1
    return r


def invert(rows: list[int], d: int) -> list[int]:
    aug = [rows[i] | (1 << (d + i)) for i in range(d)]
    for col in range(d):
        pivot = next((i for i in range(col, d) if (aug[i] >> col) & 1), None)
        if pivot is None:
            raise ValueError("singular")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        for i in range(d):
            if i != col and ((aug[i] >> col) & 1):
                aug[i] ^= aug[col]
    return [(row >> d) & ((1 << d) - 1) for row in aug]


def random_invertible(d: int, rng: random.Random) -> list[int]:
    rows = [1 << i for i in range(d)]
    for _ in range(8 * d + 1):
        i, j = rng.sample(range(d), 2)
        rows[i] ^= rows[j]
        if rng.randrange(2):
            rows[i], rows[j] = rows[j], rows[i]
    return rows


def pair_list(m: int) -> list[tuple[int, int]]:
    return [(i, j) for i in range(m) for j in range(i + 1, m)]


def random_independent_masks(count: int, width: int, rng: random.Random) -> list[int]:
    rows: list[int] = []
    while len(rows) < count:
        x = rng.randrange(1, 1 << width)
        if rank(rows + [x], width) == len(rows) + 1:
            rows.append(x)
    return rows


def payload_value(u: int, m: int, q_masks: list[int], linear: list[int], constants: int) -> int:
    mon = 0
    for k, (i, j) in enumerate(pair_list(m)):
        mon |= (((u >> i) & 1) & ((u >> j) & 1)) << k
    out = 0
    for j, (qmask, lmask) in enumerate(zip(q_masks, linear)):
        bit = parity(qmask & mon) ^ parity(lmask & u) ^ ((constants >> j) & 1)
        out |= bit << j
    return out


def shear(z: int, m: int, n: int, q_masks: list[int], linear: list[int], constants: int) -> int:
    u = z & ((1 << m) - 1)
    v = (z >> m) & ((1 << n) - 1)
    return u | ((v ^ payload_value(u, m, q_masks, linear, constants)) << m)


def output_quadratic_mask(row: int, m: int, n: int, q_masks: list[int]) -> int:
    ans = 0
    for j in range(n):
        if (row >> (m + j)) & 1:
            ans ^= q_masks[j]
    return ans


def nonlinear_output_matrix(d: int, m: int, n: int, q_masks: list[int], rng: random.Random) -> list[int]:
    for _ in range(2000):
        rows = random_invertible(d, rng)
        if all(output_quadratic_mask(row, m, n, q_masks) for row in rows):
            return rows
    raise AssertionError("failed to sample an invertible all-nonlinear output mixing")


def boundary(s: int, x: int) -> int:
    out = 0
    for i in range(s):
        bit = 0
        for j in range(s):
            bit ^= (x >> (i * s + j)) & 1
        out |= bit << i
    for j in range(s):
        bit = 0
        for i in range(s):
            bit ^= (x >> (i * s + j)) & 1
        out |= bit << (s + j)
    return out


def project_cotree(s: int, x: int) -> int:
    y = 0
    k = 0
    for i in range(1, s):
        for j in range(1, s):
            y |= ((x >> (i * s + j)) & 1) << k
            k += 1
    return y


def lift(s: int, charge: int, y: int) -> int:
    if parity(charge):
        raise ValueError("inconsistent charge")
    x = 0
    k = 0
    for i in range(1, s):
        for j in range(1, s):
            x |= ((y >> k) & 1) << (i * s + j)
            k += 1
    for i in range(1, s):
        bit = (charge >> i) & 1
        for j in range(1, s):
            bit ^= (x >> (i * s + j)) & 1
        x |= bit << (i * s)
    for j in range(1, s):
        bit = (charge >> (s + j)) & 1
        for i in range(1, s):
            bit ^= (x >> (i * s + j)) & 1
        x |= bit << j
    bit = charge & 1
    for j in range(1, s):
        bit ^= (x >> j) & 1
    x |= bit
    if boundary(s, x) != charge:
        raise AssertionError("forest lift failed")
    return x


def recognize(obj: object) -> tuple[bool, str]:
    if not isinstance(obj, dict) or set(obj) != KEYS:
        return False, "schema-keys"
    if obj["schema"] != SCHEMA:
        return False, "schema-tag"
    for key in ("side", "charge", "split", "constants", "input_phase", "output_phase", "target"):
        if type(obj[key]) is not int:
            return False, "integer-fields"
    s = obj["side"]
    if s < 5 or s % 2 == 0:
        return False, "side"
    d = (s - 1) ** 2
    m = obj["split"]
    n = d - m
    if m < 2 or n < 1 or n > m * (m - 1) // 2:
        return False, "split"
    if obj["charge"] < 0 or obj["charge"] >= 1 << (2 * s) or parity(obj["charge"]):
        return False, "charge"
    if obj["constants"] < 0 or obj["constants"] >= 1 << n:
        return False, "constants"
    for key in ("input_phase", "output_phase", "target"):
        if obj[key] < 0 or obj[key] >= 1 << d:
            return False, key
    qwidth = m * (m - 1) // 2
    q_masks = obj["quadratic_masks"]
    linear = obj["linear_masks"]
    if not isinstance(q_masks, list) or len(q_masks) != n or any(type(x) is not int or x <= 0 or x >= 1 << qwidth for x in q_masks):
        return False, "quadratic-masks"
    if rank(q_masks, qwidth) != n:
        return False, "quadratic-rank"
    if not isinstance(linear, list) or len(linear) != n or any(type(x) is not int or x < 0 or x >= 1 << m for x in linear):
        return False, "linear-masks"
    for key in ("input_matrix", "output_matrix"):
        rows = obj[key]
        if not isinstance(rows, list) or len(rows) != d or any(type(x) is not int or x < 0 or x >= 1 << d for x in rows):
            return False, key + "-shape"
        if rank(rows, d) != d:
            return False, key + "-rank"
    if any(output_quadratic_mask(row, m, n, q_masks) == 0 for row in obj["output_matrix"]):
        return False, "output-linear-coordinate"
    return True, "ok"


def residual(obj: dict, edge_assignment: int) -> int:
    s = obj["side"]
    d = (s - 1) ** 2
    m = obj["split"]
    n = d - m
    y = project_cotree(s, edge_assignment)
    z = mat_vec(obj["input_matrix"], y) ^ obj["input_phase"]
    w = shear(z, m, n, obj["quadratic_masks"], obj["linear_masks"], obj["constants"])
    return mat_vec(obj["output_matrix"], w) ^ obj["output_phase"]


def solve(obj: dict) -> int:
    ok, why = recognize(obj)
    if not ok:
        raise ValueError(why)
    s = obj["side"]
    d = (s - 1) ** 2
    m = obj["split"]
    n = d - m
    w = mat_vec(invert(obj["output_matrix"], d), obj["target"] ^ obj["output_phase"])
    z = shear(w, m, n, obj["quadratic_masks"], obj["linear_masks"], obj["constants"])
    y = mat_vec(invert(obj["input_matrix"], d), z ^ obj["input_phase"])
    return lift(s, obj["charge"], y)


def make_payload(m: int, n: int, rng: random.Random) -> tuple[list[int], list[int], int]:
    q_masks = random_independent_masks(n, m * (m - 1) // 2, rng)
    linear = [rng.randrange(1 << m) for _ in range(n)]
    constants = rng.randrange(1 << n)
    return q_masks, linear, constants


def main() -> None:
    start = time.perf_counter()
    rng = random.Random(SEED)
    checks = 0
    failures: list[str] = []
    records = []

    def check(cond: bool, label: str) -> None:
        nonlocal checks
        checks += 1
        if not cond:
            failures.append(label)

    # Exhaustive truth tables for two arbitrary dense payloads on seven bits.
    for trial in range(2):
        m, n, d = 4, 3, 7
        q_masks, linear, constants = make_payload(m, n, rng)
        seen = set()
        for z in range(1 << d):
            w = shear(z, m, n, q_masks, linear, constants)
            check(shear(w, m, n, q_masks, linear, constants) == z,
                  f"involution-t{trial}-z{z}")
            seen.add(w)
        check(len(seen) == 1 << d, f"singleton-fibers-t{trial}")
        check(rank(q_masks, m * (m - 1) // 2) == n, f"payload-rank-t{trial}")

    # Complete Tseitin reconstruction after explicit dense affine conjugation.
    for s in (5, 7, 9):
        d = (s - 1) ** 2
        m = d // 2
        n = d - m
        q_masks, linear, constants = make_payload(m, n, rng)
        arows = random_invertible(d, rng)
        brows = nonlinear_output_matrix(d, m, n, q_masks, rng)
        iphase = rng.randrange(1 << d)
        ophase = rng.randrange(1 << d)
        charge = rng.randrange(1 << (2 * s))
        if parity(charge):
            charge ^= 1
        targets = [rng.randrange(1 << d) for _ in range(64)]
        obj = None
        for tnum, target in enumerate(targets):
            obj = {
                "schema": SCHEMA, "side": s, "charge": charge, "split": m,
                "quadratic_masks": q_masks, "linear_masks": linear,
                "constants": constants, "input_matrix": arows,
                "output_matrix": brows, "input_phase": iphase,
                "output_phase": ophase, "target": target,
            }
            ok, why = recognize(obj)
            check(ok and why == "ok", f"recognize-s{s}-t{tnum}")
            x = solve(obj)
            check(boundary(s, x) == charge, f"boundary-s{s}-t{tnum}")
            check(residual(obj, x) == target, f"residual-s{s}-t{tnum}")
        assert obj is not None
        quadratic_supports = [output_quadratic_mask(row, m, n, q_masks).bit_count() for row in brows]
        check(min(quadratic_supports) > 0, f"all-output-coordinates-nonlinear-s{s}")
        check(rank(q_masks, m * (m - 1) // 2) == n, f"independent-payload-s{s}")
        records.append({
            "side": s, "cotree_dimension": d, "payload_input_bits": m,
            "payload_output_bits": n, "quadratic_monomials": m * (m - 1) // 2,
            "quadratic_relation_rank": rank(q_masks, m * (m - 1) // 2),
            "minimum_output_quadratic_support": min(quadratic_supports),
            "maximum_output_quadratic_support": max(quadratic_supports),
            "targets_and_witnesses_checked": len(targets),
            "encoded_json_bytes": len(json.dumps(obj, separators=(",", ":")).encode()),
        })

    # Malformed and off-domain controls.
    s = 5
    d = 16
    m = n = 8
    q_masks, linear, constants = make_payload(m, n, rng)
    base = {
        "schema": SCHEMA, "side": s, "charge": 0, "split": m,
        "quadratic_masks": q_masks, "linear_masks": linear,
        "constants": constants, "input_matrix": [1 << i for i in range(d)],
        "output_matrix": nonlinear_output_matrix(d, m, n, q_masks, rng),
        "input_phase": 0, "output_phase": 0, "target": 0,
    }
    malformed = []
    cases = [
        ("missing-key", lambda q: q.pop("target")),
        ("bad-tag", lambda q: q.__setitem__("schema", "bad")),
        ("small-side", lambda q: q.__setitem__("side", 3)),
        ("even-side", lambda q: q.__setitem__("side", 6)),
        ("odd-charge", lambda q: q.__setitem__("charge", 1)),
        ("bad-split", lambda q: q.__setitem__("split", 1)),
        ("dependent-payload", lambda q: q.__setitem__("quadratic_masks", [q_masks[0]] * n)),
        ("input-singular", lambda q: q.__setitem__("input_matrix", [1 << i for i in range(d - 1)] + [1 << (d - 2)])),
        ("target-range", lambda q: q.__setitem__("target", 1 << d)),
    ]
    for label, mutate in cases:
        q = dict(base)
        mutate(q)
        ok, why = recognize(q)
        check(not ok, "malformed-" + label)
        malformed.append({"case": label, "reason": why})

    elapsed = time.perf_counter() - start
    result = {
        "run_id": "QUADSHEAR1",
        "status": "PASS" if not failures else "FAIL",
        "seed": SEED,
        "checks": checks,
        "failures": failures,
        "elapsed_seconds": elapsed,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "records": records,
        "malformed_controls": malformed,
        "exact_identity": "S_P(S_P(u,v))=(u,v) for every explicit Boolean quadratic P",
        "fiber_size": 1,
        "scope": "symbolic involution plus bounded exhaustive/sample audit; no arbitrary-MQ or runtime lower bound",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
