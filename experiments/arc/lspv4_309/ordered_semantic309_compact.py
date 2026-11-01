#!/usr/bin/env python3
"""LSPV-4 309 compact independent exact cyclic-source transfer control.
Standard-library Python 3, no repository dependencies or prior producer imports.
Restricted infinite family: same canonical G_(6q), opposite pinned residual labels.
"""
from itertools import product
from collections import Counter
from math import ceil, log2

POS=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
NEG=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
INTERNAL=(1,2,3,4,6,7,8,9)
PINS={'P2':{2:1,6:0,7:1,9:1},'P8':{1:0,3:0,6:0},
      'PB':{4:0,6:0},'PC':{1:0,3:0}}
S=('P2','P8','PB','P8','PC','PB')
U=('P2','P8','PC','PB','P8','PB')

def boundary(pin):
    out=[[0,0],[0,0]]
    for a,b in product(range(2),repeat=2):
        for v in product(range(2),repeat=8):
            d=dict(zip(INTERNAL,v));d[5]=a
            if any(d[k]!=value for k,value in pin.items()):continue
            posok=all(any((b if j==0 and k==5 else d[k])==1
                          for k in clause) for j,clause in enumerate(POS))
            negok=all(any(d[k]==0 for k in clause) for clause in NEG)
            if posok and negok:out[a][b]+=1
    return out

def mm(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(2))
             for j in range(2)] for i in range(2)]

def product_m(word,mats):
    A=[[1,0],[0,1]]
    for name in word:A=mm(A,mats[name])
    return A

def bigrams(word):
    return Counter((word[i],word[(i+1)%len(word)])
                   for i in range(len(word)))

def original(g):
    out=[]
    for i in range(g):
        for j,cs in enumerate(POS):
            out.append(tuple(9*((i+1)%g)+5 if j==0 and x==5
                             else 9*i+x for x in cs))
        for cs in NEG:out.append(tuple(-(9*i+x) for x in cs))
    return out

def canonical(F,n):
    if n<=0 or n%3 or len(F)*3!=4*n:return False
    tally=Counter();seen=set()
    for cs in F:
        if len(cs)!=3 or len({abs(v) for v in cs})!=3:return False
        if not(all(v>0 for v in cs) or all(v<0 for v in cs)):return False
        if any(abs(v)>n or abs(v)<1 for v in cs):return False
        key=tuple(sorted(cs))
        if key in seen:return False
        seen.add(key)
        for v in cs:tally[abs(v),v>0]+=1
    return all(tally[i,p]==2 for i in range(1,n+1) for p in (0,1))

def check():
    M={name:boundary(pin) for name,pin in PINS.items()}
    assert M=={
      'P2':[[0,2],[0,0]],'P8':[[0,0],[0,10]],
      'PB':[[3,9],[0,3]],'PC':[[0,0],[8,18]]}
    assert boundary({})==[[34,47],[23,36]]
    assert Counter(S)==Counter(U) and bigrams(S)==bigrams(U)
    assert product_m(S,M)==[[14400,75600],[0,0]]
    assert product_m(U,M)==[[0,75600],[0,0]]
    root=tuple(POS)+tuple(tuple(-z for z in c) for c in NEG)
    assert canonical(root,9)
    assert sum(all(any((bool(a&(1<<(abs(z)-1)))==(z>0))
                       for z in c) for c in root) for a in range(512))==70
    for q in (1,2,4,8,16):
        wordS=S*q;wordU=U*q
        assert canonical(original(6*q),54*q)
        assert Counter(wordS)==Counter(wordU)
        assert bigrams(wordS)==bigrams(wordU)
        A=product_m(wordS,M);B=product_m(wordU,M)
        assert A[0][0]+A[1][1]==14400**q
        assert B[0][0]+B[1][1]==0
        n=54*q;m=72*q
        gamma=lambda x:(x.bit_length()*2-1)
        source_bits=gamma(n)+gamma(m)+m*(1+3*ceil(log2(n+1)))
        print(f"q={q} n={n} m={m} source_bits={source_bits} SAT={14400**q} UNSAT=0")
    print("PASS: canonical source, exact local matrices, ordered product, 1+2-gram collision")
if __name__=='__main__':check()
