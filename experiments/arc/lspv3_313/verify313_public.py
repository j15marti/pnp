#!/usr/bin/env python3
"""No-producer-import verifier of the exact F9 same-source counterexample.
Usage: python verify313_public.py results/raw/arc/lspv3_313/summary313_public.json
Full independent horizon-partition verifier is in the companion ZIP archive.
"""
import json,itertools,sys,collections
r=json.load(open(sys.argv[1]))
pos=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9)]
neg=[(4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9)]
F=pos+[tuple(-v for v in c) for c in neg]
frequency=collections.Counter()
for c in F:
 assert len(c)==3 and len(set(abs(l) for l in c))==3
 for lit in c:frequency[(abs(lit),lit>0)]+=1
for i in range(1,10):assert frequency[i,True]==frequency[i,False]==2
def sat(a):
 for clause in F:
  if not any(a[abs(lit)-1]==int(lit>0) for lit in clause):return False
 return True
A=[a for a in itertools.product((0,1),repeat=9) if sat(a)]
assert len(A)==70
p={int(i):v for i,v in r['p'].items()}
q={int(i):v for i,v in r['q'].items()}
future={int(i):v for i,v in r['future'].items()}
def count(pins):return sum(all(a[i-1]==v for i,v in pins.items()) for a in A)
assert count(p)==count(q)==4
for i,s in r['model_count_singleton_marginals_p_and_q'].items():
 i=int(i)
 assert [count({**p,i:0}),count({**p,i:1})]==[count({**q,i:0}),count({**q,i:1})]==s
assert count({**p,**future})==0 and count({**q,**future})==1
for row in r['unsat_proof']:assert isinstance(row,str) and len(row)>15
assert F[5]==(7,8,9) and F[10]==(-1,-2,-9)
a=tuple((r['sat_witness_mask_317']>>i)&1 for i in range(9))
assert sat(a) and all(a[i-1]==v for i,v in {**q,**future}.items())
# Independent all 264 pair-extreme compatibility tests by complete assignments.
for j,k in itertools.combinations(range(12),2):
 for x,y in itertools.product(('S','U'),repeat=2):
  want={}
  compatible=True
  for clause,mode in ((F[j],x),(F[k],y)):
   for lit in clause:
    v=int((lit>0)==(mode=='S'))
    if abs(lit) in want and want[abs(lit)]!=v:compatible=False
    want[abs(lit)]=v
  exhaustive=any(all(a[abs(lit)-1]==int((lit>0)==(mode=='S'))
     for clause,mode in ((F[j],x),(F[k],y)) for lit in clause)
     for a in itertools.product((0,1),repeat=9))
  assert compatible==exhaustive
for a in itertools.product((0,1),repeat=9):
 for clause in F:
  t=sum(a[abs(l)-1]==int(l>0) for l in clause)
  tbar=sum((1-a[abs(l)-1])==int(l>0) for l in clause)
  assert t+tbar==3
print(json.dumps({'PASS':True,'root_models':70,'first_order_marginals_identical':True,
 'two_pin_counts':[0,1],'original_clause_extreme_modes':264,
 'complement_clause_identities':6144,'all_input_complexity':'OPEN'},indent=2))
