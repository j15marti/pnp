#!/usr/bin/env python3
"""Independent exact finite controls for TMR-1/029 padding transition theorem.
Only small exhaustive gate-count checks are computational; asymptotic theorem is separate.
"""
import json, math, hashlib
from pathlib import Path


def circuit_caps(n, cap=2):
    nbits = 1 << n
    full = (1 << nbits) - 1
    base = [0, full]
    base += [sum(((i >> j) & 1) << i for i in range(nbits)) for j in range(n)]
    mins = {f: 0 for f in base}
    states = {()}
    for gates in range(1, cap + 1):
        new = set()
        for old in states:
            wires = base + list(old)
            for x in wires:
                new.add(old + (full ^ x,))
                for y in wires:
                    new.add(old + (x & y,))
                    new.add(old + (x | y,))
        states = new
        for gate_tuple in states:
            val = gate_tuple[-1]
            mins.setdefault(val, gates)
    return mins


def pad_bits(f, n, r):
    width = 1 << n
    return sum(f << (j * width) for j in range(1 << r))


def check_numeric(n, a, b):
    assert n >= 8 and 0 < a < b
    s = (1 << n) // (16 * n)
    # Upper bound on the logarithm of the number of circuits with <=s gates.
    ub = math.log2(s + 1) + math.log2(n + s + 2) + s * (math.log2(3) + 2 * math.log2(n + s + 2))
    assert ub < (1 << n), (n, ub)
    B = n * (1 << n) + n + 2
    r = 0
    # Exact algebraic comparisons for fractional powers: 2^(a(n+r)/b) >= B.
    while (1 << (a * (n + r))) < B ** b:
        r += 1
    upper_r = r
    assert (1 << (a * (n + upper_r))) >= B ** b
    if upper_r > 0:
        assert (1 << (a * (n + upper_r - 1))) < B ** b
    lower_r = -1
    for r in range(upper_r + 1):
        # 2^(a(n+r)/b) < s+1 implies floor of threshold <=s.
        if (1 << (a * (n + r))) < (s + 1) ** b:
            lower_r = r
    assert lower_r < upper_r
    return {'n': n, 'mu': f'{a}/{b}', 'NO_guaranteed_through_r': lower_r,
            'all_YES_by_r': upper_r, 'transition_width_at_most': upper_r - lower_r - 1,
            'old_N_bits': str(1 << n), 'out_N_at_upper_bits': upper_r + n}


def main():
    comparisons = 0
    examples = []
    for n in (1, 2, 3):
        original = circuit_caps(n)
        for r in (1, 2) if n < 3 else (1,):
            padded = circuit_caps(n + r)
            for f in range(1 << (1 << n)):
                a = original.get(f, 3)
                b = padded.get(pad_bits(f, n, r), 3)
                assert a == b, (n, r, f, a, b)
                comparisons += 1
            examples.append({'arity': n, 'dummy_inputs': r, 'functions': 1 << (1 << n),
                             'gate_cap': 2, 'status': 'PASS'})
    numeric = [check_numeric(n, a, b) for n in (8, 12, 16, 32, 64, 128)
               for a, b in ((1, 4), (1, 2), (3, 4))]
    out = {'tag': 'TMR1_PADWINDOW035', 'gate_cap_checks': comparisons,
           'positive_numeric_checks': len(numeric), 'failures': 0,
           'gate_tests': examples, 'transition_samples': numeric,
           'status': 'COMPUTATIONAL finite tests only; theorem requires separate proof'}
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
