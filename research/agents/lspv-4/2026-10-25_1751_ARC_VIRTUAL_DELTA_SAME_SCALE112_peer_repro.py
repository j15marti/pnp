#!/usr/bin/env python3
"""Peer test: two exact Shannon levels and bit-for-bit virtual vs physical CNF.
Finite checks, NOT FLMV time/space tape instrumentation. Standard library."""
import json
import random

SEED=1122026
Y=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))

def u(x,w):return format(x,'0%db'%w)
def slot(c,w):
    return u(len(c),2)+''.join(u((abs(v)+(1<<(w-1))*(v<0)) if j<len(c) else 0,w)
                                for j,v in enumerate(tuple(c)+(0,)*(3-len(c))))
def enc(f,n,w):
    return u(w,8)+u(n,w)+u(len(f),w)+''.join(slot(c,w) for c in f)
def rstr(f,a):
    return tuple(tuple(v for v in c if abs(v) not in a) for c in f
                 if not any(abs(v) in a and a[abs(v)]==(v>0) for v in c))
def sat(f,n):
    return any(all(any(bool((z>>(abs(v)-1))&1)==(v>0) for v in c) for c in f)
               for z in range(1<<n))
def virtual_bit(parent,f,a,w,j,n):
    H=8+2*w;B=2+3*w
    deleted=[];edits={}
    for idx,c in enumerate(f):
        hit=[v for v in c if abs(v) in a]
        if not hit:continue
        if any(a[abs(v)]==(v>0) for v in hit):deleted.append(idx)
        else:edits[idx]=slot(tuple(v for v in c if abs(v) not in a),w)
    m=len(f)-len(deleted)
    header=u(w,8)+u(n,w)+u(m,w)
    if j<H:return header[j]
    x,off=divmod(j-H,B)
    for idx in deleted:
        if idx<=x:x+=1
        else:break
    return edits[x][off] if x in edits else parent[H+x*B+off]
def test(f,n):
    w=max(3,(4*(n+len(f)+2)).bit_length())
    base=enc(f,n,w);total=0
    answer=sat(f,n)
    for direction in (0,1):
        work=[({},f)]
        for level in range(2):
            temp=[]
            for a,g in work:
                variables=sorted({abs(v) for c in g for v in c})
                if not variables:
                    temp.append((a,g));continue
                x=variables[-1] if direction else variables[0]
                for b in (False,True):
                    aa=dict(a);aa[x]=b;temp.append((aa,rstr(g,{x:b})))
            work=temp
        assert any(sat(g,n) for a,g in work)==answer
        total+=1
        for a,g in work:
            actual=enc(g,n,w)
            decoded=''.join(virtual_bit(base,f,a,w,j,n) for j in range(len(actual)))
            assert decoded==actual
            total+=len(actual)
    assert sum(int(x) for x in base)%2==sum(int(base[j]) for j in range(len(base)-1,-1,-1))%2
    return total+1
def main():
    rng=random.Random(SEED);checks=0;cases=0
    fixtures=[(Y,6),
              (Y+tuple(tuple((abs(v)+6)*(1 if v>0 else -1) for v in c) for c in Y),12),
              (tuple(tuple((1 if (p>>j)&1 else -1)*(j+1) for j in range(3)) for p in range(8)),3),
              (((1,),(-1,2),(-2,)),2),
              (((1,2),(-1,-2),(1,-2),(-1,2)),2)]
    for k in range(96):
        n=rng.randrange(3,8)
        f=tuple(tuple(v if rng.randrange(2) else -v for v in rng.sample(range(1,n+1),rng.randrange(1,4)))
                for _ in range(rng.randrange(2,12)))
        fixtures.append((f,n))
    for f,n in fixtures:checks+=test(f,n);cases+=1
    print(json.dumps({'test':'ARC-VIRTUAL-DELTA112-peer','seed':SEED,'cases':cases,
                      'bit_and_answer_checks':checks,'failures':0,
                      'label':'finite exact, not full FLMV machine measurement'}))
if __name__=='__main__':main()
