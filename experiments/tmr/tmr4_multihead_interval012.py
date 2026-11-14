#!/usr/bin/env python3
"""TMR-4/012: independently reproducible exact multihead MAY distance audit.
One charged transition reads every pre-move head cell and moves each head by <=1.
Extra MAY edges reading subsets cannot shorten an optimal path since observation is monotone.
"""
from collections import deque
from itertools import product
from functools import lru_cache
import json, random, hashlib

SEED=202611132136
R=random.Random(SEED)
counts=dict(seed=SEED,comparisons=0,all_edge_checks=0,abstract_states=0,
            bfs_edges=0,full_observation_bfs=0,negative_controls=0,failures=0,
            multiple_head_cases=0,one_head_cases=0)

def potential(L,head,V,supports):
    unhit=tuple(d for d in supports if d & V == 0)
    if not unhit: return 0
    options=[]
    for p in head:
        o=[]
        for a in range(p+1):
            for b in range(p,L):
                mask=((1<<(b-a+1))-1)<<a
                hits=sum((1<<i) for i,d in enumerate(unhit) if d&mask)
                turns=(b-a)+min(p-a,b-p)
                o.append((hits,turns))
        options.append(o)
    target=(1<<len(unhit))-1
    best=10**9
    for tuple_opt in product(*options):
        if max(t for _,t in tuple_opt)+1>=best:continue
        covered=0
        for hits,_ in tuple_opt: covered|=hits
        if covered==target:
            best=min(best,1+max(t for _,t in tuple_opt))
    assert best<10**9
    return best

def moves(L,head):
    return product(*[tuple(x for x in (p-1,p,p+1) if 0<=x<L) for p in head])

def bfs(L,head,V,supports):
    if all(d&V for d in supports):return 0,0,0
    q=deque([(head,V,0)])
    seen={(head,V)}
    edges=0
    while q:
        h,v,t=q.popleft()
        full=v
        for p in h:full|=1<<p
        for hn in moves(L,h):
            edges+=1
            if all(d&full for d in supports):
                return t+1,len(seen),edges
            s=(hn,full)
            if s not in seen:
                seen.add(s);q.append((hn,full,t+1))
    raise AssertionError('unreachable')

def check(L,head,supports,edge_audit=False):
    V=0
    formula=potential(L,head,V,supports)
    short,nstates,nedges=bfs(L,head,V,supports)
    assert formula==short, (L,head,supports,formula,short)
    counts['comparisons']+=1
    counts['abstract_states']+=nstates
    counts['bfs_edges']+=nedges
    counts['full_observation_bfs']+=1
    counts['multiple_head_cases' if len(head)>1 else 'one_head_cases']+=1
    if edge_audit:
        @lru_cache(None)
        def pot(h,v):return potential(L,h,v,supports)
        for h in product(range(L),repeat=len(head)):
            for v in range(1<<L):
                before=pot(h,v)
                if all(d&v for d in supports):assert before==0
                for hn in moves(L,h):
                    for chosen in range(1<<len(head)):
                        observed=v
                        for j,p in enumerate(h):
                            if chosen>>j&1:observed|=1<<p
                        after=pot(hn,observed)
                        assert before<=1+after,(L,h,v,hn,chosen,before,after)
                        counts['all_edge_checks']+=1
    return formula

# Fixed hostile tests.
assert check(11,(5,), (1<<0,1<<10))==16
assert check(11,(0,10), (1<<0,1<<10))==1
assert check(11,(0,0), (1<<0,1<<10))==11
assert potential(11,(5,), (1<<0)|(1<<10),(1<<0,1<<10))==0
assert potential(11,(0,), 0,(1<<10,))==11
assert potential(11,(10,), 1<<10,(1<<10,))==0
# An *illegally free* remote-read jump would break potential inequality.
assert potential(11,(0,),0,(1<<10,))>1+potential(11,(10,),1<<10,(1<<10,))
counts['negative_controls']=7

for L in range(2,8):
    for hnum in (1,2,3):
        if hnum==3 and L>=7:continue
        for z in range(14 if L<=5 else 8):
            head=tuple(R.randrange(L) for _ in range(hnum))
            supports=tuple(R.randrange(1,1<<L) for _ in range(R.randint(1,5)))
            check(L,head,supports,edge_audit=(L<=4 and hnum<=2 and z<2))

# Exact every-edge audit of a larger 2-head configuration.
check(5,(1,3),(1<<0,1<<4,(1<<1)|(1<<2)),edge_audit=True)

assert counts['failures']==0
text=json.dumps(counts,sort_keys=True,indent=2)+'\n'
open('/mnt/data/tmr4_2136/raw012.json','w').write(text)
print(text)
