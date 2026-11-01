#!/usr/bin/env python3
"""LSPV-2 305 independently runnable restricted F9 cyclic-transfer controls.
Complete controller, no-import verifier and native-like events are archived separately.
No all-input SAT or complexity separation claim. Standard Python library only.
"""
from itertools import product
POS=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
NEG=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
CLAUSES=tuple((1,c) for c in POS)+tuple((-1,c) for c in NEG)
PA=(1,0,1,0,None,None,None,0,None)
PB=(1,1,0,0,None,None,None,0,None)
def local(pin):
    counts=[[0,0],[0,0]]
    free=[x for x in range(1,10) if x!=5 and pin[x-1] is None]
    for a,b in product((0,1),repeat=2):
        for values in product((0,1),repeat=len(free)):
            d={x:pin[x-1] for x in range(1,10) if pin[x-1] is not None}
            d.update(zip(free,values))
            d[5]=a
            if all(any((b if j==0 and x==5 else d[x])==(sg==1)
                       for x in triple) for j,(sg,triple) in enumerate(CLAUSES)):
                counts[a][b]+=1
    return counts
def mul(A,B):
    return [[sum(A[i][k]*B[k][j] for k in (0,1))
             for j in (0,1)] for i in (0,1)]
def power(W,t):
    out=[[1,0],[0,1]]
    while t:
        if t&1:out=mul(out,W)
        t//=2
        if t:W=mul(W,W)
    return out
def count(W,t):
    M=power(W,t)
    return M[0][0]+M[1][1]
W=local((None,)*9)
WA=local(PA)
WB=local(PB)
assert W==[[34,47],[23,36]]
assert WA==[[1,1],[0,0]]
assert WB==[[0,0],[0,0]]
assert [count(W,t) for t in range(1,5)]==[70,4614,312970,21248098]
assert all(count(WA,t)==1 and count(mul(WB,power(WA,t-1)),1)==0
           for t in (1,2,4,128))
print('PASS: restricted exact transfer and both-label coherent original-source pins')
print('W=',W,'WA=',WA,'WB=',WB)
print('counts t=1..4:',[count(W,t) for t in range(1,5)])
print('P versus NP OPEN')
