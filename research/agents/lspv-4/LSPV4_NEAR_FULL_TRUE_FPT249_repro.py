#!/usr/bin/env python3
"""LSPV-4 NEAR-FULL-TRUE-FPT249, standard-library exact source experiment.

The parameterized problem solved by the front end is: does F have a complete
SAT assignment with at most k clauses having 1 or 2 TRUE literals? This is
NOT general SAT; a NO certificate is only a budget-k NO, while full fallback
UP-DPLL separately solves F.

All truth counts, S/U targets, pair modes, and original source IDs are retained.
Work is an intentionally explicit count of selected logical source/literal/branch
operations, not processor cycles or an unconditional complexity lower bound.
"""
from __future__ import annotations
import argparse, collections, hashlib, itertools, json, random, sys, time
from pathlib import Path

RUN='LSPV4_NEAR_FULL_TRUE_FPT249'; SEED=202610300500
W1='-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'
H1=((1,3,5),(1,-3,6),(-1,4,5),(-1,-4,6),(2,3,-5),(2,-3,-6),(-2,4,-5),(-2,-4,-6))

def parse(s): return tuple(tuple(map(int,c.split())) for c in s.split(';'))

def ring(r):
 out=[]
 for j in range(r):
  for k,c in enumerate(H1):
   out.append(tuple((1 if lit>0 else -1)*(6*((j-1)%r if k==0 and i==0 else j)+abs(lit)) for i,lit in enumerate(c)))
 return tuple(out)

def value(l,a):return ((a>>(abs(l)-1))&1)==(l>0)

def counts(F,a):return tuple(sum(value(l,a) for l in c) for c in F)

def hist(t):return [t.count(i) for i in range(4)]

def sat(F,a):return all(any(value(l,a) for l in c) for c in F)

def nvar(F):return max((abs(l) for c in F for l in c),default=0)

def split_pair_extreme(F):
 data=[]
 for j,c in enumerate(F):
  d=[]
  for p,l in enumerate(c):
   v=abs(l);sv=int(l>0);uv=1-sv
   d.append({'occurrence':f'x_{{{v},{j}}}','var':v,'clause':j,'position':p,'literal':l,
             'S_target':sv,'S_inverted_to_U':1-sv,'U_target':uv,'U_inverted_to_S':1-uv})
  data.append({'clause':j,'literals':list(c),'occurrences':d,'S':{str(abs(l)):int(l>0) for l in c},
               'U':{str(abs(l)):int(l<0) for l in c}})
 pairs=[];H=[];sum_events=0
 for j in range(len(F)):
  for k in range(j+1,len(F)):
   a={abs(l):l>0 for l in F[j]};b={abs(l):l>0 for l in F[k]}
   ss=[v for v in a.keys()&b.keys() if a[v]==b[v]]
   oo=[v for v in a.keys()&b.keys() if a[v]!=b[v]]
   modes={'SS':not oo,'SU':not ss,'US':not ss,'UU':not oo}
   pairs.append({'source_clause_pair':[j,k], 'same_sign_vars':sorted(ss),
                 'opposite_sign_vars':sorted(oo),'modes':modes,
                 'all_four_infeasible':bool(ss and oo)})
   if oo:H.append((j,k))
   sum_events+=len(F[j])*len(F[k])
 return data,pairs,H,sum_events

def brute_modes(F,j,k):
 c=F[j];d=F[k];vs=sorted(set(map(abs,c+d)));ans={x:False for x in ('SS','SU','US','UU')}
 for a in range(1<<len(vs)):
  x=sum(1<< (v-1) for i,v in enumerate(vs) if (a>>i)&1)
  tc=sum(value(l,x) for l in c);td=sum(value(l,x) for l in d)
  if tc in (0,3) and td in (0,3):ans[('S' if tc==3 else 'U')+('S' if td==3 else 'U')]=True
 return ans

def target_multi_consistency(F,js,states):
 demands={}
 for j,q in zip(js,states):
  for l in F[j]:
   v=abs(l);val=int(l>0) if q=='S' else int(l<0)
   if v in demands and demands[v]!=val:return False
   demands[v]=val
 return True

def triple_audit(F,limit=32):
 r=0;results=[]
 for js in itertools.islice(itertools.combinations(range(len(F)),3),limit):
  union=sorted({abs(l) for j in js for l in F[j]})
  for states in itertools.product('SU',repeat=3):
   pred=target_multi_consistency(F,js,states)
   obs=False
   for b in range(1<<len(union)):
    a=sum(1<<(v-1) for p,v in enumerate(union) if (b>>p)&1)
    if all(sum(value(l,a) for l in F[j])==(3 if mode=='S' else 0) for j,mode in zip(js,states)):
     obs=True;break
   assert obs==pred,(js,states)
   r+=1
  if len(results)<3:results.append({'triple':list(js),'modes_checked':8})
 return {'checked':r,'samples':results}

