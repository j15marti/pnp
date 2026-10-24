#!/usr/bin/env python3
"""SELECTOR-SPLIT119 compact stand-alone source-coherent compiler audit.
All controls here have at most eight 3-literal clauses; no imported SAT labels.
The larger 198/264 benchmark and 162-case audit are in the conversation ZIP.
"""
import itertools,random,math,json
SEED=202610240912
R=random.Random(SEED)
checks=0
def ck(v):
 global checks
 checks+=1
 assert v
def sat_original(F,n):
 for a in itertools.product([0,1],repeat=n):
  if all(any(a[abs(z)-1]==(z>0) for z in C) for C in F):return a
 return None
def split(F,n):
 m=len(F)
 affine=[tuple(3*i+j for j in range(3)) for i in range(m)]
 binary=[]
 for i,C in enumerate(F):
  for j in range(3):
   for k in range(j+1,3):
    binary.append((-(3*i+j+1),-(3*i+k+1)))
   # selector implies source literal (positive or negative)
   binary.append((-(3*i+j+1),3*m+C[j] if C[j]>0 else -(3*m+abs(C[j]))))
 return affine,binary,3*m+n
def satisfies_split(aff,binary,z):
 return all(sum(z[i] for i in row)%2==1 for row in aff) and all(
  (z[abs(u)-1] if u>0 else not z[abs(u)-1]) or
  (z[abs(v)-1] if v>0 else not z[abs(v)-1]) for u,v in binary)
def selector_certificate(F,a):
 if a is None:return None
 y=[0]*(3*len(F))
 for i,C in enumerate(F):
  hit=next(j for j,z in enumerate(C) if a[abs(z)-1]==(z>0))
  y[3*i+hit]=1
 return tuple(y)+tuple(a)
def chosen_join(F):
 for choices in itertools.product(range(3),repeat=len(F)):
  required={};okay=True
  for i,j in enumerate(choices):
   z=F[i][j];v=abs(z);b=(z>0)
   if v in required and required[v]!=b:okay=False;break
   required[v]=b
  if okay:return True
 return False
def test(F,n):
 m=len(F)
 ck(m<=8 and all(len(set(abs(z) for z in C))==3 for C in F))
 A,B,dim=split(F,n)
 ck(len(A)==m and len(B)==6*m and dim==3*m+n)
 zz=[int(i%3==0) for i in range(3*m)]+[0]*n
 ck(all(sum(zz[i] for i in row)%2 for row in A))
 ck(all((not 0) for u,v in B)) # all selectors 0 satisfies every B clause
 model=sat_original(F,n)
 ck(bool(model is not None)==chosen_join(F))
 if model is not None:
  cert=selector_certificate(F,model)
  ck(satisfies_split(A,B,cert))
 return model is not None
def run():
 all8=[tuple(i+1 if bit else -(i+1) for i,bit in enumerate(bits))
       for bits in itertools.product([0,1],repeat=3)]
 cases=[(all8,3),(all8[:-1],3)]
 for k in range(65):
  n=R.choice([3,4,5]);m=R.randrange(2,9)
  F=[tuple(v if R.randrange(2) else -v for v in R.sample(range(1,n+1),3)) for _ in range(m)]
  cases.append((F,n))
 labels=[test(F,n) for F,n in cases]
 n,m=198,264
 w=math.ceil(math.log2(64*(n+m+1)))
 source=(4*m+2)*w
 W1=math.ceil(math.log2(64*(3*m+m+1)))
 W2=math.ceil(math.log2(64*(3*m+n+6*m+1)))
 child_a=(4*m+2)*W1
 child_b=(3*6*m+2)*W2
 assert (source,child_a,child_b)==(15870,17986,85572)
 print(json.dumps({'run':'SELECTOR-SPLIT119-compact','controls':len(cases),'sat':sum(labels),
                   'unsat':len(labels)-sum(labels),'assertions':checks,
                   'source_bits':source,'affine_bits':child_a,'binary_bits':child_b,
                   'warning':'Not an unrestricted SAT lower bound; U198 UNSAT not checked in compact audit.'},indent=2))
if __name__=='__main__':run()
