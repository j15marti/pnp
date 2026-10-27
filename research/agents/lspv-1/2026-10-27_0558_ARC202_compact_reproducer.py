#!/usr/bin/env python3
"""ARC202: reproducible W1 exact22 / zero-observation / indexed-probe controls.
Standard library only. All tests exhaustive on stated finite parameters.
"""
import itertools,collections,json
W=((-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
   (5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),
   (-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),
   (2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14))
A=((6,0),(11,0)); B=((17,2),(9,2))
def H(a,b):
 f=[list(c) for c in W]
 for changed,locs in ((not a,A),(not b,B)):
  if changed:
   for i,j in locs:f[i][j]*=-1
 return tuple(map(tuple,f))
def sat(f,x):return all(any(bool(x>>(abs(v)-1)&1)==(v>0) for v in c) for c in f)
def source(y):
 m=len(y); groups=[H(v,1) for v in y];out=[]
 for js in ((6,11),tuple(j for j in range(20) if j not in (6,11,9,17)),(9,17)):
  for i,f in enumerate(groups):
   for j in js:out.append(tuple((abs(v)+15*i)*(1 if v>0 else -1) for v in f[j]))
 return out
def module(f,m,i):
 out=[];fixed=[j for j in range(20) if j not in (6,11,9,17)]
 for j in range(20):
  pos=(2*i+(0 if j==6 else 1) if j in (6,11) else
       18*m+2*i+(0 if j==9 else 1) if j in (9,17) else
       2*m+16*i+fixed.index(j))
  out.append(tuple((abs(v)-15*i)*(1 if v>0 else -1) for v in f[pos]))
 return tuple(out)
counts={};checks=0
for a,b in itertools.product((0,1),repeat=2):
 f=H(a,b);seen=collections.Counter()
 for clause in f:
  assert len(set(map(abs,clause)))==3
  for v in clause:seen[(abs(v),v>0)]+=1
 assert len(set(f))==20 and all(seen[(i,p)]==2 for i in range(1,16) for p in (0,1))
 counts[str(a)+str(b)]=sum(sat(f,x) for x in range(32768));checks+=32769
assert counts=={'00':772,'01':272,'10':272,'11':0}
rows=[]
for m in range(1,9):
 for y in itertools.product((0,1),repeat=m):
  f=source(y);seen=collections.Counter()
  for clause in f:
   assert len(set(map(abs,clause)))==3
   for v in clause:seen[(abs(v),v>0)]+=1
  assert all(seen[(i,p)]==2 for i in range(1,15*m+1) for p in (0,1))
  assert all((module(f,m,i)==H(1,1))==bool(y[i]) for i in range(m))
  # Matching 20 actual source clauses implies UNSAT, independent of other clauses.
  assert any(module(f,m,i)==H(1,1) for i in range(m))==any(y)
  # Proof ignored: zero-observation verifier on this canonical promise.
  assert (not any(module(f,m,i)==H(1,1) for i in range(m)))==(not any(y))
  checks+=4+m
  if not any(y):
   for i in range(m):
    alt=[0]*m;alt[i]=1;g=source(alt)
    diff=[(j,k) for j in range(len(f)) for k in range(3) if f[j][k]!=g[j][k]]
    assert len(diff)==2 and all(j<2*m for j,k in diff)
    checks+=1
 rows.append({'m':m,'inputs':2**m,'SAT':1,'UNSAT':2**m-1,
              'witness_proof_bits':(m-1).bit_length(),
              'SAT_allzero_indexed_probe_floor':m})
print(json.dumps({'run':'ARC202','status':'COMPUTATIONAL finite controls',
 'seed':None,'model_counts':counts,'validation_units':checks,
 'failures':0,'rows':rows,'limitation':'Promise query lower bound, not all-SAT lower bound'},
 sort_keys=True,indent=2))
