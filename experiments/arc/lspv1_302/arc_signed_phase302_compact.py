#!/usr/bin/env python3
"""Restricted original-source signed-payment / distance-three plateau verifier.
Standalone Python stdlib, no SAT oracle. Full source+no-import verification in ZIP.
No native indexed FLMV Turing-machine measurement. P versus NP OPEN.
"""
from itertools import product,combinations
from collections import Counter,defaultdict
import json,math

FAMILIES={
"Y6":((1,2,3),(1,4,5),(2,4,6),(3,5,6),
      (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6)),
"F9":((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
      (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9)),
"F15":((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),
       (6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15),
       (-1,-2,-11),(-2,-3,-11),(-1,-3,-12),(-4,-5,-13),(-5,-6,-14),
       (-4,-6,-15),(-7,-8,-12),(-8,-9,-13),(-9,-10,-14),(-10,-7,-15))}
def valid(F):
    n=max(abs(l) for c in F for l in c)
    counts=Counter(l for c in F for l in c)
    return n%3==0 and 3*len(F)==4*n and len({tuple(sorted(c)) for c in F})==len(F) and all(
       len(c)==3 and len(set(map(abs,c)))==3 and
       (all(x>0 for x in c) or all(x<0 for x in c)) for c in F
    ) and all(counts[i]==counts[-i]==2 for i in range(1,n+1))
def stats(F,p):
    n=len(p); pos=Counter();neg=Counter();live=[];B=[]
    for j,c in enumerate(F,1):
        free=[l for l in c if p[abs(l)-1]<0]
        if any(p[abs(l)-1]==int(l>0) for l in c):
            for l in free:
                if l>0:pos[l]+=1
                else:neg[-l]+=1
        else:
            live.append(j)
            if len(free)==2:B.append((j,abs(free[0]),abs(free[1])))
    free=[x for x in range(1,n+1) if p[x-1]<0]
    e=2*len(free)-len(live)
    eta=sum(min(pos[x],neg[x]) for x in free)
    return dict(e=e,eta=eta,r=e-eta,pos=pos,neg=neg,free=free,
                uncovered=live,binary=B)
def distance_three(F,n):
    adj=[set() for _ in range(n+1)]
    for c in F:
        for x,y in combinations([abs(l) for l in c],2):
            adj[x].add(y);adj[y].add(x)
    assert max(map(len,adj))<=8
    remaining=set(range(1,n+1));out=[]
    while remaining:
        x=min(remaining);out.append(x);ball={x}|adj[x]
        for y in adj[x]:ball.update(adj[y])
        remaining.difference_update(ball)
    assert len(out)>=math.ceil(n/65)
    for x,y in combinations(out,2):
        assert y not in adj[x] and not adj[x].intersection(adj[y])
    return out
def oddcycle(B):
    adj=defaultdict(list)
    for _,x,y in B:adj[x].append(y);adj[y].append(x)
    color={}
    for r in adj:
        if r in color:continue
        color[r]=0;queue=[r]
        for x in queue:
            for y in adj[x]:
                if y not in color:
                    color[y]=1-color[x];queue.append(y)
                elif color[y]==color[x]:return True
    return False
def pivot_law(F,p,x,b):
    s=stats(F,p);q=list(p);q[x-1]=b;t=stats(F,q)
    sx=s['pos'][x] if b else s['neg'][x]
    sxmin=min(s['pos'][x],s['neg'][x])
    acquired=sum(min(t['pos'][y],t['neg'][y])-min(s['pos'][y],s['neg'][y])
                 for y in s['free'] if y!=x)
    assert acquired>=0 and sx-sxmin>=0
    assert s['e']-t['e']==sx and s['r']-t['r']==sx-sxmin+acquired
    return s['r']==t['r']
def truth(F,a):
    return all(any(a[abs(x)-1]==int(x>0) for x in C) for C in F)
def main():
    out={};alltrans=flat=0
    for name,F in FAMILIES.items():
        assert valid(F) and not valid(F+F[:1])
        n=max(abs(l) for c in F for l in c);m=len(F)
        I=distance_three(F,n)
        checked=0
        for policy in ('zero','one','alternate'):
            p=[-1]*n
            for k,x in enumerate(I,1):
                p[x-1]=(0 if policy=='zero' else 1 if policy=='one' else (k-1)%2)
                s=stats(F,p)
                assert (s['e'],s['eta'],s['r'],len(s['uncovered']))==(
                     2*n//3,0,2*n//3,m-2*k)
                assert len(s['binary'])==2*k and not oddcycle(s['binary'])
                assert all(not (len(c)==1 and j in s['uncovered'])
                           for j,c in enumerate(F,1))
                checked+=1
        choices=product((-1,0,1),repeat=n) if n<=9 else (
             (tuple([-1]*6+list(b)) for b in product((0,1),repeat=9)))
        transitions=0
        for p in choices:
            for x in range(1,n+1):
                if p[x-1]>=0:continue
                for b in (0,1):
                    flat+=int(pivot_law(F,p,x,b));transitions+=1
        alltrans+=transitions
        models=sum(truth(F,a) for a in product((0,1),repeat=n))
        assert models=={'Y6':20,'F9':70,'F15':1032}[name]
        endpoints=[]
        for val in (0,1):
            a=[val]*n
            h=Counter(sum(a[abs(l)-1]==int(l>0) for l in c) for c in F)
            endpoints.append([h[k] for k in range(4)])
        assert endpoints==[[m//2,0,0,m//2]]*2
        out[name]=dict(n=n,m=m,selected=I,plateau_checks=checked,
                       sibling_transition_checks=transitions,models=models,
                       extreme_ends=endpoints)
    print(json.dumps(dict(status='PASS',original_source_scope=True,
         families=out,transition_checks=alltrans,flat_transitions=flat,
         native_FLMV='NOT SIMULATED',P_versus_NP='OPEN'),indent=2,sort_keys=True))
if __name__=='__main__':main()
