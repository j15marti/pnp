import itertools as it, json, collections, random, networkx as nx
from p3_lane_explore import oct_chain, incidence, oracle, closure, formula

def solve(T,n):
    T=set(T); source=T.copy(); pinned=set(); remaining={(i,v) for i in range(3) for v in range(n)}; rounds=0
    while True:
        rounds+=1
        maps=[sorted(v for j,v in remaining if j==i) for i in range(3)]; inv=[{v:j for j,v in enumerate(a)} for a in maps]; r=len(maps[0])
        def decode(t):return tuple(maps[i][v] for i,v in enumerate(t))
        S,P=closure({tuple(inv[i][v] for i,v in enumerate(t)) for t in T},r)
        if S is None:return 'NO','matching/owner',None,rounds
        P={decode(t) for t in P};pinned|=P;remaining-={(i,v) for t in P for i,v in enumerate(t)};T={decode(t) for t in S}
        if not T:return 'YES','forced',sorted(pinned),rounds
        ts,D,cs,G=formula(T);C={v:k for k,c in enumerate(nx.strongly_connected_components(G)) for v in c}
        if any(C[i,0]==C[i,1] for i in range(len(ts))):return 'NO','2SAT',None,rounds
        reach={v:nx.descendants(G,v) for v in G}
        fix={i:int((i,1) in reach[i,0]) for i in range(len(ts)) if (i,1) in reach[i,0] or (i,0) in reach[i,1]}
        if not fix:break
        P={ts[i] for i,v in fix.items() if v};pinned|=P;remaining-={(i,v) for t in P for i,v in enumerate(t)}
        T={t for i,t in enumerate(ts) if i not in fix and not any((j,v) not in remaining for j,v in enumerate(t))}
    weights=collections.Counter(); classes={};base=len(pinned); reps={}
    for i in range(len(ts)):
        a,b=C[i,0],C[i,1];r=min(a,b);q=int(b==r);classes[i]=(r,q);weights[r]+=1 if q else -1;base+=1-q;reps.setdefault(r,(i,q))
    active=sorted(r for r in reps if weights[r]); H=nx.Graph();H.add_nodes_from(active); forb=[]
    for r,s in it.combinations(active,2):
        i,q=reps[r];j,p=reps[s]
        for a,b in it.product((0,1),repeat=2):
            l=(i,a if q else 1-a);m=(j,b if p else 1-b)
            if (j,1-m[1]) in reach[l]:
                par=1^a^b;forb.append((r,a,s,b))
                if H.has_edge(r,s) and H[r][s]['par']!=par:return 'UNKNOWN','orientation',None,rounds
                H.add_edge(r,s,par=par)
    color={}
    for r in H:
        if r in color:continue
        color[r]=0;queue=[r]
        for u in queue:
            for v,e in H[u].items():
                val=color[u]^e['par']
                if v in color:
                    if val!=color[v]:return 'UNKNOWN','orientation',None,rounds
                else:color[v]=val;queue.append(v)
    s0='source';t0='sink';K=nx.DiGraph();K.add_nodes_from([s0,t0]+active);gain={r:weights[r]*(1-2*color[r]) for r in active};base+=sum(weights[r]*color[r] for r in active);inf=1+sum(abs(w) for w in gain.values())
    for r,w in gain.items():
        if w>0:K.add_edge(s0,r,capacity=w)
        if w<0:K.add_edge(r,t0,capacity=-w)
    for r,a,s,b in forb:
        a^=color[r];b^=color[s];assert a!=b
        u,v=(r,s) if a else (s,r);K.add_edge(u,v,capacity=inf)
    value,(left,right)=nx.minimum_cut(K,s0,t0); optimum=base+sum(w for w in gain.values() if w>0)-value
    assert optimum<=n
    F=G.copy()
    for r in active:
        i,q=reps[r];z=int(r in left)^color[r];a=z if q else 1-z;F.add_edge((i,1-a),(i,a))
    comps=list(nx.strongly_connected_components(F));M={v:i for i,c in enumerate(comps) for v in c};assert all(M[i,0]!=M[i,1] for i in range(len(ts)))
    topo={v:i for i,v in enumerate(nx.topological_sort(nx.condensation(F,comps)))};word={ts[i] for i in range(len(ts)) if topo[M[i,1]]>topo[M[i,0]]};W=pinned|word
    assert len(W)==optimum and all(len({t[i] for t in W})==len(W) for i in range(3)) and W<=source
    method='invariant' if not active else 'mincut'
    return ('YES',method,sorted(W),rounds) if optimum==n else ('NO',method,None,rounds)

if __name__=='__main__':
 rng=random.Random(20261125); stats=collections.Counter(); examples={}; checked=0; neighbors=[]
 for n in [2,3,4,5,6,8]:
  U=sorted(oct_chain(n))
  for j in range(400):
   p=rng.uniform(.3,1);T={t for t in U if rng.random()<p};assert nx.check_planarity(incidence(T,n))[0];w=oracle(T,n);r,m,v,k=solve(T,n);checked+=1;stats[r,m]+=1
   assert r=='UNKNOWN' or (r=='YES')==(w is not None),(T,r,w)
   if v is not None:assert len(v)==n and all(len({t[i] for t in v})==n for i in range(3))
   key=r,m
   if key not in examples:examples[key]=dict(n=n,T=sorted(T),witness=v,oracle=w,rounds=k)
   if r=='NO' and m in ('invariant','mincut') and len(neighbors)<10:
    for t in U:
     if t not in T and oracle(T|{t},n) is not None:
      neighbors.append(dict(n=n,T=sorted(T),add=t,unsat_method=m,sat_terminal=solve(T|{t},n)[:2]));break
 print(json.dumps(dict(seed=20261125,checked=checked,stats={str(k):v for k,v in stats.items()},examples={str(k):v for k,v in examples.items()},neighbors=neighbors),indent=2))
