"""Exact blind directed balanced series-cycle adapter for actual P3DM sources.
Requires sibling p3fcg12 and transitive archived dependencies.
"""
import sys,pathlib,itertools as I,collections as C,json
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent.parent/'p3fcg12'))
import audit as a
import networkx as nx
BASE=((0,0,1),(0,0,2),(0,1,0),(0,2,0),(1,0,1),(1,1,0),(1,1,1),(2,0,2),(2,2,0),(2,2,2))
W=(((0,0,1),(1,1,0),(2,2,2)),((0,0,2),(1,1,1),(2,2,0)),((0,1,0),(1,0,1),(2,2,2)),((0,2,0),(1,1,1),(2,0,2)))
def make(k):
    e=BASE[0]
    def move(t,i):return (3*i+t[0],3*((i+1)%k if t==e else i)+t[1],3*i+t[2])
    return tuple(sorted(move(t,i) for i in range(k) for t in BASE)),3*k,lambda w:tuple(move(t,i) for i in range(k) for t in w)
def edge(u,v):return tuple(sorted((u,v)))
def candidates(G):
    sig={edge(u,v):0 for u,v in G.edges}
    for j,C0 in enumerate(nx.cycle_basis(G)):
        for u,v in zip(C0,C0[1:]+C0[:1]):sig[edge(u,v)] |= 1<<j
    classes=C.defaultdict(list)
    for e,b in sig.items():
        if b:classes[b].append(e)
    return sorted((sorted(S) for S in classes.values() if len(S)>1),key=lambda S:(-len(S),S))
def acquire(T,n,cap=12):
    G=a.old.incidence(T,n)
    if not nx.is_connected(G):return None
    for S in candidates(G):
        directed=[(u,v) if len(u)==3 else (v,u) for u,v in S]
        if len({v[0] for u,v in directed})!=1:continue
        c=directed[0][1][0];H=G.copy();H.remove_edges_from(S);blocks=list(nx.connected_components(H))
        if len(blocks)!=len(S):continue
        ids={v:i for i,B in enumerate(blocks) for v in B};out={};inc={};ok=True
        for t,r in directed:
            i,j=ids[t],ids[r]
            if i==j or i in out or j in inc:ok=False;break
            out[i]=t;inc[j]=r
        if not ok or len(out)!=len(blocks) or len(inc)!=len(blocks):continue
        chart=[]
        for i,B in enumerate(blocks):
            Ts=sorted(v for v in B if len(v)==3);rows=[sorted(v[1] for v in B if len(v)==2 and v[0]==d) for d in range(3)]
            if len(Ts)>cap or len(set(map(len,rows)))!=1 or not rows[0]:ok=False;break
            maps=[{v:j for j,v in enumerate(L)} for L in rows];mp={}
            for t in Ts:
                u=list(t)
                if t==out[i]:u[c]=inc[i][1]
                q=tuple(maps[d][u[d]] for d in range(3));mp[q]=t
            if len(mp)!=len(Ts) or not a.old.check(tuple(mp),len(rows[0])):ok=False;break
            pin=next(q for q,t in mp.items() if t==out[i]);chart.append((mp,len(rows[0]),pin))
        if ok:return chart
    return None
def solve(T,n):
    assert a.old.check(T,n);E=a.old.Engine();R,_=E.closure(T,n)
    if R is None:return dict(decision='NO',native=True,calls=E.calls)
    if len(R)==n and a.old.verify(T,n,R):return dict(decision='YES',native=True,calls=E.calls,witness=R)
    chart=acquire(T,n)
    if chart is None:return dict(decision='UNKNOWN',calls=E.calls)
    allowed=set(R);counts=[];attempts=0;witness=None
    for bit in (0,1):
        W0=[];count=1
        for mp,m,p in chart:
            D=tuple(q for q,t in mp.items() if t in allowed and ((q==p)==bool(bit) or (bit and all(q[d]!=p[d] for d in range(3))))) if bit else tuple(q for q,t in mp.items() if t in allowed and q!=p)
            # bit 1 retains p and tuples disjoint from p; reject if p was already deleted.
            if bit and p not in D:count=0;break
            R0,_=E.closure(D,m);attempts+=1
            if R0 is None:count=0;break
            # exact enumeration is capped by original atom size (<=12 tuples).
            by={x:[t for t in R0 if t[0]==x] for x in range(m)}
            sols=[q for q in I.product(*by.values()) if a.old.verify(R0,m,q)]
            if not sols:count=0;break
            if bit:assert all(p in s for s in sols)
            count*=len(sols);W0.extend(mp[q] for q in sols[0])
        if count:
            assert a.old.verify(T,n,W0);witness=W0
        counts.append(count)
    return dict(decision='YES' if sum(counts) else 'NO',counts=counts,atoms=len(chart),calls=E.calls,attempts=attempts,witness=witness)
def hostile(k):
    T,n,move=make(k);E=a.old.Engine();R,_=E.closure(T,n);assert R==T
    assert a.old.check(T,n) and nx.is_connected(a.old.incidence(T,n));covers=[move(w) for w in W];assert all(a.old.verify(T,n,w) for w in covers);assert set(T)==set().union(*map(set,covers))
    obs=[]
    for c,ijk in enumerate(((0,1,2),(1,0,2),(0,1,2))):
        J=a.prev.Join(T,n,c,E,'reference');ws=[]
        for i in ijk:
            p={}
            for t in covers[i]:p.update(J.tuplepins(t))
            ws.append(p)
        q={p:a.dd(*(w[p] for w in ws)) for p in J.ports};D=[t for t in T if all(q[p]==v for p,v in J.tuplepins(t).items())]
        missing=[(d,x) for d in range(3) for x in range(n) if not any(t[d]==x for t in D)]
        assert missing and J.lift(q) is None;obs.append(dict(center=c,missing=len(missing),first=missing[0]))
    res=solve(T,n);assert res['decision']=='YES' and sum(res['counts'])==1+3**k and sorted(res['counts'])==[1,3**k]
    res.pop('witness');return dict(k=k,m=len(T),obstructions=obs,solver=res)
def neighbors(k):
    T,n,move=make(k); e=move(W[0])[0]; # first block requires e; second block splice tuple deletion gives NO.
    S=tuple(t for t in T if t[0]!=e[0] or t==e);e2=move(W[0])[3];U=tuple(t for t in S if t!=e2)
    assert a.old.verify(S,n,move(W[0]));assert a.old.check(U,n)
    A=solve(S,n);B=solve(U,n);assert A['decision']=='YES' and B['decision']=='NO';A.pop('witness',None)
    return dict(k=k,S=len(S),U=len(U),positive=A,negative=B)
if __name__=='__main__':print(json.dumps(dict(hostile=[hostile(k) for k in (2,3,4,8,16,32,64)],neighbors=[neighbors(k) for k in (2,4,8,16,32,64)])))
