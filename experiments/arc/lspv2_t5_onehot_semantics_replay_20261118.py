#!/usr/bin/env python3
"""Independent complete-source reference check for T5 EXACTONE witness ROM semantics.
This is NOT the original authoring compiler, a SAT oracle, or the gate-counted DAG evaluator.
Use the standalone gate-level evaluator in the evidence archive for exact Boolean counts.
"""
import argparse, hashlib, itertools, json, pathlib

def read_source(path):
    raw=pathlib.Path(path).read_bytes()
    lines=raw.decode('ascii').splitlines()
    head=lines[0].split()
    assert head[:2]==['p','t5'] and len(head)==4
    n,m=map(int,head[2:])
    assert lines[1:n+1]==[f'v {i}' for i in range(n)]
    edges=[]
    for row in lines[n+1:]:
        tag,u,v=row.split()
        assert tag=='a'
        edges.append((int(u),int(v)))
    assert len(edges)==m and edges==sorted(set(edges))
    assert all(0<=u<n and 0<=v<n and u!=v and (v,u) not in edges for u,v in edges)
    return n,edges,hashlib.sha256(raw).hexdigest()

def R(a,b):
    return (b-a)%5 in (1,3)

def evaluate(n,edges,witnesses,present):
    E=set(edges)
    foreign=any(present.get((u,v),False) for u in range(n) for v in range(n)
                if u!=v and (u,v) not in E)
    missing=[i for i,e in enumerate(edges) if not present.get(e,False)]
    valid=(not foreign and len(missing)==1)
    # The one-hot output factorization is meaningful on ALL full source masks.
    col=[sum((1<<j) if any(((witnesses[i][v]>>j)&1) for i in missing) else 0
             for j in range(3)) if valid else 0 for v in range(n)]
    certified=valid and all(0<=c<5 for c in col) and all(
        R(col[u],col[v]) for u,v in edges if present.get((u,v),False))
    return bool(valid),bool(certified),col

def run(source,raw):
    n,edges,sha=read_source(source)
    data=json.loads(pathlib.Path(raw).read_text())
    assert data['source_sha256']==sha
    witnesses=data['witnesses']
    assert len(witnesses)==len(edges)
    base={e:True for e in edges}
    tested=0
    for i,e in enumerate(edges):
        x=base.copy();x[e]=False
        valid,cert,col=evaluate(n,edges,witnesses,x)
        assert valid and cert and col==witnesses[i]
        tested+=1
    assert not evaluate(n,edges,witnesses,base)[0];tested+=1
    for a,b in itertools.combinations(edges,2):
        x=base.copy();x[a]=x[b]=False
        assert evaluate(n,edges,witnesses,x)==(False,False,[0]*n)
        tested+=1
    for u in range(n):
        for v in range(n):
            if u==v or (u,v) in base:continue
            x=base.copy();x[edges[0]]=False;x[u,v]=True
            assert evaluate(n,edges,witnesses,x)==(False,False,[0]*n)
            tested+=1
    return {'source_sha256':sha,'n':n,'m':len(edges),'positive':len(edges),
            'tested_complete_source_masks':tested,'status':'PASS independent Boolean semantics'}

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('source_t5')
    ap.add_argument('compiler_raw_json')
    args=ap.parse_args()
    print(json.dumps(run(args.source_t5,args.compiler_raw_json),sort_keys=True))
