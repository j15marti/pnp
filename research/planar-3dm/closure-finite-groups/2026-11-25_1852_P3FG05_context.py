import networkx as nx,itertools as it,random,json
from collections import Counter

def brute(n,T):
    return [u for u in it.product(*[[t for t in T if t[0]==i] for i in range(n)]) if len({t[1] for t in u})==len({t[2] for t in u})==n]

def gf(n,T,p=None,b=0):
    B={}
    rows=[(sum(1<<j for j,t in enumerate(T) if t[c]==v),1) for c in range(3) for v in range(n)]
    if p is not None: rows.append((1<<p,b))
    for a,v in rows:
        while a and a.bit_length() in B:
            u,w=B[a.bit_length()];a^=u;v^=w
        if a:B[a.bit_length()]=(a,v)
        elif v:return False
    return True

def match(n,T,c,d,p=None):
    L=[('l',i) for i in range(n) if p is None or i!=p[c]];R=[('r',i) for i in range(n) if p is None or i!=p[d]]
    G=nx.Graph();G.add_nodes_from(L+R);G.add_edges_from((('l',t[c]),('r',t[d])) for t in T if p is None or (t[c]!=p[c] and t[d]!=p[d]))
    a=nx.algorithms.bipartite.maximum_matching(G,top_nodes=L)
    return len(a)==len(L)+len(R)

def closure(n,T):
    T=list(T)
    while True:
        if not gf(n,T) or any(not match(n,T,c,d) for c,d in [(0,1),(0,2),(1,2)]):return None
        delete=set()
        for j,t in enumerate(T):
            if not gf(n,T,j,1) or any(not match(n,T,c,d,t) for c,d in [(0,1),(0,2),(1,2)]):delete.add(j)
            if not gf(n,T,j,0) or any(sum(q[c]==t[c] for q in T)==1 for c in range(3)):
                delete.update(k for k,q in enumerate(T) if k!=j and any(q[c]==t[c] for c in range(3)))
        if not delete:return T
        T=[t for j,t in enumerate(T) if j not in delete]

def compile_chart(n,T,lane=(0,1,2)):
    T=[tuple(t[c] for c in lane) for t in T];m=len(T)
    G=nx.Graph();G.add_nodes_from(range(3*n+m));G.add_edges_from((3*n+j,c*n+v) for j,t in enumerate(T) for c,v in enumerate(t))
    yes,E=nx.check_planarity(G)
    if not yes or not nx.is_connected(G):return None
    E.check_structure();fd={};seen=set();F=0
    for a,b in E.edges():
        if (a,b) not in seen:
            face=E.traverse_face(a,b,seen)
            for u,v in zip(face,face[1:]+face[:1]):fd[u,v]=F
            F+=1
    par=list(range(F))
    def root(i):
        while par[i]!=i:par[i]=par[par[i]];i=par[i]
        return i
    for j,(x,y,z) in enumerate(T):
        a,b=3*n+j,2*n+z;par[root(fd[a,b])]=root(fd[b,a])
    roots={r:i for i,r in enumerate(sorted({root(i) for i in range(F)}))};face=lambda a,b:roots[root(fd[a,b])];F=len(roots)
    # Directed incidence difference: + face on one side, - on other. A global reversal is immaterial.
    E2=nx.Graph();E2.add_nodes_from(range(2*n));E2.add_edges_from((x,n+y) for x,y,z in T);M=nx.algorithms.bipartite.maximum_matching(E2,top_nodes=set(range(n)))
    if len(M)!=2*n:return None
    s0=[0]*m
    for i in range(n):s0[next(j for j,t in enumerate(T) if t[:2]==(i,M[i]-n))]=1
    edges=[];hosts={};C=[]
    for j,(x,y,z) in enumerate(T):
        a,b=face(x,3*n+j),face(3*n+j,x);f=face(3*n+j,2*n+z)
        assert a==face(3*n+j,n+y) and b==face(n+y,3*n+j) and f in (a,b)
        if z in hosts:assert hosts[z]==f
        hosts[z]=f;edges.append((s0[j],a,b));C.extend([(0,a,b,1-s0[j]),(0,b,a,s0[j])])
    for i,j in it.combinations(range(m),2):
        if T[i][2]!=T[j][2] or T[i][0]==T[j][0] or T[i][1]==T[j][1]:continue
        f=hosts[T[i][2]];s,a,b=edges[i];t,c,d=edges[j]
        if a==b:
            if s:C.append((0,c,d,-t))
            continue
        if c==d:
            if t:C.append((0,a,b,-s))
            continue
        p=1 if a==f else -1;q=1 if c==f else -1;u=b if p==1 else a;v=d if q==1 else c
        if p!=q:
            if p==-1:u,v=v,u
            C.append((0,v,u,1-s-t))
        elif p==1:C.append((1,f,u,-s,v,-t))
        else:C.append((-1,f,u,s,v,t))
    return F,C,edges,T

def holds(C,x):
    return all(x[a]<=x[b]+c if s==0 else x[a]<=max(x[b]+c,x[r[0]]+r[1]) if s==1 else x[a]>=min(x[b]+c,x[r[0]]+r[1]) for s,a,b,c,*r in C)
