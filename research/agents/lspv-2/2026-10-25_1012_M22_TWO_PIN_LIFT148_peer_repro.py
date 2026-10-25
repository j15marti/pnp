#!/usr/bin/env python3
"""Independent compact reproduction of LSPV-2 M22-TWO-PIN-LIFT148.
No third-party modules. Exhaustive 75^2 six-source pairs and all two-pins.
"""
from itertools import combinations,product
import json
V=range(1,7)
triples=list(combinations(V,3))
blocks=[p for p in combinations(triples,4) if all(sum(v in e for e in p)==2 for v in V)]
assert len(blocks)==75
failP={e:sum(1<<i for i in range(64) if all(not(i>>(v-1)&1) for v in e)) for e in triples}
failQ={e:sum(1<<i for i in range(64) if all(i>>(v-1)&1 for v in e)) for e in triples}
balanced=sum(1<<i for i in range(64) if i.bit_count()==3)
allowed={(a,b,x,y):sum(1<<w for w in range(64) if (w>>(a-1)&1)==x and (w>>(b-1)&1)==y) for a,b in combinations(V,2) for x,y in product((0,1),repeat=2)}
formulas=patterns=exceptional=fully=0
minimum=999;ex=[]
for P in blocks:
 pbad=0
 for e in P:pbad|=failP[e]
 for Q in blocks:
  qbad=0
  for e in Q:qbad|=failQ[e]
  good=((1<<64)-1)&~(pbad|qbad)
  assert good
  formulas+=1;fully+=int(P==Q)
  for a,b in combinations(V,2):
   tp=sum(a in e and b in e for e in P)
   tq=sum(a in e and b in e for e in Q)
   for x,y in product((0,1),repeat=2):
    ext=good&allowed[(a,b,x,y)]
    n=ext.bit_count()
    assert n>0
    minimum=min(minimum,n)
    nbal=(ext&balanced).bit_count()
    if x!=y:assert nbal>=2
    elif nbal==0:
     assert tp==tq==2
     pext={next(v for v in e if v not in (a,b)) for e in P if a in e and b in e}
     qext={next(v for v in e if v not in (a,b)) for e in Q if a in e and b in e}
     assert len(pext)==len(qext)==2 and not (pext&qext)
     w=sum(1<<(v-1) for v in pext) +(x<<(a-1))+(x<<(b-1))
     assert ext&(1<<w)
     exceptional+=1
    patterns+=1
exampleP=((1,2,3),(1,2,4),(3,5,6),(4,5,6))
exampleQ=((1,2,5),(1,2,6),(3,4,5),(3,4,6))
for x,y in product((0,1),repeat=2):
 words=[w for w in range(64) if (w&1)==x and ((w>>1)&1)==y and all(any(w>>(v-1)&1 for v in c) for c in exampleP) and all(any(not(w>>(v-1)&1) for v in c) for c in exampleQ)]
 ex.append({'pins':f'{x}{y}','models':len(words),'balanced':sum(w.bit_count()==3 for w in words)})
assert (formulas,fully,patterns,exceptional,minimum)==(5625,75,337500,180,1)
assert [x['models'] for x in ex]==[1,10,10,1]
print(json.dumps({'formulas':formulas,'in_Cstar':formulas-fully,'fully_paired':fully,'two_pin_patterns':patterns,'zero_balanced_exceptions':exceptional,'minimum_extensions':minimum,'exception_control':ex,'failures':0},indent=2))
