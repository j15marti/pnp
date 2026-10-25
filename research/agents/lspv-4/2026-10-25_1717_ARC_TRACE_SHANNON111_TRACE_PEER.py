#!/usr/bin/env python3
"""Actual traced two-level source-dependent Shannon SAT contractor; standard Python."""
from itertools import product
def restrict(f,v,b):
    return tuple(tuple(z for z in c if z!=(-v if b else v))
                 for c in f if (v if b else -v) not in c)
class ExactProgram:
    def __init__(self,read_order):self.read_order=read_order
    def run(self,f):
        ids=range(len(f)) if self.read_order=='front' else reversed(range(len(f)))
        for i in ids:
            literals=f[i] if self.read_order=='front' else tuple(reversed(f[i]))
            for z in literals:yield ('READ',z)
        def solve(g):
            yield ('NODE',len(g))
            if any(len(c)==0 for c in g):return False
            if not g:return True
            v=min(abs(z) for c in g for z in c)
            for b in (False,True):
                yield ('BRANCH',v)
                if (yield from solve(restrict(g,v,b))):return True
            return False
        result=yield from solve(f)
        yield ('HALT',result)
def contractor(f,A,d=2,budget=2):
    if d==0:
        return next(ev[1] for ev in A.run(f) if ev[0]=='HALT')
    v=None
    for i,ev in enumerate(A.run(f)):
        if ev[0]=='READ' and v is None:v=abs(ev[1])
        if ev[0]=='HALT':return ev[1]
        if i+1==budget:break
    if v is None:
        v=next((abs(z) for c in f for z in c),None)
    if v is None:return len(f)==0
    return contractor(restrict(f,v,False),A,d-1,budget) or contractor(restrict(f,v,True),A,d-1,budget)
def check():
    base=[tuple(-j-1 if row>>j&1 else j+1 for j in range(3)) for row in range(8)]
    checks=0
    for bits in range(256):
        f=tuple(c for j,c in enumerate(base) if (bits>>j)&1)
        expected=any(all(any(a[abs(z)-1]==(z>0) for z in c) for c in f)
                     for a in product((False,True),repeat=3))
        for order in ('front','back'):
            assert contractor(f,ExactProgram(order))==expected
            checks+=1
    return {'checks':checks,'failures':0,'observed_trace_first_variables':{
        'front':next(ev[1] for ev in ExactProgram('front').run(tuple(base)) if ev[0]=='READ'),
        'back':next(ev[1] for ev in ExactProgram('back').run(tuple(base)) if ev[0]=='READ')}}
if __name__=='__main__':print(check())
