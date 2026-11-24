import networkx as nx, random, json, itertools, collections, time
from fractions import Fraction
C=collections.Counter()

def pf(A):
    A=[list(map(Fraction,r)) for r in A]; n=len(A); out=Fraction(1)
    for k in range(0,n,2):
        j=next((j for j in range(k+1,n) if A[k][j]),None)
        if j is None:return 0
        if j!=k+1:
            A[j],A[k+1]=A[k+1],A[j]
            for row in A:row[j],row[k+1]=row[k+1],row[j]
            out=-out
        p=A[k][k+1];out*=p; C['pf_pivots']+=1
        for i in range(k+2,n):
            for j in range(i+1,n):
                A[i][j]-=(A[k][i]*A[k+1][j]-A[k][j]*A[k+1][i])/p
                A[j][i]=-A[i][j]; C['pf_updates']+=1
    assert out.denominator==1
    return int(out)

def orient(G):
    ok,emb=nx.check_planarity(G); assert ok
    ori={tuple(sorted(e)):1 for e in G.edges}; faces=[]; f={};seen=set()
    for u,v in emb.edges():
        if (u,v) in seen:continue
        face=emb.traverse_face(u,v,seen); h=list(zip(face,face[1:]+face[:1])); i=len(faces);faces.append(h)
        for a,b in h:f[a,b]=i
    D=nx.Graph();D.add_nodes_from(range(len(faces)))
    for u,v in G.edges:
        if f[u,v]!=f[v,u]:D.add_edge(f[u,v],f[v,u],edge=tuple(sorted((u,v))))
    for comp in nx.connected_components(D):
        root=min(comp);tree=nx.bfs_tree(D,root)
        for i in reversed(list(tree)):
            if i==root:continue
            p=next(tree.predecessors(i))
            parity=sum(ori[tuple(sorted((a,b)))]==(1 if a<b else -1) for a,b in faces[i])%2
            if not parity:ori[D[i][p]['edge']]*=-1
    return ori

class Kernel:
    def __init__(self,n,edges):
        self.n=n; self.edges=edges; G=nx.Graph();G.add_nodes_from(range(n));G.add_edges_from(edges)
        ok,E=nx.check_planarity(G);assert ok
        self.paths=[];self.components=[]
        for comp in nx.connected_components(G):
            root=min(comp); self.components.append(sum(1<<v for v in comp));
            for v in comp:
                p=nx.shortest_path(G,root,v); self.paths.append((v,sum(1<<edges.index(tuple(sorted(e))) for e in zip(p,p[1:]))))
        # Split each vertex along its cyclic order into a path of bags of <=3 ports.
        H=nx.Graph(); port={};aux=[]; serial=0
        def fresh():
            nonlocal serial
            v=serial;serial+=1;H.add_node(v);return v
        for u in G:
            nbr=list(E.neighbors_cw_order(u)); d=len(nbr)
            if not d:continue
            bags=[nbr] if d<=3 else [nbr[:2]]+[[v] for v in nbr[2:-2]]+[nbr[-2:]]
            last=None
            for i,bag in enumerate(bags):
                ports=[]
                if last is not None:
                    p=fresh();ports.append(p);aux.append((last,p))
                for v in bag:p=fresh();port[u,v]=p;ports.append(p)
                if i+1<len(bags):last=fresh();ports.append(last)
                H.add_edges_from(itertools.combinations(ports,2))
        self.links=[]
        for u,v in [ (port[u,v],port[v,u]) for u,v in edges]+aux:
            a,b=fresh(),fresh();H.add_edges_from([(u,a),(a,b),(b,v)]);self.links.append((tuple(sorted((u,a))),tuple(sorted((a,b)))))
        self.H=H; self.ori=orient(H);self.size=serial; C['compiled_vertices']+=serial;C['compiled_edges']+=H.number_of_edges()
        # All-unselected pattern exists, hence common matching sign is nonzero.
        self.sign=1 if self.eval_raw({})>0 else -1
    def eval_raw(self,weights):
        A=[[0]*self.size for _ in range(self.size)]
        for (u,v),s in self.ori.items():A[u][v]=s*weights.get((u,v),1);A[v][u]=-A[u][v]
        C['pf_calls']+=1
        return pf(A)
    def character(self,a,ab):
        if any((a&c).bit_count()%2 for c in self.components):return 0
        twist=0
        for v,p in self.paths:
            if a>>v&1:twist^=p
        weights={}
        for i,(A,B) in enumerate(ab):
            if twist>>i&1:A,B=B,A
            e0,e1=self.links[i];weights[e0]=A;weights[e1]=B
        val=self.sign*self.eval_raw(weights)
        d=self.n-len(self.edges)
        if d>=0:return val<<d
        assert val%(1<<(-d))==0
        return val//(1<<(-d))
    def query(self,costs,guards=(),masks=None):
        C['queries']+=1; B=1<<(self.n+1); W=sum(max(c) for c in costs)
        masks=masks or [3]*len(costs)
        ab=[]
        for (c0,c1),mask in zip(costs,masks):
            a=B**c0 if mask&1 else 0;b=B**c1 if mask&2 else 0;ab.append((a+b,a-b))
        # Reduce affine rows, rejecting inconsistency; keep original source coordinates.
        piv={}
        for a,b in guards:
            while a and a.bit_length()-1 in piv:
                v,w=piv[a.bit_length()-1];a^=v;b^=w
            if not a:
                if b:return [0]*(W+1)
            else:piv[a.bit_length()-1]=(a,b)
        rows=list(piv.values()); val=0
        for word in range(1<<len(rows)):
            a=b=0
            for i,(v,w) in enumerate(rows):
                if word>>i&1:a^=v;b^=w
            val+=(-1 if b else 1)*self.character(a,ab); C['character_terms']+=1
        assert val%(1<<len(rows))==0;val//=1<<len(rows);assert val>=0
        out=[]
        for _ in range(W+1):out.append(val%B);val//=B
        assert val==0
        return out

