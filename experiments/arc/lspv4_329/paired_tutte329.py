#!/usr/bin/env python3
"""Exact source-typed all-pin complement-paired M22 -> f-factor -> 1-factor.
Requires networkx for general graph maximum cardinality matching.
Finite controls are independent of the matching oracle via exhaustive truth.
This is host-level word computation, NOT a native FLMV machine trace.
"""
from itertools import product
from collections import Counter
from random import Random
import json
import networkx as nx

SOURCES={
 "K4":((1,2,3),(1,4,5),(2,4,6),(3,5,6)),
 "K33":((1,2,3),(4,5,6),(7,8,9),(1,4,7),(2,5,8),(3,6,9))
}

def valid(pos):
    n=max((max(c) for c in pos),default=0)
    if not n or not all(len(c)==3 and len(set(c))==3 for c in pos):
        return False
    if len(set(map(lambda c:tuple(sorted(c)),pos)))!=len(pos):
        return False
    if 3*len(pos)!=2*n:return False
    return Counter(x for c in pos for x in c)==Counter({i:2 for i in range(1,n+1)})

def source_models(pos):
    n=max(max(c) for c in pos)
    return [a for a in product((0,1),repeat=n)
            if all(1<=sum(a[i-1] for i in c)<=2 for c in pos)]

def make_gadget(pos,p,h):
    q=len(pos)
    bounds=[]
    for C in pos:
        t=sum(p.get(x,-1)==1 for x in C)
        r=sum(x not in p for x in C)
        lo,up=max(0,1-t),min(r,2-t)
        if lo>up:return None
        bounds.append((lo,up))
    E=[]
    for x in range(1,max(max(C) for C in pos)+1):
        if x in p:continue
        ends=[v for v,C in enumerate(pos) if x in C]
        assert len(ends)==2
        E.append((ends[0],ends[1],("source",x)))
    for v,(lo,up) in enumerate(bounds):
        E += [(v,q,("slack",v,j)) for j in range(up-lo)]
    B=sum(up-lo for lo,up in bounds)
    if h<0 or h>B or (h-sum(up for lo,up in bounds))%2:
        return None
    f=[up for lo,up in bounds]+[h]
    incidence=[[] for _ in f]
    graph=nx.Graph()
    for k,(v,w,tag) in enumerate(E):
        a=("port",k,v)
        b=("port",k,w)
        graph.add_edge(a,b)
        incidence[v].append(a)
        incidence[w].append(b)
    for v,ports in enumerate(incidence):
        for j in range(len(ports)-f[v]):
            d=("dummy",v,j)
            for port in ports:graph.add_edge(d,port)
    return graph,E,B

def barrier(graph, size):
    # Gallai-Edmonds barrier from vertices exposable by maximum matching.
    D=set()
    for vertex in graph:
        sub=graph.copy()
        sub.remove_node(vertex)
        if len(nx.max_weight_matching(sub,maxcardinality=True))==size:
            D.add(vertex)
    U={w for v in D for w in graph[v]}-D
    sub=graph.copy()
    sub.remove_nodes_from(U)
    odds=sum(len(comp)%2 for comp in nx.connected_components(sub))
    assert odds>len(U)
    return {"U":[list(v) for v in sorted(U,key=str)],"odd":odds,"U_count":len(U)}

def decide(pos,p,certify=False):
    assert valid(pos)
    bounds=[]
    for C in pos:
        t=sum(p.get(x,-1)==1 for x in C)
        r=sum(x not in p for x in C)
        lo,up=max(0,1-t),min(r,2-t)
        if lo>up:return {"sat":False,"local_source_conflict":True,"cases":[]}
        bounds.append((lo,up))
    B=sum(up-lo for lo,up in bounds)
    total=sum(up for lo,up in bounds)
    cases=[]
    for h in range(B+1):
        if h%2!=total%2:continue
        graph,E,_=make_gadget(pos,p,h)
        matching=nx.max_weight_matching(graph,maxcardinality=True)
        good=2*len(matching)==len(graph)
        rec={"h":h,"vertices":len(graph),"edges":graph.number_of_edges(),"perfect":good}
        if good:
            selected={a[1] for a,b in matching
                      if a[0]=="port" and b[0]=="port" and a[1]==b[1]}
            assignment={x:b for x,b in p.items()}
            for k,(_,_,tag) in enumerate(E):
                if tag[0]=="source":assignment[tag[1]]=int(k in selected)
            assert all(1<=sum(assignment[x] for x in C)<=2 for C in pos)
            rec["witness"]=[assignment[i] for i in range(1,max(map(max,pos))+1)]
            cases.append(rec)
            return {"sat":True,"cases":cases}
        if certify:rec["tutte"]=barrier(graph,len(matching))
        cases.append(rec)
    return {"sat":False,"cases":cases}

def brute_count(pos,p):
    return sum(all(a[i-1]==b for i,b in p.items()) for a in source_models(pos))

def selfcheck():
    results={}
    for name,pos in SOURCES.items():
        assert valid(pos)
        n=max(map(max,pos))
        pairs=({4:0,5:0,6:0},{4:1,5:0,6:0}) if name=="K4" else (
            {3:0,6:0,7:1,8:1},{3:1,6:0,7:1,8:1})
        rows=[]
        for pin in pairs:
            result=decide(pos,pin,certify=True)
            count=brute_count(pos,pin)
            assert result["sat"]==(count>0)
            rows.append({"pins":pin,"models":count,"decision":result})
        trials=36 if name=="K4" else 28
        rng=Random(202611020140+n)
        tally=Counter()
        for _ in range(trials):
            pin={i:v for i in range(1,n+1)
                 if (v:=rng.choice((-1,0,1)))!=-1}
            result=decide(pos,pin)
            cnt=brute_count(pos,pin)
            assert result["sat"]==(cnt>0)
            tally["SAT" if cnt else "UNSAT"]+=1
        results[name]={"root_models":len(source_models(pos)),
                       "same_original_pins":rows,"sample":dict(tally)}
    return results

if __name__=="__main__":
    print(json.dumps(selfcheck(),indent=2,sort_keys=True))
