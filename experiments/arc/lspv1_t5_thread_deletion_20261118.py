#!/usr/bin/env python3
"""Independent original-arc T5 critical-thread audit; Python 3 stdlib."""
from itertools import product
from collections import Counter
from math import comb
import json

def R(a,b): return (b-a)%5 in (1,3)
words=["BBB","FBB","FFF","BB"]
arcs=[]; paths=[]; n=2
for w in words:
    vs=[0]+list(range(n,n+len(w)-1))+[1]; n+=len(w)-1
    ids=[]
    for i,c in enumerate(w):
        u,v=vs[i:i+2]
        ids.append(len(arcs)); arcs.append((u,v) if c=="F" else (v,u))
    paths.append((w,vs,ids))
assert n==9 and len(arcs)==11

def mask(L,r):
    return frozenset((L+r+2*j)%5 for j in range(L+1))
types=[(L,r,mask(L,r)) for L in range(1,4) for r in range(L+1)]
assert len(types)==9
irred=[]
for bits in range(1,512):
    f=[types[i][2] for i in range(9) if bits>>i&1]
    intersection=lambda sets: set.intersection(set(range(5)),*map(set,sets))
    if all(intersection(f[:j]+f[j+1:])!=intersection(f) for j in range(len(f))):
        irred.append(len(f))
assert max(irred)==4

def row(word):
    ans=[0]*5
    for mid in product(range(5),repeat=len(word)-1):
        for end in range(5):
            z=(0,)+mid+(end,)
            if all(R(z[i],z[i+1]) if c=="F" else R(z[i+1],z[i])
                   for i,c in enumerate(word)): ans[end]+=1
    L=len(word);r=word.count("B")
    expect=[sum(comb(L,j) for j in range(L+1)
                if (L+r+2*j)%5==d) for d in range(5)]
    assert ans==expect,(word,ans,expect)
    return ans
rows=[row(w) for w,_,_ in paths]

def count_direct(removed):
    adj=[[] for _ in range(n)]
    for i,(u,v) in enumerate(arcs):
        if i!=removed:adj[u].append((v,1));adj[v].append((u,-1))
    a=[-1]*n;a[0]=0
    found=Counter();first=None
    def dfs(left):
        nonlocal first
        if not left:
            d=a[1]%5;found[d]+=1
            if first is None:first=a[:]
            return
        vertices=[v for v in range(1,n) if a[v]<0]
        v=max(vertices,key=lambda t:(sum(a[w]>=0 for w,_ in adj[t]),len(adj[t]),-t))
        for color in range(5):
            if all(a[w]<0 or (R(color,a[w]) if s==1 else R(a[w],color))
                   for w,s in adj[v]):
                a[v]=color;dfs(left-1)
        a[v]=-1
    dfs(n-1)
    return {str(d):5*c for d,c in sorted(found.items())},first

results=[]
for e in [-1]+list(range(len(arcs))):
    direct,witness=count_direct(e)
    if e<0:assert not direct;continue
    p=next(i for i,(_,_,ids) in enumerate(paths) if e in ids)
    expect={}
    for d in range(5):
        count=5*2**(len(words[p])-1)
        for j in range(len(paths)):
            if j!=p:count*=rows[j][d]
        if count:expect[str(d)]=count
    assert direct==expect,(e,direct,expect)
    assert all(e==i or R(witness[u],witness[v]) for i,(u,v) in enumerate(arcs))
    assert not R(witness[arcs[e][0]],witness[arcs[e][1]])
    results.append(dict(removed_edge=e,thread=words[p],models=sum(expect.values()),
                        endpoint_counts=expect,witness=witness))
print(json.dumps(dict(n=n,m=len(arcs),critical=True,
                      nine_short_types=len(types),max_irredundant=max(irred),
                      unsat_full=True,deletions=results),indent=2))
