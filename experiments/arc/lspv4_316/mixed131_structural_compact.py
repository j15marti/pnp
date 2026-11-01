#!/usr/bin/env python3
"""LSPV-4 316: standalone 42-clause M and 131-clause mixed 2P2N tile structure.
Verified complete 512-case witness/UP-DPLL proofs are in conversation reproducibility ZIP.
No claims about MILP-derived UNSAT are made by this compact structural verifier.
"""
from collections import Counter
from itertools import product

M=[
(1,('x1','x2','u1')),(-1,('x2','x3','u2')),(-1,('x2','x4','u3')),
(-1,('x3','x5','x6')),(-1,('x4','x5','x6')),
(1,('x5','x7','x8')),(1,('x6','x7','x8')),
(-1,('x7','z1','z2')),(-1,('x7','z3','z4')),
(-1,('x8','z1','z2')),(-1,('x8','z3','z4')),
(1,('x3','y1','y2')),(1,('x3','y3','y4')),
(1,('x4','y5','y6')),(1,('x4','y7','y8')),
(1,('y1','y4','y7')),(1,('y2','y5','y9')),(1,('y3','y8','y9')),
(-1,('y1','y5','y8')),(-1,('y1','y6','y9')),
(-1,('y2','y3','y6')),(-1,('y2','y4','y8')),
(-1,('y3','y5','y7')),(-1,('y4','y7','y9')),
(-1,('x1','z5','z6')),(-1,('x1','z7','z8')),
(1,('x2','z7','z15')),(1,('z1','z6','z8')),
(1,('z1','z11','z12')),(1,('z2','z6','z8')),
(1,('z2','z11','z12')),(1,('z3','z5','z9')),
(1,('z3','z13','z14')),(1,('z4','z5','z14')),
(1,('z4','z9','z10')),(1,('z7','z10','z13')),
(-1,('z5','z8','z15')),(-1,('z6','z7','z9')),
(-1,('z9','z11','z13')),(-1,('z10','z11','z14')),
(-1,('z10','z12','z14')),(-1,('z12','z13','z15'))]
BRIDGE=[
(('x1',0),('x5',0),('x6',0)),
(('y6',0),('z15',0),('x1',1)),
(('x5',1),('x6',1),('y6',1)),
(('z15',1),('x1',2),('x5',2)),
(('x6',2),('y6',2),('z15',2))]
def tile():
 c=[]
 for b in range(3):
  for sign,row in M:
   c.append((sign,tuple(f'u{3*b+int(v[1:])}' if v.startswith('u') else f'{v}@{b}' for v in row)))
 c.extend((1,tuple(f'{v}@{b}' for v,b in bridge)) for bridge in BRIDGE)
 return c
C=tile()
assert len(M)==42 and len(C)==131
assert all(len(s)==3 and len(set(s))==3 for _,s in C)
assert len(set((sign,tuple(sorted(row))) for sign,row in C))==131
internal={v for _,r in C for v in r if '@' in v}
ports={v for _,r in C for v in r if '@' not in v}
assert len(internal)==96 and ports=={f'u{i}' for i in range(1,10)}
quota=Counter((v,sign) for sign,row in C for v in row)
assert all(quota[v,1]==quota[v,-1]==2 for v in internal)
assert all(quota[f'u{i}',1]==int(i%3==1) and quota[f'u{i}',-1]==int(i%3!=1) for i in range(1,10))
assert sum(sign==1 for sign,_ in C)==65 and sum(sign==-1 for sign,_ in C)==66
def source_clauses_satisfied(bits):
 return all(bits[3*b] or not bits[3*b+1] or not bits[3*b+2] for b in range(3))
count=sum(source_clauses_satisfied(bits) for bits in product((0,1),repeat=9))
assert count==343 and 512-count==169
print('PASS: 42 original M records; 131 target clauses; 96 internal 2P2N names; 343/169 source-port truth partition')
print('Finite extension equivalence and full witnesses must be checked against full raw certificate in reproducibility ZIP.')
