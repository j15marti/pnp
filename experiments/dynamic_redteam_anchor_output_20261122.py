"""Packed-source guard audit; not a native Turing-machine implementation."""
from itertools import product
from collections import Counter
from fractions import Fraction
import json


def gamma(v):
    b = bin(v)[2:]
    return '0' * (len(b)-1) + b


def encode(n, rows):
    w = n.bit_length()
    return '1'*n + '0' + gamma(len(rows)+1) + ''.join(
        format(v+1, '0%db' % w) for row in rows for v in row)


def parse(text):
    if not text or any(c not in '01' for c in text):
        raise ValueError('alphabet')
    n = text.find('0')
    if n < 1:
        raise ValueError('unary header')
    p = n+1
    z = 0
    while p+z < len(text) and text[p+z] == '0':
        z += 1
    end = p+2*z+1
    if end > len(text):
        raise ValueError('gamma header')
    m = int(text[p+z:end], 2)-1
    w = n.bit_length()
    if len(text)-end != 3*m*w:
        raise ValueError('length')
    rows = []
    for a in range(end, len(text), 3*w):
        row = tuple(int(text[a+j*w:a+(j+1)*w], 2)-1 for j in range(3))
        if len(set(row)) != 3 or not all(0 <= v < n for v in row):
            raise ValueError('identifier')
        rows.append(row)
    return n, rows, end


def family(bits, i, c):
    k = len(bits)
    rows = []
    for j, bit in enumerate(bits):
        block = [(0,1,2)]*3 + [(0,3,4), (1+bit,3,4)]
        rows.extend(tuple(5*j+v for v in row) for row in block)
    u = 5*i+1+c
    a,b,d = 5*k,5*k+1,5*k+2
    return encode(5*k+3, rows+[(u,a,b),(u,b,d),(u,d,a)])


def recognize(n, rows):
    if n < 8 or (n-3) % 5 or len(rows) != n:
        return None
    k = (n-3)//5
    cache = []
    for j in range(k):
        block = [tuple(v-5*j for v in row) for row in rows[5*j:5*j+5]]
        if block[:4] != [(0,1,2)]*3+[(0,3,4)]:
            return None
        if block[4] not in ((1,3,4),(2,3,4)):
            return None
        cache.append(block[4][0]-1)
    u = rows[-3][0]
    i, local = divmod(u,5)
    a,b,d = 5*k,5*k+1,5*k+2
    if not (i < k and local in (1,2)):
        return None
    if rows[-3:] != [(u,a,b),(u,b,d),(u,d,a)]:
        return None
    return cache[i] ^ (local-1)


def exhaustive(n, rows):
    return any(all(sum((a >> v)&1 for v in row)==1 for row in rows)
               for a in range(1 << n))


def solve(text):
    try:
        n, rows, _ = parse(text)
    except ValueError:
        return 'MALFORMED', 'parser'
    answer = recognize(n, rows)
    if answer is not None:
        return ('SAT' if answer else 'UNSAT'), 'guard'
    return ('SAT' if exhaustive(n, rows) else 'UNSAT'), 'fallback'


def audit():
    counts = Counter()
    # New test: exact guard against physical single-bit source mutations.
    for x,c in product((0,1), repeat=2):
        original = family((x,),0,c)
        for p in range(len(original)):
            text = original[:p]+str(1-int(original[p]))+original[p+1:]
            try:
                n, rows, _ = parse(text)
                assert n <= 10
                expected = 'SAT' if exhaustive(n, rows) else 'UNSAT'
            except ValueError:
                expected = 'MALFORMED'
            actual, branch = solve(text)
            assert actual == expected
            counts['mutations'] += 1
            counts['mutation_'+branch] += 1
    layout = []
    for k in range(1,9):
        text = family((0,)*k,0,0)
        n,rows,h = parse(text)
        w = n.bit_length()
        p = h+15*k*w
        assert len(text) == p+9*w
        # Cache X makes H(D|X,I,C)=0. Output-at-origin still differs for
        # one member of each complementary pair, for either preset bit.
        pairs = changed = 0
        for bits in product((0,1), repeat=k):
            for i in range(k):
                for preset in (0,1):
                    changes = sum((bits[i]^c) != preset for c in (0,1))
                    assert changes == 1
                    pairs += 1
                    changed += changes
                for c in (0,1):
                    result, branch = solve(family(bits,i,c))
                    assert branch == 'guard'
                    assert (result == 'SAT') == bool(bits[i]^c)
                    counts['admitted_guard_checks'] += 1
        layout.append(dict(k=k,L=len(text),R_start=h,R_length=p-h,
                           selector_position=p,paired_cases=pairs,
                           must_change_fraction=str(Fraction(changed,2*pairs)),
                           expected_return_distance_floor=str(Fraction(p,2)),
                           expected_region_reads_floor=str(Fraction(p-h,2)),
                           conditional_decision_entropy_full_cache=0))
    return dict(status='PASS',counts=dict(counts),layouts=layout,seed=None,
                scope='Guard, malformed-input, and output-pair geometry checks; no native tape run')


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2))
