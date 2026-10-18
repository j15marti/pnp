#!/usr/bin/env python3
"""Exact audit of a pin-free proper signed-NAE compiler.

The compiler replaces each proper 3-CNF clause (a or b or c) by

  NAE(a,b,u_i) and NAE(not u_i,c,z_i),

then links local gauge variables z_i by

  EQ(z_i,z_{i+1};e_i) :=
    NAE(z_i,not z_{i+1},e_i) and
    NAE(z_i,not z_{i+1},not e_i).

This file performs exhaustive local truth-table checks, seeded formula-level
SAT/projection checks, exact count/occurrence audits, binary codec round trips,
invalid-input rejection tests, and 6/8-boundary separator checks.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import random
import struct
import time
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

SEED = 202610190500
MAGIC = b"NGC1"


@dataclass(frozen=True, order=True)
class Lit:
    var: int
    neg: bool = False

    def value(self, assignment: tuple[int, ...]) -> int:
        return assignment[self.var] ^ int(self.neg)

    def flip(self) -> "Lit":
        return Lit(self.var, not self.neg)


Clause = tuple[Lit, Lit, Lit]


def nae_values(a: int, b: int, c: int) -> bool:
    return not (a == b == c)


def sat_clause(clause: Clause, assignment: tuple[int, ...]) -> bool:
    return nae_values(*(lit.value(assignment) for lit in clause))


def sat_formula(clauses: list[Clause], assignment: tuple[int, ...]) -> bool:
    return all(sat_clause(c, assignment) for c in clauses)


def proper(clause: Clause) -> bool:
    return len({lit.var for lit in clause}) == 3


def canonical_clause(clause: Clause) -> tuple[tuple[int, bool], ...]:
    # NAE is invariant under simultaneous literal complementation.
    a = tuple(sorted((x.var, x.neg) for x in clause))
    b = tuple(sorted((x.var, not x.neg) for x in clause))
    return min(a, b)


def eq_gadget(x: int, y: int, e: int) -> list[Clause]:
    return [
        (Lit(x), Lit(y, True), Lit(e)),
        (Lit(x), Lit(y, True), Lit(e, True)),
    ]


def validate_source(n: int, source: list[Clause]) -> None:
    if n < 1 or not source:
        raise ValueError("source must be nonempty and have at least one variable")
    for clause in source:
        if not proper(clause):
            raise ValueError("source clause is not proper")
        for lit in clause:
            if not (0 <= lit.var < n):
                raise ValueError("source literal outside declared variable range")


@dataclass
class Compiled:
    n_source: int
    n_target: int
    clauses: list[Clause]
    u: list[int]
    z: list[int]
    e: list[int]
    clause_owner: list[tuple[str, int]]


def compile_formula(n: int, source: list[Clause]) -> Compiled:
    validate_source(n, source)
    m = len(source)
    u = list(range(n, n + m))
    z = list(range(n + m, n + 2 * m))
    e = list(range(n + 2 * m, n + 3 * m - 1))
    out: list[Clause] = []
    owners: list[tuple[str, int]] = []
    for i, (a, b, c) in enumerate(source):
        out.append((a, b, Lit(u[i])))
        owners.append(("front", i))
        out.append((Lit(u[i], True), c, Lit(z[i])))
        owners.append(("front", i))
    for i in range(m - 1):
        out.extend(eq_gadget(z[i], z[i + 1], e[i]))
        owners.extend([("link", i), ("link", i)])
    return Compiled(n, n + 3 * m - 1, out, u, z, e, owners)


def source_sat(source: list[Clause], assignment: tuple[int, ...]) -> bool:
    return all(any(lit.value(assignment) for lit in c) for c in source)


def any_model(n: int, predicate) -> tuple[int, ...] | None:
    for a in itertools.product((0, 1), repeat=n):
        if predicate(a):
            return a
    return None


def project_target(comp: Compiled, target: tuple[int, ...]) -> tuple[int, ...]:
    if not sat_formula(comp.clauses, target):
        raise ValueError("not a target model")
    gauge = target[comp.z[0]]
    if any(target[v] != gauge for v in comp.z):
        raise AssertionError("equality chain failed")
    src = target[: comp.n_source]
    return src if gauge == 0 else tuple(1 - b for b in src)


def extend_source(comp: Compiled, source: list[Clause], src: tuple[int, ...], gauge: int = 0) -> tuple[int, ...]:
    if not source_sat(source, src):
        raise ValueError("not a source model")
    # For gauge 1, the target source coordinates are the complement of src.
    base = src if gauge == 0 else tuple(1 - b for b in src)
    a = list(base) + [0] * (comp.n_target - comp.n_source)
    for v in comp.z:
        a[v] = gauge
    for i, (la, lb, lc) in enumerate(source):
        found = False
        for ui in (0, 1):
            a[comp.u[i]] = ui
            if sat_clause(comp.clauses[2 * i], tuple(a)) and sat_clause(comp.clauses[2 * i + 1], tuple(a)):
                found = True
                break
        if not found:
            raise AssertionError("front-end witness missing")
    # Equal z_i satisfy every equality gadget; equality auxiliaries may be zero.
    out = tuple(a)
    if not sat_formula(comp.clauses, out):
        raise AssertionError("constructed target witness is invalid")
    return out


def occurrence_counts(comp: Compiled) -> Counter[int]:
    return Counter(lit.var for clause in comp.clauses for lit in clause)


def pack_formula(comp: Compiled) -> tuple[bytes, int]:
    n, m = comp.n_target, len(comp.clauses)
    width = max(1, math.ceil(math.log2(n + 1)))
    bits: list[int] = []
    for clause in comp.clauses:
        for lit in clause:
            bits.append(int(lit.neg))
            value = lit.var + 1
            bits.extend((value >> j) & 1 for j in reversed(range(width)))
    payload_bits = 96 + len(bits)
    while len(bits) % 8:
        bits.append(0)
    body = bytes(sum(bits[i + j] << (7 - j) for j in range(8)) for i in range(0, len(bits), 8))
    return MAGIC + struct.pack(">II", n, m) + body, payload_bits


def unpack_formula(data: bytes) -> tuple[int, list[Clause], int]:
    if len(data) < 12 or data[:4] != MAGIC:
        raise ValueError("bad magic or truncated header")
    n, m = struct.unpack(">II", data[4:12])
    if n < 1 or m < 1:
        raise ValueError("invalid dimensions")
    width = max(1, math.ceil(math.log2(n + 1)))
    needed = 3 * m * (width + 1)
    body = data[12:]
    if len(body) * 8 < needed:
        raise ValueError("truncated payload")
    bits = [(byte >> (7 - j)) & 1 for byte in body for j in range(8)]
    clauses: list[Clause] = []
    pos = 0
    for _ in range(m):
        lits = []
        for _ in range(3):
            neg = bool(bits[pos]); pos += 1
            value = 0
            for _ in range(width):
                value = 2 * value + bits[pos]; pos += 1
            if not (1 <= value <= n):
                raise ValueError("variable id outside range")
            lits.append(Lit(value - 1, neg))
        clause = tuple(lits)
        if not proper(clause):
            raise ValueError("improper target clause")
        clauses.append(clause)  # type: ignore[arg-type]
    # Padding must be all zero and no trailing bytes are accepted.
    pad = (-needed) % 8
    if any(bits[pos:pos + pad]) or len(body) * 8 != needed + pad:
        raise ValueError("noncanonical padding or trailing data")
    return n, clauses, 96 + needed


def recognize_image(n_target: int, clauses: list[Clause]) -> tuple[int, list[Clause]]:
    """Recognize the compiler's ordered image and recover its source formula."""
    M = len(clauses)
    if M < 2 or (M + 2) % 4:
        raise ValueError("wrong image clause count")
    m = (M + 2) // 4
    n = n_target - 3 * m + 1
    if n < 1:
        raise ValueError("wrong image variable count")
    u = list(range(n, n + m))
    z = list(range(n + m, n + 2 * m))
    e = list(range(n + 2 * m, n + 3 * m - 1))
    source: list[Clause] = []
    for i in range(m):
        c0, c1 = clauses[2 * i], clauses[2 * i + 1]
        if c0[2] != Lit(u[i]) or c1[0] != Lit(u[i], True) or c1[2] != Lit(z[i]):
            raise ValueError("front-end syntax mismatch")
        src = (c0[0], c0[1], c1[1])
        if not proper(src) or any(l.var >= n for l in src):
            raise ValueError("recovered source is not proper")
        source.append(src)
    pos = 2 * m
    for i in range(m - 1):
        want = eq_gadget(z[i], z[i + 1], e[i])
        if clauses[pos:pos + 2] != want:
            raise ValueError("equality-chain syntax mismatch")
        pos += 2
    return n, source


