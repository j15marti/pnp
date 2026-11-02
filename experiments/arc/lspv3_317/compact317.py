#!/usr/bin/env python3
"""GATE317 compact self-contained canonical paired-source continuation checker.
No external libraries; exhaustive only for t<=2. P versus NP OPEN.
"""
from itertools import product
BASE = ((1,2,3),(1,4,5),(2,4,6),(3,5,6))

def source(t):
    F = []
    for j in range(2*t):
        for c in BASE:
            row = tuple(6*j + x for x in c)
            if c == BASE[0]:
                row = (6*((j-1)%(2*t))+1, 6*j+2, 6*j+3)
            F.append(row)
        F.extend(tuple(-v for v in c) for c in F[-4:])
    return tuple(F)

def pins(t, word, suffix=None):
    p = {6*j+1:0 for j in range(2*t)}
    for i,mark in enumerate(word):
        p[12*i+2] = 0 if mark == 'A' else 1
        p[12*i+8] = 1 if mark == 'A' else 0
    for i in suffix or ():
        p[12*i+4] = 0
    return p

def count(F,p):
    n=max(abs(l) for c in F for l in c)
    free=[v for v in range(1,n+1) if v not in p]
    answer=0
    for bits in product((0,1),repeat=len(free)):
        a={**p,**dict(zip(free,bits))}
        answer += all(any(a[abs(l)] == (l>0) for l in c) for c in F)
    return answer

def check_source(F):
    n=max(abs(l) for c in F for l in c)
    assert len(F)*3 == 4*n
    assert len({(tuple(sorted(map(abs,c))),c[0]>0) for c in F})==len(F)
    assert all(len(c)==3 and len({abs(l) for l in c})==3 and all((l>0)==(c[0]>0) for l in c) for c in F)
    assert all(sum(v in c for c in F)==2 and sum(-v in c for c in F)==2 for v in range(1,n+1))
    supports={tuple(sorted(c)) for c in F if c[0]>0}
    assert supports=={tuple(sorted(-l for l in c)) for c in F if c[0]<0}

for t in (1,2):
    F=source(t); check_source(F)
    for w in product('AB',repeat=t):
        assert count(F,pins(t,w))==18**t
        for i in range(t):
            assert count(F,pins(t,w,(i,)))==(0 if w[i]=='A' else 9*18**(t-1))
        assert count(F,pins(t,w,range(t)))==(9**t if all(v=='B' for v in w) else 0)
    print('t',t,'n',12*t,'m',16*t,'exact_prefix_count',18**t,'continuation_classes',2**t)
print('GATE317 PASS (restricted, no universal SAT bound; P versus NP OPEN)')
