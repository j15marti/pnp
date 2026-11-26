"""Independent nested-Q construction; source edge IDs are list indices.
Run with c03_08_small_poles.py in same directory. No external graph data.
"""
import json, hashlib, collections, itertools, random, time
import networkx as nx
from c03_08_small_poles import affine, direct, verify, CAPQ, QPORT
class Builder:
    def __init__(self):self.n=0;self.E=[];self.f=[];self.c=[];self.groups=[];self.regions=[]
    def v(self):v=self.n;self.n+=1;return v
    def edge(self,u,v,f,c=None):
        self.E.append((u,v));self.f.append(f);self.c.append(f if c is None else c);return len(self.E)-1
    def q(self,p):
        vv=[self.v() for _ in range(8)];w=(1,1,p,p);a=direct(8,CAPQ,QPORT,w);assert a is not None
        for (u,v),x in zip(CAPQ,a):self.edge(vv[u],vv[v],x)
        return [vv[i] for i in QPORT],vv
    def make(self,k):
        A,V=self.q(1);B,W=self.q(2);self.groups.append(V+W)
        u,v,w=[self.v() for _ in range(3)]
        for j,t in [(2,u),(3,v)]:self.edge(A[j],t,1);self.edge(B[j],t,2)
        bad1=self.edge(u,w,3);self.edge(v,w,3)
        old=[A[0],A[1],B[0],B[1],w];self.regions.append((set(range(self.n)),list(old)))
        for j in range(1,k):
            A,V=self.q(1);B,W=self.q(2);self.groups.append(V+W)
            t=[self.v() for _ in range(4)];r=[self.v() for _ in range(2)];s=[self.v() for _ in range(2)]
            self.edge(old[4],t[0],0,2);self.edge(old[0],t[0],1);self.edge(old[1],t[3],1)
            for a,b,f,c in zip(t,t[1:],(1,3,1),(3,1,3)):self.edge(a,b,f,c)
            for l in range(2):
                self.edge(t[l+1],r[l],2);self.edge(old[l+2],r[l],1);self.edge(r[l],s[l],3)
                self.edge(A[l+2],s[l],1);self.edge(B[l+2],s[l],2)
            old=[A[0],A[1],B[0],B[1],t[3]];self.regions.append((set(range(self.n)),list(old)))
        x=self.v();bad2=self.edge(old[0],x,1);self.edge(old[2],x,1);self.edge(old[4],x,0,2);self.edge(old[1],old[3],1)
        return bad1,bad2

def inc(n,E):
    A=[[] for _ in range(n)]
    for i,(u,v) in enumerate(E):A[u].append(i);A[v].append(i)
    return A

def authenticate(n,E,f):
    g=nx.Graph();g.add_nodes_from(range(n));g.add_edges_from(E);assert g.number_of_edges()==len(E)==3*n//2 and nx.is_connected(g)
    assert all(g.degree(v)==3 for v in g);A=inc(n,E)
    assert all(f[i]^f[j]^f[k]==0 for i,j,k in A);return g,A

def min_defect_certificate(b):
    # For each nested prefix, its boundary is exactly four Q port edges + one e-edge.
    # Each disjoint charged set includes all incident edges of its two Qs and the e-edge.
    G=[]
    for (R,ports),Q in zip(b.regions,b.groups):
        cut=[i for i,(u,v) in enumerate(b.E) if (u in R)!=(v in R)]
        assert len(cut) in (3,5) # final joining two ports is internal, so last cut has three
        # For last prefix the remaining two Q ports are joined internally; parity counts that edge twice, canceling.
        ee=[i for i in cut if ports[4] in b.E[i]];assert len(ee)==1
        q=set(Q);charge={i for i,(u,v) in enumerate(b.E) if u in q or v in q}|set(ee)
        # Every cut edge other than e has an endpoint in the layer Qs.
        assert set(cut)-set(ee)<=charge
        assert all(not (charge & prev) for prev in G)
        G.append(charge)
    return G

def source(k):
    b=Builder();bad=b.make(k);g,A=authenticate(b.n,b.E,b.f);assert b.f.count(0)==k
    groups=min_defect_certificate(b)
    # In independently supplied improper word, delete two edges and directly check a proper coloring.
    badset=set(bad);P=[];w=[]
    for e in bad:
        for v in b.E[e]:
            keep=[b.c[i] for i in A[v] if i not in badset];assert len(set(keep))==2
            P.append(v);w.append(next(c for c in (1,2,3) if c not in keep))
    assert len(set(P))==4 and w[0]!=w[1] and w[2]!=w[3] and (w[0]^w[1]^w[2]^w[3])==0
    assert all(len({b.c[i] for i in row if i not in badset})==len([i for i in row if i not in badset]) for row in A)
    E=[e for i,e in enumerate(b.E) if i not in badset];f=[c for i,c in enumerate(b.c) if i not in badset]
    z,q=affine(8,CAPQ,QPORT,w);assert z==1 and verify(8,CAPQ,QPORT,w,q)
    E+= [(b.n+u,b.n+v) for u,v in CAPQ];f+=list(q)
    E+= [(v,b.n+p) for v,p in zip(P,QPORT)];f+=w
    pg,PA=authenticate(b.n+8,E,f);assert f.count(0)==1
    assert nx.is_connected(g.edge_subgraph([e for i,e in enumerate(b.E) if i not in badset]))
    # Independent adversarial random conserved pairs via cycle basis; check lower certificate per group.
    rng=random.Random(k);cb=nx.cycle_basis(g);ids={frozenset(e):i for i,e in enumerate(b.E)}
    for trial in range(100):
        zflow=[0]*len(b.E)
        for C in cb:
            val=rng.randrange(4)
            for u,v in zip(C,C[1:]+C[:1]):zflow[ids[frozenset((u,v))]]^=val
        assert all(zflow[i]^zflow[j]^zflow[l]==0 for i,j,l in A)
        assert all(any(zflow[e]==0 for e in S) for S in groups)
    return {'k':k,'child_n':b.n,'parent_n':b.n+8,'child_rf_exact':k,'parent_defects':1,'child_girth':nx.girth(g),'parent_girth':nx.girth(pg),'deleted_edge_ids':bad,'boundary':w,'groups':[sorted(s) for s in groups], 'child_edges':b.E,'child_flow':b.f,'child_improper':b.c,'parent_edges':E,'parent_flow':f,'fingerprint':hashlib.sha256(json.dumps([E,f],separators=(',',':')).encode()).hexdigest()}
if __name__=='__main__':
    t=time.monotonic();rows=[source(k) for k in (1,2,3,5,10,20)]
    print([(r['k'],r['child_n'],r['parent_n'],r['child_girth'],r['parent_girth'],r['boundary']) for r in rows]);print('seconds',time.monotonic()-t)
    with open('/mnt/data/c03_08_amplifier_results.json','w') as f:json.dump(rows,f,indent=2)
