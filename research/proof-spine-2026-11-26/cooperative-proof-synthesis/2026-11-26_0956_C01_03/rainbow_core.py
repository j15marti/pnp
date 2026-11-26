"""Extracted core of executed region03.py; exact local_cover from guarded_macro.py.
Full original runners, dependencies, guards and witnesses in C01_03_guarded_rainbow_contraction.tar.gz.
Requires Python 3 and NetworkX.
"""
import collections as C,itertools as I
from functools import lru_cache
import networkx as nx

def local_cover(byid,J,req,ones):
    V=sorted(req);ix={v:i for i,v in enumerate(V)};mask=(1<<len(V))-1;B={j:sum(1<<ix[v] for v in byid[j]) for j in J if all(v in ix for v in byid[j])};O=[[] for v in V];out=[]
    for j,b in B.items():
        for v in byid[j]:O[ix[v]].append(j)
    for j in sorted(ones):
        if j not in B or B[j]&mask!=B[j]:return None,0
        mask^=B[j];out.append(j)
    nodes=0
    @lru_cache(None)
    def rec(R):
        nonlocal nodes;nodes+=1
        if not R:return ()
        best=None;tmp=R
        while tmp:
            a=tmp&-tmp;tmp^=a;L=[j for j in O[a.bit_length()-1] if B[j]&R==B[j]]
            if not L:return None
            if best is None or len(L)<len(best):best=L
        for j in best:
            r=rec(R^B[j])
            if r is not None:return (j,)+r
        return None
    z=rec(mask)
    if z is None:return None,nodes
    w=out+list(z);S=[v for j in w for v in byid[j]];assert len(S)==len(set(S)) and set(S)==req
    return w,nodes

def contract(T,n,L,B,one=(),cap=169):
    byid={j:tuple(enumerate(T[j])) for j in L};G=nx.Graph();G.add_nodes_from((c,v) for c in range(3) for v in range(n) if (c,v) not in B);G.add_nodes_from(('t',j) for j in L)
    G.add_edges_from((('t',j),v) for j,t in byid.items() for v in t if v not in B);W=[];opts=[];covered=set();st=C.Counter()
    for U in nx.connected_components(G):
        J=sorted(v for c,v in U if c=='t');P={v for v in U if v[0]!='t'};K=sorted({v for j in J for v in byid[j] if v in B});st['components']+=1
        if len(J)>cap or len({v[0] for v in K})!=len(K):return 'OPEN',None,{**st,'wide_region':len(J),'boundary':len(K)}
        R={};c0=[sum(v[0]==c for v in P) for c in range(3)]
        for b in I.product((0,1),repeat=len(K)):
            q=c0.copy();S={v for v,t in zip(K,b) if t}
            for c,v in S:q[c]+=1
            if len(set(q))!=1:continue
            w,nodes=local_cover(byid,J,P|S,set(J)&set(one));st['local_queries']+=1;st['nodes']+=nodes
            if w is not None:R[b]=w
        if not R:return 'NO',None,dict(st)
        if len(R)==2:
            assert len(K)==3 and set(R)=={(0,0,0),(1,1,1)};opts.append((K,R));continue
        b,w=next(iter(R.items()));S={v for v,t in zip(K,b) if t}
        if covered&S:return 'NO',None,dict(st)
        covered|=S;W.extend(w)
    B0=B-covered;C0=[sorted(v for v in B0 if v[0]==c) for c in range(3)]
    if len(set(map(len,C0)))!=1:return 'NO',None,dict(st)
    idx={v:i for L0 in C0 for i,v in enumerate(L0)};TT=[];lift=[]
    for K,R in opts:
        if set(K)<=B0:TT.append(tuple(idx[v] for v in K));lift.append(R)
        else:W.extend(R[(0,0,0)])
    D={};A=[];H=[]
    for t,r in zip(TT,lift):
        if t in D:W.extend(r[(0,0,0)])
        else:D[t]=len(A);A.append(t);H.append(r)
    st['coarse_triples']=len(A);st['coarse_owners']=len(C0[0]);return 'OK',(A,len(C0[0]),W,H),dict(st)

def lift_original(R,coarse_witness):
    A,n0,W,H=R;S=set(coarse_witness)
    return sorted(W+[j for i,r in enumerate(H) for j in r[(1,1,1) if i in S else (0,0,0)]])
