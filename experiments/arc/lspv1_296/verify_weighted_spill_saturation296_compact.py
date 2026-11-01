#!/usr/bin/env python3
"""Independent truth-table/certificate checker for ARC-SATURATION296.
Imports no producer code, uses direct bit masks and original source IDs.
"""
from collections import Counter
from itertools import product
F=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),
(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15),
(-1,-2,-11),(-2,-3,-11),(-1,-3,-12),(-4,-5,-13),
(-5,-6,-14),(-4,-6,-15),(-7,-8,-12),(-8,-9,-13),
(-9,-10,-14),(-10,-7,-15))
P={'UNSAT':(0,0,0,0,1,1,1,1,0),'SAT':(1,0,0,0,1,1,1,1,0)}
C={'UNSAT':((1,2,12),(3,4,15)),'SAT':((11,2,12),(3,4,15))}
def t(mask,c):return sum(bool(mask&(1<<(abs(x)-1)))==(x>0) for x in c)
def sat(mask):return all(t(mask,c)>0 for c in F)
def live(p):
    r={};s={i:[0,0] for i in range(1,7)}
    for j,c in enumerate(F,1):
        hit=any(p[abs(x)-1]==int(x>0) for x in c)
        if hit:
            for x in c:
                if abs(x)<=6:s[abs(x)][int(x<0)]+=1
        else:r[j]=tuple(x for x in c if p[abs(x)-1]<0)
    return r,s
def check_cycle(r,cy):
    degree=Counter();adj={}
    for j in cy:
        c=r[j]; assert len(c)==2
        u,v=map(abs,c);degree.update((u,v));adj.setdefault(u,set()).add(v);adj.setdefault(v,set()).add(u)
    assert len(cy)%2 and len(cy)>=3
    assert len(degree)==len(cy) and all(v==2 for v in degree.values())
    reach={next(iter(degree))};stack=list(reach)
    while stack:
        for v in adj[stack.pop()]:
            if v not in reach:reach.add(v);stack.append(v)
    assert len(reach)==len(degree)
def main():
    assert len(set(tuple(sorted(c)) for c in F))==20
    occurrences=Counter(x for c in F for x in c)
    assert all(occurrences[i]==occurrences[-i]==2 for i in range(1,16))
    assert all(len(set(map(abs,c)))==3 and (all(x>0 for x in c) or all(x<0 for x in c)) for c in F)
    allw=[a for a in range(1<<15) if sat(a)]
    assert len(allw)==1032
    out={};assertions=0
    for name,pins in P.items():
        p=(-1,)*6+pins;r,s=live(p)
        e=2*6-len(r);eta=sum(min(a,b) for a,b in s.values())
        used=set()
        for cy in C[name]:
            assert used.isdisjoint(cy);used.update(cy);check_cycle(r,cy)
        gap=e-eta-len(C[name])
        sol=[a for a in allw if all(((a>>(i+6))&1)==b for i,b in enumerate(pins))]
        force={i:int(b>a) for i,(a,b) in s.items() if abs(a-b)>gap} if gap>=0 else {}
        if name=='UNSAT':assert gap==-1 and not sol
        else:
            assert gap==0 and len(sol)==2 and force=={1:0,2:0,4:1}
            for mask in sol:
                assert all(((mask>>(i-1))&1)==v for i,v in force.items())
                for j,c in r.items():
                    if len(c)==3 or (len(c)==2 and j not in used):assert t(mask,c)==1
        out[name]={'gap':gap,'solutions':len(sol),'forced':force};assertions+=1+len(sol)
    print({'status':'PASS','all_source_witnesses':1032,'checks':assertions,
           'same_source':out,'scope':'finite certificate replay, ARC/FLMV OPEN'})
if __name__=='__main__':main()
