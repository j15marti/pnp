#!/usr/bin/env python3
"""No-import verifier for REFEREE273."""
from __future__ import annotations
import argparse,itertools,json,random
from pathlib import Path

I=((1,0),(0,1));X=((0,1),(1,0))
P={"2":((0,2),(0,0)),"8":((0,0),(0,10)),"B":((3,9),(0,3)),"C":((0,0),(8,18))}
S=("2","8","B","8","C","B");U=("2","8","C","B","8","B")
def mm(a,b):return tuple(tuple(sum(a[i][k]*b[k][j] for k in (0,1)) for j in (0,1)) for i in (0,1))
def mt(a):return tuple(tuple(a[j][i] for j in (0,1)) for i in (0,1))
def prod(ms):
 z=I
 for m in ms:z=mm(z,m)
 return z
def tr(a):return a[0][0]+a[1][1]
def gauge(ms,g):
 q=[X if z else I for z in g]
 return tuple(mm(mm(q[i],ms[i]),q[(i+1)%len(ms)]) for i in range(len(ms)))
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--raw",required=True);ap.add_argument("--out",required=True);a=ap.parse_args()
 raw=json.loads(Path(a.raw).read_text());assert raw["run"]=="ANONYMOUS_INTERFACE_GAUGE_REFEREE273" and raw["P_vs_NP"]=="OPEN"
 checks=0
 for word,want in ((S,14400),(U,0)):
  ms=tuple(P[x] for x in word);assert tr(prod(ms))==want;checks+=1
  for g in itertools.product((0,1),repeat=len(ms)):
   assert tr(prod(gauge(ms,g)))==want;checks+=1
  for r in range(len(ms)):
   z=ms[r:]+ms[:r];assert tr(prod(z))==want;checks+=1
   assert tr(prod(tuple(mt(x) for x in reversed(z))))==want;checks+=1
 rng=random.Random(273)
 for n in range(1,25):
  for _ in range(500):
   ms=tuple(tuple(tuple(rng.randrange(12) for _ in range(2)) for _ in range(2)) for _ in range(n))
   g=tuple(rng.randrange(2) for _ in range(n));base=tr(prod(ms))
   assert tr(prod(gauge(ms,g)))==base;checks+=1
   r=rng.randrange(n);z=ms[r:]+ms[:r]
   assert tr(prod(z))==base;checks+=1
   assert tr(prod(tuple(mt(x) for x in reversed(z))))==base;checks+=1
 assert raw["controls"]=={"Y6_models":20,"F9_models":70,"F9_SU_pair_modes":264,"F15_SAT_models":2,"F15_UNSAT_models":0,"malformed_rejected":5}
 out={"run":"ANONYMOUS_INTERFACE_GAUGE_REFEREE273_NO_IMPORT_VERIFY","status":"PASS","checks":checks,
      "independence":"did not import producer","P_vs_NP":"OPEN"}
 Path(a.out).parent.mkdir(parents=True,exist_ok=True);Path(a.out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
 print(json.dumps(out,indent=2))
if __name__=="__main__":main()
