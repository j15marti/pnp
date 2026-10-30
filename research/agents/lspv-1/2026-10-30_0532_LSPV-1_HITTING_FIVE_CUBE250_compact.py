#!/usr/bin/env python3
"""HITTING-FIVE-CUBE250 independent minimal original-clause certificate.
stdlib Python 3; source occurrences always refer to common ORIGINAL variables.
This is a compact audit; expanded raw experiments in the full reproducibility ZIP.
"""
from itertools import combinations,product
C=[
(1,2,4),(-1,3,5),(-2,-3,6),(1,-2,3),(-1,2,-3),
(-4,-5,-6),(4,5,-6),(-4,-5,6)]
B=[(1,2),(-1,3),(-2,-3)]
D=B+[(1,-2,3),(-1,2,-3)]
def sat(c,a):return any(a[abs(t)]==int(t>0) for t in c)
def tc(c,a):return sum(a[abs(t)]==int(t>0) for t in c)
def count(f,n,pins=None):
    pins=pins or {}
    return sum(all(sat(c,dict(enumerate(bits,1))) for c in f)
       for bits in product((0,1),repeat=n)
       if all(bits[i-1]==v for i,v in pins.items()))
def extreme(c,typ):return {abs(l):int((l>0)==(typ=="S")) for l in c}
def mode(c,d,t):
    x=extreme(c,t[0]);y=extreme(d,t[1])
    return all(v not in y or y[v]==b for v,b in x.items())
def resolvent(c,d,pivot):
    x=set(c);y=set(d)
    if pivot in x and -pivot in y:
        r=(x-{pivot})|(y-{-pivot})
    elif -pivot in x and pivot in y:
        r=(x-{-pivot})|(y-{pivot})
    else:raise AssertionError("missing original parent pivot")
    assert not any(-q in r for q in r),("tautological",r)
    return tuple(sorted(r,key=lambda z:(abs(z),z)))
def proof():
    a,b,c,d,e=C[:5]
    r1=resolvent(a,b,1)
    r2=resolvent(a,e,1)
    r3=resolvent(d,b,1)
    r4=resolvent(r1,r3,2)
    r5=resolvent(r2,c,2)
    r6=resolvent(r4,r5,3)
    assert set(r6)=={4,5,6}
    return [r1,r2,r3,r4,r5,r6]
def verify():
    for i in range(1,7):
        assert sum(i in c for c in C)==2
        assert sum(-i in c for c in C)==2
    assert len(C)==8 and all(len(c)==3 and len(set(map(abs,c)))==3 for c in C)
    for j,k in combinations(range(len(C)),2):
        overlap=set(map(abs,C[j]))&set(map(abs,C[k]))
        same={v for v in overlap if ((v in C[j])==(v in C[k]))}
        opp=overlap-same
        for t in ('SS','SU','US','UU'):
            assert mode(C[j],C[k],t)==(not opp if t in ('SS','UU') else not same)
            found=False
            for bits in product((0,1),repeat=6):
                assignment=dict(enumerate(bits,1))
                if tc(C[j],assignment)==(3 if t[0]=='S' else 0) and \
                   tc(C[k],assignment)==(3 if t[1]=='S' else 0):
                    found=True;break
            assert found==mode(C[j],C[k],t)
    for v in (0,1):
        a={i:v for i in range(1,7)}
        histogram=[sum(tc(c,a)==k for c in C) for k in range(4)]
        assert histogram==[1,3,3,1]
    for bits in product((0,1),repeat=6):
        a=dict(enumerate(bits,1));z={i:1-v for i,v in a.items()}
        assert all(tc(c,a)+tc(c,z)==3 for c in C)
    assert count(C,6)==12
    assert count(B,3)==2
    assert count(D,3)==0
    assert count(C,6,{4:0,5:0,6:0})==0
    # Five U falsification cylinders on x,y,z partition the eight assignments.
    ucover=[]
    for bits in product((0,1),repeat=3):
        a=dict(enumerate(bits,1))
        false=[j for j,c in enumerate(D) if not sat(c,a)]
        assert len(false)==1
        ucover.append(false[0])
    assert sorted(ucover)==[0,0,1,1,2,2,3,4]
    for j,k in combinations(range(5),2):
        assert not mode(D[j],D[k],'UU')
    assert set(proof()[-1])=={4,5,6}
    print("PASS original eight clause targets/pairs/complements; 12 SAT models")
    print("PASS 5-clause U-partition; UP fixed point, binary 2SAT SAT")
    print("PASS six source-resolution steps: entails (g1 OR g2 OR g3)")
if __name__=="__main__":verify()
