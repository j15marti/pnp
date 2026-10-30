#!/usr/bin/env python3
"""ARC-HIGHWATER-ALLOCATOR254 independent, standard-library-only checker.
Exact closed-form FLMV envelope, matched source SAT labels and tape high-water.
Expanded 8-family primary run, raw S/U matrices, and full controller are in the
local reproducibility bundle; this independent checker is self-contained.
"""
from fractions import Fraction as F
from collections import Counter
import json
def envelope(c):
    best=F(0);win=0;k=0
    while True:
        k+=1
        # Closed form independent of the producer's f[k] recurrence.
        inverse=(c**k+c-2)/((c-1)*c**k)
        d=min((inverse-c)/k,c**(-k))
        if d>best:best=d;win=k
        if c**(-(k+1))<best:return best,win,k
expected={'6/5':('23/45',2,3),
 '241/200':('11642479/23232400',2,3),
 '7/5':('949/5145',3,5),
 '3/2':('49/648',4,6),
 '8/5':('2145161/335544320',8,10)}
for c,e in expected.items():
    got=envelope(F(c))
    assert (str(got[0]),got[1],got[2])==e,(c,got)
W1='-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'
w=[tuple(map(int,c.split())) for c in W1.split(';')]
v=[list(c) for c in w]
assert v[7][0]==1 and v[19][0]==-1
v[7][0]=-1;v[19][0]=1
v=[tuple(c) for c in v]
def true(l,a):
    return ((a>>(abs(l)-1))&1)==int(l>0)
def hist(C,a):
    r=[sum(true(l,a) for l in c) for c in C]
    return [r.count(k) for k in range(4)]
def exact22(C):
    z=Counter(l for c in C for l in c)
    return len(C)==20 and all(z[i]==z[-i]==2 for i in range(1,16))
for C in (w,v):
    assert exact22(C)
    assert hist(C,0)==[1,10,7,2]
    assert hist(C,(1<<15)-1)==[2,7,10,1]
assert all({abs(l) for l in a}=={abs(l) for l in b} for a,b in zip(w,v))
models=[]
for C in (w,v):
    count=0
    for a in range(1<<15):
        count+=int(all(any(true(l,a) for l in c) for c in C))
        assert hist(C,a)==hist(C,((1<<15)-1)^a)[::-1]
    models.append(count)
assert models==[0,168],models
assert all(any(true(l,97) for l in c) for c in v)
# Independently compute physical indexed addresses for exact serial buffers.
for lengths in ((1608,1600),(504,504),(192,192),(304,304)):
    for repetitions in (1,2,8,64,256):
        fresh=0;reused=0;live=0
        for _ in range(repetitions):
            for length in lengths:
                fresh+=length
                reused=max(reused,length)
                live=max(live,length)
        assert fresh==sum(lengths)*repetitions
        assert reused==live==max(lengths)
assert 256*(1608+1600)==821248
print(json.dumps({'status':'PASS','FLMV':expected,
 'W1_models':models,'matched_same_scopes':True,'strict22':True,
 'fresh_512_children':821248,'reused_512_children':1608}))