def endpoints_trail(F,n):
 allones=(1<<n)-1;paths=[[0],[allones]]
 paths[0]+=[1<<i for i in range(min(n,4))]
 paths[0]+=[sum(1<<i for i in range(min(n,h))) for h in (2,3,min(n,6))]
 paths[1]+=[allones^(1<<i) for i in range(min(n,4))]
 paths[1]+=[allones^sum(1<<i for i in range(min(n,h))) for h in (2,3,min(n,6))]
 out=[]
 for seq in paths:
  states=[]
  for a in dict.fromkeys(seq):
   t=counts(F,a);com=counts(F,allones^a)
   assert hist(t)==hist(com)[::-1]
   states.append({'assignment_mask':a,'bits':[int((a>>i)&1) for i in range(n)],
                  't_by_original_clause':list(t),'N0_N1_N2_N3':hist(t),
                  'false_source_clauses':[j for j,z in enumerate(t) if z==0],
                  'sat':0 not in t})
  out.append(states)
 return out

def strict22(F,n):
 c=collections.Counter(l for C in F for l in C)
 return len(F)*3==4*n and all(len(C)==3 and len(set(map(abs,C)))==3 for C in F) and all(c[v]==2 and c[-v]==2 for v in range(1,n+1))

def source_resolvent(F):
 for j,c in enumerate(F):
  for k,d in enumerate(F[j+1:],j+1):
   for pivot in c:
    if -pivot in d:
     remain=[l for l in c if l!=pivot]+[l for l in d if l!=-pivot]
     if any(-l in remain for l in remain):continue
     z=sorted(set(remain),key=lambda l:(abs(l),l<0))
     cube={str(abs(l)):int(l<0) for l in z}
     # Actual full assignment extensions of the falsifying cube MUST contradict the two parents.
     n=max(max(map(abs,c)),max(map(abs,d)))
     for a in range(1<<min(n,16)):
      if all(((a>>(int(v)-1))&1)==val for v,val in cube.items()):
       assert not (any(value(l,a) for l in c) and any(value(l,a) for l in d))
     return {'source_parent_clause_indices':[j,k],'pivot_original_var':abs(pivot),
             'source_parent_pivot_signs':[pivot,-pivot], 'non_tautological_resolvent':z,
             'forbidden_original_variable_cube':cube, 'proof_rule':'single-pivot source resolution'}
 return None

class Work:
 def __init__(self):self.c=collections.Counter()
 def add(self,k,v=1):self.c[k]+=v
 def total(self):return sum(self.c.values())
 def data(self):return dict(self.c)

def up(F,rho,w,proof=False):
 r=dict(rho);trace=[]
 while True:
  w.add('unit_rounds');changed=False
  for j,c in enumerate(F):
   w.add('clause_scan');satflag=False;unassigned=[]
   for l in c:
    w.add('literal_test');v=abs(l)
    if v not in r:unassigned.append(l)
    elif r[v]==int(l>0):satflag=True;break
   if satflag:continue
   if not unassigned:
    w.add('conflicts')
    return False,r,trace,j
   if len(unassigned)==1:
    l=unassigned[0];v=abs(l);t=int(l>0)
    r[v]=t;trace.append((v,t,j));w.add('unit_assignments');changed=True
  if not changed:return True,r,trace,None

def dpll(F,n,initial=None):
 w=Work();leaves=[];nodes=0
 def go(rho,path):
  nonlocal nodes
  nodes+=1;w.add('recursion_nodes')
  ok,r,trace,bad=up(F,rho,w)
  if not ok:
   leaves.append({'branch_decisions':path,'unit_steps':trace,'conflict_original_clause':bad})
   return None
  v=next((i for i in range(1,n+1) if i not in r),None)
  if v is None:
   a=sum((1<<(i-1)) for i in range(1,n+1) if r[i]);
   for c in F:
    w.add('witness_clause_check')
    for l in c:
     w.add('witness_literal_check')
     if value(l,a):break
    else:raise RuntimeError('DPLL bogus model')
   return a
  for b in (0,1):
   w.add('branch_decisions');q=dict(r);q[v]=b
   a=go(q,path+[(v,b)])
   if a is not None:return a
  return None
 model=go(initial or {},[])
 return {'answer':'SAT' if model is not None else 'UNSAT','model':model,'nodes':nodes,
         'work':w.total(),'ledger':w.data(),'complete_leaf_count':len(leaves),'proof_leaves':leaves}

