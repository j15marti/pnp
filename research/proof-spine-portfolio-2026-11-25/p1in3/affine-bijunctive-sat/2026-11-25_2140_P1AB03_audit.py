import itertools as it, json, random, hashlib
import numpy as np
import networkx as nx
from collections import Counter
C=[(0,1,6),(0,1,3),(1,3,6),(2,3,4),(2,4,5),(0,4,5),(2,10,11),(7,8,9),(8,9,10),(8,12,13),(9,10,11),(5,7,11),(6,7,17),(12,13,14),(13,14,15),(14,15,16),(15,16,17),(12,16,17)]
U=C.copy(); U[4]=(2,5,6); U[12]=(7,17,4)
K=Counter(); rng=random.Random(20261125)
def source(k,bad=False):
    c=[tuple(v+18*j for v in r) for j in range(k) for r in (U if bad and j==k//2 else C)]
    for j in range(k-1):
        a,b=18*j+7,18*(j+1)+9; x,y=18*j+7,18*(j+1)+12
        c[a]=tuple(y if v==x else v for v in c[a]); c[b]=tuple(x if v==y else v for v in c[b])
    n=len(c); G=nx.Graph(); G.add_nodes_from(range(2*n)); G.add_edges_from((v,n+i) for i,r in enumerate(c) for v in r)
    assert all(len(set(r))==3 for r in c) and all(d==3 for _,d in G.degree()) and nx.is_connected(G)
    planar,emb=nx.check_planarity(G); assert planar; emb.check_structure(); K['planarity']+=1
    return c
def mat(c):
    n=len(c); A=np.zeros((n,n+1),dtype=np.int64)
    for i,r in enumerate(c): A[i,list(r)]=1; A[i,n]=1
    return A
def gauss(M,p):
    K['gauss'+str(p)]+=1; M=np.array(M,dtype=np.int64)%p; n=M.shape[1]-1; r=0; piv=[]
    for i in range(n):
        j=next((j for j in range(r,len(M)) if M[j,i]),None)
        if j is None: continue
        M[[r,j]]=M[[j,r]]; M[r]=M[r]*pow(int(M[r,i]),-1,p)%p
        a=M[:,i].copy(); a[r]=0; M=(M-a[:,None]*M[r])%p; piv.append(i); r+=1
    if any(M[r:,-1]): return None
    F=[i for i in range(n) if i not in piv]; a=np.zeros(n,dtype=np.int64); D=np.zeros((n,len(F)),dtype=np.int64)
    for j,i in enumerate(F): D[i,j]=1
    for j,i in enumerate(piv): a[i]=M[j,-1]; D[i]=-M[j,F]%p
    return a,D,F
def augmented(A,pins,G=()):
    n=len(A); P=[]
    for i,v in pins.items():
        r=[0]*(n+1); r[i]=1; r[-1]=v; P.append(r)
    return np.vstack([A]+[np.array(x) for x in (P,G) if len(x)])
def basic(c,A,pins,G):
    n=len(c)
    while True:
        old=len(pins)
        def pin(i,v):
            if i in pins: return pins[i]==v
            pins[i]=v; K['pins']+=1; return True
        for r in c:
            t=sum(pins.get(i)==1 for i in r); f=[i for i in r if i not in pins]
            if t>1 or (not t and not f): return None
            if t or len(f)==1:
                for i in f:
                    if not pin(i,0 if t else 1): return None
        Q2=gauss(augmented(A,pins,G),2); Q3=gauss(augmented(A,pins),3)
        if Q2 is None or Q3 is None: return None
        for a,D,F in (Q2,Q3):
            for i in range(n):
                if not any(D[i]) and (a[i]==2 or not pin(i,int(a[i]))): return None
        a,D,F=Q3; groups={}
        for i,d in enumerate(D):
            j=next((j for j,v in enumerate(d) if v),None)
            if j is None: continue
            q=int(d[j]); key=tuple(d*q%3); allowed,L=groups.setdefault(key,(set(range(3)),[]))
            allowed.discard((2-int(a[i]))*q%3); L.append((i,q))
        for allowed,L in groups.values():
            if not allowed: return None
            if len(allowed)==1:
                t=next(iter(allowed))
                for i,q in L:
                    if not pin(i,(int(a[i])+q*t)%3): return None
        if len(pins)>old: continue
        H=nx.Graph(); left=[('c',i) for i,r in enumerate(c) if not any(pins.get(j)==1 for j in r)]; H.add_nodes_from(left)
        for _,i in left: H.add_edges_from((('c',i),('v',j,k)) for j in c[i] if j not in pins for k in range(3))
        K['matching']+=1
        if len(nx.algorithms.bipartite.maximum_matching(H,top_nodes=left))!=2*len(left): return None
        return Q3
def close(c,A,pins,G):
    while True:
        q=basic(c,A,pins,G)
        if q is None: return None
        for i in range(len(c)):
            if i in pins: continue
            bad=[]
            for v in (0,1):
                K['probes']+=1
                if basic(c,A,{**pins,i:v},G) is None: bad.append(v)
            if len(bad)==2: return None
            if bad: pins[i]=1-bad[0]; break
        else: return q
def cover(S,cap):
    def rec(B,k):
        K['search']+=1; a=next((s-B for s in S if len(s-B)>2),None)
        if a is None: return B
        if not k: return None
        for i in sorted(a)[:3]:
            z=rec(B|{i},k-1)
            if z is not None: return z
        return None
    for k in range(cap+1):
        z=rec(set(),k)
        if z is not None: return z
    return None
def sat2(d,F):
    K['sat2']+=1; E=nx.DiGraph(); E.add_nodes_from(range(2*d))
    for c in F:
        if not c: return None
        a=c[0]; b=c[-1]; E.add_edge(a^1,b); E.add_edge(b^1,a)
    R=[nx.descendants(E,i)|{i} for i in range(2*d)]
    if any((2*i+1 in R[2*i] and 2*i in R[2*i+1]) for i in range(d)): return None
    H=set()
    for i in range(d):
        if 2*i in H or 2*i+1 in H: continue
        for v in (2*i,2*i+1):
            Z=H|R[v]
            if all((x^1) not in Z for x in Z): H=Z; break
        else: raise AssertionError('2SAT extension')
    x=tuple(int(2*i+1 in H) for i in range(d)); assert all(any(x[l//2]==l%2 for l in c) for c in F)
    return x,R
def guardok(y,G): return all(sum(int(v)*int(w) for v,w in zip(r[:-1],y))%2==r[-1] for r in G)
def seed_search(sol,h,accept):
    x,R=sol; d=len(x)
    for k in range(min(h,d)+1):
        for seed in it.combinations(range(d),k):
            K['seedWords']+=1; H=set().union(*(R[2*i+1-x[i]] for i in seed))
            if any((v^1) in H for v in H): continue
            y=tuple(1-v if 2*i+1-v in H else v for i,v in enumerate(x))
            if accept(y): return y
    return None
def terminal(q,G,cap):
    a,D,F=q; d=len(F); S=[set(np.flatnonzero(r).tolist()) for r in D]; B=cover(S,cap)
    if B is None: return 'UNKNOWN',None,None,d
    B=sorted(B); J=[i for i in range(d) if i not in B]; idx={v:i for i,v in enumerate(J)}
    for w in it.product((0,1),repeat=len(B)):
        K['fibers']+=1; z=np.zeros(d,dtype=np.int64); z[B]=w; b=(a+D@z)%3; clauses=[]
        for i,s in enumerate(S):
            L=sorted(s-set(B)); assert len(L)<=2
            for u in it.product((0,1),repeat=len(L)):
                if (int(b[i])+sum(int(D[i,j])*v for j,v in zip(L,u)))%3==2: clauses.append(tuple(2*idx[j]+1-v for j,v in zip(L,u)))
        sol=sat2(len(J),clauses)
        if sol is None: continue
        def lift(x):
            z[J]=x; y=(a+D@z)%3; assert all(y<2); return y
        x=seed_search(sol,2*len(G),lambda x:guardok(lift(x),G)) if len(G) else sol[0]
        if x is not None:
            K['lifts']+=1; return 'SAT',lift(x),len(B),d
    return 'UNSAT',None,len(B),d
def solve(c,G=(),pins=None,cap=4):
    A=mat(c); pins={} if pins is None else dict(pins); q=close(c,A,pins,G)
    if q is None: return 'UNSAT',None,None,None
    r=terminal(q,G,cap)
    if r[1] is not None:
        y=r[1]; assert all(sum(y[list(t)])==1 for t in c) and guardok(y,G) and all(y[i]==v for i,v in pins.items())
    return r
def ref(c,G,pins):
    q=gauss(augmented(mat(c),pins,G),2)
    if q is None: return False
    a,D,F=q; assert len(F)<=16
    for z in it.product((0,1),repeat=len(F)):
        y=(a+D@np.array(z,dtype=np.int64))%2
        if all(sum(y[list(t)])==1 for t in c) and guardok(y,G): return True
    return False
def guards(n,k): return [[rng.randrange(2) for _ in range(n+1)] for _ in range(k)]
def seam_chart(q,J):
    a,D,F=q; d=len(F); assert len(J)==d
    M=np.hstack([D[J],np.eye(d,dtype=np.int64)])%3
    for i in range(d):
        j=next(j for j in range(i,d) if M[j,i]); M[[i,j]]=M[[j,i]]; M[i]=M[i]*pow(int(M[i,i]),-1,3)%3
        f=M[:,i].copy(); f[i]=0; M=(M-f[:,None]*M[i])%3
    E=D@M[:,d:]%3; b=(a-E@a[J])%3
    assert np.array_equal(E[J],np.eye(d,dtype=np.int64)) and not any(b[J])
    return b,E,J

def audit():
    cases=[]
    for k in (1,3,5):
        for bad in (False,True):
            c=source(k,bad); label,y,b,d=solve(c); expect='UNSAT' if bad else 'SAT'; assert label in (expect,'UNKNOWN')
            R=dict(n=len(c),bad=bad,status=label,b=b,d=d)
            if not bad and k>1 and y is not None:
                j=k//2; seq=[38034]*j+[260370]+[149778]*j; s=np.array([(w>>i)&1 for w in seq for i in range(18)])
                assert all(sum(s[list(t)])%2==1 for t in c) and sum(sum(s[list(t)])==3 for t in c)==6
                R['repair']=int(sum(s!=y))
            cases.append(R)
    jobs=Counter()
    for bad in (False,True):
        c=source(1,bad)
        for j in range(40):
            G=guards(len(c),1+j%2); pins={rng.randrange(len(c)):rng.randrange(2)} if j%3==0 else {}
            expect=ref(c,G,pins); label,*_=solve(c,G,pins); assert label=='UNKNOWN' or (label=='SAT')==expect
            jobs['guard_jobs']+=1; jobs['guard_sat' if expect else 'guard_unsat']+=1; jobs['guard_'+label]+=1
    for j in range(200):
        d=rng.randrange(2,7); D=np.vstack([np.eye(d,dtype=np.int64),np.array([[rng.randrange(3) for _ in range(d)] for _ in range(5)])]); a=np.array([0]*d+[rng.randrange(3) for _ in range(5)]); q=(a,D,list(range(d))); G=guards(len(a),j%3)
        actual=any(all(y<2) and guardok(y,G) for y in ((a+D@np.array(z))%3 for z in it.product((0,1),repeat=d)))
        label,y,b,_=terminal(q,G,d); assert (label=='SAT')==actual
        jobs['chart_jobs']+=1; jobs['chart_positive_b']+=b>0; jobs['chart_unsat']+=not actual
    seams=[]
    for k in (1,3,5,9,17):
        c=source(k); p={}; q=basic(c,mat(c),p,[]); a,D,F=q; J=[12]+[18*j+7 for j in range(k)]
        R=seam_chart(q,J); label,y,b,d=terminal(R,[],0); assert label=='SAT' and all(sum(y[list(t)])==1 for t in c)
        assert max(np.count_nonzero(R[1],axis=1))<=2 and max(np.count_nonzero(D,axis=1))==k+1
        seams.append(dict(n=len(c),raw_max_support=k+1,raw_backdoor_lower_bound=k-1,seam_max_support=int(max(np.count_nonzero(R[1],axis=1))),b=b,pins=len(p)))
    return dict(seed=20261125,counts=dict(K),cases=cases,jobs=dict(jobs),seams=seams)
if __name__=='__main__': print(json.dumps(audit(),indent=2))
