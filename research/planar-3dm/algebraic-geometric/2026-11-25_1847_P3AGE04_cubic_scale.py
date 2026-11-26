import itertools as I, json, networkx as nx

def make(k):
    assert k%2==0
    T={v:[None]*3 for v in I.product(range(2),range(k))};labels=[0]*3;top=[];bottom=[];rung=[]
    def e(a,b,c):
        j=labels[c];labels[c]+=1;T[a][c]=T[b][c]=j;return (c,j)
    for i in range(k):
        top.append(e((0,i),(0,(i+1)%k),i%2));bottom.append(e((1,i),(1,(i+1)%k),1-i%2));rung.append(e((0,i),(1,i),2))
    assert labels==[k]*3
    orig=[tuple(t) for t in T.values()];extra=[]
    for i in range(k):
        v=[None]*3
        for c,j in (top[i],bottom[i],rung[i]):v[c]=j
        extra.append(tuple(v))
    return orig,extra

def graft(t,j):
    a,b,c=t
    return [(j,j,j),(a,j,j),(j,b,j),(j,j,c)]

def graph(T,n):
    G=nx.Graph();G.add_nodes_from(I.product(range(3),range(n)));G.add_edges_from((('t',i),(c,v)) for i,t in enumerate(T) for c,v in enumerate(t));return G

def audit(k,unsat):
    orig,extra=make(k);n=k;remove={0,k} if unsat else {0};T=[t for i,t in enumerate(orig) if i not in remove];grafts=[]
    for t in extra+[orig[i] for i in sorted(remove)]:
        start=len(T);T.extend(graft(t,n));grafts.append((n,start));n+=1
    G=graph(T,n);assert len(set(T))==len(T)==3*n and set(dict(G.degree()).values())=={3} and nx.check_planarity(G)[0] and nx.is_connected(G)
    # Exact supplied gadget-region mask: independent enumeration of four internal triples.
    forced=set();forbidden=set()
    for j,start in grafts:
        region={('t',i) for i in range(start,start+4)}|{(c,j) for c in range(3)};assert nx.is_connected(G.subgraph(region))
        ports=[(u,v) for u,v in G.edges() if (u in region)!=(v in region)];assert len(ports)==3
        states=[]
        for b in I.product((0,1),repeat=4):
            if all(sum(b[i] for i,t in enumerate(T[start:start+4]) if t[c]==j)==1 for c in range(3)):states.append(b)
        assert states==[(1,0,0,0)];forced.add(start);forbidden.update(range(start+1,start+4))
    # All projections support every indexed edge by cubic regularity. Verify one
    # perfect matching per lane and the required degrees (the proof gives full support).
    for c,d in I.combinations(range(3),2):
        A=[(c,i) for i in range(n)];B=[(d,i) for i in range(n)];H=nx.Graph();H.add_nodes_from(A+B);H.add_edges_from(((c,t[c]),(d,t[d])) for t in T);assert len(nx.bipartite.maximum_matching(H,top_nodes=A))==2*n
    # Unit propagation after the exact mask deductions, retaining actual IDs.
    live=set(range(len(T)))-forbidden;selected=set();remaining=set(I.product(range(3),range(n)));steps=0
    while remaining:
        by={v:[] for v in remaining}
        for i in live:
            for c,v in enumerate(T[i]):
                if (c,v) in by:by[c,v].append(i)
        if any(not a for a in by.values()):status='UNSAT';break
        unit=next((a[0] for a in by.values() if len(a)==1),None)
        if unit is None:status='UNKNOWN';break
        selected.add(unit);steps+=1;remaining-={(c,v) for c,v in enumerate(T[unit])};live={i for i in live if all(T[i][c]!=T[unit][c] for c in range(3))}
    else:status='SAT'
    assert status==('UNSAT' if unsat else 'SAT')
    if status=='SAT':assert forced<=selected and len(selected)==n and all(len({T[i][c] for i in selected})==n for c in range(3))
    return {'rim':k,'elements_per_color':n,'triples':len(T),'initial_projection_support':'all (cubic)','exact_zero_caps':len(grafts),'status':status,'unit_steps':steps}

if __name__=='__main__':print(json.dumps([audit(k,u) for k in (4,8,16,32,64,128) for u in (False,True)],indent=2))
