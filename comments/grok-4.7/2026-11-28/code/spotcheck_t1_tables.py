#!/usr/bin/env python3
"""Grok independent spot-check of T1 signed all-B (sum2) K5 / K5-e / K4 terminal tables.
Model (from T1 report 0686e24): each vertex has 4 ports, exactly two set (B = sum2).
Internal edge (i,j) with sign s: bit at i's port = x, bit at j's port = x XOR s.
Exposed ports carry boundary bits; boundary word bit i = exposed port at vertex i."""
import itertools, json
def support(n, edges, exposed, signs):
    # exposed: list of vertices with one exposed port (order = boundary bit order)
    sup=set()
    for xs in itertools.product((0,1), repeat=len(edges)):
        occ=[0]*n
        for (i,j),s,x in zip(edges,signs,xs):
            occ[i]+=x; occ[j]+=x^s
        need=[2-occ[v] for v in range(n)]
        ok=True; w=0
        for v in range(n):
            e = 1 if v in exposed else 0
            if not (0<=need[v]<=e): ok=False;break
        if not ok: continue
        for k,v in enumerate(exposed):
            w|=need[v]<<k
        sup.add(w)
    return sup
out={}
# closed K5
E5=list(itertools.combinations(range(5),2))
feas_even=feas_odd=inf_even=inf_odd=0
for sg in itertools.product((0,1),repeat=10):
    f=bool(support(5,E5,[],sg)); ev=sum(sg)%2==0
    if f and ev: feas_even+=1
    elif f: feas_odd+=1
    elif ev: inf_even+=1
    else: inf_odd+=1
out['K5_closed']=dict(feasible_even=feas_even,feasible_odd=feas_odd,infeasible_even=inf_even,infeasible_odd=inf_odd)
# K5 minus edge 01, exposed ports at 0,1
E5e=[e for e in E5 if e!=(0,1)]
bad=0
for sg in itertools.product((0,1),repeat=9):
    S=support(5,E5e,[0,1],sg); par=sum(sg)%2
    want={w for w in range(4) if bin(w).count('1')%2==par}
    if S!=want: bad+=1
out['K5e_signings_not_full_parity']=bad
# K4 with one exposed port per vertex; edge order (01,02,03,12,13,23), bit k of mask = sign of edge k
E4=list(itertools.combinations(range(4),2))
full=0; tables={}
for m in range(64):
    sg=[(m>>k)&1 for k in range(6)]
    S=support(4,E4,[0,1,2,3],sg); par=sum(sg)%2
    want={w for w in range(16) if bin(w).count('1')%2==par}
    assert S<=want
    if S==want: full+=1
    else: tables[m]=sorted(S)
out['K4_full_parity_signings']=full
out['K4_exceptions']={str(k):v for k,v in tables.items()}
print(json.dumps(out,indent=1))
