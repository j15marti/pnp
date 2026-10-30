#!/usr/bin/env python3
"""Independent stdlib replay: LSPV-1 EXTREME-LOCAL-SUPPORT249 (source-specific).
No SAT oracle, external libraries or producer imports. Full raw and charged
DPLL producer live in EXTREME_LOCAL_SUPPORT249_REPRO_BUNDLE.zip."""
from itertools import combinations
W1=[(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
(5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),(-2,-6,12),
(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),(2,-9,11),
(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)]
SW=list(W1); SW[9]=(-5,6,-15); SW[13]=(-3,-6,-15)
OMIT={1:0,3:8209,4:608,5:10245,6:24597,7:0,8:608,
      9:616,10:96,11:840,12:8213,13:0,14:1,15:8213}
def true(C,a):
    return any(((a>>(abs(l)-1))&1)==int(l>0) for l in C)
def count(F,a):
    t=[sum(((a>>(abs(l)-1))&1)==int(l>0) for l in C) for C in F]
    return t,tuple(t.count(j) for j in range(4))
def targets(C):
    S={abs(l):int(l>0) for l in C}
    U={i:1-v for i,v in S.items()}
    return S,U
def pair(C,D):
    common={abs(l) for l in C}&{abs(l) for l in D}
    same={v for v in common if (v in C)==(v in D)}
    opp=common-same
    return (not opp,not same,not same,not opp)
def modes(F):
    checks=0
    for j,k in combinations(range(len(F)),2):
        A=F[j]; B=F[k]; S,U=targets(A); T,V=targets(B)
        for expected,X,Y in zip(pair(A,B),(S,S,U,U),(T,V,T,V)):
            actual=all(i not in Y or Y[i]==v for i,v in X.items())
            assert actual==expected,(j,k)
            checks+=1
    return checks
def supports_omission(F,pin,omission):
    assert pin.get(2,0)==0
    for v,mask in omission.items():
        assert (mask>>1)&1==0
        for C in F:
            if any(abs(l) in pin and pin[abs(l)]==int(l>0) for l in C):continue
            if v in [abs(l) for l in C if abs(l) not in pin]:continue
            assert true(C,mask),(v,mask,C)
def all_models(F,pin={}):
    return [a for a in range(1<<15)
            if all((a>>(i-1))&1==b for i,b in pin.items())
            and all(true(C,a) for C in F)]
def audit():
    assert all(len(set(map(abs,C)))==3 for C in W1)
    for F in (W1,SW):
        for i in range(1,16):
            assert sum(l==i for C in F for l in C)==2
            assert sum(l==-i for C in F for l in C)==2
        for C in F:
            S,U=targets(C)
            assert all(U[i]==1-S[i] for i in S)
        assert modes(F)==760
        assert count(F,0)[1]==(1,10,7,2)
        assert count(F,(1<<15)-1)[1]==(2,7,10,1)
        for mask in (0,1,5,70,127,17609,32767):
            x,_=count(F,mask);y,_=count(F,mask^32767)
            assert all(a+b==3 for a,b in zip(x,y))
    assert len(all_models(W1))==0
    assert len(all_models(SW))==54
    assert not all_models(SW,{2:0})
    supports_omission(SW,{2:0},OMIT)
    # The source-authenticated parent resolvent C0,C19, pivot x14.
    assert -14 in W1[0] and 14 in W1[19]
    R=set(W1[0]+W1[19])-{14,-14}
    assert R=={-1,3,13}
    for a in range(1<<15):
        if (a&1) and not (a&4) and not (a&(1<<12)):
            assert not (true(W1[0],a) and true(W1[19],a))
    # Hostile inconsistent XOR cycle: all proper vertex-deleted subformulas SAT.
    for k in (3,7,11):
        Q=[]
        for j in range(k):
            x=j+1;y=(j+1)%k+1
            Q.extend(((x,y),(-x,-y)) if j==k-1 else ((-x,y),(x,-y)))
        assert not any(all(true(C,a) for C in Q) for a in range(1<<k))
        for omit in range(1,k+1):
            R=[C for C in Q if omit not in [abs(z) for z in C]]
            assert any(all(true(C,a) for C in R) for a in range(1<<k))
    print("PASS original S/U targets and 1520 indexed four-mode checks")
    print("PASS endpoints, complete complements, source-parent forbidden cube")
    print("PASS W1 UNSAT, SWAP6 54 SAT, x2=0 UNSAT, 14 omission witnesses")
    print("PASS XOR k=3,7,11 essential-support hostile controls")
if __name__=="__main__":
    audit()
