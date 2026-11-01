#!/usr/bin/env python3
"""Standalone exact finite matching/UP/Krom controls, no external dependencies.
Proof status: known matching cut; finite reproducibility, P versus NP OPEN.
"""
import collections,itertools,json
Y=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
T=((1,2,4),(2,3,5),(1,3,6),(4,7,8),(5,7,9),(6,8,9),(-1,-2,-7),(-2,-3,-8),(-1,-3,-9),(-4,-5,-7),(-4,-6,-8),(-5,-6,-9))
def valid(f):
 n=max(abs(z) for c in f for z in c)
 t=collections.Counter(z for c in f for z in c)
 return (3*len(f)==4*n and len({tuple(sorted(c)) for c in f})==len(f)
  and all(len(c)==3 and len({abs(z) for z in c})==3 and (all(z>0 for z in c) or all(z<0 for z in c)) for c in f)
  and all(t[v]==t[-v]==2 for v in range(1,n+1)))
def residual(f,p):
 return [tuple(z for z in c if abs(z) not in p) for c in f
  if not any(abs(z) in p and p[abs(z)]==int(z>0) for z in c)]
def min_cover(req,free):
 if any(not q for q in req):return float('inf')
 for k in range(len(free)+1):
  for S in itertools.combinations(free,k):
   if all(set(S).intersection(q) for q in req):return k
 raise AssertionError('Original required clause lacks a free supporter')
def budget(f,p):
 n=max(abs(z) for c in f for z in c)
 free=[v for v in range(1,n+1) if v not in p]
 total=0
 for sign in (1,-1):
  req=[]
  for c in f:
   if c[0]*sign<0:continue
   if any(abs(z) in p and p[abs(z)]==int(z>0) for z in c):continue
   req.append([abs(z) for z in c if abs(z) not in p])
  total+=min_cover(req,free)
 return total>len(free)
def up(r):
 c=list(r);p={}
 while True:
  if any(not x for x in c):return False,c
  unit=next((x[0] for x in c if len(x)==1),None)
  if unit is None:return True,c
  v,b=abs(unit),int(unit>0)
  if v in p and p[v]!=b:return False,c
  p[v]=b
  c=[tuple(z for z in x if abs(z)!=v) for x in c if unit not in x]
def krom_sat(r):
 c=[x for x in r if len(x)<=2]
 vars=sorted({abs(z) for row in c for z in row})
 for bits in itertools.product((0,1),repeat=len(vars)):
  a=dict(zip(vars,bits))
  if all(any(a[abs(z)]==int(z>0) for z in row) for row in c):return True
 return False
def whole_sat(f):
 n=max(abs(z) for c in f for z in c)
 return sum(all(any(bits[abs(z)-1]==int(z>0) for z in row) for row in f)
  for bits in itertools.product((0,1),repeat=n))
def run(name,f):
 assert valid(f);n=max(abs(z) for c in f for z in c)
 k=collections.Counter()
 for trits in itertools.product((-1,0,1),repeat=n):
  p={j+1:v for j,v in enumerate(trits) if v>=0}
  r=residual(f,p)
  k['all_cubes']+=1
  if any(not x for x in r) or not budget(f,p):continue
  k['matching_cuts']+=1
  result,rr=up(r)
  if not result:k['already_UP']+=1
  elif not krom_sat(rr):k['already_Krom']+=1
  else:k['new_vs_UP_Krom']+=1
 assert k['new_vs_UP_Krom']==0
 return {'name':name,'satisfying_assignments':whole_sat(f),'cubes':dict(k)}
if __name__=='__main__':
 out={'Y6':run('Y6',Y),'TRI9':run('TRI9',T),
      'status':'Finite check only; matching cut known from GATE244; P versus NP OPEN'}
 assert out['Y6']['cubes']['matching_cuts']==12
 assert out['TRI9']['cubes']['matching_cuts']==829
 assert out['TRI9']['cubes']['already_UP']==828
 assert out['TRI9']['cubes']['already_Krom']==1
 print(json.dumps(out,indent=2,sort_keys=True))
