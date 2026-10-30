#!/usr/bin/env python3
"""Independent original-source oracle for DERIVATIVE-WITNESS248 raw JSON; no producer imports."""
import sys,json,itertools,math,collections,hashlib

def truth(l,a):return int(a[abs(l)]==int(l>0))
def N4(F,a):
 t=[sum(truth(l,a) for l in c) for c in F]
 return [t.count(k) for k in range(4)]
def model(F,a):return N4(F,a)[0]==0

def main(path):
 D=json.load(open(path));stats=collections.Counter()
 for o in D['cases']:
  F=o['source_CNF'];n=o['n'];m=o['m'];r=o['r'];assert len(F)==m
  # Original signed occurrences are NOT independent variables.
  for row,c in zip(o['audit']['original_extreme_occurrences'],F):
   j=row['source_clause'];assert row['signed_literals']==c
   for z,entry in zip(c,row['occurrences']):
    assert entry['x_i_j']==[abs(z),j] and entry['sign']==(1 if z>0 else -1)
    assert (entry['S_literal_TRUE'],entry['S_inverted_U'],entry['U_literal_FALSE'],entry['U_inverted_S'])==(int(z>0),int(z<0),int(z<0),int(z>0))
    for p,q in [('S_j','invert_S_j_U_j'),('U_j','invert_U_j_S_j')]:
     assert row[p][str(abs(z))] + row[q][str(abs(z))]==1
    stats['signed_occurrences']+=1
  # Coherent clause pair modes exhaustively checked over shared original variables.
  for row in o['audit']['pair_modes']:
   j,k=[u-1 for u in row['source_pair']];test={q:False for q in ['SS','SU','US','UU']}
   scope=sorted({abs(z) for z in F[j]+F[k]})
   for bits in itertools.product((0,1),repeat=len(scope)):
    a=dict(zip(scope,bits));tj=sum(truth(z,a) for z in F[j]);tk=sum(truth(z,a) for z in F[k]);
    p='S' if tj==len(F[j]) else 'U' if tj==0 else 'M'
    q='S' if tk==len(F[k]) else 'U' if tk==0 else 'M'
    if p+q in test:test[p+q]=True
    stats['pair_assignments']+=1
   assert test==row['SS_SU_US_UU']
   stats['source_pairs']+=1
  # All recorded full endpoint, incremental flip and complement states.
  for trail in o['audit']['coherent_endpoints_and_flip_trails'].values():
   for state in trail:
    a={i:int(ch) for i,ch in enumerate(state['assignment'],1)}
    assert [sum(truth(z,a) for z in c) for c in F]==state['per_original_clause_t']
    assert N4(F,a)==list(state['N0_N1_N2_N3'])
    assert model(F,a)==state['source_SAT']
    b={i:1-v for i,v in a.items()}
    na=N4(F,a);nb=N4(F,b)
    assert nb==na[::-1]
    stats['flip_complement_states']+=1
  R=o['audit']['source_parent_prohibited_cube']
  if R:
   j,k=[i-1 for i in R['parent_clause_indices']];pivot=R['pivot'];rr=R['resolvent'];cube={int(i):v for i,v in R['prohibited_cube'].items()}
   assert any(pivot==abs(z) for z in F[j]) and any(pivot==abs(z) for z in F[k])
   assert pivot not in cube and all(truth(z,cube)==0 for z in rr)
   for bits in itertools.product((0,1),repeat=n-len(cube)):
    a=dict(cube);a.update(dict(zip((i for i in range(1,n+1) if i not in cube),bits)))
    assert not model(F,a)
    stats['forbidden_cube_extensions']+=1
  # Exact all-radius-r ground truth, including every derivative at every selected prefix.
  base={i:0 for i in range(1,n+1)};solutions=[];vectors=collections.Counter()
  for S in itertools.combinations(range(1,n+1),r):
   a={i:int(i in S) for i in range(1,n+1)};N=tuple(N4(F,a));vectors[N]+=1
   if N[0]==0:solutions.append(set(S))
   stats['radius_assignments']+=1
  assert len(solutions)==o['target_count']==o['oracle_target_count']
  assert len(vectors)==o['radius_hist_distinct_vectors']
  assert {'/'.join(map(str,k)):v for k,v in vectors.items()}==o['radius_hist_counts']
  grads={str(i):sum(i in S for S in solutions) for i in range(1,n+1)}
  assert grads==o['gradient_by_original_variable']
  for p in o['derivative_passes']:
   T=set(p['selected_before']);selected_count=sum(T<=S for S in solutions)
   possible=sorted(i for i in range(1,n+1) if i not in T and sum(T|{i}<=S for S in solutions)>0)
   assert selected_count==int(p['source_confirmed_target_extensions'])
   assert possible==p['positive_gradient_variables']
   stats['independent_derivative_prefixes']+=1
  chosen=o['selected_flips'];replay=o['replay_selected_flips']
  assert (chosen is None)==(not solutions)
  if chosen is not None:
   assert set(chosen) in solutions and set(replay) in solutions
   assert N4(F,{i:int(i in chosen) for i in range(1,n+1)})==list(o['selected_source_checked_witness']['original_clause_N4'])
  # Every solver's SAT/UNSAT answer independently checked on full finite space.
  sat_count=0
  for bits in itertools.product((0,1),repeat=n):
   if model(F,dict(zip(range(1,n+1),bits))):sat_count+=1
   stats['full_assignments']+=1
  assert (sat_count>0)==(o['baseline_witness'] is not None)
  assert o['complete_hybrid']['answer']==('SAT' if sat_count else 'UNSAT')
  if o['strict22']:
   count=collections.Counter(z for c in F for z in c)
   assert all(count[i]==count[-i]==2 for i in range(1,n+1))
   assert m*3==n*4
   stats['strict22_original_cases']+=1
  stats['cases']+=1
 # Independently evaluate ancillary 2SAT/Horn/affine labels.
 for row in D['ancillary_controls']:
  F=row['original_signed_clauses'];n=row['n'];models=sum(model(F,dict(zip(range(1,n+1),b))) for b in itertools.product((0,1),repeat=n))
  assert models==row['models'] and (models>0)==row['SAT']
  for v in row['recognition'].values():
   if v['applicable']:assert v['SAT']==(models>0)
  stats['ancillary_controls']+=1
 print(json.dumps({'PASS':True,'raw_sha256':hashlib.sha256(open(path,'rb').read()).hexdigest(),'checks':stats},indent=2))
if __name__=='__main__':main(sys.argv[1])