def brute(n,edges,costs,guards=(),masks=None):
    out=[0]*(sum(max(c) for c in costs)+1);masks=masks or [3]*len(edges)
    for x in range(1<<n):
        C['reference_assignments']+=1
        if any((a&x).bit_count()%2!=b for a,b in guards):continue
        z=[((x>>u)^(x>>v))&1 for u,v in edges]
        if all(m>>i&1 for m,i in zip(masks,z)):out[sum(c[i] for c,i in zip(costs,z))]+=1
    return out

def lift(K,costs,guards):
    # Exact zero-cost support closure, before and after each forced edge; then branch only inside a witnessed nonempty fiber.
    masks=[3]*len(costs)
    def close():
        while True:
            C['closure_passes']+=1
            if not K.query(costs,guards,masks)[0]:return False
            changed=False
            for i,m in enumerate(masks):
                if m!=3:continue
                for b in (0,1):
                    test=masks[:];test[i]=1<<b
                    if not K.query(costs,guards,test)[0]:
                        masks[i]=1<<(1-b);C['forced_edges']+=1;changed=True;break
                if changed:break
            if not changed:return True
    if not close():return None
    for i,m in enumerate(masks):
        if m==3:
            masks[i]=1;C['witness_pins']+=1;assert close()
    # Solve affine edge equations and guards; no accumulating external guard rank in the kernel.
    piv={}
    for a,b in list(guards)+[((1<<u)^(1<<v),m==2) for (u,v),m in zip(K.edges,masks)]:
        while a and a.bit_length()-1 in piv:
            v,w=piv[a.bit_length()-1];a^=v;b^=w
        if a:piv[a.bit_length()-1]=(a,b)
        else:assert not b
    x=0
    for k,(a,b) in sorted(piv.items()):
        if (a&x).bit_count()%2!=b:x|=1<<k
    assert all((a&x).bit_count()%2==b for a,b in guards)
    assert sum(c[((x>>u)^(x>>v))&1] for (u,v),c in zip(K.edges,costs))==0
    return x

def run():
    rng=random.Random(20261124); results=[]; start=time.monotonic()
    for i in range(30):
        n=rng.randrange(3,7);G=nx.Graph();G.add_nodes_from(range(n));ee=list(itertools.combinations(range(n),2));rng.shuffle(ee)
        for e in ee[:rng.randrange(1,len(ee)+1)]:
            G.add_edge(*e)
            if not nx.check_planarity(G)[0]:G.remove_edge(*e)
        edges=sorted(tuple(sorted(e)) for e in G.edges);K=Kernel(n,edges)
        # Hard signed equality/disequality or soft zero/one/two energies.
        costs=[rng.choice([(0,1),(1,0),(0,0),(0,2),(2,0)]) for e in edges]
        for j in range(4):
            guards=[(rng.randrange(1,1<<n),rng.randrange(2)) for _ in range(j%3)]
            masks=[rng.choice([1,2,3,3]) for e in edges] if j==3 else None
            got=K.query(costs,guards,masks);ref=brute(n,edges,costs,guards,masks);assert got==ref
            C['spectra']+=1;C['zero_sat' if got[0] else 'zero_unsat']+=1
        if i<5:
            guards=[(rng.randrange(1,1<<n),rng.randrange(2))];ref=brute(n,edges,costs,guards);w=lift(K,costs,guards);assert (w is not None)==bool(ref[0]);C['lift_controls']+=1
        results.append({'n':n,'edges':edges,'costs':costs})
    # Nonedge guard: host path 0-1-2-3, quartic conditioned by x0+x2, remaining pair (1,3) absent.
    # Use host edges 0-1,1-3,3-2: guard (0,2) absent, complement (1,3) present.
    edges=[(0,1),(1,3),(2,3)];K=Kernel(4,edges)
    for g in (0,1):
        costs=[(0,0),(g,1-g),(0,0)] # penalty 1 iff total parity is 1
        got=K.query(costs,[(5,g)]);assert got==brute(4,edges,costs,[(5,g)]);assert got[0]==4
        C['nonhost_guard_controls']+=1
    # Actual witness branching with nonhost affine guard and no initially forced edge.
    K=Kernel(4,[(0,1),(1,2),(2,3)]); costs=[(0,0)]*3
    w=lift(K,costs,[(9,1)]); assert w is not None; C['lift_controls']+=1
    # Fano NAE source reference only: K7 not planar, one-owner relaxations not symmetric.
    fano=[(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
    counts=[]
    for drop in [-1]+list(range(14)):
        counts.append(sum(all(k==drop or any(((x>>v)&1)==(k%2) for v in fano[k//2]) for k in range(14)) for x in range(128)))
    assert counts==[0]+[5]*14
    assert not nx.check_planarity(nx.complete_graph(7))[0]
    print(json.dumps({'seed':20261124,'counts':dict(C),'fano_reference':counts,'cases':results,'networkx':nx.__version__},sort_keys=True))
if __name__=='__main__':run()
