from mixed import *
from obstruction import allcovers
import random

def run():
    G=a.old.incidence(BASE,3);ok,P=nx.check_planarity(G);assert ok;P.check_structure();seen=set();faces=[]
    for u,v in P.edges:
        if (u,v) not in seen:faces.append(P.traverse_face(u,v,seen))
    assert len(seen)==2*G.number_of_edges() and len(faces)==G.number_of_edges()-len(G)+2
    H=G.copy();H.remove_edge(BASE[0],(1,0));assert nx.is_connected(H) and not list(nx.bridges(H));assert set(allcovers(BASE,3))==set(W)
    rng=random.Random(261126);checks=[]
    for r in (1,2,4):
        T,n,_=mixed(r);perm=[rng.sample(range(n),n) for _ in range(3)];S=tuple(sorted(tuple(perm[d][t[d]] for d in range(3)) for t in T));q=solve(S,n);assert q['decision']=='YES' and sum(q['counts'])==1+3**(3*r) and a.old.verify(S,n,q['witness'])
        count=None
        if r<=2:count=len(allcovers(S,n));assert count==sum(q['counts'])
        checks.append(dict(r=r,m=len(T),count=count,blind_count=sum(q['counts']),atoms=q['atoms']))
    return dict(base_vertices=len(G),base_edges=G.number_of_edges(),base_faces=len(faces),rotation=[(u,list(P.neighbors_cw_order(u))) for u in sorted(P)],base_covers=W,renumbered=checks)
if __name__=='__main__':print(json.dumps(run()))
