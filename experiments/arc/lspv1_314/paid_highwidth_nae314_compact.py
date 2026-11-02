#!/usr/bin/env python3
"""Exact paired-support/bipartite decision terminal and explicit large-treewidth canonical controls.
LSPV-1 2026-11-01 18:00 PST. Independent expanded verifier/raw in reproducibility archive.
Classical Hall perfect-matching technique; no unrestricted P-vs-NP claim.
"""
from collections import Counter, defaultdict, deque
from itertools import combinations
import hashlib, json

def canonical(F):
    if not F or any(len(c)!=3 or len({abs(x) for x in c})!=3 or
                    not (all(x>0 for x in c) or all(x<0 for x in c)) for c in F):
        return False
    n=max(abs(x) for c in F for x in c)
    cnt=Counter(x for c in F for x in c)
    return (3*len(F)==4*n and
            len({tuple(sorted(c)) for c in F})==len(F) and
            all(cnt[v]==cnt[-v]==2 for v in range(1,n+1)))

def satisfied(F,a):
    return all(any((a[abs(x)]==1)==(x>0) for x in c) for c in F)

def grid_source(k):
    assert k>=4 and not k%2
    def port(i,j,t): return (i%k,j%k,t)
    edges=set(); chosen=set()
    for i in range(k):
        for j in range(k):
            N,E,S,W=[port(i,j,p) for p in "NESW"]
            for v,w,on in ((N,E,1),(E,S,0),(S,W,1),(W,N,0),
                           (E,port(i,j+1,'W'),0),(S,port(i+1,j,'N'),0)):
                edge=tuple(sorted((v,w)))
                assert edge not in edges
                edges.add(edge)
                if on: chosen.add(edge)
    ordered=sorted(edges)
    incid=defaultdict(list)
    for x,(v,w) in enumerate(ordered,1):
        incid[v].append(x);incid[w].append(x)
    pos=tuple(tuple(sorted(incid[v])) for v in sorted(incid))
    F=pos+tuple(tuple(-x for x in c) for c in pos)
    witness={x:int(edge in chosen) for x,edge in enumerate(ordered,1)}
    assert len(incid)==4*k*k and len(edges)==6*k*k and canonical(F)
    assert satisfied(F,witness)
    return F,witness

def paired_bipartite_decision(F, make_witness=False):
    """INVALID, SAT or UNRESOLVED. The SAT decision needs no witness construction."""
    if not canonical(F):return "INVALID",None
    pos=[tuple(sorted(map(abs,c))) for c in F if c[0]>0]
    neg=[tuple(sorted(map(abs,c))) for c in F if c[0]<0]
    if set(pos)!=set(neg):return "UNRESOLVED",None
    incid=defaultdict(list)
    for i,clause in enumerate(pos):
        for x in clause:incid[x].append(i)
    n=max(abs(x) for c in F for x in c)
    if any(len(incid[x])!=2 for x in range(1,n+1)):return "UNRESOLVED",None
    adj=[[] for _ in pos]
    for x in range(1,n+1):
        v,w=incid[x];adj[v].append((w,x));adj[w].append((v,x))
    colors={}
    for start in range(len(pos)):
        if start in colors:continue
        colors[start]=0; queue=deque([start])
        while queue:
            v=queue.popleft()
            for w,x in adj[v]:
                if w not in colors:colors[w]=1-colors[v];queue.append(w)
                elif colors[w]==colors[v]:return "UNRESOLVED",None
    if not make_witness:return "SAT",None
    left=[i for i in colors if colors[i]==0]
    paired_right={}
    def visit(u,seen):
        for v,x in adj[u]:
            if v in seen:continue
            seen.add(v)
            if v not in paired_right or visit(paired_right[v][0],seen):
                paired_right[v]=(u,x);return True
        return False
    if any(not visit(u,set()) for u in left):raise AssertionError("Hall failure")
    a={x:0 for x in range(1,n+1)}
    for _,x in paired_right.values():a[x]=1
    assert satisfied(F,a)
    return "SAT",a

def gamma(x):
    b=bin(x)[2:]
    return "0"*(len(b)-1)+b

def encode(F):
    assert canonical(F)
    n=max(abs(x) for c in F for x in c)
    w=n.bit_length()
    return gamma(n)+gamma(len(F))+''.join(
        ('1' if c[0]>0 else '0')+''.join(format(abs(x),f'0{w}b') for x in c)
        for c in F)

F9_P=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
F9_N=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
F9=F9_P+tuple(tuple(-x for x in c) for c in F9_N)

def models(F,p=None):
    p=p or {}
    n=max(abs(x) for c in F for x in c)
    out=[]
    for z in range(1<<n):
        a={i:(z>>(i-1))&1 for i in range(1,n+1)}
        if all(a[x]==v for x,v in p.items()) and satisfied(F,a):out.append(z)
    return out

def main():
    records=[]
    for k in (4,6,8):
        F,a=grid_source(k)
        verdict,empty=paired_bipartite_decision(F)
        assert verdict=="SAT" and empty is None
        assert paired_bipartite_decision(F,True)[0]=="SAT"
        b=encode(F)
        records.append(dict(k=k,n=6*k*k,m=8*k*k,bits=len(b),
            signed_delta=4*k*k,primal_treewidth_floor=(k-2)/2,
            source_sha256=hashlib.sha256(b.encode()).hexdigest()))
    assert len(models(F9))==70
    pS={1:0,3:0,5:1,6:0,7:0,8:0};pU=dict(pS,x1=1) if False else {**pS,1:1}
    assert len(models(F9,pS))==2 and not models(F9,pU)
    P6=((1,2,3),(1,4,5),(2,4,6),(3,5,6))
    K4=P6+tuple(tuple(-x for x in c) for c in P6)
    assert canonical(K4) and len(models(K4))==18
    assert paired_bipartite_decision(K4)[0]=="UNRESOLVED"
    print(json.dumps({"status":"RESTRICTED_EXACT_P_VS_NP_OPEN","cases":records,
                      "F9_SAT_UNSAT_residuals":[2,0],
                      "K4_paired_nonbipartite":"UNRESOLVED"},indent=2))
if __name__=="__main__":main()
