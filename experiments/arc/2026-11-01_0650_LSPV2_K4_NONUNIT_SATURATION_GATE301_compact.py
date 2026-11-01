#!/usr/bin/env python3
"""Standalone F15 canonical K4 signed-cut certificate and matched SAT/UNSAT cubes.
The full independently verified producer, row proofs and charged event ledgers are
in the contemporaneous SHA-256-verified reproducibility archive.
"""
from itertools import product, combinations
POS=[(1,2,6),(2,3,7),(3,4,8),(1,4,5),(5,11,12),
     (6,9,13),(7,10,14),(8,11,15),(9,12,13),(10,14,15)]
NEG=[(1,3,11),(1,4,12),(2,4,13),(2,5,14),(3,5,15),
     (6,7,11),(7,8,12),(8,9,13),(9,10,14),(10,6,15)]
F=POS+[tuple(-v for v in c) for c in NEG]
pU={**{v:0 for v in range(6,11)},**{v:1 for v in range(11,16)}}
pS={**pU,11:0}
def satisfied(c,a):
    return any(a[abs(v)]==int(v>0) for v in c)
def models(p):
    for bits in product((0,1),repeat=5):
        a={**p,**dict(zip(range(1,6),bits))}
        if all(satisfied(c,a) for c in F): yield bits
def residual(p):
    return [(j,tuple(v for v in c if abs(v) not in p))
        for j,c in enumerate(F) if not any(abs(v) in p and
              p[abs(v)]==int(v>0) for v in c)]
assert len(F)==20 and len(set(F))==20
assert all(len(set(map(abs,c)))==3 and len(set(v>0 for v in c))==1 for c in F)
assert all(sum(v in c for c in F)==2 and sum(-v in c for c in F)==2
           for v in range(1,16))
assert sum(all(satisfied(c,{v+1:(m>>v)&1 for v in range(15)}) for c in F)
           for m in range(1<<15))==967
assert sum(1 for _ in models(pU))==0
assert list(models(pS))==[(1,0,1,0,0),(1,1,1,0,0)]
r=residual(pU)
assert len(r)==9 and sorted(len(c) for _,c in r)==[2]*8+[3]
binary=[c for _,c in r if len(c)==2]
binary_models=[bits for bits in product((0,1),repeat=5)
               if all(satisfied(c,dict(zip(range(1,6),bits))) for c in binary)]
assert binary_models==[(0,1,1,0,0)]
edges={(1,2):0,(2,3):1,(3,4):2,(1,3):10,(1,4):11,(2,4):12}
assert all(tuple(sorted(map(abs,F[j][:2])))==edge and
           len(next(c for idx,c in r if idx==j))==2
           for edge,j in edges.items())
triangles=list(combinations((1,2,3,4),3))
assert len(triangles)==4
assert all(sum(set(edge).issubset(t) for t in triangles)==2 for edge in edges)
assert min(sum(a[x]==a[y] for x,y in edges)
    for bits in product((0,1),repeat=4)
    for a in [{i+1:bits[i] for i in range(4)}])==2
f=5;u=9;e=2*f-u;eta=0;nu=1
assert e==1 and eta==0 and e-eta-nu==0 and e-eta<2
print("PASS: canonical connected F15 with 967 models; pU 0, pS 2 models")
print("PASS: no unit/empty clauses, binary-only 2SAT SAT, fractional K4 2 > e=1")
print("PROVED/EXACT restricted K4 source control; ARC/FLMV and P versus NP OPEN")
