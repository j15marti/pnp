#!/usr/bin/env python3
"""TMR-5/100 compact independently auditable native T5 controls."""
from itertools import product
from fractions import Fraction

R=lambda a,b: (b-a)%5 in (1,3)
arcs=[(0,2),(2,1),(0,3),(1,3),(4,0),(1,4)]
blocks=[arcs[:4],arcs[4:]]
def count(edges):
    return sum(all(R(x[u],x[v]) for u,v in edges) for x in product(range(5),repeat=5))
def local(i,d):
    edges=blocks[i]
    private=sorted({x for uv in edges for x in uv}-{0,1})
    for x in product(range(5),repeat=len(private)):
        lab={0:0,1:d,**dict(zip(private,x))}
        if all(R(lab[u],lab[v]) for u,v in edges):
            return True
    return False
checks=0
assert count(arcs)==0
checks+=1
for j in range(6):
    assert count(arcs[:j]+arcs[j+1:])>0
    checks+=1
status=[]
for d in range(5):
    f=tuple(i for i in range(2) if not local(i,d))
    status.append(f)
    checks+=1
assert status==[(0,1),(0,),(1,),(0,),(0,)]
for m in range(1,7):
    patterns=set()
    for d in product(range(5),repeat=m):
        patterns.add(tuple(status[x] for x in d))
        checks+=1
    assert len(patterns)==3**m
    checks+=1
cycles=0
for ell in range(3,12):
    for eps in product((0,1),repeat=ell):
        q=sum(eps)
        t=next((t for t in range(min(4,ell)+1)
                if (ell+q+2*t)%5==0),None)
        assert t is not None
        # Fully realized valid T5 assignment on the oriented cycle.
        color=[0]*ell
        for i in range(ell-1):
            color[i+1]=(color[i]+1+eps[i]+2*(i<t))%5
        assert (color[-1]+1+eps[-1]+2*(ell-1<t))%5==0
        for i in range(ell):
            u,v=i,(i+1)%ell
            assert (R(color[u],color[v]) if eps[i]==0 else R(color[v],color[u]))
        cycles+=1;checks+=1
assert cycles==4088
assert Fraction(169,200)+Fraction(7,20)*Fraction(97,70)==Fraction(133,100)
assert Fraction(239,200)+Fraction(7,20)==Fraction(309,200)
print({'status':'PASS','tests':checks,'native_critical_arc_deletions':6,
       'cycle_orientations':cycles,'m6_failure_profiles':729,
       'decision_seed_exponent_t1':str(Fraction(239,200)),
       'naive_blackbox_search_exponent_t1':str(Fraction(309,200))})
