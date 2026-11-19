#!/usr/bin/env python3
"""Standard-library independent T5 Q two-head parity theorem audit."""
from collections import defaultdict, deque
from itertools import combinations, product
import json
W=({1,3},{2,4},{0,3},{1,4},{0,2})
def q(c,h,u,v):return (c[u] in W[c[h]]) != (c[v] in W[c[h]])
def witness(n,clauses):
    heads=sorted({h for h,_,_ in clauses})
    if len(heads)>2:raise ValueError('unsupported: >2 heads')
    c=[0]*n
    if len(heads)==2:c[heads[1]]=2
    bits={}
    for h in heads:
        graph=defaultdict(list)
        for x,u,v in clauses:
            if x==h:graph[u].append(v);graph[v].append(u)
        p={}
        for start in graph:
            if start in p:continue
            p[start]=0;todo=deque([start]);component=[start]
            while todo:
                u=todo.popleft()
                for v in graph[u]:
                    b=p[u]^1
                    if v in p:
                        if p[v]!=b:return None
                    else:p[v]=b;todo.append(v);component.append(v)
            anchor=[v for v in component if v in heads]
            if anchor:
                assert len(anchor)==1
                v=anchor[0];flip=p[v]^int(c[v] in W[c[h]])
                for v in component:p[v]^=flip
        bits[h]=p
    for v in range(n):
        if v in heads:continue
        for a in range(5):
            if all(v not in bits[h] or int(a in W[c[h]])==bits[h][v] for h in heads):
                c[v]=a;break
        else:raise AssertionError('missing T5 signature')
    assert all(q(c,*cl) for cl in clauses)
    return c

def audit(n):
    domain=list(product(range(5),repeat=n))
    total=sat=errors=0
    for heads in combinations(range(n),2):
        scopes=[(h,)+tail for h in heads for tail in combinations([v for v in range(n) if v!=h],2)]
        masks=[sum(1<<i for i,c in enumerate(domain) if q(c,*s)) for s in scopes]
        intersection=[(1<<len(domain))-1]*(1<<len(scopes))
        for subset in range(1,len(intersection)):
            bit=subset&-subset;j=bit.bit_length()-1
            intersection[subset]=intersection[subset^bit]&masks[j]
        for subset,expected_mask in enumerate(intersection):
            clauses=[scopes[j] for j in range(len(scopes)) if subset>>j&1]
            ans=witness(n,clauses)
            total+=1;sat+=bool(expected_mask)
            if (ans is not None)!=bool(expected_mask) or ans is not None and not all(q(ans,*cl) for cl in clauses):
                errors+=1;raise AssertionError((n,heads,subset))
    return {'n':n,'total_pair_duplicated_subsets':total,'SAT':sat,'UNSAT':total-sat,'mismatches':errors}

if __name__=='__main__':print(json.dumps([audit(4),audit(5)],indent=2))
