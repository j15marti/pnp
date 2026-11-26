import itertools as I, json, networkx as nx
from fractions import Fraction as F
from functools import lru_cache

def signature(S):
    if not S:return {}
    p=next(iter(S)).bit_count()%2
    if any(x.bit_count()%2!=p for x in S):return None
    N={x^p for x in S}; A=[(0,15),(5,10)];B=[(3,12),(6,9)]
    a=[(x,y) for x,y in A if x in N and y in N]; b=[(x,y) for x,y in B if x in N and y in N]
    if bool(a)!=bool(b):return None
    w={x:1 for x in N}
    if a:
        for x,y in a:w[x]=len(b)
        for x,y in b:w[x]=len(a)
    return {x^p:v for x,v in w.items()}

def gadget(w):
    # Normalize a nonzero entry to all ports removed; planarized K4.
    a=min(w); flip=15^a; v={x^flip:F(y,w[a]) for x,y in w.items()}
    E={}; ports=list(range(4)); n=10
    def add(i,j,z):
        if z:E[tuple(sorted((i,j)))]=F(z)
    for i,j in [(0,1),(1,2),(2,3),(0,3)]:add(i,j,v.get(15^(1<<i)^(1<<j),0))
    for i,j,z in [(4,5,1),(4,8,1),(5,9,1),(8,9,-1),(8,7,1),(9,6,1),(7,6,1)]:add(i,j,z)
    for i in range(4):add(i,4+i,v.get(15^(1<<i)^(1<<(i+2)),0) if i<2 else 1)
    for i in range(4):
        if flip>>i&1:add(i,n,1);ports[i]=n;n+=1
    add(n,n+1,w[a]);n+=2
    @lru_cache(None)
    def pm(mask):
        if not mask:return F(1)
        i=(mask&-mask).bit_length()-1; rem=mask^(1<<i)
        return sum((z*pm(rem^(1<<j)) for (ii,j),z in E.items() if ii==i and rem>>j&1),F(0))
    G=nx.Graph();G.add_nodes_from(range(n));G.add_edges_from(E);assert nx.check_planarity(G)[0]
    return {s:pm(((1<<n)-1)^sum(1<<ports[i] for i in range(4) if s>>i&1)) for s in range(16)}

def all_masks():
    stats=[]
    for p in (0,1):
        W=[x for x in range(16) if x.bit_count()%2==p];ok=bad=0
        for m in range(1,256):
            S={x for i,x in enumerate(W) if m>>i&1};w=signature(S)
            if w is None:bad+=1;continue
            ok+=1;g=gadget(w);assert all(g[x]==w.get(x,0) for x in range(16))
        stats.append([p,ok,bad])
    return stats

Q=[t for t in I.product(range(2),repeat=3) if t not in [(0,0,0),(1,1,1)]]
S=[(0,0,2),(0,2,0),(0,2,2),(1,0,1),(1,1,0),(1,1,1),(2,0,1),(2,1,0),(2,2,2)]
U=[(0,0,2),(0,1,1),(0,3,0),(1,1,2),(1,1,3),(1,2,3),(2,0,1),(2,2,2),(2,2,3),(3,0,0),(3,3,0),(3,3,1)]
V=[tuple(map(int,t)) for t in '000 002 010 011 021 022 100 101 111 201 202 221'.split()]
def graph(T):
    G=nx.Graph();G.add_edges_from((('t',i),(c,v)) for i,t in enumerate(T) for c,v in enumerate(t));return G

def closure_stagnant(T):
    n=max(max(t) for t in T)+1;assert len(set(T))==len(T)
    assert min(graph(T).degree(v) for v in graph(T) if v[0]!='t')>=2
    for c,d in I.combinations(range(3),2):
        for t in T:
            A=[(c,i) for i in range(n) if i!=t[c]];B=[(d,i) for i in range(n) if i!=t[d]]
            G=nx.Graph();G.add_nodes_from(A+B);G.add_edges_from(((c,u[c]),(d,u[d])) for u in T if u[c]!=t[c] and u[d]!=t[d]);assert len(nx.bipartite.maximum_matching(G,top_nodes=A))==2*(n-1)

def solutions(T):
    n=max(max(t) for t in T)+1
    return {tuple(p) for p in I.combinations(range(len(T)),n) if all(len({T[i][c] for i in p})==n for c in range(3))}

def table(G,R,cut):
    ts=sorted(v for v in R if v[0]=='t');out={}
    for vals in I.product((0,1),repeat=len(ts)):
        a=dict(zip(ts,vals))
        for b in I.product((0,1),repeat=4):
            wire=dict(zip(cut,b))
            if any(t in R and a[t]!=wire[t,e] for t,e in cut):continue
            if all(sum(a[w] if w in R else wire[w,v] for w in G[v])==1 for v in R if v[0]!='t'):
                out[sum(x<<i for i,x in enumerate(b))]=tuple(t[1] for t in ts if a[t])
    return out

def cut_order(G,emb,R,cut):
    t,e=cut[0];start=(t,e) if t in R else (e,t);cur=start;order=[]
    for _ in range(2*G.number_of_edges()+5):
        a,b=cur
        if b not in R:order.append((a,b) if a[0]=='t' else (b,a));cur=(b,a)
        else:cur=(b,emb[b][a]['cw'])
        if cur==start:break
    assert len(order)==4;return order

