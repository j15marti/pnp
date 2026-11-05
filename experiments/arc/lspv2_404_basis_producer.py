#!/usr/bin/env python3
"""Exact cost of auxiliary-free CNF bases with B(k,s) upper weights.
For k<=4, Dijkstra over all forbidden truth-table subsets; independently replayable.
No assertion about an actual proof-system minimum is made here.
"""
from __future__ import annotations
import json,heapq,time,hashlib,sys

def all_clauses(k):
    out=[]
    for trits in __import__('itertools').product((-1,0,1),repeat=k):
        w=sum(t!=0 for t in trits)
        if not w: continue
        bad=0
        for a in range(1<<k):
            if all(t==0 or ((a>>i)&1)==(1 if t==1 else 0) for i,t in enumerate(trits)):
                bad |=1<<a
        cost=(1<<(k-w))-1+3*max(w-1,0)
        out.append({'mask':bad,'trits':trits,'width':w,'cost':cost})
    return out

def dijkstra(k):
    clauses=all_clauses(k)
    maxmask=(1<<(1<<k))-1
    dist=[10**9]*(maxmask+1)
    dist[0]=0
    prev=[None]*(maxmask+1)
    h=[(0,0)]
    settled=0
    while h:
        d,s=heapq.heappop(h)
        if d!=dist[s]:continue
        settled+=1
        for j,c in enumerate(clauses):
            t=s|c['mask'];nd=d+c['cost']
            if nd<dist[t]:
                dist[t]=nd;prev[t]=(s,j);heapq.heappush(h,(nd,t))
    parity_even=0;parity_odd=0
    for a in range(1<<k):
        if a.bit_count()%2:parity_odd|=1<<a
        else:parity_even|=1<<a
    mx=max(dist); maximizers=sum(x==mx for x in dist)
    threshold=3*(k-1)*(1<<(k-1))
    assert settled==len(dist)
    assert mx==threshold
    assert dist[parity_even]==mx and dist[parity_odd]==mx
    for s in range(len(dist)):
        t=s;cost=0;cover=0
        while t:
            p,j=prev[t];c=clauses[j];cost+=c['cost'];cover |=c['mask'];assert p|c['mask']==t
            assert p<t
            t=p
        assert cost==dist[s] and cover==s
    hist={}
    for d in dist:hist[d]=hist.get(d,0)+1
    return {'k':k,'relations':len(dist),'clause_types':len(clauses),'max_weighted_basis':mx,'maximizers':maximizers,
            'parity_bad_masks':[parity_even,parity_odd],'parity_costs':[dist[parity_even],dist[parity_odd]],
            'histogram':dict(sorted(hist.items())),'distance_sha256':hashlib.sha256(','.join(map(str,dist)).encode()).hexdigest(),
            'settled':settled}

def main():
    start=time.monotonic();runs=[dijkstra(k) for k in (2,3,4)]
    result={'claim':'exact minimax of weighted auxiliary-free CNF bases, NOT a proof-DAG minimum',
            'weight':'B(k,s)=2^(k-s)-1+3max(s-1,0)',
            'runs':runs,'elapsed_s':round(time.monotonic()-start,5),
            'malformed_rejections':0}
    def check_mask(k,m):
        if not isinstance(k,int) or k<1 or k>4 or not isinstance(m,int) or m<0 or m>=(1<<(1<<k)):
            raise ValueError('malformed table')
    for bad in [(-1,0),(4,-1),(4,1<<16),('4',0),(3,1<<8),(0,0)]:
        try:check_mask(*bad)
        except ValueError:result['malformed_rejections']+=1
    assert result['malformed_rejections']==6
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
