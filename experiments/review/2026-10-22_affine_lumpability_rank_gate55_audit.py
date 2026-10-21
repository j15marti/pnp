#!/usr/bin/env python3
"""Finite controls for AFFINE-LUMPABILITY-RANK-GATE55.

The accompanying report proves the general affine rank criterion.  This audit
checks small random instances, exact quotient propagation, collision witnesses,
and the DIGEST-LUMP19 nonlinear consistency gadget.  Finite checks do not imply
P=RP, P!=RP, or P!=NP.
"""

import json
import random


checks = 0
good_instances = 0
bad_instances = 0
propagation_steps = 0
nonlinear_assignments = 0


def check(condition):
    global checks
    checks += 1
    assert condition


def parity(x):
    return x.bit_count() & 1


def apply(rows, vector):
    return sum(parity(row & vector) << i for i, row in enumerate(rows))


def rank(rows):
    basis = {}
    for row in rows:
        x = row
        while x:
            pivot = x.bit_length() - 1
            if pivot in basis:
                x ^= basis[pivot]
            else:
                basis[pivot] = x
                break
    return len(basis)


def compose(left_rows, right_rows):
    """Rows for the linear map left(right(x))."""
    output = []
    for left in left_rows:
        row = 0
        for i, right in enumerate(right_rows):
            if (left >> i) & 1:
                row ^= right
        output.append(row)
    return output


def rowspace_coefficients(target, rows):
    for mask in range(1 << len(rows)):
        value = 0
        for i, row in enumerate(rows):
            if (mask >> i) & 1:
                value ^= row
        if value == target:
            return mask
    return None


def quotient_rows(hash_rows, transition_rows):
    ha_rows = compose(hash_rows, transition_rows)
    q_rows = []
    for target in ha_rows:
        coefficients = rowspace_coefficients(target, hash_rows)
        if coefficients is None:
            return None
        q_rows.append(coefficients)
    return q_rows


def random_full_rank(rows, columns, rng):
    while True:
        matrix = [rng.randrange(1 << columns) for _ in range(rows)]
        if rank(matrix) == rows:
            return matrix


def preimages(rows, target, input_bits):
    return [x for x in range(1 << input_bits) if apply(rows, x) == target]


def construct_lumpable_transition(hash_rows, state_bits, rng):
    hash_bits = len(hash_rows)
    q_rows = [rng.randrange(1 << hash_bits) for _ in range(hash_bits)]
    qh_rows = compose(q_rows, hash_rows)
    columns = []
    for column in range(state_bits):
        desired = sum(((row >> column) & 1) << i for i, row in enumerate(qh_rows))
        choices = preimages(hash_rows, desired, state_bits)
        columns.append(rng.choice(choices))
    transition_rows = []
    for output_bit in range(state_bits):
        transition_rows.append(
            sum(((columns[column] >> output_bit) & 1) << column for column in range(state_bits))
        )
    return transition_rows


def transition(rows, coin_rows, constant, state, coin):
    return apply(rows, state) ^ apply(coin_rows, coin) ^ constant


rng = random.Random(202610220348)
size_results = []
for state_bits in range(3, 8):
    hash_bits = min(3, state_bits - 1)
    local_good = 0
    local_bad = 0
    for _ in range(80):
        hash_rows = random_full_rank(hash_bits, state_bits, rng)

        # Positive instance: construct A with H A = Q H, recover Q from rows,
        # and exhaustively verify same-fiber transition consistency.
        a_rows = construct_lumpable_transition(hash_rows, state_bits, rng)
        derived_q = quotient_rows(hash_rows, a_rows)
        check(derived_q is not None)
        check(rank(hash_rows + compose(hash_rows, a_rows)) == rank(hash_rows))
        coin_bits = 2
        b_rows = [rng.randrange(1 << coin_bits) for _ in range(state_bits)]
        constant = rng.randrange(1 << state_bits)
        hb_rows = compose(hash_rows, b_rows)
        hc = apply(hash_rows, constant)
        for state in range(1 << state_bits):
            h = apply(hash_rows, state)
            for coin in range(1 << coin_bits):
                next_state = transition(a_rows, b_rows, constant, state, coin)
                predicted = apply(derived_q, h) ^ apply(hb_rows, coin) ^ hc
                check(apply(hash_rows, next_state) == predicted)
        good_instances += 1
        local_good += 1

        # Negative instance: rejection of the rank test must yield a concrete
        # same-hash pair whose next hashes disagree for the same coin.
        while True:
            bad_a = [rng.randrange(1 << state_bits) for _ in range(state_bits)]
            if quotient_rows(hash_rows, bad_a) is None:
                break
        ha_rows = compose(hash_rows, bad_a)
        witness = next(
            z
            for z in range(1, 1 << state_bits)
            if apply(hash_rows, z) == 0 and apply(ha_rows, z) != 0
        )
        check(apply(hash_rows, 0) == apply(hash_rows, witness))
        check(apply(hash_rows, apply(bad_a, 0)) != apply(hash_rows, apply(bad_a, witness)))
        check(rank(hash_rows + ha_rows) > rank(hash_rows))
        bad_instances += 1
        local_bad += 1
    size_results.append(
        {"state_bits": state_bits, "hash_bits": hash_bits, "good": local_good, "bad": local_bad}
    )


