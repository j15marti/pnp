#!/usr/bin/env python3
"""Independent stdlib spot-check of BALANCED-OCCURRENCE-FIREWALL243.
Source-indexed only; full solver and 666KB data remain in the downloadable bundle.
No program herein claims to solve unrestricted SAT in polynomial time.
"""
from itertools import product, combinations

K4 = [
 (1,2,3),(-1,-2,-3),(1,4,5),(-1,-4,-5),
 (2,4,6),(-2,-4,-6),(3,5,6),(-3,-5,-6)
]
CUBE9 = [
 (1,2,4),(2,3,5),(3,1,6),(-1,-2,-7),(-2,-3,-8),(-3,-1,-9),
 (-4,-6,-7),(7,-5,8),(5,9,6),(8,-9,-6),(7,-4,9),(4,-8,-5)
]
def nvars(F): return max(abs(z) for c in F for z in c)
def littrue(z,a): return a[abs(z)-1] == (z>0)
def count(c,a): return sum(littrue(z,a) for z in c)
def sat(F,a): return all(count(c,a)>=1 for c in F)
def target(c,mode): return {abs(z):int((z>0) if mode=="S" else (z<0)) for z in c}
def compatible(c,d,p,q):
    a,b=target(c,p),target(d,q)
    return all(a[i]==b[i] for i in a.keys() & b.keys())
def direct_compatible(c,d,p,q):
    n=max(max(map(abs,c)),max(map(abs,d)))
    return any(all(count(x,a)==(3 if mode=="S" else 0)
                   for x,mode in ((c,p),(d,q)))
               for a in product((0,1),repeat=n))
def status(F,a):
    t=[count(c,a) for c in F]
    return t,[t.count(i) for i in range(4)]
def metrics(F,pin):
    n=nvars(F); m=len(F); k=len(pin)
    cfixed=[sum((abs(z) in pin and pin[abs(z)]==(z>0)) for z in c) for c in F]
    z=sum(x==0 for x in cfixed)
    h2=sum(x>=2 for x in cfixed);h3=sum(x==3 for x in cfixed)
    empty_unit=any(
        fixed==0 and sum(abs(z) not in pin for z in c)<=1
        for c,fixed in zip(F,cfixed))
    return z,h2,h3,empty_unit
def strict22(F):
    n=nvars(F); m=len(F)
    if 3*m!=4*n or any(len(c)!=3 or len(set(map(abs,c)))!=3 for c in F):
        return False
    return all(sum(z==v for c in F for z in c)==2
               and sum(z==-v for c in F for z in c)==2
               for v in range(1,n+1))
def residual(F,pin):
    return [tuple(z for z in c if abs(z) not in pin)
            for c in F if not any(abs(z) in pin and pin[abs(z)]==(z>0)
                                  for z in c)]
def check_formula(F, exhaustive_pins=True):
    assert strict22(F)
    n=nvars(F);m=len(F);checked=0
    for aa in product((0,1),repeat=n):
        a=tuple(aa)
        ts,ns=status(F,a)
        inv=tuple(1-v for v in a)
        assert [3-t for t in ts]==status(F,inv)[0]
        assert ns[::-1]==status(F,inv)[1]
        assert sum(ts)==2*n
        if sat(F,a):
            assert ns[1]==m//2+ns[3] and ns[2]==m//2-2*ns[3]
    if exhaustive_pins:
        for pin_vals in product((-1,0,1),repeat=n):
            pin={i+1:v for i,v in enumerate(pin_vals) if v>=0}
            z,h2,h3,unit=metrics(F,pin)
            k=len(pin)
            assert h2+h3==2*k-m+z
            if not unit: assert h2+h3<=m//2
            if not unit and h2+h3==m//2:
                assert all(len(c)==2 for c in residual(F,pin))
            checked+=1
    return checked

def pair_check():
    F=[c for support in combinations(range(1,5),3)
       for signs in product((-1,1),repeat=3)
       for c in [tuple(x*s for x,s in zip(support,signs))]]
    pair_count=0; incompatible_exact_one=0
    for c,d in combinations(F,2):
        for p in 'SU':
            for q in 'SU':
                assert compatible(c,d,p,q)==direct_compatible(c,d,p,q)
                pair_count+=1
        actual=any(count(c,a)==1==count(d,a) for a in product((0,1),repeat=4))
        odd_same=(set(map(abs,c))==set(map(abs,d))
                  and sum((u>0)!=(v>0) for u,v in zip(c,d))%2==1)
        assert actual!=(odd_same)
        incompatible_exact_one+=int(not actual)
    return pair_count,incompatible_exact_one

def main():
    assert strict22(K4) and strict22(CUBE9)
    checks=check_formula(K4,True)+check_formula(CUBE9,False)
    pin={4:0,5:0,6:0,7:1,8:1,9:1}
    z,h2,h3,unit=metrics(CUBE9,pin)
    assert (z,h2,h3,unit)==(6,4,2,False)
    assert residual(CUBE9,pin)==[
        (1,2),(2,3),(3,1),(-1,-2),(-2,-3),(-3,-1)]
    for a in product((0,1),repeat=3):
        full=a+(0,0,0,1,1,1)
        assert not sat(CUBE9,full)
    pair_modes,incompatible=pair_check()
    # Separately each pair is exactly-one feasible, the triple is not.
    counter=[(-1,-2,-3),(-1,-2,-4),(-1,3,4)]
    assignments=list(product((0,1),repeat=4))
    for c,d in combinations(counter,2):
        assert any(count(c,a)==count(d,a)==1 for a in assignments)
    assert not any(all(count(c,a)==1 for c in counter) for a in assignments)
    assert any(sat(counter,a) for a in assignments)
    assert pair_modes==1984 and incompatible==64
    print({"status":"PASS","K4_partial_cubes":checks,"pair_extreme_modes":pair_modes,
           "incompatible_exact_one_pairs":incompatible,
           "CUBE9_pinned_UNSAT":True,
           "scope":"finite controls only; proofs in public TeX"})

if __name__=="__main__":
    main()
