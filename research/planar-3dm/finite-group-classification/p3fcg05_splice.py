from p3fcg05_audit import incidence, closure
import itertools as it, json, collections as co
import networkx as nx

BASE=[(0,0,0),(0,0,1),(0,1,0),(1,0,1),(1,1,0),(1,1,1)]

def family(k):
    # Central units 0..k-1, leaves k..2k-1; triples indexed in binary order.
    T=[tuple(2*i+v for v in t) for i in range(2*k) for t in BASE]
    def swap(i,j,c):
        a,b=list(T[i]),list(T[j]);a[c],b[c]=b[c],a[c];T[i],T[j]=tuple(a),tuple(b)
    for i in range(k-1):swap(6*i+5,6*(i+1),1)
    for i in range(k):swap(6*i+1,6*(k+i)+1,2)
    return T

def witness(k,T,bits):
    # B=001,110, C=010,101. Y-swapped A=000,111 never selected here.
    ids=[6*i+j for i in range(2*k) for j in ((1,4) if bits[i%k] else (2,3))]
    W=[T[i] for i in ids];assert len(W)==4*k and all(len({t[c] for t in W})==4*k for c in range(3))
    return ids

def cut_atoms(G):
    # Deterministic bridge search per deleted edge. No bridge in the admitted graph.
    verts=list(G);idx={v:i for i,v in enumerate(verts)};edges=list(G.edges);adj=[[] for v in verts]
    for e,(u,v) in enumerate(edges):
        u,v=idx[u],idx[v];adj[u].append((v,e));adj[v].append((u,e))
    def bridges(skip):
        tin=[-1]*len(verts);low=[0]*len(verts);clock=0;out=[]
        for root in range(len(verts)):
            if tin[root]>=0:continue
            tin[root]=low[root]=clock;clock+=1;stack=[(root,-1,-1,0)]
            while stack:
                u,p,pe,j=stack[-1]
                if j==len(adj[u]):
                    stack.pop()
                    if p>=0:
                        if low[u]>tin[p]:out.append(pe)
                        low[p]=min(low[p],low[u])
                    continue
                stack[-1]=(u,p,pe,j+1);v,e=adj[u][j]
                if e in (skip,pe):continue
                if tin[v]>=0:low[u]=min(low[u],tin[v]);continue
                tin[v]=low[v]=clock;clock+=1;stack.append((v,u,e,0))
        return out
    if bridges(-1):return None
    cut=set()
    for e in range(len(edges)):
        other=bridges(e)
        if other:cut.add(e);cut.update(other)
    H=G.copy();H.remove_edges_from(edges[e] for e in cut)
    atoms=list(nx.connected_components(H));owner={v:i for i,A in enumerate(atoms) for v in A};Q=nx.Graph();Q.add_nodes_from(range(len(atoms)));ports={}
    for e in cut:
        u,v=edges[e];a,b=owner[u],owner[v]
        if a==b:return None
        q=tuple(sorted((a,b)));ports.setdefault(q,[]).append(e);Q.add_edge(*q)
    if not nx.is_forest(Q) or any(len(es)!=2 for es in ports.values()):return None
    return atoms,owner,Q,ports,edges

