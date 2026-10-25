#!/usr/bin/env python3
"""Finite, independently rerunnable fixed-three-round M22 projection audit.

Run from the j15marti/pnp repository root:
python research/agents/lspv-2/2026-10-24_2212_M22_FIXED_DEPTH_STREAM153_peer_repro.py

This reference materializes Python lists and uses greedy pivots. It does not
implement or physically measure the separate logarithmic-space seed theorem.
Döcker U198 UNSAT is an imported published label, not brute-force verified.
"""
import ast
import itertools
import json
import math
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
P=((1,2,3),(1,4,5),(2,4,6),(3,5,6))
Q=((1,2,4),(1,3,6),(2,3,5),(4,5,6))
Y=P+tuple(tuple(-x for x in c) for c in Q)
H=P+tuple(tuple(-x for x in c) for c in P)

def clause(c):
    s=set(c)
    if any(-x in s for x in s): return None
    return tuple(sorted(s,key=lambda x:(abs(x),x<0)))

def canonical(F):
    return tuple(sorted({v for c in F if (v:=clause(c)) is not None},key=lambda c:(len(c),c)))

def names(F):
    return {abs(z) for c in F for z in c}

def m22(F):
    pp=Counter();nn=Counter();seen=set()
    for c in F:
        assert len(c)==3 and len(set(map(abs,c)))==3
        assert all(x>0 for x in c) or all(x<0 for x in c)
        assert clause(c) not in seen
        seen.add(clause(c))
        for x in c:(pp if x>0 else nn)[abs(x)]+=1
    assert all(pp[x]==nn[x]==2 for x in names(F))
    assert len(F)*3==len(names(F))*4
    plus={tuple(sorted(abs(x) for x in c)) for c in F if c[0]>0}
    minus={tuple(sorted(abs(x) for x in c)) for c in F if c[0]<0}
    return plus!=minus

def primal(F):
    G={x:set() for x in names(F)}
    for c in F:
        for x in c:
            G[abs(x)].update(abs(y) for y in c if abs(y)!=abs(x))
    return G

def pivots(G):
    chosen=[]
    for x in sorted(G):
        if not any(z in G[x] for z in chosen): chosen.append(x)
    assert all(y not in G[x] for i,x in enumerate(chosen) for y in chosen[:i])
    return tuple(chosen)

def dp(F,x):
    pp=[];nn=[];other=[]
    for c in F:
        if x in c:pp.append(tuple(t for t in c if t!=x))
        elif -x in c:nn.append(tuple(t for t in c if t!=-x))
        else:other.append(c)
    return canonical(other+[a+b for a in pp for b in nn])

def bits(F,k):
    L=max(1,math.ceil(math.log2(k+1)))
    return 2*L+sum(3+len(c)*(L+1) for c in F)

def evalcnf(F,a):
    return all(any(a[abs(z)]==(z>0) for z in c) for c in F)

def check_projection(source,dest,eliminated):
    ids=sorted(names(source))
    keep=sorted(set(ids)-set(eliminated))
    good=set()
    for values in itertools.product((False,True),repeat=len(ids)):
        a=dict(zip(ids,values))
        if evalcnf(source,a):good.add(tuple(a[x] for x in keep))
    for values in itertools.product((False,True),repeat=len(keep)):
        assert evalcnf(dest,dict(zip(keep,values)))==(values in good)
    return {'rows':2**len(keep),'sat_rows':len(good)}

def cyclic(r):
    def a(i):return 3*(i%r)+1
    def b(i):return 3*(i%r)+2
    def c(i):return 3*(i%r)+3
    out=[]
    for i in range(r):
        out.extend(((a(i),b(i),c(i)),(a(i),b(i+1),c(i+2)),
                    (-a(i),-b(i+2),-c(i+1)),(-a(i),-b(i+3),-c(i+3))))
    return tuple(out)

def run(name,F,small):
    eligible=m22(F)
    if name=='U198':assert eligible and len(names(F))==198 and len(F)==264
    k=len(names(F));G=canonical(F);removed=set();rows=[]
    for j in range(4):
        graph=primal(G)
        rec={'round':j,'active':len(graph),'clauses':len(G),
             'bits':bits(G,k),'max_width':max((len(c) for c in G),default=0),
             'max_primal_degree':max((len(x) for x in graph.values()),default=0),
             'deleted_original':len(removed)}
        if small:rec['projection']=check_projection(F,G,removed)
        rows.append(rec)
        if j<3:
            batch=pivots(graph)
            rec['pivots_next']=len(batch)
            old=names(G)
            for x in batch:G=dp(G,x)
            removed.update(batch)
            assert names(G).issubset(old-set(batch))
    return {'name':name,'C_star':eligible,'rounds':rows}

def main():
    source=ROOT/'research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt'
    raw=source.read_text()
    U=tuple(tuple(c) for c in ast.literal_eval(raw[raw.index('[['):]))
    result={'run':'M22-FIXED-DEPTH-STREAM153','model':'materialized greedy 3-round finite audit',
            'U198_UNSAT_label':'imported, not brute-forced',
            'cases':[run('Y6',Y,True),run('H6_paired_outside_star',H,True),
                     run('CYCLIC_F5',cyclic(5),True),run('U198',U,False)]}
    expected={'Y6':([6,5,4,3],[126,85,74,21]),
              'H6_paired_outside_star':([6,4,0,0],[126,82,6,6]),
              'CYCLIC_F5':([15,10,9,8],[368,468,561,380]),
              'U198':([198,156,132,119],[7936,9448,14830,39400])}
    for row in result['cases']:
        n,b=expected[row['name']]
        assert [q['active'] for q in row['rounds']]==n
        assert [q['bits'] for q in row['rounds']]==b
    print(json.dumps(result,indent=2,sort_keys=True))
    print('PASS: all four source families, every declared projection control')

if __name__=='__main__':main()
