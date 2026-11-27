import itertools as it, json, hashlib, math
T=[(2,4,6),(3,7,8),(1,2,3),(5,6,7),(1,2,5),(2,3,7),(2,5,8),(0,3,7),(6,7,8),(0,3,6),(4,5,8),(1,4,8)]
rows=[[j for j,t in enumerate(T) if e in t] for e in range(9)]
def rref(eqs):
    D={}
    for u,b in eqs:
        while u:
            p=u.bit_length()-1
            if p not in D: D[p]=(u,b); break
            v,c=D[p];u^=v;b^=c
        if not u and b:return None
    return D
def reduce(u,D):
    b=0
    for p,(v,c) in sorted(D.items(),reverse=True):
        if u>>p&1:u^=v;b^=c
    return u,b
def basis(vs):return [v for v,b in rref((v,0) for v in vs).values()]
def inter(A,B):
    D=rref((v,0) for v in B); E={}; out=[]
    for a in A:
        u=reduce(a,D)[0]; v=a
        while u:
            p=u.bit_length()-1
            if p not in E:E[p]=(u,v);break
            x,y=E[p];u^=x;v^=y
        if not u:out.append(v)
    return basis(out)
def bit(u,z):return (u&z).bit_count()%2
# independently acquire affine chart by Gaussian elimination of original equations
D=rref((sum(1<<j for j in r),1) for r in rows);free=[i for i in range(12) if i not in D]
def lift(z):
    x=sum((z>>i&1)<<j for i,j in enumerate(free))
    for p,(v,b) in sorted(D.items()):x|=(b^bit(v,x))<<p
    return x
a=lift(0); V=[lift(1<<i)^a for i in range(len(free))]; B=[sum(((v>>j)&1)<<i for i,v in enumerate(V)) for j in range(12)]
assert len(V)==3
A={lift(z) for z in range(8)}
assert A=={x for x in range(4096) if all(sum(x>>j&1 for j in r)%2==1 for r in rows)}
# factor construction from local literal products, no global enumeration
def mul(P,Q):
    C={}
    for u,c in P.items():
        for v,b in Q.items():C[u^v]=(C.get(u^v,0)+c*b)%3
    return {u:c for u,c in C.items() if c}
def add(P,Q):
    C=P.copy()
    for u,c in Q.items():C[u]=(C.get(u,0)+c)%3
    return {u:c for u,c in C.items() if c}
X=[]
for j,u in enumerate(B):X.append(add({0:2},{u: -2*(-1)**(a>>j&1)%3}))
F=[]
for r in rows:
    f={}
    for j in r:
        p=X[j]
        for l in r:
            if l!=j:p=mul(p,add({0:1},{u:-c%3 for u,c in X[l].items()}))
        f=add(f,p)
    F.append(f)
    for z in range(8):assert sum(c*(-1)**bit(u,z) for u,c in f.items())%3==int(sum(lift(z)>>j&1 for j in r)==1)
assert not any(all(sum(x>>j&1 for j in r)==1 for r in rows) for x in range(4096))

def instance(k):
    order=[(j,e) for j in range(k) for e in range(4)]+[(j,e) for j in range(k) for e in range(4,9)]
    return [{u<<(3*j):c for u,c in F[e].items()} for j,e in order],order

def layout(fs):
    U=[basis(f) for f in fs];L=[[]];R=[[] for _ in range(len(fs)+1)]
    for u in U:L.append(basis(L[-1]+u))
    for i in reversed(range(len(U))):R[i]=basis(U[i]+R[i+1])
    return [inter(l,r) for l,r in zip(L,R)]
CAP=100000
class Stop(Exception):pass
class Meter:
    def __init__(self):self.calls=0;self.terms=0
    def check(self,f,eqs):
        if self.calls>=CAP:raise Stop
        self.calls+=1; D=rref(eqs)
        if D is None:return False
        C={}
        for u,c in f.items():
            self.terms+=1;v,b=reduce(u,D);C[v]=(C.get(v,0)+c*(-1)**b)%3
        return any(C.values())
def keys(W,k):return [(u,k>>i&1) for i,u in enumerate(W)]
def enumerate_keys(f,eqs,W,m):
    out=[];stack=[(0,0)]
    while stack:
        h,k=stack.pop()
        if not m.check(f,eqs+keys(W[:h],k)):continue
        if h==len(W):out.append(k)
        else:stack.extend([(h+1,k),(h+1,k|(1<<h))])
    return out

def run(fs,W,dense):
    m=Meter();K={0};maxK=1;maxb=0;stages=0
    try:
        for i,f in enumerate(fs):
            J=set();maxb=max(maxb,len(W[i+1]));stages+=1
            for a0 in K:
                eqs=keys(W[i],a0)
                if dense:
                    for b0 in range(1<<len(W[i+1])):
                        if m.check(f,eqs+keys(W[i+1],b0)):J.add(b0)
                else:J.update(enumerate_keys(f,eqs,W[i+1],m))
            K=J;maxK=max(maxK,len(K))
            if not K:break
        status='UNSAT' if not K else 'FEASIBLE'
    except Stop:status='UNKNOWN'
    return dict(status=status,calls=m.calls,terms=m.terms,max_keys=maxK,max_rank=maxb,stages=stages)
