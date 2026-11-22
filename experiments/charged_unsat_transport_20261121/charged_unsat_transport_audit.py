#!/usr/bin/env python3
"""Finite semantic and encoding audit for charged UNSAT transport.

This program does not simulate an arbitrary Turing machine. Its operation
counters and wall time are audit costs, not the proved machine lower bounds.
The asymptotic theorem is proved separately in Charged_UNSAT_Transport.md.
Standard-library Python only. No random sampling is used.
"""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import permutations, product
from math import factorial
from pathlib import Path
import json
import platform
import time


COUNTS = Counter()


def require(condition, label):
    COUNTS["assertions"] += 1
    if not condition:
        raise AssertionError(label)


def gamma(number):
    bits = format(number, "b")
    return "0" * (len(bits) - 1) + bits


def literal_value(literal, assignment):
    bit = bool(assignment & (1 << (abs(literal) - 1)))
    return bit if literal > 0 else not bit


def masks(clauses):
    return tuple((sum(1 << (v - 1) for v in c if v > 0),
                  sum(1 << (-v - 1) for v in c if v < 0)) for c in clauses)


def satisfies(compiled_masks, assignment):
    COUNTS["assignment_evaluations"] += 1
    for positive, negative in compiled_masks:
        COUNTS["clause_evaluations"] += 1
        if not (assignment & positive or (~assignment) & negative):
            return False
    return True


def source_formula(left_map, right_map):
    r = len(left_map)
    if r < 3 or len(right_map) != r:
        raise ValueError("Two equal-length maps with length at least three required")
    if any(not 1 <= j <= r for j in (*left_map, *right_map)):
        raise ValueError("Map values must be between one and r")
    padding = 2 * r + 1
    chain = tuple(range(2 * r + 2, 3 * r - 1))
    left = tuple(c for i, j in enumerate(left_map, 1)
                 for c in ((-i, r + j, padding), (-i, r + j, -padding)))
    right = tuple(c for i, j in enumerate(right_map, 1)
                  for c in ((-i, -(r + j), padding), (-i, -(r + j), -padding)))
    if r == 3:
        middle = ((1, 2, 3),)
    else:
        middle = ((1, 2, chain[0]),)
        middle += tuple((-chain[j], j + 3, chain[j + 1])
                        for j in range(r - 4))
        middle += ((-chain[-1], r - 1, r),)
    return left + middle + right, 3 * r - 2, chain


def compile_compatibility(source, source_n):
    y, u, v = source_n + 1, source_n + 2, source_n + 3
    clauses = [(y, u, v), (y, u, -v), (y, -u, v), (y, -u, -v)]
    for j, (a, b, c) in enumerate(source):
        z = source_n + 4 + j
        clauses.extend(((-y, a, z), (-z, b, c)))
    n = source_n + len(source) + 3
    alpha = 1 << (u - 1)
    beta = alpha | (1 << (v - 1))
    return tuple(clauses), n, y, u, v, alpha, beta


def encode(clauses, n, y, alpha, beta, r):
    width = n.bit_length()
    header = "1" * n + "0" + gamma(len(clauses) + 1)
    data = "".join(("1" if lit < 0 else "0") + format(abs(lit), f"0{width}b")
                   for clause in clauses for lit in clause)
    witnesses = "".join("1" if a & (1 << j) else "0"
                        for a in (alpha, beta) for j in range(n))
    bits = header + data + witnesses + format(y, f"0{width}b")
    clause_width = 3 * (width + 1)
    middle_start = len(header) + (4 + 4 * r) * clause_width
    middle_end = middle_start + (2 * r - 4) * clause_width
    return bits, bits[:middle_start], bits[middle_start:middle_end], bits[middle_end:]


def local_gadget_audit():
    selector = masks(((1, 2, 3), (1, 2, -3), (1, -2, 3), (1, -2, -3)))
    for assignment in range(8):
        require(satisfies(selector, assignment) == bool(assignment & 1),
                "Selector equals its first variable")
    pair = masks(((-1, 2, 5), (-5, 3, 4)))
    for y, a, b, c in product((0, 1), repeat=4):
        assignment = y | (a << 1) | (b << 2) | (c << 3)
        projected = any(satisfies(pair, assignment | (z << 4)) for z in (0, 1))
        require(projected == bool(not y or a or b or c), "Guarded projection")


