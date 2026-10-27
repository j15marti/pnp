#!/usr/bin/env python3
"""LSPV-4 ANISOTROPIC161: exact unit-head sequential comparator audit.
The simulated finite controller does not read R,C. R,C are host test sizes,
and 'cut', trace buffers, and counters are external measurement only.
"""
import json
from dataclasses import dataclass
CHECKS=0
def ck(x,m="failed"):
    global CHECKS
    CHECKS+=1
    if not x: raise AssertionError(m)
def src(R,C,a,b):
    def rows(v): return '|'.join(''.join(str(int(v[i*C+j])) for j in range(C)) for i in range(R))
    return '^'+rows(a)+'#'+'X'*(8*R*C)+'#'+rows(b)+'$'
@dataclass
class M:
    z:str; R:int; C:int
    ipos:int=1; row:int=0; col:int=0
    T:int=0; H:int=0; rev:int=0; prev:int=0
    row_max:int=0; col_max:int=0; D:int=0; crosses:int=0
    cache_a:int=0; cache_b:int=0; phase:str="init"
    def __post_init__(self):
        self.cut=self.z.index('#')+4*self.R*self.C
        self.history=[]
    def move_input(self,d):
        old=self.ipos
        self.ipos+=d; ck(0<=self.ipos<len(self.z),"source end")
        self.T+=1;self.H+=1
        if self.prev and self.prev!=d: self.rev+=1
        self.prev=d
        if (old<=self.cut<self.ipos) or (self.ipos<=self.cut<old):
            self.crosses+=1
            self.history.append((d,self.phase,self.cache_a,self.cache_b,self.row,self.col))
    def move_work(self,t,d):
        p=(self.row if t==0 else self.col)+d
        ck(p>=0,"work left end")
        if t==0: self.row=p; self.row_max=max(self.row_max,p)
        else: self.col=p; self.col_max=max(self.col_max,p)
        self.T+=1
    def fetch(self,shore):
        ck((self.z[self.ipos-1]=='^') if shore=='a' else (self.z[self.ipos-1]=='#'))
        base=self.ipos; sr=self.row; sc=self.col
        while self.row:
            while self.z[self.ipos] in '01': self.move_input(1)
            if self.z[self.ipos]!='|':
                while self.ipos>base and self.z[self.ipos-1] in '01':self.move_input(-1)
                while self.ipos>base:
                    ck(self.z[self.ipos-1]=='|')
                    self.move_input(-1);self.move_work(0,1)
                    while self.ipos>base and self.z[self.ipos-1] in '01':self.move_input(-1)
                ck((self.row,self.col)==(sr,sc))
                return 'row_oob'
            self.move_input(1);self.move_work(0,-1)
        while self.col and self.z[self.ipos] in '01':
            self.move_input(1);self.move_work(1,-1)
        val=int(self.z[self.ipos]) if self.col==0 and self.z[self.ipos] in '01' else 'col_oob'
        while self.ipos>base and self.z[self.ipos-1] in '01':
            self.move_input(-1);self.move_work(1,1)
        while self.ipos>base:
            ck(self.z[self.ipos-1]=='|')
            self.move_input(-1);self.move_work(0,1)
            while self.ipos>base and self.z[self.ipos-1] in '01':self.move_input(-1)
        ck((self.row,self.col)==(sr,sc) and self.ipos==base)
        return val
    def to_bob(self):
        self.phase='bob_nav'; seen=0
        while seen<2:
            if self.z[self.ipos]=='#':seen+=1
            self.move_input(1)
        ck(self.z[self.ipos-1]=='#')
    def to_alice(self):
        self.phase='alice_nav'
        while self.z[self.ipos]!='^':self.move_input(-1)
        self.move_input(1)
    def decide(self):
        comparisons=0
        while True:
            self.phase='fetch_a'; a=self.fetch('a')
            if a=='col_oob':
                self.phase='carry'
                while self.col:self.move_work(1,-1)
                self.move_work(0,1)
                continue
            if a=='row_oob':return True,comparisons
            self.cache_a=a;self.to_bob()
            self.phase='fetch_b';b=self.fetch('b')
            ck(b in (0,1),"Bob parser")
            self.cache_b=b;comparisons+=1
            if a and b:return False,comparisons
            self.to_alice()
            self.phase='advance';self.move_work(1,1)
            ck(comparisons<=self.R*self.C,"audit only")
def bits(t,m):return tuple((t>>i)&1 for i in range(m))
def run(R,C,a,b):
    o=M(src(R,C,a,b),R,C)
    ans,q=o.decide()
    ck(ans==all(not(x and y) for x,y in zip(a,b)))
    ck(o.D==0 and o.row_max<=R and o.col_max<=C)
    ck(o.H<=o.T and o.crosses<=2*q)
    if ans:
        ck(q==R*C and o.crosses==2*R*C)
        ck((o.row_max,o.col_max)==(R,C))
        ck(o.T<40*R*C*len(o.z)+1000)
    return o,ans,q
exhaustive=0
for R,C in [(1,1),(1,2),(2,1),(2,2),(2,3),(3,2)]:
    m=R*C
    for i in range(1<<m):
        for j in range(1<<m):
            run(R,C,bits(i,m),bits(j,m));exhaustive+=1
diagonals=0; collisions=0
for R,C in [(1,1),(2,2),(2,3),(3,2),(3,3),(1,8),(8,1)]:
    m=R*C;full=set();partial=set()
    for i in range(1<<m):
        a=bits(i,m);b=tuple(1-x for x in a)
        x,ans,q=run(R,C,a,b)
        hist=tuple(x.history)
        ck(hist not in full)
        full.add(hist)
        reduced=tuple((d,phase,r,c) for d,phase,ca,cb,r,c in hist)
        if reduced in partial:collisions+=1
        else:partial.add(reduced)
        diagonals+=1
    ck(len(full)==(1<<m))
ck(collisions>0,"omitting cached bits must create false collision")
controls=[]
for R,C in [(1,64),(64,1),(2,128),(128,2),(4,64),(64,4),(8,64),(64,8),(16,32),(32,16)]:
    m=R*C;a=tuple((i*7+3)%5<2 for i in range(m))
    o,ans,q=run(R,C,a,tuple(1-x for x in a))
    controls.append(dict(R=R,C=C,N=len(o.z),S1=o.row_max+1,S2=o.col_max+1,T=o.T,H=o.H,Rev=o.rev,D=o.D,Cross=o.crosses))
    ck(o.crosses==2*m and o.D==0)
for B in [2,3,4,5]:
    for p,q in [(1,1),(1,2),(2,1),(1,3),(3,1)]:
        R,C=B**p,B**q
        if R*C>512:continue
        m=R*C
        o,ans,_=run(R,C,(0,)*m,(1,)*m)
        ck(o.crosses==2*m)
result=dict(run='ANISOTROPIC-WRITE-CROSS161',checks=CHECKS,failures=0,exhaustive_pairs=exhaustive,diagonal_histories=diagonals,cache_omission_collisions=collisions,controls=controls)
print(json.dumps(result,sort_keys=True,indent=2))
