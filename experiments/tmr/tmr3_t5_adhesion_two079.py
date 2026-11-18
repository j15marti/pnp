#!/usr/bin/env python3
"""TMR-3/079, authenticated exact T5 counting by clique-separator gluing.
Input: one JSON object {"n": nonnegative integer, "arcs": [[u,v], ...], "budget": nonnegative integer}.
If stdin is empty, run deterministic selftests and output JSON audit.
The fast method applies only to 3-parent private-sink incidence graphs and
fragments with bounded relative factor covers; fallback is always exact.
No external packages or network.
"""
from __future__ import annotations
from itertools import combinations, product
from collections import deque
import json, sys, random, hashlib

REVISION = 'TMR3-T5-ADHESION-TWO079-v1'
SEED = 202611180019

def beat(a,b): return (b-a)%5 in (1,3)
def w3(a,b,c): return sum(beat(a,z) and beat(b,z) and beat(c,z) for z in range(5))

def table3(): return tuple(w3(*cols) for cols in product(range(5),repeat=3))
TRIPLE = table3()

def idx(vals):
    z=0
    for v in vals: z=5*z+v
    return z

def forest_count(n,edges):
    """Original-arc exact spanning-forest difference enumeration with Z5 symmetry."""
    adj=[[] for _ in range(n)]
    for u,v in edges:
        adj[u].append((v,(1,3)));adj[v].append((u,(-1,-3)))
    seen=set(); total=1
    for root in range(n):
        if root in seen: continue
        order=[root];seen.add(root);par={root:None};delta={}
        for u in order:
            for v,opts in adj[u]:
                if v not in seen:
                    seen.add(v);par[v]=u;delta[v]=opts;order.append(v)
        edgeset=[(u,v) for u,v in edges if u in par and v in par]
        accepted=0
        for bits in product((0,1),repeat=len(order)-1):
            x={root:0}
            for v,bit in zip(order[1:],bits):x[v]=(x[par[v]]+delta[v][bit])%5
            if all(beat(x[u],x[v]) for u,v in edgeset):accepted+=1
        total *= 5*accepted
    return total

def direct_count(n,arcs):
    return sum(all(beat(x[u],x[v]) for u,v in arcs) for x in product(range(5),repeat=n))

def normalize(n, arcs):
    if type(n)!=int or n<0:raise ValueError('n must be nonnegative integer')
    if not isinstance(arcs,list):raise ValueError('arcs must be list')
    edges=set()
    for a in arcs:
        if not isinstance(a,(list,tuple)) or len(a)!=2 or any(type(v)!=int or v<0 or v>=n for v in a):
            raise ValueError('invalid arc')
        edges.add(tuple(a))
    return sorted(edges)

def incidence(n,edges):
    """Return (hubs, triples) or None. Every private sink has indegree 3."""
    indeg=[0]*n;outdeg=[0]*n; parents=[[] for _ in range(n)]
    for u,v in edges:outdeg[u]+=1;indeg[v]+=1;parents[v].append(u)
    hubs=tuple(i for i in range(n) if indeg[i]==0)
    hs=set(hubs)
    triples=[]
    for i in range(n):
        if i in hs: continue
        if outdeg[i]!=0 or indeg[i]!=3 or any(u not in hs for u in parents[i]):return None
        triples.append(tuple(sorted(parents[i])))
    return hubs,triples

# Each factor is (ordered variable scope, flattened array, type)
# The triple table is translation-invariant but is stored once globally.
def factors_for(triples):return [(tuple(sorted(e)), TRIPLE, 'sink') for e in triples]

def connected_components(W, adj, banned):
    left=set(W)-set(banned);out=[]
    while left:
        u=min(left);left.remove(u); q=[u];C=[u]
        for v in q:
            for x in adj[v]:
                if x in left:
                    left.remove(x);q.append(x);C.append(x)
        out.append(set(C))
    return out

