"""Deterministic order-independent multiset certificate; bounded finite field test."""
import itertools as it
import json
import random
import signal
from collections import Counter
signal.signal(signal.SIGALRM,lambda *_: (_ for _ in ()).throw(TimeoutError()))
signal.alarm(24)
P=65537

def codes(f,a,v,m):
    for row in f:
        s=set(); sat=False
        for x in row:
            m['literal_reads']+=1
            assert 1<=abs(x)<=v
            if abs(x) in a: sat |= a[abs(x)]==(x>0)
            else: s.add(x)
        if sat or any(-x in s for x in s): continue
        code=1
        for x in sorted(s): code=code*(2*v+1)+(2*abs(x)-(x>0))
        if code>=P: raise ValueError('clause code outside field; no modular encoding allowed')
        yield code

def compare(f,a,b,v,cap,m):
    na=sum(1 for _ in codes(f,a,v,m)); nb=sum(1 for _ in codes(f,b,v,m))
    if na!=nb:return 'DISTINCT'
    if na>=P:raise ValueError('degree exceeds field')
    for z in range(min(cap,na+1)):
        pa=pb=1
        for c in codes(f,a,v,m):pa=pa*(z-c)%P
        for c in codes(f,b,v,m):pb=pb*(z-c)%P
        m['evaluation_pairs']+=1
        if pa!=pb:return 'DISTINCT'
    return 'EQUAL' if cap>=na+1 else 'UNKNOWN'

def main():
    assert all(P%d for d in range(2,257))
    cases=0
    clauses=tuple(it.product((-2,2),(-3,3)))
    for a in range(16):
        for b in range(16):
            left=tuple(c for i,c in enumerate(clauses) if a>>i&1)
            right=tuple(c for i,c in enumerate(clauses) if b>>i&1)
            f=tuple((1,)+c for c in left)+tuple((-1,)+c for c in reversed(right))
            got=compare(f,{1:False},{1:True},3,10,Counter())
            assert (got=='EQUAL')==(left==right)
            cases+=1
    rows=[]
    for size in (8,32,128,512):
        core=[(2+i%15,) for i in range(size)]
        other=core.copy();random.Random(13).shuffle(other)
        f=tuple((1,)+c for c in core)+tuple((-1,)+c for c in other)
        for cap in (4,size+1):
            m=Counter();ans=compare(f,{1:False},{1:True},16,cap,m)
            assert ans==('EQUAL' if cap>=size+1 else 'UNKNOWN')
            rows.append(dict(size=size,cap=cap,answer=ans,**m))
    # One evaluation is not an exact certificate: product collision at z=0.
    assert (1*6)%P==(2*3)%P
    assert ((1-1)*(1-6))%P!=((1-2)*(1-3))%P
    print(json.dumps(dict(status='COMPUTATIONAL',cases=cases,prime=P,seed=13,
                         single_point_collision=[[1,6],[2,3]],scaling=rows),indent=2))
if __name__=='__main__':main()
