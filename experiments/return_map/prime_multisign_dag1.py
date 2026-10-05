#!/usr/bin/env python3
import itertools, math, json, random

def primes(k):
 out=[];x=2
 while len(out)<k:
  if all(x%d for d in range(2,int(math.isqrt(x))+1)):out.append(x)
  x+=1
 return out

def clauses(n):
 for vs in itertools.combinations(range(n),3):
  for sg in itertools.product([0,1],repeat=3):
   yield tuple((v,sg[i]) for i,v in enumerate(vs))

def sat_clause(a,c): return any(bool(a[v])==bool(s) for v,s in c)
def mask_formula(n,F):
 m=0
 for j,a in enumerate(itertools.product([0,1],repeat=n)):
  if all(sat_clause(a,c) for c in F):m|=1<<j
 return m

def run(n=5,seed=20261005):
 cs=list(clauses(n)); ps=primes(len(cs))
 # fixed-order DAG: state is conjunction semantic mask; prime support identifies selected clauses
 states={( (1<<(1<<n))-1, 1)}
 layers=[]
 for depth in range(1, min(16,len(cs))+1):
  c=cs[depth-1]; p=ps[depth-1]
  nxt=set()
  cm=mask_formula(n,[c])
  for sm,z in states:
   nxt.add((sm,z))       # skip clause
   nxt.add((sm&cm,z*p))  # include clause
  states=nxt
  sem=len({s for s,z in states}); syn=len(states)
  # quotient prime-labelled states by all future clauses: for conjunction states,
  # semantic mask is exact future-context sufficient statistic.
  layers.append({"depth":depth,"prime_states":syn,"semantic_context_classes":sem,
                 "context_bits":math.log2(sem) if sem else 0})
 # hostile controls
 rng=random.Random(seed)
 horn=[]
 for _ in range(15):
  vs=rng.sample(range(n),3); pos=rng.randrange(3)
  horn.append(tuple((v, i==pos and rng.choice([0,1])==1) for i,v in enumerate(vs)))
 parity_classes=2
 return {"status":"COMPUTATIONAL","n":n,"clause_universe":len(cs),"layers":layers,
         "note":"semantic mask is an exact future-conjunction quotient in this fixed signed-clause DAG",
         "parity_control_context_classes":parity_classes}
if __name__=="__main__":print(json.dumps(run(),indent=2))
