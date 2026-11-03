"""Exhaustive, deterministic local substitution probe: q <-> (a AND b).
Checks every proper 4-name clause pair and every signed gate-input orientation.
A derived target may be reached by at most two RES layers followed by weakening.
This is NOT a global ER2 proof-size experiment or unrestricted hardness result.
"""
from itertools import product
import json
from pathlib import Path
def norm(a):
    s=frozenset(a)
    if any(-x in s for x in s):return None
    return s
def subst(c,a,b):
    if 1 in c:
        z=c-{1}
        return [x for x in (norm(z|{a}),norm(z|{b})) if x is not None]
    if -1 in c:return [x for x in [norm((c-{-1})|{-a,-b})] if x is not None]
    return [c]
def pivot(c,d,p):
    if p in c and -p in d:return norm((c-{p})|(d-{-p}))
    if -p in c and p in d:return norm((c-{-p})|(d-{p}))
    return None
clauses=[]
for signs in product((-1,0,1),repeat=4):
    clauses.append(frozenset((j+1)*s for j,s in enumerate(signs) if s))
count=0;errors=[]
for a in (2,-2):
 for b in (3,-3):
  for c in clauses:
   for d in clauses:
    for p in range(1,5):
     r=pivot(c,d,p)
     if r is None:continue
     count+=1
     known=set(subst(c,a,b)+subst(d,a,b))
     for layer in range(2):
        newer=set()
        for e in known:
         for f in known:
          for x in (2,3,4):
           t=pivot(e,f,x)
           if t is not None:newer.add(t)
        known|=newer
     for goal in subst(r,a,b):
      if not any(k<=goal for k in known):
       errors.append({'a':a,'b':b,'c':sorted(c),'d':sorted(d),'pivot':p,'target':sorted(goal)})
result={'status':'PASS' if not errors else 'FAIL','checks':count,'failures':errors[:12],
        'scope':'four named variables, four signed gate orientations; local two-RES-layer subsumption'}
print(json.dumps(result,indent=2))
if errors:raise AssertionError('local gate elimination falsified')
