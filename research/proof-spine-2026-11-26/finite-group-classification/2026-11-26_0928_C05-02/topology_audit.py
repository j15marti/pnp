"""Topology and exact dual unicycle check on the independently reconstructed C01 sphere."""
from affine_chart import *

def topological(D,M,X):
    M=set(M);H=nx.MultiGraph();H.add_nodes_from(X)
    for e in M:
        a,b=D[e];H.add_edge(a,b,key=e)
    comps=list(nx.connected_components(H));ix={x:i for i,C in enumerate(comps) for x in C}
    K=nx.Graph();K.add_edges_from((('y',y),('z',z)) for y,z in D if (y,z) not in M)
    K.add_nodes_from(('y',y) for y,z in M);K.add_nodes_from(('z',z) for y,z in M)
    assert set(dict(K.degree()).values())<={1,2}
    tree=nx.Graph();tree.add_nodes_from(range(len(comps)));p=Counter();paths=0;cycles=0
    for C in nx.connected_components(K):
        Q=K.subgraph(C);sides=set()
        for u,v in Q.edges():
            if u[0]=='z':u,v=v,u
            a,b=D[u[1],v[1]];sides.add(tuple(sorted((ix[a],ix[b]))))
        assert len(sides)==1;i,j=next(iter(sides))
        if Q.number_of_edges()==len(C):assert i!=j and not tree.has_edge(i,j);tree.add_edge(i,j);cycles+=1
        else:assert Q.number_of_edges()==len(C)-1 and i==j;p[i]+=1;paths+=1
    assert paths==2 and nx.is_tree(tree)
    ranks=[]
    for i,C in enumerate(comps):
        r=H.subgraph(C).number_of_edges()-len(C)+1;assert r==tree.degree(i)+p[i]-1;ranks.append(r)
    delta=sum(r==0 for r in ranks);assert delta==fixed_hall(D,M,X)
    marks=[i for i,v in p.items() for _ in range(v)]
    good=len(nx.shortest_path(tree,*marks))-1==cycles
    assert good==(delta==0)
    if not delta:
        F,L,G=chart(D,sorted(M),sorted(M),X);s,W,st=join(F,(1<<len(X))-1,0);assert s=='YES'
        # Each pair-domain choice is one bit; dimension agrees with dual cycle count.
        U=[v for f in F for v in f[0][1]];assert len(U)-len(basis(U))==len(comps)
        assert len(lift_chart(F,L,W))==len(X)
        if len(X)<=6:
            cnt=0
            for z in it.product(*(tuple(D[e]) for e in sorted(M))):cnt+=len(set(z))==len(X)
            assert cnt==1<<len(comps)
    return dict(delta=delta,cycles=cycles,regions=len(comps),marks=marks,ranks=ranks,unicycle_count=len(comps) if good else None)

def main():
    data=json.load(open('pooled_results.json'));rng=random.Random(261126056);out=[]
    for k in [1,2,4,5,7,8,13]:
        T,R=sphere(k);D=pairs(T);X={x for c,x in R if c==0};rec=[]
        if k in [4,5,7,8,13]:
            mats=[a[key] for b in data['native'] if b['k']==k for a in b['trials'] for key in ('chart0','chart1')]
        else:mats=[pm(D,{e:rng.randrange(1000) for e in sorted(D)}) for _ in range(16)]
        for M in mats:rec.append(topological(D,[tuple(e) for e in M],X))
        out.append(dict(k=k,m=len(T),trials=rec));print(k,len(rec),sum(not a['delta'] for a in rec),max(a['cycles'] for a in rec),flush=True)
    json.dump(out,open('topology_results.json','w'),indent=2)
if __name__=='__main__':main()
