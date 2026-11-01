#!/usr/bin/env python3
"""Independent finite raw-cofactor grammar checker for ARC293.
Run alongside U_source.json and Y6_source.json from the full repro archive.
The complete UNSAT certificate, SAT witness, signed occurrence and physical
microtrace checkers are separate archived programs.
"""
import json
from pathlib import Path
from itertools import product
from collections import Counter
from random import Random

ROOT=Path(__file__).resolve().parent

def valid(clauses):
    if not clauses or any(len(c)!=3 for c in clauses):
        return False
    n=max(abs(v) for c in clauses for v in c)
    if n%3!=0 or len(clauses)*3!=4*n:
        return False
    counts=Counter()
    unique=set()
    for c in clauses:
        if not all(isinstance(v,int) and not isinstance(v,bool) and v!=0 for v in c):
            return False
        if not (all(x>0 for x in c) or all(x<0 for x in c)):
            return False
        if len({abs(x) for x in c})!=3:
            return False
        t=tuple(sorted(c))
        if t in unique: return False
        unique.add(t)
        for lit in c:
            counts[abs(lit),1 if lit>0 else -1]+=1
    return all(counts[i,sgn]==2 for i in range(1,n+1) for sgn in (-1,1))

def components(clauses):
    neighbors={}
    for c in clauses:
        vs=[abs(x) for x in c]
        for v in vs: neighbors.setdefault(v,set()).update(vs)
    unseen=set(neighbors)
    out=[]
    while unseen:
        seed=next(iter(unseen));stack=[seed];comp=set()
        while stack:
            v=stack.pop()
            if v in comp:continue
            comp.add(v);stack.extend(neighbors[v]-comp)
        out.append(comp);unseen-=comp
    return out

def cofactor(clauses,p):
    out=[]
    for c in clauses:
        if any((lit>0)==p[abs(lit)] for lit in c if abs(lit) in p):
            continue
        out.append([lit for lit in c if abs(lit) not in p])
    return out

def predicted(clauses,p):
    keep=[c for c in components(clauses) if not (c & p.keys())]
    if not keep:return False
    retained=set().union(*keep)
    return all(any((lit>0)==p[abs(lit)] for lit in cl if abs(lit) in p)
               for cl in clauses if not all(abs(lit) in retained for lit in cl))

def check_one(clauses,p):
    child=cofactor(clauses,p)
    assert bool(child and valid(child))==predicted(clauses,p),p
    return int(bool(child and valid(child)))

def test():
    y=json.loads((ROOT/'Y6_source.json').read_text())
    u=json.loads((ROOT/'U_source.json').read_text())
    v=[row[:] for row in u]
    v[1][0],v[7][0]=v[7][0],v[1][0]
    for source in [y,u,v]:
        assert valid(source)
        assert len(components(source))==1
    rng=Random(293111)
    totals={}
    for name,source in [('Y6',y),('U198',u),('V198',v)]:
        n=max(abs(x) for c in source for x in c)
        cubes=[]
        if n==6:
            for vals in product((-1,0,1),repeat=6):
                cubes.append({i+1:int(v) for i,v in enumerate(vals) if v!=-1})
        else:
            cubes=[{}]
            cubes += [{i:v} for i in range(1,n+1) for v in (0,1)]
            for _ in range(528):
                size=rng.randint(2,min(16,n))
                ks=rng.sample(range(1,n+1),size)
                cubes.append({i:rng.randrange(2) for i in ks})
        yes=sum(check_one(source,p) for p in cubes)
        assert yes==1
        totals[name]={'coherent_cubes':len(cubes),'valid_nonempty_children':yes,
                      'connected':True,'n':n,'m':len(source)}
    assert [totals[t]['coherent_cubes'] for t in ('Y6','U198','V198')]==[729,925,925]
    for core in (u,v):
        n=max(abs(x) for c in core for x in c)
        source=core+[[x+(n if x>0 else -n) for x in c] for c in y]
        assert valid(source)
        assert len(components(source))==2
        witness={n+i:b for i,b in enumerate((0,0,1,0,1,1),1)}
        assert cofactor(source,witness)==core
        assert predicted(source,witness)
    print(json.dumps({'result':'PASS','scope':'finite grammar/cofactor checks only',
                      'claims':totals,'P_vs_NP':'OPEN'},indent=2,sort_keys=True))

if __name__=='__main__':test()
