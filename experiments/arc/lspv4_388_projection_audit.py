#!/usr/bin/env python3
"""LSPV-4/388. Deterministic exact projection controls; no SAT oracle."""
import json,itertools,random,argparse,hashlib,pathlib

def valid(v):
 if not isinstance(v,dict) or set(v)!={'u','e','clauses'}:return False
 u,e=v['u'],v['e']
 if type(u)!=int or type(e)!=int or u<0 or e<0 or u+e>16 or type(v['clauses'])!=list:return False
 for c in v['clauses']:
  if type(c)!=list or not c or len(c)>max(1,u+e):return False
  if any(type(l)!=int or not 1<=abs(l)<=u+e for l in c):return False
 return True

def evaluate(cs,b):
 return all(any((b[abs(l)-1]==1)==(l>0) for l in c) for c in cs)

def projection_enum(o):
 if not valid(o):raise ValueError("invalid CNF")
 u,e=o['u'],o['e'];out=[];checks=0
 for x in itertools.product((0,1),repeat=u):
  val=0
  for y in itertools.product((0,1),repeat=e):
   checks+=1
   if evaluate(o['clauses'],x+y):val=1;break
  out.append(val)
 return out,checks

def projection_independent(o):
 if not valid(o):raise ValueError("invalid CNF")
 u,e=o['u'],o['e'];mask=0;checks=0
 for a in range(1<<(u+e)):
  b=tuple((a>>i)&1 for i in range(u+e));checks+=1
  if evaluate(o['clauses'],b):mask|=1<<sum(b[i]<<i for i in range(u))
 return [mask>>sum(x[i]<<i for i in range(u))&1 for x in itertools.product((0,1),repeat=u)],checks

def seeded(u,e,seed,m):
 rng=random.Random(seed);cs=[]
 for j in range(m):
  k=rng.randint(1,min(3,u+e));inds=rng.sample(range(1,u+e+1),k)
  cs.append([v if rng.randrange(2) else -v for v in inds])
 return dict(u=u,e=e,clauses=cs)

def guard(cs):
 return dict(u=1,e=2,clauses=[[-1]+[l+1 if l>0 else l-1 for l in c] for c in cs])

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',default='lspv4_388_results.json');args=p.parse_args()
 checks=0;invalid=0;ct=dict(cases=0,top_true=0,top_false=0,zero_true=0,zero_false=0,nontrivial_projection=0,guard_sat=0,guard_unsat=0);fixtures=[]
 lits=[1,-1,2,-2]
 base=[list(c) for k in (1,2) for c in itertools.combinations(lits,k) if len(set(map(abs,c)))==k]
 for mask in range(1<<len(base)):
  o=dict(u=1,e=1,clauses=[base[j] for j in range(len(base)) if mask>>j&1])
  v,c=projection_enum(o);w,d=projection_independent(o);assert v==w
  checks+=1+c+d;ct['cases']+=1
  ct['top_true' if all(v) else 'top_false']+=1;ct['zero_true' if not any(v) else 'zero_false']+=1
  ct['nontrivial_projection']+=(v in ([1,0],[0,1]))
 for u,e in ((1,2),(2,1),(2,2),(3,2),(2,3)):
  for seed in range(155):
   o=seeded(u,e,137+10000*u+1000*e+seed,5+seed%8)
   v,c=projection_enum(o);w,d=projection_independent(o);assert v==w
   checks+=1+c+d;ct['cases']+=1
   ct['top_true' if all(v) else 'top_false']+=1;ct['zero_true' if not any(v) else 'zero_false']+=1
   if seed in (0,29,71) and len(fixtures)<12:fixtures.append(dict(u=u,e=e,seed=seed,projected_relation=v,clauses=o['clauses']))
 for mask in range(1<<len(base)):
  H=[base[j] for j in range(len(base)) if mask>>j&1]
  h,_=projection_independent(dict(u=0,e=2,clauses=H));g,_=projection_enum(guard(H))
  assert g==([1,1] if h[0] else [1,0]);checks+=1;ct['guard_sat' if h[0] else 'guard_unsat']+=1
 for o,expect in [(dict(u=1,e=1,clauses=[[-1,2],[1,-2]]),[1,1]),(dict(u=1,e=1,clauses=[[1,2],[1,-2]]),[0,1]),(dict(u=1,e=1,clauses=[[2],[-2]]),[0,0]),(dict(u=1,e=1,clauses=[]),[1,1])]:
  assert projection_enum(o)[0]==expect;checks+=1
 bad=[{},[],dict(u=1,e=1,clauses=[[0]]),dict(u=1,e=1,clauses=[[3]]),dict(u=1,e=1,clauses=[[1.0]]),dict(u=1,e=1,clauses=[[1],[]]),dict(u=-1,e=1,clauses=[[1]]),dict(u=1,e=True,clauses=[[1]]),dict(u=1,e=1,clauses='abc'),dict(u=1,e=1,clauses=[[1]],advice='UNSAT')]
 for o in bad:
  assert not valid(o);invalid+=1;checks+=1
  try:projection_enum(o);raise AssertionError('malformed accepted')
  except ValueError:checks+=1
 result=dict(schema='LSPV4-388-1',run='2026-11-04 07:36 PST',method='two deterministic exact enumeration orders; 256 exhaustive guards',checks=checks,malformed_rejected=invalid,counts=ct,fixtures=fixtures,symbolic_results=['ProjEqTop Pi2P complete by forall-exists 3CNF','ProjEqZero coNP complete','guarded one-public-bit equivalence to NOT x iff H UNSAT','NOT a rule in fixed R_mix341'])
 raw=json.dumps(result,indent=2,sort_keys=True)+'\n'
 pathlib.Path(args.output).write_text(raw)
 print(json.dumps(dict(checks=checks,malformed_rejected=invalid,counts=ct,sha256=hashlib.sha256(raw.encode()).hexdigest()),sort_keys=True))
if __name__=='__main__':main()
