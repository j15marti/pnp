#!/usr/bin/env python3
"""Standalone independent original-source ARC263 theorem and both-label checker."""
import itertools, collections, json
W=[(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),(5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),(-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),(2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)]
S=list(W);S[9]=(-5,6,-15);S[13]=(-3,-6,-15)

def residual(F,a):
    out=[]
    for C in F:
        if any(abs(z) in a and a[abs(z)]==(z>0) for z in C):continue
        out.append(tuple(z for z in C if abs(z) not in a))
    return out

def check(F):
    n=max(abs(z) for C in F for z in C);m=len(F);assert 3*m==4*n
    assert all(len(C)==3 and len(set(map(abs,C)))==3 for C in F)
    for v in range(1,n+1):
        assert sum(v in C for C in F)==sum(-v in C for C in F)==2
        for truth in (False,True):
            R=residual(F,{v:truth});h=collections.Counter(map(len,R))
            assert (len(R),h[1],h[2],h[3],sum(map(len,R)))==(m-2,0,2,m-4,3*m-8)
    qtotal=0
    for u,v in itertools.combinations(range(1,n+1),2):
        shared=[C for C in F if u in set(map(abs,C)) and v in set(map(abs,C))]
        q=len(shared);qtotal+=q
        outcomes=[]
        for bu,bv in itertools.product((False,True),repeat=2):
            a={u:bu,v:bv};R=residual(F,a);h=collections.Counter(map(len,R))
            ntt=nff=0
            for C in shared:
                signs={abs(z):(z>0) for z in C}
                ntt+=(a[u]==signs[u] and a[v]==signs[v])
                nff+=(a[u]!=signs[u] and a[v]!=signs[v])
            assert (len(R),h[1],h[2],h[3],sum(map(len,R)))==(m-4+ntt,nff,4-q+ntt-nff,m-8+q,3*m-16+q+2*ntt-nff)
            outcomes.append((len(R),h[1],sum(map(len,R))))
        assert sum(x[0] for x in outcomes)==4*(m-4)+q
        assert sum(x[1] for x in outcomes)==q
        assert sum(x[2] for x in outcomes)==12*m-64+5*q
    assert qtotal==3*m
    for j,k in itertools.combinations(range(m),2):
        shared=set(map(abs,F[j]))&set(map(abs,F[k]))
        same=any(next(z for z in F[j] if abs(z)==v)*next(z for z in F[k] if abs(z)==v)>0 for v in shared)
        opp=any(next(z for z in F[j] if abs(z)==v)*next(z for z in F[k] if abs(z)==v)<0 for v in shared)
        for A,B in itertools.product((False,True),repeat=2):
            req=[]
            for choice,C in ((A,F[j]),(B,F[k])):
                req += [(abs(z),(z>0) if choice else (z<0)) for z in C]
            valid=all(not any(v==w and x!=y for w,y in req) for v,x in req)
            assert valid==((not opp) if A==B else (not same))
    count=0
    for bits in itertools.product((False,True),repeat=n):
        if all(any(bits[abs(z)-1]==(z>0) for z in C) for C in F):count+=1
    return {'n':n,'m':m,'pairs':n*(n-1)//2,'models':count}

if __name__=='__main__':
    r={'W1_UNSAT':check(W),'SWAP6_SAT':check(S)}
    assert r['W1_UNSAT']['models']==0 and r['SWAP6_SAT']['models']==54
    print(json.dumps({'status':'PASS','source_specific':r,'general_proof':'See accompanying LaTeX; finite tests do not prove the asymptotic theorem.'},indent=2,sort_keys=True))
