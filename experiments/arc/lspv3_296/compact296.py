#!/usr/bin/env python3
"""GATE296 compact self-contained exact M22 DP. No third-party packages.
Input: JSON {"name":{"n":int,"source":[[signed_lits],...]},...}
Usage: python compact296.py fixtures296.json
This is a word-RAM Python controller, NOT a native FLMV indexed-tape simulator.
Full source, raw, and independent verification are in the reproducibility archive.
"""
import sys, json, itertools, collections

def canonical(c,n):
    if type(n)!=int or n<3 or type(c)!=list or len(c)*3!=4*n:return False
    seen=set();occ=collections.Counter()
    for row in c:
        if type(row)!=list or len(row)!=3:return False
        if any(type(l)!=int or l==0 or abs(l)>n for l in row):return False
        if len({abs(l) for l in row})!=3:return False
        if not (all(l>0 for l in row) or all(l<0 for l in row)):return False
        k=tuple(sorted(row))
        if k in seen:return False
        seen.add(k);occ.update(row)
    return all(occ[v]==occ[-v]==2 for v in range(1,n+1))

def acquire(c,n):
    graph={v:set() for v in range(1,n+1)}
    for cl in c:
        for a,b in itertools.combinations([abs(x) for x in cl],2):
            graph[a].add(b);graph[b].add(a)
    bags={};order=[];probes=0
    while graph:
        choice=None;rank=None
        for v in sorted(graph):
            nb=sorted(graph[v]);fill=0
            for a,b in itertools.combinations(nb,2):
                probes+=1
                if b not in graph[a]:fill+=1
            r=(fill,len(nb),v)
            if rank is None or r<rank:rank=r;choice=v
        nb=sorted(graph[choice]);bags[choice]=[choice]+nb;order.append(choice)
        for a,b in itertools.combinations(nb,2):
            graph[a].add(b);graph[b].add(a)
        for a in nb:graph[a].remove(choice)
        del graph[choice]
    idx={v:i for i,v in enumerate(order)}
    par={v:min((u for u in bags[v] if u!=v),key=lambda u:idx[u])
         if len(bags[v])>1 else None for v in order}
    ch={v:[] for v in order}
    for v in order:
        if par[v] is not None:ch[par[v]].append(v)
    return order,bags,par,ch,probes

def decide(c,n):
    if not canonical(c,n):return {"decision":"REJECT"}
    order,bags,par,ch,probes=acquire(c,n)
    idx={v:i for i,v in enumerate(order)}
    owned={v:[] for v in order}
    for j,cl in enumerate(c):
        v=min((abs(l) for l in cl),key=lambda q:idx[q])
        assert set(map(abs,cl))<=set(bags[v])
        owned[v].append(j)
    sep={v:sorted(set(bags[v])&set(bags[par[v]])) if par[v] else [] for v in order}
    tables={};rows=0
    def key(a,ids):return sum(int(a[q])<<i for i,q in enumerate(ids))
    def clause_ok(cl,a):return any(a[abs(l)]==(l>0) for l in cl)
    for v in order:
        yes=set()
        for bits in itertools.product([False,True],repeat=len(bags[v])):
            rows+=1;a=dict(zip(bags[v],bits))
            if any(not clause_ok(c[j],a) for j in owned[v]):continue
            if any(key(a,sep[u]) not in tables[u] for u in ch[v]):continue
            yes.add(key(a,sep[v]))
        tables[v]=yes
    roots=[v for v in order if par[v] is None]
    sat=all(0 in tables[v] for v in roots)
    ans=None
    if sat:
        ans={}
        def back(v,k):
            for bits in itertools.product([False,True],repeat=len(bags[v])):
                a=dict(zip(bags[v],bits))
                if key(a,sep[v])!=k:continue
                if any(not clause_ok(c[j],a) for j in owned[v]):continue
                if any(key(a,sep[u]) not in tables[u] for u in ch[v]):continue
                for q,b in a.items():
                    assert q not in ans or ans[q]==b
                    ans[q]=b
                for u in ch[v]:back(u,key(a,sep[u]))
                return
            raise RuntimeError("invalid DP certificate")
        for v in roots:back(v,0)
        assert len(ans)==n and all(clause_ok(cl,ans) for cl in c)
    return {"decision":"SAT" if sat else "UNSAT",
            "w":max(map(len,bags.values()))-1,
            "minfill_pair_probes":probes,"forward_rows":rows,
            "bitmap_bits":sum(1<<len(sep[v]) for v in order),
            "witness":''.join(str(int(ans[v])) for v in range(1,n+1)) if sat else None}

if __name__=="__main__":
    if len(sys.argv)!=2:raise SystemExit("usage: compact296.py fixtures296.json")
    src=json.load(open(sys.argv[1]))
    for name,entry in src.items():
        print(json.dumps({"name":name,**decide(entry["source"],entry["n"])}))
