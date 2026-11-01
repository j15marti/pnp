#!/usr/bin/env python3
"""Count exact original-source SAT extensions via disjoint affine-cycle branches.
This is a producer-side model-count crosscheck, not an independent referee.
"""
from itertools import product
from collections import Counter
import json
from pathlib import Path
import saturated_cycle_affine_terminal_greedy as P

def saturated_count(F,p):
 g=P.signed_gate(F,p)
 if g['status']!='GATE' or g['delta']!=0:return None
 n=max(abs(l) for c in F for l in c)
 free=g['free'];covered_cycle={j for cycle in g['cycles'] for j in cycle}
 base=[]
 for j in g['uncovered']:
  if j not in covered_cycle:
   rest=[l for l in F[j] if abs(l) not in p]
   base.append((sum(1<<(abs(l)-1) for l in rest),1 if F[j][0]>0 else (1^(len(rest)&1)),{j}))
 for v,b in g['pref'].items():base.append((1<<(v-1),b,{1000+v}))
 count=0;rows_tested=0
 for chosen in product(*g['cycles']):
  chosen=set(chosen);rows=list(base)
  for cycle in g['cycles']:
   for j in cycle:
    r=[abs(l) for l in F[j] if abs(l) not in p]
    if j in chosen:
     for v in r:rows.append((1<<(v-1),int(F[j][0]>0),{2000+j*20+v}))
    else:rows.append(((1<<(r[0]-1))^(1<<(r[1]-1)),1,{3000+j}))
  z=P.gaussian(rows,n)
  rows_tested+=1
  if z['consistent']:count+=1<<(len(free)-z['rank'])
 return {'count':count,'systems':rows_tested,'nu':g['nu']}

def main():
 out={}
 for name,F,roots in [('Y6',P.Y6,[{}]),('F15',P.F15,[P.P_U,P.P_S])]:
  checked=0;predicted=0;brute=0;counter=Counter()
  for root in roots:
   free=[v for v in range(1,max(abs(l) for c in F for l in c)+1) if v not in root]
   for assign in product((-1,0,1),repeat=len(free)):
    p={**root,**{v:b for v,b in zip(free,assign) if b!=-1}}
    c=saturated_count(F,p)
    if c is None:continue
    actual=sum(1 for _ in P.all_models(F,p))
    assert c['count']==actual,(name,p,c,actual)
    checked+=1;predicted+=c['count'];brute+=actual
    counter['linear_systems']+=c['systems'];counter[f"nu_{c['nu']}"]+=1
  out[name]={'saturated_cubes_counted':checked,'SAT_extensions_exact':predicted,'ground_truth_extensions':brute,**dict(counter)}
 print(json.dumps(out,indent=2))
 (Path(__file__).resolve().parent / 'count_saturated_models_results.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
