#!/usr/bin/env python3
"""Reproduce restricted connected exact-one/equality bridge semantics.
This compact audit is smaller than the separately supplied 3,896-check run.
"""
from itertools import product
from collections import Counter, defaultdict
import json

checks=0

def ck(value):
    global checks
    checks+=1
    assert value

def oracle(H, n):
    return any(all(sum((a[v]==s) for v,s in C)==1 for C in H)
               for a in product((0,1),repeat=n))

def normalize(H):
    E=[]; equal=[]; copies=defaultdict(list); v=0
    for C in H:
        module=[]
        for src,sign in C:
            module.append((v,sign));copies[src].append(v);v+=1
        E.append(tuple(module))
    for group in copies.values():
        equal.extend(zip(group,group[1:]))
    parent={a:a for a in copies}
    def root(a):
        while parent[a]!=a:
            parent[a]=parent[parent[a]];a=parent[a]
        return a
    for C in H:
        a=C[0][0]
        for b,_ in C[1:]: parent[root(b)]=root(a)
    groups=defaultdict(list)
    for a,cp in copies.items():groups[root(a)].append(cp)
    deg=Counter(u for uv in equal for u in uv)
    ends=[]
    for group in groups.values():
        eligible=sorted({u for seq in group for u in seq if deg[u]<=1})
        ck(len(eligible)>=2)
        ends.append(iter(eligible))
    c=len(ends)
    for i in range(c-1):
        u,w=next(ends[i]),next(ends[i+1])
        up,z,a,vp,z2,b=range(v,v+6);v+=6
        E += [((up,1),(z,1),(a,1)),((vp,1),(z2,1),(b,1))]
        equal += [(u,up),(z,z2),(w,vp)]
    return E,equal,v,c

def joined(E, equal):
    adj=defaultdict(set)
    for u,v in equal: adj[u].add(v);adj[v].add(u)
    def choices(C):
        ids=[u for u,_ in C]
        for bits in product((0,1),repeat=3):
            assignment=dict(zip(ids,bits))
            if sum(assignment[u]==s for u,s in C)==1:
                yield assignment
    partial={}
    def go(i):
        if i==len(E):return True
        for a in choices(E[i]):
            if all(w not in partial or partial[w]==b
                   for u,b in a.items() for w in adj[u]):
                partial.update(a)
                if go(i+1):return True
                for u in a:del partial[u]
        return False
    return go(0)

def connected(E,equalities):
    graph=defaultdict(set)
    for C in E:
        for u,_ in C:
            graph[u].update(v for v,_ in C if v!=u)
    for u,v in equalities:graph[u].add(v);graph[v].add(u)
    seen={next(iter(graph))};todo=list(seen)
    while todo:
        for w in graph[todo.pop()]:
            if w not in seen:seen.add(w);todo.append(w)
    return len(seen)==len(graph)

def case(H,n):
    E,Q,num,c=normalize(H)
    d=Counter(u for C in E for u,s in C)
    d.update(u for p in Q for u in p)
    ck(max(d.values())<=3)
    ck(connected(E,Q))
    ck(all(sum(u in [z for z,s in C] for C in E)==1 for u in range(num)))
    ck(num==3*len(E))
    ck(oracle(H,n)==joined(E,Q))
    return dict(label=oracle(H,n),source_components=c,
                typed_module_count=len(E),equality_count=len(Q),
                proper_cnf_variables=4*len(E)+2*len(Q),
                proper_cnf_clauses=6*len(E)+4*len(Q))

def main():
    triples=[[0,1,2],[0,1,3],[0,2,3],[1,2,3],[4,5,6]]
    unsat=[tuple((v,1) for v in row) for row in triples]
    sat=[tuple((v,0 if j==3 and v==1 else 1) for v in row)
         for j,row in enumerate(triples)]
    a=case(unsat,7);b=case(sat,7)
    ck(a['label'] is False and b['label'] is True)
    ck(a['source_components']==b['source_components']==2)
    ck((a['typed_module_count'],a['equality_count'])==(7,11))
    ck((a['proper_cnf_variables'],a['proper_cnf_clauses'])==(50,86))
    for p in product((0,1),repeat=4):
        H=[]
        for j in range(2):
            row=triples[j]
            H.append(tuple((v,p[(j*2+i)%4]) for i,v in enumerate(row)))
        x=case(H,7)
        ck(x['typed_module_count']==2)
    print(json.dumps(dict(status='COMPUTATIONAL',pair=[a,b],
                          total_checks=checks,errors=0),indent=2,sort_keys=True))

if __name__=='__main__':main()
