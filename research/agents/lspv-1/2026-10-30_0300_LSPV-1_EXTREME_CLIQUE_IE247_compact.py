#!/usr/bin/env python3
"""Standalone original-source extreme-cube IE certificate, Python stdlib.
This is a compact independently runnable version of the expanded producer.
The literal +/- integer is a sign-aware occurrence of ONE global variable.
"""
from itertools import combinations
W1=[(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
(5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),(-2,-6,12),
(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),(2,-9,11),
(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)]
V=list(W1);V[9]=(-5,6,-15);V[13]=(-3,-6,-15)

def clause_targets(C):
    S={abs(l):int(l>0) for l in C}
    U={x:1-v for x,v in S.items()}
    return {'S':S,'invert_S_U':U,'U':U,'invert_U_S':S}

def mode_pair(A,B):
    a=clause_targets(A)['S']; b=clause_targets(B)['S']; same=[];opp=[]
    for x in a.keys()&b.keys():
        (same if a[x]==b[x] else opp).append(x)
    return {'same':same,'opposite':opp,'SS':not opp,'SU':not same,'US':not same,'UU':not opp}

def restrict(F,pins):
    R=[]
    for C in F:
        if any(abs(l) in pins and pins[abs(l)]==int(l>0) for l in C):continue
        residual=tuple(l for l in C if abs(l) not in pins)
        if not residual:return None
        R.append(residual)
    return R

def ie(F,n,pins):
    R=restrict(F,pins);u=n-len(pins)
    if R is None:return 0,[0],0
    support=[sum(1<<(abs(l)-1) for l in C) for C in R]
    demand=[sum(1<<(abs(l)-1) for l in C if l<0) for C in R]
    conflict=[0]*len(R)
    for j,k in combinations(range(len(R)),2):
        if (demand[j]^demand[k])&(support[j]&support[k]):
            conflict[j]|=1<<k; conflict[k]|=1<<j
    A=[0]*(len(R)+1);A[0]=1<<u;subsets=0
    def dfs(remaining,vars_used,depth):
        nonlocal subsets
        while remaining:
            bit=remaining&-remaining;j=bit.bit_length()-1;remaining-=bit
            vnew=vars_used|support[j]
            A[depth+1]+=1<<(u-vnew.bit_count());subsets+=1
            dfs(remaining&~conflict[j],vnew,depth+1)
    dfs((1<<len(R))-1,0,0)
    return sum((-1 if i&1 else 1)*v for i,v in enumerate(A)),A,subsets

def models(F,n):
    return [a for a in range(1<<n) if all(any(bool(a&(1<<(abs(l)-1)))==(l>0) for l in C) for C in F)]

def counts(F,n,a):
    t=[sum(int(bool(a&(1<<(abs(l)-1)))==(l>0)) for l in C) for C in F]
    return t,[t.count(i) for i in range(4)]

def unit_refute(F,pins):
    a=dict(pins)
    while True:
        changed=False
        for C in F:
            if any(abs(l) in a and a[abs(l)]==int(l>0) for l in C):continue
            rem=[l for l in C if abs(l) not in a]
            if not rem:return True
            if len(rem)==1:
                a[abs(rem[0])]=int(rem[0]>0);changed=True;break
        if not changed:return False

def verify():
    n=15;src=V
    for F in (W1,V):
        assert len(F)==20 and all(len(C)==3 and len(set(map(abs,C)))==3 for C in F)
        assert all(sum(l==v for C in F for l in C)==2 and
                   sum(l==-v for C in F for l in C)==2 for v in range(1,n+1))
        for C in F:
            T=clause_targets(C)
            assert T['invert_S_U']==T['U'] and T['invert_U_S']==T['S']
        for j,k in combinations(range(len(F)),2):
            p=mode_pair(F[j],F[k])
            for mode in ('SS','SU','US','UU'):
                ta=clause_targets(F[j])[mode[0]];tb=clause_targets(F[k])[mode[1]]
                compatible=all(x not in tb or tb[x]==v for x,v in ta.items())
                assert p[mode]==compatible,(j,k,mode)
        _,nh0=counts(F,n,0);_,nh1=counts(F,n,(1<<n)-1)
        assert nh0==[1,10,7,2] and nh1==[2,7,10,1]
    assert not models(W1,n)
    assert len(models(V,n))==54 and 19186 in models(V,n)
    assert ie(V,n,{2:0})==(0,[16384,40960,36608,14336,2452,148]+[0]*13,542)
    assert ie(V,n,{2:1})[0]==54
    assert not unit_refute(V,{2:0})
    # Coherent global flip trail and its bitwise complement (all source clauses).
    mask=0
    for v in [1,3,2,5,7,1,2]:
        mask^=1<<(v-1)
        t0,h0=counts(V,n,mask);t1,h1=counts(V,n,mask^((1<<n)-1))
        assert all(a+b==3 for a,b in zip(t0,t1)) and h1==list(reversed(h0))
    print('PASS: original targets, all 190 clause pairs, both endpoints, coherent flips')
    print('W1 UNSAT model count=0; SWAP6 SAT model count=54')
    print('SWAP6 pin x2=0 IE coefficients [16384,40960,36608,14336,2452,148]')
    print('Total=0, 542 compatible subsets; source UP does not refute; hence SWAP6 entails x2')
if __name__=='__main__': verify()