def check_dpll_unsat(F,n,leaves):
 # Verify complete branch tree independently from leaf descriptions by reconstructing
 # a decision tree with all visited paths, and redoing source UP with this new routine.
 def check_up(r):
  r=dict(r)
  while True:
   changed=False
   for j,c in enumerate(F):
    rem=[l for l in c if abs(l) not in r]
    if any(r[abs(l)]==int(l>0) for l in c if abs(l) in r):continue
    if not rem:return False
    if len(rem)==1:
     l=rem[0];v=abs(l);b=int(l>0)
     if v in r and r[v]!=b:return False
     if v not in r:r[v]=b;changed=True
   if not changed:return True
 paths={tuple(tuple(z) for z in l['branch_decisions']) for l in leaves}
 assert len(paths)==len(leaves)
 assert all(not check_up(dict(p)) for p in paths)
 # For each proper prefix of any leaf path, both child branches appear somewhere.
 for p in paths:
  for z in range(len(p)):
   pref=p[:z+1];other=p[:z]+((pref[-1][0],1-pref[-1][1]),)
   assert any(q[:len(other)]==other for q in paths)
 return {'verified':True,'conflicting_leaf_count':len(paths)}

def fpt(F,n,k,H):
 """At most k original middle clauses (t=1 or2), checked exactly."""
 w=Work();w.add('input_literal_preparation',sum(len(c) for c in F))
 # Recount deterministic graph acquisition from raw signed occurrences, no free oracle H.
 pos=collections.defaultdict(list);neg=collections.defaultdict(list)
 for j,c in enumerate(F):
  for l in c:
   w.add('occurrence_index_add')
   (pos if l>0 else neg)[abs(l)].append(j)
 edges=set()
 for v in range(1,n+1):
  for j in pos[v]:
   for h in neg[v]:
    w.add('opposite_occurrence_pair_event')
    edges.add(tuple(sorted((j,h))))
 ed=sorted(edges)
 assert ed==sorted(H)
 proof_leaves=[];states=0;answer=None;remaining_middle=None;free_enum_tests=0
 def go(K):
  nonlocal states,answer,remaining_middle,free_enum_tests
  states+=1;w.add('cover_nodes')
  if len(K)>k:return
  e=None
  for u,v in ed:
   w.add('conflict_edge_scan')
   if u not in K and v not in K:e=(u,v);break
  if e:
   if len(K)>=k:
    proof_leaves.append({'K':sorted(K),'reason':'uncovered_SS_incompatible_opposite_sign_edge','edge':e})
    w.add('budget_exhaustion_leaves')
    return
   for z in e:
    w.add('cover_branches')
    if go(K|{z}):return True
   return False
  # Outside K all source clauses forced S. Their S target demands must be consistent.
  forced={}
  for j,c in enumerate(F):
   if j in K:continue
   for l in c:
    w.add('forced_S_literal_assignment');v=abs(l);val=int(l>0)
    if v in forced:assert forced[v]==val
    forced[v]=val
  free=[i for i in range(1,n+1) if i not in forced]
  assert len(free)<=3*len(K) # because every free original variable appears only in K
  for q in range(1<<len(free)):
   w.add('free_completion_attempts');free_enum_tests+=1
   w.add('forced_assignment_copy',len(forced))
   a=sum(1<<(v-1) for v,b in forced.items() if b)
   for z,v in enumerate(free):
    w.add('free_variable_bit_set')
    if (q>>z)&1:a|=1<<(v-1)
   bad=None
   for j in K:
    w.add('remaining_clause_check')
    if not any(value(l,a) for l in F[j]):
     bad=j;break
   if bad is None:
    assert sat(F,a)
    w.add('whole_source_witness_verification',sum(len(c) for c in F))
    answer=a;remaining_middle=sum(0<z<3 for z in counts(F,a));
    assert remaining_middle<=k
    return True
   w.add('remaining_clause_counterexamples')
  proof_leaves.append({'K':sorted(K),'reason':'all_remaining_variable_completions_fail_original_source',
                       'free_vars':free,'forcing':forced,'enumerated_completions':1<<len(free)})
  return False
 if strict22(F,n) and 4*k<3*len(F):
  # Exact arithmetic consequence of fixed literal total under a SAT witness.
  w.add('strict22_balance_check',len(F)+n)
  proof_leaves=[{'reason':'strict22_SAT_requires_middle_at_least_ceil_3m_over_4',
                 'threshold':(3*len(F)+3)//4,'budget':k}]
 else:
  # Cheap certified vertex-cover lower bound from disjoint opposite-sign
  # source-clause pairs. A matching of k+1 edges needs k+1 distinct
  # middle clauses in ANY ordinary SAT assignment, since each endpoint
  # pair is SS-incompatible. No claim of full SAT UNSAT.
  used=set();matching=[]
  for j,h in ed:
   w.add('matching_edge_scan')
   if j not in used and h not in used:
    used.update((j,h));matching.append((j,h));w.add('matching_edge_selected')
   if len(matching)>k:break
  if len(matching)>k:
   certificate=[]
   for j,h in matching:
    pivot=next(v for v in set(map(abs,F[j]))&set(map(abs,F[h]))
      if any(l in F[j] and -l in F[h] for l in (v,-v)))
    w.add('matching_proof_source_lit_tests',6)
    certificate.append({'source_clause_pair':[j,h],'opposite_sign_shared_variable':pivot})
   proof_leaves=[{'reason':'matching_of_k_plus_1_conflicting_source_clause_pairs',
                 'disjoint_pairs':certificate,'budget':k}]
  else:go(frozenset())
 return {'budget':k,'within_budget_SAT':answer is not None,'SAT_witness':answer,
         'witness_middle_count':remaining_middle,'conflict_edges':len(ed),
         'cover_nodes':states,'budget_rejection_leaves':len(proof_leaves),
         'free_completion_attempts':free_enum_tests,'work':w.total(),'ledger':w.data(),
         'parameter_certificate_leaves':proof_leaves}

def independent_bounded_oracle(F,n,k):
 for a in range(1<<n):
  t=counts(F,a)
  if all(x>0 for x in t) and sum(x in (1,2) for x in t)<=k:return a
 return None

def tseitin_K4(odd=1):
 # Each graph vertex degree 3. Each ternary parity constraint is 4 clauses
 # forbidding the four non-target parity assignments.
 E=[(1,2),(1,3),(1,4),(2,3),(2,4),(3,4)];out=[]
 for vertex in range(1,5):
  incident=[i+1 for i,(u,v) in enumerate(E) if vertex in (u,v)]
  charge=odd if vertex==1 else 0
  for bits in itertools.product((0,1),repeat=3):
   if sum(bits)%2==charge:continue
   out.append(tuple(v if b==0 else -v for v,b in zip(incident,bits)))
 return tuple(out)

def parity3(parity):
 return tuple(tuple(v if b==0 else -v for v,b in zip((1,2,3),bits))
  for bits in itertools.product((0,1),repeat=3) if sum(bits)%2!=parity)

def pad2sat_unsat():
 base=[(1,2),(1,-2),(-1,2),(-1,-2)]
 return tuple(tuple(c)+(sign*(3+j),) for j,c in enumerate(base) for sign in (1,-1))

def planted(n,m,seed):
 rng=random.Random(seed);target=sum((1<<v) for v in range(n) if rng.randrange(2))
 F=set()
 while len(F)<m:
  vs=rng.sample(range(1,n+1),3)
  c=tuple((1 if rng.randrange(2) else -1)*v for v in vs)
  if any(value(l,target) for l in c):F.add(c)
 return tuple(sorted(F)),target

def cases():
 W=parse(W1);G=[list(c) for c in W];assert G[7][0]==1 and G[19][0]==-1
 G[7][0]*=-1;G[19][0]*=-1
 D,planted_witness=planted(9,24,SEED)
 F={
  'positive_only':((1,2,3),(2,3,4),(1,4,5)),
  'one_conflict_SAT':((1,2,3),(-1,4,5),(2,4,6)),
  'two_conflicts_SAT':((1,2,3),(-1,4,5),(2,-4,6),(3,5,6)),
  'all_eight_signs_UNSAT':tuple(tuple(v if b==0 else -v for v,b in zip((1,2,3),bits)) for bits in itertools.product((0,1),repeat=3)),
  'H1_strict22_SAT':H1,
  'H2_strict22_SAT':ring(2),
  'W1_strict22_UNSAT':W,
  'W1_two_sign_swaps_SAT':tuple(tuple(c) for c in G),
  'xor3_parity0_SAT':parity3(0),
  'xor3_both_parities_UNSAT':parity3(0)+parity3(1),
  'odd_K4_Tseitin_UNSAT':tseitin_K4(1),
  'Horn_SAT':((-1,-2,3),(-2,-3,4),(-1,-3,4),(1,2,3)),
  'padded_2SAT_UNSAT':pad2sat_unsat(),
  'planted_dense_3CNF_SAT':D,
 }
 return F,{'planted_dense_3CNF_SAT':planted_witness}

def run(out):
 c,known=cases();raw={'id':RUN,'seed':SEED,'time_utc':'2026-10-30T12:00:36Z',
  'interpretation':'bounded-middle FPT is NOT full SAT, and k may be linear in strict22',
  'cases':{}}
 totals=collections.Counter()
 for label,F in c.items():
  n=nvar(F);m=len(F);assert all(len(z)==3 and len(set(map(abs,z)))==3 for z in F)
  t0=time.perf_counter();ext,pair,H,cost_pairs=split_pair_extreme(F)
  for p in pair: assert p['modes']==brute_modes(F,*p['source_clause_pair'])
  tri=triple_audit(F,limit= min(5,m*(m-1)*(m-2)//6))
  trails=endpoints_trail(F,n)
  cert=source_resolvent(F)
  complete=dpll(F,n)
  if complete['answer']=='UNSAT':checker=check_dpll_unsat(F,n,complete['proof_leaves'])
  else:checker={'verified':sat(F,complete['model'])}
  assert checker['verified']
  exact_sat=independent_bounded_oracle(F,n,m)
  assert (exact_sat is None)==(complete['model'] is None)
  if label in known:assert sat(F,known[label])
  # One comparison budget=2, and a separate boundary computation on H1 with k=6.
  budgets=sorted(set([0,1,2,3]+([6] if label=='H1_strict22_SAT' else [])))
  fronts=[]
  for k in budgets:
   r=fpt(F,n,k,H)
   oracle=independent_bounded_oracle(F,n,k)
   assert r['within_budget_SAT']==(oracle is not None),(label,k,r,oracle)
   # The exact full SAT controller runs the SAME baseline fallback if front fails.
   if r['within_budget_SAT']:
    states=r['cover_nodes']
    final='SAT';fallback_nodes=0;fallback_work=0
   else:
    final=complete['answer'];states=r['cover_nodes']+complete['nodes'];fallback_nodes=complete['nodes'];fallback_work=complete['work']
   r.update({'full_controller_answer':final,'full_controller_nodes':states,
             'fallback_nodes':fallback_nodes,'fallback_work':fallback_work,
             'total_selected_work':r['work']+fallback_work,
             'total_proof_replay_not_included':True})
   fronts.append(r)
  exact_count=0;best_mid=None;min_witness=None
  for a in range(1<<n):
   z=counts(F,a)
   if all(x>=1 for x in z):
    exact_count+=1;mm=sum(0<x<3 for x in z)
    if best_mid is None or mm<best_mid:best_mid=mm;min_witness=a
   assert hist(z)==hist(counts(F,((1<<n)-1)^a))[::-1]
  assert (exact_count==0)==(complete['model'] is None)
  strict=strict22(F,n)
  if strict and exact_count:
   assert best_mid*4>=3*m
  totals['source_pair_modes_checked']+=4*len(pair)
  totals['triple_modes_checked']+=tri['checked']
  totals['complement_complete_states_checked']+=1<<n
  raw['cases'][label]={
   'n':n,'m':m,'original_source':[list(z) for z in F], 'strict22':strict,
   'signed_occurrence_targets':ext, 'original_clause_pair_compatibility':pair,
   'source_opposite_sign_conflict_graph_edges':[list(z) for z in H],
   'explicit_dense_pair_compare_events':cost_pairs,'triple_mode_controls':tri,
   'coherent_0_1_and_global_flip_trails':trails,'parent_resolvent_forbidden_cube':cert,
   'independent_exact_models':exact_count,'exact_min_middle_in_any_SAT_model':best_mid,
   'exact_min_middle_witness':min_witness,'dpll':complete,
   'independent_full_solver_proof_check':checker,'bounded_middle_controllers':fronts,
   'runtime_seconds':round(time.perf_counter()-t0,5)}
  print(label, 'n',n,'m',m,'SATmodels',exact_count,'bestM',best_mid,
        'UPDPLLnodes',complete['nodes'],'UPDPLLwork',complete['work'],
        'k2controllerwork',fronts[2]['total_selected_work'],
        'k2nodes',fronts[2]['full_controller_nodes'], 'secs',round(time.perf_counter()-t0,3))
 raw['assertions']=dict(totals)
 out.write_text(json.dumps(raw,indent=2,sort_keys=True))
 return raw

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--out',default='LSPV4_NEAR_FULL_TRUE_FPT249_raw.json');a=ap.parse_args()
 r=run(Path(a.out));s=json.dumps(r,sort_keys=True).encode();print('FINISHED',r['assertions'], 'sha256',hashlib.sha256(Path(a.out).read_bytes()).hexdigest(),'bytes',Path(a.out).stat().st_size)