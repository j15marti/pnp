#!/usr/bin/env python3
"""Independent verifier for 249 raw JSON. No producer import.
Validates every source-indexed signed S/U extreme and inversion, exhaustive
pair modes, actual coherent flips/complements, 1D/2D/4D radii, resolvents,
SAT witnesses and complete 15-variable UNSAT controls.
"""
import sys,json,itertools,math,collections,hashlib

def truth(lit,assignment):return assignment[abs(lit)] == (1 if lit>0 else 0)
def four(F,a):
 counts=[sum(truth(z,a) for z in c) for c in F]
 return tuple(counts.count(i) for i in range(4))
def allmodels(F,n):
 ct=0
 for values in itertools.product((0,1),repeat=n):
  a={i+1:v for i,v in enumerate(values)}
  ct+= (four(F,a)[0]==0)
 return ct

def main(path):
 data=json.load(open(path));stats=collections.Counter()
 for obj in data['cases']:
  F=tuple(tuple(c) for c in obj['source_CNF']); n=obj['source_n'];m=len(F)
  assert obj['source_sha256']==hashlib.sha256(str(F).encode()).hexdigest()
  assert obj['source_m']==m
  original={i:collections.Counter() for i in range(1,n+1)}
  for c in F:
   assert len(set(abs(x) for x in c))==len(c)
   for lit in c:original[abs(lit)][1 if lit>0 else -1]+=1
  balanced=all(v[1]==v[-1] for v in original.values())
  assert balanced==obj['balanced_formula']
  if obj['strict22']:assert all(v[1]==v[-1]==2 for v in original.values()) and all(len(c)==3 for c in F)
  for j,row in enumerate(obj['audit']['signed_occurrences'],1):
   assert row['source_clause_index']==j and tuple(row['signed_literals'])==F[j-1]
   for e,z in zip(row['occurrences'],F[j-1]):
    assert e['x_i_j']==[abs(z),j] and e['signed_source_literal']==z
    S=1 if z>0 else 0
    assert (e['S_j_all_literals_true'],e['invert_S_j_U_j'],e['U_j_all_literals_false'],e['invert_U_j_S_j'])==(S,1-S,1-S,S)
    stats['source_occurrences']+=1
  for pair in obj['audit']['pair_matrix']:
   j,k=[x-1 for x in pair['source_clause_pair']];C=F[j];D=F[k]
   signs={abs(z):int(z>0) for z in C};signd={abs(z):int(z>0) for z in D}
   shared=set(signs)&set(signd)
   same=sorted(i for i in shared if signs[i]==signd[i]);opp=sorted(i for i in shared if signs[i]!=signd[i])
   assert same==pair['same_polarity_shared'] and opp==pair['opposite_polarity_shared']
   pred={'SS':not opp,'SU':not same,'US':not same,'UU':not opp}
   got={a:False for a in pred};sats=False
   ids=sorted(set(signs)|set(signd))
   for vals in itertools.product((0,1),repeat=len(ids)):
    a=dict(zip(ids,vals));s=sum(truth(z,a) for z in C);t=sum(truth(z,a) for z in D)
    sats |= s>0 and t>0
    u=('S' if s==len(C) else 'U' if s==0 else 'M')+('S' if t==len(D) else 'U' if t==0 else 'M')
    if u in got:got[u]=True
    stats['coherent_pair_assignments']+=1
   assert got==pred==pair['SS_SU_US_UU']
   assert sats==pair['both_original_disjunctions_may_be_SAT']
   assert pair['forced_one_middle_clause']==(not any(got.values()))
   stats['source_clause_pairs']+=1
  for trail in obj['audit']['coherent_endpoint_and_flip_trails'].values():
   for state in trail:
    a={i:int(v) for i,v in enumerate(state['assignment'],1)}
    literal=[sum(truth(z,a) for z in c) for c in F]
    assert literal==state['per_original_clause_true_literal_counts']
    vec=four(F,a)
    assert list(vec)==state['N0_N1_N2_N3'] and (vec[0]==0)==state['original_formula_SAT']
    complement={i:1-v for i,v in a.items()};cvec=four(F,complement)
    assert list(cvec)==state['complement_N0_N1_N2_N3']
    if all(len(c)==3 for c in F):assert cvec==vec[::-1]
    if balanced and all(len(c)==3 for c in F):
     assert vec[1]==m//2-2*vec[0]+vec[3]
     assert vec[2]==m//2+vec[0]-2*vec[3]
    stats['coherent_flip_states']+=1
  for res in obj['audit']['source_parent_non_tautological_resolvents']:
   j,k=[x-1 for x in res['parent_indices']];p=res['pivot_original_variable'];clauses=[F[j],F[k]]
   assert any(p in c and -p in d for c,d in [tuple(clauses),tuple(reversed(clauses))])
   expected=set(z for c in clauses for z in c if abs(z)!=p)
   assert expected==set(res['resolvent']) and not any(-z in expected for z in expected)
   cube={int(i):int(v) for i,v in res['forbidden_original_variable_cube'].items()}
   assert all(not truth(z,cube) for z in expected)
   for b in itertools.product((0,1),repeat=n-len(cube)):
    a=dict(cube);a.update(dict(zip((i for i in range(1,n+1) if i not in cube),b)))
    assert four(F,a)[0]>0
    stats['forbidden_cube_extensions']+=1
  for tt in obj.get('radius_tests',[]):
   r=tt['radius'];anchor=tt['anchor'];cnt=collections.Counter()
   for bits in itertools.combinations(range(1,n+1),r):
    a={i:(anchor ^ int(i in bits)) for i in range(1,n+1)}
    cnt[four(F,a)]+=1
    stats['independent_radius_assignments']+=1
   hist={'/'.join(map(str,k)):v for k,v in sorted(cnt.items())}
   assert hist==tt['explicit']['histogram']==tt['two_coordinate']['histogram']==tt['four_coordinate']['histogram']
   marginal=collections.Counter()
   for key,v in hist.items():marginal[key.split('/')[0]]+=v
   assert dict(marginal)==tt['one_coordinate_SAT_only']['histogram']
   assert sum(v for vec,v in cnt.items() if vec[0]==0)==tt['one_coordinate_SAT_only']['sat_count_at_radius']
   assert sum(cnt.values())==math.comb(n,r)
  solver=obj['solver_baseline'];w=solver['witness']
  if w:
   a={i:int(z) for i,z in enumerate(w,1)}
   assert four(F,a)[0]==0
  else:
   for leaf in solver['UNSAT_conflict_leaves']:
    a=dict(leaf['branch_path'])
    # independently repeat saturation, not the producer's propagator
    while True:
     change=False;conflict=False
     for c in F:
      if any(abs(z) in a and truth(z,a) for z in c):continue
      unknown=[z for z in c if abs(z) not in a]
      if not unknown:conflict=True;break
      if len(unknown)==1:
       z=unknown[0];i=abs(z);value=int(z>0)
       if i in a and a[i]!=value:conflict=True;break
       if i not in a:a[i]=value;change=True
     if conflict:break
     assert change,'invalid supposed UP contradiction leaf'
    stats['unsat_source_refutation_leaves']+=1
  if n<=15 and obj['name'] in ('W1_STRICT22_UNSAT','S15_STRICT22_SAT','W1_SIGN_PERMUTATION'):
   ct=allmodels(F,n)
   assert (ct>0)==solver['SAT']
   stats['exhaustive_full_assignments']+=2**n
   print(obj['name'],'exact models',ct)
  stats['cases']+=1
 print('INDEPENDENT CHECK PASS',dict(stats))
 return stats
if __name__=='__main__':
 r=main(sys.argv[1]);json.dump({'status':'PASS','counts':dict(r)},open(sys.argv[2],'w'),indent=2)