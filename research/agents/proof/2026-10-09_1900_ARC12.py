"""Capped natural-run residual merge. Logical counters, not Python bit costs."""
import heapq
import itertools as it
import json
import random
import signal
from collections import Counter

signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError()))
signal.alarm(24)

def residual(row,a,m):
    s=set(); sat=False
    for x in row:
        m['literal_reads']+=1
        if abs(x) in a:
            sat |= a[abs(x)] == (x>0)
        else:
            s.add(x)
    if sat or any(-x in s for x in s): return None
    return tuple(sorted(s))

def discover(f,a,cap,m):
    runs=[]; start=end=None; prev=None; direction=0
    for pos,row in enumerate(f):
        c=residual(row,a,m)
        if c is None: continue
        if start is None:
            start=end=pos; prev=c; continue
        delta=(c>prev)-(c<prev)
        if direction and delta and direction!=delta:
            runs.append((start,end,direction))
            if len(runs)>=cap:
                m['cap_exceeded']+=1
                return None
            start=pos; direction=0
        elif not direction and delta:
            direction=delta
        end=pos; prev=c
    if start is not None:
        runs.append((start,end,direction or 1))
    if len(runs)>cap: return None
    m['run_descriptors']+=len(runs)
    return runs

def canonical(f,a,runs,m):
    heap=[]
    def advance(pos,end,step,ident):
        while (pos<=end if step==1 else pos>=end):
            c=residual(f[pos],a,m)
            pos+=step
            if c is not None:
                heapq.heappush(heap,(c,ident,pos,end,step))
                m['heap_pushes']+=1
                return
    for ident,(lo,hi,direction) in enumerate(runs):
        advance(lo if direction>0 else hi,hi if direction>0 else lo,direction,ident)
    prev=None
    while heap:
        c,ident,pos,end,step=heapq.heappop(heap)
        m['heap_pops']+=1
        if prev is None or c!=prev:
            yield c
            prev=c
        advance(pos,end,step,ident)

def compare(f,a,b,cap,m):
    ra=discover(f,a,cap,m)
    if ra is None: return 'UNKNOWN'
    rb=discover(f,b,cap,m)
    if rb is None: return 'UNKNOWN'
    sentinel=object()
    for x,y in it.zip_longest(canonical(f,a,ra,m),canonical(f,b,rb,m),fillvalue=sentinel):
        m['comparisons']+=1
        if x!=y: return 'DISTINCT'
    return 'EQUAL'

def oracle(f,a):
    return tuple(sorted(set(c for row in f if (c:=residual(row,a,Counter())) is not None)))

def main():
    checks=0
    for p in it.permutations(range(1,8)):
        f=tuple((v,) for v in p)
        m=Counter(); runs=discover(f,{},7,m)
        assert tuple(canonical(f,{},runs,m))==oracle(f,{})
        checks+=1
    core=tuple(it.product((-1,1),(-2,2),(-3,3)))
    for mask in range(256):
        f=tuple(c for j,c in enumerate(core) if mask>>j&1)
        noisy=f+tuple(tuple(reversed(c)) for c in reversed(f))+((1,-1),())
        for a in ({},{1:False},{1:True}):
            m=Counter(); r=discover(noisy,a,32,m)
            assert tuple(canonical(noisy,a,r,m))==oracle(noisy,a)
            checks+=1
    rows=[]
    for size in (8,32,128,512):
        core=tuple((v,v+1,v+2) for v in range(2,size+2))
        for mode in ('reverse','shuffle','two_runs','alternating'):
            other=list(core)
            if mode=='reverse': other.reverse()
            elif mode=='shuffle': random.Random(12).shuffle(other)
            elif mode=='two_runs': other=other[::2]+list(reversed(other[1::2]))
            else: other=[core[i] for pair in zip(range(size-1,size//2-1,-1),range(size//2)) for i in pair]
            f=tuple((1,)+c for c in core)+tuple((-1,)+c for c in other)
            m=Counter(); answer=compare(f,{1:False},{1:True},4,m)
            if mode in ('reverse','two_runs'): assert answer=='EQUAL'
            rows.append(dict(size=size,mode=mode,answer=answer,**m))
    m=Counter()
    assert compare(((1,2),(1,-2),(-1,3),(-1,-3)),{1:False},{1:True},4,m)=='DISTINCT'
    print(json.dumps(dict(status='COMPUTATIONAL',checks=checks,seed=12,cap=4,scaling=rows),indent=2))

if __name__=='__main__': main()
