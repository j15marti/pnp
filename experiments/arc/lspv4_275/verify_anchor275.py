#!/usr/bin/env python3
"""Independent checker for ARC-ANCHORED-INDEX275, no producer imports.
Usage: python verify_anchor275.py arc_anchor275_raw.json
Requires the complete signed-source raw JSON from the reproducibility ZIP.
No native FLMV transition claims.
"""
import json,itertools,sys,hashlib
from fractions import Fraction

raw=json.load(open(sys.argv[1]))
checks=0
def check(cond,message):
 global checks
 checks+=1
 if not cond:raise AssertionError(message)
def holds(clause,assignment):
 return any(assignment[abs(z)-1]==int(z>0) for z in clause)
def ntrue(clause,assignment):
 return sum(assignment[abs(z)-1]==int(z>0) for z in clause)
for case in raw['cases']:
 cs=case['original_clauses'];n=case['n'];m=len(cs)
 check(case['m']==m,case['name']+' m')
 check(all(len(c)==3 and len(set(abs(z) for z in c))==3 for c in cs),'proper width3')
 check(case['source_scan_chars']==case['ordinary_child_length'],'scan')
 models=sum(1 for bits in itertools.product((0,1),repeat=n) if all(holds(c,bits) for c in cs))
 check(models==case['models'],case['name']+' models')
 check((models>0)==(case['label']=='SAT'),case['name']+' label')
 for endpoint,key in (([0]*n,'0^n'),([1]*n,'1^n')):
  check(case['endpoints'][key]==[sum(ntrue(c,endpoint)==j for c in cs) for j in range(4)],'endpoint')
 for obj in case['occurrence_targets']:
  j=obj['clause'];c=obj['literals']
  check(c==cs[j-1],'original clause ID')
  for o,z in zip(obj['occurrences'],c):
   check(o['i']==abs(z) and o['j']==j and o['literal']==z,'occ source')
   check((o['S'],o['invS'],o['U'],o['invU']) == (int(z>0),int(z<0),int(z<0),int(z>0)),'S/U')
 for obj in case['pair_compatibility']:
  i,j=obj['source_pair'];c=cs[i-1];d=cs[j-1];vv=sorted(set(abs(z) for z in c+d))
  for k,mode in enumerate(['SS','SU','US','UU']):
   target=(mode[0]=='S',mode[1]=='S')
   feasible=False
   for bits in itertools.product((0,1),repeat=len(vv)):
    assign=dict(zip(vv,bits))
    tc=[assign[abs(z)]==int(z>0) for z in c]
    td=[assign[abs(z)]==int(z>0) for z in d]
    if all(q==target[0] for q in tc) and all(q==target[1] for q in td):
     feasible=True;break
   check(feasible==bool(obj['SS_SU_US_UU'][k]),'pair '+str((i,j,mode)))
 for r in case['resolution_forbidden_cubes']:
  i,j=r['parents'];lset=set(cs[i-1]);rset=set(cs[j-1]);p=r['pivot']
  check((p in lset and -p in rset) or (-p in lset and p in rset),'pivot')
  px=p if p in lset else -p
  res=set((lset-{px})|(rset-{-px}))
  check(set(r['resolvent'])==res and not any(-z in res for z in res),'resolvent')
  cube={int(k):v for k,v in r['forbidden_cube'].items()}
  check(cube=={abs(z):int(z<0) for z in res},'cube')
  var=sorted(set(abs(z) for z in cs[i-1]+cs[j-1]))
  for bits in itertools.product((0,1),repeat=len(var)):
   asgn=dict(zip(var,bits))
   if all(asgn[q]==v for q,v in cube.items()):
    check(not(any(asgn[abs(z)]==int(z>0) for z in cs[i-1]) and any(asgn[abs(z)]==int(z>0) for z in cs[j-1])),'cube sound')
 for seq in case['complement_flip_trails']:
  for t in seq['steps']:
   a=t['mask'];v=[ntrue(c,a) for c in cs]
   check(t['hist']==[v.count(z) for z in range(4)],'flip hist')
   check(t['sat']==all(z>0 for z in v),'flip sat')
   inv=[1-x for x in a];v2=[ntrue(c,inv) for c in cs]
   check([v.count(z) for z in range(4)]==[v2.count(z) for z in range(3,-1,-1)],'complement')
 check(case['guest_DPLL_nodes']==case['baseline']['nodes'],'nodes')
 check(case['host']['events']>1000 and case['host']['input_reads']>=10,'traces')
 check(case['host']['h_high_water']==256,'index high-water')
 check(case['host']['boundary_oscillation_naive_bit_flips']>=512*2*256,'binary carry')
for e in raw['flmv']:
 c=Fraction(e['c']);u=Fraction(1);best=None;k=0;at=None
 while True:
  k+=1;u=c*u/(1+u);v=min(((1/u)-c)/k,c**(-k))
  if best is None or v>best:best=v;at=k
  if c**(-k-1)<best:break
  check(k<100,'FLMV termination')
 check(str(best)==e['d'] and at==e['max_index'],'FLMV exact')
 check(c**(-k-1)<best,'tail certified')
check(raw['summary']['all_correct'],'status')
print(json.dumps({'run':'ANCHOR275_INDEPENDENT','checks':checks,'cases':len(raw['cases']),'pass':True,
 'sha256':hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest()},indent=2))
