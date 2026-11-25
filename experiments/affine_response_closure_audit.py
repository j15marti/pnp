#!/usr/bin/env python3
"""Finite audits for affine-response span composition and shift-reachability closure.
All brute-force loops are reference tests or explicitly bounded local kernels.
No claim of a general polynomial SAT algorithm.
"""
from itertools import product, combinations
from collections import deque, Counter
from random import Random
import json, time
from pathlib import Path

rng=Random(20261125)
stat=Counter()

def dot(a,b): return (a&b).bit_count()&1

def red(x,B):
    for p,v in sorted(B.items(),reverse=True):
        if (x>>p)&1: x^=v
    return x

def basis(xs):
    B={}
    for x in xs:
        y=red(x,B)
        if y:B[y.bit_length()-1]=y
    return B

def rank(xs): return len(basis(xs))

def same_span(A,B):
    U=basis(A);V=basis(B)
    return len(U)==len(V) and all(not red(x,V) for x in U.values())

def actual_basis(xs,key=lambda x:x):
    B={};ret=[]
    for x in xs:
        y=red(key(x),B)
        if y: B[y.bit_length()-1]=y;ret.append(x)
    return ret

def solve(eq):
    B={}
    for v,b in eq:
        while v:
            p=v.bit_length()-1
            if p not in B:B[p]=(v,b);break
            w,c=B[p];v^=w;b^=c
        else:
            if b:return None
    x=0
    for p,(v,b) in sorted(B.items()):
        if dot(v,x)!=b:x|=1<<p
    return x

def legal(M,q,x):
    return all(not (x>>i&1) or dot(row,x)==(q>>i&1) for i,row in enumerate(M))

def reps(M,i,q):
    e=1<<i;m=M[i];b=q>>i&1
    return [(e,0),(m,b),(e^m,1^b)]

def choices(M,q):
    return [reps(M,i,q) for i in range(len(M))]

def transversal(groups,protected=()):
    """Deterministic linear/partition matroid intersection, tagged elements.
    Returns actual (owner, local index) pairs; dependent quotient directions ignored.
    """
    stat['matroid_calls']+=1
    B=basis(protected)
    E=[(i,j,red(a,B)) for i,g in enumerate(groups) for j,(a,_) in enumerate(g)]
    I=set();U={};owners=set()
    for k,(i,j,v) in enumerate(E):
        z=red(v,U)
        if i not in owners and z:
            owners.add(i);I.add(k);U[z.bit_length()-1]=z
    def lin(J):return rank(E[j][2] for j in J)==len(J)
    def part(J):return len({E[j][0] for j in J})==len(J)
    while len(I)<len(groups):
        out=[j for j in range(len(E)) if j not in I]
        prev={j:None for j in out if part(I|{j})};Q=deque(prev);end=None
        while Q:
            j=Q.popleft()
            if j not in I and lin(I|{j}):end=j;break
            nxt=([i for i in sorted(I) if lin((I-{i})|{j})] if j not in I
                 else [i for i in out if part((I-{j})|{i})])
            for i in nxt:
                if i not in prev:prev[i]=j;Q.append(i)
        if end is None:break
        while end is not None:I.symmetric_difference_update({end});end=prev[end]
        assert lin(I) and part(I)
        stat['augmentations']+=1
    return [(E[j][0],E[j][1]) for j in sorted(I)]

def response_selector(M,q,x):
    assert legal(M,q,x)
    g=choices(M,q)
    sat_indices=[[j for j,(a,b) in enumerate(row) if dot(a,x)==b] for row in g]
    assert all(len(s)==2 for s in sat_indices)
    G=[[g[i][j] for j in ids] for i,ids in enumerate(sat_indices)]
    sel=transversal(G);assert len(sel)==len(M)
    out=[None]*len(M)
    for i,j in sel:out[i]=sat_indices[i][j]
    return out

def response(M,q,T):
    x=solve([reps(M,i,q)[j] for i,j in enumerate(T)])
    assert x is not None and legal(M,q,x)
    return x

