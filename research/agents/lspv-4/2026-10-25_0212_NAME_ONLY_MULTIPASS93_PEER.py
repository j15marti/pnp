#!/usr/bin/env python3
"""Independent compact identifier-only proper-3CNF SAT join reproducer."""
from itertools import combinations, product
from math import ceil, log2, comb

def pin(x,a,b,v):
    return [(x if v else -x, sa*a, sb*b)
            for sa,sb in product((1,-1), repeat=2)]

def make(q,A,B):
    ans=[]
    for j,(x,v) in enumerate([(x,1) for x in sorted(A)] +
                             [(x,0) for x in sorted(B)], start=1):
        ans+=pin(x,q+2*j-1,q+2*j,v)
    return ans

def sat_eval(cls,bits):
    return all(any(bool(bits>>(abs(l)-1)&1)==(l>0) for l in clause)
               for clause in cls)

def main():
    assertions=0
    for q in (2,4,6,8):
        sets=[frozenset(z) for z in combinations(range(1,q+1),q//2)]
        w=ceil(log2(64*(7*q+1)))
        N=(16*q+2)*w
        yes=no=0
        for A in sets:
            for B in sets:
                C=make(q,A,B)
                assert len(C)==4*q and all(len(set(map(abs,c)))==3 for c in C)
                assertions+=1
                expected=not(A&B)
                assert expected==(B==frozenset(set(range(1,q+1))-A))
                assertions+=1
                if expected:
                    yes+=1
                    witness=sum(1<<(x-1) for x in A)
                    assert sat_eval(C,witness)
                else:
                    no+=1
                    x=next(iter(A&B))
                    assert any(x in c for c in C) and any(-x in c for c in C)
                assertions+=1
                if q<=4:
                    actual=sum(sat_eval(C,z) for z in range(1<<(3*q)))
                    assert actual == ((1<<(2*q)) if expected else 0)
                    assertions+=1
        assert yes==comb(q,q//2) and no==len(sets)**2-yes
        assertions+=1
        for A in sets:
            for D in sets:
                if A!=D:
                    assert A & (set(range(1,q+1))-D)
                    assertions+=1
        print({'q':q,'N':N,'yes':yes,'no':no,'fooling':len(sets)})
    print({'status':'PASS','assertions':assertions})

if __name__=='__main__':
    main()
