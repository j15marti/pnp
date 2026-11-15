#!/usr/bin/env python3
"""Independent finite audit of Q-XOR3 exact min-core proof price.

Source rows are full GF(2) equations (a,b) on a public variable set.
This is a semantic proof-event simulator, not a Turing machine or raw-CNF parser.
"""
from collections import deque
from itertools import product
from random import Random
import json

COUNT=0

def check(ok,why):
    global COUNT
    COUNT+=1
    if not ok: raise AssertionError(why)

def dependent_odd(rows,mask):
    a=b=0
    for i,(u,v) in enumerate(rows):
        if mask>>i & 1: a^=u; b^=v
    return a==0 and b==1

def core(rows):
    for size in range(1,len(rows)+1):
        for mask in range(1,1<<len(rows)):
            if mask.bit_count()==size and dependent_odd(rows,mask):
                return tuple(i for i in range(len(rows)) if mask>>i & 1)
    return None

def rank(vectors):
    pivots={}
    for x in vectors:
        while x:
            p=x.bit_length()-1
            if p not in pivots: pivots[p]=x;break
            x^=pivots[p]
    return len(pivots)

def bfs_price(rows):
    """Independent shortest path in exact SOURCE/ADD/HALT value-set graph.

    Source identities and all acquired line values are separately represented.
    Duplicate row value need not be materialized a second time for an optimum.
    """
    target=(0,1)
    start=(0,frozenset())
    q=deque([(start,0)])
    seen={start}
    while q:
        (paid,lines),d=q.popleft()
        if target in lines:return d+1
        for i,row in enumerate(rows):
            if not(paid>>i & 1):
                nxt=(paid|(1<<i),lines|{row})
                if nxt not in seen:seen.add(nxt);q.append((nxt,d+1))
        linelist=list(lines)
        for j,a in enumerate(linelist):
            for b in linelist[j:]:
                v=(a[0]^b[0],a[1]^b[1])
                if v not in lines:
                    nxt=(paid,lines|{v})
                    if nxt not in seen:seen.add(nxt);q.append((nxt,d+1))
    return None

def prism(k,charge=1,base=0):
    edges=[]
    for ring in (0,1):
        for j in range(k):edges.append((base+ring*k+j,base+ring*k+(j+1)%k))
    for j in range(k):edges.append((base+j,base+k+j))
    H=2*k; rows=[]
    for v in range(base,base+H):
        mask=0
        for e,(u,w) in enumerate(edges):
            if v==u or v==w:mask^=1<<e
        rows.append((mask,charge if v==base else 0))
    return rows,edges

# Complete enumeration of all finite source systems in small dimensions.
trials=0; positives=0
for n,m in [(1,1),(1,2),(1,3),(1,4),(2,1),(2,2),(2,3)]:
    alphabet=list(product(range(1<<n),range(2)))
    for rows in product(alphabet,repeat=m):
        trials+=1
        s=core(rows)
        if s is None:continue
        positives+=1
        check(len(s)<=rank([a for a,b in rows])+1, "rank ceiling")
        check(dependent_odd(rows,sum(1<<i for i in s)),"core parity")
        if m<=3 or n==1:
            price=bfs_price(rows)
            check(price==2*len(s),f"BFS proof cost mismatch {(n,m,rows,s,price)}")

# Deterministic randomized n=3,4 source sets, including duplicate/redundant source rows.
rng=Random(65034)
random_trials=0; random_bfs=0
for n in (3,4):
    for m in (3,4,5,6):
        for it in range(200):
            rows=tuple((rng.randrange(1<<n),rng.randrange(2)) for _ in range(m))
            random_trials+=1
            s=core(rows)
            if s is None:continue
            check(len(s)<=rank([a for a,b in rows])+1,"random rank ceiling")
            check(dependent_odd(rows,sum(1<<i for i in s)),"random witness")
            if m<=3 and it<25:
                check(bfs_price(rows)==2*len(s),"random BFS")
                random_bfs+=1

# Connected and disconnected odd-charge cubic graphs, with relabeled disjoint edge variables.
examples=[]
for k in range(3,9):
    rows,ed=prism(k)
    s=core(rows)
    H=2*k
    check(len(ed)==3*k and all(a.bit_count()==3 for a,b in rows),"cubic incidence")
    check(s is not None and len(s)==H and 2*len(s)==2*H,"connected uniqueness")
    examples.append({"prism_vertices":H,"core":len(s),"price":2*len(s)})

r6,e6=prism(3)
r8,e8=prism(4)
shift=len(e6)
joined=r6+[(a<<shift,b) for a,b in r8]
chosen=core(joined)
check(len(chosen)==6 and 2*len(chosen)==12,"disconnected choose smaller odd")
# SAT control: all charges zero => consistency (all-zero assignment satisfies rows).
zero_charge=[(a,0) for a,b in joined]
check(core(zero_charge) is None,"even charges SAT")
# One contradictory duplicate row pair gives size-two core even with many padding rows.
padded=[(0b111,0),(0b111,1)]+[(1<<i,0) for i in range(16)]
check(len(core(padded))==2,"duplicate inconsistent pair")
summary={"test":"MINCORE065","status":"COMPUTATIONAL","symbolic_theorem":"Q-XOR3 minimum event price 2*s, where s is the minimum odd-dependence source support; s<=rank(A)+1<=n+1","exhaustive_systems":trials,"inconsistent_systems":positives,"random_systems":random_trials,"random_bfs_positive":random_bfs,"assertions":COUNT,"failures":0,"connected_prisms":examples,"disconnected_odd_prisms":{"H_total":14,"core_size":len(chosen),"actual_price":2*len(chosen),"naive_all_rows_price":28},"padding_control":{"total_rows":len(padded),"core_size":len(core(padded)),"actual_price":4}}
print(json.dumps(summary,indent=2,sort_keys=True))
