"""BH12: python 3, networkx 3.6.1. Exact planar signed NAE terminal.
None denotes UNKNOWN; False denotes proved UNSAT; dict denotes a model.
"""
import itertools as it, random, json, collections
import networkx as nx
L=collections.Counter()

def valid(F,O,x):
    return all(len({x[v]^s for v,s in f})>1 for f in F) and all(any(x[v]^s for v,s in f) for f in O)

def closure(n,F,O,pins):
    # y_v xor y_ref is the original bit. Keep a signed representative map.
    p=list(range(n+1)); d=[0]*(n+1)
    def merge(a,b,t):
        t^=d[a]^d[b]; a,b=p[a],p[b]
        if a==b: return t==0
        for i in range(n+1):
            if p[i]==a: p[i]=b; d[i]^=t
        L['merges']+=1
        return True
    for v,b in pins:
        if not merge(v,n,b): return False
    while True:
        L['closure_scans']+=1; A=[]; B=[]; forced=None
        for f in F:
            z=set((p[v],d[v]^s) for v,s in f)
            if any((v,s^1) in z for v,s in z): continue
            if len(z)<2: return False
            if len(z)==2:
                (u,a),(v,b)=sorted(z); forced=(u,v,1^a^b); break
            A.append(tuple(sorted(z)))
        if forced is None:
            for f in O:
                z=set((p[v],d[v]^s^d[n]) for v,s in f)
                if (p[n],1) in z or any((v,s^1) in z for v,s in z): continue
                z.discard((p[n],0))
                if not z: return False
                if len(z)==1:
                    u,a=next(iter(z)); forced=(u,n,1^a^d[n]); break
                B.append(tuple(sorted(z)))
        if forced is None: return p,d,A,B
        if not merge(*forced): return False

def planar_energy(vertices,F):
    J=collections.Counter()
    for f in F:
        assert len(f)==3
        for (u,a),(v,b) in it.combinations(f,2): J[tuple(sorted((u,v)))]+=(-1)**(a^b)
    G=nx.Graph(); G.add_nodes_from(vertices)
    for (u,v),j in J.items():
        if j: G.add_edge(u,v,w=abs(j),pref=int(j>0))
    L['planarity_calls']+=1
    ok,E=nx.check_planarity(G)
    if not ok: return None
    y={}; total=0
    for C in nx.connected_components(G):
        H=G.subgraph(C); root=min(C)
        if H.number_of_edges()==0: y[root]=0; continue
        # Enumerate oriented face walks, including bridge twice.
        marked=set(); side={}; T=set(); nf=0
        for u,v in E.edges():
            if u not in C or (u,v) in marked: continue
            walk=E.traverse_face(u,v,marked); parity=0
            for a,b in zip(walk,walk[1:]+walk[:1]):
                side[a,b]=nf; parity^=G[a][b]['pref']
            if parity: T.add(nf)
            nf+=1
        L['dual_faces']+=nf; L['odd_faces']+=len(T)
        D=nx.Graph(); D.add_nodes_from(range(nf))
        for u,v,dat in H.edges(data=True):
            a,b=side[u,v],side[v,u]; w=dat['w']
            if a==b: continue
            if not D.has_edge(a,b) or w<D[a][b]['weight']:
                D.add_edge(a,b,weight=w,edge=tuple(sorted((u,v))))
        K=nx.Graph(); K.add_nodes_from(T); paths={}
        for a in sorted(T):
            dist,path=nx.single_source_dijkstra(D,a,weight='weight'); L['shortest_paths']+=1
            for b in sorted(T):
                if a<b: K.add_edge(a,b,weight=dist[b]); paths[a,b]=path[b]
        bad=set()
        if T:
            L['blossom_calls']+=1; M=nx.min_weight_matching(K,weight='weight')
            assert len(M)*2==len(T)
            for a,b in M:
                path=paths[tuple(sorted((a,b)))]; L['matched_pairs']+=1
                for q,r in zip(path,path[1:]): bad.symmetric_difference_update({D[q][r]['edge']})
            assert sum(G[u][v]['w'] for u,v in bad)==sum(K[a][b]['weight'] for a,b in M)
        y[root]=0; Q=[root]
        for u in Q:
            for v,dat in H[u].items():
                t=y[u]^dat['pref']^(tuple(sorted((u,v))) in bad)
                if v not in y: y[v]=t; Q.append(v)
                else: assert y[v]==t
        total+=sum(G[u][v]['w'] for u,v in bad)
    e=len(F)-sum(abs(j) for j in J.values())+2*total
    assert e==4*sum(len({y[v]^s for v,s in f})==1 for f in F)
    L['energy_checks']+=1
    return e,y

