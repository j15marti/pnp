#!/usr/bin/env python3
"""LSPV-2 336. One-sided-prism source SAT/#SAT. P versus NP OPEN.
Run: python experiments/arc/lspv2_336_compact.py
Depends only on previously verified sibling lspv2_335_compact.py.
"""
from collections import defaultdict
from lspv2_335_compact import accept, discover, prism
import json

def source_dp(F,n,pins=None):
    if not accept(F,n): return "MALFORMED",None
    neg=[c for c in F if c[0]<0]
    virtual=[tuple(-x for x in c) for c in neg]+neg
    label,graph=discover(virtual,n)
    if label!="PRISM":return "UNRESOLVED",None
    order,ends=graph
    pos={frozenset(c):j for j,c in enumerate(F) if c[0]>0}
    paired={i for i,c in enumerate(neg) if frozenset(-x for x in c) in pos}
    matched={pos[frozenset(-x for x in neg[i])] for i in paired}
    defect=[j for j,c in enumerate(F) if c[0]>0 and j not in matched]
    memberships=defaultdict(list)
    for d,j in enumerate(defect):
        for x in F[j]:memberships[x].append(d)
    r=[3]*len(neg);s=[3]*len(defect);states={((),()):1};peak=1;work=0
    pins=pins or {}
    for x in order:
        u,v=ends[x];new={}
        for (vk,dk),ways in states.items():
            for bit in ([pins[x]] if x in pins else [0,1]):
                work+=1;vv=dict(vk);dd=set(dk);bad=False
                for z in (u,v):
                    val=vv.get(z,0)|((1<<bit) if z in paired else int(bit==0))
                    if r[z]==1:
                        if (z in paired and val!=3) or (z not in paired and not(val&1)):
                            bad=True;break
                        vv.pop(z,None)
                    else:vv[z]=val
                if bad:continue
                for d in memberships[x]:
                    if bit:dd.add(d)
                    if s[d]==1:
                        if d not in dd:bad=True;break
                        dd.remove(d)
                if bad:continue
                key=(tuple(sorted(vv.items())),tuple(sorted(dd)))
                new[key]=new.get(key,0)+ways
        states=new;r[u]-=1;r[v]-=1
        for d in memberships[x]:s[d]-=1
        assert len(states)<=1+3**6*2**len(defect)
        peak=max(peak,len(states))
    return "EXACT",{"count":states.get(((),()),0),"peak":peak,"work":work,"d":len(defect)}

def swap_prism(k):
    F=[list(c) for c in prism(k)]
    for i in range(2*k):
        for j in range(i+1,2*k):
            if set(F[i])&set(F[j]):continue
            for a in range(3):
                for b in range(3):
                    G=[c[:] for c in F]
                    G[i][a],G[j][b]=G[j][b],G[i][a]
                    if accept(G,3*k):
                        P={frozenset(c) for c in G if c[0]>0}
                        M={frozenset(-z for z in c) for c in G if c[0]<0}
                        if len(P-M)==2:return G
    raise AssertionError("swap not found")

if __name__=="__main__":
    result={}
    for k in (3,4,5,6,8):
        label,r=source_dp(swap_prism(k),3*k)
        assert label=="EXACT"
        result[k]=r
    print(json.dumps({"status":"PROVED/EXACT restricted; P vs NP OPEN",
                      "swapped_prism_cases":result},indent=2))
