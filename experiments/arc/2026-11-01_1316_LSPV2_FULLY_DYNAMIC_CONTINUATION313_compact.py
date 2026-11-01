#!/usr/bin/env python3
"""LSPV-2 313 compact source-level DISJ family and fully dynamic continuation check.
No all-input P-vs-NP result. Full independent checker is in reproducibility ZIP.
"""
from itertools import product
from collections import Counter

P=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
N=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
A={5:1}; B={5:1,4:0,6:0}; Z={}; Q={1:0,5:0,6:0}

def source(k):
    rows=[]
    for j in range(k):
        rows.extend(tuple(9*j+x if (i,x)!=(0,5) else 9*((j+1)%k)+5
                          for x in c) for i,c in enumerate(P))
        rows.extend(tuple(-(9*j+x) for x in c) for c in N)
    return rows

def valid(F,n):
    if n<1 or n%3 or 3*len(F)!=4*n:return False
    cnt=Counter(); seen=set()
    for C in F:
        if len(C)!=3 or len(set(map(abs,C)))!=3:return False
        if not(all(x>0 for x in C) or all(x<0 for x in C)):return False
        if min(map(abs,C))<1 or max(map(abs,C))>n:return False
        key=tuple(sorted(C))
        if key in seen:return False
        seen.add(key);cnt.update(C)
    return all(cnt[i]==2 and cnt[-i]==2 for i in range(1,n+1))

def matrix(pin):
    M=[[0,0],[0,0]]
    for a in product((0,1),repeat=9):
        if any(a[x-1]!=v for x,v in pin.items()):continue
        if not all(any(not a[x-1] for x in c) for c in N):continue
        for b in (0,1):
            if all(any(b if (i==0 and x==5) else a[x-1] for x in c)
                   for i,c in enumerate(P)):
                M[a[4]][b]+=1
    return M

def mul(X,Y):
    return [[sum(X[i][j]*Y[j][k] for j in (0,1))
             for k in (0,1)] for i in (0,1)]

def minimal_classes(t):
    states=range(1<<(2*t))
    def yes(s):
        return all(not ((s>>i)&1 and (s>>(i+t))&1) for i in range(t))
    updates=[(j,v) for j in range(2*t) for v in (0,1)]
    group=[int(yes(s)) for s in states]
    while True:
        ids={}; nextgroup=[]
        for s in states:
            sig=(yes(s), tuple(group[(s&~(1<<j))|(v<<j)]
                                for j,v in updates))
            if sig not in ids:ids[sig]=len(ids)
            nextgroup.append(ids[sig])
        if len(ids)==len(set(group)):return len(ids)
        group=nextgroup

class Dynamic:
    def __init__(self,t):
        self.b=[0]*t;self.s=[0]*t;self.c=0;self.reads=0;self.writes=0
    def set(self,which,i,v):
        A=self.b if which=="b" else self.s
        old=self.b[i]*self.s[i];self.reads+=2
        if A[i]!=v:self.writes+=1
        A[i]=v
        self.c+=self.b[i]*self.s[i]-old
        return self.c==0

if __name__=="__main__":
    mats={k:matrix(v) for k,v in (("A",A),("B",B),("Z",Z),("Q",Q))}
    assert mats=={
        "A":[[0,0],[23,36]],"B":[[0,0],[0,3]],
        "Z":[[34,47],[23,36]],"Q":[[0,13],[0,0]]}
    theta={(b,s):mul(mats["B" if b else "A"],
                     mats["Q" if s else "Z"])[1][1]
           for b in (0,1) for s in (0,1)}
    assert theta=={(0,0):2377,(0,1):299,(1,0):108,(1,1):0}
    for t in (1,2,3,4,5):
        assert valid(source(2*t),18*t)
        assert minimal_classes(t)==4**t
    for t in (1,2,4,8,32,128):
        D=Dynamic(t)
        for i in range(t):
            for which,v in (("b",1),("s",1),("b",0),("s",0)):
                got=D.set(which,i,v)
                assert got==all(theta[D.b[j],D.s[j]]>0 for j in range(t))
        assert D.reads==8*t and D.writes==4*t
    print("PASS: same canonical source; 4^t continuation classes, t<=5; O(1) word-update exact decision, t<=128; P vs NP OPEN")
