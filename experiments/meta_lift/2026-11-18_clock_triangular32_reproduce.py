#!/usr/bin/env python3
"""Independent compact verifier for CLOCKTRIANGULAR32; finite controls only."""
import itertools,json

def T(f):
    a=1;z=[]
    for i,b in enumerate(f):
        z.append(b if not i else b^a)
        a&=b
    return tuple(z)

def inv(z):
    a=1;f=[]
    for i,b in enumerate(z):
        x=b if not i else b^a
        f.append(x);a&=x
    return tuple(f)

def H(f):
    z=T(f)
    return tuple(z[(1<<r)-1] for r in range(len(f).bit_length()))

checks=0
summary={}
for n in range(1,5):
    N=1<<n
    hist={}
    for f in itertools.product((0,1),repeat=N):
        y=H(f)
        assert inv(T(f))==f
        assert H(inv(T(f)))==y
        checks+=2
        hist[y]=hist.get(y,0)+1
    assert len(hist)==1<<(n+1)
    checks+=1
    for y in itertools.product((0,1),repeat=n+1):
        z=[0]*N
        for r,b in enumerate(y):z[(1<<r)-1]=b
        g=inv(z)
        assert H(g)==y
        assert hist[y]==1<<(N-(n+1))
        checks+=2
    summary[n]={"fiber_count":len(hist),"fiber_size":1<<(N-n-1)}
print(json.dumps({"report":"CLOCKTRIANGULAR32", "source_tests":65812,"checks":checks,
                  "failures":0,"by_n":summary,"scope":"finite source/fiber inversion only"},sort_keys=True))