def affine_basis(qs):
    q0=qs[0]
    return [q0]+actual_basis(qs[1:],key=lambda q:q^q0)

def reachable(M,qs):
    R=0
    for q in qs:R|=q^qs[0]
    while True:
        old=R
        for i,row in enumerate(M):
            if row&R:R|=1<<i
        if R==old:return R

def reachable_target(M,qs,ell):
    """Acquire an actual (q,x) with ell*x=1 when ell touches reachable variation."""
    n=len(M);q0=qs[0];Q=affine_basis(qs);D=[q^q0 for q in Q[1:]]
    assert ell&reachable(M,Q)
    G=[]
    for i,row in enumerate(M):
        shift=sum((v>>i&1)<<(n+j) for j,v in enumerate(D))
        G.append([(1<<i,0),(row|shift,q0>>i&1)])
    T=transversal(G,[ell]);assert len(T)==n
    u=solve([(ell,1)]+[G[i][j] for i,j in T]);assert u is not None
    x=u&((1<<n)-1);qstar=q0
    for j,v in enumerate(D):
        if u>>(n+j)&1:qstar^=v
    assert legal(M,qstar,x) and dot(ell,x)==1
    T=response_selector(M,qstar,x)
    for q in Q:
        x=response(M,q,T);stat['response_evaluations']+=1
        if dot(ell,x):
            assert q in qs;stat['target_lifts']+=1;return q,x
    raise AssertionError('affine response failed to lift')

def frozen_reference(M,qs):
    """Brute reference confined to frozen coordinates. Not used in activated large test."""
    n=len(M);R=reachable(M,qs);F=[i for i in range(n) if not(R>>i&1)]
    assert all(not(M[i]&R) for i in F)
    words=[]
    for a in range(1<<len(F)):
        x=sum((a>>j&1)<<i for j,i in enumerate(F))
        if legal(M,qs[0],x):words.append(x)
    return actual_basis(words),R

def acquire(M,qs,frozen_words,R):
    """Extend exact frozen-span basis to exact union basis with actual shift witnesses."""
    n=len(M);pairs=[(qs[0],x) for x in frozen_words]
    B=basis(x for q,x in pairs)
    while True:
        i=next((i for i in range(n) if R>>i&1 and red(1<<i,B)),None)
        if i is None:break
        ell=solve([(v,0) for v in B.values()]+[(1<<i,1)])
        assert ell is not None
        q,x=reachable_target(M,qs,ell)
        y=red(x,B);assert y;B[y.bit_length()-1]=y;pairs.append((q,x))
    assert all(not red(1<<i,B) for i in range(n) if R>>i&1)
    assert all(legal(M,q,x) and q in qs for q,x in pairs)
    return pairs

def test_response():
    for n in (1,2,3,4):
        mats=product(range(1<<n),repeat=n) if n<=3 else (tuple(rng.randrange(1<<n) for _ in range(n)) for _ in range(40))
        for M in mats:
            Ts=[]
            for T in product(range(3),repeat=n):
                if rank(reps(M,i,0)[j][0] for i,j in enumerate(T))==n:Ts.append(T)
            for q in range(1<<n):
                got={response(M,q,T) for T in Ts}
                ref={x for x in range(1<<n) if legal(M,q,x)}
                assert got==ref
                stat['response_set_comparisons']+=1
            # Every bad-shift set is affine or empty, test all nonzero targets.
            for ell in range(1,1<<n):
                bad=[q for q in range(1<<n) if not any(legal(M,q,x) and dot(ell,x) for x in range(1<<n))]
                if bad: assert len(bad)==1<<rank(q^bad[0] for q in bad)
                stat['bad_shift_flat_checks']+=1
            stat['response_geometries']+=1

