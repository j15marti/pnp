#!/usr/bin/env python3
"""Independent Python LSPV-4/548 cap-five in-place DAG exhaustor.
This is a fixed occurrence DAG register-slot model, NOT a SAT lower bound.
Run: python3 experiments/arc/lspv4_548_independent_cap5.py
"""
import json
from collections import deque

P=[[],[0],[0],[1],[2],[],[5],[5],[6],[4,8],[9],[7],[3,11],[12],[],[14],[15],[14],[17],[],[19],[19],[21],[22,18],[23],[13,24],[20],[26,16],[27],[28,10],[25,29],[],[31],[],[33],[34,32],[35],[],[37],[],[39],[40,38],[41],[42,36],[43],[],[45],[],[47],[46,48],[49],[],[51],[],[53],[54,52],[55],[50,56],[57],[44,58],[59,30],[60]]
n=len(P)
full=(1<<n)-1
pm=[sum(1<<j for j in pred) for pred in P]
sm=[0]*n
for i,pred in enumerate(P):
    for j in pred: sm[j]|=1<<i

def live(mask):
    todo=full^mask
    return sum(bool(mask>>i&1 and sm[i]&todo) for i in range(n))

def reusable(mask,i):
    todo=full^mask
    return any((sm[j]&todo)==1<<i for j in P[i])

def search(cap):
    seen={0}
    q=deque([0])
    visited=0
    transitions=0
    furthest=0
    while q:
        mask=q.popleft()
        visited+=1
        furthest=max(furthest,mask.bit_count())
        if mask==full:
            return {'cap':cap,'reached':True,'visited':len(seen),
                    'transitions':transitions,'furthest':furthest}
        alive=live(mask)
        for i in range(n):
            if mask>>i&1 or pm[i]&~mask: continue
            if alive+(0 if reusable(mask,i) else 1)>cap: continue
            nxt=mask|1<<i
            transitions+=1
            if nxt not in seen:
                seen.add(nxt)
                q.append(nxt)
    return {'cap':cap,'reached':False,'visited':len(seen),
            'transitions':transitions,'furthest':furthest}

mask=0
peak=0
overwrite_count=0
for i in range(n):
    assert not pm[i]&~mask
    use=reusable(mask,i)
    overwrite_count+=use
    peak=max(peak,live(mask)+(0 if use else 1))
    mask|=1<<i
assert mask==full
result=search(5)
assert n==62 and peak==6
assert not result['reached']
assert result['visited']==185340
assert result['transitions']==725941
assert result['furthest']==48
assert overwrite_count==46
print(json.dumps({'model':'whole-clause slots, no recomputation, any last-use overwrite',
                  'proofNodes':n,'logicalWorkIncludingOwner':63,
                  'givenAreaOrderInplacePeak':peak,
                  'givenAreaOrderLastUseReuses':overwrite_count,
                  'cap5':result,'status':'finite exhaustive verified'},
                 indent=2))
