"""TMR-3/090: source-authenticated T5 block-cut product counting.

Reuses the /089 exact count routine on each biconnected source block.
Run from experiments/tmr. Python standard library only.
"""
from itertools import product
from tmr3_t5_perturb089_repo import count as count_block

def beat(x, y):
    return (y-x) % 5 in (1,3)

def biconnected(n, arcs):
    adj = [set() for _ in range(n)]
    for u,v in arcs:
        adj[u].add(v); adj[v].add(u)
    disc = [-1]*n; low=[0]*n; stack=[]; groups=[]; clock=0
    def dfs(u,parent):
        nonlocal clock
        disc[u]=low[u]=clock; clock+=1
        for v in sorted(adj[u]):
            if disc[v]<0:
                stack.append((u,v)); dfs(v,u)
                low[u]=min(low[u],low[v])
                if low[v]>=disc[u]:
                    group=[]
                    while True:
                        a,b=stack.pop()
                        group.append((min(a,b),max(a,b)))
                        if (a,b)==(u,v): break
                    groups.append(group)
            elif v != parent and disc[v]<disc[u]:
                stack.append((u,v)); low[u]=min(low[u],disc[v])
    for u in range(n):
        if disc[u]<0: dfs(u,-1)
    assert not stack
    return groups,adj

def count(n, arcs, details=False):
    E=set(arcs)
    if any(not(0<=u<n and 0<=v<n) for u,v in E):
        raise ValueError('invalid vertex index')
    if any(u==v or (v,u) in E for u,v in E):
        return (0, {'short_circuit':True}) if details else 0
    groups,adj=biconnected(n,E)
    visited=set(); components=0
    for u in range(n):
        if u in visited: continue
        components+=1;visited.add(u);q=[u]
        while q:
            x=q.pop()
            for y in adj[x]:
                if y not in visited: visited.add(y);q.append(y)
    z=5**components; factors=[]
    for edges in groups:
        edge_set=set(edges)
        nodes=sorted({w for e in edges for w in e})
        index={v:i for i,v in enumerate(nodes)}
        sub=[(index[u],index[v]) for u,v in E
             if (min(u,v),max(u,v)) in edge_set]
        block_total=count_block(len(nodes),sub)
        assert block_total%5==0
        z*=block_total//5
        factors.append((len(nodes),len(edges),block_total//5))
    info={'components':components,'blocks':len(groups),
          'block_factors':factors}
    return (z,info) if details else z

def brute(n,arcs):
    return sum(all(beat(x[u],x[v]) for u,v in arcs)
               for x in product(range(5),repeat=n))

def tests():
    from random import Random
    rng=Random(90118);checks=0
    for n in range(1,6):
        for _ in range(42):
            E=[(u,v) for u in range(n) for v in range(n)
               if rng.random()<0.14]
            assert count(n,E)==brute(n,E)
            checks+=1
    for _ in range(12):
        arcs=[]
        for U,V in [((0,1),(2,3)), ((1,4),(5,6))]:
            for u in U:
                for v in V:
                    arcs.append((u,v) if rng.randrange(2)==0 else (v,u))
        assert count(7,arcs)==brute(7,arcs)
        checks+=1
    assert count(3,[(0,1),(1,2),(2,0)])==15
    assert count(4,[(0,1),(1,2),(2,3)])==40
    checks+=2
    print(checks,'checks PASS')

if __name__=='__main__':
    tests()
