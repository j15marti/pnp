#!/usr/bin/env python3
"""M22-BLOCK-CUT-FACTOR139 compact independent source audit.
Standard library only. This tests explicit small blocks and their message joins,
not a polynomial general-(g,f)-factor implementation or FLMV bit-machine trace.
"""
from itertools import product
from collections import Counter
import json

def build(b):
    assert b>=1
    C=[]; nxt=b+2; modules=[]
    def add(p,n,terminals):
        start=len(C)
        for s,L in ((1,p),(-1,n)):
            for t in L:C.append(tuple(s*z for z in sorted(t)))
        modules.append((C[start:],tuple(terminals)))
    for t in (1,b+1):
        a,d,c,e=range(nxt,nxt+4);nxt+=4
        p=[(t,a,d),(a,c,e),(d,c,e)]
        add(p,p,[t])
    for i in range(1,b+1):
        x,y=i,i+1
        a,d,c,e,f=range(nxt,nxt+5);nxt+=5
        p=[(x,y,a),(a,d,c),(d,e,f),(c,e,f)]
        n=[(x,y,d),(a,d,c),(a,e,f),(c,e,f)]
        add(p,n,[x,y])
    return sorted(C),modules

def validate(C):
    cnt=Counter()
    for t in C:
        if len(t)!=3 or len(set(map(abs,t)))!=3 or not(all(x>0 for x in t) or all(x<0 for x in t)):
            return False
        for v in t:cnt[(abs(v),v>0)]+=1
    ids={abs(v) for t in C for v in t}
    return len(C)==len(set(C)) and all(cnt[x,s]==2 for x in ids for s in (0,1))

def defect(C):
    p={tuple(abs(v) for v in t) for t in C if t[0]>0}
    n={tuple(abs(v) for v in t) for t in C if t[0]<0}
    return len(p-n),len(n-p)

def sat(a,C):
    return all(any((a[abs(l)]==1)==(l>0) for l in t) for t in C)

def local_table(C,terminals):
    V=sorted({abs(v) for t in C for v in t})
    assert len(V)<=7
    T={}
    for bits in product((0,1),repeat=len(V)):
        a=dict(zip(V,bits))
        if sat(a,C):
            key=tuple(a[t] for t in terminals)
            T.setdefault(key,a)
    return T

def length_bits(C):
    k=max(abs(v) for t in C for v in t)
    def gamma(n):
        x=bin(n)[2:];return '0'*(len(x)-1)+x
    return len(gamma(k))+len(gamma(len(C)))+len(C)*(1+3*k.bit_length())

def test(b):
    C,M=build(b)
    assert validate(C)
    q=defect(C);assert q==(2*b,2*b)
    tabs=[local_table(*x) for x in M]
    assert all(len(t)==2 for t in tabs[:2])
    assert all(len(t)==4 for t in tabs[2:])
    for cl,term in M:
        pos,neg=defect(cl)
        assert pos==neg and pos in (0,2)
    # True dynamic-programming messages: cap(left) -> each segment -> cap(right).
    left=set(k[0] for k in tabs[0])
    stages=[set(left)]
    for T in tabs[2:]:
        left={y for (x,y) in T if x in left}
        stages.append(set(left))
    assert left & {t[0] for t in tabs[1]}
    # Backtrack coherent source witnesses through more than two block levels.
    value=next(iter(sorted(left & {t[0] for t in tabs[1]})))
    ass=dict(tabs[1][(value,)])
    for i in range(b-1,-1,-1):
        T=tabs[i+2]
        prev=next(x for (x,y) in sorted(T) if y==value and x in stages[i])
        for v,x in T[(prev,value)].items():
            assert v not in ass or ass[v]==x
            ass[v]=x
        value=prev
    for v,x in tabs[0][(value,)].items():
        assert v not in ass or ass[v]==x
        ass[v]=x
    assert sat(ass,C)
    k=len(ass);assert k==6*b+9 and len(C)==8*b+12
    return {'b':b,'k':k,'m':len(C),'N':length_bits(C),'q':q[0],
            'qmax':max(defect(cl)[0] for cl,_ in M),
            'blocks':len(M),'messages':len(stages),'SAT':True}

def models(C):
    k=max(abs(v) for t in C for v in t)
    return sum(sat({v:(mask>>(v-1))&1 for v in range(1,k+1)},C)
               for mask in range(1<<k))

if __name__=='__main__':
    rows=[test(b) for b in (1,2,3,6,12,24,48,96,192)]
    assert models(build(1)[0])==1960
    bad=list(build(1)[0]);bad[0]=(abs(bad[0][0]),)+bad[0][1:]
    assert not validate(bad)
    paired=[]
    for clauses,_ in build(1)[1]:
        if defect(clauses)[0]==0:paired+=clauses
    assert defect(paired)==(0,0)
    print(json.dumps({'tag':'M22-BLOCK-CUT-FACTOR139','status':'FINITE COMPUTATIONAL',
      'rows':rows,'b1_models':1960,'note':'Local truth tables verify finite joins; graph-factor and asymptotic bounds are separate mathematical proof.'},indent=2))
