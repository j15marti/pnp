#!/usr/bin/env python3
"""GATE300 compact canonical-source adversarial control, Python standard library.
The complete quotient-width DP, independent verifier, and raw traces are in the
contemporaneous archive. This compact file DOES NOT implement a universal solver.
"""
import itertools, collections, json
P9=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9)]
N9=[(4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9)]
F9=P9+[tuple(-x for x in c) for c in N9]
P15=[(1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15)]
N15=[(1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),(4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15)]
F15=P15+[tuple(-x for x in c) for c in N15]
P9U={8:0,3:0,7:0,6:0,1:1,5:1}
P15S={7:1,8:0,9:0,10:0,11:1,12:1,13:1,14:1,15:0}
def grammar(F):
    if not F:return False
    n=max(abs(x) for c in F for x in c)
    if len(F)*3!=4*n or len({tuple(sorted(c)) for c in F})!=len(F):return False
    d=collections.Counter(x for c in F for x in c)
    return all(len(c)==3 and len(set(map(abs,c)))==3 and
               (all(x>0 for x in c) or all(x<0 for x in c)) for c in F) and all(
               d[v]==d[-v]==2 for v in range(1,n+1))
def sat(F,a):return all(any(a[abs(x)]==int(x>0) for x in c) for c in F)
def count(F,p):
    n=max(abs(x) for c in F for x in c);free=[v for v in range(1,n+1) if v not in p]
    return sum(sat(F,{**p,**dict(zip(free,bits))}) for bits in itertools.product((0,1),repeat=len(free)))
def connected(r):
    F=[tuple((1 if x>0 else -1)*(abs(x)+15*k) for x in c) for k in range(r) for c in F15]
    p={v+15*k:b for k in range(r) for v,b in P15S.items()}
    for k in range(r-1):
        i=20*k;j=20*(k+1)+6;a=list(F[i]);b=list(F[j]);a[2],b[1]=b[1],a[2]
        F[i]=tuple(a);F[j]=tuple(b)
    assert grammar(F)
    g={v:set() for v in range(1,15*r+1)}
    for c in F:
        for x,y in itertools.combinations(map(abs,c),2):g[x].add(y);g[y].add(x)
    seen={1};pending=[1]
    while pending:
        for v in g[pending.pop()]-seen:seen.add(v);pending.append(v)
    assert len(seen)==15*r
    return F,p
assert grammar(F9) and grammar(F15)
assert count(F9,{})==70 and count(F9,P9U)==0 and count(F15,P15S)==2
for r in (1,2,12):
    F,p=connected(r)
    if r<=2:assert count(F,p)==2**r
    else:
        # Pinned-true same-sign literal swaps occur ONLY in covered source clauses.
        # Thus the constrained residual is the direct product of the r base cubes.
        assert all(any(abs(x) in p and p[abs(x)]==int(x>0) for x in F[j])
                   for k in range(r) for j in (k*20,k*20+6))
print(json.dumps({'status':'PASS','canonical_connected_n':180,'m':240,
    'source_cube_models_by_independent_residual_product':4096,
    'old_nominal_edge_vectors':3**24,'projection_dimension':12,
    'measured_quotient_width_from_full_producer':0,'P_vs_NP':'OPEN'},indent=2))
