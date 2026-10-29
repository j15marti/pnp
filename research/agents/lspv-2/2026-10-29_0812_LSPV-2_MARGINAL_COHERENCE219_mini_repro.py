#!/usr/bin/env python3
"""LSPV-2 MARGINAL-COHERENCE219: independent compact exact source generator.
Expanded parser, native bit serialization, exhaustive full checks and raw JSON
are supplied in the downloadable MARGINAL_COHERENCE219 reproducibility package.
"""
from itertools import product
from collections import Counter
import json

def family(k, one_equal=None):
    assert k >= 1 and (one_equal is None or 1 <= one_equal <= k)
    clauses, modules, n = [], [], 0
    def fresh():
        nonlocal n
        n += 1
        return n
    def add(a,b,c):
        assert len({abs(a),abs(b),abs(c)}) == 3
        clauses.append((a,b,c))
    def pad(a,b):
        w=fresh()
        add(a,b,w); add(a,b,-w)
    def pin(v):
        u,z=fresh(),fresh()
        for s,t in product((1,-1),repeat=2):
            add(-v,s*u,t*z)
    def module_A(equal):
        a,b,c=fresh(),fresh(),fresh()
        if equal:
            pad(-a,b);pad(a,-b)
        else:
            pad(a,b);pad(-a,-b)
        pin(c)
        modules.append((a,b,c))
    a,b,c=fresh(),fresh(),fresh()
    for x in (a,b,c):pin(x)
    modules.append((a,b,c))
    for i in range(1,k+1):module_A(one_equal==i)
    for i,(_,b,c) in enumerate(modules):
        add(modules[i-1][0],b,c)
    return tuple(clauses),n

def structural(k):
    no,n=family(k)
    assert n==7*k+9 and len(no)==9*k+13
    def signatures(C):
        scopes=Counter(tuple(sorted(map(abs,c))) for c in C)
        signs=Counter((abs(x),x>0) for c in C for x in c)
        deg=Counter(abs(x) for c in C for x in c)
        assert max(deg.values()) <= 5
        adj={v:set() for v in range(1,n+1)}
        for c in C:
            for x in map(abs,c):adj[x].update(map(abs,c))
        seen={1}; todo=[1]
        while todo:
            for v in adj[todo.pop()]:
                if v not in seen:seen.add(v);todo.append(v)
        assert len(seen)==n
        return scopes,signs
    ref=signatures(no)
    for j in range(1,k+1):
        yes,n2=family(k,j)
        assert n2==n and signatures(yes)==ref
        assert sum(a!=b for C,D in zip(no,yes) for a,b in zip(C,D))==4
    return n,len(no)

def cnf(C,a):
    return all(any(a[abs(l)] == (l>0) for l in clause) for clause in C)

def exhaustive_k1():
    no,n=family(1)
    yes,_=family(1,1)
    Nyes=Nno=0
    for mask in range(1<<n):
        a=[False]+[bool((mask>>(v-1))&1) for v in range(1,n+1)]
        Nyes+=cnf(yes,a)
        Nno+=cnf(no,a)
    assert Nyes==1024 and Nno==0
    return {"truth_assignments_per_source":1<<n,"sat_witnesses":Nyes,"unsat_witnesses":Nno}

def main():
    sizes=[1,2,3,4,5,8,16,32,64]
    counts=[{"k":k,"variables":structural(k)[0],"clauses":9*k+13} for k in sizes]
    print(json.dumps({"status":"PASS","family_counts":counts,
       "k1":exhaustive_k1(),"profiles":{"E":[[0,0],[1,1]],
       "X":[[0,1],[1,0]],"B":[[0,0]]},
       "source_sign_changes":4,"max_variable_occurrences":5,
       "proof_scope":"restricted connected ordinary 3CNF, not strict exact22",
       "P_vs_NP":"OPEN"},indent=2,sort_keys=True))
if __name__=="__main__":main()
