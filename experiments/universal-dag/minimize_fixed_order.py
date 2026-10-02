#!/usr/bin/env python3
from itertools import combinations
from math import comb, log2

def clause_masks(n):
    out=[]
    A=1<<n
    for vs in combinations(range(n),3):
        for pat in range(8):
            mask=0
            for a in range(A):
                if all(((a>>vs[t])&1)==((pat>>t)&1) for t in range(3)):
                    mask |= 1<<a
            out.append(mask)
    return out

def solve(n,m):
    cs=clause_masks(n); C=len(cs); full=(1<<(1<<n))-1
    levels=[set() for _ in range(C+1)]
    levels[0].add((0,0))
    for i,cm in enumerate(cs):
        rem=C-i-1
        for k,cov in levels[i]:
            if k+rem>=m: levels[i+1].add((k,cov))
            if k<m: levels[i+1].add((k+1,cov|cm))
    ids={}
    for k,cov in levels[C]:
        ids[(C,k,cov)]=1 if k==m and cov==full else (0 if k==m else 2)
    nextid=3; widths=[]
    for i in range(C-1,-1,-1):
        local={}; cm=cs[i]; rem=C-i-1
        for k,cov in levels[i]:
            lo=ids.get((i+1,k,cov),2)
            hi=ids.get((i+1,k+1,cov|cm),2) if k<m else 2
            if lo==hi: nid=lo
            else:
                sig=(lo,hi)
                if sig not in local:
                    local[sig]=nextid; nextid+=1
                nid=local[sig]
            ids[(i,k,cov)]=nid
        widths.append(len(local))
    nodes=sum(widths)
    return C,comb(C,m),sum(map(len,levels)),nodes,max(widths),log2(nodes) if nodes else 0

for n in (3,4):
    print(n,solve(n,8))
