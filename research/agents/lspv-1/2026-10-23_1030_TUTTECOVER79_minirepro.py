#!/usr/bin/env python3
"""TUTTECOVER79: finite independently reproducible Tutte-Berge / matching audit.
No SAT lower bound is claimed. Python 3 standard library only.
"""
from functools import lru_cache
from itertools import combinations
import json, random

def sharp_graph():
    edges = []
    for i in range(3):
        a,b,c = 1+3*i,2+3*i,3+3*i
        edges += [(a,b),(a,b),(a,c),(b,c),(0,c)]
    return 10, edges

def exact_matching(n,edges):
    nbr=[set() for _ in range(n)]
    for a,b in edges:
        assert a != b
        nbr[a].add(b); nbr[b].add(a)
    @lru_cache(None)
    def rec(mask):
        if not mask: return 0
        first = mask & -mask
        i=first.bit_length()-1
        rem=mask ^ first
        best=rec(rem)
        for j in nbr[i]:
            if rem & (1 << j):
                best=max(best,1+rec(rem ^ (1 << j)))
        return best
    return rec((1<<n)-1)

def odd_components_after(n,edges,removed):
    adj=[set() for _ in range(n)]
    for a,b in edges:
        adj[a].add(b); adj[b].add(a)
    todo=set(range(n))-removed; odd=0
    while todo:
        root=todo.pop(); seen={root}; stack=[root]
        while stack:
            v=stack.pop()
            for w in adj[v]:
                if w in todo:
                    todo.remove(w); seen.add(w); stack.append(w)
        odd += len(seen)%2
    return odd

def verify(n,edges):
    assert all(a!=b for a,b in edges)
    assert len(edges)*2 == n*3
    assert all(sum(v in e for e in edges)==3 for v in range(n))
    nu=exact_matching(n,edges)
    assert 5*nu >= 2*n
    deficiencies=[]
    for mask in range(1<<n):
        selected={i for i in range(n) if mask & (1<<i)}
        deficiencies.append(odd_components_after(n,edges,selected)-len(selected))
    assert max(deficiencies)==n-2*nu
    return {"vertices":n,"edges":len(edges),"matching":nu,
            "deficiency":max(deficiencies),"bound_floor_cover":n-(2*n+4)//5}

def random_cubic(n,rng):
    for attempt in range(200000):
        stubs=[i for i in range(n) for _ in range(3)]
        rng.shuffle(stubs)
        edges=[(stubs[k],stubs[k+1]) for k in range(0,len(stubs),2)]
        if all(a!=b for a,b in edges): return edges
    raise RuntimeError("No loopless configuration sampled")

def main():
    rng=random.Random(202610231030)
    n,edges=sharp_graph()
    sharp=verify(n,edges)
    assert sharp["matching"]==4 and sharp["deficiency"]==2
    out={"sharp":sharp,"random":[]}
    for n in (2,4,6,8,10,12):
        for k in range(5):
            ed=random_cubic(n,rng)
            out["random"].append(verify(n,ed))
    print(json.dumps({"status":"COMPUTATIONAL","seed":202610231030,
      "random_checked":len(out["random"]),"sharp":sharp,"all_passed":True},
      sort_keys=True))

if __name__=="__main__":
    main()
