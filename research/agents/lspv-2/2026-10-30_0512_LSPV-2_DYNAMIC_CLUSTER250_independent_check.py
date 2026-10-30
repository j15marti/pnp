#!/usr/bin/env python3
"""Independent direct truth-table + parent-pivot resolution checker.
Does not import the producer or its dynamic algorithm. Standard library only.
"""
import sys,json,itertools,collections,math
p=sys.argv[1] if len(sys.argv)>1 else 'raw250_r3.json'
d=json.load(open(p));checked=collections.Counter()
for case in d['cases']:
 C=case['source_clauses'];n=case['n'];m=len(C);audit=case['source_extreme_audit']
 assert all(len(c)==3 and len(set(map(abs,c)))==3 for c in C)
 if case['strict22']:
  for i in range(1,n+1):
   assert sum(i in c for c in C)==2 and sum(-i in c for c in C)==2
  # A single connected cooccurrence component, not a disconnected product.
  g={i:set() for i in range(1,n+1)}
  for c in C:
   for i,j in itertools.combinations(map(abs,c),2):g[i].add(j);g[j].add(i)
  seen={1};q=[1]
  for i in q:
   for j in g[i]-seen:seen.add(j);q.append(j)
  assert len(seen)==n
 for j,rec in enumerate(audit['local_extremes_and_inverses'],1):
  assert rec['C_j']==j and rec['literals']==C[j-1]
  for l,s in zip(C[j-1],rec['S_occurrences']):
   assert s['literal']==l and s['occurrence']==f'x_{{{abs(l)},{j}}}'
   assert s['S']==int(l>0)==s['invert_U_is_S']
   assert s['U']==int(l<0)==s['invert_S_is_U']
   checked['signed_occurrence_targets']+=1
 for rec in audit['pair_modes']:
  A=C[rec['j']-1];B=C[rec['k']-1];vs=sorted(set(map(abs,A+B)))
  wanted={mode:False for mode in ('SS','SU','US','UU')}
  for z in itertools.product((0,1),repeat=len(vs)):
   a=dict(zip(vs,z));ta=sum(a[abs(l)]==(l>0) for l in A);tb=sum(a[abs(l)]==(l>0) for l in B)
   for mode in wanted:
    if ta==(3 if mode[0]=='S' else 0) and tb==(3 if mode[1]=='S' else 0):wanted[mode]=True
   checked['pair_combined_support_assignments']+=1
  assert rec['SS_SU_US_UU']==wanted
 for triple in audit['triple_modes']:
  ids=[k-1 for k in triple['original_clause_indices']]
  vs=sorted({abs(l) for j in ids for l in C[j]})
  for mode,expect in triple['modes'].items():
   valid=False
   for z in itertools.product((0,1),repeat=len(vs)):
    a=dict(zip(vs,z));t=[sum(a[abs(l)]==(l>0) for l in C[j]) for j in ids]
    if all(t[k]==(3 if mode[k]=='S' else 0) for k in range(3)):
     valid=True;break
   assert valid==expect;checked['triple_mode_verifications']+=1
 for key,states in audit['globally_coherent_endpoint_and_flip_trails'].items():
  old=None
  for v in states:
   a=v['a'];t=[sum(a[abs(l)-1]==(l>0) for l in c) for c in C]
   assert t==v['t_j']
   assert tuple(t.count(i) for i in range(4))==tuple(v['N0_N1_N2_N3'])
   if old is not None:
    i=v['flip_source_variable']-1
    assert sum(x!=y for x,y in zip(old,a))==1 and a[i]!=old[i]
   ac=[1-x for x in a];tbar=[sum(ac[abs(l)-1]==(l>0) for l in c) for c in C]
   assert tbar==[3-v for v in t]
   assert v['source_SAT']==(t.count(0)==0)
   checked['coherent_source_flip_states']+=1;old=a
 # Source-parent and intermediate derived resolution DAG is independently replayed.
 seen={f'C{j}':c for j,c in enumerate(C,1)}
 for node in audit['source_resolution_DAG']:
  A=seen[node['parent1']];B=seen[node['parent2']]
  q=node['pivot_literal_from_parent1']
  assert q in A and -q in B
  cl=sorted((set(A)-{q})|(set(B)-{-q}))
  assert len(cl)==len(set(cl)) and all(-x not in cl for x in cl)
  assert cl==node['clause']
  assert node['forbidden_original_variable_cube']=={str(abs(l)):int(l<0) for l in cl}
  if n<=15:
   pin=node['forbidden_original_variable_cube'];free=[i for i in range(1,n+1) if str(i) not in pin]
   # Any violating assignment of an entailed resolvent must violate some source clause.
   for z in itertools.product((0,1),repeat=len(free)):
    a={int(k):v for k,v in pin.items()};a.update(zip(free,z))
    assert not all(any(a[abs(l)]==(l>0) for l in c) for c in C)
    checked['proof_cube_extension_checks']+=1
  seen[node['id']]=cl;checked['resolution_DAG_nodes']+=1
 for event in case['dynamic_compiler']['coherent_flips']:
  a=event['global_base_assignment']
  base=[sum(a[abs(l)-1]==(l>0) for l in c) for c in C]
  assert tuple(base.count(i) for i in range(4))==tuple(event['global_base_N'])
  for k,table in event['all_exact_radius_histograms'].items():
   h=collections.Counter()
   for S in itertools.combinations(range(n),int(k)):
    b=a[:]
    for i in S:b[i]^=1
    t=[sum(b[abs(l)-1]==(l>0) for l in c) for c in C]
    h[','.join(map(str,(t.count(0),t.count(1),t.count(2),t.count(3))))]+=1
    checked['radius_masks']+=1
   assert dict(h)=={key:int(v) for key,v in table.items()}
   assert sum(h.values())==math.comb(n,int(k))
 checked['instances']+=1
 if n<=15:
  has_model=False
  for bits in itertools.product((0,1),repeat=n):
   if all(any(bits[abs(l)-1]==(l>0) for l in c) for c in C):has_model=True
   checked['full_source_assignments']+=1
  assert has_model==case['baseline_DPLL']['result']['sat']==case['hybrid_solver']['result']['sat']
 else:
  assert case['baseline_DPLL']['result']['sat']==case['hybrid_solver']['result']['sat']
  a=case['baseline_DPLL']['result']['witness'];assert a is not None
  assert all(any(a[abs(l)-1]==(l>0) for l in c) for c in C)
