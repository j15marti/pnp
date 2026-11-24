#!/usr/bin/env python3
"""Exact signed NAE syndrome compilation and punctured-subspace closure.
No external dependencies. Test command: python punctured_syndrome.py
All integers are GF(2) bit vectors. Explicit DP is only a small-instance oracle.
"""
import itertools as it
import random, json
from collections import Counter


def reduce_vec(x, B):
    for b in B:
        if x & (1 << (b.bit_length()-1)):
            x ^= b
    return x


def basis(vectors):
    B=[]
    for x in vectors:
        x=reduce_vec(x,B)
        if x:
            B.append(x); B.sort(reverse=True)
    return tuple(B)


def span(B):
    s={0}
    for b in B:
        s |= {x^b for x in s}
    return s


def add(A,B):
    return {a^b for a in A for b in B}


def closure(spaces, target, absorb=()):
    """Spaces represent nonzero choices; absorb represents free linear choices.
    Returns (remaining quotient bases, target, rank of absorbed space, stats).
    No enumeration of a subspace: dimension-one overlap recovered via linear algebra.
    """
    U=basis(absorb); P=[basis(v) for v in spaces]; stats=Counter()
    assert all(P)
    while True:
        new=[]; changed=False
        for V in P:
            Q=basis(reduce_vec(v,U) for v in V)
            if len(Q)<len(V):
                U=basis((*U,*Q)); stats['project_absorb']+=1; changed=True
            else:
                new.append(Q)
        P=new
        target=reduce_vec(target,U)
        if changed: continue
        # Remaining bases are in one common quotient coordinate system.
        pair=None
        for i,j in it.combinations(range(len(P)),2):
            W=basis((*P[i],*P[j])); d=len(P[i])+len(P[j])-len(W)
            if d:
                pair=(i,j,W,d); break
        if pair is None:
            return P,target,len(U),dict(stats)
        i,j,W,d=pair; V1,V2=P[i],P[j]
        if d==1:
            # Null relation among columns of the two bases; recover intersection.
            piv=[]; witnesses=[]; h=None
            for k,v in enumerate((*V1,*V2)):
                a=v; mask=1<<k
                for b,m in zip(piv,witnesses):
                    if a & (1<<(b.bit_length()-1)):
                        a^=b;mask^=m
                if not a:
                    h=0
                    for z,b in enumerate(V1):
                        if mask>>z&1:h^=b
                    break
                pairs=sorted(zip(piv+[a],witnesses+[mask]),reverse=True)
                piv,witnesses=map(list,zip(*pairs))
            assert h
            target^=h; stats['punctured_fuse']+=1
            P=[v for k,v in enumerate(P) if k not in (i,j)]+[W]
        else:
            U=basis((*U,*W));stats['pair_absorb']+=1
            P=[v for k,v in enumerate(P) if k not in (i,j)]


def dp(spaces,target,absorb=()):
    S=span(absorb)
    for V in spaces:
        S=add(S,span(V)-{0})
    return target in S


def compile_nae(n, clauses):
    """Incidence cycle-basis columns. Clause entries are (variable, negation bit)."""
    m=len(clauses); adj=[[] for _ in range(n+m)]; edges=[]; signs=[]
    for j, C in enumerate(clauses):
        assert len(C)==3 and len({v for v,s in C})==3
        for v,s in C:
            e=len(edges);w=n+j;edges.append((v,w));signs.append(s)
            adj[v].append((w,e));adj[w].append((v,e))
    paths={};tree=set();components=0
    for v in range(n+m):
        if v in paths:continue
        components+=1;paths[v]=0;stack=[v]
        while stack:
            u=stack.pop()
            for w,e in adj[u]:
                if w not in paths:
                    paths[w]=paths[u]^(1<<e);tree.add(e);stack.append(w)
    cycles=[paths[v]^paths[w]^(1<<e) for e,(v,w) in enumerate(edges) if e not in tree]
    assert len(cycles)==2*m-n+components
    cols=[sum(((c>>e)&1)<<j for j,c in enumerate(cycles)) for e in range(3*m)]
    target=0; P=[]; U=[]
    for e,s in enumerate(signs):
        if s:target^=cols[e]
    for j in range(m):
        a,b,c=cols[3*j:3*j+3];assert a^b^c==0
        V=basis((a,b,c))
        if len(V)<2:U.extend(V)
        else:P.append(V)
    return P,target,basis(U),len(cycles)


