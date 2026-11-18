"""Compact, independently executed semantic reproducer for CLOCKREACHCIRCUIT33.
Not the full local audit; no asymptotic circuit lower bounds are tested.
"""
from itertools import product
import json

def reach(T):
    N=len(T); K=len(T[0]); R={}
    for i in range(N):
        R[(i,1)] = [set(T[i][p]) for p in range(K)]
    h=2
    while h<=N:
        for i in range(0,N,h):
            a,b=R[(i,h//2)],R[(i+h//2,h//2)]
            R[(i,h)]=[{q for mid in a[p] for q in b[mid]} for p in range(K)]
        h*=2
    return R

def recover(T,R,p,q):
    N=len(T); out=[None]*N; K=len(T[0])
    def go(i,h,p,q):
        if h==1:
            out[i]=0 if T[i][p][0]==q else 1
        else:
            a,b=R[(i,h//2)],R[(i+h//2,h//2)]
            mid=next(r for r in range(K) if r in a[p] and q in b[r])
            go(i,h//2,p,mid);go(i+h//2,h//2,mid,q)
    go(0,N,p,q)
    return tuple(out)

def final(T,x):
    p=0
    for i,b in enumerate(x):p=T[i][p][b]
    return p

checks=0
for bits in product((0,1),repeat=4):
    T=[((bits[0],bits[1]),(bits[2],bits[3]))]*8
    R=reach(T)
    for x in product((0,1),repeat=8):
        q=final(T,x)
        z=recover(T,R,0,q)
        assert final(T,z)==q
        checks+=1
for pattern in product((0,1),repeat=8):
    T=[((0,1) if b==0 else (1,0),(1,1)) for b in pattern]
    R=reach(T)
    assert recover(T,R,0,0)==pattern
    for mat in R.values():
        assert mat[0]=={0,1} and mat[1]=={1}
    checks+=1
print(json.dumps({'checks':checks,'failures':0,'model':'terminal-state dyadic reachability','claim':'finite semantic check only'},sort_keys=True))