def find_split(W,factors,U):
    """Find an explicit clique separator of size <=2, or None."""
    adj={v:set() for v in W}
    for scope,tab,kind in factors:
        for a,b in combinations(scope,2):adj[a].add(b);adj[b].add(a)
    if len(U)==2:
        a,b=U;adj[a].add(b);adj[b].add(a)  # virtual interface edge only
    sep_list=[()]+[(a,) for a in sorted(W)]+[(a,b) for a in sorted(W) for b in sorted(adj[a]) if a<b]
    for S in sep_list:
        comps=connected_components(W,adj,S)
        if len(comps)<2:continue
        outside=set(U)-set(S)
        anchors=[i for i,C in enumerate(comps) if outside<=C]
        if not anchors:continue
        return tuple(S),comps,anchors[0]
    return None

def cover_search(W,factors,U,t):
    """Relative factor cover: 2 fixed per triple, 1 fixed per 2-ary message."""
    def walk(chosen):
        fixed=set(U)|chosen
        if len(chosen)>t:return None
        deficiency=None; options=None
        for scope,tab,kind in factors:
            req=max(0,len(scope)-1) if len(scope)>1 else 0
            # All factors are at most ternary. Need enough fixed so <=1 free.
            left=[v for v in scope if v not in fixed]
            if len(left)>1:
                deficit=len(left)-1
                opts=list(combinations(left,deficit))
                if options is None or len(opts)<len(options):
                    deficiency=scope;options=opts
        if options is None:return tuple(sorted(chosen))
        if len(chosen)>=t:return None
        for additions in options:
            if len(chosen)+len(additions)>t:continue
            r=walk(chosen|set(additions))
            if r is not None:return r
        return None
    return walk(set())

def evaluate_base(W,factors,U,cover):
    """Sum unrestricted non-cover variables independently. Count variables once."""
    U=tuple(U);cover=tuple(cover)
    free=sorted(set(W)-set(U)-set(cover))
    output=[]
    for bc in product(range(5),repeat=len(U)):
        s=0
        for cc in product(range(5),repeat=len(cover)):
            fixed=dict(zip(U,bc));fixed.update(zip(cover,cc))
            constant=1; byfree={v:[] for v in free}
            for scope,table,kind in factors:
                rem=[v for v in scope if v not in fixed]
                if not rem:
                    constant*=table[idx(fixed[x] for x in scope)]
                else:
                    if len(rem)>1:raise AssertionError('non-unary remainder')
                    byfree[rem[0]].append((scope,table))
            z=constant
            if z:
                for v in free:
                    subtotal=0
                    for c in range(5):
                        fixed[v]=c
                        term=1
                        for scope,table in byfree[v]:
                            term*=table[idx(fixed[x] for x in scope)]
                        subtotal+=term
                    fixed.pop(v)
                    z*=subtotal
            s+=z
        output.append(s)
    return tuple(output)

class BudgetExceeded(Exception):pass

def decompose_count(hubs,triples,budget=3):
    stats={'splits':0,'prime_pieces':0,'max_interface':0,'max_cover':0,'ternary':len(triples),'binary_messages':0,'fallback':False}
    def rec(W,factors,U):
        W=frozenset(W);U=tuple(sorted(U));assert set(U)<=set(W) and len(U)<=2
        stats['max_interface']=max(stats['max_interface'],len(U))
        splitter=find_split(W,factors,U)
        if splitter is None:
            C=cover_search(W,factors,U,budget)
            if C is None:raise BudgetExceeded()
            stats['prime_pieces']+=1;stats['max_cover']=max(stats['max_cover'],len(C))
            return evaluate_base(W,factors,U,C)
        S,comps,anchor=splitter
        stats['splits']+=1
        anchorW=comps[anchor]|set(S)
        rootf=[];childf=[[] for _ in comps]
        for f in factors:
            scope=f[0]
            nonsep=set(scope)-set(S)
            if not nonsep:
                rootf.append(f)
                continue
            hits=[j for j,C in enumerate(comps) if nonsep<=C]
            if len(hits)!=1:raise AssertionError('factor crosses split')
            if hits[0]==anchor:rootf.append(f)
            else:childf[hits[0]].append(f)
        for i,C in enumerate(comps):
            if i==anchor:continue
            childW=C|set(S)
            msg=rec(childW,childf[i],S)
            rootf.append((S,msg,'message'))
            if len(S)==2:stats['binary_messages']+=1
        return rec(anchorW,rootf,U)
    result=rec(set(hubs),factors_for(triples),())
    return result[0],stats

