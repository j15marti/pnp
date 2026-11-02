#!/usr/bin/env python3
"""LSPV-2 CROSSTAUTO320 companion 2x2 source transfer acquisition.
No third-party dependencies. Prints 81->7 exact semantic relation distribution.
"""
import itertools
from collections import Counter
P=((0,1,2),(0,3,4),(1,3,6),(2,4,5))
N=((0,1,3),(0,2,4),(1,3,5),(2,4,5))

def table(pins=(None,)*4, projected=False):
    counts=[[0,0],[0,0]]
    for ei,en in itertools.product((0,1),repeat=2):
        for x,a,b,c,d in itertools.product((0,1),repeat=5):
            if projected and x:continue
            if any(p is not None and p!=v for p,v in zip(pins,(a,b,c,d))):continue
            v=(x,a,b,c,d,ei,en)
            pp=P[2:] if projected else P
            nn=N[2:] if projected else N
            if all(any(v[q] for q in C) for C in pp) and all(any(not v[q] for q in C) for C in nn):
                counts[ei][en]+=1
    return counts

def mask(A):
    return sum(int(A[i][j]>0)<<(2*i+j) for i in (0,1) for j in (0,1))

def mul(A,B):
    return [[A[i][0]*B[0][j]+A[i][1]*B[1][j] for j in (0,1)] for i in (0,1)]

def trace(A):return A[0][0]+A[1][1]

if __name__=="__main__":
    W=table();H=table(projected=True)
    assert W==[[11,14],[8,11]] and H==[[9,12],[6,9]]
    for t,mcount,hcount in ((1,22,18),(2,466,306),(3,10054,5346)):
        M=[[1,0],[0,1]];N=[[1,0],[0,1]]
        for _ in range(t):M=mul(M,W);N=mul(N,H)
        assert trace(M)==mcount and trace(N)==hcount
    tally=Counter(mask(table(p)) for p in itertools.product((None,0,1),repeat=4))
    assert dict(tally)=={15:49,3:15,12:7,10:7,8:1,2:1,0:1}
    p3=table((None,1,None,1));p15=W;p2=table((0,1,0,1))
    assert trace(p3)>0 and trace(p15)>0
    assert trace(mul(p3,p2))==0 and trace(mul(p15,p2))==8
    print({"W":W,"projected":H,"syntactic_profiles":81,
           "relation_classes":7,"distribution":dict(tally),
           "same_original_C2_opposite_label_extensions":[0,8]})
