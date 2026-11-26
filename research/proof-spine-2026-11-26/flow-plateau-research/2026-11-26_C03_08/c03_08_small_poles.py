import itertools as it, json, collections, hashlib, time
import networkx as nx
WORDS=[(1,1,1,1),(1,1,2,2),(1,2,1,2),(1,2,2,1)]
PERMS=list(it.permutations((1,2,3)))
CAPQ=[(0,1),(0,5),(1,2),(1,6),(2,7),(3,5),(3,6),(4,6),(4,7),(5,7)]
QPORT=(2,3,0,4)
counts=collections.Counter()
def graphs(n):
    def rec(i,rem,E):
        while i<n and rem[i]==0:i+=1
        if i==n:
            yield tuple(E);return
        choices=[j for j in range(i+1,n) if rem[j]>0]
        for js in it.combinations(choices,rem[i]):
            r=rem.copy();r[i]=0
            for j in js:r[j]-=1
            if all(0<=r[j]<=sum(r[k]>0 for k in range(i+1,n) if k!=j) for j in range(i+1,n)):
                yield from rec(i+1,r,E+[(i,j) for j in js])
    yield from rec(0,[2]*4+[3]*(n-4),[])
def incid(n,E,P):
    inc=[[] for _ in range(n)]
    for k,(u,v) in enumerate(E):inc[u].append(k);inc[v].append(k)
    for k,u in enumerate(P):inc[u].append(len(E)+k)
    assert all(len(x)==3 for x in inc)
    return inc
# A direct local coloring; unit closure, source-indexed original edges.
def direct(n,E,P,w):
    inc=incid(n,E,P); m=len(E); vals=[0]*m+list(w)
    def go():
        counts['direct_nodes']+=1
        used=[];best=None
        for row in inc:
            c=[vals[e] for e in row if vals[e]]
            if len(set(c))!=len(c):return None
        for e,(u,v) in enumerate(E):
            if vals[e]:continue
            allowed=set((1,2,3))-{vals[j] for j in inc[u]+inc[v]}
            if not allowed:return None
            if best is None or len(allowed)<len(best[1]):best=(e,allowed)
        if best is None:return tuple(vals[:m])
        e,allowed=best
        for c in sorted(allowed):
            vals[e]=c;res=go();vals[e]=0
            if res is not None:return res
        return None
    return go()
# B spanning-tree affine reconstruction: exhaustive chord values including zero.
def affine(n,E,P,w):
    g=nx.Graph();g.add_nodes_from(range(n));g.add_edges_from(E)
    tree=nx.minimum_spanning_tree(g);T={tuple(sorted(e)) for e in tree.edges};ch=[i for i,e in enumerate(E) if tuple(sorted(e)) not in T]
    ids={tuple(sorted(e)):i for i,e in enumerate(E)}; parent={v:u for u,v in nx.bfs_edges(tree,0)}
    order=list(nx.bfs_tree(tree,0)); best=999;wit=None
    for vals in it.product(range(4),repeat=len(ch)):
        counts['affine_assignments']+=1
        labels=[0]*len(E);rhs=[0]*n
        for v,c in zip(P,w):rhs[v]^=c
        for e,c in zip(ch,vals):
            labels[e]=c;u,v=E[e];rhs[u]^=c;rhs[v]^=c
        for v in reversed(order[1:]):
            u=parent[v];e=ids[tuple(sorted((u,v)))];labels[e]=rhs[v];rhs[u]^=rhs[v]
        if rhs[0]:continue
        z=labels.count(0)
        if z<best:best=z;wit=tuple(labels)
    return best,wit
