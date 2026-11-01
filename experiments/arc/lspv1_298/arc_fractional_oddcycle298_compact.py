#!/usr/bin/env python3
"""ARC-FRACTIONAL-ODD-CYCLE298: canonical K5 source and exact fractional
odd-cycle budget. Stdlib compact reproducibility. Offline finite audit,
not a universal SAT algorithm or a native FLMV TM measurement.
"""
import itertools, json
from collections import Counter,defaultdict
from fractions import Fraction

P=((1,2),(2,3),(3,4),(4,5),(1,5))
Q=tuple(e for e in itertools.combinations(range(1,6),2) if e not in P)
F=tuple((u,v,6+i) for i,(u,v) in enumerate(P))+tuple(
 (-u,-v,-11-i) for i,(u,v) in enumerate(Q))+tuple(
 (6+i,11+i,11+(i+1)%5) for i in range(5))+tuple(
 (-(11+i),-(6+i),-(6+(i+1)%5)) for i in range(5))
PU=(-1,)*5+(0,)*5+(1,)*5
PS=(-1,)*5+(1,0,0,0,0)+(1,1,1,1,0)

def grammar(A,n):
 h=Counter(v for c in A for v in c)
 return (n%3==0 and 3*len(A)==4*n and
   len(set(tuple(sorted(c)) for c in A))==len(A) and
   all(len(c)==3 and len(set(map(abs,c)))==3 and
       (all(x>0 for x in c) or all(x<0 for x in c)) for c in A)
   and all(h[i]==h[-i]==2 for i in range(1,n+1)))

def sat(a):
 return all(any(a[abs(x)-1]==int(x>0) for x in c) for c in F)

def residual(p):
 r={};covered=[]
 for j,C in enumerate(F,1):
  if any(p[abs(x)-1]==int(x>0) for x in C):
   covered.append(j)
  else:r[j]=tuple(x for x in C if p[abs(x)-1]<0)
 return r,covered

def cert(p,mode):
 r,_=residual(p)
 E={tuple(sorted(map(abs,c))):j for j,c in r.items() if len(c)==2}
 triangles=[]
 for v in itertools.combinations(range(1,6),3):
  edges=list(itertools.combinations(v,2))
  if all(x in E for x in edges):
   triangles.append((v,[E[x] for x in edges]))
 if mode=="fractional":
  return [(v,ids,Fraction(1,3)) for v,ids in triangles]
 chosen=[];used=set()
 for v,ids in triangles:
  if not used.intersection(ids):
   chosen.append((v,ids,Fraction(1)))
   used.update(ids)
   if len(chosen)==2:break
 assert len(chosen)==2
 return chosen

def verify(p,proof):
 r,covered=residual(p)
 loads=defaultdict(Fraction);total=Fraction()
 for v,ids,w in proof:
  assert len(v)==3 and len(ids)==3 and len(set(ids))==3 and w>0
  assert {tuple(sorted(map(abs,r[j]))) for j in ids}==set(itertools.combinations(v,2))
  assert all(j in r and len(r[j])==2 for j in ids)
  for j in ids:loads[j]+=w
  total+=w
 assert all(value<=1 for value in loads.values())
 f=sum(x==-1 for x in p);u=len(r);e=2*f-u
 spill=Counter()
 for j in covered:
  for x in F[j-1]:
   if p[abs(x)-1]<0:spill[(abs(x),x>0)]+=1
 eta=sum(min(spill[(i,True)],spill[(i,False)]) for i in range(1,16) if p[i-1]<0)
 w={};preferred={}
 for i in range(1,16):
  if p[i-1]!=-1:continue
  pos=spill[(i,True)];neg=spill[(i,False)]
  if pos!=neg:
   w[i]=abs(pos-neg);preferred[i]=int(neg>pos)
 k=(total.numerator+total.denominator-1)//total.denominator
 return {'e':e,'eta':eta,'fractional':str(total),'ceil':k,
         'gap':e-eta-k,'preferred':preferred,'weights':w,
         'active_original_clause_ids':list(r)}

