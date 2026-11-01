#!/usr/bin/env python3
"""LSPV-3 GATE309 compact source-authenticated retroactive DISJ certificate."""
from itertools import product
P=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
N=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
PRIVATE=(1,2,3,4,6,7,8,9)
def block(pins):
    M=[[0,0],[0,0]]
    for a,b in product(range(2),repeat=2):
        for vals in product(range(2),repeat=8):
            x=dict(zip(PRIVATE,vals));x[5]=a
            if any(x[k]!=v for k,v in pins.items()):continue
            if any(not any(b if j==0 and k==5 else x[k] for k in cl) for j,cl in enumerate(P)):continue
            if any(all(x[k] for k in cl) for cl in N):continue
            M[a][b]+=1
    return M
A,B,Q,Z=(block(p) for p in ({5:1},{5:1,4:0,6:0},{1:0,5:0,6:0},{}))
assert (A,B,Q,Z)==([[0,0],[23,36]],[[0,0],[0,3]],[[0,13],[0,0]],[[34,47],[23,36]])
def mul(X,Y):
    return [[sum(X[i][k]*Y[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def trace(word):
    T=[[1,0],[0,1]]
    for x in word:T=mul(T,x)
    return T[0][0]+T[1][1]
f={(0,0):2377,(0,1):299,(1,0):108,(1,1):0}
for t in range(1,8):
    words=list(product((0,1),repeat=t))
    responses=set()
    for beta in words:
        row=[]
        for sigma in words:
            M=[v for b,q in zip(beta,sigma) for v in (B if b else A,Q if q else Z)]
            exact=trace(M)
            predicted=1
            for b,q in zip(beta,sigma):predicted*=f[b,q]
            assert exact==predicted
            assert (exact>0)==(not any(b and q for b,q in zip(beta,sigma)))
            row.append(exact>0)
        responses.add(tuple(row))
    assert len(responses)==2**t
print("PASS: retroactive contexts = DISJ_t; 2^t continuation classes; 21844 checked beta/sigma pairs, t<=7")
