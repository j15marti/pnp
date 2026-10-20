#!/usr/bin/env python3
"""Finite controls for LOW-SIDE-ORBIT-COLLAPSE29.

The theorem is a counting statement about deterministic maps.  This audit
exhausts all small maps, checks larger reproducible maps, and constructs
same-label proper-3CNF padding orbits for both SAT and UNSAT.  It does not
estimate unrestricted SAT time or prove a SAT-to-MKTP reduction.
"""

from itertools import combinations, product
import json


checks = 0
failures: list[str] = []


def check(condition: bool, label: str) -> None:
    global checks
    checks += 1
    if not condition:
        failures.append(label)


def decode_map(code: int, source_size: int, target_size: int) -> list[int]:
    values = []
    for _ in range(source_size):
        values.append(code % target_size)
        code //= target_size
    return values


# Exhaust all maps {0,1}^r -> [T] for r<=3 and T<=4.  For every low-target
# subset L, |R^{-1}(L)| <= |L| times the largest fiber.  If the whole orbit is
# low, some fiber has size at least ceil(2^r/|L|).
exhaustive_maps = 0
for r in range(0, 4):
    source_size = 1 << r
    for target_size in range(1, 5):
        for code in range(target_size ** source_size):
            mapping = decode_map(code, source_size, target_size)
            counts = [mapping.count(y) for y in range(target_size)]
            max_fiber = max(counts)
            image_size = sum(c > 0 for c in counts)
            exhaustive_maps += 1
            check(image_size * max_fiber >= source_size,
                  f"image-fiber:r={r}:T={target_size}:code={code}")
            for low_size in range(target_size + 1):
                for low_set in combinations(range(target_size), low_size):
                    low_preimage = sum(counts[y] for y in low_set)
                    check(low_preimage <= low_size * max_fiber,
                          f"preimage:r={r}:T={target_size}:code={code}:L={low_set}")
                    if low_preimage == source_size and low_size:
                        required = (source_size + low_size - 1) // low_size
                        check(max_fiber >= required,
                              f"collapse:r={r}:T={target_size}:code={code}:L={low_set}")