def construct_witness(left_map, right_map, chain, source, source_n):
    r = len(left_map)
    mismatch = next(i for i in range(r) if left_map[i] != right_map[i])
    assignment = (1 << mismatch) | (1 << (r + left_map[mismatch] - 1))
    for j, variable in enumerate(chain):
        if not assignment & ((1 << (j + 2)) - 1):
            assignment |= 1 << (variable - 1)
    require(satisfies(masks(source), assignment), "Constructive source witness")
    target = assignment | (1 << source_n) | (1 << (source_n + 1))
    for j, (a, _, _) in enumerate(source):
        if not literal_value(a, assignment):
            target |= 1 << (source_n + 3 + j)
    return target


def audit_pair(left_map, right_map, references, exhaustive):
    r = len(left_map)
    source, source_n, chain = source_formula(left_map, right_map)
    built = compile_compatibility(source, source_n)
    clauses, n, y, u, v, alpha, beta = built
    require(source_n == 3 * r - 2 and len(source) == 5 * r - 2, "Source size")
    require(n == 8 * r - 1 and len(clauses) == 10 * r, "Compiled size")
    require(all(len(set(map(abs, c))) == 3 for c in source + clauses), "Proper width three")
    require(len(set(clauses)) == len(clauses), "Compiled clauses distinct")
    horn = tuple(c for c in clauses if sum(lit > 0 for lit in c) <= 1)
    dual = tuple(c for c in clauses if sum(lit > 0 for lit in c) >= 2)
    require(satisfies(masks(horn), alpha), "Horn witness")
    require(satisfies(masks(dual), beta), "Dual-Horn witness")
    require((alpha ^ beta).bit_count() == 1, "Adjacent supplied witnesses")
    failed = [[j for j, c in enumerate(clauses)
               if not any(literal_value(lit, a) for lit in c)] for a in (alpha, beta)]
    require(failed == [[2], [3]], "Exactly one failed clause per witness")
    bits, left, middle, right = encode(clauses, n, y, alpha, beta, r)
    width = n.bit_length()
    expected_n = 3 * n + 2 + 2 * ((len(clauses) + 1).bit_length() - 1)
    expected_n += 3 * len(clauses) * (width + 1) + width
    require(len(bits) == expected_n, "Exact encoded input length including metadata")
    require(len(middle) - 1 == 6 * (r - 2) * (width + 1) - 1, "Exact gap")
    if references is not None:
        require(left == references[left_map][0], "Left depends only on left map")
        require(middle == references[left_map][1] == references[right_map][1], "Common middle")
        require(right == references[right_map][2], "Right depends only on right map")
    expected_sat = left_map != right_map
    projected_count = None
    if exhaustive:
        projected = set()
        source_masks = masks(source)
        for assignment in range(1 << source_n):
            COUNTS["source_assignments_enumerated"] += 1
            if satisfies(source_masks, assignment):
                projected.add(assignment & ((1 << (2 * r)) - 1))
        direct = set()
        for assignment in range(1 << (2 * r)):
            if not assignment & ((1 << r) - 1):
                continue
            if all(not (assignment & (1 << i)) or
                   ((assignment & (1 << (r + left_map[i] - 1))) and
                    not (assignment & (1 << (r + right_map[i] - 1))))
                   for i in range(r)):
                direct.add(assignment)
        require(projected == direct, "Exact projection to X and Y")
        require(bool(projected) == expected_sat, "UNSAT exactly on diagonal")
        projected_count = len(projected)
    witness = None
    if expected_sat:
        witness = construct_witness(left_map, right_map, chain, source, source_n)
        require(satisfies(masks(clauses), witness), "Constructive compiled witness")
    COUNTS["pair_instances"] += 1
    COUNTS["sat_instances" if expected_sat else "unsat_instances"] += 1
    return {"r": r, "left_map": left_map, "right_map": right_map,
            "source_variables": source_n, "source_clauses": len(source),
            "target_variables": n, "target_clauses": len(clauses),
            "horn_clauses": len(horn), "dual_horn_clauses": len(dual),
            "input_bits": len(bits), "middle_bits": len(middle),
            "selected_boundaries": len(middle) - 1,
            "input_sha256": sha256(bits.encode("ascii")).hexdigest(),
            "sat": expected_sat, "projected_model_count_XY": projected_count,
            "compiled_witness_integer": witness, "exhaustive_source_projection": exhaustive}


