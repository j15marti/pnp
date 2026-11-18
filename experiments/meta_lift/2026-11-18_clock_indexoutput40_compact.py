#!/usr/bin/env python3
"""Standalone CLOCKINDEXOUTPUT40 exhaustive semantic control, Python 3, stdlib only."""
from itertools import product
import random, json
rng=random.Random(20261118094041)
counts={'models':0,'sources':0,'targets':0,'relation_checks':0,'witnesses':0,'failures':0}

def run(x,t):
    p=0; out=''
    for i,b in enumerate(x):
        p,w=t[i,p,b];out+=w
    return out,p

def relation(n,k,t,y):
    R={}; B={}
    for i in range(1<<n):
        for p in range(k):
            for b in range(2):
                q,w=t[i,p,b]
                for a in range(len(y)+1):
                    z=a+len(w)
                    if z<=len(y) and y[a:z]==w:
                        R[n,i,p,q,a,z]=1
                        B[n,i,p,q,a,z,b]=1
    for d in range(n-1,-1,-1):
        for i in range(1<<d):
            for p,q in product(range(k),repeat=2):
                for a in range(len(y)+1):
                    for z in range(a,len(y)+1):
                        if any(R.get((d+1,2*i,p,s,a,h)) and R.get((d+1,2*i+1,s,q,h,z))
                               for s in range(k) for h in range(a,z+1)):
                            R[d,i,p,q,a,z]=1
    return R,B

def extract(n,k,t,y,q,R,B):
    g=[-1]*(1<<n)
    def go(d,i,p,q,a,z):
        if d==n:
            g[i]=next(b for b in range(2) if B.get((d,i,p,q,a,z,b)))
            return
        s,h=next((s,h) for s in range(k) for h in range(a,z+1)
                 if R.get((d+1,2*i,p,s,a,h)) and R.get((d+1,2*i+1,s,q,h,z)))
        go(d+1,2*i,p,s,a,h);go(d+1,2*i+1,s,q,h,z)
    go(0,0,0,q,0,len(y))
    return tuple(g)

for n in (2,3):
    for v in range(8):
        k=2; t={}
        for i,p,b in product(range(1<<n),range(k),range(2)):
            t[i,p,b]=(rng.randrange(k),rng.choice(('','0','1','00')))
        fibers={}
        for x in product(range(2),repeat=1<<n):
            fibers.setdefault(run(x,t),[]).append(x); counts['sources']+=1
        for (y,q),xs in fibers.items():
            if len(y)>4: continue
            R,B=relation(n,k,t,y)
            if not R.get((0,0,0,q,0,len(y))):raise AssertionError('root')
            g=extract(n,k,t,y,q,R,B)
            assert g in xs and run(g,t)==(y,q)
            counts['witnesses']+=1
            # Independent exhaustive interval oracle for every relation cell.
            for d in range(n+1):
                size=1<<(n-d)
                for a in range(1<<d):
                    for p,r in product(range(k),repeat=2):
                        for lo in range(len(y)+1):
                            for hi in range(lo,len(y)+1):
                                expected=False
                                for w in product(range(2),repeat=size):
                                    state=p;word=''
                                    for j,bit in enumerate(w):
                                        state,em=t[a*size+j,state,bit];word+=em
                                    if state==r and word==y[lo:hi]:
                                        expected=True;break
                                assert bool(R.get((d,a,p,r,lo,hi)))==expected
                                counts['relation_checks']+=1
            counts['targets']+=1
        counts['models']+=1
print(json.dumps(counts,sort_keys=True))
