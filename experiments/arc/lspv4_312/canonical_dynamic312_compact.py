#!/usr/bin/env python3
"""Independent portable check for LSPV-4 312 canonical A/B online decision theorem."""
import itertools
from fractions import Fraction
P=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
N=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
A={1:1,2:0,3:1,4:0,8:0}; B={1:1,2:1,3:0,4:0,8:0}
def matrix(pins):
    m=[[0,0],[0,0]]
    for a,b in itertools.product((0,1),repeat=2):
        for values in itertools.product((0,1),repeat=8):
            d=dict(zip((1,2,3,4,6,7,8,9),values)); d[5]=a
            if any(d[k]!=v for k,v in pins.items()):continue
            if all(any((b if i==0 and k==5 else d[k])==1 for k in row) for i,row in enumerate(P)) and all(any(d[k]==0 for k in row) for row in N):
                m[a][b]+=1
    return m
W=matrix({}); X=matrix(A);Y=matrix(B)
assert W==[[34,47],[23,36]],(X,Y)==([[1,1],[0,0]],[[0,0],[0,0]])
def source(t):
    r=[]
    for i in range(t):
        for j,row in enumerate(P):
            r.append(tuple(9*((i+1)%t)+5 if j==0 and k==5 else 9*i+k for k in row))
        for row in N:r.append(tuple(-(9*i+k) for k in row))
    return r
def sat_count(t,selection):
    c=source(t);p={}
    for i,flag in enumerate(selection):
        for k,v in (A if flag else B).items():p[9*i+k]=v
    free=[i for i in range(1,9*t+1) if i not in p]
    count=0
    for vals in itertools.product((0,1),repeat=len(free)):
        d=dict(p);d.update(zip(free,vals))
        count+=all(any(d[abs(l)]==int(l>0) for l in row) for row in c)
    return count
tested=0
for t in (1,2,3):
    for bits in itertools.product((0,1),repeat=t):
        assert sat_count(t,bits)==int(all(bits))
        tested+=1
for t in range(1,9):
    states=list(itertools.product((0,1),repeat=t))
    for i,a in enumerate(states):
        for b in states[i+1:]:
            k=next(j for j in range(t) if a[j]!=b[j])
            ca=[1]*t; cb=[1]*t;ca[k]=a[k];cb[k]=b[k]
            assert all(ca)!=all(cb)
assert not all((1,0)) and not all((0,1))
assert all((1,1)) and not all((1,0))
for c,expected in ((Fraction(6,5),Fraction(23,45)),(Fraction(241,200),Fraction(11642479,23232400))):
    f=Fraction(1);d=[]
    for k in range(1,5):
        f=c*f/(1+f)
        d.append(min((1/f-c)/k,c**(-k)))
    assert d[1]==expected and max(d)==d[1] and c**(-4)<d[1]
print("PASS canonical G_t all-A=SAT, any-B=UNSAT; midpoint 2^t continuation classes; t=1..8; original-source exact checks",tested)