def cuts(T):
    G=graph(T);p,emb=nx.check_planarity(G);assert p and nx.is_connected(G);closure_stagnant(T)
    E=sorted((a,b) if a[0]=='t' else (b,a) for a,b in G.edges());vertices=list(G);ix={v:i for i,v in enumerate(vertices)};adj=[[] for v in vertices]
    for i,(a,b) in enumerate(E):adj[ix[a]].append((ix[b],i));adj[ix[b]].append((ix[a],i))
    def component(bad):
        seen={0};stack=[0]
        while stack:
            for b,i in adj[stack.pop()]:
                if i not in bad and b not in seen:seen.add(b);stack.append(b)
        return seen
    ref=solutions(T); counts={};example=None;nc=0;pin_checks=0
    for ci in I.combinations(range(len(E)),4):
        R=component(set(ci))
        if len(R)==len(vertices):continue
        cut=[E[i] for i in ci];R={vertices[i] for i in R};C=set(G)-R
        if not nx.is_connected(G.subgraph(C)) or not all((t in R)!=(e in R) for t,e in cut):continue
        cut=cut_order(G,emb,R,cut);L=table(G,R,cut);H=table(G,C,cut);nc+=1
        shared=set(L)&set(H);assert bool(shared)==bool(ref)
        for x in shared:assert tuple(sorted(L[x]+H[x])) in ref
        for side,M in [(R,L),(C,H)]:
            colors=len({e[0] for t,e in cut});w=signature(set(M));key=f'{colors}colors_'+('empty' if not M else 'gate' if w is not None else 'defect');counts[key]=counts.get(key,0)+1
            if w:assert gadget(w)=={x:w.get(x,0) for x in range(16)}
            if w is None and M and colors==2:
                example=example or {'cut':cut,'left':sorted(L),'right':sorted(H)}
            if set(dict(G.degree()).values())=={3}:
                # Any cubic four-cut has a single-port parity backdoor.
                eligible=[]
                for i in range(4):
                    if all(len({x.bit_count()%2 for x in M if x>>i&1==b})<=1 for b in (0,1)):eligible.append(i)
                assert eligible;pin_checks+=1
                if colors==2:assert all(((a&b)|(a&c)|(b&c)) in M for a,b,c in I.product(M,repeat=3))
                # Every conditioned table is a parity-definite <=3-port relation.
                for b in (0,1):
                    J={x for x in M if x>>eligible[0]&1==b};w2=signature(J);assert w2 is not None
                    if w2:assert gadget(w2)=={x:w2.get(x,0) for x in range(16)}
    return {'triples':len(T),'solutions':len(ref),'cuts':nc,'types':counts,'pin_checks':pin_checks,'defect_example':example}

def prism(k):
    # 3-edge-colored planar prism; same cycle colors on both rims.
    cs=[i%2 for i in range(k)]
    if k%2:cs[-1]=2
    g=nx.Graph();colored=[]
    for r in (0,1):
        for i,c in enumerate(cs):colored.append(((r,i),(r,(i+1)%k),c))
    for i in range(k):colored.append(((0,i),(1,i),3-cs[i]-cs[(i-1)%k]))
    ids=[0,0,0];T={(r,i):[None]*3 for r in (0,1) for i in range(k)}
    for a,b,c in colored:
        z=ids[c];ids[c]+=1;T[a][c]=T[b][c]=z;g.add_edge(a,b)
    T=[tuple(t) for t in T.values()];G=graph(T);assert ids==[k]*3 and len(set(T))==2*k and nx.check_planarity(G)[0] and nx.is_connected(G)
    # Pair adjacent rung triples with their shared element; four ports each.
    # The other elements are degree-two complement factors. All wire bits in a
    # consistent connected instance belong to one signed equality class.
    for i in range(k):
        a,b=T[i],T[k+i];same=[c for c in range(3) if a[c]==b[c]];assert len(same)==1
        c=same[0];R={('t',i),('t',k+i),(c,a[c])};cut=[(u,v) if u[0]=='t' else (v,u) for u,v in G.edges() if (u in R)!=(v in R)];assert len(cut)==4
        M=table(G,R,cut);assert len(M)==2 and signature(set(M)) is None
    # Exact-one closure: no units; all projection supports by 2-regularity.
    # Stronger complement propagation (BFS) is the backdoor acquisition.
    assert all(G.degree(v)==2 for v in G if v[0]!='t');sat=nx.is_bipartite(g);assert sat==(k%2==0)
    if sat:
        col=nx.bipartite.color(g);W=[T[i] for i,v in enumerate([(r,j) for r in (0,1) for j in range(k)]) if col[v]];assert len(W)==k and all(len({t[c] for t in W})==k for c in range(3))
    return {'n':k,'triples':2*k,'four_port_defects':k,'signed_classes':1 if sat else 0,'status':'SAT' if sat else 'UNSAT'}

if __name__=='__main__':
    print(json.dumps({'all_masks':all_masks(),'source_cuts':[cuts(T) for T in (Q,S,U,V,V+[(1,1,0)])],'prisms':[prism(k) for k in (4,5,8,9,16,17,32,33,64,65,128,129)]},indent=2))