def joint_bound(r, q, z):
    if q < 2 or q & (q - 1):
        raise ValueError("This integer audit uses a power-of-two state count")
    n, m = 8 * r - 1, 10 * r
    width, ell = n.bit_length(), q.bit_length() - 1
    input_bits = 3 * n + 2 + 2 * ((m + 1).bit_length() - 1)
    input_bits += 3 * m * (width + 1) + width
    boundaries = 6 * (r - 2) * (width + 1) - 1
    p = factorial(r)
    h0 = p.bit_length() - 1
    h = h0 - z
    crossings = max(0, h // ell)
    sizes = [h - j * ell for j in range(1, crossings + 1)]
    for j, s in enumerate(sizes, 1):
        exceptions = (pow(q, j) - 1) // (q - 1) + pow(q, j) * (pow(2, s) - 1)
        require(exceptions * pow(2, z) <= p, "Finite per-event bad-fraction bound")
    failure = Fraction(boundaries * crossings, pow(2, z))
    return {"r": r, "states_Q": q, "z": z, "input_bits": input_bits,
            "selected_boundaries_D": boundaries, "floor_log2_factorial": h0,
            "crossings_per_boundary": crossings,
            "time_lower_bound_transitions": boundaries * crossings,
            "configuration_code_CM_lower_bound": boundaries * sum(sizes),
            "failure_probability_upper_fraction": str(min(Fraction(1), failure)),
            "success_probability_lower": float(max(Fraction(0), 1 - failure)),
            "interpretation": "Symbolic theorem instantiation, not a measured solver runtime"}


def main():
    started = time.perf_counter()
    local_gadget_audit()
    records = []
    for r in (3, 4):
        choices = list(permutations(range(1, r + 1)))
        references = {}
        for p in choices:
            source, source_n, _ = source_formula(p, p)
            clauses, n, y, _, _, alpha, beta = compile_compatibility(source, source_n)
            _, left, middle, right = encode(clauses, n, y, alpha, beta, r)
            references[p] = (left, middle, right)
        for left_map, right_map in product(choices, repeat=2):
            records.append(audit_pair(left_map, right_map, references, True))
    # Nonpermutation controls justify a recognizer that need not check injectivity.
    for r in (3, 4, 5, 8):
        constant = (1,) * r
        changed = (2,) + (1,) * (r - 1)
        records.append(audit_pair(constant, constant, None, r <= 4))
        records.append(audit_pair(constant, changed, None, r <= 4))
    bounds = [joint_bound(r, 256, z) for r, z in ((64, 30), (1000, 40))]
    result = {"dependency": "CHARGED-UNSAT-TRANSPORT1",
              "scope": "Finite semantic/layout verification; no arbitrary-machine simulation",
              "encoding": "1^n 0 || gamma(m+1) || ordered sign+ID triples || alpha || beta || yID",
              "seed": None, "mode": "exhaustive for permutation pairs r=3,4; constructive controls otherwise",
              "python_version": platform.python_version(),
              "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
              "counters": dict(COUNTS), "joint_bounds": bounds, "records": records,
              "elapsed_seconds": time.perf_counter() - started}
    destination = Path(__file__).with_name("charged_unsat_transport_results.json")
    destination.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("dependency", "counters", "joint_bounds", "elapsed_seconds")}, indent=2))


if __name__ == "__main__":
    main()
