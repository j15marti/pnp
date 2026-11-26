import itertools as it, random, json
from collections import defaultdict
from math import prod
import networkx as nx

def faces(g):
    ok,emb=nx.check_planarity(g); assert ok
    seen=set(); fs=[]
    for u,v in emb.edges():
        if (u,v) not in seen: fs.append(emb.traverse_face(u,v,seen))
    return emb,fs

def pf(A):
    A=[r[:] for r in A]; n=len(A); sign=1; prev=1
    if not n:return 1
    for k in range(0,n,2):
        j=next((j for j in range(k+1,n) if A[k][j]),None)
        if j is None:return 0
        if j!=k+1:
            A[j],A[k+1]=A[k+1],A[j]
            for r in A:r[j],r[k+1]=r[k+1],r[j]
            sign=-sign
        a=A[k][k+1]
        for i in range(k+2,n):
            for j in range(i+1,n):
                v=a*A[i][j]-A[k][i]*A[k+1][j]+A[k][j]*A[k+1][i]
                assert v%prev==0
                A[i][j]=v//prev; A[j][i]=-A[i][j]
        prev=a
    return sign*prev

class Even:
    # Weighted even-subgraph sum: each edge has weights for absent,present.
    def __init__(self,g):
        emb,_=faces(g); self.edges=list(g.edges()); ix={frozenset(e):i for i,e in enumerate(self.edges)}
        H=nx.Graph(); wires={i:[] for i in range(len(self.edges))}; nxt=len(wires)
        for v in g:
            es=[ix[frozenset((v,u))] for u in emb.neighbors_cw_order(v)]
            while len(es)>3:
                wires[nxt]=[]; self.city(H,wires,es[:2]+[nxt]); es=[nxt]+es[2:]; nxt+=1
            self.city(H,wires,es)
        self.paths=[]; pairs=[]
        for i,(u,v) in wires.items():
            a=len(H); H.add_node(a); b=len(H); H.add_node(b)
            H.add_edges_from([(u,a),(a,b),(b,v)]); self.paths.append((u,a,b,v)); pairs.extend([(u,a),(b,v)])
        _,fs=faces(H); E=list(H.edges()); ei={frozenset(e):i for i,e in enumerate(E)}; piv={}
        # Odd number of darts agreeing with reference orientation in each bounded face.
        for f in fs[1:]:
            row=0; rhs=1
            for u,v in zip(f,f[1:]+f[:1]):
                j=ei[frozenset((u,v))]; row^=1<<j; rhs^=int(E[j]==(u,v))
            while row:
                j=row.bit_length()-1
                if j not in piv: piv[j]=(row,rhs); break
                r,s=piv[j]; row^=r; rhs^=s
            if not row:assert rhs==0
        bits=0
        for j,(r,s) in sorted(piv.items()):
            if ((r&bits).bit_count()&1)!=s:bits|=1<<j
        self.N=len(H); self.signs={}
        for j,(u,v) in enumerate(E):
            s=1-2*((bits>>j)&1); self.signs[u,v]=s; self.signs[v,u]=-s
        # Reference matching = empty even subgraph, all outer path edges.
        seq=[x for p in pairs for x in p]; assert sorted(seq)==list(range(self.N))
        self.cal=(-1)**sum(a>b for i,a in enumerate(seq) for b in seq[i+1:])*prod(self.signs[p] for p in pairs)
        self.E=E
    @staticmethod
    def city(H,wires,es):
        ports=[]
        for e in es:
            p=len(H);H.add_node(p);ports.append(p);wires[e].append(p)
        H.add_edges_from(it.combinations(ports,2))
    def value(self,weights):
        A=[[0]*self.N for _ in range(self.N)]
        for u,v in self.E:A[u][v]=self.signs[u,v];A[v][u]=-A[u][v]
        for i,(u,a,b,v) in enumerate(self.paths):
            w0,w1=weights[i] if i<len(weights) else (1,1)
            for x,y,w in [(u,a,w0),(a,b,w1)]:A[x][y]=self.signs[x,y]*w;A[y][x]=-A[x][y]
        return self.cal*pf(A)

def count_aligned(g,anchors,base,target,pins=None):
    if target<0:return 0
    ev=Even(g); E=ev.edges; pins=pins or {}; vals=[]
    for u,v in E:
        j=g[u][v]['j']; p=base**(abs(j)+j); q=base**(abs(j)-j)
        if frozenset((u,v)) in pins:
            if pins[frozenset((u,v))]==1:q=0
            else:p=0
        vals.append((p+q,p-q)) # twice high-temperature coefficients
    paths=[]; pos={frozenset(e):i for i,e in enumerate(E)}
    for a in anchors[1:]:
        p=nx.shortest_path(g,anchors[0],a);paths.append(sum(1<<pos[frozenset(e)] for e in zip(p,p[1:])))
    masks=[0]
    for p in paths:masks += [m^p for m in masks]
    total=0
    for m in masks:total+=ev.value([w[::-1] if m>>i&1 else w for i,w in enumerate(vals)])
    # 2^r from spin sum, 2^-|E| from doubled coefficients, 2^-(k-1) from agreement.
    power=len(g)-len(E)-len(paths)
    if power<0: assert total%(1<<-power)==0;total//=1<<-power
    else:total*=1<<power
    assert total>=0
    return total//(base**target)%base

def ref(n,T):
    return sum(len(set(y for x,y,z in W))==n and len(set(z for x,y,z in W))==n for W in it.product(*[[t for t in T if t[0]==x] for x in range(n)]))

