#!/usr/bin/env python3
"""TMR-2/091 compact independent fixed-T5 cycle-rank obstruction verifier."""
from itertools import product, combinations
from collections import Counter
import json
R=lambda a,b:(b-a)%5 in (1,3)
def tensor(w):
    q=[1,0,0,0,0]
    for s in w:
        nxt=[0]*5
        for d,x in enumerate(q):
            for step in ((1,3) if s=='+' else (2,4)):
                nxt[(d+step)%5]+=x
        q=nxt
    return q
def count_paths(ws):
    rows=[tensor(w) for w in ws]
    return 5*sum(__import__('math').prod(row[d] for row in rows) for d in range(5))
def expand(ws):
    arcs=[];n=2
    for w in ws:
        path=[0]+list(range(n,n+len(w)-1))+[1];n+=len(w)-1
        for u,v,s in zip(path,path[1:],w):
            arcs.append((u,v) if s=='+' else (v,u))
    return n,tuple(arcs)
def direct(n,arcs):
    pred=[[] for _ in range(n)]
    for u,v in arcs:
        if u>v: pred[u].append((v,False))
        else:pred[v].append((u,True))
    a=[0]*n;z=0
    def dfs(k):
        nonlocal z
        if k==n: z+=1;return
        for b in range(5):
            a[k]=b
            if all(R(a[v],b) if forward else R(b,a[v]) for v,forward in pred[k]):dfs(k+1)
    dfs(0)
    return z
assert [sorted(i for i,v in enumerate(tensor('+'*k)) if v) for k in (1,2,3,4)] == [[1,3],[1,2,4],[0,2,3,4],[0,1,2,3,4]]
for k in range(1,5):
    for w in product('+-',repeat=k):
        assert sum(tensor(w))==2**k
        assert sum(v>0 for v in tensor(w))==(k+1 if k<4 else 5)
# Sharp analytic rank-two theorem has no theta orientation of girth >=5 that is UNSAT.
r2=0
for a in range(1,5):
  for b in range(a,5):
    for c in range(b,5):
      if sum(k==1 for k in (a,b,c))>1 or a+b<5:continue
      for x in product('+-',repeat=a):
        for y in product('+-',repeat=b):
          for z in product('+-',repeat=c):
            assert count_paths((''.join(x),''.join(y),''.join(z)))>0
            r2+=1
# Low-girth small NOs and exact edge-deletion checks.
no4=(4,((0,1),(1,2),(0,3),(1,3),(2,3)))
no5=expand(('++','+-','--'))
for n,edges in [no4,no5]:
    assert direct(n,edges)==0
    for i in range(len(edges)):
        assert direct(n,edges[:i]+edges[i+1:])>0
# FIRST girth-five obstruction: four paths with three independent cycles.
words=('++','+++','++-','---')
n,edges=expand(words)
rows=[tensor(w) for w in words]
zeros=[sorted(i for i,x in enumerate(row) if x==0) for row in rows]
assert (n,len(edges))==(9,11)
assert zeros==[[0,3],[1],[2],[4]]
assert count_paths(words)==direct(n,edges)==0
proper=[count_paths(words[:i]+words[i+1:]) for i in range(4)]
assert proper==[90,15,15,10]
for i in range(11):assert direct(n,edges[:i]+edges[i+1:])>0
yes=edges[1:];yes=((edges[0][1],edges[0][0]),)+yes
assert direct(n,yes)==135
g5=Counter()
for a in product('+-',repeat=2):
 for b,c,d in product(list(product('+-',repeat=3)),repeat=3):
    g5['UNSAT' if count_paths((''.join(a),''.join(b),''.join(c),''.join(d)))==0 else 'SAT']+=1
assert g5=={'SAT':2012,'UNSAT':36}
g6=Counter()
for a,b,c,d in product(list(product('+-',repeat=3)),repeat=4):
    g6['SAT' if count_paths((''.join(a),''.join(b),''.join(c),''.join(d)))>0 else 'UNSAT']+=1
assert g6=={'SAT':4096}
# K4 edge-double-subdivision, 4096 orientation combinations; no UNSAT.
edges4=list(combinations(range(4),2))
truth=list(product(range(5),repeat=4))
km=[]
for u,v in edges4:
    options=[]
    for w in product('+-',repeat=2):
        row=tensor(w);mask=0
        for i,x in enumerate(truth):
            if row[(x[v]-x[u])%5]:mask|=1<<i
        options.append(mask)
    km.append(options)
min_live=625
for p in product(range(4),repeat=6):
    m=(1<<625)-1
    for edge,j in enumerate(p):m &= km[edge][j]
    min_live=min(min_live,m.bit_count())
assert min_live==5
print(json.dumps({'revision':'TMR2_T5_BICYCLIC_TRANSFER091',
'proven_scope':'girth >=5 and cycle rank <=2 always SAT for simple oriented graphs',
'NO9':{'vertices':9,'arcs':11,'girth':5,'cycle_rank':3,'count':0,
'forbidden_terminal_differences':zeros,'three_path_count_controls':proper,
'one_edge_flip_yes_count':135},
'girth5_4path_orientation_census':dict(g5),
'girth6_4path_orientation_census':dict(g6),
'girth6_2subdivided_K4_min_endpoint_count':min_live,
'girth5_rank2_orientations_tested':r2,'P_versus_NP':'OPEN'},indent=2))
