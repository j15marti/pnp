#!/usr/bin/env python3
"""TMR-3/058: exhaustive reference audit for source-indexed frontier eviction.
The Python program materializes test traces; this is NOT a measured TM space bound.
"""
from __future__ import annotations
import json, hashlib, itertools
from collections import Counter

REV='tmr3-source-frontier058-py-v1'

def source(x): return '1'*len(x)+'0'+x

def parse(s):
    if not s or set(s)-{'0','1'}: return None
    b=s.find('0')
    if b<1 or len(s)!=2*b+1: return None
    return s[b+1:]

def stages(x):
    for j,ch in enumerate(x,1):
        if ch=='1':
            for a,op in ((j-1,'hold'),(j-2,'hold'),(j-1,'hold')):
                yield (j,a,op,int(ch))
        for a,op in ((j-1,'hold'),(j-2,'a'),(j-1,'p'),(j,'write')):
            yield (j,a,op,int(ch))

def step_at(x,k):
    # Indexable source-only schedule. No cached movement word.
    t=0
    for j,ch in enumerate(x,1):
        if ch=='1':
            for a,op in ((j-1,'hold'),(j-2,'hold'),(j-1,'hold')):
                if t==k: return (j,a,op,int(ch))
                t+=1
        for a,op in ((j-1,'hold'),(j-2,'a'),(j-1,'p'),(j,'write')):
            if t==k: return (j,a,op,int(ch))
            t+=1
    raise IndexError(k)

def nsteps(x): return 4*len(x)+3*x.count('1')

def graph_frontier(trace,t):
    before={a for _,a,_,_ in trace[:t+1]}
    after={a for _,a,_,_ in trace[t+1:]}
    return before & after

def reference(x):
    cells={}; a=p=0; output=0; events=list(stages(x)); logs=[]
    prev_head=0
    for t,(j,addr,op,bit) in enumerate(events):
        assert abs(addr-prev_head)<=1
        prev_head=addr
        val=cells.get(addr,0)
        if op=='a': a=val
        if op=='p': p=val
        if op=='write':
            output=(p&a)^bit
            cells[addr]=output
        logs.append((addr,op,val,output))
    return output,events,logs

def virtual(x):
    H=nsteps(x); cache={}; a=p=0; output=0
    calls=0; peak=0; logs=[]
    for t in range(H):
        j,addr,op,bit=step_at(x,t); calls+=1
        val=cache.get(addr,0)
        if op=='a': a=val
        if op=='p': p=val
        if op=='write': output=(p&a)^bit; val=output
        future=False
        for u in range(t+1,H):
            jj,aa,oo,bb=step_at(x,u); calls+=1
            if aa==addr: future=True;break
        if future: cache[addr]=val
        else: cache.pop(addr,None)
        peak=max(peak,len(cache))
        logs.append((addr,op,val if op!='write' else cache.get(addr,output),output,set(cache)))
    return output,peak,calls,logs

def recurrence(x):
    p=a=0
    for bit in x:
        c=(p&a)^int(bit)
        a,p=p,c
    return p

def main():
    checks=0; count=0; bad=0; largest=0; max_w=0; max_c=0; all_steps=0; graph_edges=0
    byB=[]
    for B in range(1,9):
        words=[''.join(w) for w in itertools.product('01',repeat=B)] if B<=7 else [format(k,'08b') for k in [0,1,2,3,7,15,31,63,85,127,128,170,192,224,240,248,252,254,255]]
        wb=0; cb=0
        for x in words:
            out,tr,logs=reference(x)
            vout,peak,calls,vlogs=virtual(x)
            width=max((len(graph_frontier(tr,t)) for t in range(len(tr))),default=0)
            checks+=3
            assert out==vout==recurrence(x)
            assert len(tr)==nsteps(x)
            assert peak<=width
            for t,e in enumerate(tr):
                checks+=3
                assert step_at(x,t)==e
                assert vlogs[t][:2]==(e[1],e[2])
                assert vlogs[t][4]==graph_frontier(tr,t)
                if t>0:
                    checks+=1
                    assert abs(tr[t][1]-tr[t-1][1])<=1
                # Last access predecessor is an authentic source-derived edge.
                prior=[u for u in range(t) if tr[u][1]==e[1]]
                if prior:
                    graph_edges+=1
                    checks+=1
                    assert tr[prior[-1]][1]==e[1]
            checks+=1
            assert calls<=nsteps(x)*(nsteps(x)+1)//2
            count+=1; wb=max(wb,width); cb=max(cb,calls)
            max_w=max(max_w,width);max_c=max(max_c,calls);all_steps+=len(tr)
        byB.append(dict(B=B,cases=len(words),max_width=wb,max_calls=cb))
    # A one-cell no-retention scheme cannot compute the nonaffine B=3 instance x=110.
    checks+=2
    assert recurrence('110')==1
    assert ((0 & 1)^0)==0
    for s in ['','0','110','1110','11100','1110a','111001','111100']:
        if parse(s) is None:bad+=1
    checks+=1
    assert bad==8
    result={'revision':REV,'mode':'exhaustive B<=7; deterministic B8 controls','seed':None,'cases':count,'simulated_steps':all_steps,'source_last_visit_edges':graph_edges,'assertions':checks,'failures':0,'max_frontier_width':max_w,'max_generator_calls':max_c,'per_B':byB,'note':'Python reference stores traces for checking; not physical workspace measurement'}
    print(json.dumps(result,sort_keys=True,separators=(',',':')))
if __name__=='__main__':main()
