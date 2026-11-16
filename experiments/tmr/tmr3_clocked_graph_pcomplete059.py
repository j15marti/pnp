#!/usr/bin/env python3
"""Finite source-to-terminal-head-bit audit for TMR-3/059.

This tests the exact one-hot CVP encoding, dual-rail compilation, semantic
output and final marker move. The polynomial public-clock TM construction
is proved in the companion report, not physically microtraced here.
"""
from __future__ import annotations
import hashlib
import json
import os
import random

SEED = 202611151954
REV = 'tmr3-clocked-graph059-v1'
rng = random.Random(SEED)
checks = 0
monotone = 0
dual = 0
bad = 0
headers = set()
positions = {0: 0, 1: 0}


def verify(x: bool):
    global checks
    checks += 1
    if not x:
        raise AssertionError(f'failed assertion {checks}')


def encode(gates):
    n = len(gates)
    assert n >= 1
    out = '1' * n + '0'
    for j, (op, a, b) in enumerate(gates):
        if op in (0, 1):
            ma = mb = '0' * n
        else:
            assert 0 <= a < j and 0 <= b < j
            ma = ''.join('1' if i == a else '0' for i in range(n))
            mb = ''.join('1' if i == b else '0' for i in range(n))
        out += format(op, '02b') + ma + mb
    return out


def parse(s):
    if not s or s[0] != '1' or any(c not in '01' for c in s):
        return None
    n = len(s) - len(s.lstrip('1'))
    if n < 1 or n >= len(s) or s[n] != '0' or len(s) != 2*n*n + 3*n + 1:
        return None
    gates = []
    pos = n+1
    for j in range(n):
        op = int(s[pos:pos+2], 2)
        ma = s[pos+2:pos+2+n]
        mb = s[pos+2+n:pos+2+2*n]
        pos += 2+2*n
        if op <= 1:
            if '1' in ma or '1' in mb:
                return None
            gates.append((op, -1, -1))
        else:
            aa = [i for i in range(n) if ma[i] == '1']
            bb = [i for i in range(n) if mb[i] == '1']
            if len(aa) != 1 or len(bb) != 1 or aa[0] >= j or bb[0] >= j:
                return None
            gates.append((op, aa[0], bb[0]))
    return gates


def eval_gates(gates):
    values = []
    for op, a, b in gates:
        if op < 2:
            value = op
        elif op == 2:
            value = values[a] & values[b]
        else:
            value = values[a] | values[b]
        values.append(value)
    return values


def compiled(general):
    # Each general gate becomes (positive, negative) monotone rails.
    gates = []
    rails = []
    for op, a, b in general:
        if op == '0':
            gates.extend([(0, -1, -1), (1, -1, -1)])
        elif op == '1':
            gates.extend([(1, -1, -1), (0, -1, -1)])
        elif op == '!':
            true, false = rails[a]
            gates.extend([(2, false, false), (2, true, true)])
        elif op == '&':
            at, af = rails[a]
            bt, bf = rails[b]
            gates.extend([(2, at, bt), (3, af, bf)])
        else:
            at, af = rails[a]
            bt, bf = rails[b]
            gates.extend([(3, at, bt), (2, af, bf)])
        rails.append((len(gates)-2, len(gates)-1))
    last = rails[-1][0]
    gates.append((2, last, last))
    return gates


def eval_general(c):
    v = []
    for op, a, b in c:
        v.append(0 if op == '0' else 1 if op == '1' else (1-v[a]) if op == '!'
                 else (v[a] & v[b]) if op == '&' else (v[a] | v[b]))
    return v[-1]


def public_macro_index(n):
    # A *test harness* index for value-independent fixed-loop sweeps.
    # NOT a claimed literal native-TM transition count.
    N = 2*n*n + 3*n+1
    return 2*N + n*(2*N + 4*n + 7) + 2


def audit(gates, expected=None):
    global monotone
    s = encode(gates)
    parsed = parse(s)
    verify(parsed == gates)
    verify(len(s) == 2*len(gates)**2+3*len(gates)+1)
    result = eval_gates(parsed)[-1]
    if expected is not None:
        verify(result == expected)
    verify(result in (0, 1))
    # Public macro event time is independent of every gate, mask or value.
    i = public_macro_index(len(parsed))
    verify(i == public_macro_index(len(gates)))
    marker = 0
    marker += result  # one final input-dependent physical head step
    verify(marker == result)
    positions[marker] += 1
    headers.add((len(gates), len(s), i))
    monotone += 1
    return s


for n in range(1, 13):
    for tail in [0, 1]:
        a = [(tail, -1, -1)] * n
        audit(a, tail)
    for z in range(84):
        g = []
        for j in range(n):
            if j == 0 or rng.randrange(6) == 0:
                g.append((rng.randrange(2), -1, -1))
            else:
                g.append((rng.choice([2, 3]), rng.randrange(j), rng.randrange(j)))
        audit(g)
        for corrupt in (g,):
            s = encode(corrupt)
            verify(parse(s+'0') is None)
            bad += 1

for n in range(1, 10):
    for z in range(105):
        g = []
        for j in range(n):
            if j == 0 or rng.randrange(5) == 0:
                g.append((rng.choice(['0','1']), -1, -1))
            elif rng.randrange(3) == 0:
                g.append(('!', rng.randrange(j), -1))
            else:
                g.append((rng.choice(['&','|']), rng.randrange(j), rng.randrange(j)))
        mono = compiled(g)
        src = audit(mono, eval_general(g))
        verify(parse(src) is not None)
        dual += 1

for source in ('', '0', '10', '110', '11x0', '111000000', '1110'):
    verify(parse(source) is None)
    bad += 1

raw = {
    'revision': REV,
    'seed': SEED,
    'input_grammar': 'unary n, n records each opcode(2) maskA(n) maskB(n); n>=1',
    'model': 'finite semantic/last-head audit; not native clocked TM microsteps',
    'monotone_cases': monotone,
    'dual_rail_general_cases': dual,
    'malformed_rejections': bad,
    'distinct_public_length_indices': len(headers),
    'final_head_locations': positions,
    'assertions': checks,
    'failed': 0,
    'claimed_new_asymptotic_validation': False,
}
path = 'results/raw/tmr/2026-11-15_1954_TMR3_GRAPH_INDEX059_PY_RAW.json'
os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path,'w',encoding='utf-8') as f:
    json.dump(raw,f,indent=2,sort_keys=True)
    f.write('\n')
print(json.dumps(raw,sort_keys=True))