def test_reachability():
    for _ in range(240):
        n=rng.randrange(1,9)
        M=tuple(rng.randrange(1<<n) if rng.randrange(3) else rng.randrange(1<<(i+1)) for i in range(n))
        qs=rng.sample(range(1<<n),rng.randint(1,min(6,1<<n)))
        F,R=frozen_reference(M,qs)
        ref=actual_basis(x for q in qs for x in range(1<<n) if legal(M,q,x))
        predicted=F+[1<<i for i in range(n) if R>>i&1]
        assert same_span(ref,predicted)
        A=acquire(M,qs,F,R)
        assert same_span(ref,[x for _,x in A])
        stat['reachability_instances']+=1
        stat['reachable_dimensions']+=R.bit_count()
        stat['frozen_dimensions']+=n-R.bit_count()
        stat['reachable_nonempty']+=bool(R)
        stat['reachability_basis_witnesses']+=len(A)

def masks(n,t):
    return [sum(1<<j for j in S) for k in range(min(n,t)+1) for S in combinations(range(n),k)]

def lift(x,ms):return sum(1<<j for j,a in enumerate(ms) if x&a==a)

def lifted_block_basis(M,q,sizes,t):
    prev=[0];off=0
    for k in sizes:
        new=off+k;ms=masks(new,t);cand=[]
        for v in prev:
            for u in range(1<<k):
                w=v|(u<<off)
                if all(not(w>>i&1) or dot(M[i],w)==(q>>i&1) for i in range(off,new)):
                    cand.append(w)
                stat['local_kernel_probes']+=1
        prev=actual_basis(cand,key=lambda x:lift(x,ms));off=new
        assert all(legal(M[:off],q,w) for w in prev)
    return prev

def test_lifted():
    for _ in range(120):
        n=rng.randrange(2,11);sizes=[];z=n
        while z:k=rng.randint(1,min(z,4));sizes.append(k);z-=k
        M=[];off=0
        for k in sizes:
            M += [rng.randrange(1<<(off+k)) for i in range(k)];off+=k
        q=rng.randrange(1<<n);t=rng.randrange(1,5);ms=masks(n,t)
        got=lifted_block_basis(M,q,sizes,t)
        ref=[x for x in range(1<<n) if legal(M,q,x)]
        assert same_span([lift(x,ms) for x in got],[lift(x,ms) for x in ref])
        assert all(x in ref for x in got)
        stat['lifted_block_instances']+=1
        stat['lifted_actual_basis_witnesses']+=len(got)

def closed(M,S): return all(not(M[i]&~S) for i in range(len(M)) if S>>i&1)

def pivot(M,S):
    n=len(M);A=[M[i] if S>>i&1 else 1<<i for i in range(n)]
    if rank(A)<n:return None
    C=[1<<i if S>>i&1 else M[i] for i in range(n)]
    out=[0]*n
    for j in range(n):
        x=solve([(a,int(i==j)) for i,a in enumerate(A)])
        for i,row in enumerate(C):out[i]|=dot(row,x)<<j
    return out

def test_pivot():
    for _ in range(300):
        n=rng.randrange(2,9);M=[rng.randrange(1<<n) for _ in range(n)]
        P=pivot(M,rng.randrange(1<<n))
        if P is None:continue
        for S in range(1<<n):
            assert closed(M,S)==closed(P,S)
            stat['pivot_closed_subset_checks']+=1
        stat['valid_pivots']+=1

def test_large():
    out=[]
    for n in (8,16,32,64):
        # Directed cycle with diagonal ones; at zero shift only 0 and all-ones are legal.
        # A single variable shift at row 0 reaches the entire SCC.
        M=[(1<<i)|(1<<((i+1)%n)) for i in range(n)]
        qs=[0,1];R=reachable(M,qs);assert R==(1<<n)-1
        start=time.monotonic();A=acquire(M,qs,[],R)
        assert rank(x for q,x in A)==n
        assert all(legal(M,q,x) for q,x in A)
        out.append({'dimension':n,'unshifted_span_rank':1,'activated_span_rank':n,'actual_witnesses':len(A),'seconds':round(time.monotonic()-start,4)})
    return out

