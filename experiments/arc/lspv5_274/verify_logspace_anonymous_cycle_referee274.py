#!/usr/bin/env python3
"""No-producer-import verifier for REFEREE274 raw invariants."""
import argparse,itertools,json
from pathlib import Path
P=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
Q=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
def family(t):
 F=[]
 for i in range(t):
  f=lambda x:9*i+x
  F.append((f(1),f(6),9*((i+1)%t)+5));F.extend(tuple(f(x) for x in c) for c in P[1:]);F.extend(tuple(-f(x) for x in c) for c in Q)
 return 9*t,F
def valid(n,F):
 from collections import Counter
 q=Counter();seen=set()
 if 3*len(F)!=4*n:return False
 for c in F:
  if len(c)!=3 or len({abs(x) for x in c})!=3 or not(all(x>0 for x in c) or all(x<0 for x in c)):return False
  k=tuple(sorted(c))
  if k in seen:return False
  seen.add(k);q.update(c)
 return all(q[v]==q[-v]==2 for v in range(1,n+1))
def local(pins):
 M=[[0,0],[0,0]]
 for a,b in itertools.product((0,1),repeat=2):
  for z in itertools.product((0,1),repeat=8):
   v={5:a};v.update(zip((1,2,3,4,6,7,8,9),z))
   if any(v[x]!=y for x,y in pins.items()):continue
   if all(any(v[x] for x in c) for c in P[1:]) and all(any(not v[x] for x in c) for c in Q) and (v[1] or v[6] or b):M[a][b]=1;break
 return M
def bm(A,B):return [[int(any(A[i][k] and B[k][j] for k in (0,1))) for j in (0,1)] for i in (0,1)]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--raw',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();r=json.loads(Path(a.raw).read_text())
 assert r['run']=='LOGSPACE_ANONYMOUS_CYCLE_REFEREE274' and r['P_vs_NP']=='OPEN';checks=0
 A=local({1:1,2:0,3:1,4:0,8:0});B=local({1:1,2:1,3:0,4:0,8:0});assert A==[[1,1],[0,0]] and B==[[0,0],[0,0]];checks+=2
 for t in range(2,13):
  n,F=family(t);assert valid(n,F);checks+=1
  x=[[1,0],[0,1]]
  for _ in range(t):x=bm(x,A)
  assert x[0][0] or x[1][1];checks+=1
  for bad in range(t):
   x=[[1,0],[0,1]]
   for i in range(t):x=bm(x,B if i==bad else A)
   assert not(x[0][0] or x[1][1]);checks+=1
 assert len(r['tests'])==12 and all(z['SAT']=='SAT' and z['UNSAT']=='UNSAT' and z['SAT_ledger']['max_live_source_ids']<=18 for z in r['tests']);checks+=len(r['tests'])*3
 assert r['controls']=={'Y6_models':20,'F9_models':70,'G2_SAT_models':1,'G2_UNSAT_models':0,'F9_SU_pair_modes':264,'F15_SAT_models':2,'F15_UNSAT_models':0};checks+=7
 out={'run':'LOGSPACE_ANONYMOUS_CYCLE_REFEREE274_NO_IMPORT_VERIFY','status':'PASS','checks':checks,'P_vs_NP':'OPEN','independence':'no producer import'}
 Path(a.out).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
