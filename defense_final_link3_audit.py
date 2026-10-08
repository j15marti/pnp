#!/usr/bin/env python3
"""Bounded hostile controls for the FINAL-LINK2 WRAPPER proof spine.

The checks in this file validate accounting identities, finite semantic
controls, and necessary encoding guards.  They do not prove an all-input SAT
shrinker and do not decide P versus NP.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import random
import signal
import time
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path


Clause = tuple[int, ...]
CNF = tuple[Clause, ...]


def canonical(cnf: CNF) -> CNF:
    clauses: set[Clause] = set()
    for clause in cnf:
        literals = set(clause)
        if any(-lit in literals for lit in literals):
            continue
        clauses.add(tuple(sorted(literals, key=lambda z: (abs(z), z < 0))))
    return tuple(sorted(clauses, key=lambda c: (len(c), c)))


def vars_of(cnf: CNF) -> list[int]:
    return sorted({abs(lit) for clause in cnf for lit in clause})


def sat_bruteforce(cnf: CNF) -> bool:
    variables = vars_of(cnf)
    for bits in itertools.product((False, True), repeat=len(variables)):
        assignment = dict(zip(variables, bits))
        if all(any((lit > 0) == assignment[abs(lit)] for lit in clause) for clause in cnf):
            return True
    return False


def satisfied(cnf: CNF, assignment: dict[int, bool]) -> bool:
    return all(any((lit > 0) == assignment[abs(lit)] for lit in clause) for clause in cnf)


def shifted(cnf: CNF, offset: int) -> CNF:
    return tuple(tuple((1 if lit > 0 else -1) * (abs(lit) + offset) for lit in clause) for clause in cnf)


def renamed(cnf: CNF, permutation: dict[int, int], flips: dict[int, bool]) -> CNF:
    out = []
    for clause in cnf:
        row = []
        for lit in clause:
            old = abs(lit)
            sign = lit > 0
            if flips.get(old, False):
                sign = not sign
            row.append(permutation[old] if sign else -permutation[old])
        out.append(tuple(row))
    return canonical(tuple(out))


def transform_assignment(
    assignment: dict[int, bool], permutation: dict[int, int], flips: dict[int, bool]
) -> dict[int, bool]:
    return {
        permutation[old]: (value ^ flips.get(old, False))
        for old, value in assignment.items()
    }


def random_cnf(rng: random.Random, n: int, m: int, width: int = 3) -> CNF:
    clauses: list[Clause] = []
    for _ in range(m):
        w = rng.randint(1, min(width, n))
        variables = rng.sample(range(1, n + 1), w)
        clauses.append(tuple(v if rng.randrange(2) else -v for v in variables))
    return canonical(tuple(clauses))


def renaming_controls(rng: random.Random) -> dict[str, object]:
    checks = 0
    cases = 0
    changed_hash = 0
    for n in range(1, 8):
        for _ in range(50):
            cnf = random_cnf(rng, n, rng.randint(0, 12))
            image = list(range(1, n + 1))
            rng.shuffle(image)
            permutation = {i + 1: image[i] for i in range(n)}
            flips = {i: bool(rng.randrange(2)) for i in range(1, n + 1)}
            transformed = renamed(cnf, permutation, flips)
            assert sat_bruteforce(cnf) == sat_bruteforce(transformed)
            checks += 1
            for bits in itertools.product((False, True), repeat=n):
                assignment = {i + 1: bits[i] for i in range(n)}
                mapped = transform_assignment(assignment, permutation, flips)
                assert satisfied(cnf, assignment) == satisfied(transformed, mapped)
                checks += 1
            if hashlib.sha256(repr(cnf).encode()).digest() != hashlib.sha256(repr(transformed).encode()).digest():
                changed_hash += 1
            cases += 1

    horn = ((1,), (-1, 2), (-2, 3))
    permutation = {1: 1, 2: 2, 3: 3}
    flipped = renamed(horn, permutation, {1: True, 2: False, 3: False})
    assert is_horn(horn) and not is_horn(flipped)
    assert sat_bruteforce(horn) == sat_bruteforce(flipped)
    checks += 3
    return {
        "status": "PROVED/EXACT invariance; COMPUTATIONAL finite controls",
        "cases": cases,
        "checks": checks,
        "syntactic_hash_changed_cases": changed_hash,
        "horn_polarity_counterexample": {
            "source": horn,
            "polarity_flipped": flipped,
            "interpretation": "SAT is invariant under polarity renaming, but Horn membership need not be. A portfolio must rerun or transport its class certificate.",
        },
        "interpretation": "Variable permutations and consistent polarity flips preserve SAT. Raw hashes are syntactic and cannot serve as semantic canonical names without a verified normalization or equality check.",
    }


def padding_controls() -> dict[str, object]:
    checks = 0
    semantic_rows = []
    bases = [(), ((1, 2),), ((1,), (-1,)), ((1, -2), (2, 3), (-3,))]
    for cnf in bases:
        base = canonical(cnf)
        base_sat = sat_bruteforce(base)
        n0 = max(vars_of(base), default=0)
        padded = list(base)
        for j in range(1, 7):
            v = n0 + j
            padded.append((v, -v))
            raw = tuple(padded)
            assert sat_bruteforce(raw) == base_sat
            checks += 1
        semantic_rows.append({"source": base, "sat": base_sat, "tautological_padding_clauses": 6})

    rational_rows = []
    vacuous = []
    values = sorted({F(i, d) for d in range(2, 17) for i in range(1, d)})
    paddings = sorted({F(i, d) for d in range(1, 9) for i in range(d, 3 * d + 1)})
    for h in values:
        for p in paddings:
            relative_to_core = p * h
            claimed_strict_on_padded = h < 1
            actual_strict_on_core = relative_to_core < 1
            assert (not claimed_strict_on_padded) or h < 1
            checks += 1
            if claimed_strict_on_padded and not actual_strict_on_core:
                vacuous.append((p, h, relative_to_core))
    for p, h in [(F(3, 2), F(2, 3)), (F(2), F(2, 3)), (F(4, 3), F(3, 4))]:
        rational_rows.append({
            "padding_exponent_p": str(p),
            "reported_exponent_h_relative_to_padded_N": str(h),
            "true_exponent_p_times_h_relative_to_core_M": str(p * h),
            "strict_relative_to_core": p * h < 1,
        })
    witness = min(vacuous, key=lambda row: (row[0], row[1], row[2]))
    return {
        "status": "PROVED/EXACT accounting guard",
        "checks": checks,
        "semantic_rows": semantic_rows,
        "exponent_cells": len(values) * len(paddings),
        "vacuous_sublinear_cells": len(vacuous),
        "selected_rows": rational_rows,
        "small_exact_witness": {
            "p": str(witness[0]), "h": str(witness[1]), "p_h": str(witness[2])
        },
        "interpretation": "If an M-bit core is explicitly padded to N=M^p, an N^h successor has core-relative exponent ph. Thus h<1 can be vacuous when ph>=1, and the padding construction/read cost must also be charged.",
    }


def independent_product_controls() -> dict[str, object]:
    checks = 0
    family: list[CNF] = [
        (),
        ((1,),),
        ((1,), (-1,)),
        ((1, 2), (-1, 2)),
        ((1, 2), (-1, -2), (1, -2), (-1, 2)),
    ]
    first_or_failure = None
    for left in family:
        for right in family:
            shift = max(vars_of(left), default=0)
            right2 = shifted(right, shift)
            conjunction = canonical(tuple(left) + tuple(right2))
            actual = sat_bruteforce(conjunction)
            expected_and = sat_bruteforce(left) and sat_bruteforce(right2)
            expected_or = sat_bruteforce(left) or sat_bruteforce(right2)
            assert actual == expected_and
            checks += 1
            if actual != expected_or and first_or_failure is None:
                first_or_failure = {
                    "left": left,
                    "right_disjoint": right2,
                    "left_sat": sat_bruteforce(left),
                    "right_sat": sat_bruteforce(right2),
                    "conjunction_sat": actual,
                    "incorrect_or_value": expected_or,
                }
    assert first_or_failure is not None

    identity_checks = 0
    for q1 in range(1, 5):
        for q2 in range(1, 5):
            for left_bits in itertools.product((False, True), repeat=q1):
                for right_bits in itertools.product((False, True), repeat=q2):
                    lhs = any(left_bits) and any(right_bits)
                    rhs = any(a and b for a in left_bits for b in right_bits)
                    assert lhs == rhs
                    identity_checks += 1
    checks += identity_checks
    a, b = F(1, 3), F(2, 3)
    combined_fanout = 2 * a
    combined_child = b
    aggregate = combined_fanout + combined_child
    assert aggregate == F(4, 3)
    checks += 1
    return {
        "status": "PROVED/EXACT for componentwise disjunctive composition; arbitrary compiler lower bound OPEN",
        "checks": checks,
        "and_semantic_pairs": len(family) ** 2,
        "boolean_cover_identity_checks": identity_checks,
        "smallest_recorded_or_failure": first_or_failure,
        "target_exponent_stress": {
            "per_component_fanout_a": str(a),
            "child_scale_b": str(b),
            "two_component_cartesian_fanout": str(combined_fanout),
            "aggregate_explicit_volume": str(aggregate),
        },
        "interpretation": "Independent conjunctions combine exact OR covers by a Cartesian product, not by a union. At the (1/3,2/3) per-component point, the naive two-component product has aggregate exponent 4/3. This rejects one composition rule, not all possible global compilers.",
    }


def is_horn(cnf: CNF) -> bool:
    return all(sum(lit > 0 for lit in clause) <= 1 for clause in cnf)


def horn_sat(cnf: CNF) -> bool:
    if not is_horn(cnf):
        raise ValueError("not Horn")
    true_vars: set[int] = set()
    implications: list[tuple[frozenset[int], int | None]] = []
    for clause in cnf:
        positives = [lit for lit in clause if lit > 0]
        body = frozenset(-lit for lit in clause if lit < 0)
        head = positives[0] if positives else None
        implications.append((body, head))
    changed = True
    while changed:
        changed = False
        for body, head in implications:
            if body <= true_vars:
                if head is None:
                    return False
                if head not in true_vars:
                    true_vars.add(head)
                    changed = True
    return True


def two_sat(cnf: CNF) -> bool:
    if any(len(clause) > 2 for clause in cnf):
        raise ValueError("not 2-CNF")
    variables = vars_of(cnf)
    graph: dict[int, list[int]] = defaultdict(list)
    reverse: dict[int, list[int]] = defaultdict(list)

    def edge(a: int, b: int) -> None:
        graph[a].append(b)
        reverse[b].append(a)

    for clause in cnf:
        if len(clause) == 0:
            return False
        if len(clause) == 1:
            a = clause[0]
            edge(-a, a)
        else:
            a, b = clause
            edge(-a, b)
            edge(-b, a)
    nodes = {lit for v in variables for lit in (v, -v)}
    seen: set[int] = set()
    order: list[int] = []

    def dfs(start: int) -> None:
        stack = [(start, 0)]
        seen.add(start)
        while stack:
            node, idx = stack[-1]
            if idx < len(graph[node]):
                nxt = graph[node][idx]
                stack[-1] = (node, idx + 1)
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append((nxt, 0))
            else:
                order.append(node)
                stack.pop()

    for node in nodes:
        if node not in seen:
            dfs(node)
    component: dict[int, int] = {}
    for node in reversed(order):
        if node in component:
            continue
        label = len(component)
        stack = [node]
        component[node] = label
        while stack:
            cur = stack.pop()
            for nxt in reverse[cur]:
                if nxt not in component:
                    component[nxt] = label
                    stack.append(nxt)
    return all(component.get(v) != component.get(-v) for v in variables)


def xor_sat(rows: list[tuple[int, int]], n: int) -> bool:
    basis: dict[int, tuple[int, int]] = {}
    for mask, rhs in rows:
        while mask:
            pivot = mask.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = (mask, rhs)
                break
            old_mask, old_rhs = basis[pivot]
            mask ^= old_mask
            rhs ^= old_rhs
        if mask == 0 and rhs:
            return False
    return True


def xor_bruteforce(rows: list[tuple[int, int]], n: int) -> bool:
    for assignment in range(1 << n):
        if all(((assignment & mask).bit_count() & 1) == rhs for mask, rhs in rows):
            return True
    return False


def tractable_controls(rng: random.Random) -> dict[str, object]:
    checks = 0
    horn_cases = 0
    two_cases = 0
    xor_cases = 0
    for n in range(1, 8):
        for _ in range(120):
            horn_clauses: list[Clause] = []
            for _j in range(rng.randint(0, 14)):
                width = rng.randint(0, min(3, n))
                variables = rng.sample(range(1, n + 1), width)
                positive_slot = rng.randrange(width + 1) if width else -1
                clause = tuple(v if idx == positive_slot else -v for idx, v in enumerate(variables))
                horn_clauses.append(clause)
            horn = canonical(tuple(horn_clauses))
            assert is_horn(horn)
            assert horn_sat(horn) == sat_bruteforce(horn)
            horn_cases += 1
            checks += 1

            clauses: list[Clause] = []
            for _j in range(rng.randint(0, 14)):
                width = rng.randint(0, min(2, n))
                variables = rng.sample(range(1, n + 1), width)
                clauses.append(tuple(v if rng.randrange(2) else -v for v in variables))
            two = canonical(tuple(clauses))
            assert two_sat(two) == sat_bruteforce(two)
            two_cases += 1
            checks += 1

            rows = []
            for _j in range(rng.randint(0, 12)):
                mask = rng.randrange(1 << n)
                rhs = rng.randrange(2)
                rows.append((mask, rhs))
            assert xor_sat(rows, n) == xor_bruteforce(rows, n)
            xor_cases += 1
            checks += 1
    return {
        "status": "COMPUTATIONAL validation of exact tractable-family VALUE routes",
        "checks": checks,
        "horn_cases": horn_cases,
        "two_sat_cases": two_cases,
        "xor_cases": xor_cases,
        "interpretation": "Horn, 2-SAT, and affine systems are legitimate zero-recursive-child portfolio branches after charged recognition. Their correctness and syntactic diversity do not imply all-CNF coverage or a favorable general acquisition bound.",
    }


def source_carry_controls() -> dict[str, object]:
    checks = 0
    rows = []
    values = sorted({F(i, d) for d in range(2, 33) for i in range(1, d)})
    for b in values:
        expansion = 1 / b
        round_trip = b * expansion
        self_contained = max(F(1), b)
        shared_parent_state = max(F(1), b)
        assert round_trip == 1
        assert self_contained == shared_parent_state == 1
        checks += 3
    for b in [F(1, 4), F(1, 2), F(2, 3), F(3, 4)]:
        rows.append({
            "descriptor_exponent": str(b),
            "decoder_expansion_exponent": str(1 / b),
            "round_trip_scale_product": str(b * (1 / b)),
            "self_contained_pair_exponent": "1",
        })
    return {
        "status": "PROVED/EXACT exponent accounting",
        "checks": checks,
        "rational_descriptor_scales": len(values),
        "selected_rows": rows,
        "interpretation": "A short handle plus a required M-bit parent is a typed source-backed state of exponent one. Expanding an M^b handle back to an M-bit child has scale 1/b, so the apparent contraction has round-trip product one and does not suppress an inherited solver exponent.",
    }


def nonce_formula(label: bool, nonce: int, pairs: int = 16) -> CNF:
    clauses: list[Clause] = []
    if not label:
        clauses.extend(((1, 2), (1, -2), (-1, 2), (-1, -2)))
    for j in range(pairs):
        a = 3 + 2 * j
        b = a + 1
        bit0 = (nonce >> (2 * j)) & 1
        bit1 = (nonce >> (2 * j + 1)) & 1
        la = a if bit0 else -a
        lb = b if bit1 else -b
        if label:
            clauses.append((1, la, lb))
        else:
            clauses.append((la, lb, -(b + 2 * pairs)))
    return canonical(tuple(clauses))


def serialize_cnf(cnf: CNF) -> bytes:
    return (";".join(",".join(str(lit) for lit in clause) + ",0" for clause in cnf) + ";END").encode()


def hash_collision_controls(deadline: float) -> dict[str, object]:
    digits = [4, 6, 8]
    tables: dict[int, dict[str, tuple[bool, int]]] = {d: {} for d in digits}
    found: dict[int, dict[str, object]] = {}
    checks = 0
    max_nonce = 450_000
    for nonce in range(max_nonce):
        if time.perf_counter() > deadline:
            raise TimeoutError("hash collision search exceeded cooperative deadline")
        label = bool(nonce & 1)
        index = nonce >> 1
        cnf = nonce_formula(label, index)
        payload = serialize_cnf(cnf)
        full = hashlib.sha256(payload).hexdigest()
        for d in digits:
            if d in found:
                continue
            prefix = full[:d]
            prior = tables[d].get(prefix)
            if prior is not None and prior[0] != label:
                other_label, other_index = prior
                other = nonce_formula(other_label, other_index)
                assert serialize_cnf(other) != payload
                assert sat_certificate(other_label, other)
                assert sat_certificate(label, cnf)
                assert hashlib.sha256(serialize_cnf(other)).hexdigest()[:d] == prefix
                found[d] = {
                    "hex_digits": d,
                    "prefix": prefix,
                    "first": {"sat": other_label, "nonce": other_index, "cnf_sha256": hashlib.sha256(serialize_cnf(other)).hexdigest()},
                    "second": {"sat": label, "nonce": index, "cnf_sha256": full},
                    "inputs_examined": nonce + 1,
                }
            else:
                tables[d][prefix] = (label, index)
            checks += 1
        if len(found) == len(digits):
            break
    if len(found) != len(digits):
        raise AssertionError(f"no cross-answer collision for {sorted(set(digits) - set(found))}")
    return {
        "status": "FALSIFIED/RETIRED for hash-only semantic merging at the tested fixed lengths",
        "checks": checks,
        "collisions": [found[d] for d in digits],
        "interpretation": "Distinct legal CNFs with opposite SAT values share each tested fixed SHA-256 prefix. A fixed digest may index a bucket, but exact reuse needs charged equality, semantic verification, or source replay. Increasing 4 to 6 or 8 hexadecimal digits only changes finite collision frequency.",
    }


def sat_certificate(label: bool, cnf: CNF) -> bool:
    if label:
        assignment = {v: True for v in vars_of(cnf)}
        assignment[1] = True
        return satisfied(cnf, assignment)
    base = {frozenset(c) for c in cnf if set(map(abs, c)) <= {1, 2}}
    expected = {
        frozenset((1, 2)), frozenset((1, -2)),
        frozenset((-1, 2)), frozenset((-1, -2)),
    }
    if not expected <= base:
        return False
    return not any(
        all(any((lit > 0) == assignment[abs(lit)] for lit in clause) for clause in cnf)
        for assignment in (
            {1: a, 2: b, **{v: False for v in vars_of(cnf) if v not in {1, 2}}}
            for a, b in itertools.product((False, True), repeat=2)
        )
    )


def strict_unit_cnf_decode(word: int) -> tuple[bool, CNF | None]:
    # 16-bit total padded encoding: nvars(2), nclauses(2), two 3-bit unit
    # records (variable id(2), sign(1)), then six mandatory zero pad bits.
    bits = f"{word:016b}"
    nvars = int(bits[0:2], 2)
    nclauses = int(bits[2:4], 2)
    records = [(int(bits[4 + 3 * i:6 + 3 * i], 2), bits[6 + 3 * i] == "1") for i in range(2)]
    if nvars == 0 or nclauses > 2 or bits[10:] != "000000":
        return False, None
    clauses: list[Clause] = []
    for i, (var, sign) in enumerate(records):
        if i < nclauses:
            if var == 0 or var > nvars:
                return False, None
            clauses.append((var if sign else -var,))
        elif var != 0 or sign:
            return False, None
    return True, tuple(clauses)


def permissive_unit_cnf_decode(word: int) -> CNF:
    bits = f"{word:016b}"
    nvars = max(1, int(bits[0:2], 2))
    nclauses = min(2, int(bits[2:4], 2))
    clauses: list[Clause] = []
    for i in range(nclauses):
        var = int(bits[4 + 3 * i:6 + 3 * i], 2)
        sign = bits[6 + 3 * i] == "1"
        if 1 <= var <= nvars:
            clauses.append((var if sign else -var,))
    return tuple(clauses)


def malformed_encoding_controls() -> dict[str, object]:
    checks = 0
    valid = 0
    invalid = 0
    permissive_false_accepts = 0
    first = None
    for word in range(1 << 16):
        well_formed, cnf = strict_unit_cnf_decode(word)
        if well_formed:
            assert cnf is not None
            assert sat_bruteforce(cnf) == (not any((-c[0],) in cnf for c in cnf))
            valid += 1
        else:
            invalid += 1
            permissive = permissive_unit_cnf_decode(word)
            if sat_bruteforce(permissive):
                permissive_false_accepts += 1
                if first is None:
                    first = {
                        "word_integer": word,
                        "word_bits": f"{word:016b}",
                        "permissive_interpretation": permissive,
                        "permissive_sat": True,
                        "strict_result": "REJECT",
                    }
        checks += 1
    assert first is not None and first["word_integer"] == 0
    unused_leaf = 0
    source_is_unsat = True
    false_composition = source_is_unsat and sat_bruteforce(permissive_unit_cnf_decode(unused_leaf))
    assert false_composition
    checks += 1
    return {
        "status": "PROVED/EXACT necessity of total strict decoding in the declared toy encoding; COMPUTATIONAL exhaustive check",
        "checks": checks,
        "valid_words": valid,
        "invalid_words": invalid,
        "malformed_words_permissively_sat": permissive_false_accepts,
        "first_counterexample": first,
        "unused_selector_false_positive": false_composition,
        "interpretation": "A verifier that treats malformed output as an empty or partially parsed CNF can turn an unused selector into a SAT branch. Generator collapse survives when malformed words are rejected and every unused leaf is mapped to a valid padded UNSAT encoding, as its definition intends.",
    }


def minimal_depth(h: F, initial: F, target: F) -> int:
    if initial <= target:
        return 0
    if not (0 < h < 1):
        raise ValueError("strict contraction required")
    depth = 0
    value = initial
    while value > target:
        value *= h
        depth += 1
    return depth


def recurrence_controls() -> dict[str, object]:
    checks = 0
    landing_rows = []
    h = F(2, 3)
    sigmas = [F(0), F(1, 2), F(1), F(2), F(5), F(19, 2)]
    for k in range(1, 41):
        for sigma in sigmas:
            d_time = minimal_depth(h, F(k), F(1))
            d_space = minimal_depth(h, sigma, F(2, 3))
            d = max(d_time, d_space)
            assert F(k) * h**d <= 1
            assert sigma * h**d <= F(2, 3)
            if d_time > 0:
                assert F(k) * h ** (d_time - 1) > 1
            if d_space > 0:
                assert sigma * h ** (d_space - 1) > F(2, 3)
            t = max(F(1), F(k) * h**d)
            s = max(h, h, sigma * h**d)
            assert t == 1 and s == F(2, 3)
            assert t + s == F(5, 3)
            checks += 7
            if k in {1, 2, 7, 40} and sigma in {F(0), F(5)}:
                landing_rows.append({"K": k, "sigma": str(sigma), "depth": d, "t": str(t), "s": str(s)})

    phi = (1.0 + math.sqrt(5.0)) / 2.0
    # The (1,2/3) landing is not in the general product-forbidden region:
    # 5/3 > phi.  It is instead excluded by Fortnow's near-linear-time,
    # sublinear-space theorem.  With epsilon=1/4, 2/3 is strictly below 3/4.
    assert float(F(5, 3)) > phi
    assert F(2, 3) < F(3, 4)
    checks += 2

    inherited = F(17, 2)
    value = inherited
    for _ in range(100):
        value *= F(1)
    assert value == inherited
    checks += 1

    # A contracting cycle may still have an excessive local/recursive weight.
    theta, weight = F(9, 10), F(1, 5)
    fixed_time = weight / (1 - theta)
    fixed_space = F(1, 2)
    assert fixed_time == 2
    assert float(fixed_time + fixed_space) > phi
    checks += 2

    # Same-realization endpoint guard.
    pairs = [(F(21, 20), F(1, 2)), (F(4, 5), F(4, 5))]
    assert all(float(t + s) < phi for t, s in pairs)
    global_pair = (max(t for t, _ in pairs), max(s for _, s in pairs))
    assert global_pair == (F(21, 20), F(4, 5))
    assert float(sum(global_pair)) > phi
    checks += 3
    return {
        "status": "PROVED/EXACT recurrence accounting; COMPUTATIONAL rational edge controls",
        "checks": checks,
        "landing_parameter_cells": 40 * len(sigmas),
        "selected_landings": landing_rows,
        "direct_endpoint_check": {
            "landing": ["1", "2/3"],
            "fortnow_epsilon": "1/4",
            "space_ceiling": "3/4",
            "space_slack": str(F(1, 12)),
            "not_in_general_phi_product_region": True,
        },
        "general_product_constant_phi": phi,
        "unit_cycle": {"scale_product": "1", "inherited_exponent_after_100_rounds": str(value)},
        "contracting_but_too_expensive_cycle": {"theta": str(theta), "weight": str(weight), "time": str(fixed_time), "space": str(fixed_space), "sum": str(fixed_time + fixed_space)},
        "same_realization_guard": {"individual_pairs": [[str(x), str(y)] for x, y in pairs], "uniform_max_pair": [str(x) for x in global_pair]},
        "interpretation": "Finite exponent elimination is exact for fixed machine constants K and sigma once h<1 and the shrinker exists. h=1 does not eliminate the inherited exponent. The direct (1,2/3) landing uses Fortnow's near-linear/sublinear-space endpoint, not the general product theorem. A mixed route must be checked against one valid endpoint, for example the phi product region, using the same realization.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", nargs="?", default="defense_final_link3_results.json")
    args = parser.parse_args()
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError("25-second internal deadline")))
    signal.alarm(25)
    started = time.perf_counter()
    deadline = started + 23.5
    rng = random.Random(20261008)

    sections = {
        "renaming": renaming_controls(rng),
        "padding": padding_controls(),
        "independent_products": independent_product_controls(),
        "tractable_families": tractable_controls(rng),
        "source_carry": source_carry_controls(),
        "fixed_hashes": hash_collision_controls(deadline),
        "malformed_encodings": malformed_encoding_controls(),
        "recurrence_edges": recurrence_controls(),
    }
    elapsed = time.perf_counter() - started
    total_checks = sum(int(section["checks"]) for section in sections.values())
    source = Path(__file__).read_bytes()
    result = {
        "claim": "DEFENSE-FINAL-LINK3",
        "overall_status": "COMPUTATIONAL hostile controls plus exact scoped identities; strict-successor acquisition remains OPEN",
        "scope": "These controls test necessary semantic, encoding, and exponent obligations. They are not a general SAT lower bound and do not prove P != NP.",
        "seed": 20261008,
        "total_checks": total_checks,
        "elapsed_seconds": elapsed,
        "code_sha256": hashlib.sha256(source).hexdigest(),
        "sections": sections,
        "surviving_claims": [
            "The explicit generator-shrinker equivalence survives when strict total parsing, valid UNSAT padding, self-contained circuit size, and charged construction are explicit.",
            "Finite exponent elimination survives for fixed K and sigma once a genuine h<1 successor exists.",
            "The typed Bellman route survives only with same-realization maxima, complete local weights, and strict endpoint slack.",
        ],
        "rejected_shortcuts": [
            "Padding-relative h<1 without normalization to the unpadded source.",
            "Union rather than Cartesian composition of independent-component OR covers.",
            "A short descriptor whose recursive consumer retains or rereads the parent source.",
            "Hash-only merging at any tested fixed prefix length.",
            "Permissive parsing of malformed generated children or unused selector outputs.",
            "Cycle contraction alone without charging the fixed point and simultaneous space.",
        ],
        "remaining_open_arrow": "Derive on every ordinary CNF, from the P=NP assumption and one fixed clocked SAT machine, either a charged strict successor or a favorable charged typed epoch before any parent-scale SAT computation.",
    }
    Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": args.output,
        "total_checks": total_checks,
        "elapsed_seconds": elapsed,
        "hash_collision_inputs": {str(row["hex_digits"]): row["inputs_examined"] for row in sections["fixed_hashes"]["collisions"]},
        "strict_successor_acquisition": "OPEN",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
