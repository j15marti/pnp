#!/usr/bin/env python3
"""LSPV-4 HITTING-CUBE250, source-indexed independent finite controls.
Standard library only.  Python 3.11+, bounded n<=15 controls.
All UNSAT claims rely on checked hitting-cover certificates or complete DPLL trees.
"""
from __future__ import annotations
from collections import Counter,defaultdict
from itertools import combinations,product
import json,hashlib,random,sys,time,math,tracemalloc

SEED=202610300530
RNG=random.Random(SEED)
W1='-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'
H1=[(1,3,5),(1,-3,6),(-1,4,5),(-1,-4,6),(2,3,-5),(2,-3,-6),(-2,4,-5),(-2,-4,-6)]
G8=[(1,2,4),(-1,3,5),(-2,-3,6),(1,-2,3),(-1,2,-3),(4,-5,-6),(-4,5,-6),(-4,-5,6)]
K6=[(-4,5,-2),(-2,6,-3),(-3,4,5),(3,1,4),(-1,-5,6),(3,-6,2),(-1,-5,-6),(-4,2,1)]

def parse(s):return [tuple(map(int,c.split())) for c in s.split(';')]
def swap_w1(F):
 G=[list(c) for c in F];assert G[7][0]==1 and G[19][0]==-1
 G[7][0]=-1;G[19][0]=1;return [tuple(c) for c in G]
def ring(r):
 out=[]
 for b in range(r):
  for j,C in enumerate(H1):
   out.append(tuple((1 if l>0 else -1)*(6*((b-1)%r)+abs(l)) if j==0 and h==0 else (1 if l>0 else -1)*(6*b+abs(l)) for h,l in enumerate(C)))
 return out

def lit_true(l,a):return a.get(abs(l),None)==(l>0)
def lit_status(l,a):
 v=a.get(abs(l),None)
 return None if v is None else (v==(l>0))
def status(C,a):return sum(lit_true(l,a) for l in C)
def full_status(F,a):return [status(c,a) for c in F]
def hist(t):return [t.count(i) for i in range(4)]
def assignment_dict(mask,n):return {i:bool((mask>>(i-1))&1) for i in range(1,n+1)}
def source_n(F):return max([abs(x) for C in F for x in C]+[0])
def source_comp(F,a):return {i:not a[i] for i in a}