def solve(n,arcs,budget=3):
    if type(budget)!=int or budget<0:raise ValueError('budget must be nonnegative integer')
    edges=normalize(n,arcs)
    if any(u==v or (v,u) in set(edges) for u,v in edges):
        return 0,{'mode':'structural-zero'}
    inc=incidence(n,edges)
    if inc is not None:
        try:
            z,stats=decompose_count(*inc,budget=budget)
            stats['mode']='adhesion-two'
            return z,stats
        except BudgetExceeded:
            return hub_reference_count(*inc),{'mode':'hub-fallback'}
    return forest_count(n,edges),{'mode':'forest-fallback'}

def chain(r):
    """r K4 clique atoms sharing successive TWO-hub interfaces."""
    assert r>=1
    arcs=[]; nextid=2*(r+1)
    for i in range(r):
        pair0=(2*i,2*i+1); pair1=(2*i+2,2*i+3)
        hubs=pair0+pair1
        for triple in combinations(hubs,3):
            z=nextid;nextid+=1
            arcs.extend((u,z) for u in triple)
    assert nextid==6*r+2
    return nextid,arcs

def hub_reference_count(hubs,triples):
    import math
    hs=tuple(hubs); k=len(hs); look={v:i for i,v in enumerate(hs)}
    ts=[tuple(look[u] for u in e) for e in triples]
    result=0
    for x in product(range(5),repeat=k):
        z=1
        for e in ts:
            z*=TRIPLE[idx(x[i] for i in e)]
            if not z:break
        result+=z
    return result

def test():
    rng=random.Random(SEED); categories={}; failures=[]; examples={}
    def chk(label, cond):
        categories[label]=categories.get(label,0)+1
        if not cond:failures.append(label)
    # Arithmetic and structural checks
    chk('template',all(sum(beat(a,b) for b in range(5))==2 for a in range(5)))
    chk('template',all(w3(a,b,c) in (0,1,2) for a,b,c in product(range(5),repeat=3)))
    for n in range(1,7):
        for j in range(12):
            arcs=[(a,b) for a in range(n) for b in range(n) if rng.random()<0.13]
            z,st=solve(n,arcs)
            chk('arbitrary',z==direct_count(n,arcs))
    for k in range(2,7):
        for j in range(10):
            triples=[]
            for tri in combinations(range(k),3):
                if rng.random()<0.36:triples.append(tri)
                if rng.random()<0.09:triples.append(tri)
            arcs=[]
            for i,e in enumerate(triples):arcs.extend((u,k+i) for u in e)
            z,st=solve(k+len(triples),arcs,budget=3)
            chk('incidence',z==hub_reference_count(range(k),triples))
    for r in range(1,13):
        n,arcs=chain(r)
        z,st=solve(n,arcs,budget=3)
        chk('chain',st['mode']=='adhesion-two')
        if r<=3:
            inc=incidence(n,normalize(n,arcs))
            chk('chain',z==hub_reference_count(*inc))
        examples[r]={'n':n,'m':len(arcs),'count':str(z),'digits':len(str(z)),'stats':st}
    n,arcs=chain(1)
    chk('full-direct',solve(n,arcs)[0]==direct_count(n,arcs))
    for n, arcs in [(2,[(0,0)]),(2,[(0,1),(1,0)]),(2,[(0,1),(0,1)]),(0,[])]:
        z,st=solve(n,arcs)
        chk('controls',z==direct_count(n,arcs))
    for bad in [(-1,[]),(3,[(0,3)]),(1,[(0,1.0)]),(1,[(0,1,2)]),(1,'x')]:
        try:solve(*bad); chk('malformed',False)
        except (ValueError, TypeError):chk('malformed',True)
    return {'revision':REVISION,'seed':SEED,'total_checks':sum(categories.values()),'checks_by_group':categories,'failures':failures,'chain_examples':{str(k):v for k,v in examples.items() if k in (1,2,3,5,12)}}

def main():
    raw=sys.stdin.read().strip()
    if raw:
        d=json.loads(raw)
        z,meta=solve(d['n'],d['arcs'],d.get('budget',3))
        print(json.dumps({'count':str(z),'satisfiable':z>0,'metadata':meta},sort_keys=True))
    else:
        print(json.dumps(test(),sort_keys=True,indent=2))
if __name__=='__main__':main()
