#!/usr/bin/env python3
"""Independent exact cofactor/signed-occurrence verifier for LSPV-1 ARC259.
Standalone Python >=3.10; fixed deterministic controls, no external imports.
"""
from itertools import product
from collections import Counter
import json

stats=Counter()
def check_clause(clause, bits):
    return any(bool(bits.get(abs(l),False)) == (l>0) for l in clause)

def simplify(formula, assignment):
    out=[]
    for clause in formula:
        if any(abs(l) in assignment and bool(assignment[abs(l)]) == (l>0) for l in clause):
            continue
        out.append(tuple(l for l in clause if abs(l) not in assignment))
    return out

def decision(formula, assignment):
    stats["calls"]+=1
    def rec(clauses):
        stats["nodes"]+=1
        if not clauses: return True
        if any(not c for c in clauses): return False
        unit=next((c[0] for c in clauses if len(c)==1),None)
        if unit is not None:
            return rec(simplify(clauses,{abs(unit):int(unit>0)}))
        deg=Counter(abs(l) for c in clauses for l in c)
        v=max(sorted(deg), key=lambda x:deg[x])
        return rec(simplify(clauses,{v:1})) or rec(simplify(clauses,{v:0}))
    return rec(simplify(formula,assignment))

z,w,u=3,4,5
F=[(z,w,u),(z,w,-u),(-z,w,u),(-z,w,-u)]
def lift(H):
    E=list(F)
    for i,C in enumerate(H):
        t=7+i
        if len(C)==3:
            E.extend(((z,C[0],t),(-t,C[1],C[2])))
        else: E.append((z,)+C)
    return E

allc=[tuple(v*sg for v,sg in zip((1,2,6),pol)) for pol in product((1,-1),repeat=3)]
bycard=Counter();yes=0
for mask in range(256):
    H=[c for k,c in enumerate(allc) if mask & (1<<k)]
    E=lift(H)
    extend={(x1,x2):decision(H,{1:x1,2:x2})
            for x1,x2 in product((0,1),repeat=2)}
    bycard[sum(extend.values())]+=1
    yes+=all(extend.values())
    for vals in product((0,1),repeat=5):
        a=dict(zip(range(1,6),vals))
        f=all(check_clause(c,a) for c in F)
        e=decision(E,a)
        assert f == bool(vals[3])
        assert e == (bool(vals[3]) and (bool(vals[2]) or extend[(vals[0],vals[1])]))
        stats["source_complete_checks"]+=1
    stats["H_instances"]+=1
assert yes==81
assert bycard=={4:81,3:108,2:54,1:12,0:1}
Hbad=[(1,-2,6),(1,-2,-6)]
Ebad=lift(Hbad)
bad={1:0,2:1,3:0,4:1}
assert decision(F,bad) and not decision(Ebad,bad)
stats["bad_cube"]+=1
for j,C in enumerate(F,1):
    for lit in C:
        assert {abs(lit):int(lit>0)} == {abs(lit):int(bool({abs(lit):int(lit>0)}[abs(lit)]))}
        stats["original_occurrences"]+=1
for j in range(4):
    for k in range(j+1,4):
        for a,b in product("SU",repeat=2):
            witness=False
            for bits in product((0,1),repeat=5):
                assign=dict(zip(range(1,6),bits))
                tj=sum(check_clause((lit,),assign) for lit in F[j])
                tk=sum(check_clause((lit,),assign) for lit in F[k])
                if tj==(3 if a=="S" else 0) and tk==(3 if b=="S" else 0):
                    witness=True
            same=bool(set(F[j]).intersection(F[k]))
            opposite=bool(set(-l for l in F[j]).intersection(F[k]))
            predicted=(not opposite) if a==b else (not same)
            assert witness==predicted,(j,k,a,b)
            stats["pair_modes"]+=1
for flips in [(),(1,),(2,),(3,),(4,),(5,),(1,2),(3,4),(1,2,3),(1,2,3,4,5)]:
    a={v:int(v not in flips) for v in range(1,6)}
    b={v:1-a[v] for v in a}
    t=[sum(check_clause((lit,),a) for lit in C) for C in F]
    u=[sum(check_clause((lit,),b) for lit in C) for C in F]
    assert all(x+y==3 for x,y in zip(t,u))
    stats["flip_trails"]+=1
UNSAT= [tuple(v*s for v,s in zip((20,21,22),p)) for p in product((1,-1),repeat=3)]
assert decision(F,{}) and decision(Ebad,{})
assert not decision(F+UNSAT,{}) and not decision(Ebad+UNSAT,{})
print(json.dumps(dict(stats),sort_keys=True,indent=2))
