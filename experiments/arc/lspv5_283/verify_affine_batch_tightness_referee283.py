#!/usr/bin/env python3
"""Independent no-import verifier for REFEREE283."""
import argparse,itertools,json
P=(((1,2,3),(4,5,6),(7,8,9)),((1,4,7),(2,5,8),(3,6,9)),((1,5,9),(2,6,7),(3,4,8)),((1,6,8),(2,4,9),(3,5,7)))
A=tuple(c if d<2 else tuple(-x for x in c) for d,q in enumerate(P) for c in q)
F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
def sat(F,z):return all(any(((z>>(abs(x)-1))&1)==int(x>0) for x in c) for c in F)
def graph(F,n):
 a=[set() for _ in range(n+1)]
 for c in F:
  for x,y in itertools.combinations(map(abs,c),2):a[x].add(y);a[y].add(x)
 return a
def lift(r):
 out=[]
 for d,pc in enumerate(P):
  for li,c in enumerate(pc):
   for t in range(r):
    q=[]
    for x in c:
     j=(t-1)%r if d==0 and li==0 and x==1 else t;v=9*j+x;q.append(v if d<2 else -v)
    out.append(tuple(q))
 return tuple(out)
def alpha_dp(F,r):
 a=graph(F,9*r);opts=[]
 for j in range(r):
  V=range(9*j+1,9*j+10);q=[]
  for mask in range(512):
   S=tuple(v for i,v in enumerate(V) if (mask>>i)&1)
   if all(y not in a[x] for x,y in itertools.combinations(S,2)):q.append(S)
  opts.append(q)
 best=0
 for first in opts[0]:
  dp={first:len(first)}
  for j in range(1,r):
   dp={cur:max((v for prev,v in dp.items() if all(y not in a[x] for x in prev for y in cur)),default=-999)+len(cur) for cur in opts[j]}
  best=max(best,max((v for last,v in dp.items() if all(y not in a[x] for x in last for y in first)),default=0))
 return best
def main():
 ap=argparse.ArgumentParser();ap.add_argument("raw");a=ap.parse_args();r=json.load(open(a.raw));checks=0
 assert sum(sat(A,z) for z in range(512))==18;checks+=512
 g=graph(A,9);assert all(len(g[v])==8 for v in range(1,10));checks+=9
 for x,y in itertools.combinations(range(1,10),2):assert y in g[x];checks+=1
 for t,e in enumerate(r["product_tightness"],1):
  assert e["alpha"]==t and e["n"]==9*t and e["components"]==t and e["witness_check"];checks+=4
  assert e["scrambled_recognition"]["components"]==t and e["scrambled_recognition"]["local_trials"]<=512*t;checks+=2
 for q in r["connected_lifts"]:
  k=q["r"];F=lift(k);got=alpha_dp(F,k);want=1 if k==1 else k+k//2
  assert got==q["alpha"]==want;checks+=1
 # Same-source opposite labels.
 p={2:0,3:0,4:0,5:1,6:1,7:1,8:0,9:0};cnt=[]
 for x1 in (0,1):
  q=sum(sat(A,z) and (z&1)==x1 and all(((z>>(v-1))&1)==b for v,b in p.items()) for z in range(512));cnt.append(q);checks+=512
 assert cnt==[0,1];checks+=1
 assert sum(sat(F9,z) for z in range(512))==70;checks+=512
 assert r["A9"]["OBDD"]=={"best":42,"natural":43,"worst":50};checks+=1
 assert r["F9_controls"]["OBDD"]=={"best":52,"natural":66,"worst":80};checks+=1
 assert r["projection_truth_rows"]==384 and r["malformed_rejected"]==6 and r["P_vs_NP"]=="OPEN";checks+=3
 print(json.dumps({"status":"PASS","assertions":checks,"A9_models":18,"same_original_models":cnt,"lift_alpha":[q["alpha"] for q in r["connected_lifts"]],"OBDD":{"A9":r["A9"]["OBDD"],"F9":r["F9_controls"]["OBDD"]},"P_vs_NP":"OPEN"},indent=2))
if __name__=="__main__":main()
