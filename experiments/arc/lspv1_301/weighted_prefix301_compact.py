#!/usr/bin/env python3
"""Compact no-dependency canonical M22 weighted ticket budget and truth controls.
Full prefix proof DAG producer and independent verifier are in reproducibility ZIP.
This script does not measure native FLMV machine time/space.
"""
from itertools import combinations,product
from collections import Counter
import json
Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
P9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
N9=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
F9=P9+tuple(tuple(-v for v in row) for row in N9)
P15=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15))
N15=((1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),(4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15))
F15=P15+tuple(tuple(-v for v in row) for row in N15)
PS=dict(zip(range(7,16),(1,0,0,0,1,1,1,1,0)))
PU=dict(zip(range(7,16),(0,0,0,0,1,1,1,1,0)))
P9PIN={8:0,3:0,7:0,6:0,1:1,5:1}
CASES=(
 ('Y6_S_d1',Y6,{5:0,6:1},1,8,6),
 ('Y6_S_d2',Y6,{4:0,6:1},2,41,6),
 ('F9_U_d0',F9,P9PIN,0,3,0),
 ('F15_S_d1',F15,{**PS,2:0,6:0},1,8,1),
 ('F15_U_d1',F15,{**PU,2:0,6:0},1,9,0))
def grammar(F):
 n=max(abs(x) for row in F for x in row)
 counts=Counter(x for row in F for x in row)
 return (3*len(F)==4*n and
  len({tuple(sorted(row)) for row in F})==len(F) and
  all(len(row)==3 and len({abs(x) for x in row})==3 and
  (all(x>0 for x in row) or all(x<0 for x in row)) for row in F) and
  all(counts[i]==counts[-i]==2 for i in range(1,n+1)))
def cl_true(row,a):
 return any(a[abs(x)]==int(x>0) for x in row)
def completions(F,p):
 n=max(abs(x) for row in F for x in row)
 free=[i for i in range(1,n+1) if i not in p]
 for bits in product((0,1),repeat=len(free)):
  yield {**p,**dict(zip(free,bits))}
def acquisition(F,p):
 n=max(abs(x) for row in F for x in row)
 free=[i for i in range(1,n+1) if i not in p]
 uncovered=[j for j,row in enumerate(F) if not any(
  abs(x) in p and p[abs(x)]==int(x>0) for x in row)]
 assert not any(all(abs(x) in p for x in F[j]) for j in uncovered)
 spill=Counter((abs(x),int(x>0)) for j,row in enumerate(F)
  if j not in uncovered for x in row if abs(x) in free)
 eta=sum(min(spill[v,0],spill[v,1]) for v in free)
 edges={}
 for j in uncovered:
  support=tuple(sorted(abs(x) for x in F[j] if abs(x) in free))
  if len(support)==2:edges.setdefault(support,[]).append(j)
 tris=[]
 for a,b,c in combinations(free,3):
  if all(edge in edges for edge in ((a,b),(a,c),(b,c))):
   tris.extend(tuple(sorted(ids)) for ids in
      product(edges[a,b],edges[a,c],edges[b,c]))
 cycles=[];used=set()
 for cy in sorted(set(tris)):
  if not used.intersection(cy):cycles.append(cy);used.update(cy)
 delta=2*len(free)-len(uncovered)-eta-len(cycles)
 polys=[]
 for cy in cycles:
  polys.append([r-1 for r in range(1,len(cy)+1,2)
               for _ in combinations(cy,r)])
 for j in uncovered:
  if j in used:continue
  width=sum(abs(x) in free for x in F[j])
  polys.append({1:[0],2:[0,1],3:[0,1,1,1,2]}[width])
 for v in free:
  w=abs(spill[v,1]-spill[v,0])
  if w:polys.append([0,w])
 return delta,cycles,polys,uncovered
def coefficient(polys,delta):
 a=[0]*(delta+1);a[0]=1
 for options in polys:
  b=[0]*(delta+1)
  for cost in options:
   for k in range(cost,delta+1):b[k]+=a[k-cost]
  a=b
 return a[delta]
def main():
 result=[]
 for name,F,p,want_d,want_B,want_models in CASES:
  assert grammar(F)
  delta,cycles,polys,uncovered=acquisition(F,p)
  B=coefficient(polys,delta)
  count=sum(all(cl_true(row,a) for row in F) for a in completions(F,p))
  assert (delta,B,count)==(want_d,want_B,want_models)
  if name=='F9_U_d0':
   cycleids={j for cy in cycles for j in cy}
   outside=[j for j in uncovered if j not in cycleids]
   assert any(all(sum(a[abs(x)]==int(x>0) for x in F[j])%2==1
        for j in outside) for a in completions(F,p))
   assert count==0  # consistent outside parity does NOT certify SAT
  result.append({'case':name,'delta':delta,
   'cycles':len(cycles),'legal_tickets':B,'true_models':count})
 assert coefficient([[0,1],[0,1]],1)==2
 assert coefficient([[0,1]],1)==1  # weighted suffix after a cost-0 prefix
 assert all(not grammar(F[:-1]) for F in (Y6,F9,F15))
 print(json.dumps({'status':'PASS','cases':result,
  'scope':'finite canonical original-source truth + budget coefficient',
  'not_claimed':'general polynomial SAT / ARC / native FLMV',
  'P_vs_NP':'OPEN'},indent=2))
if __name__=='__main__':main()
