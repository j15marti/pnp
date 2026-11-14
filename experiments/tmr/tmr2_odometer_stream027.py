#!/usr/bin/env python3
"""TMR-2/027: independent physical-tape proxy of improved MCSP[0] streaming decision.

One working tape stores interleaved (binary length-counter bit, projection-match flag)
cells; finite control holds carry, current input bit, all-zero, all-one.
The model supports a one-way read-only input and O(1) work per visited tape cell.
Python list/index are validation instrumentation, not charged word-RAM primitives.
"""
import json
import random
import math


def streamed_zero_gate(word, check_invariants=False):
    # Tape spans [left marker, B_0, ..., B_k, right marker]; data cells below.
    # Cell B_i=(i-th bit of the number already read, projection x_i match).
    tape = [[0, 1]]
    a0, a1 = 1, 1
    transitions = 0
    max_data_cells = 1
    observed = [] if check_invariants else None
    for bit in word:
        if bit not in (0, 1):
            raise ValueError("only binary input")
        # Capture the input bit in the fixed control, then advance input head.
        transitions += 1
        a0 &= 1 - bit
        a1 &= bit
        carry = 1
        # Single forward sweep. Read old counter bit before increment,
        # compare the projection's current bit, and propagate the carry.
        for cell in tape:
            old = cell[0]
            cell[1] &= int(bit == old)
            cell[0] = old ^ carry
            carry &= old
            transitions += 2  # local read/write and rightward head move
        if carry:
            # Current source index was 2^k-1. The new input bit x_k is
            # zero at every previously observed coordinate, so its matching
            # flag is precisely the just-updated all-zero prefix flag.
            tape.append([1, a0])
            transitions += 3  # extend boundary, mark new cell, move right
        # Return the single work head to the beginning, including end marker.
        transitions += len(tape) + 1
        max_data_cells = max(max_data_cells, len(tape))
        if check_invariants:
            observed.append(bit)
            count = len(observed)
            assert sum(c[0] << i for i, c in enumerate(tape)) == count
            for i, cell in enumerate(tape):
                match = all(observed[j] == ((j >> i) & 1) for j in range(count))
                assert cell[1] == int(match), (count, i, cell, observed)
            assert a0 == int(not any(observed))
            assert a1 == int(all(observed))
    # Endmarker check: a positive power-of-two length at least 2. The top
    # counter position has not been an input variable yet, so exclude it.
    is_length_valid = len(tape) >= 2 and sum(c[0] for c in tape) == 1 and tape[-1][0] == 1
    if not is_length_valid:
        return None, transitions + 2 * len(tape), max_data_cells
    accepted = bool(a0 or a1 or any(cell[1] for cell in tape[:-1]))
    return accepted, transitions + 2 * len(tape), max_data_cells


def independent_decision(word):
    N = len(word)
    if N < 2 or N & (N - 1):
        return None
    if all(v == 0 for v in word) or all(v == 1 for v in word):
        return True
    n = N.bit_length() - 1
    return any(all(word[j] == ((j >> i) & 1) for j in range(N)) for i in range(n))


def zero_gate_code(n):
    N = 1 << n
    c = [tuple([v] * N) for v in (0, 1)]
    c += [tuple((j >> i) & 1 for j in range(N)) for i in range(n)]
    assert len(set(c)) == n + 2
    return c


def min_dist(word, code):
    return min(sum(x != y for x, y in zip(word, f)) for f in code)


def exact_query_certificate_checks():
    # New general packing lemma: for any code with pairwise distances >=2r,
    # a YES query transcript has exact minimum possible length N-r+1.
    # Check the 0-gate code for every eta radius r in 1..N/4.
    cases = 0
    flips = 0
    from itertools import combinations
    out = []
    for n in (2, 3, 4):
        N = 1 << n
        C = zero_gate_code(n)
        d = min(sum(a != b for a, b in zip(x, y)) for k, x in enumerate(C) for y in C[k+1:])
        assert d == N // 2
        for r in range(1, N // 4 + 1):
            for x in C:
                # All r-subset flips are promised NO. This defeats every
                # < N-r+1-query accepting path by selecting an unseen r-set.
                for indices in combinations(range(N), r):
                    y = list(x)
                    for j in indices:
                        y[j] ^= 1
                    assert min_dist(y, C) >= r
                    flips += 1
                cases += 1
            # Upper: fixed first N-r+1 positions allow a sound promise
            # decision, because unseen positions number only r-1.
            # Exhaust all complete 16-bit tables at largest n.
            q = N - r + 1
            rejected_far = 0
            accepted_yes = 0
            for mask in range(1 << N):
                y = tuple((mask >> j) & 1 for j in range(N))
                is_consistent = any(y[:q] == f[:q] for f in C)
                distance = min_dist(y, C)
                if distance == 0:
                    assert is_consistent
                    accepted_yes += 1
                elif distance >= r:
                    assert not is_consistent
                    rejected_far += 1
            out.append({"n": n, "N": N, "r": r, "distance": d, "query_depth": q,
                        "accepted_yes": accepted_yes, "rejected_promised_no": rejected_far})
    return cases, flips, out


def main():
    exhaustive = 0
    yes = no = 0
    max_ratio = 0
    layer=[]
    for n in (1, 2, 3, 4):
        N = 1 << n
        y = 0
        max_cells = 0
        max_steps = 0
        for mask in range(1 << N):
            word = tuple((mask >> j) & 1 for j in range(N))
            got, step, cells = streamed_zero_gate(word, check_invariants=(n <= 3))
            assert got == independent_decision(word), (n, mask, got)
            max_cells = max(max_cells, cells)
            max_steps = max(max_steps, step)
            y += int(got)
        assert y == n + 2
        layer.append({"n": n, "N": N, "inputs": 1 << N, "yes": y,
                      "max_work_cells": max_cells, "max_proxy_steps": max_steps})
        exhaustive += 1 << N
        yes += y
        no += (1 << N) - y
    rng = random.Random(20261114)
    random_checked = 0
    for N in (32, 64, 128):
        for _ in range(64):
            word = tuple(rng.randrange(2) for j in range(N))
            got, step, cells = streamed_zero_gate(word, check_invariants=(N <= 64))
            assert got == independent_decision(word)
            assert cells <= N.bit_length() + 1
            max_ratio = max(max_ratio, step / (N * math.log2(N + 2)))
            random_checked += 1
    malformed = 0
    for N in range(0, 45):
        if N not in (2, 4, 8, 16, 32):
            word = [0] * N
            assert streamed_zero_gate(word)[0] is None
            malformed += 1
    cert_cases, flip_checks, cert_layers = exact_query_certificate_checks()
    output = {
        "study": "TMR2-027-ODOMETER-CODE-CERTIFICATE",
        "model": "N=2^n, free constants/input wires, 0 AND/OR/NOT gates; one-way source, single locally moving work tape",
        "implementation": "independent Python local-tape-cell proxy of symbol-level update; symbolic finite TM compiler",
        "exhaustive_full_tables": exhaustive, "positive_tables": yes, "negative_tables": no,
        "layers": layer, "random_large_tables": random_checked, "malformed_lengths": malformed,
        "exact_code_certificate_cases": cert_cases, "flipped_far_no_witnesses": flip_checks,
        "certificate_layers": cert_layers, "max_proxy_step_ratio_to_NlogN": max_ratio,
        "failed_assertions": 0,
        "warning": "finite tests are COMPUTATIONAL and do not imply any positive-threshold MCSP time lower bound"
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
