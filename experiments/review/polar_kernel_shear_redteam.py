#!/usr/bin/env python3
"""Independent red-team audit of affine-conjugated quadratic shears.

The inverter receives only the expanded Boolean quadratic ANF of a square map
F: GF(2)^d -> GF(2)^d and a target.  It is not given the shear split, payload,
or affine conjugating maps.  It recovers the space of affine output
combinations from the kernel of the output-polar map, fixes that quotient, and
then solves the remaining affine restriction by Gaussian elimination.
"""

from __future__ import annotations

import hashlib
import json
import random
import time
from dataclasses import dataclass
from pathlib import Path


SEED = 22362026
RUN_ID = "POLARKERNEL1"
OUT = Path("results/raw/review/2026-10-13_2236_polar_kernel_shear_redteam.json")


def parity(x: int) -> int:
    return x.bit_count() & 1


def rank(rows: list[int], width: int) -> int:
    a = [x for x in rows if x]
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
        if r == len(a):
            break
    return r


def nullspace(rows: list[int], width: int) -> list[int]:
    a = [x for x in rows if x]
    r = 0
    pivots: list[int] = []
    for col in range(width):
        pivot = next((i for i in range(r, len(a)) if (a[i] >> col) & 1), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        for i in range(len(a)):
            if i != r and ((a[i] >> col) & 1):
                a[i] ^= a[r]
        pivots.append(col)
        r += 1
        if r == len(a):
            break
    pivot_set = set(pivots)
    basis: list[int] = []
    for free in range(width):
        if free in pivot_set:
            continue
        x = 1 << free
        for i, p in enumerate(pivots):
            if (a[i] >> free) & 1:
                x |= 1 << p
        basis.append(x)
    return basis


def solve_linear(rows: list[int], rhs: list[int], width: int) -> tuple[int, list[int]] | None:
    aug = [rows[i] | ((rhs[i] & 1) << width) for i in range(len(rows))]
    r = 0
    pivots: list[int] = []
    for col in range(width):
        pivot = next((i for i in range(r, len(aug)) if (aug[i] >> col) & 1), None)
        if pivot is None:
            continue
        aug[r], aug[pivot] = aug[pivot], aug[r]
        for i in range(len(aug)):
            if i != r and ((aug[i] >> col) & 1):
                aug[i] ^= aug[r]
        pivots.append(col)
        r += 1
    mask = (1 << width) - 1
    if any((row & mask) == 0 and ((row >> width) & 1) for row in aug):
        return None
    x = 0
    for i, p in enumerate(pivots):
        if (aug[i] >> width) & 1:
            x |= 1 << p
    return x, nullspace(rows, width)


def mat_vec(rows: list[int], x: int) -> int:
    return sum(parity(row & x) << i for i, row in enumerate(rows))


def random_invertible(d: int, rng: random.Random) -> list[int]:
    rows = [1 << i for i in range(d)]
    for _ in range(10 * d + 3):
        i, j = rng.sample(range(d), 2)
        rows[i] ^= rows[j]
        if rng.randrange(2):
            rows[i], rows[j] = rows[j], rows[i]
    assert rank(rows, d) == d
    return rows


def pairs(d: int) -> list[tuple[int, int]]:
    return [(i, j) for i in range(d) for j in range(i + 1, d)]


def independent_masks(count: int, width: int, rng: random.Random) -> list[int]:
    ans: list[int] = []
    while len(ans) < count:
        x = rng.randrange(1, 1 << width)
        if rank(ans + [x], width) == len(ans) + 1:
            ans.append(x)
    return ans


def payload(u: int, m: int, q_masks: list[int], linear: list[int], constant: int) -> int:
    mon = 0
    for k, (i, j) in enumerate(pairs(m)):
        mon |= (((u >> i) & 1) & ((u >> j) & 1)) << k
    return sum((parity(q & mon) ^ parity(l & u) ^ ((constant >> j) & 1)) << j
               for j, (q, l) in enumerate(zip(q_masks, linear)))


def shear(z: int, m: int, n: int, q_masks: list[int], linear: list[int], constant: int) -> int:
    u = z & ((1 << m) - 1)
    v = (z >> m) & ((1 << n) - 1)
    return u | ((v ^ payload(u, m, q_masks, linear, constant)) << m)


def nonlinear_output_matrix(d: int, m: int, q_masks: list[int], rng: random.Random) -> list[int]:
    n = d - m
    for _ in range(5000):
        rows = random_invertible(d, rng)
        good = True
        for row in rows:
            mask = 0
            for j in range(n):
                if (row >> (m + j)) & 1:
                    mask ^= q_masks[j]
            good &= mask != 0
        if good:
            return rows
    raise AssertionError("failed to sample all-nonlinear output mixing")


@dataclass(frozen=True)
class QuadANF:
    d: int
    constant: int
    linear_columns: tuple[int, ...]
    quadratic_columns: tuple[int, ...]

    def evaluate(self, x: int) -> int:
        y = self.constant
        for i, col in enumerate(self.linear_columns):
            if (x >> i) & 1:
                y ^= col
        for (i, j), col in zip(pairs(self.d), self.quadratic_columns):
            if ((x >> i) & 1) and ((x >> j) & 1):
                y ^= col
        return y


def recover_anf(d: int, oracle) -> tuple[QuadANF, int]:
    c = oracle(0)
    values = [oracle(1 << i) for i in range(d)]
    linear = tuple(v ^ c for v in values)
    quad = []
    for i, j in pairs(d):
        quad.append(oracle((1 << i) ^ (1 << j)) ^ values[i] ^ values[j] ^ c)
    return QuadANF(d, c, linear, tuple(quad)), 1 + d + d * (d - 1) // 2


def polar_vector(anf: QuadANF, a: int, b: int) -> int:
    ans = 0
    for (i, j), col in zip(pairs(anf.d), anf.quadratic_columns):
        if (((a >> i) & 1) & ((b >> j) & 1)) ^ (((a >> j) & 1) & ((b >> i) & 1)):
            ans ^= col
    return ans


@dataclass(frozen=True)
class PolarKernelPlan:
    affine_covectors: tuple[int, ...]
    quotient_rows: tuple[int, ...]
    quotient_constants: tuple[int, ...]
    fiber_directions: tuple[int, ...]
    quadratic_rank: int


def build_plan(anf: QuadANF) -> tuple[PolarKernelPlan | None, str]:
    d = anf.d
    quadratic_rank = rank(list(anf.quadratic_columns), d)
    covectors = nullspace(list(anf.quadratic_columns), d)
    m = len(covectors)
    if m == 0 or m == d:
        return None, "improper-affine-quotient"
    quotient_rows = []
    constants = []
    for lam in covectors:
        row = sum(parity(lam & anf.linear_columns[i]) << i for i in range(d))
        quotient_rows.append(row)
        constants.append(parity(lam & anf.constant))
    if rank(quotient_rows, d) != m:
        return None, "rank-deficient-affine-quotient"
    directions = nullspace(quotient_rows, d)
    if len(directions) != d - m:
        return None, "fiber-dimension"
    for i in range(len(directions)):
        for j in range(i + 1, len(directions)):
            if polar_vector(anf, directions[i], directions[j]) != 0:
                return None, "nonaffine-fiber-restriction"
    return PolarKernelPlan(tuple(covectors), tuple(quotient_rows), tuple(constants),
                           tuple(directions), quadratic_rank), "ok"


def invert_with_plan(anf: QuadANF, plan: PolarKernelPlan, target: int) -> tuple[int | None, str]:
    rhs = [parity(lam & target) ^ c
           for lam, c in zip(plan.affine_covectors, plan.quotient_constants)]
    quotient_solution = solve_linear(list(plan.quotient_rows), rhs, anf.d)
    if quotient_solution is None:
        return None, "inconsistent-affine-quotient"
    y0, directions = quotient_solution
    if tuple(directions) != plan.fiber_directions:
        return None, "fiber-basis-drift"
    f0 = anf.evaluate(y0)
    delta = [anf.evaluate(y0 ^ direction) ^ f0 for direction in directions]
    n = len(directions)
    if rank(delta, anf.d) != n:
        return None, "rank-deficient-affine-fiber"
    rows = [sum(((col >> out) & 1) << j for j, col in enumerate(delta))
            for out in range(anf.d)]
    zsol = solve_linear(rows, [((target ^ f0) >> out) & 1 for out in range(anf.d)], n)
    if zsol is None:
        return None, "target-outside-affine-fiber"
    z, _ = zsol
    y = y0
    for j, direction in enumerate(directions):
        if (z >> j) & 1:
            y ^= direction
    if anf.evaluate(y) != target:
        return None, "verification-failed"
    return y, "ok"


def make_hidden(d: int, m: int, rng: random.Random, dependent: bool = False):
    n = d - m
    width = m * (m - 1) // 2
    q_masks = independent_masks(n, width, rng)
    if dependent and n >= 2:
        q_masks[-1] = q_masks[0]
    linear = [rng.randrange(1 << m) for _ in range(n)]
    constant = rng.randrange(1 << n)
    arows = random_invertible(d, rng)
    brows = nonlinear_output_matrix(d, m, q_masks, rng) if not dependent else random_invertible(d, rng)
    iphase = rng.randrange(1 << d)
    ophase = rng.randrange(1 << d)

    def hidden(y: int) -> int:
        z = mat_vec(arows, y) ^ iphase
        return mat_vec(brows, shear(z, m, n, q_masks, linear, constant)) ^ ophase

    return hidden


def main() -> None:
    started = time.perf_counter()
    rng = random.Random(SEED)
    checks = 0
    failures: list[str] = []
    records = []

    def check(cond: bool, label: str) -> None:
        nonlocal checks
        checks += 1
        if not cond:
            failures.append(label)

    for d, m, target_count in ((7, 4, 1 << 7), (16, 8, 48), (36, 18, 32), (64, 32, 16)):
        hidden = make_hidden(d, m, rng)
        anf, queries = recover_anf(d, hidden)
        plan, why = build_plan(anf)
        check(plan is not None and why == "ok", f"plan-d{d}-{why}")
        if plan is None:
            continue
        check(plan.quadratic_rank == d - m, f"quadratic-rank-d{d}")
        check(len(plan.affine_covectors) == m, f"polar-kernel-dimension-d{d}")
        check(rank(list(plan.quotient_rows), d) == m, f"quotient-linear-rank-d{d}")
        check(all(any((col >> out) & 1 for col in anf.quadratic_columns)
                  for out in range(d)), f"all-displayed-coordinates-nonlinear-d{d}")
        targets = list(range(1 << d)) if d == 7 else [rng.randrange(1 << d) for _ in range(target_count)]
        for tnum, target in enumerate(targets):
            y, reason = invert_with_plan(anf, plan, target)
            check(y is not None and reason == "ok", f"invert-d{d}-t{tnum}-{reason}")
            if y is not None:
                check(hidden(y) == target, f"hidden-verify-d{d}-t{tnum}")
        records.append({
            "dimension": d,
            "hidden_split_m": m,
            "quadratic_rank_from_raw_anf": plan.quadratic_rank,
            "polar_kernel_dimension": len(plan.affine_covectors),
            "affine_quotient_row_rank": rank(list(plan.quotient_rows), d),
            "fiber_dimension": len(plan.fiber_directions),
            "raw_anf_acquisition_evaluations": queries,
            "targets_inverted": len(targets),
            "all_displayed_coordinates_nonlinear": True,
        })

    # A dependent payload is deliberately outside the theorem's independence
    # hypothesis.  The intrinsic recognizer may still accept it if the larger
    # affine quotient and smaller residual fiber satisfy the checked ranks.
    hidden = make_hidden(9, 5, rng, dependent=True)
    dependent_anf, _ = recover_anf(9, hidden)
    dependent_plan, dependent_reason = build_plan(dependent_anf)
    dependent_success = False
    if dependent_plan is not None:
        y, reason = invert_with_plan(dependent_anf, dependent_plan, rng.randrange(1 << 9))
        dependent_success = y is not None and reason == "ok"
    check(dependent_success, "dependent-payload-broader-recognition")

    # Off-image controls: the recognizer rejects instead of silently assuming
    # a shear decomposition.  A caller may hand such inputs to another solver.
    identity = QuadANF(5, 0, tuple(1 << i for i in range(5)), tuple(0 for _ in pairs(5)))
    zero = QuadANF(5, 0, tuple(0 for _ in range(5)), tuple(0 for _ in pairs(5)))
    random_anf = QuadANF(7, rng.randrange(1 << 7),
                         tuple(rng.randrange(1 << 7) for _ in range(7)),
                         tuple(rng.randrange(1 << 7) for _ in pairs(7)))
    controls = []
    for label, anf in (("affine-identity", identity), ("zero-map", zero),
                       ("random-quadratic", random_anf)):
        plan, reason = build_plan(anf)
        check(plan is None, "off-image-reject-" + label)
        controls.append({"case": label, "accepted": plan is not None, "reason": reason})

    elapsed = time.perf_counter() - started
    result = {
        "run_id": RUN_ID,
        "status": "PASS" if not failures else "FAIL",
        "seed": SEED,
        "checks": checks,
        "failures": failures,
        "elapsed_seconds": elapsed,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "records": records,
        "dependent_payload_control": {
            "recognized": dependent_plan is not None,
            "reason": dependent_reason,
            "inverted": dependent_success,
            "polar_kernel_dimension": len(dependent_plan.affine_covectors) if dependent_plan else None,
        },
        "off_image_controls": controls,
        "scope": "exact raw-ANF polar-kernel algorithm plus bounded audit; no arbitrary-MQ or runtime lower bound",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
