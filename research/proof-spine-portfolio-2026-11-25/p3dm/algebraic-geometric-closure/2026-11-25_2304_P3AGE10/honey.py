import networkx as nx, json
from audit import *
def honey(m,n):
    H=nx.hexagonal_lattice_graph(m,n);V=sorted(H);idx={u:i for i,u in enumerate(V)}
    T=[list(2*i+x for x in t) for i in range(len(V)) for t in [(0,0,0),(1,1,1),(0,0,1),(1,1,0),(0,1,0),(1,0,1)]]
    for u,v in H.edges():
        x,y=H.nodes[u]['pos'];a,b=H.nodes[v]['pos'];dx,dy=a-x,b-y
        if abs(dy)<1e-6:port,c=2,2
        elif dx*dy>0:port,c=1,1
        else:port,c=4,1
        r,s=6*idx[u]+port,6*idx[v]+port;T[r][c],T[s][c]=T[s][c],T[r][c]
    return list(map(tuple,T)),2*len(V)
if __name__=='__main__':
    out=[]
    for k in (1,2,3,4):
        T,n=honey(k,k);G=source(T,n);assert nx.is_connected(G);S,calls=close(T,n);assert S==list(range(len(T)));C=cols(T,n);s,W,meta=solve_leaf(T,C,n,set(range(len(T))),(1<<(3*n))-1,4);out.append({'m':len(T),'status':s,'meta':meta});print(out[-1],flush=True)
    with open('honey_results.json','w') as f:json.dump(out,f,indent=2)