def solve(n,T,cap=8):
    # Preserve original IDs. Repeated unit + matching-support closure.
    T=set(T); V={(c,i) for c in range(3) for i in range(n)}; forced=[]
    I=nx.Graph(); I.add_nodes_from(V); I.add_edges_from((t,(c,t[c])) for t in T for c in range(3));assert nx.check_planarity(I)[0]
    while True:
        D={v:{t for t in T if t[v[0]]==v[1]} for v in V}
        if any(not a for a in D.values()):return 0,0,[]
        one=next((next(iter(a)) for a in D.values() if len(a)==1),None)
        if one is not None:
            forced.append(one);V-={(c,one[c]) for c in range(3)};T={t for t in T if all(t[c]!=one[c] for c in range(3))};continue
        bad=set()
        for c,d in it.combinations(range(3),2):
            L={v for v in V if v[0]==c};R={v for v in V if v[0]==d}; G=nx.Graph();G.add_nodes_from(L|R);G.add_edges_from(((c,t[c]),(d,t[d])) for t in T)
            if len(nx.bipartite.maximum_matching(G,top_nodes=L))!=2*len(L):return 0,0,[]
            for t in T:
                u,v=(c,t[c]),(d,t[d]);H=G.copy();H.remove_nodes_from([u,v])
                if len(nx.bipartite.maximum_matching(H,top_nodes=L-{u}))!=2*(len(L)-1):bad.add(t)
        if bad:T-=bad;continue
        break
    if not T:return 1,0,forced
    if max(map(len,D.values()))>3:return None,None,None
    G=nx.Graph();G.add_nodes_from(T)
    for a in D.values():
        if len(a)==2:G.add_edge(*sorted(a))
    if not nx.is_bipartite(G):return 0,0,[]
    phase={};sgn={}
    for i,C in enumerate(nx.connected_components(G)):
        for t,b in nx.bipartite.color(G.subgraph(C)).items():phase[t]=i;sgn[t]=1-2*b
    J=defaultdict(int);h=defaultdict(int);C=0
    for a in D.values():
        if len(a)!=3:continue
        C+=4
        for t in a:h[phase[t]]+=2*sgn[t]
        for t,u in it.combinations(sorted(a),2):
            j=2*sgn[t]*sgn[u]; p,q=phase[t],phase[u]
            if p==q:C+=j
            else:J[tuple(sorted((p,q)))]+=j
    g=nx.Graph();g.add_nodes_from(set(phase.values()));g.add_edges_from((p,q,{'j':j}) for (p,q),j in J.items() if j)
    # connect by zero couplings (bridges) for a single embedding and lift tree
    cs=[min(c) for c in nx.connected_components(g)];g.add_edges_from((a,b,{'j':0}) for a,b in zip(cs,cs[1:]))
    _,fs=faces(g); uncovered={v for v in g if h[v]}; groups=[]
    if len(g)==1 and uncovered:groups=[set(uncovered)];uncovered.clear()
    while uncovered:
        F=max((set(f)&uncovered for f in fs),key=len);assert F;groups.append(F);uncovered-=F
    k=len(groups)
    if k>cap:return None,k,None
    anchors=[]
    for F in groups:
        a=len(g);g.add_node(a);anchors.append(a);g.add_edges_from((a,v,{'j':h[v]}) for v in F)
    assert nx.check_planarity(g)[0]
    B=1<<(len(g)+1);target=sum(abs(d['j']) for _,_,d in g.edges(data=True))-C
    total=count_aligned(g,anchors,B,target); ans=total//(2 if k else 1);assert total==ans*(2 if k else 1)
    if not ans:return 0,k,[]
    pins={};root=anchors[0] if k else next(iter(g)); spins={root:1}
    for u,v in nx.bfs_edges(g,root):
        e=frozenset((u,v));pins[e]=1
        if not count_aligned(g,anchors,B,target,pins):pins[e]=-1
        spins[v]=spins[u]*pins[e]
    W=forced+[t for t in T if spins[phase[t]]*sgn[t]==1];assert len(W)==n and all(len({t[c] for t in W})==n for c in range(3))
    return ans,k,W

def main():
    rng=random.Random(231125); out={'seed':231125,'even_checks':0,'sources':0,'sat':0,'unsat':0,'unknown':0,'max_faces':0,'nontrivial_faces':{},'fixtures':[]}
    for g in [nx.cycle_graph(5),nx.complete_graph(4),nx.octahedral_graph(),nx.path_graph(6)]:
        ev=Even(g);E=ev.edges
        for _ in range(20):
            w=[(rng.randint(-3,3),rng.randint(-3,3)) for e in E];v=0
            for bits in it.product((0,1),repeat=len(E)):
                S=defaultdict(int)
                for (a,b),x in zip(E,bits):S[a]^=x;S[b]^=x
                if not any(S.values()):v+=prod(p[x] for p,x in zip(w,bits))
            assert v==ev.value(w);out['even_checks']+=1
    cube=list(it.product(range(2),repeat=3)); f=(0,0,1);tri=[t for t in cube if t!=f]+[t for t in it.product(*[(f[c],2) for c in range(3)]) if t!=f]
    controls=[(2,[t for i,t in enumerate(cube) if mask>>i&1]) for mask in range(256)]
    controls += [(3,rng.sample(tri,rng.randint(6,12))) for _ in range(150)]
    for n,T in controls:
        if max(sum(t[c]==i for t in T) for c in range(3) for i in range(n))>3:continue
        a,k,W=solve(n,T);r=ref(n,T);out['sources']+=1
        if a is None:out['unknown']+=1;continue
        assert a==r,(T,a,r);out['sat' if a else 'unsat']+=1;out['max_faces']=max(out['max_faces'],k)
        out['nontrivial_faces'][str(k)]=out['nontrivial_faces'].get(str(k),0)+1
        if k>=2 and len(out['fixtures'])<4:out['fixtures'].append({'n':n,'T':T,'count':a,'faces':k,'witness':W})
    print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
