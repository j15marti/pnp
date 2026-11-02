#!/usr/bin/env python3
"""Exact finite F9 all-order ROBDD optimization by paid 2^n-subset DP.
Uses source truth table as an OFFLINE experimental oracle. Nothing here proves a
lower bound for arbitrary SAT algorithms, and acquisition is explicitly charged.
"""
import json
from pathlib import Path
from functools import lru_cache
from itertools import product
from producer323 import F9
ROOT=Path(__file__).resolve().parent
N=9;ALL=(1<<N)-1
costs={'source_assignment_checks':0,'source_clause_fetches':0,'source_literal_probes':0,'truth_table_bit_reads':0,'cofactor_bit_reads':0,'pair_equality_bit_probes':0,'prefix_subset_states':0,'subset_policy_edges':0}
truth=[]
for mask in range(1<<N):
 assignment={i+1:(mask>>i)&1 for i in range(N)}
 ok=True
 costs['source_assignment_checks']+=1
 for c in F9:
  costs['source_clause_fetches']+=1
  success=False
  for l in c:
   costs['source_literal_probes']+=1
   if assignment[abs(l)]==int(l>0):success=True;break
  if not success:ok=False;break
 truth.append(int(ok))
assert sum(truth)==70

@lru_cache(None)
def cofactors(prefix):
 costs['prefix_subset_states']+=1
 fixed=[i for i in range(N) if (prefix>>i)&1]
 free=[i for i in range(N) if not (prefix>>i)&1]
 unique={}
 for mask in range(1<<len(fixed)):
  source0=sum(((mask>>j)&1)<<v for j,v in enumerate(fixed))
  bits=0
  for ext in range(1<<len(free)):
   src=source0|sum(((ext>>j)&1)<<v for j,v in enumerate(free))
   costs['truth_table_bit_reads']+=1
   bits|=truth[src]<<ext
  unique[bits]=True
 return tuple(sorted(unique)),free

def source_dep(fn,width,pos):
 for i in range(1<<width):
  if (i>>pos)&1:continue
  costs['pair_equality_bit_probes']+=1
  costs['cofactor_bit_reads']+=2
  if ((fn>>i)&1)!=((fn>>(i|(1<<pos)))&1):return True
 return False

@lru_cache(None)
def edge(P,v):
 costs['subset_policy_edges']+=1
 funcs,free=cofactors(P)
 pos=free.index(v)
 return sum(source_dep(f,len(free),pos) for f in funcs)

@lru_cache(None)
def min_suffix(P):
 if P==ALL:return (0,())
 best=None
 for v in range(N):
  if P>>v&1:continue
  future,order=min_suffix(P|(1<<v))
  val=(edge(P,v)+future,(v+1,)+order)
  if best is None or val<best:best=val
 return best

@lru_cache(None)
def max_suffix(P):
 if P==ALL:return (0,())
 best=None
 for v in range(N):
  if P>>v&1:continue
  future,order=max_suffix(P|(1<<v))
  val=(edge(P,v)+future,(v+1,)+order)
  if best is None or val>best:best=val
 return best

def count_order(order):
 P=0;layers=[]
 for v in order:
  k=edge(P,v-1);layers.append(k);P|=1<<(v-1)
 assert P==ALL
 return {'nodes':sum(layers),'by_level':layers}

def main():
 low,pi=min_suffix(0);high,bad=max_suffix(0)
 natural=count_order(tuple(range(1,10)))
 reverse=count_order(tuple(range(9,0,-1)))
 best=count_order(pi);worst=count_order(bad)
 assert (low,high,natural['nodes'],reverse['nodes'])==(52,80,66,70),(low,high,natural,reverse)
 assert costs['prefix_subset_states']==511 and costs['subset_policy_edges']==2304
 output={'tag':'LSPV2_F9_EXACT_ORDER_FORWARD_REVERSE324','status':'EXACT_FINITE_COMPUTATION_NOT_UNRESTRICTED_LOWER_BOUND','models':70,'best_node_count':low,'best_order':pi,'worst_node_count':high,'worst_order':bad,'natural':natural,'reverse':reverse,'best':best,'worst':worst,'discovery_work_counts':costs,'source_oracle':'All 512 exact source-CNF input values were computed and stored OFFLINE; this is PAID acquisition, not free SAT-label oracle'}
 (ROOT/'obdd324.json').write_text(json.dumps(output,indent=2)+'\n')
 print(json.dumps(output,indent=2))
if __name__=='__main__':main()
