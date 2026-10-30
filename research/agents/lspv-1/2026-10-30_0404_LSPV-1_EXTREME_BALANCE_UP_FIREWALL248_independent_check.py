#!/usr/bin/env python3
"""Independent replay for EXTREME-BALANCE-UP-FIREWALL248.
No imports from the producer. Reads the producer's separate raw JSON outputs.
"""
import itertools,json,sys,collections

def value(l,mask):
 return ((mask//(2**(abs(l)-1)))%2)==(l>0)
def tvec(F,mask):return [sum(value(l,mask) for l in c) for c in F]
def mode_ok(c,d,a,b):
 vs=sorted({abs(z) for z in c+d})
 for assign in itertools.product((0,1),repeat=len(vs)):
  bits=dict(zip(vs,assign))
  xs=sum(bits[abs(x)]==int(x>0) for x in c)
  ys=sum(bits[abs(x)]==int(x>0) for x in d)
  if xs==(len(c) if a=='S' else 0) and ys==(len(d) if b=='S' else 0):return True
 return False

def check_source(src):
 n=src['n'];clauses=[tuple(rec['source_literals']) for rec in src['local_targets_original_clause_index']]
 assert src['m']==len(clauses)
 checked=collections.Counter()
 for j,rec in enumerate(src['local_targets_original_clause_index']):
  assert j==rec['source_clause_index']
  for p,row in enumerate(rec['signed_occurrences']):
   l=clauses[j][p]
   assert l==row['signed_literal']
   assert row['signed_occurrence']==f'x_{{{abs(l)},{j}}}'
   s=int(l>0)
   assert [row['S_local_all_true'],row['inverted_S_is_U'],row['U_local_all_false'],row['inverted_U_is_S']]==[s,1-s,1-s,s]
   checked['occurrences']+=1
 for pair in src['source_indexed_four_way_pair_compatibility']:
  i,j=pair['source_clause_indices']
  for mode,info in pair['four_modes'].items():
   assert info['feasible']==mode_ok(clauses[i],clauses[j],mode[0],mode[1])
   checked['pair_modes']+=1
 for a in [0,(1<<n)-1]:
  t=tvec(clauses,a)
  got=src['actual_global_all_zero'] if a==0 else src['actual_global_all_one']
  assert t==got['per_clause_true_counts']
  assert [t.count(r) for r in range(4)]==got['N0_N1_N2_N3']
  checked['endpoints']+=1
 for seq in src['partial_multiple_flip_trails']:
  for step in seq:
   st=step['status']
   assert st['per_clause_true_counts']==tvec(clauses,st['mask'])
   assert [tvec(clauses,st['mask'])[i] for i in range(len(clauses))]==[3-x for x in tvec(clauses,st['mask']^((1<<n)-1))]
   checked['global_flip_steps']+=1
 for cube in src['proved_forbidden_cubes']:
  a={int(x):v for x,v in cube['forbidden_original_variable_cube'].items()}
  p,q=cube['original_parent_indices'];v=cube['pivot_variable']
  for pivot in [0,1]:
   one=dict(a);one[v]=pivot
   for j in (p,q):
    if all(x in one for x in (abs(l) for l in clauses[j])):
     pass
   assert any(all(one[abs(l)]!=int(l>0) for l in clauses[j]) for j in (p,q))
   checked['forbidden_cube_pivot_replays']+=1
 satcount=0
 for mask in range(1<<n):
  ts=tvec(clauses,mask)
  if min(ts)>0:satcount+=1
  if n<=15 and ts!=[3-x for x in tvec(clauses,mask^((1<<n)-1))]:raise AssertionError('complement broken')
  checked['coherent_complete_assignments']+=1
 assert satcount==src['model_count_by_exhaustive_global_assignments']
 return dict(checked)

def check_tests(raw):
 assert not raw['violations']
 assert raw['converse_counterexample']['theta']<=raw['converse_counterexample']['budget']
 assert raw['converse_counterexample']['UP_refutes_immediately']
 assert raw['balanced_assumption_counterexample']['theta']>raw['balanced_assumption_counterexample']['unjustified_balanced_budget_m_times_k_minus2_div2']
 return {'partial_cubes':sum(c['count']['checked_partial_cubes'] for c in raw['balanced_partial_cube_tests']),
         'triggered':sum(c['count'].get('budget_triggered',0) for c in raw['balanced_partial_cube_tests']),
         'UP_closed_consistent':sum(c['count'].get('UP_closed_consistent',0) for c in raw['balanced_partial_cube_tests'])}

def check_bench(raw):
 for r in raw['runs_same_source']:
  a=r['baseline_complete_UP_DPLL'];b=r['same_DPLL_plus_conservation_after_UP']
  assert a['SAT']==b['SAT'] and a['nodes']==b['nodes']
  assert b.get('balance_rejections',0)==0
  assert a['selected_events']<=b['selected_events']
 return len(raw['runs_same_source'])

if __name__=='__main__':
 root=sys.argv[1] if len(sys.argv)>1 else '.'
 with open(f'{root}/audit_results.json') as fh:audit=json.load(fh)
 with open(f'{root}/test_results.json') as fh:tests=json.load(fh)
 with open(f'{root}/benchmark_results.json') as fh:bench=json.load(fh)
 out={'source_checks':{name:check_source(src) for name,src in audit['source_runs'].items()},
      'partial_cube_checks':check_tests(tests),'bench_cases':check_bench(bench)}
 print('INDEPENDENT CHECK PASS')
 print(json.dumps(out,indent=2,sort_keys=True))
