#!/usr/bin/env python3
"""Complete six-variable M22 antipodal/hitting audit. Python standard library only."""
from itertools import combinations
from collections import Counter
from math import comb
import json
V=tuple(range(6))
triples=tuple(combinations(V,3))
number={t:i for i,t in enumerate(triples)}
masks=[sum(1<<x for x in t) for t in triples]
opposite={j:number[tuple(x for x in V if x not in t)] for j,t in enumerate(triples)}
B=[a for a in range(64) if a.bit_count()==3]
Pfamilies=[p for p in combinations(range(20),4)
  if all(sum(x in triples[j] for j in p)==2 for x in V)]
assert len(Pfamilies)==75 and len(B)==20
counts=Counter()
badsets=set()
fixed=[7,11,13,14,19] # TRUE supports 123,124,134,234,125, indexed 1..6
for P in Pfamilies:
    for Q in Pfamilies:
        q=4-len(set(P)&set(Q))
        h=len(set(P)&{opposite[j] for j in Q})
        sat=lambda a:(all(a&masks[j] for j in P) and
                      all((~a)&masks[j] for j in Q))
        balanced=[a for a in B if sat(a)]
        assert len(balanced)==12+h and h!=3
        assert any(sat(a) for a in fixed)
        assert all(any(((a>>v)&1)==bit for a in balanced)
                   for v in V for bit in (0,1))
        assert any(sat(a) for a in range(64))
        badsets.add(frozenset(i for i,a in enumerate(B) if not sat(a)))
        counts[q,h]+=1
assert sum(counts.values())==5625
assert sum(n for (q,h),n in counts.items() if q>0)==5550
assert len(badsets)==2085
failed4=set()
for bad in badsets:
    failed4.update(combinations(sorted(bad),4))
assert len(failed4)==comb(20,4)==4845
assert counts=={(0,0):30,(0,4):45,(2,0):180,(2,2):1080,
                (3,0):240,(3,1):1440,(4,0):2160,(4,1):240,
                (4,2):180,(4,4):30}
print(json.dumps({"run":"M22-ANTIPODAL-SIX103","source_families":75,
 "source_pairs":5625,"target_pairs":5550,"distinct_badsets":2085,
 "failed_four_candidate_lists":4845,
 "minimal_fixed_balanced_test_count":5,
 "fixed_true_sets":[[v+1 for v in V if a>>v&1] for a in fixed],
 "qh_counts":{str(q)+","+str(h):n for (q,h),n in sorted(counts.items())},
 "failed_assertions":0},indent=2,sort_keys=True))
