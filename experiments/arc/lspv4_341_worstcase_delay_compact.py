#!/usr/bin/env python3
"""Compact public check: PHP labels, resolution witnesses, and symbolic B2 inequality.
No imported SAT solver. Complete independent auditing is in the run archive.
"""
from itertools import combinations

def php(k):
    v=lambda p,h:p*k+h+1
    c=[[v(p,h) for h in range(k)] for p in range(k+1)]
    c += [[-v(i,h),-v(j,h)] for h in range(k) for i,j in combinations(range(k+1),2)]
    return k*(k+1),c

def count(n,cs):
    return sum(all(any(((a>>(abs(l)-1))&1)==(l>0) for l in c) for c in cs)
               for a in range(1<<n))

def norm(c):
    s=set(c)
    return None if any(-x in s for x in s) else tuple(sorted(s,key=lambda x:(abs(x),x<0)))

def resolution(cs):
    states=[norm(c) for c in cs]
    assert all(c is not None for c in states)
    ids={c:i for i,c in enumerate(states)}
    active=set(range(len(cs))); trace=[]
    for v in range(1,max(abs(x) for c in cs for x in c)+1):
        pos=sorted(i for i in active if v in states[i])
        neg=sorted(i for i in active if -v in states[i])
        rest={i for i in active if v not in states[i] and -v not in states[i]}
        for i in pos:
            for j in neg:
                c=norm([x for x in states[i] if x!=v]+[x for x in states[j] if x!=-v])
                if c is None: continue
                if c not in ids:
                    ids[c]=len(states);states.append(c);trace.append((i,j,v,c))
                rest.add(ids[c])
                if c==(): return trace
        active=rest
    raise AssertionError('input not refuted')

for k in (1,2,3):
    n,cs=php(k)
    neighbor=[c[:] for c in cs];neighbor[0][0]*=-1
    assert count(n,cs)==0
    positive=count(n,neighbor)
    assert positive>0
    proof=resolution(cs)
    allc=[norm(c) for c in cs]
    for i,j,v,c in proof:
        assert v in allc[i] and -v in allc[j]
        assert c==norm([x for x in allc[i] if x!=v]+[x for x in allc[j] if x!=-v])
        allc.append(c)
    assert allc[-1]==()
    byid={len(cs)+t:(i,j) for t,(i,j,v,c) in enumerate(proof)}
    used=set()
    def visit(z):
        if z<len(cs) or z in used:return
        used.add(z)
        i,j=byid[z];visit(i);visit(j)
    visit(len(cs)+len(proof)-1)
    print('PHP',k,'vars',n,'clauses',len(cs),'original models 0',
          'SAT-neighbor models',positive,'valid DAG upper bound',len(used))
for N in range(1,20):
    assert 3**N <= (2**N)**2
print('PASS: symbolic B2 single-solver inequality; not universal B2 or B3')
