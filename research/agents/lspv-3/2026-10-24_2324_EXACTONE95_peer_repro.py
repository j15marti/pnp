#!/usr/bin/env python3
"""EXACTONE95 compact reproducibility: source-named 3-state equality joins.
Runs entirely in Python's standard library. No universal SAT lower bound.
"""
from collections import defaultdict
from itertools import product
import json
import random

def rel(lits, values):
    return sum((values[abs(x)-1] if x > 0 else 1-values[abs(x)-1])
               for x in lits) == 1

def source_sat(n, clauses):
    return any(all(rel(c,x) for c in clauses)
               for x in product((0,1), repeat=n))

def domain(clause):
    return [a for a in product((0,1),repeat=3)
            if sum(a[j] if clause[j]>0 else 1-a[j] for j in range(3))==1]

def make(n, source):
    copies=defaultdict(list)
    local=[]; out=[]; nid=1
    for i,c in enumerate(source):
        assert len(c)==3 and len({abs(x) for x in c})==3
        v=(nid,nid+1,nid+2);nid+=3
        local.append(v)
        for j,lit in enumerate(c): copies[abs(lit)].append((i,j))
    def padded(a,b):
        nonlocal nid
        z=nid;nid+=1
        out.extend([(a,b,z),(a,b,-z)])
    for i,c in enumerate(source):
        literals=[v if lit>0 else -v for v,lit in zip(local[i],c)]
        for bits in product((0,1),repeat=3):
            if sum(bits)%2==0:
                out.append(tuple(l if bit==0 else -l
                                 for l,bit in zip(literals,bits)))
        padded(-literals[0],-literals[1])
    links=[]
    for var,occ in sorted(copies.items()):
        for (i,j),(k,l) in zip(occ,occ[1:]):
            links.append(((i,j),(k,l)))
            a=local[i][j];b=local[k][l]
            padded(-a,b);padded(a,-b)
    L=len(links);m=len(source)
    assert nid-1==4*m+2*L
    assert len(out)==6*m+4*L
    assert all(len(c)==3 and len({abs(x) for x in c})==3 for c in out)
    assert len(set(out))==len(out)
    return dict(n=nid-1,source=source,links=links,cnf=out)

def join(D):
    rels=[domain(c) for c in D['source']]
    return any(all(choice[i][j]==choice[k][l]
                   for (i,j),(k,l) in D['links'])
               for choice in product(*rels))

def arc(D):
    m=len(D['source'])
    dom=[domain(c) for c in D['source']]
    edge=defaultdict(list)
    for (i,j),(k,l) in D['links']:
        if i<k:edge[(i,k)].append((j,l))
        else:edge[(k,i)].append((l,j))
    def consistent(i,a,k,b):
        if i>k:return all(a[y]==b[x] for x,y in edge[(k,i)])
        return all(a[x]==b[y] for x,y in edge[(i,k)])
    rounds=0
    while True:
        nxt=[]
        for i in range(m):
            N=[]
            for a in dom[i]:
                if all(any(consistent(i,a,k,b) for b in dom[k])
                       for k in range(m) if (min(i,k),max(i,k)) in edge):
                    N.append(a)
            nxt.append(N)
        if nxt==dom: break
        dom=nxt;rounds+=1
    return list(map(len,dom)),rounds

def dpll(cnf):
    clauses=[set(c) for c in cnf]
    def rec(cs):
        if any(not c for c in cs):return False
        if not cs:return True
        unit=next((next(iter(c)) for c in cs if len(c)==1),None)
        if unit is not None:
            return rec([c-{ -unit } for c in cs if unit not in c])
        lit=next(iter(min(cs,key=len)))
        return any(rec([c-{ -x } for c in cs if x not in c])
                   for x in (lit,-lit))
    return rec(clauses)

def main():
    base=[(1,2,3),(1,2,4),(1,3,4),(2,3,4)]
    cases=[base,base[:3]+[(-2,3,4)]]
    answers=[]
    prev=None
    for expect,src in zip((False,True),cases):
        C=make(4,src)
        assert (C['n'],len(C['cnf']))==(32,56)
        assert source_sat(4,src)==join(C)==dpll(C['cnf'])==expect
        assert arc(C)==([3,3,3,3],0)
        supports=[tuple(map(abs,c)) for c in C['cnf']]
        if prev is not None:assert supports==prev
        prev=supports;answers.append(int(expect))
    for mask in range(8):
        src=base[:3]+[tuple(-x if mask&(1<<j) else x
                             for j,x in enumerate((2,3,4)))]
        assert join(make(4,src))==source_sat(4,src)==(mask in (1,2,4))
    rng=random.Random(20261024)
    YES=NO=0
    for _ in range(160):
        n=rng.randint(3,7);m=rng.randint(1,5)
        source=[]
        for j in range(m):
            source.append(tuple(x if rng.getrandbits(1) else -x
                                for x in rng.sample(range(1,n+1),3)))
        truth=source_sat(n,source)
        C=make(n,source)
        assert truth==join(C)==dpll(C['cnf'])
        if truth:YES+=1
        else:NO+=1
    print(json.dumps(dict(status='COMPUTATIONAL',matched=answers,
                          seed=20261024,random_SAT=YES,random_UNSAT=NO,
                          discrepancies=0),sort_keys=True,indent=2))

if __name__=='__main__':
    main()
