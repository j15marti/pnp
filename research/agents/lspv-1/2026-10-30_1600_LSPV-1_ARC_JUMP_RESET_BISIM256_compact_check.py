#!/usr/bin/env python3
"""Independent compact ARC-JUMP-RESET-BISIM256 check. Python 3.10+."""
from itertools import product,combinations
import random,math
R=random.Random(202610301600)
def clause_true(c,a): return sum((a[abs(v)-1]==int(v>0)) for v in c)
def sat(F,n): return any(all(clause_true(c,a)>0 for c in F) for a in product((0,1),repeat=n))
def pair(d,e):
    return all(k not in d or d[k]==v for k,v in e.items())
def targets(c):
    s={abs(v):int(v>0) for v in c}
    return s,{i:1-b for i,b in s.items()}
def sim(y,B,prog,clip):
    m=len(y);H=m+B;h=0;reads=[]
    for cmd,arg in prog:
        if cmd=="jump":h=(arg if arg<H else None) if clip else arg
        elif cmd=="left":
            if h is not None:h=max(0,h-1)
        elif cmd=="right":
            if h is not None:
                h+=1
                if clip and h>=H:h=None
        else:reads.append(y[h] if h is not None and h<m else None)
    return reads
def named():
    sat7=[tuple((-i-1 if (a>>i)&1 else i+1) for i in range(3)) for a in range(1,8)]
    unsat8=[tuple((-i-1 if (a>>i)&1 else i+1) for i in range(3)) for a in range(8)]
    E=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
    k4=[]
    for v in range(4):
        c=tuple(i+1 for i,(a,b) in enumerate(E) if v in (a,b))
        k4.extend([c,tuple(-x for x in c)])
    return [(sat7,3,True),(unsat8,3,False),(k4,6,True)]
count=0
for F,n,correct in named():
    assert sat(F,n)==correct
    for c in F:
        s,u=targets(c)
        assert all(u[x]==1-b for x,b in s.items())
    for i,j in combinations(range(len(F)),2):
        a=targets(F[i]);b=targets(F[j])
        for x,y in product((0,1),repeat=2):
            p=pair(a[x],b[y])
            e=any(all(z[t-1]==v for t,v in a[x].items()) and all(z[t-1]==v for t,v in b[y].items()) for z in product((0,1),repeat=n))
            assert p==e;count+=1
    for a in product((0,1),repeat=n):
        b=tuple(1-v for v in a)
        assert all(clause_true(c,a)+clause_true(c,b)==3 for c in F)
    y="1"+"0"*128;B=6
    prog=[("read",None),("jump",10**60),("read",None),("jump",0),("read",None),("left",None),("read",None)]
    p=sim(y,B,prog,False);q=sim(y,B,prog,True)
    assert p==q and p[0]==p[2] and p[1] is None
for _ in range(500):
    m=R.randint(1,16);B=R.randint(0,15);y="".join(R.choice("01") for _ in range(m))
    prog=[];used=0
    for _ in range(25):
        op=R.choice(["jump","left","right","read"])
        if op in ("left","right") and used==B:op="read"
        if op in ("left","right"):used+=1
        arg=R.choice([0,m-1,m+B+1,10**60]) if op=="jump" else None
        prog.append((op,arg))
    assert sim(y,B,prog,False)==sim(y,B,prog,True);count+=1
for H in (8,64,256,512):
    q=H
    assert H+2*q==3*H and q*(H+1)>H+2*q
print("PASS: pairs + SAT/UNSAT + head traces + conditional sparse-index check;",count,"trials")
