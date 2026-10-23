#!/usr/bin/env python3
"""CUTFLOW85 compact verifier. Python3 standard library only.
Checks proper-3CNF equality, charged two-way head trajectory, SAT/UNSAT
switching, and interleaved-layout bypass. Finite checks do not prove bounds.
"""
import itertools

def E(u,v,interleaved=False):
    k=len(u); groups=[]
    for h,z in enumerate((u,v)):
        hh=[]
        for i,bit in enumerate(z):
            x=5*i+1;a=x+1+2*h;b=x+2+2*h
            hh.append([(x if bit else -x,sa*a,sb*b)
                       for sa in (1,-1) for sb in (1,-1)])
        groups.append(hh)
    if interleaved:
        return [c for i in range(k) for h in (0,1) for c in groups[h][i]]
    return [c for h in (0,1) for q in groups[h] for c in q]

def sat(F,n):
    return any(all(any(((mask>>(abs(z)-1))&1)==(z>0) for z in c) for c in F)
               for mask in range(1<<n))

def site(k,h,i,interleaved=False):
    return 3+16*((2*i+h) if interleaved else (h*k+i))

def words(F,n):
    return [n,len(F)]+[y for c in F for y in (3,*c)]

def walk(F,n,B,hybrid=False,interleaved=False):
    k=n//5;tape=words(F,n);pos=0;moves=0;reads=0;peak=0;sw=0
    def rd(q):
        nonlocal pos,moves,reads
        moves+=abs(q-pos);pos=q;reads+=1
        return tape[q]
    if rd(0)!=n or rd(1)!=8*k:raise ValueError('header')
    for j in range(2*k):
        i=j//2 if interleaved else j%k
        h=j%2 if interleaved else j//k
        x=5*i+1;a=x+1+2*h;b=x+2+2*h;last=None
        for r in range(4):
            base=2+16*j+4*r
            width,lit,p,q=[rd(base+t) for t in range(4)]
            if (width!=3 or abs(lit)!=x or p!=(a if r<2 else -a)
                or q!=(b if r%2==0 else -b) or (last is not None and lit!=last)):
                raise ValueError('bad quartet')
            last=lit
    lo=0
    while lo<k:
        width=1 if hybrid and lo==0 else B
        hi=min(k,lo+width)
        saved=[rd(site(k,0,i,interleaved))>0 for i in range(lo,hi)]
        peak=max(peak,len(saved))
        for offset,i in enumerate(range(lo,hi)):
            if saved[offset]!=(rd(site(k,1,i,interleaved))>0):
                return ('UNSAT',moves+reads,peak,sw)
        lo=hi
        if hybrid and lo==1 and lo<k:sw+=1
    return ('SAT',moves+reads,peak,sw)

def check():
    count=0
    for k in (1,2):
        for u in itertools.product((0,1),repeat=k):
            for v in itertools.product((0,1),repeat=k):
                F=E(u,v)
                assert sat(F,5*k)==(u==v)
                assert len(F)==8*k and len(set(F))==8*k
                assert walk(F,5*k,1)[0]==('SAT' if u==v else 'UNSAT')
                assert walk(E(u,v,True),5*k,1,interleaved=True)[0]==('SAT' if u==v else 'UNSAT')
                count+=1
    for k in (8,16,32,64):
        u=tuple(i%2 for i in range(k))
        for flip in (-1,0,k-1):
            v=list(u)
            if flip>=0:v[flip]^=1
            F=E(u,v);expected='SAT' if flip<0 else 'UNSAT'
            for B in (1,8,k):
                for adaptive in (False,True):
                    assert walk(F,5*k,B,adaptive)[0]==expected
                    count+=1
        assert sum(j+(k-j) for j in range(1,k))==k*(k-1)
        count+=1
    print('CUTFLOW85 compact assertions passed:',count)
    k=64;u=tuple(i%2 for i in range(k));F=E(u,u)
    for B in (1,8,64):print('SAT grouped',k,B,walk(F,5*k,B))
    print('SAT interleaved',walk(E(u,u,True),5*k,1,interleaved=True))
if __name__=='__main__':check()
