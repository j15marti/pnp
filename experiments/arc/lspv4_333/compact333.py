#!/usr/bin/env python3
"""LSPV4 CONNECTED-MONOTONE-TRANSFER333; Python stdlib, no SAT oracle.
Valid canonical monotone 3-SAT-(2,2), connected occurrence-swapped Z6 chain.
All-length recurrence is restricted-model #SAT upper bound, not P vs NP.
"""
from collections import Counter
import json
Z=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-3),(-1,-4,-5),(-2,-4,-6),(-3,-5,-6))
F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
def valid(F,n):
 if n<1 or n%3 or len(F)*3!=4*n:return False
 c=Counter(); seen=set()
 for cl in F:
  if len(cl)!=3 or len({abs(v) for v in cl})!=3 or any(not 1<=abs(v)<=n for v in cl):return False
  if not(all(v>0 for v in cl) or all(v<0 for v in cl)):return False
  k=tuple(sorted(cl))
  if k in seen:return False
  seen.add(k);c.update(cl)
 return all(c[j]==c[-j]==2 for j in range(1,n+1))
def chain(t):
 if t<1:raise ValueError
 F=[[v//abs(v)*(abs(v)+6*i) for v in cl] for i in range(t) for cl in Z]
 for i in range(t-1):
  a,b=8*i+1,8*(i+1)
  assert F[a][1]==6*i+4 and F[b][0]==6*(i+1)+1
  F[a][1],F[b][0]=F[b][0],F[a][1]
 F=tuple(map(tuple,F))
 assert valid(F,6*t)
 return F
def sat(F,a):
 return all(any(((a>>(abs(v)-1))&1)==int(v>0) for v in cl) for cl in F)
def bit(a,j):return (a>>(j-1))&1
def h(a):return all(any(bit(a,abs(v))==int(v>0) for v in cl) for j,cl in enumerate(Z) if j not in (0,1))
def sig(a):return 4*bit(a,1)+2*bit(a,4)+bit(a,5)
def mat():
 v=[0]*8;u=[int(bool((r>>2)&1 or (r>>1)&1 or r&1)) for r in range(8)]
 M=[[0]*8 for _ in range(8)]
 B=[a for a in range(64) if h(a)]
 for b in B:
  if any(bit(b,i) for i in (1,2,3)):v[sig(b)]+=1
 for r in range(8):
  x1,x4,x5=(r>>2)&1,(r>>1)&1,r&1
  for b in B:
   if (x1 or bit(b,1) or x5) and (x4 or bit(b,2) or bit(b,3)):M[r][sig(b)]+=1
 return v,M,u,len(B)
def mul(v,M):
 return [sum(v[i]*M[i][j] for i in range(8)) for j in range(8)]
def main():
 v,M,u,H=mat(); assert H==27
 assert v==[4,3,3,3,3,3,3,0] and u==[0,1,1,1,1,1,1,1]
 w1=mul(v,M);w2=mul(w1,M);w3=mul(w2,M)
 assert all(w3[j]-15*w2[j]-50*w1[j]+36*v[j]==0 for j in range(8))
 seq=[];w=v
 for t in range(1,13):
  seq.append(sum(w[i]*u[i] for i in range(8)))
  w=mul(w,M)
 assert seq[:5]==[18,318,5630,99702,1765582]
 for j in range(9):assert seq[j+3]==15*seq[j+2]+50*seq[j+1]-36*seq[j]
 models={}
 for t in (1,2,3):
  F=chain(t);models[t]=sum(sat(F,a) for a in range(1<<(6*t)))
  assert models[t]==seq[t-1]
 A=tuple(Z)+tuple(tuple((abs(v)+6)*(1 if v>0 else -1) for v in cl) for cl in Z)
 B=chain(2);before={a for a in range(4096) if sat(A,a)};after={a for a in range(4096) if sat(B,a)}
 assert (len(before),len(after),len(before&after),len(before-after),len(after-before))==(324,318,270,54,48)
 def cnt(p):
  return sum(all(bit(a,i)==b for i,b in p.items()) for a in after)
 assert cnt({1:0,2:1,4:1})==53 and cnt({1:1,2:1,4:1})==0
 malformed=[B+(B[0],),((1,-2,3),)+B[1:],((1,1,3),)+B[1:],B[:-1],((1,2,13),)+B[1:],((0,2,3),)+B[1:]]
 assert all(not valid(x,12) for x in malformed)
 assert valid(F9,9) and sum(sat(F9,a) for a in range(512))==70
 return dict(run="CONNECTED_MONOTONE_TRANSFER333",t_1_12=[str(x) for x in seq],
             brute_models=models,source_rows=266304,source_private_gates=[23,47,71],
             v=v,u=u,M=M,annihilator_vector=[0]*8,
             before_models=324,after_models=318,both=270,before_only=54,after_only=48,
             pinned_SAT_0=53,pinned_UNSAT_1=0,malformed_rejected=6,
             F9_models=70,F9_private_gates=35,P_vs_NP="OPEN")
if __name__=="__main__":print(json.dumps(main(),indent=2,sort_keys=True))