# Exact dynamic propagation on the quotient versus enumeration of complete
# state distributions.  One fresh random coin bit is consumed per step.
propagation_cases = 0
for _ in range(240):
    state_bits = rng.randrange(3, 8)
    hash_bits = rng.randrange(1, min(3, state_bits - 1) + 1)
    hash_rows = random_full_rank(hash_bits, state_bits, rng)
    initial = rng.randrange(1 << state_bits)
    state_counts = {initial: 1}
    hash_counts = {apply(hash_rows, initial): 1}
    steps = rng.randrange(1, 8)
    for _step in range(steps):
        a_rows = construct_lumpable_transition(hash_rows, state_bits, rng)
        q_rows = quotient_rows(hash_rows, a_rows)
        b_rows = [rng.randrange(2) for _ in range(state_bits)]
        constant = rng.randrange(1 << state_bits)
        hb_rows = compose(hash_rows, b_rows)
        hc = apply(hash_rows, constant)

        next_states = {}
        for state, count in state_counts.items():
            for coin in range(2):
                nxt = transition(a_rows, b_rows, constant, state, coin)
                next_states[nxt] = next_states.get(nxt, 0) + count

        next_hashes = {}
        for h, count in hash_counts.items():
            for coin in range(2):
                nxt = apply(q_rows, h) ^ apply(hb_rows, coin) ^ hc
                next_hashes[nxt] = next_hashes.get(nxt, 0) + count

        aggregated = {}
        for state, count in next_states.items():
            h = apply(hash_rows, state)
            aggregated[h] = aggregated.get(h, 0) + count
        check(aggregated == next_hashes)
        check(sum(next_hashes.values()) == 1 << (_step + 1))

        state_counts = next_states
        hash_counts = next_hashes
        propagation_steps += 1
    propagation_cases += 1


# DIGEST-LUMP19 consistency gadget.  For h=b and
# h'=b OR (F(u) AND t), universal same-hash consistency holds iff F is UNSAT.
nonlinear_results = []
for input_bits in range(1, 4):
    table_count = 1 << (1 << input_bits)
    consistent_count = 0
    for table in range(table_count):
        globally_consistent = True
        for b in range(2):
            outputs = set()
            for u in range(1 << input_bits):
                f = (table >> u) & 1
                for t in range(2):
                    outputs.add(b | (f & t))
                    nonlinear_assignments += 1
            if len(outputs) != 1:
                globally_consistent = False
        check(globally_consistent == (table == 0))
        consistent_count += globally_consistent
    check(consistent_count == 1)
    nonlinear_results.append(
        {"input_bits": input_bits, "truth_tables": table_count, "consistent_tables": consistent_count}
    )


result = {
    "run_id": "AFFINE-LUMPABILITY-RANK-GATE55",
    "status": "PASS",
    "assertions": checks,
    "lumpable_affine_instances": good_instances,
    "non_lumpable_affine_instances": bad_instances,
    "quotient_propagation_cases": propagation_cases,
    "quotient_propagation_steps": propagation_steps,
    "nonlinear_gadget_assignments": nonlinear_assignments,
    "size_results": size_results,
    "nonlinear_results": nonlinear_results,
    "scope": (
        "Finite controls for a proved affine rank criterion and a nonlinear "
        "coNP-hardness gadget. No unrestricted derandomization, lower bound, "
        "or complexity-class separation is claimed."
    ),
}
print(json.dumps(result, indent=2, sort_keys=True))
