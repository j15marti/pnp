#!/usr/bin/env python3
"""Small independent semantic control for LSPV-2/447.
Do not confuse finite brute force with FLMV execution or a proof-size certificate.
"""
from itertools import combinations
from collections import Counter

def components(n, edges):
    todo = set(range(n))
    result = []
    while todo:
        start = min(todo)
        visited = {start}
        frontier = [start]
        while frontier:
            v = frontier.pop()
            for a,b in edges:
                w = b if a == v else a if b == v else None
                if w is not None and w not in visited:
                    visited.add(w)
                    frontier.append(w)
        result.append(tuple(sorted(visited)))
        todo -= visited
    return result

def gadget(edges, v, charge):
    ids = [i+1 for i,(a,b) in enumerate(edges) if a==v or b==v]
    assert len(ids)==3
    a,b,c=ids
    return [tuple((-lit if sign else lit) for lit,sign in zip((a,b,c),(p,q,p^q^1^charge)))
            for p in (0,1) for q in (0,1)]

def run(name, n, e):
    edges=sorted({tuple(sorted(x)) for x in e})
    assert len(edges)==3*n//2
    comp=components(n,edges)
    reach=Counter()
    for assignment in range(1<<len(edges)):
        chi=0
        for j,(a,b) in enumerate(edges):
            if assignment & (1<<j): chi^=1<<a;chi^=1<<b
        reach[chi]+=1
    assert len(reach)==1<<(n-len(comp))
    assert set(reach.values())=={1<<(len(edges)-n+len(comp))}
    for chi in range(1<<n):
        sig=[sum((chi>>v)&1 for v in group)%2 for group in comp]
        assert (chi in reach)==(not any(sig))
        for v in range(n):
            clauses=gadget(edges,v,(chi>>v)&1)
            assert len(clauses)==4 and all(len(c)==3 for c in clauses)
            for bits in range(8):
                assignment={i+1:(bits>>i)&1 for i in range(3)}
                local_ids=sorted({abs(lit) for clause in clauses for lit in clause})
                actual={local_ids[i]:assignment[i+1] for i in range(3)}
                ok=all(any((actual[abs(l)] if l>0 else not actual[abs(l)]) for l in clause)
                       for clause in clauses)
                assert ok == ((bits.bit_count()%2)==((chi>>v)&1))
    rep=[g[0] for g in comp]
    signatures=set()
    for s in range(1<<len(comp)):
        base=sum(1<<rep[i] for i in range(len(comp)) if (s>>i)&1)
        signature=[]
        for z in range(1<<len(comp)):
            delta=sum(1<<rep[i] for i in range(len(comp)) if (z>>i)&1)
            result=(base^delta) in reach
            assert result==(s==z)
            signature.append(result)
        signatures.add(tuple(signature))
    assert len(signatures)==1<<len(comp)
    print(name, 'H',n,'M',len(edges),'components',len(comp),
          'charges',1<<n,'future_functions',len(signatures))
    return (1<<n)

K4=(4,list(combinations(range(4),2)))
CUBE=(8,[(a,b) for a in range(8) for b in range(a+1,8) if (a^b).bit_count()==1])
PETERSEN=(10,[(i,(i+1)%5) for i in range(5)]
             +[(i,i+5) for i in range(5)]
             +[(i+5,5+(i+2)%5) for i in range(5)])
def join(a,b):
    n,e=a;m,f=b
    return n+m,e+[(x+n,y+n) for x,y in f]

if __name__=="__main__":
    cases=[("K4",*K4),("cube",*CUBE),("Petersen",*PETERSEN),
           ("K4+K4",*join(K4,K4)),("3xK4",*join(join(K4,K4),K4))]
    total=sum(run(*case) for case in cases)
    assert total==5648
    print("PASS",total,"exhaustive charge patterns")