def full_source_audit(name,F):
 n=source_n(F);m=len(F);proper=all(len(c)==3 and len({abs(x) for x in c})==3 for c in F)
 occ=[];targets=[]
 for j,C in enumerate(F):
  S={abs(l):int(l>0) for l in C};U={abs(l):int(l<0) for l in C}
  assert all(1-S[v]==U[v] for v in S)
  targets.append({'source_clause':j,'clause':list(C),'S_all_literals_true':S,'S_inverse_to_U':{v:1-x for v,x in S.items()},'U_all_literals_false':U,'U_inverse_to_S':{v:1-x for v,x in U.items()}})
  for pos,l in enumerate(C):occ.append({'clause':j,'literal_position':pos,'source_variable':abs(l),'source_literal':l,'S_value':int(l>0),'S_inverse_U':int(l<0),'U_value':int(l<0),'U_inverse_S':int(l>0)})
 matrix=[];pair_checks=0;triple_checks=0
 for j in range(m):
  for k in range(j+1,m):
   A,B=F[j],F[k];same=sorted({abs(l) for l in A if l in B});opp=sorted({abs(l) for l in A if -l in B})
   rule={'SS':not opp,'SU':not same,'US':not same,'UU':not opp}
   vars=sorted({abs(x) for x in (*A,*B)})
   brute={key:False for key in ('SS','SU','US','UU')}
   for bits in product([False,True],repeat=len(vars)):
    a=dict(zip(vars,bits));x=status(A,a);y=status(B,a)
    for mode,left,right in [('SS',len(A),len(B)),('SU',len(A),0),('US',0,len(B)),('UU',0,0)]:
     if x==left and y==right:brute[mode]=True
   assert rule==brute,(j,k,rule,brute)
   pair_checks+=4
   matrix.append({'source_clause_pair':[j,k],'same_sign_shared':same,'opposite_sign_shared':opp,'modes':rule,'both_extremes_impossible':bool(same and opp)})
 if proper and n<=6:
  for K in combinations(range(m),3):
   for modes in product(('S','U'),repeat=3):
    selected={};compatible=True
    for j,mode in zip(K,modes):
     for v,val in targets[j]['S_all_literals_true' if mode=='S' else 'U_all_literals_false'].items():
      if v in selected and selected[v]!=val:compatible=False
      selected[v]=val
    vars=sorted({abs(l) for j in K for l in F[j]})
    brute=False
    for bits in product((0,1),repeat=len(vars)):
     a=dict(zip(vars,bits))
     if all(status(F[j],a)==(len(F[j]) if mode=='S' else 0) for j,mode in zip(K,modes)):brute=True;break
    assert compatible==brute,(K,modes)
    triple_checks+=1
 allzero=assignment_dict(0,n);allone=assignment_dict((1<<n)-1,n)
 endpoints={'allzero':{'mask':0,'true_literal_counts':full_status(F,allzero),'buckets':hist(full_status(F,allzero))},'allone':{'mask':(1<<n)-1,'true_literal_counts':full_status(F,allone),'buckets':hist(full_status(F,allone))}}
 checks=0;models=[]
 if n<=15:
  for mask in range(1<<n):
   a=assignment_dict(mask,n);b=source_comp(F,a)
   x=full_status(F,a);y=full_status(F,b)
   assert all(xj+yj==len(C) for xj,yj,C in zip(x,y,F))
   if 0 not in x:models.append(mask)
   checks+=1
 path=[0]
 for v in range(1,min(n,4)+1):path.append(path[-1]^(1<<(v-1)))
 path.extend([(1<<n)-1,0])
 trails=[]
 for mask in path:
  a=assignment_dict(mask,n);t=full_status(F,a)
  trails.append({'mask':mask,'assignment':''.join(str(int(a[i])) for i in range(1,n+1)),'source_literal_truth':[ [int(lit_true(l,a)) for l in C] for C in F], 'per_clause_true_counts':t,'four_buckets':hist(t),'SAT':all(x>0 for x in t)})
 return {'name':name,'n':n,'m':m,'proper_three':proper,'original_signed_occurrences':occ,'source_clause_extreme_targets':targets,'four_way_original_pair_matrix':matrix,'pair_modes_exact_checked':pair_checks,'triple_extremes_exact_checked':triple_checks,'coherent_endpoints':endpoints,'coherent_flip_trails':trails,'assignment_complement_checked':checks,'model_count':len(models),'first_12_models':models[:12]}

def strict22(F):
 if not all(len(C)==3 and len({abs(x) for x in C})==3 for C in F):return False
 cnt=Counter(l for C in F for l in C);return all(cnt[v]==cnt[-v]==2 for v in range(1,source_n(F)+1))

