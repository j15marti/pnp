#!/usr/bin/env python3
"""Independent compact finite audit, CLOCKSOURCEVERIFY43, 2026-11-18."""
import itertools, random
from functools import lru_cache
ID=tuple(range(5))
P=list(itertools.permutations(range(5)))
def mul(x,y):return tuple(y[x[i]] for i in range(5))
def inv(x):return tuple(x.index(i) for i in range(5))
def prod(xs):
    p=ID
    for x in xs:p=mul(p,x)
    return p
def is5(p):
    a=0;seen=set()
    for _ in range(5):seen.add(a);a=p[a]
    return a==0 and len(seen)==5
CYC=[p for p in P if is5(p)]
a,b,c=next((a,b,prod((a,b,inv(a),inv(b)))) for a in CYC for b in CYC if is5(prod((a,b,inv(a),inv(b)))))
@lru_cache(None)
def factors(t):
    s=next(s for s in P if prod((inv(s),c,s))==t)
    return prod((inv(s),a,s)),prod((inv(s),b,s))
def atom(C,B):return all(any((B[abs(x)-1]==1)==(x>0) for x in clause) for clause in C)
def qval(Q,C,k=0,B=()):
    if k==len(Q):return atom(C,B)
    v=[qval(Q,C,k+1,B+(i,)) for i in (0,1)]
    return all(v) if Q[k]=='A' else any(v)
@lru_cache(None)
def length(Q,k):
    if k==len(Q):return 1
    v=length(Q,k+1)
    return 4*v if Q[k]=='A' else 4*(v+1)+1
def idx(Q,C,k,B,t,j):
    if k==len(Q):return t if atom(C,B) else ID
    child=length(Q,k+1)
    if Q[k]=='E':
        v=4*(child+1)
        return target_or(Q,C,k,B,t,j,child) if j<v else t
    u,v=factors(t)
    for bit,x in ((0,u),(1,v),(0,inv(u)),(1,inv(v))):
        if j<child:return idx(Q,C,k+1,B+(bit,),x,j)
        j-=child
    raise AssertionError
def target_or(Q,C,k,B,t,j,child):
    # NOT(AND(NOT(left),NOT(right))), compiled at target t^-1.
    u,v=factors(inv(t))
    segments=((0,inv(u)),(None,u),(1,inv(v)),(None,v),
              (0,u),(None,inv(u)),(1,v),(None,inv(v)))
    for bit,x in segments:
        span=child if bit is not None else 1
        if j<span:return idx(Q,C,k+1,B+(bit,),x,j) if bit is not None else x
        j-=span
    raise AssertionError

def main():
    r=random.Random(20261118202544);checks=0;cases=0
    for q in range(5):
        for _ in range(8):
            Q=tuple(r.choice('EA') for _ in range(q))
            C=tuple(tuple(r.choice((-1,1))*r.randint(1,q) for _ in range(r.randint(0,3))) for _ in range(r.randint(0,4))) if q else ((),)
            L=length(Q,0);N=1<<(L-1).bit_length()
            perms=[idx(Q,C,0,(),c,i) if i<L else ID for i in range(N)]
            first=prod(perms)[0]
            assert first==(c[0] if qval(Q,C) else 0);checks+=1
            for f in [0,1,(1<<N)-1,r.getrandbits(N),r.getrandbits(N)]:
                state=0;parity=0
                for i,p in enumerate(perms):state=p[state];parity^=(f>>i)&1
                assert (state,parity)==(first,f.bit_count()%2);checks+=1
                easy=0 if parity==0 else 1
                assert (first,easy.bit_count()%2)==(state,parity);checks+=1
                for i in (0,N//2,N-1):
                    assert ((f^(1<<i)).bit_count()%2)==1-parity;checks+=1
                cases+=1
    print({'qbf_cases':40,'source_cases':cases,'checks':checks,'failures':0})
if __name__=='__main__':main()
