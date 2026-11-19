#!/usr/bin/env python3
"""T5 original-source finite-domain bucket reference, no witness advice.
Independent executable *algorithm*, not the gate-level Boolean compiler.
The source-aware netlist compiler and independent DAG replayer are in archive.
"""
import argparse,itertools,json,pathlib

def read(path):
    lines=pathlib.Path(path).read_text().splitlines()
    p,t,n,m=lines[0].split();assert (p,t)==('p','t5');n=int(n);m=int(m)
    assert lines[1:n+1]==[f'v {v}' for v in range(n)]
    edges=[]
    for row in lines[n+1:]:
        a,u,v=row.split();assert a=='a';u=int(u);v=int(v)
        assert 0<=u<n and 0<=v<n and u!=v
        edges.append((u,v))
    assert len(edges)==m and edges==sorted(set(edges))
    assert all((v,u) not in edges for u,v in edges)
    return n,edges

def R(a,b):return ((b-a)%5) in (1,3)

def solve(n,host,active,root,order):
    assert set(active)<=set(host)
    assert sorted(order)==sorted(set(range(n))-{root})
    # Each factor is a scope and exact five-domain relation table.
    factors=[]
    for u,v in active:
        scope=tuple(sorted({u,v}-{root}))
        table={key:R(0 if u==root else key[scope.index(u)],
                     0 if v==root else key[scope.index(v)])
               for key in itertools.product(range(5),repeat=len(scope))}
        factors.append((scope,table))
    trace=[]
    for v in order:
        bucket=[f for f in factors if v in f[0]]
        factors=[f for f in factors if v not in f[0]]
        remainder=tuple(sorted({q for scope,_ in bucket for q in scope}-{v}))
        message={};entry={}
        for vals in itertools.product(range(5),repeat=len(remainder)):
            assignment=dict(zip(remainder,vals))
            for color in range(5):
                assignment[v]=color
                entry[(vals,color)]=all(tab[tuple(assignment[q] for q in scope)]
                                         for scope,tab in bucket)
            message[vals]=any(entry[(vals,color)] for color in range(5))
        factors.append((remainder,message))
        trace.append((v,remainder,entry))
    assert len(factors)==1 and factors[0][0]==()
    if not factors[0][1][()]:return None
    coloring={root:0}
    for v,remainder,entry in reversed(trace):
        vals=tuple(coloring[q] for q in remainder)
        coloring[v]=next(c for c in range(5) if entry[(vals,c)])
    witness=tuple(coloring[i] for i in range(n))
    assert all(R(witness[u],witness[v]) for u,v in active)
    return witness

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('source')
    ap.add_argument('--missing-edge-index',type=int,default=-1)
    ap.add_argument('--root',type=int,required=True)
    ap.add_argument('--order',required=True,help='JSON list of n-1 vertex IDs')
    args=ap.parse_args();n,edges=read(args.source)
    active=edges if args.missing_edge_index<0 else [e for i,e in enumerate(edges)
                                                    if i!=args.missing_edge_index]
    colors=solve(n,edges,active,args.root,json.loads(args.order))
    print(json.dumps({'sat':colors is not None,'n':n,'active_edges':len(active),
                      'colors':colors,'pin_root':args.root}))
