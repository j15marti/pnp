#!/usr/bin/env python3
"""Independent bitmask verifier for ARC-FRACTIONAL-ODD-CYCLE298.
No import of the producer; full original canonical clause list.
"""
import itertools,json
from collections import Counter
F=((1,2,6),(2,3,7),(3,4,8),(4,5,9),(1,5,10),
   (-1,-3,-11),(-1,-4,-12),(-2,-4,-13),(-2,-5,-14),(-3,-5,-15),
   (6,11,12),(7,12,13),(8,13,14),(9,14,15),(10,15,11),
   (-11,-6,-7),(-12,-7,-8),(-13,-8,-9),(-14,-9,-10),(-15,-10,-6))
Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),
    (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
def hit(m,c):
 return any(((m>>(abs(l)-1))&1)==int(l>0) for l in c)
def check_grammar(A,n):
 h=Counter(l for c in A for l in c)
 return (3*len(A)==4*n and n%3==0 and
    len({tuple(sorted(c)) for c in A})==len(A) and
    all(len(c)==3 and len({abs(l) for l in c})==3 and
        (all(l>0 for l in c) or all(l<0 for l in c)) for c in A) and
    all(h[i]==2 and h[-i]==2 for i in range(1,n+1)))
def source_partial(mask,p):
 return all(v==-1 or ((mask>>i)&1)==v for i,v in enumerate(p))
def independent_residual(p):
 r={}
 for j,c in enumerate(F,1):
  if any(p[abs(l)-1]==int(l>0) for l in c):continue
  r[j]=tuple(l for l in c if p[abs(l)-1]==-1)
 return r
def verified_fractional_bound(p):
 r=independent_residual(p)
 edges={tuple(sorted(map(abs,c))):j for j,c in r.items() if len(c)==2}
 vv=range(1,6)
 triangles=[v for v in itertools.combinations(vv,3)
            if all(pair in edges for pair in itertools.combinations(v,2))]
 counts=Counter()
 for v in triangles:
  for pair in itertools.combinations(v,2):counts[edges[pair]]+=1
 assert max(counts.values())<=3
 return len(triangles),(len(triangles)+2)//3
def main():
 assert check_grammar(F,15) and check_grammar(Y6,6)
 assert not check_grammar(F[:-1],15) and not check_grammar(F+((1,2,3),),15)
 models={a for a in range(1<<15) if all(hit(a,c) for c in F)}
 assert len(models)==770
 for m in range(1<<15):
  z=((1<<15)-1)^m
  for c in F:
   assert sum(((m>>(abs(l)-1))&1)==int(l>0) for l in c)+sum(
       ((z>>(abs(l)-1))&1)==int(l>0) for l in c)==3
 p0=(-1,)*5+(0,)*5+(1,)*5
 p1=(-1,)*5+(1,0,0,0,0)+(1,1,1,1,0)
 assert not any(source_partial(a,p0) for a in models)
 satmodels=[a for a in models if source_partial(a,p1)]
 assert len(satmodels)==2
 for x in (1,2,3,5):
  forced=0 if x in (1,2) else 1
  assert all(((a>>(x-1))&1)==forced for a in satmodels)
 assert verified_fractional_bound(p0)==(10,4)
 assert verified_fractional_bound(p1)==(4,2)
 for i in range(10):
  p=list(p0);p[i+5]^=1;p=tuple(p)
  assert verified_fractional_bound(p)==(7,3)
  assert not any(source_partial(a,p) for a in models)
 for j,k in itertools.combinations(range(20),2):
  v=sorted(set(map(abs,F[j]+F[k])))
  for (s,t) in ((1,1),(1,0),(0,1),(0,0)):
   demand=[]
   for c,z in ((F[j],s),(F[k],t)):
    demand.extend((abs(l),int(l>0) if z else int(l<0)) for l in c)
   local=all(len({val for key,val in demand if key==x})==1 for x in v)
   oracle=any(all(a[v.index(abs(l))]==(int(l>0) if z else int(l<0))
                 for c,z in ((F[j],s),(F[k],t)) for l in c)
              for a in itertools.product((0,1),repeat=len(v)))
   assert local==oracle
 pairs=list(itertools.combinations(range(5),2))
 assert max(sum(((a>>i)&1)!=((a>>j)&1) for i,j in pairs)
            for a in range(32))==6
 # Independent complete small Y6 SAT and UNSAT partial-state check.
 ym=[a for a in range(64) if all(hit(a,c) for c in Y6)]
 assert len(ym)==20
 label=Counter()
 for p in itertools.product((-1,0,1),repeat=6):
  label[any(source_partial(a,p) for a in ym)]+=1
 assert label=={True:529,False:200}
 out={'status':'PASS','independent':True,'full_models':len(models),
      'pair_modes_verified':760,'complement_clause_checks':655360,
      'K5_maxcut':6,'fractional_K5_ceil':4,'radius_one_UNSAT_states':11,
      'SAT_pin_models':len(satmodels),'Y6_SAT_partial':529,
      'Y6_UNSAT_partial':200,'U198_V198':'previously certified, not replayed'}
 print(json.dumps(out,sort_keys=True,indent=2))
if __name__=='__main__':main()
