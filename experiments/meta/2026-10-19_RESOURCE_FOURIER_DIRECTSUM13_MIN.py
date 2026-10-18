#!/usr/bin/env python3
"""Minimal SOURCE-FOURIER13 adaptive two-probe audit."""
from math import comb,sqrt
for n in (4,5,6):
 S=n+1;Q=1<<n;N=1<<S;errors=0;varying=0
 for x in range(Q):
  root=(3*x+1)%S
  choices=set()
  for a in range(N):
   first=(a>>root)&1
   nxt=((7*x+2) if first else (5*x+1))%S
   choices.add(nxt)
   guess=first^((a>>nxt)&1)^(x.bit_count()&1)
   truth=(a&1)^(((a>>1)&x).bit_count()&1)
   errors+=(guess!=truth)
  varying+=len(choices)>1
 D=1+S+comb(S,2)
 bound=max(0,(1-sqrt(D/Q))/2)
 assert varying and errors/(N*Q)+1e-12>=bound
 print(dict(n=n,cells=S,queries=Q,degree2_dimension=D,
            actual_mean_error=errors/(N*Q),bound=bound,
            data_dependent_address_queries=varying))
