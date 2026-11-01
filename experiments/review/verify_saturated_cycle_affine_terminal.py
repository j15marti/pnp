#!/usr/bin/env python3
"""No-import independent exact enumeration of saturated affine cycle decomposition.
Different code/packing enumeration from producer; tests every original assignment
and every enumerated affine branch, including same-source SAT/UNSAT controls.
"""
from itertools import combinations,product
from collections import Counter
from pathlib import Path
import json,math

YES=[(1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15)]
NO=[(1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),(4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15)]
F15=YES+[tuple(-l for l in c) for c in NO]
Y6=[(1,2,3),(1,4,5),(2,4,6),(3,5,6)]+[(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6)]
pU=dict(zip(range(7,16),(0,0,0,0,1,1,1,1,0)))
pS=dict(zip(range(7,16),(1,0,0,0,1,1,1,1,0)))

def Fsat(F,a):return all(any(a[abs(l)]==(l>0) for l in c) for c in F)

def compute(F,p):
 n=max(abs(l) for c in F for l in c)
 free=[x for x in range(1,n+1) if x not in p]
 active=[];done=[];inc=Counter()
 for i,c in enumerate(F):
  if any(abs(l) in p and p[abs(l)]==(l>0) for l in c):
   done.append(i)
   for l in c:
    if abs(l) not in p:inc[abs(l),l>0]+=1
  else:active.append(i)
 if any(all(abs(l) in p for l in F[j]) for j in active):return None
 edges=[]
 for j in active:
  rest=[abs(l) for l in F[j] if abs(l) not in p]
  if len(rest)==2:edges.append((j,*rest))
 T=[]
 for aa,bb,cc in combinations(edges,3):
  arr=(aa,bb,cc)
  degrees=Counter(x for e in arr for x in e[1:])
  if len(degrees)==3 and all(degrees[x]==2 for x in degrees):
   T.append(tuple(e[0] for e in arr))
 # Independent exhaustive search of *all* edge-disjoint triangle subcollections;
 # prefer lexicographically earliest maximum, without producer recursive code.
 best=()
 for r in range(1,len(T)+1):
  for sub in combinations(T,r):
   joined=[j for cyc in sub for j in cyc]
   if len(set(joined))==len(joined) and r>len(best):best=sub
 eta=sum(min(inc[x,True],inc[x,False]) for x in free)
 e=2*len(free)-len(active)
 D=e-eta-len(best)
 preferred={x:(0 if inc[x,True]>inc[x,False] else 1) for x in free if inc[x,True]!=inc[x,False]}
 return active,best,preferred,e,eta,D

def satisfies_branch(F,p,a,active,cycles,preferred,picks):
 if any(a[x]!=v for x,v in preferred.items()):return False
 pick=set(picks);in_cycles={j for cyc in cycles for j in cyc}
 for j in active:
  literals=[l for l in F[j] if abs(l) not in p]
  vals=[(a[abs(l)]==(l>0)) for l in literals]
  if j in pick:
   if not all(vals):return False
  elif j in in_cycles:
   if sum(vals)!=1:return False
  elif sum(vals)%2!=1:return False
 return True

def check_case(F,p):
 g=compute(F,p)
 if g is None:return 'already_empty'
 active,cycles,preferred,e,eta,D=g
 if D!=0:return 'unsaturated'
 n=max(abs(l) for c in F for l in c)
 free=[x for x in range(1,n+1) if x not in p]
 pick_list=list(product(*cycles))
 assert len(pick_list)==math.prod(map(len,cycles))
 membership=0; models=0; checks=0
 for bits in product((0,1),repeat=len(free)):
  a=dict(p);a.update(zip(free,bits))
  is_sat=Fsat(F,a)
  branch_matches=sum(satisfies_branch(F,p,a,active,cycles,preferred,choices) for choices in pick_list)
  assert is_sat==(branch_matches==1),(p,is_sat,branch_matches,D,cycles,preferred,a)
  assert branch_matches<=1
  models+=bool(is_sat); membership+=branch_matches
  checks+=len(pick_list)
 return {'status':'saturated','models':models,'cycles':len(cycles),'branches':len(pick_list),'checks':checks}

def main():
 stats=Counter();families={}
 for name,F,roots in [('Y6',Y6,[{}]),('F15',F15,[pU,pS])]:
  own=Counter();examples=[]
  for root in roots:
   fvs=[x for x in range(1,max(abs(l) for c in F for l in c)+1) if x not in root]
   for states in product((-1,0,1),repeat=len(fvs)):
    p={**root,**{x:s for x,s in zip(fvs,states) if s!=-1}}
    z=check_case(F,p)
    if isinstance(z,str):own[z]+=1
    else:
     own['saturated_checked']+=1
     own['models_total']+=z['models']
     own['branch_model_membership_checks']+=z['checks']
     own['total_branches']+=z['branches']
     if z['models']>0:own['saturated_sat_cubes']+=1
     else:own['saturated_unsat_cubes']+=1
     if z['cycles']==0:own['saturated_no_cycles']+=1
     else:own['saturated_cycles']+=1
     if len(examples)<5:examples.append({'p':p,'models':z['models'],'cycles':z['cycles'],'branches':z['branches']})
  assert sum(own[k] for k in ('already_empty','unsaturated','saturated_checked'))==len(roots)*3**len(fvs)
  families[name]={'stats':dict(own),'examples':examples}
 assert families['F15']['stats']['saturated_checked']>0
 output={'audit':'no_import_independent_complete_affine_union_by_all_assignments','families':families,'P_vs_NP':'OPEN'}
 path=Path(__file__).resolve().parent / 'verify_saturated_cycle_affine_terminal_results.json'
 path.write_text(json.dumps(output,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'families':{x:y['stats'] for x,y in families.items()},'file':str(path)},indent=2))
if __name__=='__main__':main()