def dpll(p):
 counts=Counter()
 def rec(rho):
  counts['nodes']+=1
  rho=list(rho)
  while True:
   changed=False;all_hit=True
   for C in F:
    counts['clause_scans']+=1
    free=[];hit=False
    for lit in C:
     counts['literal_reads']+=1
     q=rho[abs(lit)-1]
     if q==int(lit>0):hit=True;break
     if q<0:free.append(lit)
    if hit:continue
    all_hit=False
    if not free:return False
    if len(free)==1:
     rho[abs(free[0])-1]=int(free[0]>0)
     counts['unit_assignments']+=1
     changed=True;break
   if not changed:break
  if all_hit:return True
  idx=rho.index(-1)
  for val in (0,1):
   child=rho.copy();child[idx]=val
   if rec(tuple(child)):return True
  return False
 answer=rec(p)
 return {'label':'SAT' if answer else 'UNSAT',**counts}

def main():
 assert grammar(F,15)
 assert not grammar(F[:-1],15) and not grammar(F+((1,2,3),),15)
 models=[a for a in itertools.product((0,1),repeat=15) if sat(a)]
 assert len(models)==770
 results={}
 for name,p,mode,expected in [('UNSAT',PU,'fractional',(-4,0)),
                               ('SAT',PS,'integral',(0,2))]:
  r=verify(p,cert(p,mode))
  count=sum(all(q<0 or a[i]==q for i,q in enumerate(p)) for a in models)
  assert (r['gap'],count)==expected
  base=dpll(p)
  assert base['label']==name
  if name=='SAT':
   assert r['preferred']=={1:0,2:0,3:1,5:1}
  results[name]={'budget':r,'models':count,'DPLL':base}
 radius=[]
 for i in range(-1,10):
  p=list(PU)
  if i>=0:p[5+i]^=1
  p=tuple(p)
  r=verify(p,cert(p,'fractional'))
  assert r['gap']<0 and (r['ceil'],r['e'])==((4,0) if i<0 else (3,1))
  assert not any(all(q<0 or a[j]==q for j,q in enumerate(p)) for a in models)
  radius.append({'flip_original_variable':None if i<0 else i+6,
                 'gap':r['gap'],'cycle_weight':r['fractional']})
 graph=list(itertools.combinations(range(5),2))
 cut=max(sum(((bits>>u)&1)!=((bits>>v)&1) for u,v in graph)
         for bits in range(32))
 assert cut==6
 # Original clause-level inversion and four-way exact extreme compatibility.
 for j,k in itertools.combinations(range(20),2):
  A=F[j];B=F[k]
  same=any(x in B for x in A);opposite=any(-x in B for x in A)
  predicted=[not opposite,not same,not same,not opposite]
  for (va,vb),expected in zip(((1,1),(1,0),(0,1),(0,0)),predicted):
   requirements={};possible=True
   for C,mode in ((A,va),(B,vb)):
    for l in C:
     v=int(l>0) if mode else int(l<0)
     if abs(l) in requirements and requirements[abs(l)]!=v:possible=False
     requirements[abs(l)]=v
   assert possible==expected
 counts={}
 for label,a in (('zero',(0,)*15),('one',(1,)*15)):
  hist=[0,0,0,0]
  for c in F:hist[sum(a[abs(x)-1]==int(x>0) for x in c)]+=1
  counts[label]=hist
 assert counts=={'zero':[10,0,0,10],'one':[10,0,0,10]}
 out={'status':'PASS','source_variables':15,'source_clauses':20,
      'complete_SAT_models':len(models),'cases':results,'radius_one_UNSAT':radius,
      'source_pair_modes_checked':190*4,'endpoint_histograms':counts,
      'K5_maxcut':cut,'K5_odd_edge_disjoint_max':2,
      'scope':'no uniform ARC compiler, no numerical FLMV transfer'}
 print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
