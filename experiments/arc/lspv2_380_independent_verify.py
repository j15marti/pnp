#!/usr/bin/env python3
"""Independent oracle for LSPV-2/380; does not import the JS producer."""
import json, sys, collections, itertools
from pathlib import Path
raw=json.loads(Path(sys.argv[1]).read_text())
clauses=[tuple(c) for c in raw['all_clauses']]
assert len(clauses)==9 and len(set(clauses))==9
assert clauses[0]==()
lookup={c:i for i,c in enumerate(clauses)}
checks=0
def canon(xs):
    return tuple(sorted(xs,key=lambda z:(abs(z),z)))
def rule(a,b):
    out=set()
    for pivot in a:
        if -pivot not in b: continue
        c=set(a)-{pivot}; c.update(set(b)-{-pivot})
        if any(-v in c for v in c):continue
        out.add(canon(c))
    return out
trans={}
for a in range(9):
    for b in range(a,9):
        trans[(a,b)]={lookup[r] for r in rule(clauses[a],clauses[b])}
def min_paid(source):
    if source&1:return 0
    shortest={source:0}; queue=collections.deque([source])
    while queue:
        state=queue.popleft()
        active=[j for j in range(9) if state&(1<<j)]
        for aa,bb in itertools.combinations_with_replacement(active,2):
            for c in trans[(aa,bb)]:
                if state&(1<<c):continue
                if c==0:return shortest[state]+1
                nxt=state | (1<<c)
                if nxt not in shortest:
                    shortest[nxt]=shortest[state]+1
                    queue.append(nxt)
    return None
def holds(c,a):
    return any(bool(a&(1<<(abs(x)-1)))==(x>0) for x in c)
def sat(src,variables):
    return any(all(holds(c,a) for c in src) for a in range(1<<variables))
hist=collections.Counter();sat_count=0;unsat_count=0;commutes=0
assert len(raw['rows'])==512
for target,row in enumerate(raw['rows']):
    assert row['mask']==target
    initial=[clauses[i] for i in range(9) if target&(1<<i)]
    guarded=[canon([-3,*c]) for c in initial]
    truth=sat(initial,2)
    assert sat(guarded,3)
    entails=not any(all(holds(c,a) for c in guarded) for a in range(4,8))
    assert entails==(not truth)
    assert row['sat']==truth and row['entails_neg_t']==entails
    correct=min_paid(target)
    assert row['source_resolution_min_nodes']==correct,(target,correct,row)
    learned=set(initial)
    while True:
        following=learned.copy()
        for ca in learned:
            for cb in learned:
                following.update(rule(ca,cb))
        if following==learned:break
        learned=following
    bitset=sum(1<<lookup[c] for c in learned)
    assert row['source_closure_mask']==bitset
    for aa,bb in itertools.combinations_with_replacement(initial,2):
        left={canon([-3,*c]) for c in rule(aa,bb)}
        right=rule(canon([-3,*aa]),canon([-3,*bb]))
        assert left==right
        commutes+=1
    if truth:sat_count+=1
    else:unsat_count+=1;hist[correct]+=1
    checks+=6
assert sat_count==raw['counts']['sat']
assert unsat_count==raw['counts']['unsat']
assert {str(k):v for k,v in hist.items()}==raw['counts']['unsat_cost_hist']
assert raw['counts']['max_min_nodes']==max(hist)
assert raw['counts']['nontrivial_unsat']==sum(v for k,v in hist.items() if k>0)
print(json.dumps({'independent_checks':checks+commutes+5,'resolution_commutations':commutes,
'sat_sources':sat_count,'unsat_sources':unsat_count,'unsat_cost_hist':dict(hist),'passed':True},sort_keys=True))
