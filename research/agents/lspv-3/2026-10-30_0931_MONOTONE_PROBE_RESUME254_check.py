#!/usr/bin/env python3
"""Self-contained resumption theorem checker, not the full benchmark producer."""
import itertools, json, random
from collections import defaultdict, deque

def up(F, pins):
    a=dict(pins)
    while True:
        change=False
        for c in F:
            if any(abs(l) in a and a[abs(l)]==int(l>0) for l in c):continue
            free=[l for l in c if abs(l) not in a]
            if not free:return None
            if len(free)==1:a[abs(free[0])]=int(free[0]>0);change=True
        if not change:return a

class Resume:
    def __init__(self,F,p):
        self.F=F;self.p=p;self.a={};self.q=deque();self.bad=False
        self.oc=defaultdict(list)
        self.pending=deque(i for i,c in enumerate(F) if len(c)<=1)
        for i,c in enumerate(F):
            for l in c:self.oc[abs(l)].append(i)
    def add(self,v,b):
        if v in self.a:
            if self.a[v]!=b:self.bad=True
        else:self.a[v]=b;self.q.append(v)
    def advance(self,delta):
        for v,b in delta:self.add(v,b)
        self.add(abs(self.p),int(self.p>0))
        while (self.q or self.pending) and not self.bad:
            if not self.pending:self.pending.extend(self.oc[self.q.popleft()])
            if not self.pending:continue
            c=self.F[self.pending.popleft()]
            if any(abs(l) in self.a and self.a[abs(l)]==int(l>0) for l in c):continue
            free=[l for l in c if abs(l) not in self.a]
            if not free:self.bad=True;break
            if len(free)==1:self.add(abs(free[0]),int(free[0]>0))
        return None if self.bad else dict(self.a)

W=[(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),(5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),(-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),(2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)]
S=list(W);S[9]=(-5,6,-15);S[13]=(-3,-6,-15)

def main():
    rng=random.Random(254254);checks=0
    for _ in range(600):
        n=rng.randrange(3,8);F=[]
        for j in range(rng.randrange(1,20)):
            variables=rng.sample(range(1,n+1),rng.choice([2,3]))
            F.append(tuple(v*rng.choice([-1,1]) for v in variables))
        p=rng.randrange(1,n+1)*rng.choice([-1,1]);r=Resume(F,p);base={}
        order=list(range(1,n+1));rng.shuffle(order)
        for v in [None]+order:
            delta=[] if v is None else [(v,rng.randrange(2))]
            base.update(delta);answer=r.advance(delta)
            expected=None if abs(p) in base and base[abs(p)]!=int(p>0) else up(F,base|{abs(p):int(p>0)})
            assert answer==expected;checks+=1
            if expected is None:break
    old=up(S,{2:0,8:0,5:0});new=up(S,{2:0,8:0,10:0,5:0})
    assert old=={2:0,8:0,5:0,14:0} and new is None
    assert all(old.get(v,b)==b for v,b in {2:0,8:0,10:0}.items())
    r=Resume(S,-5);assert r.advance([(2,0),(8,0)])==old
    assert r.advance([(10,0)]) is None
    models=[mask for mask in range(1<<15) if all(any(((mask>>(abs(l)-1))&1)==int(l>0) for l in c) for c in S)]
    assert len(models)==54 and all((mask>>1)&1 for mask in models)
    F=[(-1,2),(-2,3,4),(-2,-3,4)]
    assert up(F,{1:1})=={1:1,2:1} and up(F,{1:1,4:0}) is None
    F=[(-1,-2,3)]
    assert up(F,{1:1,2:1})[3]==1 and up(F,{1:0,2:1,3:0}) is not None
    print(json.dumps({'random_formulas':600,'monotone_resume_checks':checks,'SWAP6_models':len(models),'stale_nonconflict_falsified':True,'backtrack_reuse_falsified':True},sort_keys=True,indent=2))
if __name__=='__main__':main()
