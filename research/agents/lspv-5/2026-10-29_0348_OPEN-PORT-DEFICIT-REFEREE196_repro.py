#!/usr/bin/env python3
"""Dependency-free exact enumeration for the five-variable open equality case."""
import itertools, json

def sat_clause(c,bits):
    return any((bits[abs(l)-1] == (l > 0)) for l in c)

def run(ext):
    n=5
    clauses=[]
    for vs in itertools.combinations(range(1,n+1),3):
        for sg in itertools.product((1,-1),repeat=3):
            clauses.append(tuple(v*s for v,s in zip(vs,sg)))
    keys=[(v,s) for v in range(1,6) for s in (1,-1)]
    ki={k:i for i,k in enumerate(keys)}
    target=[]
    for v,s in keys:
        target.append((1 if s==ext[v-1] else 2) if v<=2 else 2)
    vec=[]
    for c in clauses:
        a=[0]*10
        for l in c: a[ki[(abs(l),1 if l>0 else -1)]]+=1
        vec.append(a)
    exact_sets=0; tested=0; found=None
    chosen=[]
    def rec(start, left, rem):
        nonlocal exact_sets,tested,found
        if found is not None: return
        if left==0:
            if any(rem): return
            exact_sets+=1
            rel=set()
            for bits in itertools.product((0,1),repeat=5):
                if all(sat_clause(clauses[j],bits) for j in chosen):
                    rel.add((bits[0],bits[1]))
            tested+=32
            if rel=={(0,0),(1,1)}: found=[clauses[j] for j in chosen]
            return
        if len(clauses)-start<left or sum(rem)!=3*left: return
        if any(x>left for x in rem): return
        for j in range(start,len(clauses)-left+1):
            v=vec[j]
            if any(v[q]>rem[q] for q in range(10)): continue
            chosen.append(j)
            rec(j+1,left-1,[rem[q]-v[q] for q in range(10)])
            chosen.pop()
            if found is not None: return
    rec(0,6,target)
    return {'external_signs':ext,'exact_clause_sets':exact_sets,
            'assignment_evaluations':tested,'found':found is not None,
            'clauses':found}

out={'method':'dependency-free exact enumeration of all unique proper six-clause sets',
     'status':'COMPUTATIONAL','cases':[]}
for ext in itertools.product((1,-1),repeat=2): out['cases'].append(run(ext))
print(json.dumps(out,indent=2,sort_keys=True))
