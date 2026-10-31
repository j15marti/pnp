#!/usr/bin/env python3
"""Reproduce ARC-TARGET-QUOTA-BATCH284 compact results, Python stdlib only.
Full original-indexed controls and actual bit-write samples are in the conversation ZIP.
This is a DECLARED scanning policy, not a native FLMV simulator or a complete validator.
"""
import json
from pathlib import Path
from collections import Counter
from itertools import product
from fractions import Fraction
ROOT=Path(__file__).resolve().parent
U=[tuple(C) for C in json.loads((ROOT/"U_source.json").read_text())]
V=[list(C) for C in U]
V[1][0],V[7][0]=V[7][0],V[1][0]
Y=[(1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6)]
V_WITNESS="010110111001100010001111000101011110010101001111010001001011010000110010000100001001010111010000111010101010001101001010010010110001100011111001010101011011001110000100000001110110111000101100100001"
def evalC(C,a):return any(a[abs(x)-1]==int(x>0) for x in C)
def check(F):
 n=max(abs(x) for C in F for x in C);m=len(F);d=Counter(x for C in F for x in C)
 assert m==4*n//3 and n%3==0 and len({tuple(sorted(C)) for C in F})==m
 assert all(len(C)==3 and len(set(abs(x) for x in C))==3 and (all(x>0 for x in C) or all(x<0 for x in C)) for C in F)
 assert all(d[i]==d[-i]==2 for i in range(1,n+1))
 return n,m
def dpll(F):
 def f(G):
  if any(not C for C in G):return False
  if not G:return True
  u=next((C[0] for C in G if len(C)==1),None)
  if u is not None:return f(tuple(tuple(z for z in C if z!=-u) for C in G if u not in C))
  a=min(G,key=len)[0]
  return any(f(tuple(tuple(z for z in C if z!=-lit) for C in G if lit not in C)) for lit in (a,-a))
 return f(tuple(tuple(C) for C in F))
def certify():
 assert sum(all(evalC(C,a) for C in Y) for a in product((0,1),repeat=6))==20
 w=[int(q) for q in V_WITNESS]
 assert len(w)==198 and all(evalC(C,w) for C in V)
 ports=[]
 for t in range(6):
  lo=32*t+1;hi=lo+31
  raw=U[2+42*t:2+42*(t+1)]
  core=[tuple(z for z in C if lo<=abs(z)<=hi) for C in raw]
  assert not dpll(core)
  ports.append(tuple({z for C in raw for z in C if abs(z)>192}))
 for a in product((0,1),repeat=6):
  ext=[0]*192+list(a)
  assert not evalC(U[0],ext) or not evalC(U[1],ext) or any(not any(evalC((z,),ext) for z in P) for P in ports)
def batch(F,b):
 n,m=check(F);b=min(b,n);p=(n+b-1)//b
 w=n.bit_length();P=m*(1+3*w)
 updates=0
 for low in range(1,n+1,b):
  high=min(n,low+b-1)
  d=Counter(x for C in F for x in C if low<=abs(x)<=high)
  assert all(d[i]==d[-i]==2 for i in range(low,high+1))
  updates+=sum(d.values())
 assert updates==4*n
 last=n-b*(p-1)
 return {"b":b,"passes":p,"payload_bits":P,"source_bit_reads":P*p,
 "source_clause_visits":m*p,"literal_inspections":3*m*p,"counter_bits":4*b,
 "counter_XOR_adjacent":6*n+2*(n-last),"counter_XOR_endpoint":2*last,
 "counter_increments":updates,"read_space_product":4*b*P*p}
def FLMV(c,k):
 f=Fraction(1)
 for _ in range(k):f=c*f/(1+f)
 return min((1/f-c)/k,c**(-k))
def main():
 certify()
 for c,expected in [(Fraction(6,5),Fraction(23,45)),(Fraction(241,200),Fraction(11642479,23232400))]:
  d=[FLMV(c,k) for k in range(1,4)]
  assert d[1]==expected and d[1]>max(d[0],d[2],c**(-4))
 o={}
 for name,F in [("Y6_SAT",Y),("U198_UNSAT",U),("V198_SAT",V)]:
  n,m=check(F)
  o[name]={"n":n,"m":m,"label":name.split("_")[-1],"cases":[batch(F,b) for b in (1,8,32,64,198)]}
 dup=[(1,2,3)]*2+[(4,5,6)]*2+[(-1,-2,-3)]*2+[(-4,-5,-6)]*2
 mix=[list(C) for C in Y];mix[0][0]*=-1;mix[4][0]*=-1
 rep=[list(C) for C in Y];rep[0][1],rep[1][0]=rep[1][0],rep[0][1]
 for F in (dup,mix,rep):
  d=Counter(x for C in F for x in C)
  assert all(d[i]==d[-i]==2 for i in range(1,7))
  try:check(F)
  except AssertionError:pass
  else:raise AssertionError("quota-only counterfeit accepted")
 o["status"]="CERTIFIED BOTH LABELS; restricted multipass theorem only; ARC/FLMV transfer and P vs NP OPEN"
 o["FLMV"]={"6/5":"23/45","241/200":"11642479/23232400"}
 print(json.dumps(o,sort_keys=True,indent=2))
if __name__=="__main__":main()