# direct tree contraction: each copy is separate in frequency space, hence zero interface to others.
# each local factor table built by exact 8-point reference, merged by pointwise conjunction.
def tree(k):
    calls=0
    for j in range(k):
        good=set(range(8))
        for f in F:
            g=set()
            for z in range(8):
                calls+=1
                if sum(c*(-1)**bit(u,z) for u,c in f.items())%3:g.add(z)
            good &= g
        if not good:return {'status':'UNSAT','point_tests':calls,'local_rank':3}
    return {'status':'FEASIBLE','point_tests':calls,'local_rank':3}
# source adapter, exact arc IDs from L01-22, no dense mask emitted

def native(k):
    triples=[tuple(e+9*j for e in t) for j in range(k) for t in T];m=9*k;t=len(triples)
    occ=[[] for _ in range(m)]
    for j,tt in enumerate(triples):
        for e in tt:occ[e].append(j)
    centers=[];leaves=[[] for _ in range(t)];s=0
    for e,js in enumerate(occ):
        r=len(js); centers.append((s,s+r+1))
        for h,j in enumerate(js):leaves[j].extend([s+1+h,s+2*r+1-h])
        s+=2*(r+1)
    def swaps(pairs):
        p=list(range(s))
        for i,j in pairs:p[i]=j;p[j]=i
        return p
    c=swaps(centers);p=[(c[i]+1)%s for i in range(s)];kk=swaps([tuple(l[i:i+2]) for l in leaves for i in range(0,6,2)])
    g=list(range(s))
    for l in leaves:
        for i,j in zip(l,l[1:]+l[:1]):g[i]=j
    arcs=set()
    for i in range(s):
        u=s+2*i;v=u+1;arcs.update([(i,u),(u,v),(v,p[i])])
        if g[i]!=i:arcs.update([(g[i],v),(v,u),(u,p[kk[g[i]]])])
    n=3*s;assert len(arcs)==486*k and n==270*k
    def reach(rev):
        adj=[[] for _ in range(n)]
        for u,v in arcs:adj[v if rev else u].append(u if rev else v)
        seen={0};st=[0]
        while st:
            for v in adj[st.pop()]:
                if v not in seen:seen.add(v);st.append(v)
        return len(seen)
    assert reach(False)==reach(True)==n
    # all phase words lift in saturated regions. For source support use baseline odd/even parity and paired toggles.
    phase_id={i:j for j,l in enumerate(leaves) for i in l}
    def perm(x):
        P=[-1]*n
        for i in range(s):
            u=s+2*i;v=u+1
            if i in phase_id and x>>phase_id[i]&1:P[g[i]]=v;P[v]=u;P[u]=p[kk[g[i]]]
            else:P[i]=u;P[u]=v;P[v]=p[i]
        assert len(set(P))==n and all((i,j) in arcs for i,j in enumerate(P))
        seen=set();cycles=0
        for i in range(n):
            if i in seen:continue
            cycles+=1
            while i not in seen:seen.add(i);i=P[i]
        assert cycles==1+sum(abs(sum(x>>j&1 for j in js)-1) for js in occ)
        return P,cycles
    if k==1:
        for x in range(4096):assert perm(x)[1]!=1
    # any phase coordinate can take both values in a chart of correct global sign, since t>=12
    candidates=[(1<<j) if m%2 else ((1<<j)|(1<<((j+1)%t))) for j in range(t)]
    if not m%2:candidates.append(0)
    seen=set()
    for x in candidates:
        P,cy=perm(x);assert cy%2==1;seen.update(enumerate(P))
    assert seen==arcs
    return dict(n=n,arcs=len(arcs),sign_support_lifts=len(candidates),arc_fingerprint=hashlib.sha256(json.dumps(sorted(arcs),separators=(',',':')).encode()).hexdigest())

out=[]
for k in [1,2,4,8,16,32]:
    fs,order=instance(k);W=layout(fs);assert len(W[4*k])==3*k
    a0=run(fs,W,True);b0=run(fs,W,False);assert b0['status']=='UNSAT' and b0['max_keys']<=3
    out.append(dict(blocks=k,rank=max(map(len,W)),dense=a0,attained=b0,tree=tree(k),native=native(k)))
# guarded core: restrict original phase coordinates before every local predicate; reference full affine words.
guards=0
for j in range(12):
    for v in [0,1]:
        m=Meter();eq=[(B[j],v^(a>>j&1))];K=enumerate_keys(mul(mul(mul(mul(F[0],F[1]),F[2]),F[3]),F[4]),eq,[1,2,4],m)
        assert not K; guards+=1
# hostile controls: modulo-3 zero count but support nonempty; inconsistent keys; two individually feasible factors disjoint.
m=Meter();p={1:2,2:2,3:2}; assert len(enumerate_keys(p,[],[1,2],m))==3
assert not m.check({0:1},[(1,0),(1,1)])
assert run([{0:2,1:2},{0:2,1:1}],layout([{0:2,1:2},{0:2,1:1}]),False)['status']=='UNSAT'
result={'cap':CAP,'core_basis':V,'core_origin':a,'core_dictionaries':F,'guards':guards,'results':out}
print(json.dumps(result,indent=2));open('results.json','w').write(json.dumps(result,indent=2)+'\n')
