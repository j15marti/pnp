#!/usr/bin/env python3
"""Finite CLOCKPATHGUARD46 T5, polarity, and exponent controls."""
from fractions import Fraction as Q
from itertools import product
import json
checks=0
def test(v):
 global checks
 checks+=1
 assert v, checks
R=lambda a,b: (b-a)%5 in (1,3)
words=('BBB','FBB','FFF','BB')
def feasible(w,u,v):
 for mid in product(range(5),repeat=len(w)-1):
  p=(u,)+mid+(v,)
  if all(R(p[i],p[i+1]) if ch=='F' else R(p[i+1],p[i]) for i,ch in enumerate(w)): return True
 return False
support=[{d for d in range(5) if feasible(w,0,d)} for w in words]
for u,v in product(range(5),repeat=2):
 bad=[j for j,w in enumerate(words) if not feasible(w,u,v)]
 test(len(bad)==1)
 for j,w in enumerate(words): test(feasible(w,u,v)==((v-u)%5 in support[j]))
for gone in range(4):
 test(any(all(feasible(w,u,v) for j,w in enumerate(words) if j!=gone) for u,v in product(range(5),repeat=2)))
def certify(present,mask):
 chosen=[j for j in range(4) if mask>>j&1]
 if not set(chosen)<=set(present): return False
 return all(any(d not in support[j] for j in chosen) for d in range(5))
for gone in range(4):
 present=[j for j in range(4) if j!=gone]
 for mask in range(16):test(not certify(present,mask))
for mask in range(16):test(certify(range(4),mask)==(mask==15))
# Complete deterministic exact decider: capping one label defaults to the other.
for truth in (0,1):
 for costly in ('time','space','both'):
  t=(8 if costly!='space' else 2); s=(8 if costly!='time' else 2)
  for fast in (0,1):
   used=(2,2) if truth==fast else (t,s)
   got=truth if used[0]<=4 and used[1]<=4 else 1-fast
   test(got==truth)
# Layout exponents and adversarial advice frontier.
r,b,m=Q(39,200),Q(13,20),Q(7,20)
target=Q(133,100)
tcut=(target-r-b)/m;scut=Q(1,2)/m
test(tcut==Q(97,70) and scut==Q(10,7))
test(target+Q(1,100)<Q(13407,10000))
print(json.dumps({'checks':checks,'failures':0,'supports':[sorted(x) for x in support],
 'seed_time_limit':str(tcut),'seed_space_limit':str(scut),
 'excluded_alpha':'alpha < 0.01070 with uniform sound one-sided branch verifier and charged enumeration'},sort_keys=True))
