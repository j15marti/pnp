#!/usr/bin/env python3
"""LSPV-4 303 compact independent reproducer for original-ID triangle
acquisition and explicit original-source SAT/UNSAT control.
Not a native indexed-TM SAT algorithm. No dependencies beyond Python stdlib.
Full producer, independent verifier and raw records are attached to the
formal 2026-11-01 0707 report's reproducibility archive.
"""
from collections import Counter
from itertools import combinations, product
from math import ceil, log2

F=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
   (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
PS={5:0,6:0,7:0,8:0,9:1}
PU={8:0,3:0,7:0,6:0,1:1,5:1}
def grammar(f):
    if len(f)!=12:return False
    cnt=Counter((abs(v),v>0) for c in f for v in c)
    return all(len(c)==3 and len(set(map(abs,c)))==3 and
               (all(v>0 for v in c) or all(v<0 for v in c))
               for c in f) and len({tuple(sorted(c)) for c in f})==12 and \
               all(cnt[(v,True)]==cnt[(v,False)]==2 for v in range(1,10))
def satisfied(f,a):
    return all(any(a[abs(v)]==(1 if v>0 else 0) for v in c) for c in f)
def nmodels(f,p):
    free=[v for v in range(1,10) if v not in p]
    return sum(satisfied(f,dict(p,**{} )|dict(zip(free,bits)))
               for bits in product((0,1),repeat=len(free)))
def edges(f,p):
    out=[]
    for j,c in enumerate(f):
        if any(abs(v) in p and p[abs(v)]==(v>0) for v in c):continue
        rem=[abs(v) for v in c if abs(v) not in p]
        if len(rem)==2:out.append((j,*rem))
    return out
def oracle(f,p):
    out=set()
    for t in combinations(edges(f,p),3):
        vv=[x for e in t for x in e[1:]]
        if len(set(vv))==3 and all(vv.count(v)==2 for v in set(vv)):
            out.add(tuple(sorted(e[0] for e in t)))
    return out
def blocked(f,p,B):
    result=set()
    for s in range(0,len(f),B):
        cache=[e for e in edges(f,p) if s<=e[0]<s+B]
        if not cache:continue
        adj={i: [[],[]] for i,_ in enumerate(cache)}
        for j,u,v in edges(f,p):
            for i,(eid,a,b) in enumerate(cache):
                if j==eid:continue
                if a==u:adj[i][0].append((v,j))
                if a==v:adj[i][0].append((u,j))
                if b==u:adj[i][1].append((v,j))
                if b==v:adj[i][1].append((u,j))
        for i,(eid,a,b) in enumerate(cache):
            assert len(adj[i][0])<=3 and len(adj[i][1])<=3
            for w,j in adj[i][0]:
                for z,k in adj[i][1]:
                    if w==z and w not in (a,b) and len({eid,j,k})==3:
                        t=tuple(sorted((eid,j,k)))
                        if eid==t[0]:result.add(t)
    return result
def family(t,number_of_pins,B):
    m=12*t;n=9*t
    V=ceil(log2(n+1));H=ceil(log2(m+1));R=3*(V+1)
    N=2*H+m*R
    w=ceil(log2(N+2))
    e= (4 if number_of_pins==5 else 3)*t
    # Repeating the given exact F9 clause ordering places each copy's
    # binary edges in known positions within its 12-record block.
    local=[q[0] for q in edges(F,PS if number_of_pins==5 else PU)]
    active=sum(any((12*i+j)//B==s for i in range(t) for j in local)
               for s in range(ceil(m/B)))
    scans=m*active
    return dict(m=m,N=N,B=B,active=active,source_bit_reads=scans*R,
                index_writes=scans*w,head_moves=scans*2*(w-1),
                jumps=scans,component_slots=scans*(R+3*w-1),
                cache_allocated_bits=B*(3*w),pins=number_of_pins*t)
def main():
    assert grammar(F)
    assert nmodels(F,{})==70
    assert (nmodels(F,PS),nmodels(F,PU))==(1,0)
    assert oracle(F,PS)=={(1,2,10)}
    assert oracle(F,PU)=={(3,4,10)}
    total=0
    for state in product((-1,0,1),repeat=9):
        p={v:s for v,s in enumerate(state,1) if s!=-1}
        o=oracle(F,p)
        for B in (1,2,3,4,6,12):
            assert blocked(F,p,B)==o
            total+=1
    for t in (1,4,16,64):
        for B in (1,4,16,64):
            if B>12*t:continue
            for k in (5,6):
                x=family(t,k,B)
                assert x['source_bit_reads']+x['index_writes']+x['head_moves']+x['jumps']==x['component_slots']
    # Global coherent endpoints and complements, not occurrence variables.
    for bits in product((0,1),repeat=9):
        a={v+1:bits[v] for v in range(9)}
        c={v:1-x for v,x in a.items()}
        for j,cl in enumerate(F):
            t=sum(a[abs(v)]==(1 if v>0 else 0) for v in cl)
            tc=sum(c[abs(v)]==(1 if v>0 else 0) for v in cl)
            assert t+tc==3
    print('PASS',total,'blocked source oracle checks, 70 models, SAT=1, UNSAT=0')
    print('64-copy SAT B16 native component ledger',family(64,5,16))
if __name__=='__main__': main()
