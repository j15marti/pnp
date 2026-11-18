#!/usr/bin/env python3
"""Finite tests for Kun fiber decoding; these are not high-girth construction tests."""
import itertools,json
from collections import Counter
R=lambda a,b:(b-a)%5 in (1,3)
def modes(xs):
 c=Counter(xs);m=max(c.values());return [a for a in range(5) if c[a]==m]
tests=valid=0
for x in itertools.product(range(5),repeat=6):
 left,right=x[:3],x[3:]
 if all(R(a,b) for a in left for b in right):
  valid+=1
  for a,b in itertools.product(modes(left),modes(right)):
   tests+=1
   assert R(a,b)
# Projection alone is insufficient: diagonal matching, no expansion.
left=(0,1);right=(1,2)
assert all(R(a,b) for a,b in zip(left,right))
bad=[(a,b) for a,b in itertools.product(modes(left),modes(right)) if not R(a,b)]
assert bad
rels=set()
for L in range(1,9):
 for w in itertools.product((1,2),repeat=L):
  d={0}
  for a in w:d={(s+a+2*b)%5 for s in d for b in (0,1)}
  assert len(d)==min(5,L+1)
  if L<=3:rels.add(frozenset(d))
assert len(rels)==9
hist=Counter()
for mask in range(1,512):
 f=[r for i,r in enumerate(sorted(rels,key=lambda x:sorted(x))) if mask>>i&1]
 meet=set(range(5)).intersection(*f)
 if all(set(range(5)).intersection(*(f[:i]+f[i+1:]))!=meet for i in range(len(f))):
  hist[len(f)]+=1
assert hist=={1:9,2:26,3:24,4:4}
print(json.dumps({"complete_blowup_assignments":15625,"valid_lift_colorings":valid,
"all_modal_pair_checks":tests,"nonexpanding_projection_counterexample":{"left":left,"right":right,"bad_modal_pairs":bad},
"path_words":510,"irredundant_distribution":dict(hist),
"status":"PASS; finite decoder controls, no high-girth compiler executed"},indent=2))
