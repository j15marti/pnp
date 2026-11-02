#!/usr/bin/env python3
"""Independent checker; does not import the LSPV-1 producer."""
from itertools import product
plus=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
minus=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
g=((1,2,3),(1,4,5),(2,4,6),(3,5,6))
source=plus+tuple(tuple(-z for z in row) for row in minus)
gadget=g+tuple(tuple(-z for z in row) for row in g)
clauses=source+tuple(tuple((abs(z)+9)*(1 if z>0 else -1) for z in row) for row in gadget)
assert len(clauses)==20
for i in range(1,16):
 assert sum(i in row for row in clauses)==2
 assert sum(-i in row for row in clauses)==2
def true(v,row):
 return any(v[abs(z)-1] == int(z>0) for z in row)
def sat(C,v):
 return all(true(v,row) for row in C)
models=[v for v in product((0,1),repeat=15) if sat(clauses,v)]
assert len(models)==1260
profiles={
 'root':({},(630,630)),
 'SAT':({1:0,3:0,5:1,6:0,7:0,8:0},(18,18)),
 'UNSAT':({1:1,3:0,5:1,6:0,7:0,8:0},(0,0)),
 'P':({1:1,2:0,3:0},(72,72)),
 'Q':({1:1,2:1,3:0},(72,72)),
 'P+x6':({1:1,2:0,3:0,6:1},(0,0)),
 'Q+x6':({1:1,2:1,3:0,6:1},(18,18))}
for name,(pins,want) in profiles.items():
 got=tuple(sum(v[9]==b and all(v[i-1]==p for i,p in pins.items()) for v in models) for b in (0,1))
 assert got==want,(name,got)
pins=profiles['UNSAT'][0];free=[i for i in range(1,10) if i not in pins]
for values in product((0,1),repeat=3):
 data={**pins,**dict(zip(free,values))}
 v=tuple(data[i] for i in range(1,10))
 assert any(not true(v,row) for row in source)
pairs=0
for i in range(20):
 for j in range(i+1,20):
  for a,b in product((0,1),repeat=2):
   r=clauses[i];s=clauses[j]
   demand={};conflict=False
   for row,t in ((r,a),(s,b)):
    for z in row:
     key=abs(z);need=int(z>0)==t
     if key in demand and demand[key]!=need:conflict=True
     demand[key]=need
   keys=sorted({abs(z) for z in r+s})
   actual=any(sum(vals[keys.index(abs(z))]==int(z>0) for z in r)==3*a and
              sum(vals[keys.index(abs(z))]==int(z>0) for z in s)==3*b
              for vals in product((0,1),repeat=len(keys)))
   assert actual != conflict
   pairs+=1
print('PASS independent: 1260 models, seven boundary profiles, eight UNSAT original leaves,',pairs,'S/U pair modes')
