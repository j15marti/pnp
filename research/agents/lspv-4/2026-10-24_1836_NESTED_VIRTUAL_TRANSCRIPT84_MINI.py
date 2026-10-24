#!/usr/bin/env python3
"""Independent reproducible NESTED-VIRTUAL-TRANSCRIPT84 control.
Standard library only. Exhaustive 64 assignments, 2-level exact bit service.
"""
import math

def clause(r): return tuple(-i if r>>(i-1)&1 else i for i in (1,2,3))
FILL=(4,5,6)
def source(d, sat):
    return [clause(0 if sat and j==7 else j) if i%d==0 else FILL
            for i in range(8*d) for j in ([i//d] if i%d==0 else [0])]
def count(F):
    return sum(all(any((bool(a>>(abs(l)-1)&1))==(l>0) for l in C) for C in F)
               for a in range(64))
def w(n,m): return (64*(n+m+1)-1).bit_length()
def bit(F,k1,k2,j1,j2,p):
    width=w(6,k2); word,offset=divmod(p,width)
    if word==0: v=6
    elif word==1: v=k2
    else:
        i,t=divmod(word-2,4)
        C=F[(j1*k1+(j2*k2+i)%k1)%len(F)]
        v=3 if t==0 else 2*abs(C[t-1])+(C[t-1]<0)
    return (v>>(width-1-offset))&1
def leaf(F,k1,k2,j1,j2):
    return tuple(F[(j1*k1+(j2*k2+i)%k1)%len(F)] for i in range(k2))
def eager_bits(C):
    v=[6,len(C)]
    for c in C:v.extend([3]+[2*abs(l)+(l<0) for l in c])
    ww=w(6,len(C))
    return ''.join(format(x,'0%db'%ww) for x in v)
def test(d):
    M=8*d;k1=int(math.sqrt(d))|1;k2=max(2,int(math.sqrt(k1)))
    assert 1<k2<k1<d and math.gcd(M,k1)==1
    U,V=source(d,False),source(d,True)
    assert (count(U),count(V))==(0,7)
    distinct=[set(),set()]
    observations=[[],[]]
    for j1 in range(M):
        for j2 in range(k1):
            Cs=[leaf(F,k1,k2,j1,j2) for F in (U,V)]
            cnt=[count(C) for C in Cs]
            assert cnt[0]==cnt[1] and cnt[0] in (49,56)
            for z,(F,C) in enumerate(zip((U,V),Cs)):
                distinct[z].add(C)
                if j2==0:observations[z].append(cnt[z])
                B=eager_bits(C)
                for p in (0,len(B)//2,len(B)-1):
                    assert bit(F,k1,k2,j1,j2,p)==int(B[p])
    assert observations[0]==observations[1]
    assert len(distinct[0])==1+8*k2 and len(distinct[1])==1+7*k2
    print('d=%d M=%d k1=%d k2=%d leaves=%d distinct=%s parent=(UNSAT,SAT) all child counts paired'
          %(d,M,k1,k2,M*k1,(len(distinct[0]),len(distinct[1]))))
for d in (16,32,64,128):test(d)
