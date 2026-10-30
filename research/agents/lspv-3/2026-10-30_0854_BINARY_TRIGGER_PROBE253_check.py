#!/usr/bin/env python3
"""Independent source-clause proof replay. Does not call the discovery engine."""
import json, copy, itertools, sys
from pathlib import Path
W=[(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),(5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),(-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),(2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)]
F=list(W);F[9]=(-5,6,-15);F[13]=(-3,-6,-15)

def propagate_list(a,steps):
 a=dict(a)
 for cid,lit in steps:
  assert 1<=cid<=len(F)
  residual=[]
  for z in F[cid-1]:
   if abs(z) in a:
    assert a[abs(z)]!=int(z>0)
   else:residual.append(z)
  assert residual==[lit]
  a[abs(lit)]=int(lit>0)
 return a

def conflict(a,cid):
 assert 1<=cid<=len(F)
 assert all(abs(z) in a and a[abs(z)]!=int(z>0) for z in F[cid-1])

def check(proof):
 a=propagate_list({2:0},proof['base_units'])
 for r in proof['failed']:
  lit=r['probe'];assert abs(lit) not in a and r['commit']==-lit
  b=propagate_list(a|{abs(lit):int(lit>0)},r['units']);conflict(b,r['conflict'])
  a[abs(lit)]=int(lit<0);a=propagate_list(a,r['after_units'])
 conflict(a,proof['conflict']);return a

def main():
 target={'source': [[-1, 3, -14], [2, -8, 9], [10, -13, 14], [3, 7, -13], [-4, -9, -11], [5, 8, -14], [4, -8, -11], [1, 7, 13], [1, -7, 10], [-5, 6, -15], [-2, -6, 12], [-4, 9, -10], [-2, 5, -12], [-3, -6, -15], [6, -7, 11], [2, -9, 11], [4, 8, -10], [-3, 12, 15], [-5, -12, 15], [-1, 13, 14]], 'closure': {'base_units': [], 'conflict': 19, 'failed': [{'after_units': [], 'commit': -8, 'conflict': 5, 'probe': 8, 'units': [[2, 9], [16, 11], [7, 4]]}, {'after_units': [], 'commit': -10, 'conflict': 16, 'probe': 10, 'units': [[17, 4], [12, 9], [5, -11]]}, {'after_units': [], 'commit': 5, 'conflict': 9, 'probe': -5, 'units': [[6, -14], [3, -13], [20, -1], [8, 7]]}, {'after_units': [], 'commit': 14, 'conflict': 9, 'probe': -14, 'units': [[3, -13], [20, -1], [8, 7]]}, {'after_units': [], 'commit': 3, 'conflict': 8, 'probe': -3, 'units': [[1, -1], [9, -7], [4, -13]]}, {'after_units': [[14, -15], [18, 12]], 'commit': 6, 'conflict': 18, 'probe': -6, 'units': [[10, -15], [19, -12]]}]}};assert [list(c) for c in F]==target['source']
 final=check(target['closure']);models=[]
 for mask in range(1<<15):
  if all(any(((mask>>(abs(z)-1))&1)==int(z>0) for z in c) for c in F):models.append(mask)
 assert len(models)==54 and all((m>>1)&1 for m in models)
 rejected=0
 for case in range(5):
  p=copy.deepcopy(target['closure'])
  if case==0:p['failed'][0]['commit']=8
  elif case==1:p['failed'][0]['units'][0][0]=3
  elif case==2:p['failed'][0]['units'][0][1]=-9
  elif case==3:p['failed'].pop(0)
  else:p['conflict']=1
  try:check(p)
  except (AssertionError,KeyError,TypeError):rejected+=1
 assert rejected==5
 print(json.dumps({'source_models':len(models),'all_models_have_x2_1':True,'failed_probe_steps':len(target['closure']['failed']),'source_unit_steps':sum(len(r['units'])+len(r['after_units']) for r in target['closure']['failed'])+len(target['closure']['base_units']),'corrupted_certificates_rejected':rejected,'final_assignments':final},indent=2,sort_keys=True))
if __name__=='__main__':main()
