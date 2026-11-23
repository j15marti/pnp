#!/usr/bin/env python3
"""Distributed odd wheel, stdlib reproducibility. Python 3.10+.

Run: python3 research/agents/meta-solver-theorem/2026-11-23_1157_distributed_wheel_check.py
No SAT package, spectral-expander claim, or network access is required.
"""
import itertools
import json
import random

def prism(k):
    E=set()
    for a in (0,k):
        for i in range(k):
            E.add(tuple(sorted((a+i,a+(i+1)%k))))
    for i in range(k): E.add((i,k+i))
    return 2*k,sorted(E)

def random_cubic(n,seed):
    rng=random.Random(seed)
    for _ in range(200000):
        st=[v for v in range(n) for t in range(3)]
        rng.shuffle(st)
        E=[tuple(sorted((st[i],st[i+1]))) for i in range(0,3*n,2)]
        if len(set(E))!=len(E) or any(a==b for a,b in E): continue
        seen={0}
        todo=[0]
        while todo:
            u=todo.pop()
            for a,b in E:
                if a==u and b not in seen: seen.add(b);todo.append(b)
                if b==u and a not in seen: seen.add(a);todo.append(a)
        if len(seen)==n: return n,sorted(E)
    raise RuntimeError("cubic generator exhausted")

def make(H, deleted_rim_edge=None):
    n,HE=H
    assert n%2==0 and n>=6 and len(HE)==3*n//2
    r=n-1
    rim=list(range(n,n+r))
    E=set()
    for i in range(r):
        if i!=deleted_rim_edge: E.add(tuple(sorted((rim[i],rim[(i+1)%r]))))
        E.add(tuple(sorted((i,rim[i]))))
    diamonds={}
    v=n+r
    for a,b in HE:
        c,d=v,v+1;v+=2
        diamonds[(a,b)]=(c,d)
        E.update(tuple(sorted(e)) for e in
                 ((a,c),(a,d),(b,c),(b,d),(c,d)))
    return dict(n=n,r=r,rim=rim,HE=HE,E=E,V=v,diamonds=diamonds)

def detect(G):
    adj=[set() for _ in range(G["V"])]
    for a,b in G["E"]:adj[a].add(b);adj[b].add(a)
    ds=[]
    used=set()
    for c,d in sorted(G["E"]):
        if len(adj[c])!=3 or len(adj[d])!=3: continue
        ends=adj[c]-{d}
        if ends==adj[d]-{c} and len(ends)==2 and c not in used and d not in used:
            ds.append((tuple(sorted(ends)),(c,d)))
            used.update([c,d])
    return ds

def reduced(G,ds):
    parent=list(range(G["V"]))
    def find(x):
        while x!=parent[x]:
            parent[x]=parent[parent[x]]
            x=parent[x]
        return x
    for (a,b),_ in ds:
        parent[find(b)]=find(a)
    removed={z for _,pair in ds for z in pair}
    verts={find(i) for i in range(G["V"]) if i not in removed}
    eds=set()
    for a,b in G["E"]:
        if a not in removed and b not in removed:
            a,b=find(a),find(b)
            if a!=b:eds.add(tuple(sorted((a,b))))
    return verts,eds

def is_wheel_or_fan(G,ds,deleted):
    verts,eds=reduced(G,ds)
    adj={v:set() for v in verts}
    for a,b in eds: adj[a].add(b);adj[b].add(a)
    r=G["r"]
    centers=[x for x in verts if len(adj[x])>=4]
    if len(verts)!=r+1 or len(centers)!=1:return False
    center=centers[0]
    rest=verts-{center}
    if any(center not in adj[x] for x in rest):return False
    deg=sorted(len(adj[x]&rest) for x in rest)
    return deg==([1,1]+[2]*(r-2) if deleted else [2]*r)

def valid(G,color):
    return len(color)==G["V"] and all(color[a]!=color[b] for a,b in G["E"])

def deletion_model(G,deleted):
    c={i:2 for i in range(G["n"])}
    for k in range(G["r"]):
        c[G["rim"][(deleted+1+k)%G["r"]]]=k%2
    for a,b in G["diamonds"].values():c[a]=0;c[b]=1
    return c

def signature():
    ways={}
    for a,b in itertools.product(range(3),repeat=2):
        ways[(a,b)]=sum(1 for c,d in itertools.product(range(3),repeat=2)
                        if c!=d and a not in (c,d) and b not in (c,d))
    assert all(ways[a,b]==(2 if a==b else 0) for a,b in ways)
    return {"diagonal":2,"off_diagonal":0,"pairs":len(ways)}

def audit(H,label):
    G=make(H)
    n=G["n"]
    assert G["V"]==5*n-1 and len(G["E"])==19*n//2-2
    ds=detect(G)
    assert len(ds)==len(G["HE"])
    assert set(e for e,_ in ds)==set(G["HE"])
    assert is_wheel_or_fan(G,ds,False)
    assert 4*G["V"]+3*len(G["E"])==97*n//2-10
    for j in range(G["r"]):
        neighbor=make(H,j)
        assert is_wheel_or_fan(neighbor,detect(neighbor),True)
        assert valid(neighbor,deletion_model(neighbor,j))
    # Disjoint H edges certify vertex-disjoint induced option-graph P3 obstructions.
    used=set();matching=[]
    for a,b in G["HE"]:
        if a not in used and b not in used:
            matching.append((a,b));used.update((a,b))
    assert len(matching)>= (3*n+9)//10
    return {"source":label,"hub_clones":n,"graph_vertices":G["V"],
            "graph_edges":len(G["E"]),"cnf_vars":3*G["V"],
            "cnf_clauses":4*G["V"]+3*len(G["E"]),
            "diamonds_found":len(ds),"matching_lower_bound":len(matching),
            "SAT_neighbors_checked":G["r"]}

def main():
    signature()
    cases=[audit(prism(k),"prism("+str(k)+")") for k in (3,4,5,6,8,12)]
    for n in (10,12,16,20,30):
        cases.append(audit(random_cubic(n,20261123+n),"cubic("+str(n)+")"))
    assert len(cases)==11
    assert sum(x["SAT_neighbors_checked"] for x in cases)==153
    print(json.dumps({"status":"PASS","diamond_signature":signature(),
                      "cases":cases,"SAT_neighbors":153},indent=2))

if __name__=="__main__":main()
