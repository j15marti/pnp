#!/usr/bin/env python3
"""Independent ARC293 checker. No import from producer. Standard library only."""
from itertools import product
from collections import Counter,defaultdict
import json

C=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),
(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15),
(-1,-2,-11),(-2,-3,-11),(-1,-3,-12),(-4,-5,-13),(-5,-6,-14),
(-4,-6,-15),(-7,-8,-12),(-8,-9,-13),(-9,-10,-14),(-10,-7,-15))
def ok(a,clauses=C):
    return all(any((a[abs(x)-1]==1)==(x>0) for x in c) for c in clauses)
d=Counter(x for c in C for x in c)
assert len(C)==20 and all(d[x]==d[-x]==2 for x in range(1,16))
assert len({tuple(sorted(c)) for c in C})==20
assert all(len(set(map(abs,c)))==3 for c in C)
assert all(all(x>0 for x in c) or all(x<0 for x in c) for c in C)
models=[a for a in product((0,1),repeat=15) if ok(a)]
assert len(models)==1032
u=(-1,)*6+(0,)*4+(1,)*5
s=(-1,)*6+(0,)*4+(0,)+(1,)*4
assert sum(1 for a in models if all(p<0 or p==a[i] for i,p in enumerate(u)))==0
assert sum(1 for a in models if all(p<0 or p==a[i] for i,p in enumerate(s)))==2
w=(0,1,1,1,0,0,0,0,0,0,0,1,1,1,1)
assert ok(w) and all(p<0 or p==w[i] for i,p in enumerate(s))
def residual(p):
    out=[]
    for i,c in enumerate(C,1):
        if any(p[abs(x)-1]==int(x>0) for x in c):continue
        out.append((i,tuple(x for x in c if p[abs(x)-1]<0)))
    return out
R=residual(u)
assert len(R)==11 and all(len(c)>=2 for _,c in R)
assert [(i,c) for i,c in R if len(c)==3]==[(5,(2,3,5))]
binary=[c for _,c in R if len(c)==2]
assert len(binary)==10
bmodels=[a for a in product((0,1),repeat=6) if ok(a,binary)]
assert bmodels==[(1,0,0,1,0,0)]
cycles=((1,2,12),(3,4,15))
def verify_cycle(ids):
    e={i:tuple(map(abs,c)) for i,c in R if len(c)==2}
    edges=[e[i] for i in ids]
    assert len(edges)%2==1 and len(set(ids))==len(ids)
    degree=Counter(x for edge in edges for x in edge)
    assert len(degree)==len(edges) and all(v==2 for v in degree.values())
    graph=defaultdict(list)
    for a,b in edges:graph[a].append(b);graph[b].append(a)
    visited={edges[0][0]};stack=[edges[0][0]]
    while stack:
        q=stack.pop()
        for x in graph[q]:
            if x not in visited:visited.add(x);stack.append(x)
    assert visited==set(degree)
for cyc in cycles:verify_cycle(cyc)
assert not set(cycles[0])&set(cycles[1])
f=6;e=2*f-len(R)
assert e==1<len(cycles)
for a in models:
    assert all(p<0 or p==a[i] for i,p in enumerate(u)) is False
pair=Counter()
for i,c in enumerate(C):
    for t in C[i+1:]:
        same=any(x==y for x in c for y in t)
        opposite=any(x==-y for x in c for y in t)
        pair[''.join(map(str,(int(not opposite),int(not same),int(not same),int(not opposite))))]+=1
assert pair=={'1111':110,'1001':29,'0110':51}
# Exhaustive all 2x3^6 source subcubes. This charges full model lookup offline,
# independently confirming the gate's quantified soundness, not its online speed.
checked=stable=upconflict=0
for x11 in (0,1):
    fixed=(0,)*4+(x11,)+(1,)*4
    for p6 in product((-1,0,1),repeat=6):
        p=p6+fixed;checked+=1
        ext=[a for a in models if all(v<0 or v==a[i] for i,v in enumerate(p))]
        R=residual(p)
        # Exact count identity and defect bound on any complete satisfying extension.
        f=p.count(-1);u_count=len(R)
        if any(len(c)==0 for _,c in R):upconflict+=1;assert not ext;continue
        if any(len(c)==1 for _,c in R):continue # UP may force further pins
        stable+=1
        r3=sum(len(c)==3 for _,c in R)
        h=4*f-sum(len(c) for _,c in R)
        assert 2*(2*f-u_count)==r3+h
        for a in ext:
            h_true=sum(sum((a[abs(x)-1]==1)==(x>0) for x in c if p[abs(x)-1]<0)
                      for c in C if any(p[abs(x)-1]==int(x>0) for x in c))
            excess=sum(sum((a[abs(x)-1]==1)==(x>0) for x in c)-1 for _,c in R)
            assert 2*f-u_count==h_true+excess
            bad=sum(a[abs(c[0])-1]==a[abs(c[1])-1] for _,c in R if len(c)==2)
            assert bad<=2*f-u_count
assert checked==1458
print(json.dumps({'status':'PASS','independent':True,'source_models':1032,
  'SAT_cube_completions':2,'UNSAT_cube_completions':0,
  'binary_only_completions':1,'two_odd_cycles_valid':True,
  'partial_cubes_checked':checked,'pair_modes':dict(pair),
  'UP_stable_subcubes_checked_without_propagation':stable,
  'notes':'The full independent UP and exhaustive odd-cycle verifier is in companion reproducibility ZIP.'},indent=2))