def brute_nae(n,C):
    return any(all(0<sum(x[v]^s for v,s in c)<3 for c in C) for x in it.product(range(2),repeat=n))


def run():
    rng=random.Random(20261124);out={};cnt=Counter()
    # Direct verification of pair theorem with independent explicit sums.
    for _ in range(1500):
        n=rng.randint(1,8);V=basis(rng.randrange(1<<n) for _ in range(rng.randint(1,n)));W=basis(rng.randrange(1<<n) for _ in range(rng.randint(1,n)))
        if not V or not W:continue
        A,B=span(V),span(W);S=add(A-{0},B-{0});I=A&B;d=len(I).bit_length()-1
        if d==1:assert S==(add(A,B)-{next(iter(I-{0}))})
        elif d>=2:assert S==add(A,B)
        else:assert len(S)==(len(A)-1)*(len(B)-1)
        cnt[f'intersection_{min(d,2)}']+=1
    out['pair_tests']=dict(cnt);cnt=Counter()
    for _ in range(500):
        n=rng.randint(3,8);m=rng.randint(1,10)
        C=[[(v,rng.randrange(2)) for v in rng.sample(range(n),3)] for _ in range(m)]
        P,t,U,r=compile_nae(n,C);Q,t2,u,st=closure(P,t,U)
        truth=brute_nae(n,C);got=dp(Q,t2)
        assert got==truth,(n,C,P,t,U,Q,t2)
        cnt['SAT' if truth else 'UNSAT']+=1;cnt['closed' if not Q else 'residual']+=1
        for k,v in st.items():cnt[k]+=v
    out['random_nae']=dict(cnt)
    # All 3-regular bipartite incidence circulants of this form stagnate under these rules.
    out['circulant_stagnation']=[]
    for n in (4,8,16,32,64,128):
        C=[[(i,0),((i+1)%n,0),((i+2)%n,0)] for i in range(n)]
        P,t,U,r=compile_nae(n,C);Q,t2,u,st=closure(P,t,U)
        assert not st and len(Q)==n and r==n+1 and not U
        assert all(0<sum(v%2 for v,s in c)<3 for c in C)
        out['circulant_stagnation'].append(dict(clauses=n,rank=r,remaining=len(Q)))
    # Degree-two variables: clauses correspond to vertices of a cubic prism graph.
    out['degree_two_prisms']=[]
    for k in (3,4,8,16,32,64):
        es=[(i,(i+1)%k) for i in range(k)]+[(k+i,k+(i+1)%k) for i in range(k)]+[(i,i+k) for i in range(k)]
        C=[[] for _ in range(2*k)]
        for v,(a,b) in enumerate(es):C[a].append((v,rng.randrange(2)));C[b].append((v,rng.randrange(2)))
        P,t,U,r=compile_nae(len(es),C);Q,t2,u,st=closure(P,t,U)
        assert not Q and not t2 and u==r
        out['degree_two_prisms'].append(dict(clauses=2*k,rank=r,absorbed=u,**st))
    fano=[(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
    out['fano_controls']=[]
    for C0 in [fano]+[fano[:i]+fano[i+1:] for i in range(7)]:
        C=[[(v,0) for v in c] for c in C0];P,t,U,r=compile_nae(7,C);Q,t2,u,st=closure(P,t,U);got=dp(Q,t2)
        assert got==brute_nae(7,C)
        out['fano_controls'].append(dict(clauses=len(C),rank=r,absorbed=u,remaining=len(Q),sat=got,**st))
    print(json.dumps(out,indent=2));return out


if __name__=='__main__':run()
