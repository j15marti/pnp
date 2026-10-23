#!/usr/bin/env python3
"""Minimal PASSMEM84 equality->proper-3CNF and multipass control audit.
Pure Python 3 stdlib, deterministic. Full audit and raw results in user-delivered package.
"""
import itertools, math

def block(s,x,a,b):
    return [(x if s else -x, ea*a, eb*b)
            for ea in (1,-1) for eb in (1,-1)]

def encode(u,v):
    k=len(u);out=[]
    for i in range(k):
        x=5*i+1
        out+=block(u[i],x,x+1,x+2)
    for i in range(k):
        x=5*i+1
        out+=block(v[i],x,x+3,x+4)
    return out

def sat_count(F,n):
    return sum(all(any((a[abs(l)-1]==(l>0)) for l in C) for C in F)
               for a in itertools.product((False,True),repeat=n))

def run_stream(F,B):
    """No u or v prescan; all source clauses are checked sequentially each pass."""
    if len(F)%8 or not F:return ('UNSUPPORTED',1,0)
    k=len(F)//8;B=max(1,B);lo=0;passes=0
    while lo<k:
        hi=min(k,lo+B);buffer=[0]*(hi-lo)
        current=None;bad=False;mismatch=False
        for pos,C in enumerate(F):
            half=pos//(4*k);i=(pos%(4*k))//4;j=pos%4
            x=5*i+1
            a,b=(x+1,x+2) if half==0 else (x+3,x+4)
            expected=(a if j<2 else -a,b if j%2==0 else -b)
            if len(C)!=3 or abs(C[0])!=x or C[1:]!=expected:
                bad=True;continue
            if j==0:
                current=C[0]>0
                if lo<=i<hi:
                    if half==0:buffer[i-lo]=current
                    elif buffer[i-lo]!=current:mismatch=True
            elif current!=(C[0]>0):bad=True
        passes+=1
        if bad:return ('UNSUPPORTED',passes,len(buffer))
        if mismatch:return ('UNSAT',passes,len(buffer))
        lo=hi
    return ('SAT',passes,min(B,k))

def check():
    tests=0
    for k in (1,2):
        for u in itertools.product((0,1),repeat=k):
            for v in itertools.product((0,1),repeat=k):
                F=encode(u,v)
                assert len(F)==8*k
                assert len(set(F))==len(F)
                assert all(len(set(map(abs,C)))==3 for C in F)
                assert sat_count(F,5*k)==(2**(4*k) if u==v else 0)
                for B in (1,k):
                    lab,p,mem=run_stream(F,B)
                    assert lab==('SAT' if u==v else 'UNSAT')
                    assert p<=math.ceil(k/B) and mem<=B
                tests+=1
    k=32;u=tuple(i%2 for i in range(k))
    for B in (1,4,32):
        for case in ('SAT','UNSAT-early','UNSAT-late'):
            v=list(u)
            if case=='UNSAT-early':v[0]^=1
            if case=='UNSAT-late':v[-1]^=1
            lab,p,mem=run_stream(encode(u,tuple(v)),B)
            assert lab==('SAT' if case=='SAT' else 'UNSAT')
            assert p== (1 if case=='UNSAT-early' else math.ceil(k/B))
            print(k,B,case,lab,'passes',p,'payload_bits',mem,'read_words',p*(32*k+2))
            tests+=1
    print('PASSMEM84 minirepro cases:',tests,'all successful')

if __name__=='__main__':check()
