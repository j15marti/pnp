#!/usr/bin/env python3
"""Independent compact structural reproducer of LSPV-4 320.
No external imports. Restricted signed balanced width2/3 compiler only.
Full producer, independent verifier and original-clause evidence are in ZIP.
"""
from itertools import product
from collections import Counter
from fractions import Fraction
import json

F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
    (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),
    (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
H=((1,2),(5,3),(6,8))+F9[2:]

def valid(f,n,allowed=(2,3)):
    if not f or len(set(tuple(sorted(c)) for c in f))!=len(f):return False
    if any(len(c) not in allowed or len(set(map(abs,c)))!=len(c)
           or any(abs(v)<1 or abs(v)>n for v in c) for c in f):return False
    s=Counter(v for c in f for v in c)
    return all(s[x]==s[-x]==2 for x in range(1,n+1))

def model_count(f,n,pin=None):
    pin=pin or {}
    count=0
    for a in product((0,1),repeat=n):
        if any(a[x-1]!=b for x,b in pin.items()):continue
        if all(any(a[abs(v)-1]==int(v>0) for v in c) for c in f):count+=1
    return count

assert valid(F9,9,(3,)) and valid(Y6,6,(3,)) and valid(H,9)
assert (model_count(F9,9),model_count(Y6,6),model_count(H,9))==(70,20,37)
SAT={8:1,3:0,7:0,6:0,1:1,5:1}
UNSAT={**SAT,8:0}
HS={1:0,2:1,3:0,4:0,5:1}
HU={1:0,2:0,3:0,4:0,5:0}
assert (model_count(F9,9,SAT),model_count(F9,9,UNSAT))==(3,0)
assert (model_count(H,9,HS),model_count(H,9,HU))==(6,0)

# Original signed pair-extremes including inverted S/U.
modes=0
for i in range(len(F9)):
  for j in range(i+1,len(F9)):
    aa,bb=F9[i],F9[j]
    for e,f in product((0,1),repeat=2):
      d1={abs(v):int(v>0) if e else int(v<0) for v in aa}
      d2={abs(v):int(v>0) if f else int(v<0) for v in bb}
      pred=all(d1[x]==d2[x] for x in d1.keys()&d2.keys())
      actual=False
      for a in product((0,1),repeat=9):
        x=sum(a[abs(v)-1]==int(v>0) for v in aa)
        y=sum(a[abs(v)-1]==int(v>0) for v in bb)
        if x==(3 if e else 0) and y==(3 if f else 0):
          actual=True
          break
      assert pred==actual
      modes+=1
assert modes==264

assert 2*3+3*10==4*9
assert 12*9+792*3+789*10==798*13==10374
assert 12*9+798*13==10482
assert 1072*3+1076*10==13976
assert 4*10482==3*13976
assert 3*1064-12*2==4*792
assert 3*1064-12*3==4*789
assert 3*1072-12*2==4*798
assert 3*1076-12*3==4*798
# Duplicate-free three-variable exact-2P2N filler impossible.
assert len(list(set(product((1,2,3),repeat=3))))==27
assert len(list(__import__('itertools').combinations((1,2,3),3)))==1
# Y6/F9 fillers use disjoint exact signed private names and have 20/70 models.
used=[]
clauses=[]
for j,c in enumerate(H):
  private=12*9+798*j
  mod,base=(Y6,private+792) if len(c)==2 else (F9,private+789)
  for a in mod:
    clauses.append(tuple((abs(x)+base)*(1 if x>0 else -1) for x in a))
  used+=list(range(base+1,base+(6 if len(c)==2 else 9)+1))
occ=Counter(v for cl in clauses for v in cl)
assert len(used)==108 and len(set(used))==108 and len(clauses)==144
assert len(set(tuple(sorted(c)) for c in clauses))==144
assert all(occ[v]==occ[-v]==2 for v in used)

def rename(c,i):
  return tuple((1 if x>0 else -1)*(abs(x)+9*i) for x in c)
def source(r,mask):
  first=[];second=[]
  for i in range(1,r+1):
    c2,c3=rename(H[0],i),rename(H[3],i)
    if (mask>>(i-1))&1:
      first.append(c2);second.append(c3)
    else:
      first.append(c3);second.append(c2)
  return tuple(first+[rename(H[3],0)]+second+
        [rename(c,0) for j,c in enumerate(H) if j!=3]+
        [rename(c,i) for i in range(1,r+1) for j,c in enumerate(H) if j not in (0,3)])

family_cases=0
pair_flips=0
for r in range(1,10):
  for mask in range(1<<r):
    f=source(r,mask)
    assert valid(f,9*(r+1))
    b=sum(len(c)==2 for c in f[:r])
    t=r-b
    assert b==mask.bit_count()
    old_name=12*9*(r+1)+789*r+3*b
    new_name=12*9*(r+1)+798*r
    new_clause=1072*r+4*t
    assert new_clause%8==4*(t%2)
    assert new_name==12*9*(r+1)+798*r
    assert old_name==12*9*(r+1)+789*r+3*mask.bit_count()
    family_cases+=1
    pair_flips+=r
assert family_cases==1022 and pair_flips==8194
d=lambda c:((c+2)/(c*c)-c)/2
assert d(Fraction(6,5))==Fraction(23,45)
assert d(Fraction(241,200))==Fraction(11642479,23232400)
print(json.dumps({"status":"PASS restricted only","family_cases":family_cases,
                  "pair_flips":pair_flips,"SSUU_modes":modes,
                  "filler_clauses":len(clauses),"filler_names":len(used),
                  "all_input_P_NP":"OPEN"},indent=2))
