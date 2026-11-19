#!/usr/bin/env python3
"""Self-contained deterministic replay of critical T5 cycle-chain obstruction covers."""
from itertools import product
import json, hashlib

def valid(a,b): return (b-a)%5 in (1,3)
def support(w):return {(len(w)+w.count('B')+2*j)%5 for j in range(len(w)+1)}
def closure(t):
    d=(-t)%5
    return 'BB' if d==0 else 'B'*(d-1)+'F'*(4-d)
def instance(t):
    v=t+1; arcs=[]; paths=[]
    def add(u,w,word):
        nonlocal v
        chain=[u]+list(range(v,v+len(word)-1))+[w];v+=len(word)-1
        ids=[]
        for (a,b),c in zip(zip(chain,chain[1:]),word):
            if c=='B':a,b=b,a
            ids.append(len(arcs));arcs.append((a,b))
        paths.append((chain,ids,word))
    for j in range(t):add(j,j+1,'F');add(j,j+1,'FBB')
    add(t,0,closure(t))
    return v,arcs,paths

def extension(path,arcs,a,b,omit=-1):
    verts,ids,_=path
    for p in product(range(5),repeat=len(verts)-2):
        d=dict(zip(verts,[a]+list(p)+[b]))
        if all(i==omit or valid(d[arcs[i][0]],d[arcs[i][1]]) for i in ids):return d
    return None

def check(t):
    n,arcs,ps=instance(t);assert len(ps)==2*t+1
    for j,p in enumerate(ps):
        empirical={d for d in range(5) if extension(p,arcs,0,d) is not None}
        assert empirical==support(p[2])
    for i in range(t):assert support('F')&support('FBB')=={1}
    assert (-t)%5 not in support(closure(t))
    witnesses=0
    for selected,p in enumerate(ps):
        diffs=[1]*t
        if selected<2*t:diffs[selected//2]=0 if selected%2==0 else 3
        terminals=[0]
        for d in diffs:terminals.append((terminals[-1]+d)%5)
        bad=[j for j,q in enumerate(ps) if extension(q,arcs,terminals[q[0][0]],terminals[q[0][-1]]) is None]
        assert bad==[selected],(t,selected,bad)
        for removed in p[1]:
            assignment={}
            for q in ps:
                z=extension(q,arcs,terminals[q[0][0]],terminals[q[0][-1]],removed)
                assert z is not None
                for x,c in z.items():assert x not in assignment or assignment[x]==c;assignment[x]=c
            assert len(assignment)==n
            assert all(i==removed or valid(assignment[a],assignment[b]) for i,(a,b) in enumerate(arcs))
            assert not valid(assignment[arcs[removed][0]],assignment[arcs[removed][1]])
            witnesses+=1
    assert witnesses==len(arcs)
    return {'t':t,'vertices':n,'arcs':len(arcs),'essential_paths':len(ps),'edge_deletions_SAT':witnesses,'closure':closure(t)}

if __name__=='__main__':
    out=[check(t) for t in (2,3,4,5,6,7,10,12,20)]
    print(json.dumps(out,sort_keys=True))