def solve(n,F,O=(),B=(),pins=()):
    # Local closure before any branch, again after every acquired parity.
    z=closure(n,F,O,pins)
    if z is False: return False
    p,d,A,R=z
    if B:
        v,*tail=B
        if p[v]==p[n]: return solve(n,F,O,tail,pins)
        branches=[((v,b),) for b in (0,1)]
        nextB=tail
    elif R:
        # Select one true literal of one remaining OR, on ORIGINAL IDs.
        f=R[0]; branches=[]; nextB=()
        for u,s in f:
            v=next(i for i in range(n) if p[i]==u)
            branches.append(((v,1^s^d[v]^d[n]),))
    else:
        ans=planar_energy(set(p),A)
        if ans is None: L['declines']+=1; return None
        e,y=ans
        if e: return False
        x={v:y[p[v]]^d[v]^y[p[n]]^d[n] for v in range(n)}
        assert valid(F,O,x) and all(x[v]==b for v,b in pins)
        L['verified_witnesses']+=1; return x
    L['branch_nodes']+=1; unknown=False
    for b in branches:
        L['branch_edges']+=1; q=solve(n,F,O,nextB,pins+b)
        if isinstance(q,dict): return q
        unknown|=q is None
    return None if unknown else False

def full(t,s=0): return tuple((v,(s>>i)&1) for i,v in enumerate(t))
def brute(n,F,O=(),pins=()):
    L['reference_words']+=2**n
    return sum(valid(F,O,dict(enumerate(x))) and all(x[v]==b for v,b in pins) for x in it.product((0,1),repeat=n))
def check(n,F,O=(),B=(),pins=(),ref=None):
    q=solve(n,F,O,B,pins)
    if ref is None: ref=brute(n,F,O,pins)
    assert q is not None and isinstance(q,dict)==bool(ref)
    return bool(ref)
def run():
    rng=random.Random(2081240); out={}; hist=collections.Counter()
    # Fano lines; one forbidden monochromatic word retained in each neighbor.
    for n,ts,name,B in [(7,[(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)],'Fano',tuple(range(4))), (5,list(it.combinations(range(5),3)),'K5_triples',tuple(range(2)))]:
        F=[full(t) for t in ts]; assert solve(n,F) is None
        counts=[brute(n,F)]; check(n,F,B=B,ref=counts[0]); hist['UNSAT']+=1
        for i,t in enumerate(ts):
            for b in (0,1):
                G=F[:i]+F[i+1:]; O=[full(t,7*b)]; c=brute(n,G,O); counts.append(c)
                check(n,G,O,B,ref=c); hist['SAT']+=1
        out[name]={'root_and_neighbor_counts':counts,'raw_root':'UNKNOWN','modulator':B}
    # Random signed triangles on stacked planar triangulations.
    a=collections.Counter(); exact=0
    for _ in range(100):
        n=rng.randrange(4,10); faces=[(0,1,2),(0,1,3),(0,2,3),(1,2,3)]; ts=faces[:]
        for v in range(4,n):
            i=rng.randrange(len(faces)); x,y,z=faces.pop(i); new=[(x,y,v),(x,z,v),(y,z,v)]; faces+=new; ts+=new
        F=[full(rng.choice(ts),rng.randrange(8)) for j in range(rng.randrange(n,3*n+1))]
        ref=brute(n,F); a['SAT' if check(n,F,ref=ref) else 'UNSAT']+=1
        ans=planar_energy(range(n),F); assert ans is not None
        e=min(4*sum(len({(x>>v&1)^s for v,s in f})==1 for f in F) for x in range(2**n)); assert e==ans[0]; exact+=1
    out['random_planar']={**a,'minimum_energy_checks':exact}
    # A wheel whose two sign channels require opposite rim bits. One budget relaxation permits one equal pair.
    scales=[]
    for r in (5,17,65,129):
        F=[full((0,i+1,(i+1)%r+1),s) for i in range(r) for s in (0,1)]
        check(r+1,F,ref=0); check(r+1,F[1:],O=[full((0,1,2),0)],ref=1)
        scales.append({'rim':r,'vertices':r+1,'owners':2*r,'root':'UNSAT','neighbor':'SAT'})
    out['signed_wheels']=scales
    # Loose cycles have Berge girth r, independent private third bits; exact SAT control.
    for r in (7,31,127):
        F=[full((i,(i+1)%r,r+i),rng.randrange(8)) for i in range(r)]
        check(2*r,F,ref=1)
    out['loose_cycle_girths']=[7,31,127]
    # Cofacial 3-port projections, signed random stacked planar cores: all 4 relative words.
    fibers=0; proper=0
    for _ in range(40):
        n=5; ts=[(0,1,2),(0,1,3),(0,2,3),(1,2,3),(0,1,4),(0,3,4),(1,3,4)]
        F=[full(rng.choice(ts),rng.randrange(8)) for j in range(rng.randrange(3,10))]; support=[]
        for b,c in it.product((0,1),repeat=2):
            pins=((0,0),(1,b),(2,c)); support.append(check(n,F,pins=pins)); fibers+=1
        proper+=0<sum(support)<4
    out['boundary']={'queries':fibers,'proper_nonempty_supports':proper}
    out['common_benchmarks']=dict(hist); out['ledger']=dict(L); out['seed']=2081240; out['networkx']=nx.__version__
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__': run()
