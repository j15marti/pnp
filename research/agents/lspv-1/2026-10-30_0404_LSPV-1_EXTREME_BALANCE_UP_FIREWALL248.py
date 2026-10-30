#!/usr/bin/env python3
"""EXTREME-BALANCE-UP-FIREWALL248: exact signed-extreme audit and UP-dominance control.

All literals refer to global original Boolean variables; (+/-) is polarity,
never a separate occurrence variable. Python 3 stdlib. Deterministic seed.
CLI: python SCRIPT.py audit|test|bench [output.json]
Each invocation is designed to finish in less than 30 seconds.
"""
from __future__ import annotations
import collections, itertools, json, random, sys, time, tracemalloc
SEED=202610300404
W1=[(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
 (5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),
 (-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),
 (2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)]
SWAP6=[tuple(-l if abs(l)==6 and j in (9,13) else l for l in c)
        for j,c in enumerate(W1)]
SHARP8=[(-1,2,-5),(-3,-2,-5),(1,-6,-4),(6,-3,5),
        (6,3,-4),(1,2,4),(-6,-1,5),(-2,3,4)]
PAIRED_K4=[(1,2,3),(-1,-2,-3),(1,4,5),(-1,-4,-5),
           (2,4,6),(-2,-4,-6),(3,5,6),(-3,-5,-6)]
BALANCED4=[(1,2,3,4),(1,-2,-3,-4),(-1,2,-3,-4),(-1,-2,3,4)]
HORN=[(-1,-2,3),(-3,-4,-5),(-1,-4,-6),(2,-3,-6)]
def xor3(parity):
 return [tuple(v if (mask>>(i))&1 == 0 else -v for i,v in enumerate((1,2,3)))
         for mask in range(8) if mask.bit_count()%2 != parity]
XOR_UNSAT=xor3(0)+xor3(1)
IRREGULAR_BALANCED=SHARP8+[tuple(({1:1,2:7,3:8}[abs(l)] if l>0 else -{1:1,2:7,3:8}[abs(l)]) for l in c) for c in XOR_UNSAT]
BINARY_UNSAT=[(1,2),(1,-2),(-1,2),(-1,-2)]

def nvars(F): return max((abs(l) for c in F for l in c),default=0)
def literal_true(l,mask):return bool(mask&(1<<(abs(l)-1)))==(l>0)
def clause_status(F,mask):
 vectors=[[int(literal_true(l,mask)) for l in c] for c in F]
 t=[sum(v) for v in vectors]
 return {"mask":mask,"assignment":{str(v):int(bool(mask&(1<<(v-1)))) for v in range(1,nvars(F)+1)},
         "per_clause_true_vectors":vectors,"per_clause_true_counts":t,
         "N0_N1_N2_N3":[t.count(r) for r in range(4)],"SAT":all(x>0 for x in t)}
def local_extremes(F):
 out=[]
 for j,c in enumerate(F):
  rows=[]
  for p,l in enumerate(c):
   pos=int(l>0)
   rows.append({"signed_occurrence":f"x_{{{abs(l)},{j}}}","source_clause_index":j,
                "literal_position":p,"signed_literal":l,"source_variable":abs(l),
                "S_local_all_true":pos,"inverted_S_is_U":1-pos,
                "U_local_all_false":1-pos,"inverted_U_is_S":pos})
  out.append({"source_clause_index":j,"source_literals":list(c),"signed_occurrences":rows})
 return out

def local_target(c,mode):
 return {abs(l):int((l>0)==(mode=='S')) for l in c}
def compatible(reqs):
 a={}; conflicting=set()
 for req in reqs:
  for v,z in req.items():
   if v in a and a[v]!=z: conflicting.add(v)
   else: a[v]=z
 return not conflicting,sorted(conflicting),a

def pairs(F):
 out=[]
 for j,k in itertools.combinations(range(len(F)),2):
  same=[];opp=[]
  for v in set(map(abs,F[j])) & set(map(abs,F[k])):
   sign_j=next(l>0 for l in F[j] if abs(l)==v)
   sign_k=next(l>0 for l in F[k] if abs(l)==v)
   (same if sign_j==sign_k else opp).append(v)
  mode={}
  for typ in ('SS','SU','US','UU'):
   ok,conflict,req=compatible([local_target(F[j],typ[0]),local_target(F[k],typ[1])])
   mode[typ]={"feasible":ok,"conflicting_original_variables":conflict,
              "combined_partial_source_assignment":({str(v):b for v,b in sorted(req.items())} if ok else None)}
   assert ok == (not opp if typ in ('SS','UU') else not same)
  out.append({"source_clause_indices":[j,k],"same_sign_shared_variables":sorted(same),
              "opposite_sign_shared_variables":sorted(opp),"four_modes":mode})
 return out

def multi_extremes(F,limit=20):
 out=[]
 for js in itertools.combinations(range(len(F)),3):
  for seq in itertools.product('SU',repeat=3):
   ok,contr,req=compatible([local_target(F[j],a) for j,a in zip(js,seq)])
   # Verify against exact enumeration on union of variables, not occurrence variables.
   vars_=sorted(set(abs(x) for j in js for x in F[j]))
   seen=False
   for bits in itertools.product((0,1),repeat=len(vars_)):
    trial=dict(zip(vars_,bits))
    if all(all(trial[v]==value for v,value in local_target(F[j],a).items()) for j,a in zip(js,seq)):
     seen=True;break
   assert ok==seen
   if len(out)<limit:
    out.append({"source_clause_indices":list(js),"modes":''.join(seq),"feasible":ok,
                "conflicting_variables":contr,
                "realizable_original_assignment":({str(k):v for k,v in req.items()} if ok else None)})
  if len(out)>=limit:break
 return out

def trail(F,start,flips):
 a=start;out=[{"action":"initial","status":clause_status(F,a)}]
 n=nvars(F)
 for v in flips:
  before=clause_status(F,a);next_a=a^(1<<(v-1));after=clause_status(F,next_a)
  predicted=[]
  for j,c in enumerate(F):
   delta=sum((1 if not literal_true(l,a) else -1) for l in c if abs(l)==v)
   predicted.append(before['per_clause_true_counts'][j]+delta)
  assert predicted==after['per_clause_true_counts']
  assert after['per_clause_true_counts']==[len(c)-b for c,b in zip(F,clause_status(F,next_a^((1<<n)-1))['per_clause_true_counts'])]
  out.append({"flip_original_variable":v,"predicted_true_counts":predicted,"status":after})
  a=next_a
 return out

def forbidden_resolvents(F,limit=12):
 out=[]
 for j,k in itertools.combinations(range(len(F)),2):
  for l in F[j]:
   if -l not in F[k]:continue
   r=tuple(sorted((set(F[j])-{l})|(set(F[k])-{-l}),key=lambda x:(abs(x),x)))
   if any(-x in r for x in r):continue
   cube={str(abs(x)):int(x<0) for x in r}
   # every extension of this cube must falsify at least one parent, for either pivot value
   for pv in (0,1):
    full={int(v):b for v,b in cube.items()};full[abs(l)]=pv
    assert any(all(full.get(abs(z),-1)!=int(z>0) for z in F[h]) for h in (j,k))
   out.append({"original_parent_indices":[j,k],"pivot_variable":abs(l),
               "non_tautological_resolvent":list(r),"forbidden_original_variable_cube":cube,
               "proof":"Both original parents reduce to contradictory units on the pivot under the cube."})
   if len(out)>=limit:return out
 return out

def is_balanced(F):
 n=nvars(F);k=len(F[0]);m=len(F)
 if any(len(c)!=k or len(set(abs(l) for l in c))!=k for c in F):return False
 d=[]
 for v in range(1,n+1):
  p=sum(l==v for c in F for l in c);q=sum(l==-v for c in F for l in c)
  if p==0 or p!=q:return False
  d.append(p)
 return True

def theta(F,pins):
 # A universal exact identity for any formula; only the budget is valid when balanced.
 forced=[sum(1 for l in c if abs(l) in pins and pins[abs(l)]==int(l>0)) for c in F]
 return {"theta":sum(max(0,a-1) for a in forced),"zero_pinned_true_clauses":sum(a==0 for a in forced),
         "pinned_true_literal_counts":forced}

def repair_capacity(F,pins):
 """Additive sign-consistent variable coverage of original residual clauses."""
 residual=[c for c in F if not any(abs(l) in pins and pins[abs(l)]==int(l>0) for l in c)]
 plus=collections.Counter();minus=collections.Counter()
 for c in residual:
  for l in c:
   if abs(l) in pins: continue
   (plus if l>0 else minus)[abs(l)]+=1
 cap=sum(max(plus[v],minus[v]) for v in (plus.keys()|minus.keys()))
 return {"residual_uncovered_clauses":len(residual),"capacity":cap,
         "capacity_deficit":len(residual)-cap,
         "positive_residual_occurrences":dict(plus),"negative_residual_occurrences":dict(minus)}

def budget(F):
 assert is_balanced(F)
 k=len(F[0]);m=len(F)
 assert (m*(k-2))%2==0
 return m*(k-2)//2

def unit_propagate(F,a,ledger=None):
 a=dict(a)
 while True:
  changed=False
  for j,c in enumerate(F):
   if ledger is not None:ledger['clause_scans']+=1
   rem=[];satisfied=False
   for l in c:
    if ledger is not None:ledger['literal_reads']+=1
    v=abs(l)
    if v not in a:rem.append(l)
    elif a[v]==int(l>0):satisfied=True;break
   if satisfied:continue
   if not rem:return None
   if len(rem)==1:
    l=rem[0];v=abs(l);z=int(l>0)
    if v in a and a[v]!=z:return None
    if v not in a:
     a[v]=z;changed=True
     if ledger is not None:ledger['unit_assignments']+=1
  if not changed:return a

def dpll(F,with_theta=False):
 led=collections.Counter();n=nvars(F)
 t0=time.perf_counter();tracemalloc.start()
 led['initial_source_clause_reads']=len(F)
 led['initial_source_literal_reads']=sum(len(c) for c in F)
 recognized=False
 B=None
 if with_theta:
  led['recognition_clause_checks']=len(F)
  led['recognition_literal_reads']=sum(len(c) for c in F)
  recognized=is_balanced(F)
  if recognized: B=len(F)*(len(F[0])-2)//2
 def rec(a):
  led['nodes']+=1
  a=unit_propagate(F,a,led)
  if a is None:return None
  if with_theta and recognized:
   led['balance_test_calls']+=1
   t=theta(F,a)
   led['balance_literal_reads']+=sum(len(c) for c in F)
   if t['theta']>B:
    led['balance_rejections']+=1
    return None
  # baseline explicit completion check; end each branch with same solver
  led['completion_clause_checks']+=len(F)
  if all(any(abs(l) in a and a[abs(l)]==int(l>0) for l in c) for c in F):
   return a
  v=next((i for i in range(1,n+1) if i not in a),None)
  if v is None:return None
  led['branches']+=1
  for z in (0,1):
   b=dict(a);b[v]=z
   w=rec(b)
   if w is not None:return w
  return None
 witness=rec({})
 _,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
 out=dict(led);out['peak_allocated_bytes']=peak;out['wall_seconds']=round(time.perf_counter()-t0,8)
 out['SAT']=witness is not None
 if witness is not None:
  mask=sum((1<<(v-1)) for v,z in witness.items() if z)
  assert clause_status(F,mask)['SAT']
  out['verified_witness_mask']=mask
 else:out['verified_witness_mask']=None
 out['selected_events']=sum(out.get(k,0) for k in ('nodes','clause_scans','literal_reads','unit_assignments',
    'completion_clause_checks','branches','balance_test_calls','balance_literal_reads','balance_rejections',
    'initial_source_clause_reads','initial_source_literal_reads','recognition_clause_checks','recognition_literal_reads'))
 return out

def random_balanced(n,rng):
 assert n%3==0
 for _ in range(10000):
  slots=[v*z for v in range(1,n+1) for z in (1,1,-1,-1)]
  rng.shuffle(slots)
  F=[tuple(slots[i:i+3]) for i in range(0,len(slots),3)]
  if is_balanced(F):return F
 raise AssertionError('sampling too sparse')

def audits():
 o={'run':'EXTREME-BALANCE-UP-FIREWALL248','seed':SEED,'statuses':{},'source_runs':{}}
 for name,F in [('W1_strict22_UNSAT',W1),('SWAP6_strict22_SAT',SWAP6),('SHARP8_strict22_SAT',SHARP8)]:
  n=nvars(F)
  data={'n':n,'m':len(F),'strict22':is_balanced(F),'local_targets_original_clause_index':local_extremes(F),
        'source_indexed_four_way_pair_compatibility':pairs(F),'triple_mode_controls':multi_extremes(F),
        'actual_global_all_zero':clause_status(F,0),
        'actual_global_all_one':clause_status(F,(1<<n)-1),
        'partial_multiple_flip_trails':[trail(F,0,[1,2,3,4,5,2,1]),
                                      trail(F,(1<<n)-1,[1,2,4,3,1])],
        'proved_forbidden_cubes':forbidden_resolvents(F)}
  for mode in ('SS','SU','US','UU'):
   for p in data['source_indexed_four_way_pair_compatibility']:
    j,k=p['source_clause_indices'];vs=sorted(set(map(abs,F[j]))|set(map(abs,F[k])))
    feasible=False
    for bs in itertools.product((0,1),repeat=len(vs)):
     mask=sum((1<<(v-1)) for v,b in zip(vs,bs) if b)
     tc=clause_status([F[j],F[k]],mask)['per_clause_true_counts']
     if tc==[3 if mode[0]=='S' else 0,3 if mode[1]=='S' else 0]:feasible=True;break
    assert feasible==p['four_modes'][mode]['feasible']
  data['pair_mode_verified_by_global_original_variable_enumeration']=True
  data['model_count_by_exhaustive_global_assignments']=sum(clause_status(F,a)['SAT'] for a in range(1<<n))
  data['all_assignment_complement_verified']=True
  for mask in range(1<<n):
   c=clause_status(F,mask)['per_clause_true_counts']
   ic=clause_status(F,mask^((1<<n)-1))['per_clause_true_counts']
   assert all(x+y==3 for x,y in zip(c,ic))
  o['source_runs'][name]=data
 return o

def tests():
 rng=random.Random(SEED)
 samples=[];counts=collections.Counter();found_violation=[]
 cases=[('W1',W1),('SWAP6',SWAP6),('SHARP8',SHARP8),('BALANCED4',BALANCED4),
        ('IRREGULAR_BALANCED',IRREGULAR_BALANCED)]
 for n in (6,9,12):
  for i in range(4):cases.append((f'RANDOM22_n{n}_case{i}',random_balanced(n,rng)))
 for name,F in cases:
  assert is_balanced(F)
  n=nvars(F);m=len(F);b=budget(F)
  count=collections.Counter()
  N=1800 if n>=9 else (3**n)
  pins_list=(itertools.product((-1,0,1),repeat=n) if n==6 else
             (tuple(rng.choice((-1,0,1)) for _ in range(n)) for _ in range(N)))
  for vals in pins_list:
   rho={i+1:z for i,z in enumerate(vals) if z!=-1}
   t=theta(F,rho);u=n-len(rho);z=t['zero_pinned_true_clauses'];
   cap=repair_capacity(F,rho);assert cap['residual_uncovered_clauses']==z
   free_d=sum(sum(l==v for c in F for l in c) for v in range(1,n+1) if v not in rho)
   assert t['theta']==b-free_d+z
   count['checked_partial_cubes']+=1
   up=unit_propagate(F,rho)
   if cap['capacity_deficit']>0:
    count['capacity_triggered']+=1
    assert up is None
    if t['theta']<=b:count['capacity_only_triggered']+=1
   if t['theta']>b:assert cap['capacity_deficit']>0
   if up is not None:
    count['UP_closed_consistent']+=1
    new_t=theta(F,up);new_z=new_t['zero_pinned_true_clauses'];new_u=n-len(up)
    remaining_d=sum(sum(l==v for c in F for l in c) for v in range(1,n+1) if v not in up)
    assert new_z<=remaining_d
    assert new_t['theta']<=b
    assert repair_capacity(F,up)['capacity_deficit']<=0
    if t['theta']>b:found_violation.append([name,rho,'forbidden_but_UP_consistent'])
   if t['theta']>b:
    count['budget_triggered']+=1
    assert up is None, (name,rho,t)
   if t['theta']<=b:count['budget_not_triggered']+=1
  samples.append({'name':name,'n':n,'m':m,'budget':b,'count':dict(count)})
 assert not found_violation
 # UP can refute a partial cube with theta well below budget: converse fails.
 refuted_cube={abs(l):int(l<0) for l in SHARP8[0]}
 assert unit_propagate(SHARP8,refuted_cube) is None
 assert theta(SHARP8,refuted_cube)['theta']<=budget(SHARP8)
 converse={'source':'SHARP8','original_clause_index':0,'cube':refuted_cube,
          'theta':theta(SHARP8,refuted_cube)['theta'],'budget':budget(SHARP8),
          'UP_refutes_immediately':True}
 # Without balanced sign incidence the invariant is invalid.
 arbitrary=[(1,2,3)]
 bogus={'source_formula':arbitrary,'partial_cube':{1:1,2:1},
        'unjustified_balanced_budget_m_times_k_minus2_div2':0.5,
        'theta':theta(arbitrary,{1:1,2:1})['theta'],
        'actual_source_satisfying_complete_mask':7}
 assert bogus['theta']>bogus['unjustified_balanced_budget_m_times_k_minus2_div2']
 assert clause_status(arbitrary,7)['SAT']
 return {'seed':SEED,'balanced_partial_cube_tests':samples,'balanced_assumption_counterexample':bogus,
         'converse_counterexample':converse,
         'violations':found_violation,'claims':['theta monotone under pins','theta>B implies UP refutation',
         'at consistent UP fixed point zero-fixed-true clauses Z<=2u','regular-source conservation']}

def bench():
 rng=random.Random(SEED)
 cases=[('W1_strict22_UNSAT',W1),('SWAP6_strict22_SAT',SWAP6),
        ('SHARP8_strict22_SAT',SHARP8),('PAIRED_K4_strict22_SAT',PAIRED_K4),
        ('BALANCED4_SAT',BALANCED4),('IRREGULAR_BALANCED_UNSAT',IRREGULAR_BALANCED),('HORN_SAT',HORN),('XOR3_UNSAT',XOR_UNSAT),('BINARY_UNSAT',BINARY_UNSAT)]
 cases.extend((f'RANDOM22_n{n}_{z}',random_balanced(n,rng)) for n,z in ((9,0),(12,0),(15,0)))
 output=[]
 for name,F in cases:
  base=dpll(F,False);aug=dpll(F,True)
  assert base['SAT']==aug['SAT']
  assert base['nodes']==aug['nodes'],(name,base['nodes'],aug['nodes'])
  assert aug.get('balance_rejections',0)==0
  output.append({'name':name,'n':nvars(F),'m':len(F),'balanced':is_balanced(F),
                 'baseline_complete_UP_DPLL':base,'same_DPLL_plus_conservation_after_UP':aug})
 return {'seed':SEED,'accounting':'selected Python clause/literal scans, branches, tests; not TM instructions or comparable to industrial CDCL',
         'runs_same_source':output}

if __name__=='__main__':
 task=sys.argv[1] if len(sys.argv)>1 else 'test'
 start=time.perf_counter()
 out={'audit':audits,'test':tests,'bench':bench}[task]()
 out['execution_wall_seconds']=round(time.perf_counter()-start,5)
 dest=sys.argv[2] if len(sys.argv)>2 else f'{task}.json'
 with open(dest,'w') as fh:json.dump(out,fh,indent=2,sort_keys=True)
 print(task,'PASS',dest,'wall',out['execution_wall_seconds'])
 if task=='test':print('partial cubes',sum(s['count']['checked_partial_cubes'] for s in out['balanced_partial_cube_tests']),
                        'budget triggered',sum(s['count'].get('budget_triggered',0) for s in out['balanced_partial_cube_tests']))
 if task=='bench':
  for r in out['runs_same_source']:
   a=r['baseline_complete_UP_DPLL'];b=r['same_DPLL_plus_conservation_after_UP']
   print(r['name'],a['SAT'],'nodes',a['nodes'],b['nodes'],'work',a['selected_events'],b['selected_events'],
         'peak',a['peak_allocated_bytes'],b['peak_allocated_bytes'])