def hitting_source_detector(F,strict_only=True,min_clique_size=2):
 """Provable O(m) signed22 source-graph clique enumeration, bounded degree6.
 Each nontrivial clique yields a canonical pinned-U cube if exact Kraft sum hits 1.
 """
 n=source_n(F);m=len(F)
 assert strict22(F) if strict_only else True
 pos=defaultdict(list);neg=defaultdict(list)
 cost=Counter();
 for j,C in enumerate(F):
  for l in C:
   (pos if l>0 else neg)[abs(l)].append(j);cost['source_occurrence_reads']+=1
 adj=[set() for _ in range(m)]
 for v in range(1,n+1):
  for j in pos[v]:
   for k in neg[v]:
    cost['opposite_pair_events']+=1
    if j==k:continue
    adj[j].add(k);adj[k].add(j)
 if strict_only:
  assert all(len(adj[j])<=6 for j in range(m))
  assert sum(cost['opposite_pair_events'] for _ in [0])==4*n
 certificates=[];seen=set();clique_counts=Counter()
 for j in range(m):
  higher=sorted(k for k in adj[j] if k>j)
  cost['neighbor_checks']+=len(adj[j]);
  for q in range(1,1<<len(higher)):
   K=(j,)+tuple(higher[h] for h in range(len(higher)) if q>>h&1)
   if len(K)>6 and strict_only:continue
   if len(K)<min_clique_size:continue
   cost['candidate_clique_subsets']+=1
   if any(h not in adj[k] for k,h in combinations(K,2)):
    cost['failed_clique_checks']+=1;continue
   cost['verified_hitting_cliques']+=1;clique_counts[len(K)]+=1
   signed=defaultdict(set)
   for idx in K:
    for l in F[idx]:signed[abs(l)].add(l>0);cost['clique_literal_visits']+=1
   pins={v:int(next(iter(signs)) is False) for v,signs in signed.items() if len(signs)==1}
   # Note: if all parent occurrences are positive, pin x=0; if all negative, pin x=1.
   widths=[]
   for idx in K:
    width=sum(abs(l) not in pins for l in F[idx]);widths.append(width)
   # All pair-hitting contrasts are on free conflicting-sign coordinates, so the
   # remaining falsifying subcubes are disjoint under the pinned cube.
   weight=sum(2**(3-w) for w in widths)
   assert weight<=8,(K,pins,widths,weight)
   cost['exact_weight_checks']+=1
   if weight==8 and pins:
    learned=tuple(sorted((v if val==0 else -v for v,val in pins.items()),key=lambda x:(abs(x),x<0)))
    # syntax sorted keyword needs lambda in function call; see line below later
    key=(learned,tuple(K))
    if key in seen:continue
    seen.add(key)
    cert={'original_parent_indices':list(K),'pinned_U_original_variable_assignments':{str(v):val for v,val in sorted(pins.items())},'residual_source_widths':widths,'Kraft_8_weight':weight,'pairwise_opposite_source_witnesses':[{'source_pair':[p,q],'opposing_source_variables':[abs(l) for l in F[p] if -l in F[q]]} for p,q in combinations(K,2)],'learned_original_variable_clause':list(learned),'certificate_type':'pairwise-U-incompatible residual falsification cubes partition global completion cube'}
    certificates.append(cert)
    cost['learned_certificates']+=1
 # don't include original clause duplicates in final solver; preserve ALL in output.
 effective=[];canonical=set(tuple(sorted(C)) for C in F)
 for cert in sorted(certificates,key=lambda c:(len(c['learned_original_variable_clause']),c['original_parent_indices'])):
  clause=tuple(cert['learned_original_variable_clause'])
  if len(clause)>3:continue
  if tuple(sorted(clause)) in canonical:
   cost['existing_clause_duplicate']+=1;continue
  if clause in {tuple(c['learned_original_variable_clause']) for c in effective}:
   cost['learned_duplicate']+=1;continue
  effective.append(cert)
  cost['accepted_learned_clauses']+=1
 return {'certificates':certificates,'selected_certificates':effective,'source_conflict_graph':{'neighbors':[sorted(v) for v in adj],'clique_counts':dict(clique_counts),'max_degree':max(map(len,adj),default=0),'edge_count':sum(map(len,adj))//2},'cost':dict(cost)}

def verify_hitting_certificate(F,cert):
 K=cert['original_parent_indices'];pins={int(v):int(b) for v,b in cert['pinned_U_original_variable_assignments'].items()}
 assert len(set(K))==len(K) and all(0<=j<len(F) for j in K)
 assert len(K)>=2
 for j in K:
  for l in F[j]:
   if abs(l) in pins:assert pins[abs(l)]==int(l<0)
 widths=[]
 for j in K:
  widths.append(sum(abs(l) not in pins for l in F[j]))
 for a,b in combinations(K,2):
  assert any(abs(l) not in pins and -l in F[b] for l in F[a]),(a,b)
 assert sum(2**(3-w) for w in widths)==8
 learned=tuple(sorted((v if value==0 else -v for v,value in pins.items()),key=lambda x:(abs(x),x<0)))
 assert tuple(cert['learned_original_variable_clause'])==learned
 return True

def certified_forbidden_cubes_exhaust(F,certificate, max_n=15):
 n=source_n(F)
 if n>max_n:return None
 pins={int(v):int(b) for v,b in certificate['pinned_U_original_variable_assignments'].items()}
 chk=0
 for mask in range(1<<n):
  if any(((mask>>(v-1))&1)!=value for v,value in pins.items()):continue
  a=assignment_dict(mask,n)
  assert any(status(F[j],a)==0 for j in certificate['original_parent_indices'])
  chk+=1
 return chk

def dpll(F,n,order=None, initial=None, proof=False):
 """UP-first fixed variable order, complete. Counts declared operations on original+derived CNF."""
 if order is None:order=list(range(1,n+1))
 cnt=Counter(); tree=[]
 def propagate(a):
  changed=True
  while changed:
   changed=False
   for C in F:
    cnt['clause_scans']+=1;un=[];sat=False
    for l in C:
     cnt['literal_reads']+=1
     z=lit_status(l,a)
     if z is True:sat=True;break
     if z is None:un.append(l)
    if sat:continue
    if not un:
     cnt['conflicts']+=1
     return False,None
    if len(un)==1:
     l=un[0];v=abs(l);b=l>0
     if v in a and a[v]!=b:
      cnt['conflicts']+=1;return False,None
     if v not in a:a[v]=b;cnt['unit_assignments']+=1;changed=True
  return True,a
 def branch(part):
  cnt['recursive_nodes']+=1
  a=part.copy();ok,a=propagate(a)
  if not ok:
   return None,{'kind':'UP_conflict','branch_cube':{str(k):int(v) for k,v in sorted(part.items())}}
  fully=True
  for C in F:
   cnt['decision_clause_scans']+=1
   satisfied=False
   for l in C:
    cnt['decision_literal_reads']+=1
    if lit_status(l,a) is True:satisfied=True;break
   if not satisfied:fully=False;break
  if fully:
   complete={v:a.get(v,False) for v in range(1,n+1)}
   assert all(status(C,complete)>0 for C in F)
   cnt['full_witness_literal_reads']+=sum(map(len,F));return complete,{'kind':'SAT','witness':{str(v):int(complete[v]) for v in complete}}
  v=next(v for v in order if v not in a)
  cnt['decision_branches']+=1
  proofchildren=[]
  for b in (False,True):
   c=a.copy();c[v]=b
   w,rec=branch(c)
   proofchildren.append({'bit':int(b),'subtree':rec})
   if w is not None:return w,{'kind':'SAT_BRANCH','variable':v,'children':proofchildren}
  return None,{'kind':'BRANCH','variable':v,'branch_cube':{str(k):int(vv) for k,vv in sorted(part.items())},'children':proofchildren}
 witness,t=branch(initial or {})
 ans={'satisfiable':witness is not None,'witness':{str(k):int(v) for k,v in witness.items()} if witness else None,'cost':dict(cnt),'work':sum(cnt.values()),'proof_tree':t if proof or witness is None else None}
 return ans

def replay_unsat_tree(F,n,node):
 cost=Counter()
 def propagate(a):
  changed=True
  while changed:
   changed=False
   for C in F:
    cost['proof_clause_scans']+=1
    un=[];sat=False
    for l in C:
     cost['proof_literal_reads']+=1
     v=a.get(abs(l),None)
     if v is None:un.append(l)
     elif v==(l>0):sat=True;break
    if sat:continue
    if not un:return False,a
    if len(un)==1:
     l=un[0];v=abs(l)
     if v not in a:a[v]=(l>0);changed=True;cost['proof_UP']+=1
  return True,a
 def rec(node,a):
  if node['kind']=='UP_conflict':
   ok,_=propagate(a.copy());assert not ok
   cost['checked_conflict_leaves']+=1;return
  assert node['kind']=='BRANCH'
  ok,state=propagate(a.copy());assert ok
  v=node['variable'];assert v not in state
  assert sorted(x['bit'] for x in node['children'])==[0,1]
  for child in node['children']:
   new=state.copy();new[v]=bool(child['bit']);rec(child['subtree'],new)
 rec(node,{})
 return dict(cost)

def make_adverse_cases():
 W=parse(W1)
 odd8=[tuple((v if ((mask>>(v-1))&1)==0 else -v) for v in (1,2,3)) for mask in range(8)]
 xor_even=[tuple(v if ((mask>>(v-1))&1)==0 else -v for v in (1,2,3)) for mask in range(8) if mask.bit_count()%2==0]
 xor_odd=[tuple(v if ((mask>>(v-1))&1)==0 else -v for v in (1,2,3)) for mask in range(8) if mask.bit_count()%2==1]
 ren=[tuple((-abs(l) if l>0 else abs(l)) if abs(l) in (1,4) else l for l in C) for C in G8]
 seeded=[];target={i:bool((39>>(i-1))&1) for i in range(1,8)}
 while len(seeded)<15:
  sup=RNG.sample(range(1,8),3);C=tuple((v if RNG.choice((False,True)) else -v) for v in sup)
  if any(lit_true(l,target) for l in C) and C not in seeded:seeded.append(C)
 return [
 ('G8_hitting_conditional_SAT',G8),('G8_polarity_renamed_SAT',ren),
 ('H1_strict22_SAT',H1),('H2_strict22_SAT',ring(2)),('K6_hitting_clique_strict22_SAT',K6),
 ('W1_strict22_UNSAT',W),('W1_signed_swap_SAT',swap_w1(W)),
 ('XOR_even3_SAT',xor_even),('XOR_all8_UNSAT',odd8),
 ('XOR_contradictory8_UNSAT',xor_even+xor_odd),
 ('Horn_SAT',[(1,),(-1,2),(-2,3)]),('Horn_UNSAT',[(1,),(-1,2),(-2,)]),
 ('2SAT_UNSAT',[(1,2),(1,-2),(-1,2),(-1,-2)]),
 ('all_positive_SAT',[(1,2,3),(2,3,4),(1,3,4)]),
 ('planted_dense_SAT',seeded),
 ('hitting_adaptive_8_UNSAT',[(1,y,z) for y,z in [(2,3),(2,-3),(-2,3),(-2,-3)]]+[(-1,y,z) for y,z in [(2,4),(2,-4),(-2,4),(-2,-4)]])
 ]

def run():
 start=time.perf_counter();cases=make_adverse_cases();out={'id':'HITTING_CUBE250','seed':SEED,'model':'proper original CNF; strict22 exception graph only on eligible cases','cases':[],'exact_certificate_proofs':{},'timestamp':'2026-10-30T05:30:00-07:00'}
 allchecks=Counter();representative=None
 for name,F in cases:
  n=source_n(F);m=len(F);audit=full_source_audit(name,F)
  allchecks['pair_mode_checks']+=audit['pair_modes_exact_checked'];allchecks['triple_mode_checks']+=audit['triple_extremes_exact_checked'];allchecks['complete_assignment_complement_checks']+=audit['assignment_complement_checked'];
  pre=hitting_source_detector(F) if strict22(F) else {'certificates':[],'selected_certificates':[],'cost':{},'source_conflict_graph':{}}
  for cert in pre['certificates']:
   assert verify_hitting_certificate(F,cert)
   if n<=15:cert['full_completion_cubes_checked']=certified_forbidden_cubes_exhaust(F,cert)
  lean=hitting_source_detector(F,min_clique_size=5) if strict22(F) else {'certificates':[],'selected_certificates':[],'cost':{},'source_conflict_graph':{}}
  for cert in lean['certificates']: assert verify_hitting_certificate(F,cert)
  clauses=[tuple(c['learned_original_variable_clause']) for c in pre['selected_certificates']]
  leanclauses=[tuple(c['learned_original_variable_clause']) for c in lean['selected_certificates']]
  # Branch order prioritizes y variables for the G8 witness but is IDENTICAL with/without the prepass.
  order=[4,5,6,1,2,3]+list(range(7,n+1)) if name.startswith('G8') else list(range(1,n+1))
  base=dpll(F,n,order,proof=True)
  augmented=dpll(F+clauses,n,order,proof=True)
  lean_augmented=dpll(F+leanclauses,n,order,proof=True)
  assert base['satisfiable']==augmented['satisfiable']==lean_augmented['satisfiable']==(audit['model_count']>0)
  sourcecheck=Counter()
  for cert in pre['selected_certificates']:
   assert verify_hitting_certificate(F,cert)
   sourcecheck['original_clause_literal_checks']+=sum(len(F[j]) for j in cert['original_parent_indices'])
   sourcecheck['pair_witness_replay']+=len(cert['pairwise_opposite_source_witnesses'])
   sourcecheck['source_cube_coverage_checks']+=1
  leancheck=Counter()
  for cert in lean['selected_certificates']:
   assert verify_hitting_certificate(F,cert)
   leancheck['original_clause_literal_checks']+=sum(len(F[j]) for j in cert['original_parent_indices'])
   leancheck['pair_witness_replay']+=len(cert['pairwise_opposite_source_witnesses'])
   leancheck['source_cube_coverage_checks']+=1
  if not base['satisfiable']:
   base['proof_verification']=replay_unsat_tree(F,n,base['proof_tree'])
   augmented['proof_verification']=replay_unsat_tree(F+clauses,n,augmented['proof_tree'])
   lean_augmented['proof_verification']=replay_unsat_tree(F+leanclauses,n,lean_augmented['proof_tree'])
  for meth in (base,augmented,lean_augmented):
   if meth['satisfiable']:
    witness={int(k):bool(v) for k,v in meth['witness'].items()}
    assert all(status(C,witness)>0 for C in F)
   meth['refutation_or_model_validation_work']=sum(meth.get('proof_verification',{}).values()) if not meth['satisfiable'] else 3*m
  work_pre=sum(pre['cost'].values())
  # only solver-acquired source clique prepass work charged to augmented; complete diagnostic output separate.
  total_augmented=augmented['work']+work_pre+sum(sourcecheck.values())+augmented['refutation_or_model_validation_work']
  total_base=base['work']+base['refutation_or_model_validation_work']
  total_lean=lean_augmented['work']+sum(lean['cost'].values())+sum(leancheck.values())+lean_augmented['refutation_or_model_validation_work']
  report={'name':name,'n':n,'m':m,'strict22':strict22(F),'source_original_clauses':[list(C) for C in F], 'source_audit':audit, 'hitting_detector':pre,'lean_hitting_detector':lean,'proof_checker_source_cost':dict(sourcecheck), 'baseline':base,'prepass_plus_dpll':augmented,'lean_prepass_plus_dpll':lean_augmented,'charged_comparison':{'baseline_work_with_final_proof_check':total_base,'learned_controller_work_with_final_proof_check':total_augmented,'delta_controller_minus_baseline':total_augmented-total_base,'baseline_nodes':base['cost'].get('recursive_nodes',0),'controller_nodes':augmented['cost'].get('recursive_nodes',0),'prepass_work':work_pre,'lean_prepass_work':sum(lean['cost'].values()),'lean_controller_nodes':lean_augmented['cost'].get('recursive_nodes',0),'lean_controller_work_with_final_proof_check':total_lean}}
  if name=='K6_hitting_clique_strict22_SAT':
   assert int(pre['source_conflict_graph']['clique_counts'].get(6,0))>=1
  # Substitution direct check for G8:
  if name=='G8_hitting_conditional_SAT':
   assert strict22(F)
   cert=next(c for c in pre['certificates'] if c['original_parent_indices']==[0,1,2,3,4] and c['pinned_U_original_variable_assignments']=={'4':0,'5':0,'6':0})
   assert cert['residual_source_widths']==[2,2,2,3,3]
   assert set(cert['learned_original_variable_clause'])=={4,5,6}
   assert cert['Kraft_8_weight']==8
   # Three binary residuals alone are SAT and have no unit; witness x1=0 x2=1 x3=0.
   assert all(status(C,{1:False,2:True,3:False})>0 for C in [(1,2),(-1,3),(-2,-3)])
   report['new_source_forbidden_cube_certificate']=cert
   representative=report
  allchecks['hitting_certificates_verified']+=len(pre['certificates'])
  out['cases'].append(report)
 out['aggregate_exact_checks']=dict(allchecks)
 out['elapsed_seconds']=round(time.perf_counter()-start,3)
 raw='/mnt/data/lspv4_run50/LSPV4_HITTING_CUBE250_raw.json'
 with open(raw,'w') as fh:json.dump(out,fh,sort_keys=True,indent=1)
 sha=hashlib.sha256(open(raw,'rb').read()).hexdigest();bytes_=len(open(raw,'rb').read())
 compact={'id':out['id'],'seed':SEED,'raw_sha256':sha,'raw_bytes':bytes_,'aggregate_checks':dict(allchecks),'elapsed_seconds':out['elapsed_seconds'],'results':[{'name':x['name'],'n':x['n'],'m':x['m'],'SAT':x['baseline']['satisfiable'],'models':x['source_audit']['model_count'],'clique_sizes':x['hitting_detector']['source_conflict_graph'].get('clique_counts'),'learned_count':len(x['hitting_detector']['selected_certificates']),'baseline_nodes':x['charged_comparison']['baseline_nodes'],'controller_nodes':x['charged_comparison']['controller_nodes'],'baseline_work':x['charged_comparison']['baseline_work_with_final_proof_check'],'controller_work':x['charged_comparison']['learned_controller_work_with_final_proof_check'],'prepass_work':x['charged_comparison']['prepass_work'],'lean_learned_count':len(x['lean_hitting_detector']['selected_certificates']),'lean_nodes':x['charged_comparison']['lean_controller_nodes'],'lean_work':x['charged_comparison']['lean_controller_work_with_final_proof_check'],'lean_prepass_work':x['charged_comparison']['lean_prepass_work']} for x in out['cases']]}
 with open('/mnt/data/lspv4_run50/LSPV4_HITTING_CUBE250_summary.json','w') as fh:json.dump(compact,fh,indent=2,sort_keys=True)
 print(json.dumps(compact,indent=2))

if __name__=='__main__':run()
