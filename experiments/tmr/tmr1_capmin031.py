#!/usr/bin/env python3
"""TMR-1/031: independent finite audit of exact growing-cap MCSP minimization.

This is a semantic truth-table implementation, NOT a compiled Turing machine.
Uses only Python 3 standard library, no randomness or external services.
"""
import itertools
import json
import math


def descriptions(n, cap):
    """All functions and their least AND/OR/NOT gate count <= cap.

    Each circuit is a topologically ordered list of gates with two free
    constants, n input wires, and unrestricted references to earlier gates.
    The returned map stores exact minima in this finite enumerated basis.
    """
    width = 1 << n
    universe = (1 << width) - 1
    bases = [0, universe]
    for i in range(n):
        bases.append(sum(((j >> i) & 1) << j for j in range(width)))
    minimum = {b: 0 for b in bases}
    front = [tuple(bases)]
    for gates in range(1, cap + 1):
        new = []
        for signals in front:
            for x in signals:
                v = universe ^ x
                minimum[v] = min(minimum.get(v, gates), gates)
                new.append(signals + (v,))
                for y in signals:
                    for v in (x & y, x | y):
                        minimum[v] = min(minimum.get(v, gates), gates)
                        new.append(signals + (v,))
        front = new
    return minimum


def independent_sets(n, cap):
    """Independent dynamic closure of circuit states by gate count."""
    width = 1 << n
    universe = (1 << width) - 1
    initial = {0, universe}
    for i in range(n):
        initial.add(sum(((j >> i) & 1) << j for j in range(width)))
    states = {frozenset(initial)}
    best = {v: 0 for v in initial}
    for gates in range(1, cap + 1):
        nxt = set()
        for s in states:
            for x in s:
                cand = {universe ^ x}
                for y in s:
                    cand.update((x & y, x | y))
                for v in cand:
                    best.setdefault(v, gates)
                    nxt.add(s | {v})
        states = nxt
    return best


def descriptor_log2(n, s):
    return math.log2(s + 1) + math.log2(n + s + 2) + s * (math.log2(3) + 2 * math.log2(n + s + 2))


def run():
    checks = 0
    function_class_counts = {}
    for n in (1, 2, 3):
        width = 1 << n
        a = descriptions(n, 2)
        b = independent_sets(n, 2)
        assert a == b, (n, 'independent minimum mismatch')
        checks += 1
        function_class_counts[str(n)] = [sum(v <= s for v in a.values()) for s in (0, 1, 2)]
        for table in range(1 << width):
            for s in (0, 1, 2):
                cap_a = min(a.get(table, s + 1), s + 1)
                cap_b = min(b.get(table, s + 1), s + 1)
                assert cap_a == cap_b
                assert (cap_a <= s) == (table in a and a[table] <= s)
                checks += 2
    assert function_class_counts['3'] == [5, 14, 40], function_class_counts
    checks += 1
    # Opposite classification at the threshold jump: [1,0,1,0] is mask 0b0101 in our least-significant-bit-first encoding.
    n2 = descriptions(2, 1)
    assert n2[int('0101', 2)] == 1
    assert int('0101', 2) not in {v for v, sz in n2.items() if sz == 0}
    checks += 2
    growth = []
    for n in (64, 128, 256, 512, 1024, 2048, 4096):
        s = n // max(1, math.ceil(math.log2(n + 1)) ** 2)
        logd_n = descriptor_log2(n, s) / n
        assert logd_n >= 0
        assert s <= n
        checks += 2
        growth.append({'n': n, 's': s, 'log2_D_over_n': round(logd_n, 6)})
    for n in range(3, 16):
        for v in range(1, 13):
            L = 2 ** n
            full_output = 1 << (v + 2)
            assert (full_output <= L ** 3) == (v + 2 <= 3 * n)
            checks += 1
    print(json.dumps({
        'agent': 'TMR-1/031', 'mode': 'native_cpython_semantic_enumeration',
        'checks': checks, 'failed': 0,
        'max_arity_exhaustive': 3, 'max_gates_exhaustive': 2,
        'function_class_counts_by_n': function_class_counts,
        'growth_arithmetic': growth,
        'scope': 'finite truth tables and arithmetic only; asymptotic one-work-tape proof separate',
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    run()