def source_vars_by_side(source: list[Clause], side: list[int]) -> tuple[set[int], set[int]]:
    left: set[int] = set()
    right: set[int] = set()
    for i, clause in enumerate(source):
        (left if side[i] == 0 else right).update(l.var for l in clause)
    return left, right


def min_compiled_separator(comp: Compiled, side: list[int]) -> int:
    """Minimize shared variables over assignments of equality gadgets to sides."""
    m = len(side)
    crossing_links = [i for i in range(m - 1) if side[i] != side[i + 1]]
    best = 10**9
    for choices in itertools.product((0, 1), repeat=len(crossing_links)):
        link_side = {i: side[i] for i in range(m - 1) if side[i] == side[i + 1]}
        link_side.update(dict(zip(crossing_links, choices)))
        left: set[int] = set()
        right: set[int] = set()
        for clause, (kind, idx) in zip(comp.clauses, comp.clause_owner):
            s = side[idx] if kind == "front" else link_side[idx]
            (left if s == 0 else right).update(l.var for l in clause)
        best = min(best, len(left & right))
    return best


def boundary_instance(width: int, alternating: bool) -> tuple[int, list[Clause], list[int]]:
    source: list[Clause] = []
    side: list[int] = []
    next_var = width
    entries = []
    for s in (0, 1):
        for b in range(width):
            entries.append((s, b))
    if alternating:
        entries.sort(key=lambda x: x[1] * 2 + x[0])
    for s, b in entries:
        source.append((Lit(b), Lit(next_var), Lit(next_var + 1, bool((b + s) & 1))))
        side.append(s)
        next_var += 2
    return next_var, source, side