for ctl in d.get('width2_controls',[]):
 C=ctl['clauses'];n=ctl['n']
 assert all(len(c)<=2 and len(c)>=1 for c in C)
 models=[]
 for a in itertools.product((0,1),repeat=n):
  if all(any(a[abs(l)-1]==(l>0) for l in c) for c in C):models.append(a)
  checked['2SAT_full_assignments']+=1
 assert bool(models)==ctl['independent_full_oracle_sat']==ctl['decision']['sat']
 for j,r in enumerate(ctl['source_S_U_targets']):
  for l,item in zip(C[j],r['S_occurrences']):
   assert item['S']==int(l>0) and item['U']==int(l<0)
   checked['2SAT_signed_occurrences']+=1
 for p in ctl['source_SS_SU_US_UU_pair_modes']:
  A=C[p['j']-1];B=C[p['k']-1];vs=sorted(set(map(abs,A+B)))
  for mode,expect in p['SS_SU_US_UU'].items():
   got=False
   for z in itertools.product((0,1),repeat=len(vs)):
    a=dict(zip(vs,z));ta=sum(a[abs(l)]==(l>0) for l in A);tb=sum(a[abs(l)]==(l>0) for l in B)
    if ta==(len(A) if mode[0]=='S' else 0) and tb==(len(B) if mode[1]=='S' else 0):got=True
   assert got==expect
   checked['2SAT_pair_modes']+=1
print(json.dumps({'PASS':True,'source_file':sys.argv[1] if len(sys.argv)>1 else 'raw250_r3.json','checks':dict(checked)},indent=2))