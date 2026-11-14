#!/usr/bin/env python3
"""Independent TMR-1 audit of TMR-5/011. No peer imports, no UNSAT permutation tables.

Enumerate candidate 7-query sets, use Hall neighbor-union subsets directly,
then test each one-query deletion against Hall. Independently predict 4+3
physical-query pattern and count by first choosing 4 H rows, then 3 distinct J.
"""
import argparse
import itertools
import json
import math
import time
from datetime import datetime, timezone

FIXTURES={
 'projection':(0,0,1,1,6,6,7,7),
 'even':(0,0,3,3,5,5,6,6),
 'unbalanced':(1,2,3,4,5,6,7,7),
 'unsat':(0,1,2,3,4,5,6,7),
 'all_equal':(7,7,7,7,7,7,7,7),
 'five_equal':(7,7,7,7,7,0,0,0),
 'six_equal':(7,7,7,7,7,7,0,0),
}
POPCOUNT=[x.bit_count() for x in range(256)]
SINGLETONS={}
for mask in range(8):
 for coord in range(3):
  val=(mask>>coord)&1
  SINGLETONS[(coord,val)]=sum(1<<candidate for candidate in range(8) if ((candidate>>coord)&1)==val)

def hall_forced(row_masks, query, track=False):
 """True iff there is NO matching to all 8 masks, because some row subset violates Hall."""
 domains=[255]*8
 for pos in query:
  i,j=divmod(pos,3)
  domains[i] &= SINGLETONS[(j,(row_masks[i]>>j)&1)]
 active=[domain for domain in domains if domain !=255]
 n=len(active)
 if not n:return False
 unions=[0]*(1<<n)
 for subset in range(1,1<<n):
  b=subset & -subset
  index=b.bit_length()-1
  u=unions[subset^b] | active[index]
  unions[subset]=u
  if POPCOUNT[u]<POPCOUNT[subset]:
   return True
 return False

def shape(row_masks,query):
 if len(query)!=7 or len({p//3 for p in query})!=7:return False
 groups={}
 for p in query:
  row,j=divmod(p,3)
  k=(j,(row_masks[row]>>j)&1)
  groups[k]=groups.get(k,0)+1
 return len(groups)==2 and sorted(groups.values())==[3,4] and len({k[0] for k in groups})==2

def combinatorial_count(row_masks):
 # Enumeration of 4 distinct rows in halfcube H followed by 3 in distinct-coordinate J.
 # This is independent of the peer's intersection algebraic formula.
 answer=0
 for j in range(3):
  for b in (0,1):
   H={i for i,x in enumerate(row_masks) if (x>>j)&1==b}
   for chosen in itertools.combinations(sorted(H),4):
    for k in range(3):
     if k==j:continue
     for c in (0,1):
      J={i for i,x in enumerate(row_masks) if (x>>k)&1==c}-set(chosen)
      answer+=math.comb(len(J),3) if len(J)>=3 else 0
 return answer

def audit(name):
 a=FIXTURES[name]
 t0=time.monotonic(); count=0; ncert=0; nminimal=0; npred=0; cert_without_shape=0; shape_without_cert=0; mismatch=0; witness=None
 for q in itertools.combinations(range(24),7):
  count+=1
  pred=shape(a,q)
  npred+=pred
  forcing=hall_forced(a,q)
  ncert+=forcing
  if pred and not forcing:shape_without_cert+=1
  if forcing:
   minimal=all(not hall_forced(a,q[:z]+q[z+1:]) for z in range(7))
   if minimal and witness is None:witness=q
   nminimal+=minimal
   if minimal!=pred:
    mismatch+=1
    if mismatch<=3:print('MISMATCH',name,q,minimal,pred,flush=True)
   if minimal and not pred:cert_without_shape+=1
  elif pred:
   mismatch+=1
  if count % 100000==0:
   print('CHECKPOINT',name,count,'seconds',round(time.monotonic()-t0,3),flush=True)
 predicted=combinatorial_count(a)
 result={'case':name,'tuple':a,'checked_7_subsets':count,'hall_certificate_7':ncert,
  'hall_inclusion_minimal_7':nminimal,'predicted_shaped_sets':npred,
  'independent_combinatorial_count':predicted,'shape_without_certificate':shape_without_cert,
  'minimal_certificate_without_shape':cert_without_shape,'mismatches':mismatch,
  'first_minimal_witness':witness,'elapsed_seconds':round(time.monotonic()-t0,3),
  'verification': 'DIRECT_HALL_ROW_SUBSET_UNIONS_AND_DELETIONS',
  'valid': count==math.comb(24,7) and mismatch==0 and nminimal==npred==predicted}
 print(json.dumps(result,sort_keys=True),flush=True)
 assert result['valid']
 return result

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('case',choices=FIXTURES);args=parser.parse_args()
 audit(args.case)

# Independent exhaustive *structural* extremum check over a deterministic
# 2048-tuple pseudorandom sample, plus all 8 constant tuple maximizers.
# This does not simulate general SAT Turing machines.
def structural_sweep(samples=2048):
 state=0x51A7EED
 def nextrand():
  nonlocal state
  state ^= (state << 13) & 0xffffffff
  state ^= state >> 17
  state ^= (state << 5) & 0xffffffff
  return state & 0xffffffff
 top=[]; max_nonconstant=0; equal_count=0
 for z in range(samples):
  a=tuple(nextrand()%8 for _ in range(8))
  cnt=combinatorial_count(a)
  assert cnt<=1680
  if len(set(a))==1:
   assert cnt==1680
  else:
   assert cnt<1680
   max_nonconstant=max(max_nonconstant,cnt)
  if cnt==1680:equal_count+=1
 for val in range(8):
  a=(val,)*8
  assert combinatorial_count(a)==1680
  top.append({'mask':val,'M7':1680})
 out={'sweep_seed':'0x51A7EED','random_source_tuples':samples,
  'all_eight_constant_tuples':top,'max_nonconstant_sample':max_nonconstant,
  'random_exact_maximizers':equal_count,'failures':0,
  'status':'COMPUTATIONAL'}
 print(json.dumps(out,sort_keys=True),flush=True)
 return out
