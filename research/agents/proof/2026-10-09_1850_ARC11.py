"""Bounded canonical replay experiment. Run with timeout 25s python3 FILE."""
import bisect
import itertools as it
import json
import signal
from collections import Counter

signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError()))
signal.alarm(24)

def residual(c, assignment, met):
    out = set()
    satisfied = False
    for x in c:
        met['literal_reads'] += 1
        if abs(x) in assignment:
            satisfied |= assignment[abs(x)] == (x > 0)
        else:
            out.add(x)
    if satisfied or any(-x in out for x in out):
        return None
    return tuple(sorted(out))

def stream(source, assignment, capacity, met):
    assert capacity >= 1
    last = None
    while True:
        block = []
        met['passes'] += 1
        for raw in source:
            c = residual(raw, assignment, met)
            if c is None or (last is not None and c <= last):
                continue
            met['candidate_clauses'] += 1
            j = bisect.bisect_left(block, c)
            if j < len(block) and block[j] == c:
                continue
            if j < capacity:
                block.insert(j, c)
                if len(block) > capacity:
                    block.pop()
            met['peak_block_clauses'] = max(met['peak_block_clauses'], len(block))
        if not block:
            return
        for c in block:
            yield c
        last = block[-1]
        if len(block) < capacity:
            return

def equal(source, a, b, capacity, met):
    sentinel = object()
    for x,y in it.zip_longest(stream(source,a,capacity,met), stream(source,b,capacity,met), fillvalue=sentinel):
        met['stream_comparisons'] += 1
        if x != y:
            return False
    return True

def oracle(source, a):
    return tuple(sorted(set(c for row in source if (c := residual(row,a,Counter())) is not None)))

def main():
    core = tuple(it.product((-1,1),(-2,2),(-3,3)))
    checks = 0
    for mask in range(256):
        f = tuple(c for j,c in enumerate(core) if mask >> j & 1)
        # Duplicates, tautology, reversed literals and clauses.
        noisy = tuple(tuple(reversed(c)) for c in reversed(f)) + f + ((1,-1),)
        for cap in (1,2,4):
            for a in ({},{1:False},{1:True}):
                assert tuple(stream(noisy,a,cap,Counter())) == oracle(f,a)
                checks += 1
    rows = []
    for m in (8,32,128,512):
        c = tuple((i,i+1,i+2) for i in range(2,m+2))
        f = tuple((1,)+r for r in c) + tuple((-1,)+tuple(reversed(r)) for r in reversed(c))
        for cap in (1,4,16):
            met = Counter()
            assert equal(f,{1:False},{1:True},cap,met)
            assert met['peak_block_clauses'] <= cap
            rows.append(dict(m=m,capacity=cap,**met))
    # Semantically same UNSAT answer is insufficient for this syntactic merge.
    f = ((1,2),(1,-2),(-1,3),(-1,-3))
    assert not equal(f,{1:False},{1:True},2,Counter())
    # Empty clause must be emitted, not mistaken for end of stream.
    assert tuple(stream(((),),{},1,Counter())) == ((),)
    print(json.dumps(dict(status='COMPUTATIONAL',normalization_checks=checks,
        unequal_control=True,empty_clause_control=True,scaling=rows),indent=2))

if __name__ == '__main__':
    main()
