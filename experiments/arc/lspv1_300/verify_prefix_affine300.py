#!/usr/bin/env python3
"""Independent no-producer-import verification of prefix Gaussian certificates.
Reconstructs canonical sources, residual budgets, source-ID cycles, all affine
branch truth tables, XOR contradictions, full prefix cover, SAT/UNSAT labels.
"""
from collections import Counter
from itertools import product
from pathlib import Path
import json
D=Path(__file__).resolve().parent
F={
'Y6':((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6)),
'F9':((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9)),
'F15':((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15),
 (-1,-2,-11),(-2,-3,-11),(-1,-3,-12),(-4,-5,-13),(-5,-6,-14),(-4,-6,-15),(-7,-8,-12),(-8,-9,-13),(-9,-10,-14),(-10,-7,-15))}

def sat(form,a):return all(any(a[abs(l)]==int(l>0) for l in c) for c in form)

def exts(form,p):
 n=max(abs(x) for c in form for x in c)
 free=[v for v in range(1,n+1) if v not in p]
 for b in product((0,1),repeat=len(free)):
  a={**p,**dict(zip(free,b))};yield a

def unique_mask(a):return sum(a[v]<<(v-1) for v in a)

def rank(rows):
 basis={};r=0
 for mask,rhs,_ in rows:
  while mask:
   j=mask.bit_length()-1
   if j in basis:
    am,bb=basis[j];mask^=am;rhs^=bb
   else:basis[j]=(mask,rhs);r+=1;break
  if mask==0 and rhs:return None
 return r

def rows_from_tags(form,p,cycles,choices,prefs):
 # Entire conditional system at a chosen edge tuple, built without producer imports.
 used={j for cyc in cycles for j in cyc};u=[]
 for j,c in enumerate(form):
  if not any(abs(l) in p and p[abs(l)]==int(l>0) for l in c):u.append(j)
 rows=[]
 for j in u:
  if j in used:continue
  support=[abs(l) for l in form[j] if abs(l) not in p]
  bitmask=0
  for v in support:bitmask^=1<<(v-1)
  val=1^((len(support)&1) if form[j][0]<0 else 0)
  rows.append((bitmask,val,('parity',j)))
 for v,b in sorted(prefs.items()):rows.append((1<<(v-1),b,('preference',v)))
 for cyc,pick in zip(cycles,choices):
  for j in cyc:
   endpoints=[abs(l) for l in form[j] if abs(l) not in p]
   assert len(endpoints)==2
   if j==pick:
    val=int(form[j][0]>0)
    for v in endpoints:rows.append((1<<(v-1),val,('cycle_both_true',j,v)))
   else:
    rows.append(((1<<(endpoints[0]-1))^(1<<(endpoints[1]-1)),1,('cycle_one_true',j)))
 return rows

def gate(form,p,cycles):
 n=max(abs(x) for c in form for x in c)
 free=[v for v in range(1,n+1) if v not in p]
 covered=[];uncovered=[]
 for j,c in enumerate(form):
  (covered if any(abs(l) in p and p[abs(l)]==int(l>0) for l in c) else uncovered).append(j)
 assert not any(all(abs(l) in p for l in form[j]) for j in uncovered)
 count=Counter((abs(l),l>0) for j in covered for l in form[j] if abs(l) not in p)
 eta=sum(min(count[v,True],count[v,False]) for v in free)
 prefs={v:(0 if count[v,True]>count[v,False] else 1) for v in free if count[v,True]!=count[v,False]}
 ids=set()
 for cyc in cycles:
  assert len(cyc)%2 and len(cyc)>=3 and len(cyc)==len(set(cyc))
  deg=Counter()
  for j in cyc:
   assert j not in ids and j in uncovered
   ids.add(j)
   endpoints=[abs(l) for l in form[j] if abs(l) not in p]
   assert len(endpoints)==2
   deg.update(endpoints)
  assert len(deg)==len(cyc) and all(d==2 for d in deg.values())
 assert 2*len(free)-len(uncovered)-eta-len(cycles)==0
 return prefs

def checker():
 entries=[json.loads(s) for s in (D/'prefix_certificates300.jsonl').read_text().splitlines()]
 assert len(entries)==507
 total=Counter(); examples=[]
 for z in entries:
  form=F[z['source']];p={int(k):int(v) for k,v in z['pins'].items()}
  cycles=[tuple(c) for c in z['gate']['cycles']]
  prefs=gate(form,p,cycles)
  assert {int(k):v for k,v in z['gate']['prefs'].items()}==prefs
  branch_models={}
  free=[i for i in range(1,max(abs(x) for c in form for x in c)+1) if i not in p]
  allmodels={unique_mask(a) for a in exts(form,p) if sat(form,a)}
  for choice in product(*cycles):
   rows=rows_from_tags(form,p,cycles,choice,prefs)
   models={unique_mask(a) for a in exts(form,p) if all(((mask&unique_mask(a)).bit_count()&1)==rhs for mask,rhs,tag in rows)}
   assert all(sat(form,a) for a in exts(form,p) if unique_mask(a) in models)
   assert len(models)==(0 if rank(rows) is None else 1<<(len(free)-rank(rows)))
   assert not (models & set().union(*branch_models.values())) if branch_models else True
   branch_models[choice]=models
   total['branch_replays']+=1
  assert set().union(*branch_models.values())==allmodels
  assert len(allmodels)==z['model_count']
  assert (len(allmodels)>0)==(z['label']=='SAT')
  # Every row in an XOR proof must come from the corresponding source-indexed
  # equation system, and XOR to the impossible equation (0 = 1).
  for c in z['certificate']:
   prefix=tuple(c['choices'])
   assert all(prefix[i] in cycles[i] for i in range(len(prefix)))
   rows=rows_from_tags(form,p,cycles[:len(prefix)],prefix,prefs)
   allowed={tuple(r[:2])+(r[2],) for r in rows}
   lhs=0;rhs=0
   for row in c['row_proof']:
    tag=tuple(row['tag']);trip=(row['mask'],row['rhs'],tag)
    assert trip in allowed
    lhs^=row['mask'];rhs^=row['rhs']
   assert lhs==0 and rhs==1
   total['refutation_rows']+=len(c['row_proof'])
   total['refutation_prefixes']+=1
  if z['label']=='UNSAT_AFFINE':
   for complete in product(*cycles):
    assert any(complete[:len(c['choices'])]==tuple(c['choices']) for c in z['certificate'])
  total[z['source']+'_'+z['label']]+=1
  total['saturated_cubes']+=1
  if z['label']=='UNSAT_AFFINE' and len(examples)<4:
   examples.append({'source':z['source'],'pins':p,'cycles':cycles,'conflicts':[c['choices'] for c in z['certificate']]})
 assert total['saturated_cubes']==507
 assert total['F9_UNSAT_AFFINE']==3
 assert total['F15_UNSAT_AFFINE']==144 and total['F15_SAT']==66
 assert total['Y6_SAT']==294
 # Also independently verify that the original F9 six-pin cube does not admit a SAT completion.
 p9={8:0,3:0,7:0,6:0,1:1,5:1}
 assert sum(sat(F['F9'],a) for a in exts(F['F9'],p9))==0
 assert sum(sat(F['F9'],a) for a in exts(F['F9'],{}))==70
 out={'run':'ARC_PREFIX_AFFINE_CERT300','independent':True,'no_producer_import':True,'counts':dict(total),
      'examples':examples,'canonical_F9_global_SAT_models':70,'F9_cube_UNSAT':True,
      'P_versus_NP':'OPEN','status':'PASS'}
 (D/'independent_prefix300.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':checker()
