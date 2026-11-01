#!/usr/bin/env python3
"""Independent (no imports) adversarial finite control for saturated-cycle affine SAT.
F9 is canonical M22 and SAT globally, but the specified 6-pin cube is UNSAT.
Outside-cycle parity alone has a consistent solution which falsifies original C10.
"""
from itertools import product,combinations
from collections import Counter
from pathlib import Path
import json
POS=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
NEG=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
F=POS+tuple(tuple(-v for v in c) for c in NEG)
P={8:0,3:0,7:0,6:0,1:1,5:1}
CYCLE=(3,4,10)

def t(c,a):return sum(a[abs(v)]==(v>0) for v in c)
def SAT(a):return all(t(c,a)>=1 for c in F)
def all_assignments():
 for b in product((0,1),repeat=9):yield dict(enumerate(b,1))

def pack_parity(cycle_choice,a):
 # The external uncovered clauses (zero-based IDs 1 and 5) are units x2=1,x9=1.
 # Covered-occurrence imbalance additionally requires x4=1.
 if not (a[2]==a[4]==a[9]==1):return False
 for j in CYCLE:
  if j==cycle_choice:
   if t(F[j],a)!=2:return False
  else:
   if t(F[j],a)!=1:return False
 return True

def main():
 count=Counter((abs(l),l>0) for c in F for l in c)
 assert len(F)==12 and len({tuple(sorted(c)) for c in F})==12
 assert all(len(c)==3 and len({abs(v) for v in c})==3 and (all(v>0 for v in c) or all(v<0 for v in c)) for c in F)
 assert all(count[v,sgn]==2 for v in range(1,10) for sgn in (True,False))
 A=list(all_assignments());root_models=[a for a in A if SAT(a)]
 assert len(root_models)==70
 extensions=[a for a in A if all(a[v]==b for v,b in P.items())]
 assert len(extensions)==8
 assert sum(SAT(a) for a in extensions)==0
 # Original uncovered source IDs for p: 1,3,4,5,10. On this cube, the two
 # noncycle source clauses reduce to unit x2 and x9. Covered penalty forces x4=1.
 uncovered=[j for j,c in enumerate(F) if not any(abs(l) in P and P[abs(l)]==(l>0) for l in c)]
 assert uncovered==[1,3,4,5,10]
 assert all(len([l for l in F[j] if abs(l) not in P])==2 for j in CYCLE)
 assert len([a for a in extensions if a[2]==a[4]==a[9]==1])==1
 naive=next(a for a in extensions if a[2]==a[4]==a[9]==1)
 assert t(F[3],naive)==2 and t(F[4],naive)==2 and t(F[10],naive)==0
 assert all(not pack_parity(j,a) for j in CYCLE for a in extensions)
 # Full local S/U compatibility on every original clause pair, exact enumeration.
 pairs=0
 for j,k in combinations(range(len(F)),2):
  same={abs(x) for x in F[j]}&{abs(x) for x in F[k]}
  opposite=any((x>0)!=(next(z for z in F[k] if abs(z)==abs(x))>0) for x in F[j] if abs(x) in same)
  concordant=any((x>0)==(next(z for z in F[k] if abs(z)==abs(x))>0) for x in F[j] if abs(x) in same)
  for mode in product((0,3),repeat=2):
   feasible=any(t(F[j],a)==mode[0] and t(F[k],a)==mode[1] for a in A)
   predicted=(not opposite) if mode[0]==mode[1] else (not concordant)
   assert feasible==predicted,(j,k,mode,feasible,predicted)
   pairs+=1
 for b in (0,1):
  a={v:b for v in range(1,10)}
  c=Counter(t(x,a) for x in F)
  assert [c[k] for k in range(4)]==[6,0,0,6]
 assert pairs==264
 report={'target':'nine-variable canonical M22','valid':True,'global_SAT_models':70,'cube_pin':P,'cube_completions':8,'cube_SAT_models':0,'outside_affine_consistent':True,'selected_cycle_original_ids':list(CYCLE),'choice_count':3,'valid_choice_systems':0,'naive_parity_false_positive':True,'pair_extreme_checks':pairs,'endpoints':[6,0,0,6],'independent':True,'P_vs_NP':'OPEN'}
 path=Path(__file__).resolve().parent / 'verify_nine_var_parity_hole_results.json'
 path.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
 print(json.dumps(report,indent=2))


# Independent no-import positive-defect affine branch truth-table referee.
# Exactly the source F9 above is used. No producer function is imported.
P_S299={**P,1:0}
def check_positive299(F,p,dexpected):
 free=tuple(v for v in range(1,10) if v not in p)
 openids=[j for j,c in enumerate(F) if not any(abs(l) in p and p[abs(l)]==int(l>0) for l in c)]
 active={j:tuple(l for l in F[j] if abs(l) not in p) for j in openids}
 assert all(active.values())
 covered=[j for j in range(len(F)) if j not in openids]
 signed=Counter()
 for j in covered:
  for l in F[j]:
   if abs(l) in free:signed[l]+=1
 pref={x:(0 if signed[x]>signed[-x] else 1) for x in free if signed[x]!=signed[-x]}
 weights={x:abs(signed[x]-signed[-x]) for x in pref}
 eta=sum(min(signed[x],signed[-x]) for x in free)
 # This paired F9 SAT cube has no residual triangle, by independent inspection.
 edges=[(j,tuple(map(abs,r))) for j,r in active.items() if len(r)==2]
 cycles=[]
 for tri in combinations(edges,3):
  vertices={v for _,r in tri for v in r}
  if len(vertices)==3 and all(sum(v in edge for _,edge in tri)==2 for v in vertices):
   cycles.append(tuple(j for j,_ in tri))
 assert not cycles
 delta=2*len(free)-len(openids)-eta
 assert delta==dexpected
 groups=[]
 for j,r in active.items():
  options=[(0,[('xor',r,1)])]
  if len(r)==2:options.append((1,[('fix',l,1) for l in r]))
  if len(r)==3:
   for ix in range(3):options.append((1,[('fix',l,int(k!=ix)) for k,l in enumerate(r)]))
   options.append((2,[('fix',l,1) for l in r]))
  groups.append(options)
 for x,b in pref.items():
  groups.append([(0,[('fix',x,b)]),(weights[x],[('fix',x,1-b)])])
 def holds(a,rules):
  for typ,obj,val in rules:
   if typ=='fix' and a[abs(obj)]!= (val if obj>0 else 1-val):return False
   if typ=='xor' and sum(a[abs(l)] if l>0 else 1-a[abs(l)] for l in obj)%2!=val:return False
  return True
 got=Counter();examined=0
 def walk(i,left,rules):
  nonlocal examined
  if i==len(groups):
   if left:return
   examined+=1
   for vals in product((0,1),repeat=len(free)):
    a=dict(p);a.update(zip(free,vals))
    if holds(a,rules):
     assert SAT(a),('false SAT',a)
     got[vals]+=1
   return
  for cost,append in groups[i]:
   if cost<=left:walk(i+1,left-cost,rules+append)
 walk(0,delta,[])
 expected={}
 for vals in product((0,1),repeat=len(free)):
  a=dict(p);a.update(zip(free,vals))
  if SAT(a):expected[vals]=1
 assert dict(got)==expected,('overlap/omission',got,expected)
 return {'status':'PASS','source':'F9 canonical','delta':delta,
         'systems':examined,'SAT_extensions':len(expected),'unique_union':True}
def positive_main299():
 main()
 r=check_positive299(F,P_S299,2)
 print(json.dumps(r,indent=2,sort_keys=True))
if __name__=='__main__':positive_main299()
