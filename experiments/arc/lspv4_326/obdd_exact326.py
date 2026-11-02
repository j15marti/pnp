#!/usr/bin/env python3
"""LSPV-4 326 independent exact cofactor subset DP for all F9 9! OBDD orders.
Offline full-truth acquisition is CHARGED, not a free SAT-solver oracle.
"""
from collections import Counter
from itertools import permutations
import json
F=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
n=9;whole=(1<<n)-1
truth=[int(all(any(bool(a&(1<<(abs(z)-1)))==(z>0) for z in c) for c in F)) for a in range(512)]
assert sum(truth)==70
def subsets(s):
    a=[];v=s
    while True:
        a.append(v)
        if v==0:break
        v=(v-1)&s
    return a[::-1]
cof={}
read_count=0
for S in range(512):
    R=whole^S;rest=subsets(R);vals=[]
    for a in subsets(S):
        v=0
        for j,r in enumerate(rest):
            v|=truth[a|r]<<j
            read_count+=1
        vals.append(v)
    cof[S]=set(vals)
assert read_count==262144
def children(vec,p,d):
    x=y=0
    for j in range(1<<(d-1)):
        idx=(j&((1<<p)-1))|((j>>p)<<(p+1))
        x|=((vec>>idx)&1)<<j
        y|=((vec>>(idx|(1<<p)))&1)<<j
    return x,y
nodes={};split_tests=0
for S in range(512):
    rem=[v for v in range(n) if not(S>>v)&1]
    for p,v in enumerate(rem):
        c=0
        for f in cof[S]:
            a,b=children(f,p,len(rem));split_tests+=1
            if a!=b:c+=1
        nodes[S,v]=c
low={whole:0};high={whole:0}
for S in range(whole-1,-1,-1):
    candidates=[(nodes[S,v]+low[S|(1<<v)],v) for v in range(n) if not(S>>v)&1]
    low[S]=min(x for x,v in candidates)
    high[S]=max(nodes[S,v]+high[S|(1<<v)] for v in range(n) if not(S>>v)&1)
hist=Counter()
natural=None
for order in permutations(range(n)):
    S=0;total=0
    for v in order:
        total+=nodes[S,v];S|=1<<v
    hist[total]+=1
    if order==tuple(range(n)):natural=total
assert (low[0],natural,high[0],hist[52],hist[80])==(52,66,80,72,48)
print(json.dumps({'status':'exact offline restricted OBDD, P vs NP OPEN',
'models':70,'min_nodes':52,'natural_nodes':66,'max_nodes':80,
'optimal_orders':72,'maximal_orders':48,'orders':sum(hist.values()),
'cofactor_truth_reads':read_count,'split_cofactor_tests':split_tests,
'distinct_cofactor_vectors_across_subsets':sum(len(x) for x in cof.values()),
'distribution':dict(sorted(hist.items()))},indent=2))