# Larger deterministic controls.  The chosen maps include affine, folded and
# mildly nonlinear examples; the theorem depends only on fiber cardinality.
structured_maps = 0
for r in range(4, 15):
    source_size = 1 << r
    for target_size in range(3, 34):
        for seed in range(64):
            mapping = [
                ((seed + 3) * z + (z >> (seed % r)) + (z * z if seed & 1 else 0))
                % target_size
                for z in range(source_size)
            ]
            counts = [mapping.count(y) for y in range(target_size)]
            max_fiber = max(counts)
            image_size = sum(c > 0 for c in counts)
            structured_maps += 1
            check(image_size * max_fiber >= source_size,
                  f"structured-image:r={r}:T={target_size}:seed={seed}")
            for low_size in (1, min(2, target_size), target_size // 2, target_size):
                low_size = max(1, low_size)
                low_preimage = sum(counts[:low_size])
                check(low_preimage <= low_size * max_fiber,
                      f"structured-preimage:r={r}:T={target_size}:seed={seed}:B={low_size}")


def all_sign_clauses() -> list[tuple[int, int, int]]:
    return [tuple(sign * var for sign, var in zip(signs, (1, 2, 3)))
            for signs in product((-1, 1), repeat=3)]


def clause_value(clause: tuple[int, int, int], assignment: dict[int, bool]) -> bool:
    return any(assignment[abs(lit)] == (lit > 0) for lit in clause)


def proper(clause: tuple[int, int, int]) -> bool:
    return len({abs(lit) for lit in clause}) == 3


def payload_clauses(r: int, z: int) -> list[tuple[int, int, int]]:
    result = []
    for i in range(r):
        a = 4 + 3 * i
        b = a + 1
        c = a + 2
        result.append((a, b, -c if ((z >> i) & 1) else c))
    return result


def encode(formula: list[tuple[int, int, int]]) -> str:
    return "|".join(",".join(str(lit) for lit in clause) for clause in formula)


def recover_payload(formula: list[tuple[int, int, int]], r: int) -> int:
    z = 0
    for i, clause in enumerate(formula[-r:] if r else []):
        if clause[2] < 0:
            z |= 1 << i
    return z


# All eight sign patterns on three variables form an UNSAT proper-3CNF core.
# Removing one clause and duplicating another gives an eight-clause SAT core.
unsat_core = all_sign_clauses()
sat_core = unsat_core[1:] + [unsat_core[1]]

core_witness = None
for bits in range(8):
    assignment = {i + 1: bool((bits >> i) & 1) for i in range(3)}
    if all(clause_value(c, assignment) for c in sat_core):
        core_witness = assignment
        break
check(core_witness is not None, "sat-core-witness")
for bits in range(8):
    assignment = {i + 1: bool((bits >> i) & 1) for i in range(3)}
    check(not all(clause_value(c, assignment) for c in unsat_core),
          f"unsat-core:{bits}")

orbit_summaries = []
for r in range(0, 13):
    sat_encodings = set()
    unsat_encodings = set()
    lengths = []
    for z in range(1 << r):
        payload = payload_clauses(r, z)
        sat_formula = sat_core + payload
        unsat_formula = unsat_core + payload
        check(all(proper(c) for c in sat_formula), f"proper-sat:r={r}:z={z}")
        check(all(proper(c) for c in unsat_formula), f"proper-unsat:r={r}:z={z}")

        witness = dict(core_witness or {})
        for i in range(r):
            a = 4 + 3 * i
            witness[a] = True
            witness[a + 1] = False
            witness[a + 2] = False
        check(all(clause_value(c, witness) for c in sat_formula),
              f"sat-witness:r={r}:z={z}")
        # The complete eight-clause core is already UNSAT, independently of z.
        check(unsat_formula[:8] == unsat_core, f"unsat-prefix:r={r}:z={z}")
        check(recover_payload(sat_formula, r) == z, f"recover-sat:r={r}:z={z}")
        check(recover_payload(unsat_formula, r) == z, f"recover-unsat:r={r}:z={z}")

        sat_encoded = encode(sat_formula)
        unsat_encoded = encode(unsat_formula)
        sat_encodings.add(sat_encoded)
        unsat_encodings.add(unsat_encoded)
        lengths.extend((len(sat_encoded), len(unsat_encoded)))
    check(len(sat_encodings) == 1 << r, f"sat-orbit-size:r={r}")
    check(len(unsat_encodings) == 1 << r, f"unsat-orbit-size:r={r}")
    orbit_summaries.append({
        "payload_bits": r,
        "orbit_size_each_label": 1 << r,
        "clause_count": 8 + r,
        "variable_count": 3 + 3 * r,
        "min_text_encoding_bytes": min(lengths),
        "max_text_encoding_bytes": max(lengths),
    })


# Conservative ordinary indexed-KT description count.  For cost at most p,
# at most (p+1)*2^(p+1) program/time-code pairs are available.  The theorem is
# stated using the exact low-target cardinality B_p; this is only a safe bound.
kt_arithmetic_cases = 0
for p in range(1, 65):
    B = (p + 1) * (1 << (p + 1))
    for r in range(1, 4 * p + 17):
        orbit_size = 1 << r
        required_fiber = (orbit_size + B - 1) // B
        kt_arithmetic_cases += 1
        check(required_fiber * B >= orbit_size, f"kt-ceil-upper:p={p}:r={r}")
        check((required_fiber - 1) * B < orbit_size,
              f"kt-ceil-lower:p={p}:r={r}")
        if orbit_size > B:
            check(required_fiber >= 2, f"kt-injective-fails:p={p}:r={r}")


result = {
    "run": "LOW-SIDE-ORBIT-COLLAPSE29",
    "status": "PASS" if not failures else "FAIL",
    "checks": checks,
    "failures": failures[:20],
    "exhaustive_small_maps": exhaustive_maps,
    "structured_larger_maps": structured_maps,
    "kt_arithmetic_cases": kt_arithmetic_cases,
    "proper_3cnf_orbits": orbit_summaries,
    "proved_scope": (
        "A deterministic map sending an entire 2^r same-label orbit into a "
        "low-target set of size B must have a fiber of size at least ceil(2^r/B)."
    ),
    "firewall": (
        "The theorem is a necessary collision condition only.  It does not "
        "rule out padding canonicalization and gives no SAT, MKTP, ARC, or FLMV lower bound."
    ),
}
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(0 if not failures else 1)
