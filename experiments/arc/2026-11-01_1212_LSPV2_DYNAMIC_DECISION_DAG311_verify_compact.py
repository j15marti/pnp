#!/usr/bin/env python3
"""No producer import. Independent finite transfer, direct source and update audit."""
from itertools import product
from collections import Counter
P=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
N=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
A={1:1,2:0,3:1,4:0,8:0};B={1:1,2:1,3:0,4:0,8:0}
def mk(t):
    ans=[]
    for i in range(t):
        for j,C in enumerate(P):
            ans.append(tuple(9*((i+1)%t)+5 if j==0 and x==5 else 9*i+x for x in C))
        for C in N:ans.append(tuple(-(9*i+x) for x in C))
    return ans
def relation(pin):
    z=0
    for num in range(512):
        w=tuple((num>>k)&1 for k in range(9))
        if any(w[x-1]!=bit for x,bit in pin.items()):continue
        for b in range(2):
            pos=all(any(b if j==0 and x==5 else w[x-1] for x in C) for j,C in enumerate(P))
            neg=all(any(w[x-1]==0 for x in C) for C in N)
            if pos and neg:z|=1<<(2*w[4]+b)
    return z
def times(a,b):
    out=0
    for i in range(2):
        for k in range(2):
            for j in range(2):
                if (a>>(2*i+j))&1 and (b>>(2*j+k))&1:
                    out|=1<<(2*i+k)
    return out
def direct(F,p):
    var=[i for i in range(1,len(F)*3//4+1) if i not in p]
    count=0
    for v in product((0,1),repeat=len(var)):
        a=dict(p);a.update(zip(var,v))
        if all(any(a[abs(x)]==int(x>0) for x in C) for C in F):count+=1
    return count
p8={1:0,3:0,6:0};p12={5:1};k2={1:0,5:0,6:0}
assert [relation(p) for p in (A,B,p8,p12,k2)]==[3,0,8,12,2]
for p,q,value in ((p8,k2,0),(p12,k2,299),(A,A,1),(B,A,0)):
    f=dict(p);f.update({9+x:y for x,y in q.items()})
    assert direct(mk(2),f)==value
for t in (1,2,4,8,16,32,128):
    F=mk(t)
    c=Counter((abs(x),x>0) for clause in F for x in clause)
    assert len(F)==12*t and all(c[i,True]==2 and c[i,False]==2 for i in range(1,9*t+1))
    pin=[dict(A) for _ in range(t)]
    def decision():
        r=9
        for item in pin:r=times(r,relation(item))
        return bool(r&9)
    assert decision()
    for i in range(t):
        for x,val in ((2,1),(3,0),(2,0),(3,1)):
            pin[i][x]=val
            assert decision()==(x==3 and val==1)
assert not any(x==0 for row in mk(2) for x in row)
print("PASS no-import: G2 299/0, A/B 1/0, full paid-relation recompute on 7 t values")
