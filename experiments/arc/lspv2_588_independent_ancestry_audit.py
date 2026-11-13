#!/usr/bin/env python3
"""Independent source-pinned signed-RES and terminal ancestry audit for LSPV2/588.
This is a reference audit, not the original historical R_mix341 checker.
Usage: python lspv2_588_independent_ancestry_audit.py WORKDIR
"""
import os, sys, json, hashlib, subprocess
from pathlib import Path
root=Path(sys.argv[1]); p=root/'publish'/'results'/'raw'/'arc'
source=root/'SOURCE.cnf'; checker=root/'original_native386_checker.js'
sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha(checker.read_bytes())=='22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113'
assert sha(source.read_bytes())=='3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c'
cnf=[[int(x) for x in row.split()][:-1] for row in source.read_text().splitlines() if row.strip() and not row.startswith('p')]
assert len(cnf)==17 and cnf[-1]==[7]
canon=lambda c:sorted(set(c),key=lambda x:(abs(x),x))
C=[c[:-1] for c in cnf[:-1]]
def sats(clause,bits):
 return any(bool(bits&(1<<(abs(lit)-1)))==(lit>0) for lit in clause)
assert not any(all(sats(c,m) for c in C) for m in range(64))
assert all(sum(all(sats(c,m) for j,c in enumerate(C) if j!=i) for m in range(64))==2 for i in range(16))
rows=[];checks=0
for name,expected in [('DP654321',44),('DP142536',44),('DP123456',48)]:
 file=p/f'2026-11-12_2012_LSPV2_588_LIVE_PORTS_{name}.json';b=file.read_bytes();d=json.loads(b)
 assert d['spec']['guard']==7 and d['gate_defs']==[[0,8,1,4]]
 rr=d['records'];assert [r['c'] for r in rr[:17]]==cnf
 assert rr[-1]['c']==[]
 assert len(rr)==[60,60,64][['DP654321','DP142536','DP123456'].index(name)]
 for i,r in enumerate(rr):
  assert r['c']==canon(r['c'])
  assert not any(-x in r['c'] for x in r['c'])
  if r['kind']=='SOURCE': assert i<17 and r['parents']==[]
  else:
   assert r['kind']=='RES'
   assert len(r['parents'])==2 and all(0<=k<i for k in r['parents'])
   a,bb=(rr[k]['c'] for k in r['parents']);pv=r['pivot']
   assert pv in a and -pv in bb
   assert r['c']==canon([x for x in a if x!=pv]+[x for x in bb if x!=-pv]);checks+=1
  if 17<=i<=32:
   assert r['parents']==[16,i-17] and r['pivot']==7 and r['c']==C[i-17]
 live=set();stack=[len(rr)-1]
 while stack:
  i=stack.pop()
  if i not in live: live.add(i);stack+=rr[i]['parents']
 assert live==set(range(len(rr))) # every SOURCE & all distinct paid RES live
 res=sum(r['kind']=='RES' for r in rr)
 assert res+len(d['gate_defs'])==expected==d['summary']['paid_total']
 assert res==d['summary']['resolution'] and len(rr)==d['summary']['live_records']
 depth=[0]*len(rr)
 for i,r in enumerate(rr):
  if r['parents']:depth[i]=1+max(depth[k] for k in r['parents'])
 out=subprocess.run(['node',str(checker),str(file)],capture_output=True,text=True,check=True)
 native=json.loads(out.stdout)
 assert native['paid']==expected and native['negativeTests']==11
 rows.append(dict(name=name,sha256=sha(b),W=expected,sourcePorts=16,terminalLive=len(live),records=len(rr),pureDP=res-16,span=depth[-1],nativeAssertions=native['assertions']))
print(json.dumps({'independent':True,'sourceSHA256':sha(source.read_bytes()),'checkerSHA256':sha(checker.read_bytes()),'signedRESChecks':checks,'originalSourceClauseDeletionSatCount':2,'cases':rows},indent=2))