def test_guard_reduction():
    for _ in range(70):
        n=rng.randrange(3,7);m=rng.randrange(1,6)
        F=[[(i,rng.randrange(2)) for i in rng.sample(range(n),3)] for _ in range(m)]
        # y=(source x, homogenizing t, three selectors per clause).
        # literal x_i xor sign; violation=1+x_i+sign with t fixed 1.
        N=n+1+3*m;t=1<<n;M=[0]*(n+1)
        for C in F:
            for i,s in C:M.append((1<<i)^((1^s)*t))
        assert all(M[i]==0 for i in range(n+1))
        assert all(not(M[i]>>i&1) for i in range(N))
        # Verify existential projection of selector bits independently clause-by-clause.
        for x in range(1<<n):
            sat=all(any((x>>i&1)^s for i,s in C) for C in F)
            allowed=[]
            for j in range(m):
                local=[]
                for z in range(8):
                    if z.bit_count()%2!=1:continue
                    w=x|t|(z<<(n+1+3*j))
                    if legal(M,0,w):local.append(z)
                allowed.append(local)
            assert sat==all(allowed)
            if sat:
                w=x|t|sum(a[0]<<(n+1+3*j) for j,a in enumerate(allowed))
                assert legal(M,0,w)
                assert all(((w>>(n+1+3*j))&7).bit_count()%2==1 for j in range(m))
                stat['guard_lifts']+=1
            stat['guard_source_assignments']+=1
        stat['guard_reductions']+=1

def test_joint_guard_hall():
    for _ in range(180):
        n=rng.randrange(2,8);M=[rng.randrange(1<<n) for i in range(n)]
        D=list(basis(rng.randrange(1<<n) for _ in range(rng.randrange(0,n+1))).values())
        q0=rng.randrange(1<<n);P=list(basis(rng.randrange(1<<n) for _ in range(rng.randrange(0,n+1))).values())
        G=[[(1<<i,0),(row|sum((v>>i&1)<<(n+j) for j,v in enumerate(D)),q0>>i&1)] for i,row in enumerate(M)]
        T=transversal(G,P)
        maxdef=0
        for S in range(1<<n):
            ids=[i for i in range(n) if S>>i&1]
            V=[a for i in ids for a,_ in G[i]]
            leak=rank(G[i][1][0]&~S for i in ids)
            rV=rank(V);assert rV==len(ids)+leak
            inter=rV+len(P)-rank(V+P)
            dd=inter-leak
            maxdef=max(maxdef,dd);stat['joint_guard_cut_checks']+=1
        assert n-len(T)==maxdef
        if len(T)==n:
            stat['joint_guard_Hall_successes']+=1
            for b in range(1<<len(P)):
                v=solve([G[i][j] for i,j in T]+[(p,b>>i&1) for i,p in enumerate(P)])
                assert v is not None
                x=v&((1<<n)-1);q=q0
                for j,w in enumerate(D):
                    if v>>(n+j)&1:q^=w
                assert legal(M,q,x) and all(dot(p,x)==(b>>i&1) for i,p in enumerate(P))
                stat['joint_guard_witnesses']+=1
        stat['joint_guard_instances']+=1

def main():
    start=time.monotonic()
    test_response();print('response',dict(stat),flush=True)
    test_reachability();print('reachability',dict(stat),flush=True)
    test_lifted();print('lifted',dict(stat),flush=True)
    test_pivot();test_guard_reduction();test_joint_guard_hall();print('guards and pivots',dict(stat),flush=True)
    large=test_large()
    res={'seed':20261125,'counts':dict(stat),'large_activated_cycles':large,'seconds':round(time.monotonic()-start,4),'status':'all assertions passed'}
    Path(__file__).with_name('affine_response_closure_results.json').write_text(json.dumps(res,indent=2))
    print(json.dumps(res,indent=2),flush=True)
if __name__=='__main__':main()