def solve(n,T):
    V=[set(range(n)) for _ in range(3)];G=incidence(dict(enumerate(T)),V)
    if not nx.check_planarity(G)[0]:return 'INVALID',None,{}
    A=cut_atoms(G)
    if A is None:return 'UNKNOWN',None,{}
    atoms,owner,Q,ports,edges=A;tab={};max_rows=0
    for a,C in enumerate(atoms):
        triples=sorted(v for c,v in C if c==3);elements=[(c,v) for c,v in C if c!=3]
        incident=sorted(e for b in Q[a] for e in ports[tuple(sorted((a,b)))])
        if len(triples)+len(incident)>16:return 'UNKNOWN',None,{}
        ext={}
        for e in incident:
            u,v=edges[e];u=u if u in C else v;ext.setdefault(u,[]).append(e)
        rows=[]
        for s in it.product((0,1),repeat=len(triples)):
            bits=dict(zip(triples,s))
            for p in it.product((0,1),repeat=len(incident)):
                B=dict(zip(incident,p))
                if any(B[e]!=bits[t] for t in triples for e in ext.get((3,t),[])):continue
                if any(sum(bits[v] for c,v in G[u] if (c,v) in C)+sum(B[e] for e in ext.get(u,[]))!=1 for u in elements):continue
                rows.append((B,{t for t in triples if bits[t]}))
        tab[a]=rows;max_rows=max(max_rows,len(rows))
    def rec(a,parent):
        children={b:rec(b,a) for b in Q[a] if b!=parent};out={}
        for B,W in tab[a]:
            child=[]
            for b,M in children.items():
                key=tuple(B[e] for e in sorted(ports[tuple(sorted((a,b)))]))
                if key not in M:break
                child.append(M[key])
            else:
                key=() if parent is None else tuple(B[e] for e in sorted(ports[tuple(sorted((a,parent)))]))
                out.setdefault(key,W.union(*child))
        return out
    W=set();metrics={'atoms':len(atoms),'cut_edges':sum(map(len,ports.values())),'max_vertices':max(map(len,atoms)),'max_rows':max_rows}
    for C in nx.connected_components(Q):
        r=rec(min(C),None)
        if () not in r:return 'NO',None,metrics
        W|=r[()]
    assert len(W)==n and all(len({T[i][c] for i in W})==n for c in range(3))
    return 'YES',W,metrics

def main():
    base=BASE;G=incidence(dict(enumerate(base)),[set(range(2)) for _ in range(3)])
    assert nx.edge_connectivity(G)==3 and nx.check_planarity(G)[0]
    # All subsets of the three designated incidence edges deleted inside a core.
    port=[((3,0),(1,0)),((3,5),(1,1)),((3,1),(2,1))]
    for mask in range(8):
        H=G.copy();H.remove_edges_from(e for j,e in enumerate(port) if mask>>j&1);assert nx.is_connected(H)
    out={'base_edge_connectivity':3,'core_deletion_checks':8,'scales':[]}
    for k in [2,4,8,16,32,64]:
        T=family(k);V=[set(range(4*k)) for _ in range(3)];G=incidence(dict(enumerate(T)),V);assert nx.check_planarity(G)[0]
        R=closure(4*k,T);assert R is not None and len(R[0])==len(T)
        if k<=8:
            masks=set()
            for bits in it.product((0,1),repeat=k):
                W=witness(k,T,bits);masks.add(frozenset(T[i][2] for i in W if i<6*k))
            assert len(masks)==2**k
        for j in range(k):witness(k,T,[int(i==j) for i in range(k)])
        decision,W,m=solve(4*k,T);assert decision=='YES' and m['atoms']==2*k and m['max_vertices']==12 and m['cut_edges']==2*(2*k-1)
        # Source SAT/NO neighbor: force A in unit 0, then forbid A in last central unit.
        A=[t for i,t in enumerate(T) if i not in {1,2}]
        B=[t for i,t in enumerate(T) if i not in {1,2,6*(k-1)+5}]
        # Explicit A witness, every leaf uses C.
        ids=[6*i+j for i in range(k) for j in (0,5)]+[6*i+j for i in range(k,2*k) for j in (2,3)]
        W0=[T[i] for i in ids];assert set(W0)<=set(A) and all(len({t[c] for t in W0})==4*k for c in range(3))
        assert closure(4*k,A) is not None and closure(4*k,B) is None
        out['scales'].append({'k':k,'triples':len(T),'actual_masks':str(2**k),'enumerated_masks':2**k if k<=8 else None,'neighbor_sizes':[len(A),len(B)],**m})
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