# C independent color-1 perfect matching followed by forced color-2/3 parity.
def matching(n,E,P,w):
    inc=incid(n,E,P);m=len(E);fixed={m+i for i,c in enumerate(w) if c==1}
    for mask in range(1<<m):
        counts['matching_masks']+=1
        if mask.bit_count()!=(n-len(fixed))//2:continue
        M=fixed|{e for e in range(m) if mask>>e&1}
        if any(sum(e in M for e in row)!=1 for row in inc):continue
        h=nx.Graph(); h.add_nodes_from(set(range(m+4))-M)
        for row in inc:
            p,q=[e for e in row if e not in M];h.add_edge(p,q)
        if not nx.is_bipartite(h):continue
        b=nx.bipartite.color(h);ok=True
        for C in nx.connected_components(h):
            phases={b[e]^(w[e-m]-2) for e in C if e>=m}
            if len(phases)>1:ok=False;break
        if ok:return True
    return False
def verify(n,E,P,w,labels):
    a=labels+tuple(w)
    return all(a[i]^a[j]^a[k]==0 for i,j,k in incid(n,E,P))
def kempe(n,E,P,w,labels):
    # boundary words fixed; one alternating path from port 0
    m=len(E);a=list(labels)+list(w);c=w[0];d=next(x for x in (1,2,3) if x!=c and x in w) if len(set(w))>1 else (2 if c==1 else 1)
    h=nx.Graph(); h.add_nodes_from(i for i,x in enumerate(a) if x in (c,d))
    for row in incid(n,E,P):
        x,y=[e for e in row if a[e] in (c,d)];h.add_edge(x,y)
    for e in nx.node_connected_component(h,m):a[e]=c^d^a[e]
    assert verify(n,E,P,a[m:],tuple(a[:m])) and 0 not in a
    return tuple(a[m:])
def orbit(w):
    for i,v in enumerate(WORDS):
        if all((w[j]==w[k])==(v[j]==v[k]) for j in range(4) for k in range(4)):return i
    raise ValueError(w)
def main():
    start=time.monotonic();rows={};examples={};finger=hashlib.sha256();ncase=0
    for n in (4,6,8):
        hist=collections.Counter();total=0
        for E in graphs(n):
            counts[f'generated_{n}']+=1
            g=nx.Graph();g.add_nodes_from(range(n));g.add_edges_from(E)
            if not nx.is_connected(g) or any(nx.triangles(g).values()) or list(nx.bridges(g)):continue
            # Internal bridges/triangles cannot occur in cyclically 4-edge-connected nontrivial source.
            total+=1; ncase+=1;P=(0,1,2,3);S=[];finger.update(json.dumps([n,E,P],separators=(',',':')).encode())
            for i,w in enumerate(WORDS):
                A=direct(n,E,P,w);z,B=affine(n,E,P,w);C=matching(n,E,P,w)
                assert (A is not None)==(z==0)==C,(n,E,w,A,z,C)
                assert B is None or verify(n,E,P,w,B)
                if A is not None:
                    assert verify(n,E,P,w,A) and orbit(kempe(n,E,P,w,A))!=i
                    S.append(i)
            assert len(S)!=1
            key=','.join(map(str,S));hist[key]+=1; examples.setdefault(f'{n}:{key}',list(E))
        rows[n]={'admitted':total,'supports':dict(sorted(hist.items()))}
    # same Q source: test every boundary with xor=0, <=1 zero, orbit certificate.
    q=[]
    for w in it.product(range(4),repeat=4):
        if w.count(0)>1 or w[0]^w[1]^w[2]^w[3]:continue
        z,B=affine(8,CAPQ,QPORT,w);assert verify(8,CAPQ,QPORT,w,B)
        if 0 not in w:
            A=direct(8,CAPQ,QPORT,w);C=matching(8,CAPQ,QPORT,w);assert (z==0)==(A is not None)==C
            assert z==(w[0]!=w[1])
        else: assert z==0
        q.append({'boundary':w,'zeros':z,'labels':B})
    out={'rows':rows,'examples':examples,'q_order':CAPQ,'q_ports':QPORT,'q_certificates':q,'counts':dict(counts),'source_fingerprint':finger.hexdigest(),'num_poles':ncase,'elapsed_seconds':time.monotonic()-start}
    print(json.dumps({k:v for k,v in out.items() if k not in ('examples','q_certificates')},indent=2));open('/mnt/data/c03_08_results.json','w').write(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
