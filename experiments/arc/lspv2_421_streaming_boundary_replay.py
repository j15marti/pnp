#!/usr/bin/env python3
"""Standalone finite exact boundary-sieve replay, NOT native FLMV machine."""
import hashlib
import json
import math


def make(h, negate):
    rows = [f'p cnf {h + 1} {2*h}', 'c cut 1']
    for i in range(h):
        v = i + 2
        sign = '-1' if negate and i == h - 1 else '1'
        rows.extend((f'c block {v} {v}', f'{sign} {v} 0', f'{sign} -{v} 0'))
    return '\n'.join(rows) + '\n'


def exact_sat(clauses):
    if not clauses:
        return True
    if any(len(c) == 0 for c in clauses):
        return False
    v = abs(clauses[0][0])
    for value in (True, False):
        rem = []
        for c in clauses:
            if (v if value else -v) in c:
                continue
            rem.append([t for t in c if t != (-v if value else v)])
        if exact_sat(rem):
            return True
    return False


def check_case(h, negate):
    source = make(h, negate)
    N = len(source.encode()) * 8
    surviving = [True, True]
    calls = 0
    maximum = 0
    emitted = 0
    for i in range(h):
        v = i + 2
        literal = -1 if negate and i == h - 1 else 1
        group = [(literal, v), (literal, -v)]
        for boundary in range(2):
            if not surviving[boundary]:
                continue
            child = []
            for c in group:
                satisfied = (c[0] > 0) == bool(boundary)
                if not satisfied:
                    child.append(list(c[1:]))
            text = f'p cnf {h+1} {len(child)}\n'
            text += ''.join(' '.join(map(str, c)) + (' ' if c else '') + '0\n' for c in child)
            size = len(text.encode()) * 8
            maximum = max(maximum, size)
            emitted += size
            if not exact_sat(child):
                surviving[boundary] = False
            calls += 1
    result = {
        'h': h,
        'negative': negate,
        'answer': any(surviving),
        'N_bits': N,
        'actual_calls': calls,
        'possible_calls': 2*h,
        'max_child_bits': maximum,
        'child_cap_bits': math.isqrt(N),
        'call_cap': int(N**0.6),
        'emitted_bits': emitted,
        'source_sha256': hashlib.sha256(source.encode()).hexdigest(),
    }
    assert result['answer'] == (not negate)
    if h == 700:
        assert maximum <= math.isqrt(N)
        assert 2*h <= int(N**0.6)
    return result


def main():
    items = [check_case(h, negate) for h in (2, 7, 100, 700) for negate in (False, True)]
    print(json.dumps({'status': 'FINITE_REPLAY_PASS', 'cases': items, 'native_flmv_execution': False}, indent=2))


if __name__ == '__main__':
    main()