def random_source(rng: random.Random, n: int, m: int) -> list[Clause]:
    out = []
    for _ in range(m):
        vs = rng.sample(range(n), 3)
        rng.shuffle(vs)
        out.append(tuple(Lit(v, bool(rng.getrandbits(1))) for v in vs))
    return out  # repetitions are intentionally permitted


def front_formula_model(source: list[Clause], x: tuple[int, ...], gauge: int) -> bool:
    """Existentially eliminate independent u_i from the front end."""
    for a, b, c in source:
        if not any(
            nae_values(a.value(x), b.value(x), u)
            and nae_values(1 - u, c.value(x), gauge)
            for u in (0, 1)
        ):
            return False
    return True


def main() -> None:
    started = time.perf_counter()
    rng = random.Random(SEED)
    checks = Counter()
    failures: list[str] = []

    # Exact equality relation and its witness multiplicity.
    eq_projection = {}
    for x, y in itertools.product((0, 1), repeat=2):
        witnesses = []
        for e in (0, 1):
            a = (x, y, e)
            if sat_formula(eq_gadget(0, 1, 2), a):
                witnesses.append(e)
            checks["eq_truth_rows"] += 1
        eq_projection[f"{x}{y}"] = witnesses
        if bool(witnesses) != (x == y):
            failures.append(f"EQ mismatch {x}{y}: {witnesses}")

    # Exact one-clause gauge relation and projection map.
    front_projection = {}
    for abc in itertools.product((0, 1), repeat=3):
        for z in (0, 1):
            ws = []
            for u in (0, 1):
                a, b, c = abc
                if nae_values(a, b, u) and nae_values(1 - u, c, z):
                    ws.append(u)
                checks["front_truth_rows"] += 1
            front_projection["".join(map(str, abc)) + f"|z={z}"] = ws
            expected = any(abc) if z == 0 else any(1 - x for x in abc)
            if bool(ws) != expected:
                failures.append(f"front mismatch {abc},z={z}: {ws}")

    # Formula-level exhaustive decision and witness transport checks.
    formula_cases = 0
    projection_models = 0
    extension_models = 0
    codec_cases = 0
    invalid_rejections = 0
    max_aux_occurrence = 0
    count_rows = []
    for n in range(3, 7):
        for m in range(1, 8):
            for _ in range(12):
                source = random_source(rng, n, m)
                # Exercise duplicate source clauses in every batch.
                if m >= 2 and formula_cases % 7 == 0:
                    source[-1] = source[0]
                comp = compile_formula(n, source)
                formula_cases += 1
                if comp.n_target != n + 3 * m - 1 or len(comp.clauses) != 4 * m - 2:
                    failures.append("count identity failed")
                if not all(proper(c) for c in comp.clauses):
                    failures.append("improper target clause")
                if len({canonical_clause(c) for c in comp.clauses}) != len(comp.clauses):
                    failures.append("duplicate target NAE clause")
                occ = occurrence_counts(comp)
                aux_max = max(occ[v] for v in comp.u + comp.z + comp.e)
                max_aux_occurrence = max(max_aux_occurrence, aux_max)
                expected_max = 2 if m == 1 else (3 if m == 2 else 5)
                if aux_max != expected_max:
                    failures.append(f"aux occurrence mismatch m={m}: {aux_max}")
                if any(occ[v] != sum(l.var == v for c in source for l in c) for v in range(n)):
                    failures.append("source occurrence not preserved")

                sm = any_model(n, lambda a: source_sat(source, a))
                # Eliminate equality auxiliaries symbolically (all z_i equal) and
                # enumerate only the n source coordinates plus one gauge bit.
                tm_core = None
                for x in itertools.product((0, 1), repeat=n):
                    for gauge in (0, 1):
                        if front_formula_model(source, x, gauge):
                            tm_core = (x, gauge)
                            break
                    if tm_core is not None:
                        break
                checks["formula_decision"] += 1
                if (sm is None) != (tm_core is None):
                    failures.append(f"SAT mismatch n={n},m={m}")
                if sm is not None:
                    for gauge in (0, 1):
                        ext = extend_source(comp, source, sm, gauge)
                        extension_models += 1
                        if not sat_formula(comp.clauses, ext):
                            failures.append("extension failed")
                        projected = project_target(comp, ext)
                        projection_models += 1
                        if projected != sm or not source_sat(source, projected):
                            failures.append("projection failed")
                if tm_core is not None:
                    x, gauge = tm_core
                    projected = x if gauge == 0 else tuple(1 - b for b in x)
                    if not source_sat(source, projected):
                        failures.append("symbolic target projection failed")

                # Full target-space exhaustive control only where it stays tiny.
                if n == 3 and m <= 2:
                    brute_tm = any_model(comp.n_target, lambda a: sat_formula(comp.clauses, a))
                    checks["full_target_exhaustive"] += 1
                    if (brute_tm is None) != (tm_core is None):
                        failures.append("full target exhaustive mismatch")

                packed, exact_bits = pack_formula(comp)
                dn, dc, decoded_bits = unpack_formula(packed)
                codec_cases += 1
                if dn != comp.n_target or dc != comp.clauses or exact_bits != decoded_bits:
                    failures.append("codec roundtrip failed")
                rn, recovered = recognize_image(dn, dc)
                if rn != n or recovered != source:
                    failures.append("compiler-image recognition failed")
                try:
                    unpack_formula(packed[:-1])
                except ValueError:
                    invalid_rejections += 1
                else:
                    failures.append("truncation was accepted")
                if formula_cases <= 20:
                    broken = bytearray(packed)
                    broken[:4] = b"BAD!"
                    try:
                        unpack_formula(bytes(broken))
                    except ValueError:
                        invalid_rejections += 1
                    else:
                        failures.append("bad magic was accepted")
                    off_image = list(dc)
                    x, y, zz = off_image[1]
                    off_image[1] = (x, y, zz.flip())
                    try:
                        recognize_image(dn, off_image)
                    except ValueError:
                        invalid_rejections += 1
                    else:
                        failures.append("off-image formula was accepted")
                if not count_rows or count_rows[-1][0] != (n, m):
                    count_rows.append(((n, m), comp.n_target, len(comp.clauses), aux_max, exact_bits, len(packed)))

    # Explicit malformed source controls.
    malformed = [
        (3, []),
        (3, [(Lit(0), Lit(0), Lit(1))]),
        (3, [(Lit(0), Lit(1), Lit(3))]),
    ]
    for n, f in malformed:
        try:
            compile_formula(n, f)
        except ValueError:
            invalid_rejections += 1
        else:
            failures.append("malformed source accepted")

    # Exact 6/8 source boundary versus gauge-chain boundary.
    separator_rows = []
    for width in (6, 8):
        for alternating in (False, True):
            n, source, side = boundary_instance(width, alternating)
            source_left, source_right = source_vars_by_side(source, side)
            source_sep = len(source_left & source_right)
            comp = compile_formula(n, source)
            target_sep = min_compiled_separator(comp, side)
            separator_rows.append({
                "width": width,
                "order": "alternating" if alternating else "grouped",
                "source_separator": source_sep,
                "minimum_compiled_separator": target_sep,
                "increase": target_sep - source_sep,
                "clauses": len(source),
            })
            checks["separator_cases"] += 1
            if source_sep != width:
                failures.append("boundary generator wrong")
            if not alternating and target_sep != width + 1:
                failures.append("grouped separator ledger wrong")

    elapsed = time.perf_counter() - started
    result = {
        "run_id": "NAEGAUGECHAIN1",
        "seed": SEED,
        "elapsed_seconds": elapsed,
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "eq_projection": eq_projection,
        "front_projection": front_projection,
        "formula_cases": formula_cases,
        "projection_models_checked": projection_models,
        "extension_models_checked": extension_models,
        "codec_roundtrips": codec_cases,
        "invalid_encodings_rejected": invalid_rejections,
        "max_auxiliary_occurrence": max_aux_occurrence,
        "count_identity": "N=n+3m-1, M=4m-2 for m>=1",
        "encoded_payload_bits": "96+(4m-2)*3*(ceil(log2(n+3m))+1)",
        "separator_rows": separator_rows,
        "checks": dict(checks),
        "sample_count_rows": [
            {"n_m": list(nm), "N": N, "M": M, "aux_max": o, "exact_bits": b, "bytes": by}
            for nm, N, M, o, b, by in count_rows
        ],
        "limitations": [
            "Finite tests do not imply an arbitrary-machine lower bound.",
            "Separator minimization assigns each two-clause equality link as one block.",
            "REVFIX2 was not tested because no source definition was accessible.",
        ],
    }
    out = Path("results/raw/review/2026-10-19_NAEGAUGECHAIN1.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    out.write_text(text, encoding="utf-8")
    print(text, end="")
    print("raw_sha256", hashlib.sha256(text.encode()).hexdigest())
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
