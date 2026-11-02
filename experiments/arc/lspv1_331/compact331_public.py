#!/usr/bin/env python3
"""LSPV-1 BROOKS-ITERATED-DECISION331 compact independent numeric control.
For the full source-indexed polynomial Brooks selector and exact DP, see run ZIP."""
from decimal import Decimal,getcontext
from itertools import product
getcontext().prec=65
P,w,D=2,3,8
a=Decimal(1)
for r in range(7):
    a*=Decimal(D-1)/D
    print(r, "degree",D,"signed_polarity",P,"width",w,"Brooks_exponent_prefix",a)
    D,P,w=D+2*P*(P*(w-1)-1),P*P,2*(w-1)
pos=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
neg=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
F=pos+tuple(tuple(-x for x in c) for c in neg)
def ok(a):
    return all(any(a[abs(x)-1]==int(x>0) for x in c) for c in F)
models=sum(ok(x) for x in product((0,1),repeat=9))
pins={3:0,5:1,6:0,7:0,8:0}
counts={}
for val in (0,1):
    counts[val]=sum(ok(a) for a in product((0,1),repeat=9)
                    if all(a[v-1]==b for v,b in {**pins,1:val}.items()))
assert (models,counts[0],counts[1])==(70,2,0)
print("F9 original SAT models",models,"same-source branches",counts)
print("P versus NP OPEN")
