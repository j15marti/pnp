#!/usr/bin/env python3
"""Independent original-source replay of frontier tables and source-cube exclusions.
No import from experiment.py and no reliance on its SAT classifier.
"""
import json,itertools,sys,collections,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent/'raw.json'

def is_true(c,ass):return any((z>0)==bool(ass[abs(z)]) for z in c)
def vars_in(f):return sorted(set(abs(z) for c in f for z in c))
def encode(a,keys):return sum((a[k]<<j) for j,k in enumerate(keys))

def independent_replay(f,onebased,arch):
 order=[x-1 for x in onebased];m=len(order)
 prev=[set(abs(z) for t in order[:j] for z in f[t]) for j in range(m+1)]
 nextv=[set(abs(z) for t in order[j:] for z in f[t]) for j in range(m+1)]
 B=[tuple(sorted(prev[j]&nextv[j])) for j in range(m+1)]
 u=[tuple(sorted(set(B[j]) | set(abs(z) for z in f[order[j]]))) for j in range(m)]
 front=[set() for _ in range(m+1)];back=[set() for _ in range(m+1)]
 front[0].add(0);back[m].add(0);attempts=0
 for j in range(m):
  for bits in itertools.product((0,1),repeat=len(u[j])):
   a=dict(zip(u[j],bits));attempts+=1
   if encode(a,B[j]) in front[j] and is_true(f[order[j]],a):front[j+1].add(encode(a,B[j+1]))
 for j in range(m-1,-1,-1):
  for bits in itertools.product((0,1),repeat=len(u[j])):
   a=dict(zip(u[j],bits));attempts+=1
   if encode(a,B[j+1]) in back[j+1] and is_true(f[order[j]],a):back[j].add(encode(a,B[j]))
 assert [sorted(x) for x in front]==arch['left_tables']
 assert [sorted(x) for x in back]==arch['right_tables']
 pats={};supports={k:set() for k in vars_in(f)}
 for j in range(m):
  orig=order[j];vs=tuple(sorted(abs(z) for z in f[orig]));pats[orig]=set()
  for bits in itertools.product((0,1),repeat=len(u[j])):
   a=dict(zip(u[j],bits));attempts+=1
   if encode(a,B[j]) in front[j] and is_true(f[orig],a) and encode(a,B[j+1]) in back[j+1]:
    pats[orig].add(tuple(a[v] for v in vs))
    for v in vs:supports[v].add(a[v])
 assert {str(k+1):sorted(map(list,pats[k])) for k in range(m)}=={x:sorted(v) for x,v in arch['patterns'].items()}
 assert {str(k):sorted(v) for k,v in supports.items()}==arch['support']
 return attempts

def allmodels(f):
 v=vars_in(f)
 return [dict(zip(v,b)) for b in itertools.product((0,1),repeat=len(v)) if all(is_true(c,dict(zip(v,b))) for c in f)]

def unit_closure(f,ass):
 a=dict(ass)
 while True:
  changed=False
  for c in f:
   if any(abs(l) in a and a[abs(l)]==int(l>0) for l in c):continue
   q=[l for l in c if abs(l) not in a]
   if not q:return None
   if len(q)==1:
    a[abs(q[0])]=int(q[0]>0);changed=True;break
  if not changed:return a

def binary_sat(clauses):
 # Independent exhaustive 2SAT-only verifier, not the producer's SCC implementation.
 R=[tuple(c) for c in clauses if len(c)<=2];V=vars_in(R)
 if len(V)>17:raise ValueError('too many vars for independent binary truth table')
 return any(all(is_true(c,dict(zip(V,b))) for c in R) for b in itertools.product((0,1),repeat=len(V)))

def main():
 x=json.load(open(P));assert x['run']=='FRONTIER_TWO_SWEEP259';tested=0;allreplay=0
 sat_cases=unsat_cases=0
 for k,r in x['cases'].items():
  f=r['source'];v=vars_in(f);models=allmodels(f)
  assert bool(models)==r['is_SAT'] and len(models)==r['model_count'];sat_cases+=bool(models);unsat_cases+=not bool(models)
  dp=r['dp']
  if dp['status']=='done':
   allreplay+=independent_replay(f,dp['order'],dp)
   assert dp['SAT']==bool(models)
   for i,c in enumerate(f):
    keys=sorted(abs(z) for z in c);expected=sorted({tuple(a[t] for t in keys) for a in models})
    assert list(map(tuple,dp['patterns'][str(i+1)]))==expected
   tested+=1
  if r['extreme_audit']:
   ex=r['extreme_audit'];zer={u:0 for u in v};one={u:1 for u in v}
   for a,key in [(zer,'zero'),(one,'one')]:
    C=[sum(a[abs(z)]==int(z>0) for z in c) for c in f]
    assert C==ex[key]['t']
   for j,c in enumerate(f):
    z=ex['per_clause'][j]
    assert z['S_target']=={str(abs(l)):int(l>0) for l in c}
    assert z['U_target']=={str(abs(l)):int(l<0) for l in c}
   for pair,mode in ex['pair_modes'].items():
    j,t=map(lambda a:int(a)-1,pair.split('-'))
    for a in 'SU':
     for b in 'SU':
      va={abs(l):int((l>0) if a=='S' else (l<0)) for l in f[j]}
      vb={abs(l):int((l>0) if b=='S' else (l<0)) for l in f[t]}
      common=set(va)&set(vb)
      assert all(va[z]==vb[z] for z in common)==mode[a+b]
  # SAT model count is a tiny external verification oracle; no model label supplied to the controller.
 p=x['cases']['strict22_SWAP6_SAT'];f=p['source'];dp=p['dp'];extra=up=binpass=0
 examples=[]
 for j,c in enumerate(f):
  vv=sorted(abs(z) for z in c);possible={tuple(t) for t in dp['patterns'][str(j+1)]}
  for b in itertools.product((0,1),repeat=3):
   a=dict(zip(vv,b))
   if b in possible or not is_true(c,a):continue
   extra+=1
   q=unit_closure(f,a)
   if q is None:up+=1
   else:
    residual=[tuple(z for z in C if abs(z) not in q) for C in f if not any(abs(z) in q and q[abs(z)]==int(z>0) for z in C)]
    if binary_sat(residual):
     binpass+=1
     if len(examples)<5:examples.append({'source_clause':j+1,'cube':a})
 assert (extra,up,binpass)==(50,4,46)
 print(json.dumps({'independent_replay_rows':allreplay,'replayed_formulas':tested,'sat_formulas':sat_cases,'unsat_formulas':unsat_cases,'SWAP6_nontrivial_forbidden_source_cubes':extra,'UP_excluded':up,'UP_and_binary2SAT_surviving_but_unsat':binpass,'examples':examples},sort_keys=True,indent=2))
if __name__=='__main__':main()
