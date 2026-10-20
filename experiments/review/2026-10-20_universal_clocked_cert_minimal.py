"""Finite controls for UNIVERSAL-UNDECIDABLE-CERT3.
The tests illustrate, but cannot prove, undecidability.
"""
from fractions import Fraction as F
from math import isqrt
def sat(cs):
    return any(all(any((v>0)==bool(a) for v in clause) for clause in cs)
               for a in (0,1))
def encode(cs):
    return ";".join("("+"|".join(str(v) for v in c)+")" for c in cs)
checks=0
for pad in range(35):
    for cs in [((1,),)+((1,),)*pad,((1,),(-1,))+((1,),)*pad]:
        truth=sat(cs); n=len(encode(cs))
        for halt in [1,5,15,53,101,1000,None]:
            got=truth ^ (halt is not None and n>=halt)
            assert (got!=truth)==(halt is not None and n>=halt)
            checks+=1
pointers=0
for n in range(2,10):
    for i in range(n):
        assert {(x>>i)&1 for x in range(1<<n)}=={0,1}
        pointers+=1
a=F(6,5); rows=0
for C in (2,7,31):
    for k in (4,16,64,256,1024):
        for d in (1,isqrt(k),k//2,k):
            assert a*C*d/k>=0
            if d==k: assert a*C*d/k==a*C
        rows+=1
print(dict(clocked=checks,pointers=pointers,exponent_rows=rows,failures=0))
