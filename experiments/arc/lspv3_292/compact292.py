#!/usr/bin/env python3
"""GATE292 compact self-contained six-variable census, no external fixtures."""
import itertools, collections, json
T=list(itertools.combinations(range(1,7),3))
P=[s for s in itertools.combinations(T,4)
   if all(sum(v in c for c in s)==2 for v in range(1,7))]
assert len(P)==75
R=collections.Counter()
for pos in P:
 for neg in P:
  F=tuple(pos)+tuple(tuple(-v for v in c) for c in neg)
  for c in pos:
   for d in neg:
    shared=set(c)&set(d)
    R['pivot_attempts']+=len(shared)
    R['tautologies']+=len(shared) if len(shared)>1 else 0
    R['width4']+=int(len(shared)==1)
  assert R['pivot_attempts']%24==0
  for mask in range(64):
   true=[[l for l in c if bool((mask>>(abs(l)-1))&1)==(l>0)] for c in F]
   R['assignment_rows']+=1
   if any(len(t)==0 for t in true):continue
   R['models']+=1
   c1=[t[0] for t in true if len(t)==1]
   n3=sum(len(t)==3 for t in true)
   assert len(c1)==4+n3
   critical={abs(v) for v in c1}
   assert len(critical)>=2
   if len(critical)==2:R['tight_models']+=1
  R['formulas']+=1
assert dict(R)=={'pivot_attempts':135000,'tautologies':94500,'width4':40500,
 'assignment_rows':360000,'models':119250,'tight_models':14850,'formulas':5625}
print(json.dumps(dict(R),sort_keys=True))
