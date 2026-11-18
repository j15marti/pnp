#!/usr/bin/env python3
"""TMR-2/086 compact standalone verifier; standard Python 3 only.
For full 170->1445 source/girth/witness audit see local executed attachments.
"""
from itertools import product, permutations
from math import prod
import json
def beat(a,b): return (b-a)%5 in (1,3)
A=[[int(beat(a,b)) for b in range(5)] for a in range(5)]
AT=list(map(list,zip(*A)))
I=[[int(a==b) for b in range(5)] for a in range(5)]
def mul(X,Y):
    return [[sum(X[a][t]*Y[t][b] for t in range(5)) for b in range(5)] for a in range(5)]
def mpow(k):
    out=I
    for _ in range(k):out=mul(out,A)
    return out
def det(M):
    s=0
    for p in permutations(range(5)):
        inversions=sum(p[i]>p[j] for i in range(5) for j in range(i+1,5))
        s+=(-1)**inversions*prod(M[i][p[i]] for i in range(5))
    return s
def count_path(word,a,b):
    k=len(word)
    if k==0:return int(a==b)
    return sum(all((beat(t[i],t[i+1]) if sign=='+' else beat(t[i+1],t[i]))
                   for i,sign in enumerate(word))
               for mid in product(range(5),repeat=k-1)
               for t in [(a,)+mid+(b,)])
assert det(A)==2
nchecks=1
for k in range(8):
    Q=mpow(k)
    for sig in product('+-',repeat=k):
        w=''.join(sig);q=w.count('-');P=I
        for c in w:P=mul(P,A if c=='+' else AT)
        for a,b in product(range(5),repeat=2):
            assert P[a][b]==Q[a][(b-q)%5]
            nchecks+=1
            if k<=4:
                assert P[a][b]==count_path(w,a,b)
                nchecks+=1
        if k<=3:
            assert min(map(min,P))==0
        if k>=4:
            assert min(map(min,P))>=1
        if k==4:
            assert det(P)==16
            assert all(sorted(row)==[1,1,4,4,6] for row in P)
        nchecks+=1
# Independent full sum over the four original labels and 5 paths' interiors.
core=((0,1),(1,2),(0,3),(1,3),(2,3))
def word(j):
    mask=(7*j+3)%16
    return ''.join('-' if mask&(1<<i) else '+' for i in range(4))
n0=n1=0
for labels in product(range(5),repeat=4):
    n0+=int(all(beat(labels[a],labels[b]) for a,b in core))
    weighted=1
    for j,(a,b) in enumerate(core):
        weighted*=count_path(word(j),labels[a],labels[b])
    n1+=weighted
    nchecks+=1
ext=prod(count_path(word(j),0,0) for j in range(5))
assert (n0,n1,ext)==(0,257280,144)
print(json.dumps({'revision':'tmr2-t5-path-saturation086-compact.v1',
                  'assertions':nchecks,'failures':0,'original_Z':n0,
                  'subdivision_Z':n1,'old_zero_extensions':ext,
                  'minimum_all_word_saturation_length':4,
                  'det_A':2,'det_path4':16,
                  'full_170_to_1445_check':'see separately executed full Python and Node.js',
                  'P_vs_NP':'OPEN'},sort_keys=True,indent=2))
