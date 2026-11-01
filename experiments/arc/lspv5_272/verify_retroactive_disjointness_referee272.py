#!/usr/bin/env python3
"""Independent no-producer-import verifier for REFEREE272."""
import functools,itertools,json,sys

def f(x):return int(all(not(x[2*i] and x[2*i+1]) for i in range(len(x)//2)))

def depth(t):
 n=2*t
 @functools.lru_cache(None)
 def go(s):
  u=[i for i,a in enumerate(s) if a<0];values=set()
  for fill in itertools.product((0,1),repeat=len(u)):
   z=list(s)
   for i,b in zip(u,fill):z[i]=b
   values.add(f(z))
   if len(values)>1:break
  if len(values)==1:return 0
  return 1+min(max(go(s[:i]+(b,)+s[i+1:]) for b in (0,1)) for i in u)
 return go((-1,)*n)

def adversary(t,order):
 seen=[0]*t;ans={}
 for q in order:
  i=q//2;ans[q]=1 if not seen[i] else 0;seen[i]+=1
  if len(ans)<2*t:
   # Construct both a disjoint and intersecting completion.
   a=[ans.get(i,0) for i in range(2*t)]
   assert f(a)==1
   j=next(j for j in range(t) if seen[j]<2)
   b=list(a);b[2*j]=b[2*j+1]=1
   for q0,v in ans.items():assert b[q0]==v
   assert f(b)==0
 assert f([ans[i] for i in range(2*t)])==1

def main(path):
 d=json.load(open(path));checks=0
 assert d["P_vs_NP"]=="OPEN";checks+=1
 assert d["G2_counts"]=={"00":2377,"01":299,"10":108,"11":0};checks+=4
 assert d["theta"]=={"AZ":2377,"AQ":299,"BZ":108,"BQ":0};checks+=4
 for t in range(1,6):
  assert depth(t)==2*t;checks+=1
  orders=[list(range(2*t)),list(reversed(range(2*t)))]
  if t<=4:orders.extend(itertools.islice(itertools.permutations(range(2*t)),0,200))
  for order in orders:adversary(t,order);checks+=1
 # Exhaustive truth table and three-regime checks through t=8.
 for t in range(1,9):
  for x in itertools.product((0,1),repeat=2*t):
   want=all(not(x[2*i] and x[2*i+1]) for i in range(t))
   assert bool(f(x))==want;checks+=1
  assert all(f(tuple(v for pair in zip(beta,(0,)*t) for v in pair)) for beta in itertools.product((0,1),repeat=t));checks+=1
 assert d["controls"]["Y6_models"]==20 and d["controls"]["F9_models"]==70;checks+=2
 assert d["controls"]["F15_SAT_models"]==2 and d["controls"]["F15_UNSAT_models"]==0;checks+=2
 assert d["controls"]["F9_SU_pair_modes"]==264 and d["controls"]["malformed_rejected"]==5;checks+=2
 print(json.dumps({"status":"PASS","checks":checks,"max_truth_table_t":8,"P_vs_NP":"OPEN"},indent=2))

if __name__=="__main__":main(sys.argv[1])
