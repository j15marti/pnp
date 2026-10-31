#!/usr/bin/env python3
"""Independent finite check of the cofactor-tree original-source certificate partition.
No imports from the producer. Run with --source NAME to chunk by source.
"""
import json,math,itertools,collections,argparse,pathlib,hashlib
P=pathlib.Path(__file__).with_name('raw.json')
DATA=json.loads(P.read_text())

def checked(case_name,case):
 F=[tuple(c) for c in case['source_clauses']];n=case['n'];M=1<<n
 assert all(len(c)==len(set(abs(x) for x in c)) and all(x!=0 for x in c) for c in F)
 for j,c in enumerate(F,1):
  if case['S_U']['applicable']:
   assert len(c)==3
   target=case['S_U']['per_clause_targets'][j-1]
   assert target['j']==j
   for v in target['signed_occurrences']:
    assert v['S']==v['invert_U_to_S'] and v['U']==v['invert_S_to_U'] and v['S']+v['U']==1
 for pair in case['S_U'].get('pair_matrix',[]):
  j,k=pair['clauses'];same=opp=False
  for u in set(abs(x) for x in F[j-1])&set(abs(x) for x in F[k-1]):
   a=next(x for x in F[j-1] if abs(x)==u);b=next(x for x in F[k-1] if abs(x)==u)
   same|=a*b>0;opp|=a*b<0
  assert pair['same']==same and pair['opposite']==opp
  assert pair['SS_SU_US_UU']==[int(not opp),int(not same),int(not same),int(not opp)]
 models=0
 if n>16:
  assert case['canonical_witness'] and all(any(case['canonical_witness'][str(abs(x)) if str(abs(x)) in case['canonical_witness'] else abs(x)]==int(x>0) for x in c) for c in F)
 for mask in range(M if n<=16 else 0):
  a=lambda v:(mask>>(v-1))&1
  sat=all(any(a(abs(x))==int(x>0) for x in c) for c in F)
  models+=sat
  if case['S_U']['applicable']:
   for j,c in enumerate(F):
    assert sum(a(abs(x))==int(x>0) for x in c)+sum((1-a(abs(x)))==int(x>0) for x in c)==3
 assert case['complete_model_count'] in (None,models) if n<=16 else case['complete_model_count'] is None
 checks=0;alls=[]
 for limit,row in case['thresholds'].items():
  seen=bytearray(M if n<=16 else 0);kind_at=[None]*(M if n<=16 else 0);leaves=row['all_leaf_records'];mass=collections.Counter();correct=0
  for e in leaves:
   a={int(k):v for k,v in e['vars'].items()};depth=e['depth'];kind=e['kind']
   assert len(a)==depth
   if kind=='P':
    j=e['reason']-1
    assert 0<=j<len(F) and all(abs(x) in a and a[abs(x)]!=int(x>0) for x in F[j])
   elif kind=='S':
    assert all(any(abs(x) in a and a[abs(x)]==int(x>0) for x in c) for c in F)
   else:
    assert kind=='E'
    R=[tuple(x for x in c if abs(x) not in a) for c in F if not any(abs(x) in a and a[abs(x)]==int(x>0) for x in c)]
    assert [tuple(c) for c in e['residual']]==R and len(R)<=int(limit)
    w=max(1,math.ceil(math.log2(n+1)))
    assert e['child_bits']==2*w+sum(3+len(c)*(w+1) for c in R)
   mass[kind]+=1<<(n-depth)
   free=[v for v in range(1,n+1) if v not in a]
   for bits in itertools.product((0,1),repeat=len(free)) if n<=16 else []:
    m=sum((a.get(i,0) if i in a else bits[free.index(i)])<<(i-1) for i in range(1,n+1))
    assert seen[m]==0,('overlap',case_name,limit,m)
    seen[m]=1;kind_at[m]=kind
    is_sat=all(any(((m>>(abs(x)-1))&1)==int(x>0) for x in c) for c in F)
    if kind=='P':assert not is_sat
    if kind=='S':assert is_sat
    if kind=='E':
     assert is_sat==all(any(((m>>(abs(x)-1))&1)==int(x>0) for x in c) for c in R)
    checks+=1
  if n<=16: assert all(seen),('incomplete',case_name,limit)
  else:
   def compatible(a,b):return all(v not in b or b[v]==val for v,val in a.items())
   for i,e in enumerate(leaves):
    for f in leaves[i+1:]:assert not compatible({int(v):a for v,a in e['vars'].items()},{int(v):a for v,a in f['vars'].items()})
  assert sum(mass.values())==M
  assert mass['P']==row['pruned_volume'] and mass['S']==row['sat_terminal_volume'] and mass['E']==row['child_volume']
  assert len(leaves)==row['total_leaves']
  if row['tstar'] is not None:
   assert all(e['depth']>=row['tstar'] for e in leaves if e['kind']=='E')
  alls.append({'limit':int(limit),'leaves':len(leaves),'pruned_bits':mass['P'],'sat_bits':mass['S'],'child_bits':mass['E'],'enumerated_complete_assignments_checked':checks})
 return {'name':case_name,'n':n,'m':len(F),'models':models,'thresholds':alls}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--source',default=None);args=ap.parse_args()
 cases=DATA['sources']; names=[args.source] if args.source else sorted(cases)
 out=[checked(k,cases[k]) for k in names]
 print(json.dumps({'id':'ARC-BRANCH-MASS-GATE261_INDEPENDENT','source':args.source,'verified':out},indent=2))
if __name__=='__main__':main()
