#!/usr/bin/env python3
"""Independent standard-library checker for the full Tutte source-barrier JSON.
Does not import the matching producer or NetworkX.
Run from repository: python experiments/arc/lspv4_329/verify_tutte329.py
"""
import json,ast
from collections import deque
from pathlib import Path

SOURCE={
"K4":((1,2,3),(1,4,5),(2,4,6),(3,5,6)),
"K33":((1,2,3),(4,5,6),(7,8,9),(1,4,7),(2,5,8),(3,6,9))
}
RAW=Path(__file__).resolve().parents[3]/"results/raw/arc/lspv4_329/2026-11-02_0140_LSPV4_PAIRED_NAE_TUTTE_AUDIT329_full.json"

def rebuild(pos,p,h):
    q=len(pos);n=max(map(max,pos))
    free=[x for x in range(1,n+1) if p[x-1]<0]
    bounds=[]
    for C in pos:
        t=sum(p[x-1]==1 for x in C);r=sum(p[x-1]<0 for x in C)
        lo,up=max(0,1-t),min(r,2-t)
        assert lo<=up
        bounds.append((lo,up))
    B=sum(up-lo for lo,up in bounds)
    f=[up for lo,up in bounds]+[h]
    E=[]
    for x in free:
        ends=[j for j,C in enumerate(pos) if x in C]
        assert len(ends)==2
        E.append((ends[0],ends[1]))
    for v,(lo,up) in enumerate(bounds):
        E.extend([(v,q)]*(up-lo))
    ports={v:[] for v in range(q+1)}
    adj={}
    def edge(a,b):
        adj.setdefault(a,set()).add(b)
        adj.setdefault(b,set()).add(a)
    for k,(v,w) in enumerate(E):
        a=("port",k,v);b=("port",k,w)
        edge(a,b);ports[v].append(a);ports[w].append(b)
    for v in range(q+1):
        count=len(ports[v])-f[v]
        assert 0<=count<=len(ports[v])
        for j in range(count):
            d=("dummy",v,j)
            for x in ports[v]:edge(d,x)
    return adj,B,bounds

def odds_after(adj,removed):
    todo=set(adj)-removed
    count=0
    while todo:
        root=todo.pop(); seen={root}; queue=deque([root])
        while queue:
            for nxt in adj[queue.popleft()]:
                if nxt in todo:
                    todo.remove(nxt);seen.add(nxt);queue.append(nxt)
        count+=len(seen)%2
    return count

def verify(path=RAW):
    raw=json.loads(Path(path).read_text())
    checks=0
    for key,example in raw["examples"].items():
        tag=key.split(":")[0];pos=SOURCE[tag]
        pins=example["pins"]; r=example["result"]
        cases=r["h_cases"]
        if r["sat"]:
            witness=r["witness"]
            assert len(witness)==max(map(max,pos))
            assert all(a in (0,1) for a in witness)
            assert all(b<0 or a==b for a,b in zip(witness,pins))
            assert all(1<=sum(witness[x-1] for x in C)<=2 for C in pos)
            assert any(c["perfect"] for c in cases)
            checks+=1
        else:
            assert not r["local_conflict"]
            assert all(not c["perfect"] for c in cases)
            allh=[c["h"] for c in cases]
            for c in cases:
                adj,B,bounds=rebuild(pos,pins,c["h"])
                assert len(adj)==c["v"]
                assert sum(len(neighbors) for neighbors in adj.values())//2==c["edges"]
                tb=c["tutte_barrier"]
                U=set(ast.literal_eval(s) for s in tb["U"])
                assert U and U<=set(adj)
                odd=odds_after(adj,U)
                assert odd==tb["odd_components"] and len(U)==tb["U_size"]
                assert odd>len(U)
                checks+=1
            # No admissible h is itself a checked parity contradiction.
            # Rebuild intervals directly when the candidate list is empty.
            bounds=[]
            for C in pos:
                t=sum(pins[x-1]==1 for x in C)
                r=sum(pins[x-1]<0 for x in C)
                lo,up=max(0,1-t),min(r,2-t)
                assert lo<=up
                bounds.append((lo,up))
            B=sum(up-lo for lo,up in bounds)
            expected=[h for h in range(B+1)
                      if h%2==sum(up for lo,up in bounds)%2]
            assert expected==allh
    return {"status":"PASS","independent_witness_barrier_checks":checks,
            "scope":"finite original source/Tutte, no native FLMV"}

if __name__=="__main__":
    print(json.dumps(verify(),sort_keys=True))
