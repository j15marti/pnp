"""Verify certificates independently of the generation/closure code."""
import itertools as it, json, pathlib
import networkx as nx
import numpy as np

for cert in json.loads(pathlib.Path(__file__).with_name('certificates.json').read_text()):
    G=nx.from_graph6_bytes(cert['graph6'].encode()); L=np.array(cert['kernel_basis'],dtype=int)
    n,d=L.shape; assert nx.is_connected(G) and all(k==3 for _,k in G.degree())
    P={u:{v:i for i,v in enumerate(sorted(G[u]))} for u in G}
    rows=[]
    for cycle in nx.cycle_basis(G):
        r=np.zeros(n,dtype=int)
        for i,u in enumerate(cycle): r[u]=P[u][cycle[(i+1)%len(cycle)]]-P[u][cycle[i-1]]
        rows.append(r)
    A=np.array(rows)%3
    def rank(M):
        M=M.copy()%3; k=0
        for j in range(M.shape[1]):
            p=next((i for i in range(k,len(M)) if M[i,j]),None)
            if p is None: continue
            M[[p,k]]=M[[k,p]]; M[k]=M[k]*M[k,j]%3
            for i in range(k+1,len(M)): M[i]=(M[i]-M[i,j]*M[k])%3
            k+=1
        return k
    assert not np.any(A@L%3) and rank(L)==d==n-rank(A)
    B={0:np.zeros(d,dtype=int)}
    for u,v in nx.dfs_edges(G,0): B[v]=(B[u]+P[u][v]*L[u]-P[v][u]*L[v])%3
    C={}
    for u,v in G.edges:
        x=(B[u]+P[u][v]*L[u])%3; assert np.array_equal(x,(B[v]+P[v][u]*L[v])%3)
        C[tuple(sorted((u,v)))]=x
    total=np.zeros((d,d),dtype=int); rhs=0
    def sq(x): return np.outer(x,x)%3
    for coeff,info in cert['rows']:
        if info[0]=='vertex': Q=sq(L[info[1]]); b=1
        else:
            cut={tuple(e) for e in info[1]}; side={0:0}; queue=[0]
            for u in queue:
                for v in G[u]:
                    t=side[u]^(tuple(sorted((u,v))) in cut)
                    if v not in side: side[v]=t; queue.append(v)
                    else: assert side[v]==t
            U={u for u in side if side[u]}; assert cut=={tuple(sorted(e)) for e in nx.edge_boundary(G,U)}
            x=[C[tuple(e)] for e in info[1]]
            if info[0]=='cut4':
                assert len(x)==4; i,j,k,l=[(0,1,2,3),(0,2,1,3),(0,3,1,2)][info[2]]; Q=sq(x[i]-x[j])-sq(x[k]-x[l]); b=0
            else:
                assert info[0]=='cut5' and len(x)==5; Q=sum(sq(u-v) for u,v in it.combinations(x,2)); b=1
        total=(total+coeff*Q)%3; rhs=(rhs+coeff*b)%3
    assert not np.any(total) and rhs==1
    print(cert['graph6'], 'verified 0=1 from',len(cert['rows']),'rows')
