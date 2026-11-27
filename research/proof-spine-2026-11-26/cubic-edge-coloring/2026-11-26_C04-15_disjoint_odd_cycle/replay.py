"""C04-15 portable matching-first replay. Python 3 + NetworkX.
Search core and independent verifier executed locally; this standalone wrapper in repo is a repackaging of that core. All caps return UNKNOWN, not NO.
"""
import networkx as nx
import json

DOT8=[(10,21),(6,20),(10,16),(12,20),(12,21),(11,14),(19,24),(4,14),(11,13),(0,5),(2,17),(16,22),(14,25),(3,24),(16,23),(7,13),(7,25),(4,20),(12,17),(7,8),(0,2),(8,15),(4,9),(18,19),(3,9),(13,18),(5,11),(3,23),(17,19),(9,22),(2,6),(5,8),(1,15),(1,22),(1,24),(15,23),(6,10),(0,18),(21,25)]
IDS=['QGeA@GUAp??@_@O?A???Q?@W?Ao','QHeA@GEAo_?@_@O??C??Q?@W?Ao']

def run(G,E,depth,cap):
    idx={e:i for i,e in enumerate(E)};cache={};proof={};calls=nodes=0
    def oracle(P,F):
        nonlocal calls
        key=(P,F)
        if key in cache:return cache[key]
        V=[v for i in P for v in E[i]]
        if set(P)&set(F) or len(set(V))!=len(V):cache[key]=None;return None
        calls+=1
        if calls>cap:raise RuntimeError('matching cap')
        H=G.copy();H.remove_edges_from(E[i] for i in F);H.remove_nodes_from(V)
        M=nx.max_weight_matching(H,maxcardinality=True)
        cache[key]=None if len(M)*2!=len(H) else set(P)|{idx[tuple(sorted(e))] for e in M}
        return cache[key]
    def rec(P,F,d):
        nonlocal nodes
        nodes+=1;key=(P,F)
        if key in proof:return True
        M=oracle(P,F)
        if M is None:proof[key]=None;return True
        H=G.copy();H.remove_edges_from(E[i] for i in M)
        Cs=sorted([tuple(sorted(idx[tuple(sorted(e))] for e in H.subgraph(V).edges)) for V in nx.connected_components(H) if len(V)%2],key=lambda c:(len(c),c))
        if not Cs:return False
        candidates=[]
        for C in Cs:
            live=[];prev=set(F)
            for i in C:
                T=tuple(sorted((*P,i)));U=tuple(sorted(prev));prev.add(i)
                if oracle(T,U) is None:proof[T,U]=None
                else:live.append((T,U))
            if not live:proof[key]=C;return True
            candidates.append((len(live),C,live))
        if d==0:return False
        for _,C,live in sorted(candidates):
            if all(rec(T,U,d-1) for T,U in live):proof[key]=C;return True
        return False
    try:status='NO' if rec((),(),depth) else 'UNKNOWN'
    except RuntimeError:status='UNKNOWN_CAP'
    def extract(P,F,D):
        key=(P,F)
        if key in D:return
        C=proof[key];D[key]=C
        if C is None:return
        prev=set(F)
        for i in C:
            T=tuple(sorted((*P,i)));U=tuple(sorted(prev));prev.add(i);extract(T,U,D)
    D={}
    if status=='NO':extract((),(),D)
    return {'status':status,'depth':depth,'matching_queries':calls,'nodes':nodes,'proof_size':len(D),'proof':[[list(P),list(F),None if C is None else list(C)] for (P,F),C in D.items()]}

def verify(E,D):
    G=nx.Graph(E);D={(tuple(P),tuple(F)):C for P,F,C in D};visited=set();leafnodes=0
    def match_exists(P,F):
        nonlocal leafnodes
        V=[v for i in P for v in E[i]]
        if set(P)&set(F) or len(set(V))!=len(V):return False
        H=G.copy();H.remove_edges_from(E[i] for i in F);H.remove_nodes_from(V)
        def go(V):
            nonlocal leafnodes
            leafnodes+=1
            if leafnodes>1000000:raise RuntimeError('audit cap')
            if not V:return True
            u=min(V,key=lambda v:(len(set(H[v])&V),v))
            return any(go(V-{u,v}) for v in sorted(set(H[u])&V))
        return go(set(H))
    def go(P,F):
        key=(P,F)
        if key in visited:return
        visited.add(key);C=D[key]
        if C is None:assert not match_exists(P,F);return
        H=nx.Graph(E[i] for i in C)
        assert len(C)%2 and len(C)>=3 and nx.is_connected(H) and all(d==2 for _,d in H.degree())
        assert not set(P)&set(C)
        prev=set(F)
        for i in C:
            T=tuple(sorted((*P,i)));U=tuple(sorted(prev));prev.add(i);go(T,U)
    go((),());assert len(D)==len(visited)
    return {'verified_nodes':len(visited),'independent_leaf_search_nodes':leafnodes}

if __name__=='__main__':
    graphs=[('Dot8',nx.Graph(DOT8)),*(('Dot'+str(i),nx.from_graph6_bytes(s.encode())) for i,s in enumerate(IDS)),('Petersen',nx.petersen_graph()),('K4-control',nx.complete_graph(4))]
    out=[]
    for name,G in graphs:
        E=sorted(tuple(sorted(e)) for e in G.edges)
        G=nx.Graph(E);runs=[]
        for d in (1,2,3,4,5):
            q=run(G,E,d,10000)
            if q['status']=='NO':q['audit']=verify(E,q['proof'])
            runs.append(q)
            print(name,{k:v for k,v in q.items() if k!='proof'})
            if q['status']=='NO':break
        out.append({'name':name,'edges':E,'runs':runs})
    with open('disjoint_replay.json','w') as f:json.dump(out,f,indent=2)
