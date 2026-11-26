from prefix import *
from scipy.optimize import linprog
from scipy.sparse import lil_matrix
from extra_audit import word

def contains(d,b,S):
    """Some inclusion-minimal overweight cover contains indices S."""
    for k,(a,w) in enumerate(d):
        M=set(S)|{k}
        if any(d[j][1]<w for j in M):continue
        t=sum(d[j][1] for j in M);lo=max(0,b+1-t);hi=b+w-t
        if hi<lo:continue
        bits=1;mask=(1<<(hi+1))-1
        for j,(z,v) in enumerate(d):
            if j not in M and w<=v<=hi:bits=(bits|(bits<<v))&mask
        if bits>>lo:return True
    return False

def gauge(ds,n):
    """Only pair/triple subclauses needed after half-integral rounding."""
    C=set();probes=0
    for d,b in ds:
        if b<0:return 'NO',None,probes
        if sum(w for a,w in d)<=b:continue
        for k in (2,3):
            for S in it.combinations(range(len(d)),k):
                probes+=1
                if contains(d,b,S):C.add(tuple(sorted(d[i][0]^1 for i in S)))
    C=sorted(C);A=lil_matrix((len(C),n));B=[]
    for j,S in enumerate(C):
        t=1
        for a in S:
            if a%2:A[j,a//2]+=1
            else:A[j,a//2]-=1;t-=1
        B.append(t)
    if not C:g=[1]*n # half value scaled by two
    else:
        lp=linprog([0.]*n,A_ub=A.tocsr(),b_ub=B,bounds=(0,1),method='highs')
        if not lp.success:return 'UNKNOWN',None,probes
        g=[0 if v<.5-1e-8 else 2 if v>.5+1e-8 else 1 for v in lp.x]
    # Exact integer certificate; never use numerical infeasibility as source NO.
    if any(sum(g[a//2] if a%2 else 2-g[a//2] for a in S)>2 for S in C):return 'UNKNOWN',None,probes
    return 'PASS',g,probes

def qsolve(cons,n):
    ds=[norm(c,b) for c,b in cons];lab,g,p=gauge(ds,n);st={'cover_subsets':p}
    if lab!='PASS':return lab,None,st
    H={i for i in range(n) if g[i]!=1};K=set(range(n))-H
    x=[int(v==0) for v in g] # H least model: positive-weight clause literals false
    st.update(horn_vars=len(H),binary_vars=len(K),horn_forced=0)
    # Satisfy H-only minimal covers by restricting weighted literals to H.
    for _ in range(len(H)+1):
        for d,b in ds:
            C=[(a,w) for a,w in d if a//2 in H and x[a//2]==a%2];s=sum(w for a,w in C)
            if s<=b:continue
            rem=[]
            for a,w in C:
                if s-w>b:s-=w
                else:rem.append((a,w))
            heads=[a//2 for a,w in rem if (g[a//2] if (a^1)%2 else 2-g[a//2])==2]
            assert len(heads)<=1
            if not heads:return 'NO',None,st
            i=heads[0];assert x[i]==int(g[i]==0);x[i]^=1;st['horn_forced']+=1;break
        else:break
    else:raise AssertionError('least model')
    # H least model maximizes remaining constraints' slack in all mixed clauses.
    clauses=[]
    for c,b in cons:
        b-=sum(v*x[i] for i,v in c.items() if i in H);cl,exact,ok=threshold({i:v for i,v in c.items() if i in K},b)
        if not ok:return 'NO',None,st
        assert exact
        clauses.extend(cl)
    z=sat2(n,clauses)
    if z is None:return 'NO',None,st
    for i in K:x[i]=z[i]
    assert word(cons,x);return 'YES',x,st

