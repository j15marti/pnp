"""FP01 certificate verifier, Python >=3.10, no third-party packages.
Direct edge-mask parity enumeration and ordered-state BFS.
The earlier independent producer used a cycle basis and projection graph.
"""
from collections import deque
from itertools import combinations

E=[(0,2),(0,6),(0,9),(1,3),(1,7),(1,10),(2,10),(2,11),(3,8),(3,11),(4,5),(4,9),(4,11),(5,6),(5,10),(6,7),(7,8),(8,9)]
A,B=110469,185822
GOOD=(96734,178037)
P=sum(1<<i for i in (0,2,3,4,6,7,9,10,11,13,14,15))
H=(((0,1),1),((0,5),2),((0,13),3),((1,2),3),((1,10),2),((2,3),1),((2,7),2),((3,4),3),((3,12),2),((4,5),1),((4,9),2),((5,6),3),((6,7),1),((6,11),2),((7,8),3),((8,9),1),((8,13),2),((9,10),3),((10,11),1),((11,12),3),((12,13),1))
K=(((0,1),1),((2,3),1),((0,2),2),((1,3),2),((0,3),3),((1,2),3))
def incidence(edges):
    return {v:sum(1<<i for i,e in enumerate(edges) if v in e) for v in set(sum((list(e) for e in edges),[]))}
def valid(edges,a,b):
    return all(x.bit_count()==3 and (x&a).bit_count()%2==0 and (x&b).bit_count()%2==0 for x in incidence(edges).values())
def defect(edges,a,b):
    return ((1<<len(edges))-1)^(a|b)
def lift(block,size,a,b):
    out=[]; colors=[]; nv=12
    for i,(u,v) in enumerate(E):
        c=((a>>i)&1)+2*((b>>i)&1)
        if not P>>i&1:
            out.append((u,v)); colors.append(c); continue
        assert c!=0
        mapping={1:c}
        mapping.update(zip((2,3),[j for j in (1,2,3) if j!=c]))
        out.extend(((u,nv),(v,nv+1)));colors.extend((c,c))
        for e,d in block:
            if e==(0,1):continue
            out.append(tuple(nv+j for j in e));colors.append(mapping[d])
        nv+=size
    return out,sum((c&1)<<i for i,c in enumerate(colors)),sum((c>>1)<<i for i,c in enumerate(colors))
def bfs(states):
    start=(A,B);assert start in states
    seen={start};q=deque([start])
    while q:
        a,b=q.popleft()
        for x,y in states:
            if (a==x or b==y or a^b==x^y) and (x,y) not in seen:
                seen.add((x,y));q.append((x,y))
    return seen
def connected_and_girth(edges):
    adj={v:set() for v in incidence(edges)}
    for u,v in edges:
        assert u!=v and v not in adj[u]
        adj[u].add(v);adj[v].add(u)
    reached=set();girth=len(adj)+1
    for s in adj:
        dist={s:0};parent={s:None};q=deque([s])
        while q:
            u=q.popleft()
            for v in adj[u]:
                if v not in dist:
                    dist[v]=dist[u]+1;parent[v]=u;q.append(v)
                elif parent[u]!=v and parent[v]!=u:
                    girth=min(girth,dist[u]+dist[v]+1)
        reached=set(dist)
        assert len(reached)==len(adj)
    return len(adj),girth
if __name__=='__main__':
    masks=list(incidence(E).values())
    F=[a for a in range(1<<len(E)) if all((a&x).bit_count()%2==0 for x in masks)]
    assert len(F)==128 and valid(E,A,B) and valid(E,*GOOD)
    assert defect(E,A,B)==1<<5 and defect(E,*GOOD)==0
    all_pairs=[(a,b) for a,b in combinations(F,2) if defect(E,a,b).bit_count()<=1]
    assert sum(defect(E,a,b)==0 for a,b in all_pairs)==6 and len(all_pairs)==168
    unrestricted=[(a,b) for a in F for b in F if defect(E,a,b).bit_count()<=1]
    assert any(defect(E,a,b)==0 for a,b in bfs(unrestricted))
    restricted=[(a,b) for a,b in unrestricted if not defect(E,a,b)&P]
    seen=bfs(restricted)
    assert len(seen)==18 and all(defect(E,a,b).bit_count()==1 for a,b in seen)
    print('128 binary flows; 6 zero + 162 one-defect unordered pairs; protected component: 18 ordered states, none zero.')
    for block,size,expected in ((K,4,60),(H,14,180)):
        edges,a,b=lift(block,size,A,B)
        edges2,x,y=lift(block,size,*GOOD)
        assert edges==edges2 and valid(edges,a,b) and valid(edges,x,y)
        assert defect(edges,a,b).bit_count()==1 and defect(edges,x,y)==0
        n,girth=connected_and_girth(edges)
        assert n==expected and girth==(3 if size==4 else 6)
        print(n,len(edges),'girth',girth,'both witnesses verified')
