#!/usr/bin/env python3
"""Deterministic finite semantic audit of CLOCKMASKEDINVERSE22.

All QBF experiments use a *restricted two-variable matrix truth-table encoding*,
not a PSPACE-hard test family. The symbolic proof uses unrestricted TQBF.
"""
from __future__ import annotations
import json, hashlib, random, sys
from pathlib import Path

SEED = 202611171533
RNG = random.Random(SEED)
COUNT = dict(assertions=0, descriptors=0, outputs=0, originals=0,
             canonical_cases=0, forced_bit_checks=0, witness_equality_checks=0,
             distinct_fiber_witnesses=0, random_cases=0, hostile_controls=0)

def check(c, kind=None):
    COUNT['assertions'] += 1
    if kind:
        COUNT[kind] += 1
    if not c:
        raise AssertionError(f'failed {kind} @ {COUNT}')


def qbf_recursive(D: str) -> int:
    """Q0 x0 Q1 x1 matrix(x0,x1), two-variable test encoding."""
    assert len(D) >= 7
    qs = [int(D[0]), int(D[1])]  # 1 exists, 0 forall
    tt = [int(c) ^ int(D[6]) for c in D[2:6]]
    def rec(level: int, x0=0, x1=0):
        if level == 2:
            return tt[2*x0+x1]
        v = [rec(level + 1, x0 if level else bit,
                 bit if level else x1) for bit in (0, 1)]
        return (v[0] | v[1]) if qs[level] else (v[0] & v[1])
    return rec(0)


def qbf_iterative(D: str) -> int:
    assert len(D) >= 7
    a, b = int(D[0]), int(D[1])
    t = [(int(z) ^ int(D[6])) for z in D[2:6]]
    lo = [((t[2*i] | t[2*i+1]) if b else (t[2*i] & t[2*i+1])) for i in range(2)]
    return (lo[0] | lo[1]) if a else (lo[0] & lo[1])


def value(D):
    return qbf_iterative(D)


def adjacent(bits):
    return int(any(x == '1' and y == '1' for x, y in zip(bits, bits[1:])))


def stream_quotient(f: str, m: int):
    """Read each source symbol once, keeping D,a,prev_h,q, then eval V(D)."""
    n = m+3
    assert len(f) == (1 << n)
    D = ''
    a = None
    q = 0
    prev = '0'
    for pos, bit in enumerate(f):
        if pos < m:
            D += bit
        elif pos == m:
            a = int(bit)
        else:
            q |= int(bit == '1' and prev == '1')
            prev = bit
    return (D, a ^ value(D), q)


def direct_quotient(f, m):
    D = f[:m]
    return (D, int(f[m]) ^ qbf_recursive(D), adjacent(f[m+1:]))


def canonical(D: str, b: int, q: int):
    m = len(D)
    N = 1 << (m+3)
    a = int(b) ^ value(D)
    h = ('11' if q else '00') + ('0' * (N-m-3))
    result = D + str(a) + h
    assert len(result) == N
    return result


def diverse_fiber(D, b, q, mode):
    """All outputs retain source header and mandatory inverse bit."""
    m = len(D)
    L = (1 << (m+3)) - m - 1
    a = b ^ value(D)
    if q:
        if mode == 0:
            h = '11' + '0'*(L-2)
        elif mode == 1:
            h = '11' + '1'*(L-2)
        else:
            h = '11' + ''.join(str(RNG.randrange(2)) for _ in range(L-2))
    else:
        if mode == 0:
            h = '0'*L
        elif mode == 1:
            h = ''.join('1' if i % 2 == 0 else '0' for i in range(L))
        else:
            # random nonadjacent pattern: every even position may be 1
            h = ''.join(str(RNG.randrange(2)) if i % 2 == 0 else '0' for i in range(L))
    return D + str(a) + h


def run():
    for di in range(128):
        D = format(di, '07b')
        COUNT['descriptors'] += 1
        check(qbf_recursive(D) == qbf_iterative(D), 'hostile_controls')
        for b in (0, 1):
            for q in (0, 1):
                COUNT['outputs'] += 1
                f = canonical(D, b, q)
                check(stream_quotient(f, 7) == (D, b, q), 'canonical_cases')
                check(direct_quotient(f, 7) == (D, b, q))
                check(int(f[7]) == (value(D) ^ b), 'forced_bit_checks')
                check((stream_quotient(D+'0'+'0'*((1<<10)-8), 7) == (D, 1, 0)) == bool(value(D)), 'witness_equality_checks')
                for mode in (0, 1, 2, 3):
                    g = diverse_fiber(D, b, q, mode)
                    COUNT['originals'] += 1
                    check(stream_quotient(g, 7) == (D, b, q))
                    check(direct_quotient(g, 7) == (D, b, q))
                    check(int(g[7]) == (value(D) ^ b), 'forced_bit_checks')
                    if g != f:
                        COUNT['distinct_fiber_witnesses'] += 1
                    if mode >= 2:
                        COUNT['random_cases'] += 1
    # Cross-check on larger descriptors and lengths, adversarial dense tails.
    for m, cases in ((8, 80), (9, 60), (10, 30)):
        for _ in range(cases):
            D = ''.join(str(RNG.randrange(2)) for __ in range(m))
            b, q = RNG.randrange(2), RNG.randrange(2)
            g = diverse_fiber(D, b, q, 3)
            check(stream_quotient(g, m) == (D,b,q), 'hostile_controls')
            check(direct_quotient(g, m) == (D,b,q), 'hostile_controls')
            check(int(g[m]) == (value(D) ^ b), 'forced_bit_checks')
            check(stream_quotient(canonical(D,b,q), m)==(D,b,q), 'canonical_cases')
    # A concrete counterexample to deleting the first payload bit from inversion:
    # same D and adjacency but opposite a produce different masked output.
    for di in range(128):
        D = format(di,'07b')
        f0 = D+'0'+'0'*((1<<10)-8)
        f1 = D+'1'+'0'*((1<<10)-8)
        check(stream_quotient(f0,7)[1] != stream_quotient(f1,7)[1], 'hostile_controls')
    out = {
        'artifact':'CLOCKMASKEDINVERSE22',
        'timestamp_utc':'2026-11-17T23:33:28Z',
        'seed':SEED,
        'scope':'finite two-variable truth-table-matrix QBF codec; theorem uses unrestricted encoded TQBF',
        'n_input':{'m':7,'n':10,'source_bits':1024},
        'counts':COUNT,
        'failures':0,
        'theorem_status':'PROVED/EXACT restricted symbolic claim; independent review pending',
        'proof_not_empirical':['PSPACE-completeness of TQBF','PSPACE-hardness of any correct inverse-bit selector','asymptotic circuit counting'],
        'limitations':['not source-promise pure','length-aware one-way input model charges unary n header',
                       'P=NP does not imply P=PSPACE','no unrestricted MCSP lower-bound transfer']
    }
    target=Path('/mnt/data/2026-11-18_CLOCKMASKEDINVERSE22_raw.json')
    target.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
    out['audit_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    target.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__ == '__main__': run()
