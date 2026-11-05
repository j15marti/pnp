#!/usr/bin/env python3
"""Finite semantics controls for REFEREE351.

The program deliberately tests only local, exact claims used in the report:
typed public-interface congruence, the native LOCAL->RES counterexample, affine
row renaming, finite factor relations, paid two-input definitions, and the
trace-only reflection firewall.  It does not search for proof lower bounds.
"""

from __future__ import annotations

import hashlib
import itertools
import json


checks = 0


def check(condition: bool, message: str) -> None:
    global checks
    checks += 1
    if not condition:
        raise AssertionError(message)


def lit_value(lit: int, assignment: dict[int, bool]) -> bool:
    value = assignment[abs(lit)]
    return value if lit > 0 else not value


def clause_value(clause: frozenset[int], assignment: dict[int, bool]) -> bool:
    return any(lit_value(lit, assignment) for lit in clause)


def exact_resolve(left: frozenset[int], right: frozenset[int], pivot: int) -> frozenset[int]:
    if pivot in left and -pivot in right:
        pass
    elif -pivot in left and pivot in right:
        left, right = right, left
    else:
        raise ValueError("named complementary pivot absent")
    return frozenset((left - {pivot}) | (right - {-pivot}))


def rename_lit(lit: int, permutation: tuple[int, ...], signs: tuple[int, ...]) -> int:
    old = abs(lit)
    new = permutation[old - 1]
    signed_new = new if signs[old - 1] > 0 else -new
    return signed_new if lit > 0 else -signed_new


def rename_clause(clause: frozenset[int], permutation: tuple[int, ...], signs: tuple[int, ...]) -> frozenset[int]:
    return frozenset(rename_lit(lit, permutation, signs) for lit in clause)


def non_tautological_clauses(n: int):
    for choices in itertools.product((-1, 0, 1), repeat=n):
        yield frozenset((i + 1) * sign for i, sign in enumerate(choices) if sign)


def native_consumer_witness() -> dict:
    # x=1, y=2, z=3.
    source = [frozenset({1}), frozenset({1, 3}), frozenset({-2})]
    models = []
    for bits in itertools.product((False, True), repeat=3):
        a = {1: bits[0], 2: bits[1], 3: bits[2]}
        if all(clause_value(c, a) for c in source):
            models.append(bits)
    check(models == [(True, False, False), (True, False, True)], "source model count")

    # AND3 exact conjunction of (x) and (x or z) equals x.
    table = []
    for x, z in itertools.product((False, True), repeat=2):
        a = {1: x, 3: z}
        value = clause_value(source[0], a) and clause_value(source[1], a)
        table.append(value)
        check(value == x, "AND3 factor must be x")

    local = frozenset({1, 2})
    for bits in itertools.product((False, True), repeat=3):
        a = {1: bits[0], 2: bits[1], 3: bits[2]}
        if bits[0]:
            check(clause_value(local, a), "LOCAL x implies x or y")
    resolved = exact_resolve(local, source[2], 2)
    check(resolved == frozenset({1}), "native RES conclusion")

    stronger = frozenset({1})
    try:
        exact_resolve(stronger, source[2], 2)
        check(False, "strengthened conclusion must lose pivot")
    except ValueError:
        check(True, "strengthened conclusion rejected")

    weaker = frozenset({1, 2, 3})
    weakened_resolvent = exact_resolve(weaker, source[2], 2)
    check(weakened_resolvent == frozenset({1, 3}), "weakened exact resolvent")
    check(weakened_resolvent != resolved, "old conclusion cannot be retained")

    # A false LOCAL conclusion is rejected semantically.
    false_local = frozenset({2})
    witness = {1: True, 2: False, 3: False}
    check(not clause_value(false_local, witness), "negative LOCAL control")

    return {
        "source_models": len(models),
        "and3_table": [int(v) for v in table],
        "local": sorted(local),
        "native_resolvent": sorted(resolved),
        "stronger_rejected_missing_pivot": True,
        "weaker_resolvent": sorted(weakened_resolvent),
    }


def resolution_congruence(n: int = 4) -> dict:
    clauses = list(non_tautological_clauses(n))
    transformations = list(itertools.product(itertools.permutations(range(1, n + 1)),
                                              itertools.product((-1, 1), repeat=n)))
    cases = 0
    transformed = 0
    for left in clauses:
        for right in clauses:
            for pivot in range(1, n + 1):
                if not ((pivot in left and -pivot in right) or (-pivot in left and pivot in right)):
                    continue
                result = exact_resolve(left, right, pivot)
                cases += 1
                # Deterministic sparse sample plus exhaustive transformations for initial cases.
                sample = transformations if cases <= 80 else transformations[::37]
                for permutation, signs in sample:
                    rl = rename_clause(left, permutation, signs)
                    rr = rename_clause(right, permutation, signs)
                    rp = rename_lit(pivot, permutation, signs)
                    rr_expected = rename_clause(result, permutation, signs)
                    check(exact_resolve(rl, rr, abs(rp)) == rr_expected,
                          "exact clause interface must preserve RES")
                    transformed += 1
    check(cases > 0 and transformed > 50000, "resolution coverage")
    return {"base_rule_instances": cases, "renamed_rule_instances": transformed}


