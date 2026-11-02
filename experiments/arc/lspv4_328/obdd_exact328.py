#!/usr/bin/env python3
"""Independent exact reduced OBDD subset-cofactor DP for canonical A9 and F9.
Computes all-order min/max and multiplicities without free variable ordering.
Usage: python obdd_exact328.py [output.json]
Standard library only. No imports from project producers.
"""
from functools import lru_cache
import json,sys
A9=[(1,2,3),(4,5,6),(7,8,9),(1,4,7),(2,5,8),(3,6,9),(-1,-5,-9),(-2,-6,-7),(-3,-4,-8),(-1,-6,-8),(-2,-4,-9),(-3,-5,-7)]
F9=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9)]
def solve(F):
 n=9;full=(1<<n)-1
 truth=[int(all(any(((a>>(abs(v)-1))&1)==int(v>0) for v in c) for c in F)) for a in range(1<<n)]
 @lru_cache(None)
 def cof(mask,known):
  remain=[v for v in range(n) if not(mask>>v&1)];res=0
  for a in range(1<<len(remain)):
   v=known
   for j,x in enumerate(remain):v|=((a>>j)&1)<<x
   res|=truth[v]<<a
  return res
 keys={}
 for mask in range(1<<n):
  xs=[i for i in range(n) if mask>>i&1];keys[mask]=set()
  for bits in range(1<<len(xs)):
   known=sum(((bits>>j)&1)<<v for j,v in enumerate(xs))
   keys[mask].add(cof(mask,known))
 @lru_cache(None)
 def weight(mask,i):
  rem=[v for v in range(n) if not(mask>>v&1)];r=rem.index(i)
  count=0
  for f in keys[mask]:
   lo=hi=0
   for s in range(1<<(len(rem)-1)):
    p=(s&((1<<r)-1))|((s>>r)<<(r+1))
    lo|=((f>>p)&1)<<s;hi|=((f>>(p+(1<<r)))&1)<<s
   count+=int(lo!=hi)
  return count
 @lru_cache(None)
 def dp(mask):
  if mask==full:return (0,0,1,1,(),())
  choices=[]
  for i in range(n):
   if mask>>i&1:continue
   a=dp(mask|(1<<i));w=weight(mask,i)
   choices.append((w+a[0],w+a[1],a[2],a[3],(i+1,)+a[4],(i+1,)+a[5]))
  mn=min(a[0] for a in choices);mx=max(a[1] for a in choices)
  return (mn,mx,sum(a[2] for a in choices if a[0]==mn),
          sum(a[3] for a in choices if a[1]==mx),
          next(a[4] for a in choices if a[0]==mn),
          next(a[5] for a in choices if a[1]==mx))
 def count_order(order):
  s=mask=0
  for i in order:s+=weight(mask,i);mask|=1<<i
  return s
 d=dp(0)
 return dict(models=sum(truth),best_nodes=d[0],worst_nodes=d[1],
             best_order_count=d[2],worst_order_count=d[3],
             one_best_order=d[4],one_worst_order=d[5],
             natural_nodes=count_order(range(n)),orders_count=362880,
             cofactor_table_entries=cof.cache_info().currsize,
             frontier_weight_entries=weight.cache_info().currsize,
             subset_dp_entries=dp.cache_info().currsize)
if __name__=='__main__':
 data={'A9':solve(A9),'F9':solve(F9)}
 assert [data['A9'][k] for k in ('best_nodes','natural_nodes','worst_nodes')]==[42,43,50]
 assert [data['F9'][k] for k in ('best_nodes','natural_nodes','worst_nodes')]==[52,66,80]
 out=json.dumps(data,indent=2,sort_keys=True)+'\n'
 if len(sys.argv)>1:open(sys.argv[1],'w').write(out)
 print(out)