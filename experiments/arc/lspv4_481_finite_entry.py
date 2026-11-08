#!/usr/bin/env python3
"""LSPV-4/481 exact rational finite-entry verifier. No native FLMV execution."""
from fractions import Fraction as Q
from decimal import Decimal, localcontext
import json,random
TSTAR=Q(6,5); SSTAR=Q(1,2); L=Q(433,216); GAP=Q(1,90)
def beta(t): return ((t+2)/t**2-t)/2
def step(t,s): return max(Q(11,10),Q(3,5)+t/2),max(Q(1,2),s/2)
def bound(t,s):
 a=L*max(Q(0),t-TSTAR)+max(Q(0),s-SSTAR)
 j=0
 while a>Q(2**j,180): j+=1
 return j,a
def dec(q):
 with localcontext() as ctx:
  ctx.prec=32
  return str(Decimal(q.numerator)/Decimal(q.denominator))
def run():
 rng=random.Random(481)
 cases=[(Q(1),Q(0)),(Q(1),Q(1)),(TSTAR,SSTAR),(Q(1000),Q(1000)),(Q(10**6),Q(10**6)),(Q(7,6),Q(3,5)),(Q(119,100),Q(49,100)),(Q(1206,1000),Q(511,1000))]
 for _ in range(3000):
  cases.append((Q(rng.randrange(1,50001),rng.randrange(1,2501)),Q(rng.randrange(0,50001),rng.randrange(1,2501))))
 maxj=0; mingap=Q(10**6); samples=[]
 for i,(t0,s0) in enumerate(cases):
  j,a=bound(t0,s0);t,s=t0,s0
  for _ in range(j):t,s=step(t,s)
  dt=max(Q(0),t0-TSTAR);ds=max(Q(0),s0-SSTAR)
  assert t<=TSTAR+dt/Q(2**j)
  assert s<=SSTAR+ds/Q(2**j)
  assert beta(t)-s>=GAP-a/Q(2**j)
  assert beta(t)-s>=Q(1,180)
  assert j==0 or a>Q(2**(j-1),180)
  maxj=max(maxj,j);mingap=min(mingap,beta(t)-s)
  if i<8:samples.append(dict(t0=str(t0),s0=str(s0),j=j,t_j=str(t),s_j=str(s),gap=dec(beta(t)-s)))
 return dict(run="LSPV-4/481",cases=len(cases),assertions=5*len(cases),max_selected_depth=maxj,min_exact_gap_at_selected_depth=str(mingap),min_gap_decimal=dec(mingap),target_half_gap=str(Q(1,180)),lipschitz_slope=str(L),samples=samples,status="COMPUTATIONAL exact-rational controls; conditional finite-entry lemma PROVED/RESTRICTED; universal transformation OPEN")
if __name__=="__main__":print(json.dumps(run(),sort_keys=True,indent=2))