def neg(C):return [(0,b,a,c) if s==0 else (-s,a,b,-c,r[0],-r[1]) for s,a,b,c,*r in C]
def solve(F,C,B,pins,sign=1):
    if sign==-1:
        x=solve(F,neg(C),B,[(i,-v) for i,v in pins]);return None if x is None else [-v for v in x]
    x=[B]*F;lo=[-B]*F
    for i,v in pins: x[i]=lo[i]=v
    while True:
        ch=False
        for s,a,b,c,*r in C:
            assert s>=0
            v=x[b]+c if s==0 else max(x[b]+c,x[r[0]]+r[1])
            if v<x[a]:
                if v<lo[a]:return None
                x[a]=v;ch=True
        if not ch:return x

def test(n,T,lane=(0,1,2), reclose=True):
    chart=compile_chart(n,T,lane)
    if not chart:return None
    F,C,E,TT=chart;B=len(T)
    # All-pair necessary DBM tightens from both whole polarity groups.
    D=[[0 if i==j else B for j in range(F)] for i in range(F)]
    for s,a,b,c,*r in C:
        if s==0:D[b][a]=min(D[b][a],c)
    signs={s for s,*r in C if s}
    if len(signs)<2:return {'result':'pure','signs':list(signs)}
    rounds=0;live=set(TT)
    while True:
        rounds+=1;old=[r[:] for r in D]
        for sign in (1,-1):
            CC=[c for c in C if c[0]==sign]+[(0,j,i,D[i][j]) for i in range(F) for j in range(F)]
            for i in range(F):
                x=solve(F,CC,B,[(i,0)],sign)
                if x is None:return {'result':'NO','rounds':rounds}
                for j in range(F):
                    if sign==1:D[i][j]=min(D[i][j],x[j])
                    else:D[j][i]=min(D[j][i],-x[j])
        if reclose:
            L=set(live)
            for j,(s,a,b) in enumerate(E):
                if s+D[b][a]<=0:L.discard(TT[j])
                if s-D[a][b]>=1:
                    L.difference_update(q for q in live if q!=TT[j] and any(q[c]==TT[j][c] for c in range(3)))
            if L!=live:
                L=closure(n,sorted(L))
                if L is None:return {'result':'NO','rounds':rounds,'source_reclosure':True}
                live=set(L)
                for j,(s,a,b) in enumerate(E):
                    if TT[j] not in live:D[b][a]=min(D[b][a],-s)
        if old==D:break
    db=[(0,j,i,D[i][j]) for i in range(F) for j in range(F)]
    certs=[];one=[]
    for sign in (1,-1):
        CC=[c for c in C if c[0]==sign]+db
        x=solve(F,CC,B,[(0,0)],sign)
        good=holds(C,x);one.append(good)
        if good:
            vals=[s+x[a]-x[b] for s,a,b in E]
            assert all(v in (0,1) for v in vals)
            U=[t for t,v in zip(TT,vals) if v]
            assert len(U)==n and all(len({t[c] for t in U})==n for c in range(3)) and set(U)<=live
        # all hubs: canonical lower generator for +, upper for -.
        certs.append(all(solve(F,CC,B,[(j,-D[j][i] if sign==1 else D[i][j]) for j in range(F)],sign) is not None for i in range(F)))
    return {'result':'YES' if any(one) else 'UNKNOWN','rounds':rounds,'certs':certs,'faces':F,'signs':list(signs),'D':D}

if __name__=='__main__':
    T0=[tuple(map(int,s)) for s in '000 002 010 011 021 022 100 101 111 201 202 221'.split()]
    for t in [T0,T0+[(1,1,0)]]:
        L=closure(3,t); print('peer',len(t),len(brute(3,t)),len(L) if L else None, [{k:v for k,v in test(3,L,l).items() if k!='D'} for l in [(0,1,2),(0,2,1),(1,2,0)]] if L else None)
    rng=random.Random(20261125);counts=Counter();found=None
    for _ in range(1500):
        n=3;T=sorted(rng.sample(list(it.product(range(n),repeat=3)),rng.choice([9,10,11,12,13,14])))
        G=nx.Graph();G.add_nodes_from(range(3*n+len(T)));G.add_edges_from((3*n+j,c*n+v) for j,t in enumerate(T) for c,v in enumerate(t))
        if not nx.check_planarity(G)[0] or not nx.is_connected(G):continue
        L=closure(n,T)
        if not L:counts['closed']+=1;continue
        truth=bool(brute(n,T));R=[test(n,L,l) for l in [(0,1,2),(0,2,1),(1,2,0)]]
        if any(r and r['result']=='NO' for r in R):assert not truth
        if any(r and r['result']=='YES' for r in R):assert truth
        counts['SAT' if truth else 'UNSAT']+=1
        if not truth and all(r and r['result']=='UNKNOWN' for r in R):found={'T':T,'L':L,'R':R};break
    print('search',counts,'obstruction',json.dumps(found))
