#!/usr/bin/env python3
"""Independent finite tests of length-blind fixed-gate cofactor inheritance.
A semantic-mask finite proxy, NOT a native one-tape TM compiler.
"""
import itertools
import json
import random


def circuit_functions(n, s):
    width = 1 << n
    full = (1 << width) - 1
    wires = [0, full]
    for j in range(n):
        wires.append(sum(((i >> j) & 1) << i for i in range(width)))
    functions = set(wires)
    layers = {tuple(wires)}
    for _ in range(s):
        next_layers = set()
        for prev in layers:
            for a in prev:
                v = full ^ a
                functions.add(v)
                next_layers.add(prev + (v,))
            for a in prev:
                for b in prev:
                    for v in (a & b, a | b):
                        functions.add(v)
                        next_layers.add(prev + (v,))
        layers = next_layers
    return functions


def online_exact(bits, catalog):
    if len(bits) < 1:
        return False, 0
    flags = {v: (v & 1) == bits[0] for v in catalog[0]}
    transitions = 0
    for i in range(1, len(bits)):
        if i & (i - 1) == 0:
            n = i.bit_length()
            old = flags
            prefix_mask = (1 << i) - 1
            flags = {v: old[v & prefix_mask] for v in catalog[n]}
            transitions += len(flags)
        for v in flags:
            flags[v] = flags[v] and (((v >> i) & 1) == bits[i])
            transitions += 1
    if len(bits) & (len(bits) - 1):
        return False, transitions
    return any(flags.values()), transitions


def main():
    random.seed(20261114)
    max_n = 4
    results = []
    total = 0
    for s in (0, 1, 2):
        catalog = [circuit_functions(n, s) for n in range(max_n + 1)]
        cofactor_checks = sum(sum((v & ((1 << (1 << (n - 1))) - 1)) in catalog[n - 1]
                                  for v in catalog[n]) for n in range(1, max_n + 1))
        tested, yes, no, count_transitions = 0, 0, 0, 0
        for n in range(0, max_n + 1):
            N = 1 << n
            samples = range(1 << N) if n <= 3 else [random.getrandbits(N) for _ in range(512)]
            for mask in samples:
                bits = [(mask >> i) & 1 for i in range(N)]
                answer, steps = online_exact(bits, catalog)
                expected = mask in catalog[n]
                assert answer == expected, (s, n, mask, answer, expected)
                tested += 1
                count_transitions += steps
                yes += int(answer)
                no += int(not answer)
            # length-blind malformed controls at nonpower lengths, using enough stored candidates
            if n < max_n:
                for bad in (N + 1,):
                    if bad & (bad - 1):
                        flags = [random.randint(0, 1) for _ in range(bad)]
                        got, _ = online_exact(flags, catalog)
                        assert not got, (s, bad)
                        tested += 1
        total += tested + cofactor_checks
        results.append({"s": s, "candidate_count_by_n": [len(c) for c in catalog],
                        "cofactor_checks": cofactor_checks,
                        "exact_cases": tested, "yes": yes, "no": no,
                        "proxy_flag_updates": count_transitions})
    print(json.dumps({"test": "FIXEDGATE_STREAM028", "status": "PASS",
                      "model": "finite semantic-mask emulator, not one-tape physical implementation",
                      "checks": total, "results": results}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
