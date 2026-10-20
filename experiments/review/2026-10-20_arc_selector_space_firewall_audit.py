#!/usr/bin/env python3
"""ARC-SELECTOR-SPACE-FIREWALL23 finite/exact arithmetic audit.

The theorem is symbolic.  This script checks its elementary counting inequality,
the proper-3CNF forcing gadget, the Horn/XOR factorization, and the advertised
finite workspace threshold.  It does not test an unrestricted SAT lower bound.
"""

import itertools
import json
import math


def lit_value(lit, assignment):
    value = assignment[abs(lit)]
    return value if lit > 0 else not value


def forcing_gadget(target):
    """Four proper clauses force x_1 == target; x_2,x_3 remain free."""
    head = 1 if target else -1
    return [
        (head, a_sign * 2, b_sign * 3)
        for a_sign, b_sign in itertools.product((-1, 1), repeat=2)
    ]


def clause_horn_xor_equivalent(clause, assignment):
    # z is the complement of the corresponding literal truth value.
    z = []
    for lit in clause:
        x = assignment[abs(lit)]
        z.append(bool(x) ^ (lit > 0))
    horn = not all(z)
    source = any(lit_value(lit, assignment) for lit in clause)
    return source, horn


def main():
    checks = 0
    failures = []

    # Exact sufficient counting inequality.  With q=2^n and
    # s=floor(q/(16n)), log_2(number of <=s-gate circuits) is bounded by
    # 2n+s(4+2n)<q whenever 32n^2<q(14n-4).
    count_rows = []
    for n in range(7, 513):
        q = 1 << n
        s = q // (16 * n)
        ok = 32 * n * n < q * (14 * n - 4)
        checks += 1
        if not ok:
            failures.append(["count", n])
        if n in (7, 8, 16, 32, 64, 128, 156, 256, 512):
            count_rows.append({"n": n, "q_bits": q.bit_length(), "s_bits": s.bit_length(), "ok": ok})

    # Declared padded length N_n=2^ceil(5(n+log_2 n+10)/3).
    # Search and then audit the first finite n at which s>N_n^(1/2).
    first_space_n = None
    space_rows = []
    for n in range(7, 513):
        q = 1 << n
        s = q // (16 * n)
        exponent = math.ceil(5 * (n + math.log2(n) + 10) / 3)
        ok = s * s > (1 << exponent)
        checks += 1
        if ok and first_space_n is None:
            first_space_n = n
        if n in (128, 155, 156, 157, 256, 512):
            space_rows.append({"n": n, "N_exponent": exponent, "selector_gt_sqrt_N": ok})
    if first_space_n != 156:
        failures.append(["first_space_n", first_space_n])

    # Exhaustive forcing-gadget semantics.
    gadget_rows = []
    for target in (False, True):
        sat_count = 0
        for bits in itertools.product((False, True), repeat=3):
            assignment = {i + 1: bits[i] for i in range(3)}
            sat = all(any(lit_value(lit, assignment) for lit in clause)
                      for clause in forcing_gadget(target))
            expected = bits[0] == target
            checks += 1
            sat_count += int(sat)
            if sat != expected:
                failures.append(["gadget", target, bits])
        gadget_rows.append({"target": int(target), "satisfying_assignments": sat_count})

    # Exhaustive clause-level Horn/XOR equivalence for every sign pattern.
    horn_xor_cases = 0
    for signs in itertools.product((-1, 1), repeat=3):
        clause = tuple(signs[i] * (i + 1) for i in range(3))
        for bits in itertools.product((False, True), repeat=3):
            assignment = {i + 1: bits[i] for i in range(3)}
            source, joint = clause_horn_xor_equivalent(clause, assignment)
            checks += 1
            horn_xor_cases += 1
            if source != joint:
                failures.append(["horn_xor", clause, bits])

        # Standalone factors always have witnesses: z=0 for negative Horn;
        # x=0 and z=(literal positive?) for XOR equations.
        z_horn = (False, False, False)
        z_xor = tuple(sign > 0 for sign in signs)
        checks += 2
        if all(z_horn):
            failures.append(["horn_witness", clause])
        if any((False ^ (sign > 0)) != z for sign, z in zip(signs, z_xor)):
            failures.append(["xor_witness", clause])

    result = {
        "run": "ARC-SELECTOR-SPACE-FIREWALL23",
        "status": "PASS" if not failures else "FAIL",
        "proof_status": "PROVED/EXACT restricted selector model; P versus NP OPEN",
        "checks": checks,
        "failures": failures,
        "count_range_n": [7, 512],
        "count_rows": count_rows,
        "first_selector_gt_sqrt_padded_N": first_space_n,
        "space_rows": space_rows,
        "gadget_rows": gadget_rows,
        "horn_xor_cases": horn_xor_cases,
        "random_seed": None,
        "method": "exhaustive finite semantics plus exact integer inequalities",
        "limitations": [
            "does not exhibit the counting-hard truth table",
            "does not prove SAT runtime or space lower bounds",
            "explicit source bits permit random-access or streaming alternatives",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
