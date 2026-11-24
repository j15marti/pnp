import itertools as it, random, json
import networkx as nx

# owner[v] = -1 means mandatory internal vertex. Otherwise a defect port.
# Pair masks constrain (k_i mod 2, k_j mod 2), with color index 2*a+b.
def solve(owner, edges, bounds, pairs, pin=None):
    n=len(owner); G=nx.Graph(); G.add_nodes_from(range(n)); req=set(range(n))
    G.add_edges_from(edges); ports=[]; limits=[]
    if pin is not None:
        v, defect=pin
        if defect:
            G.remove_edges_from(list(G.edges(v)))
    for i,(lo,hi) in enumerate(bounds):
        vs=[v for v,o in enumerate(owner) if o==i]; hi=min(hi,len(vs))
        if lo<0 or hi<lo: return None
        limits.append(lo)
        S=[('s',i,j) for j in range(hi)]; D=[('d',i,j) for j in range(hi-lo)]
        p=('p',i); ports.append(p)
        G.add_nodes_from(S+D+[p]); req.update(S+D)
        G.add_edges_from((v,s) for v in vs for s in S if pin!=(v,0))
        G.add_edges_from(it.product(S,D)); G.add_edges_from(it.combinations(D,2))
        G.add_edges_from((d,p) for d in D)
    for i,j,mask in pairs:
        # Unconditional interval/parity closure before matching.
        for c in range(4):
            if any(not any(x%2==bit for x in range(l,min(u,owner.count(k))+1))
                   for k,bit in ((i,c>>1),(j,c&1)) for l,u in [bounds[k]]):
                mask &= ~(1<<c)
        if not mask: return None
        # actual count parity = owner-port occupancy XOR (lo mod 2)
        s=next(c for c in range(4) if mask>>c&1)
        ts=[]
        for k,shift in ((i,(s>>1)^(limits[i]&1)),(j,(s&1)^(limits[j]&1))):
            p=ports[k]; req.add(p)
            if shift==1: t=p   # triangle occupancy is 1 minus owner-side occupancy
            else:
                t=('t',k); req.add(t); G.add_edge(p,t) # equality of occupancies
            ts.append(t)
        a,b=ts; q=('q',i,j); G.add_node(q)
        for c,e in ((1,(b,q)),(2,(a,q)),(3,(a,b))):
            if mask>>(c^s)&1: G.add_edge(*e)
    for u,v in G.edges: G[u][v]['weight']=int(u in req)+int(v in req)
    M=nx.max_weight_matching(G); covered={v for e in M for v in e}
    if not req<=covered: return None
    internal=[(u,v) for u,v in M if isinstance(u,int) and isinstance(v,int)]
    assert check(owner,edges,bounds,pairs,internal,pin)
    return internal

def check(owner,edges,bounds,pairs,M,pin=None):
    E={frozenset(e) for e in edges}; used=[v for e in M for v in e]
    if len(set(used))!=len(used) or any(frozenset(e) not in E for e in M): return False
    if any(o<0 and v not in used for v,o in enumerate(owner)): return False
    k=[sum(o==i and v not in used for v,o in enumerate(owner)) for i in range(len(bounds))]
    return (all(l<=x<=u for x,(l,u) in zip(k,bounds)) and
            all(mask>>(2*(k[i]%2)+k[j]%2)&1 for i,j,mask in pairs) and
            (pin is None or (pin[0] not in used)==bool(pin[1])))

def all_matchings(n,edges):
    adj=[[] for _ in range(n)]
    for u,v in edges: adj[u].append(v); adj[v].append(u)
    def rec(V,M):
        if not V: yield M; return
        v=min(V); R=V-{v}
        yield from rec(R,M)
        for u in adj[v]:
            if u in R: yield from rec(R-{u},M+[(v,u)])
    return list(rec(set(range(n)),[]))

def main():
    rng=random.Random(82008); stats=dict(seed=82008,networkx=nx.__version__,random_instances=0,decisions=0,sat=0,unsat=0,pin_tests=0,hub_color_tests=0,exchange_tests=0,reference_matchings=0,mask_controls=0,scaling=[])
    def compare(o,e,b,p,ref,pin=None):
        expect=any(check(o,e,b,p,m,pin) for m in ref)
        got=solve(o,e,b,p,pin) is not None
        assert got==expect,(o,e,b,p,pin,expect)
        stats['decisions']+=1; stats['sat' if got else 'unsat']+=1
    for _ in range(240):
        n=rng.randrange(3,9); h=rng.choice([2,4]); o=[rng.randrange(-1,h) for v in range(n)]
        e=[(u,v) for u,v in it.combinations(range(n),2) if rng.random()<.45]
        b=[]
        for i in range(h):
            l=rng.randrange(o.count(i)+1); b.append((l,rng.randrange(l,o.count(i)+2)))
        p=[(i,i+1,rng.randrange(16)) for i in range(0,h,2)]
        ref=all_matchings(n,e); stats['reference_matchings']+=len(ref); stats['random_instances']+=1
        compare(o,e,b,p,ref)
        for i,j,mask in p:
            for c in range(4):
                ps=[(a,z,(m&(1<<c)) if (a,z)==(i,j) else m) for a,z,m in p]
                compare(o,e,b,ps,ref); stats['hub_color_tests']+=1
        # Independently verify the exchange axiom on maximum-cardinality slices.
        feasible=[M for M in ref if all(v in {x for edge in M for x in edge} for v in range(n) if o[v]<0)]
        if feasible:
            k=max(map(len,feasible)); A=set()
            for M in feasible:
                if len(M)==k:
                    used={x for edge in M for x in edge}
                    A.add(tuple(sum(a==i and v not in used for v,a in enumerate(o)) for i in range(h)))
            for x,y in it.product(A,repeat=2):
                for i in range(h):
                    if x[i]>y[i]:
                        assert any(tuple(v-(k==i)+(k==j) for k,v in enumerate(x)) in A for j in range(h) if x[j]<y[j])
                        stats['exchange_tests']+=1
        for v in range(n):
            if o[v]>=0:
                for d in (0,1): compare(o,e,b,p,ref,(v,d)); stats['pin_tests']+=1
    # All masks, both lower-bound parities, exact target counts.
    for l0,l1 in it.product(range(2),repeat=2):
        o=[0,0,1,1]; e=[(0,1),(2,3),(0,2),(1,3)]; ref=all_matchings(4,e)
        for mask in range(16):
            for a,b in it.product(range(l0,3),range(l1,3)):
                # exact counts set lower bound, with independent mask translation
                compare(o,e,[(a,a),(b,b)],[(0,1,mask)],ref); stats['mask_controls']+=1
            compare(o,e,[(l0,2),(l1,2)],[(0,1,mask)],ref); stats['mask_controls']+=1
    # Independent two-spoke regions; precisely one unmatched port per region.
    for B in (8,16,32,64,128):
        o=[x for _ in range(B) for x in (-1,0,1)]; e=[(3*i,3*i+j) for i in range(B) for j in (1,2)]
        b=[(B//2,B//2)]*2; c=3*((B//2)%2)
        assert solve(o,e,b,[(0,1,1<<c)]) is not None
        assert solve(o,e,b,[(0,1,15^(1<<c))]) is None
        stats['scaling'].append(dict(blocks=B,raw_support_power=B,sat=True,unsat=True))
    print(json.dumps(stats,indent=2))
if __name__=='__main__': main()