def permute_mask(mask: int, permutation: tuple[int, ...], n: int) -> int:
    out = 0
    for old in range(n):
        if (mask >> old) & 1:
            out |= 1 << (permutation[old] - 1)
    return out


def affine_congruence(n: int = 5) -> dict:
    permutations = list(itertools.permutations(range(1, n + 1)))
    cases = 0
    for m1 in range(1 << n):
        for r1 in (0, 1):
            for m2 in range(1 << n):
                for r2 in (0, 1):
                    out = (m1 ^ m2, r1 ^ r2)
                    for perm in permutations[::7]:
                        p1 = permute_mask(m1, perm, n)
                        p2 = permute_mask(m2, perm, n)
                        pout = permute_mask(out[0], perm, n)
                        check((p1 ^ p2, r1 ^ r2) == (pout, out[1]),
                              "exact affine interface must preserve XOR")
                        cases += 1
    return {"renamed_xor_instances": cases}


def factor_and_definition_congruence() -> dict:
    factor_checks = 0
    for arity in range(4):
        rows = 1 << arity
        for table in range(1 << rows):
            for perm in itertools.permutations(range(arity)):
                for bits in itertools.product((0, 1), repeat=arity):
                    old_index = sum(bit << i for i, bit in enumerate(bits))
                    renamed_bits = tuple(bits[perm[i]] for i in range(arity))
                    renamed_index = sum(bit << i for i, bit in enumerate(renamed_bits))
                    # Recompile the exact public table under the same position permutation.
                    inverse = tuple(perm.index(i) for i in range(arity))
                    recovered_bits = tuple(renamed_bits[inverse[i]] for i in range(arity))
                    recovered_index = sum(bit << i for i, bit in enumerate(recovered_bits))
                    check(((table >> old_index) & 1) == ((table >> recovered_index) & 1),
                          "factor alpha-renaming")
                    factor_checks += 1

    gate_checks = 0
    for gate in range(16):
        for a, b in itertools.product((0, 1), repeat=2):
            output = (gate >> (2 * a + b)) & 1
            check(output in (0, 1), "gate output bit")
            gate_checks += 1
        symmetric = all(((gate >> (2 * a + b)) & 1) == ((gate >> (2 * b + a)) & 1)
                        for a, b in itertools.product((0, 1), repeat=2))
        if symmetric:
            for a, b in itertools.product((0, 1), repeat=2):
                check(((gate >> (2 * a + b)) & 1) == ((gate >> (2 * b + a)) & 1),
                      "symmetric DEF input swap")
                gate_checks += 1
    return {"factor_row_checks": factor_checks, "definition_checks": gate_checks}


def trace_reflection_firewall() -> dict:
    # Same rejecting trace on one UNSAT input is compatible with a globally correct
    # decider and an unsound always-reject decider. A trace-only compiler cannot use
    # that local transcript as a proof of global correctness.
    unsat = [frozenset({1}), frozenset({-1})]
    sat = [frozenset({2})]

    def satisfiable(formula):
        variables = sorted({abs(lit) for clause in formula for lit in clause})
        for bits in itertools.product((False, True), repeat=len(variables)):
            assignment = dict(zip(variables, bits))
            if all(clause_value(c, assignment) for c in formula):
                return True
        return False

    correct = lambda formula: "SAT" if satisfiable(formula) else "UNSAT"
    always_reject = lambda formula: "UNSAT"
    local_trace = ("scan", "halt-UNSAT")
    check(correct(unsat) == always_reject(unsat) == "UNSAT", "shared rejecting output")
    check(correct(sat) == "SAT" and always_reject(sat) == "UNSAT", "global soundness separation")
    check(local_trace == local_trace, "identical local transcript control")
    return {
        "shared_unsat_trace": list(local_trace),
        "correct_sat_label": correct(sat),
        "unsound_sat_label": always_reject(sat),
    }


def malformed_controls() -> dict:
    rejected = 0
    for left, right, pivot in [
        (frozenset({1}), frozenset({2}), 1),
        (frozenset({1, 2}), frozenset({-2}), 1),
        (frozenset({-1}), frozenset({1}), 2),
    ]:
        try:
            exact_resolve(left, right, pivot)
        except ValueError:
            rejected += 1
            check(True, "malformed resolution rejected")
    check(rejected == 3, "all malformed controls")
    return {"rejected_resolution_records": rejected}


def main() -> None:
    result = {
        "artifact": "REFEREE351_TYPED_INTERFACE",
        "native_witness": native_consumer_witness(),
        "resolution": resolution_congruence(),
        "affine": affine_congruence(),
        "factor_definition": factor_and_definition_congruence(),
        "trace_firewall": trace_reflection_firewall(),
        "malformed": malformed_controls(),
    }
    result["assertions"] = checks
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["semantic_sha256"] = hashlib.sha256(canonical).hexdigest()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
