#!/usr/bin/env python3
"""LSPV-3/553: exact bridge-versus-cycle SAT-model theorem.
Independently validates LSPV-3/552 source family. Does NOT run any proof checker.
"""
import json
from collections import deque

BASE=[(0,2),(0,3),(1,2),(1,3),(2,3),(1,4),(8,9),(5,8),
      (6,7),(9,10),(6,9),(7,5),(0,4),(10,8),(7,10),
      (5,11),(6,11),(4,11)]

def grow(n,edges):
    a=list(edges)
    u=8
    incident=[i for i,e in enumerate(a) if u in e]
    assert len(incident)==3
    i,j=incident[1:]
    a[i]=tuple(n if v==u else v for v in a[i])
    a[j]=tuple(n+1 if v==u else v for v in a[j])
    a.extend([(u,n),(n,n+1),(n+1,u)])
    return n+2,a

def connected(n,edges,omit):
    seen={0};todo=deque([0])
    while todo:
        v=todo.popleft()
        for i,(a,b) in enumerate(edges):
            if i==omit:continue
            w=b if a==v else (a if b==v else -1)
            if w>=0 and w not in seen:
                seen.add(w);todo.append(w)
    return len(seen)==n

def rank(rows):
    piv={}
    for x in rows:
        while x:
            i=(x&-x).bit_length()-1
            if i in piv:x^=piv[i]
            else:piv[i]=x;break
    return len(piv)

def direct(n,edges,special,omit):
    E=len(edges)
    inc=[[] for _ in range(n)]
    for i,(a,b) in enumerate(edges):inc[a].append(i);inc[b].append(i)
    a,b=[e for e in inc[special] if e!=omit]
    total=0
    for word in range(1<<E):
        if ((word>>a)^(word>>b))&1 != 1:continue
        if any(((word>>e[0])^(word>>e[1])^(word>>e[2]))&1
               for v,e in enumerate(inc) if v!=special):continue
        total+=1
    return total

rows=[];n=12;edges=BASE
for t in range(6):
    if t:n,edges=grow(n,edges)
    E=len(edges)
    assert n==12+2*t and E==18+3*t and 2*E==3*n
    inc=[[] for _ in range(n)]
    for i,(a,b) in enumerate(edges):inc[a].append(i);inc[b].append(i)
    assert all(len(e)==3 for e in inc)
    assert inc[0]==[0,1,12] and 17 in inc[4]
    matrix=[sum(1<<i for i in e) for e in inc]
    assert rank(matrix)==n-1
    b12=not connected(n,edges,12)
    b17=not connected(n,edges,17)
    assert not b12 and b17
    target=matrix[:]
    target[0]=matrix[0]^(1<<12)
    assert rank(target)==n
    count=1<<(E-n)
    if t<2:
        brute=direct(n,edges,0,12)
        bridge_brute=direct(n,edges,4,17)
        assert brute==count and bridge_brute==0
    else:brute=bridge_brute=None
    if t==0:
        flows=[z for z in range(1<<E)
               if all((((z>>e[0])^(z>>e[1])^(z>>e[2]))&1)==0
                      for e in inc)]
        assert len(flows)==1<<(E-n+1)
        for vertex in range(n):
            for omitted in inc[vertex]:
                predicted=0 if not connected(n,edges,omitted) else count
                actual=sum((z>>omitted)&1 for z in flows)
                assert actual==predicted,(vertex,omitted,actual,predicted)
    rows.append(dict(t=t,V=n,E=E,clauses=4*n,paid=4*n-1,
                     bridge17=b17,cycle12=not b12,
                     cycle_rank=n-1,modified_rank=n,
                     SAT_models=count,brute=brute,bridge_brute=bridge_brute))
print(json.dumps(dict(run="LSPV-3/553",status="PASS",
 theorem="For connected G, the parity-relaxed source has 0 models when omitted edge is a bridge, otherwise 2^(E-V).",
 scope="Independent source-only analysis, not historic R_mix341 or checker execution",
 rows=rows),indent=2))
