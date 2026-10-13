#!/usr/bin/env python3
"""Audit a bijective quadratic residual with an explicit polynomial inverse.

This is a hostile control for claims that low collision entropy, singleton
fibers, high projected affine rank, nonlinearity, or dense affine wrappers
force hard witness search after Tseitin elimination.
"""

from __future__ import annotations

import hashlib
import json
import random
import time
from pathlib import Path

from field_trace_tseitin_bridge_audit import (
    boundary,
    invert,
    lift,
    mat_vec,
    parity,
    project_cotree,
    random_invertible,
    rank,
)

SEED = 22122026
SCHEMA = "BIJECTIVE-QUADRATIC-TSEITIN/v1"
KEYS = {"schema", "side", "charge", "input_matrix", "output_matrix",
        "input_phase", "output_phase", "target"}
OUT = Path("results/raw/review/2026-10-13_2212_bijective_quadratic_residual.json")


def triangular(z: int, d: int) -> int:
    out = z & 3
    z0 = z & 1
    for i in range(2, d):
        bit = ((z >> i) & 1) ^ (z0 & ((z >> (i - 1)) & 1))
        out |= bit << i
    return out


def triangular_inverse(w: int, d: int) -> int:
    z = w & 3
    z0 = z & 1
    for i in range(2, d):
        prev = (z >> (i - 1)) & 1
        bit = ((w >> i) & 1) ^ (z0 & prev)
        z |= bit << i
    return z


def recognize(obj: object) -> tuple[bool, str]:
    if not isinstance(obj, dict) or set(obj) != KEYS:
        return False, "schema-keys"
    if obj["schema"] != SCHEMA:
        return False, "schema-tag"
    for key in ("side", "charge", "input_phase", "output_phase", "target"):
        if type(obj[key]) is not int:
            return False, "integer-fields"
    s = obj["side"]
    if s < 3 or s % 2 == 0:
        return False, "side"
    d = (s - 1) ** 2
    if obj["charge"] < 0 or obj["charge"] >= 1 << (2 * s) or parity(obj["charge"]):
        return False, "charge"
    for key in ("input_phase", "output_phase", "target"):
        if obj[key] < 0 or obj[key] >= 1 << d:
            return False, key
    for key in ("input_matrix", "output_matrix"):
        rows = obj[key]
        if not isinstance(rows, list) or len(rows) != d or any(type(x) is not int for x in rows):
            return False, key + "-shape"
        if any(x < 0 or x >= 1 << d for x in rows) or rank(rows, d) != d:
            return False, key + "-rank"
    return True, "ok"


def residual(obj: dict, edge_assignment: int) -> int:
    s = obj["side"]
    d = (s - 1) ** 2
    y = project_cotree(s, edge_assignment)
    z = mat_vec(obj["input_matrix"], y) ^ obj["input_phase"]
    return mat_vec(obj["output_matrix"], triangular(z, d)) ^ obj["output_phase"]


def solve(obj: dict) -> int:
    ok, why = recognize(obj)
    if not ok:
        raise ValueError(why)
    s = obj["side"]
    d = (s - 1) ** 2
    binv = invert(obj["output_matrix"], d)
    ainv = invert(obj["input_matrix"], d)
    w = mat_vec(binv, obj["target"] ^ obj["output_phase"])
    z = triangular_inverse(w, d)
    y = mat_vec(ainv, z ^ obj["input_phase"])
    return lift(s, obj["charge"], y)


def matrix_density(rows: list[int], d: int) -> float:
    return sum(x.bit_count() for x in rows) / (d * d)


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

    # Exact truth tables for the two smallest legal dimensions.
    for d in (4, 16):
        seen = set()
        for z in range(1 << d):
            w = triangular(z, d)
            check(triangular_inverse(w, d) == z, f"inverse-d{d}-z{z}")
            seen.add(w)
        check(len(seen) == 1 << d, f"bijection-d{d}")

    # Actual Tseitin embeddings; larger dimensions are sampled, not exhausted.
    for s in (3, 5, 7, 9):
        d = (s - 1) ** 2
        arows = random_invertible(d, rng)
        brows = random_invertible(d, rng)
        iphase = rng.randrange(1 << d)
        ophase = rng.randrange(1 << d)
        charge = rng.randrange(1 << (2 * s))
        if parity(charge):
            charge ^= 1
        targets = range(1 << d) if d == 4 else [rng.randrange(1 << d) for _ in range(64)]
        for tnum, target in enumerate(targets):
            obj = {"schema": SCHEMA, "side": s, "charge": charge,
                   "input_matrix": arows, "output_matrix": brows,
                   "input_phase": iphase, "output_phase": ophase,
                   "target": target}
            ok, why = recognize(obj)
            check(ok and why == "ok", f"recognize-s{s}-t{tnum}")
            x = solve(obj)
            check(boundary(s, x) == charge, f"boundary-s{s}-t{tnum}")
            check(residual(obj, x) == target, f"residual-s{s}-t{tnum}")
        # Linear part is a full cotree interface and the quadratic core is genuine.
        check(triangular(0, d) == 0, f"zero-s{s}")
        check(triangular(1 | (1 << 2), d) != (1 | (1 << 2)), f"nonlinear-s{s}")
        encoded = len(json.dumps(obj, separators=(",", ":")).encode())
        records.append({"side": s, "cotree_dim": d, "edges": s * s,
                        "targets_checked": len(list(targets)) if not isinstance(targets, range) else len(targets),
                        "input_matrix_density": matrix_density(arows, d),
                        "output_matrix_density": matrix_density(brows, d),
                        "encoded_json_bytes": encoded})

    base = {"schema": SCHEMA, "side": 3, "charge": 0,
            "input_matrix": [1 << i for i in range(4)],
            "output_matrix": [1 << i for i in range(4)],
            "input_phase": 0, "output_phase": 0, "target": 0}
    malformed = []
    for label, mutate in [
        ("missing-key", lambda q: q.pop("target")),
        ("bad-tag", lambda q: q.__setitem__("schema", "bad")),
        ("even-side", lambda q: q.__setitem__("side", 4)),
        ("odd-charge", lambda q: q.__setitem__("charge", 1)),
        ("target-range", lambda q: q.__setitem__("target", 16)),
        ("input-singular", lambda q: q.__setitem__("input_matrix", [1, 2, 4, 4])),
        ("output-shape", lambda q: q.__setitem__("output_matrix", [1, 2, 4])),
    ]:
        q = dict(base)
        mutate(q)
        ok, why = recognize(q)
        check(not ok, "malformed-" + label)
        malformed.append({"case": label, "reason": why})

    elapsed = time.perf_counter() - start
    result = {
        "run_id": "BIJECTIVEQFW1",
        "status": "PASS" if not failures else "FAIL",
        "seed": SEED,
        "checks": checks,
        "failures": failures,
        "elapsed_seconds": elapsed,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "records": records,
        "malformed_controls": malformed,
        "exact_fiber_size": 1,
        "collision_count_for_dimension_d": "2^d",
        "scope": "exact symbolic bijection plus bounded audit; no general MQ or runtime lower bound",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
