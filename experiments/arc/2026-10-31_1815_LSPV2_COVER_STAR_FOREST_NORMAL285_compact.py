#!/usr/bin/env python3
"""COVER-STAR-FOREST-NORMAL285: complete small-source independent check (stdlib)."""
import itertools,collections,json
Y=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
K=((1,2,3),(4,5,6),(7,8,9),(1,4,7),(2,5,8),(3,6,9),
   (-1,-5,-9),(-1,-6,-8),(-2,-4,-9),(-2,-6,-7),(-3,-4,-8),(-3,-5,-7))
def grammar(F):
 n=max(abs(z) for c in F for z in c)
 assert n%3==0 and len(F)==4*n//3
 assert len(set(tuple(sorted(c)) for c in F))==len(F)
 assert all(len(c)==3 and len({abs(z) for z in c})==3 and
            all((z>0)==(c[0]>0) for z in c) for c in F)
 p=collections.Counter((abs(z),z>0) for c in F for z in c)
 assert all(p[i,True]==p[i,False]==2 for i in range(1,n+1))
 return n
def sat(F,a):
 return all(any(a[abs(z)-1]==int(z>0) for z in c) for c in F)
def reduce_witness(F,w,to_zero):
 a=list(w);n=grammar(F);kept=[];rejected=[]
 for i in range(n):
  desired=1 if to_zero else 0
  if a[i]!=desired:continue
  supporting=[(j,c) for j,c in enumerate(F) if ((i+1) if to_zero else -(i+1)) in c]
  assert len(supporting)==2
  counts=[sum(a[abs(z)-1]==int(z>0) for z in c) for j,c in supporting]
  if min(counts)<2:
   rejected.append([i+1,supporting[counts.index(1)][0]+1]);continue
  before=[sum(a[abs(z)-1]==int(z>0) for z in c) for c in F]
  a[i]^=1
  after=[sum(a[abs(z)-1]==int(z>0) for z in c) for c in F]
  changed=[j+1 for j in range(len(F)) if before[j]!=after[j]]
  assert len(changed)==4 and sat(F,a)
  assert sum(((before[j-1]^(before[j-1]>>1))^(after[j-1]^(after[j-1]>>1))).bit_count() for j in changed)==4
  kept.append([i+1,changed])
 return a,kept,rejected
def audit(F,expected_models):
 n=grammar(F);models=[a for a in itertools.product((0,1),repeat=n) if sat(F,a)]
 assert len(models)==expected_models
 for a in models:
  low,_,_=reduce_witness(F,a,True)
  high,_,_=reduce_witness(F,a,False)
  assert sum(low)<=n//2 and sum(high)>=(n+1)//2
 return {'n':n,'models':len(models),'weights':sorted(set(map(sum,models)))}
if __name__=='__main__':
 y=audit(Y,20);k=audit(K,18)
 assert k['weights']==[4,5]
 print(json.dumps({'result':'PASS','Y6':y,'K33_9':k,'note':'full large-case independent source proof and physical traces in ZIP archive'},indent=2))