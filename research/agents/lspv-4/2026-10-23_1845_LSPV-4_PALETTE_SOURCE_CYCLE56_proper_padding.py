#!/usr/bin/env python3
"""LSPV-4 proper exactly-three-clause padding companion, standard library only.
Checks q=3..8 all 504 source orientations and 3576 single-bit flips.
"""
from itertools import product
from math import ceil, log2

def graph(bits):
    q=len(bits)
    def x(i):return 3+2*(i%q)
    E=[(0,1),(1,2),(2,0)]
    for i in range(q):
        E.extend(((0,x(i)),(0,x(i)+1),(x(i),x(i)+1)))
    for i,b in enumerate(bits):
        E.append((x(i+1),x(i) if b else x(i)+1))
    assert len(E)==4*q+3
    return 2*q+3,E

def mixed_onehot(V,E):
    var=lambda v,c:3*v+c+1
    C=[]
    for v in range(V):
        C.append(tuple(var(v,c) for c in range(3)))
        C.extend((-var(v,a),-var(v,b)) for a,b in ((0,1),(0,2),(1,2)))
    for u,v in E:
        C.extend((-var(u,c),-var(v,c)) for c in range(3))
    return 3*V,C

def padded(n,C):
    P=[];j=0
    for c in C:
        if len(c)==2:
            j+=1;t=n+j
            P.extend(((c[0],c[1],t),(c[0],c[1],-t)))
        else:P.append(c)
    return n+j,P,j

def main():
    cases=flips=0
    for q in range(3,9):
        y=no=0
        for bits in product((0,1),repeat=q):
            V,E=graph(bits)
            n,C=mixed_onehot(V,E)
            np,P,a=padded(n,C)
            assert a==18*q+18
            assert np==24*q+27 and len(P)==38*q+39
            assert all(len(c)==3 and len({abs(x) for x in c})==3 for c in P)
            w=ceil(log2(64*(np+len(P)+1)))
            assert (2+4*len(P))*w==(152*q+158)*w
            if sum(bits)%2==0:y+=1
            else:no+=1
            cases+=1
            for i in range(q):
                changed=list(bits);changed[i]^=1
                v2,e2=graph(changed)
                n2,c2=mixed_onehot(v2,e2)
                np2,p2,_=padded(n2,c2)
                differences=[(j,h) for j,(c,d) in enumerate(zip(P,p2))
                             for h,(x,z) in enumerate(zip(c,d)) if x!=z]
                assert np2==np and len(p2)==len(P)
                assert len(differences)==6
                assert (sum(changed)%2)==1-(sum(bits)%2)
                flips+=1
        assert y==no==2**(q-1)
        print(f"q={q} SAT={y} UNSAT={no} vars={24*q+27} exact3={38*q+39}")
    assert cases==504 and flips==3576
    print("proper exactly-three-clause sources",cases,"six-word flips",flips)

if __name__=="__main__":main()
