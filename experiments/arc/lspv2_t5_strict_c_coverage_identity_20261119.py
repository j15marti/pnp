#!/usr/bin/env python3
"""Independent proof-by-exhaustion of the strict T5 C occupancy identity.
The full fan-in-two circuit builder, source-checked CNF emitter, and independent
replayer are in the role-owned Library archive linked from the research report.
"""
from itertools import product
def r(a,b):
    return (b-a)%5 in (1,3)
def c(a,b,d):
    return (r(a,b) and r(b,d) and r(d,a)) or (r(a,d) and r(d,b) and r(b,a))
def s(a,b,d):
    return (r(a,b) and r(d,a)) or (r(a,d) and r(b,a))
def q(a,b,d):
    return r(a,b) != r(a,d)
def p(a,b,d):
    return r(a,b) and r(a,d)
def coverage(a,b,d):
    on = {a,b,d}
    return any({i,(i+1)%5,(i+2)%5}.issubset(on) for i in range(5))
counts = {'C':0,'S':0,'Q':0,'P':0}
for triple in product(range(5),repeat=3):
    a,b,d=triple
    assert c(a,b,d)==coverage(a,b,d)
    for k,v in [('C',c(a,b,d)),('S',s(a,b,d)),('Q',q(a,b,d)),('P',p(a,b,d))]:
        counts[k]+=int(v)
assert counts=={'C':30,'S':40,'Q':60,'P':20},counts
print(counts)
