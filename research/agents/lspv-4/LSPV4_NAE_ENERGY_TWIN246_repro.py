#!/usr/bin/env python3
"""LSPV-4 2026-10-30 02:36 PDT, NAE-ENERGY-TWIN246.
Exact ORIGINAL source indexed S/U occurrence audits, pair/triple modes,
complete coherent assignment/complement enumeration, signed22 SAT/UNSAT twin,
source-proved forbidden cube, and charged UP-DPLL/E-prepass comparison.
Stdlib only, deterministic. Run phases separately (each <30 seconds):
 python LSPV4_NAE_ENERGY_TWIN246_repro.py --phase primary
 python LSPV4_NAE_ENERGY_TWIN246_repro.py --phase benchmark
Outputs JSON into --outdir; environment-dependent runtime not a proof claim.
"""
import argparse, collections, itertools, json, os, sys, time, hashlib, tracemalloc
from pathlib import Path

W1_STR='-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'
W1=tuple(tuple(map(int,cl.split())) for cl in W1_STR.split(';'))
SELECTED_CLAUSES=(0,1,2,4,7,9,12,14,16,17) # zero-indexed source clause indices
TW=tuple(tuple(-l if j in SELECTED_CLAUSES else l for l in c) for j,c in enumerate(W1))
H1=((1,3,5),(1,-3,6),(-1,4,5),(-1,-4,6),(2,3,-5),(2,-3,-6),(-2,4,-5),(-2,-4,-6))

def h_ring(r):
 f=[]
 for j in range(r):
  for k, c in enumerate(H1):
   f.append(tuple((1 if l>0 else -1)*(6*((j+r-1)%r if k==0 and h==0 else j)+abs(l)) for h,l in enumerate(c)))
 return tuple(f)

def xor3(positive=True):
 # positive = even/odd parity (4 minterms) SAT; both parities UNSAT.
 out=[]
 for a in range(8):
  if a.bit_count()%2==(1 if positive else 0):
   # clause excludes this assignment
   out.append(tuple((-(i+1) if (a>>i)&1 else i+1) for i in range(3)))
 return tuple(out)

def tseitin_k4_unsat():
 # Odd charge on K4, parity constraints encoded as 4 3-literal clauses each.
 edges=[(i,j) for i in range(4) for j in range(i+1,4)]
 incidence={i:[k+1 for k,(u,v) in enumerate(edges) if u==i or v==i] for i in range(4)}
 f=[]
 for v in range(4):
  ls=incidence[v]
  assert len(ls)==3
  for a in range(8):
   if a.bit_count()%2!=(1 if v==0 else 0):
    f.append(tuple(-l if (a>>h)&1 else l for h,l in enumerate(ls)))
 return tuple(f)

def planted_dense():
 import random
 rng=random.Random(202610300236)
 model=0b1011011011
 f=[]
 for _ in range(36):
  inds=rng.sample(range(1,11),3)
  signs=[1 if rng.randrange(2) else -1 for _ in range(3)]
  c=tuple(i*z for i,z in zip(inds,signs))
  if not any(bool((model>>(abs(l)-1))&1)==(l>0) for l in c):c=(-c[0],c[1],c[2])
  assert any(bool((model>>(abs(l)-1))&1)==(l>0) for l in c)
  f.append(c)
 return tuple(f)

CONTROLS={
 'W1_strict22_UNSAT':W1,
 'TW_strict22_SAT':TW,
 'H1_strict22_SAT':H1,
 'H2_strict22_SAT':h_ring(2),
 'H1_renamed_SAT':tuple(tuple(-l if abs(l)==1 else l for l in c) for c in H1),
 'XOR3_SAT':xor3(True),
 'XOR3_pair_UNSAT':xor3(True)+xor3(False),
 'Tseitin_K4_UNSAT':tseitin_k4_unsat(),
 'Horn_SAT':((1,),(-1,2),(-1,3),(-2,-3,4)),
 'Horn_UNSAT':((1,),(-1,2),(-2,)),
 'TwoSAT_SAT':((1,2),(-1,2),(-2,3)),
 'TwoSAT_UNSAT':((1,2),(-1,2),(1,-2),(-1,-2)),
 'Planted_dense_SAT':planted_dense(),
 'Negation_pair_SAT':((1,2,3),(-1,-2,-3)),
}

def nvars(F):return max(abs(l) for c in F for l in c)
def littrue(l,a):return bool((a>>(abs(l)-1))&1)==(l>0)
def clause_true_count(c,a):return sum(littrue(l,a) for l in c)
def clause_sat(c,a):return any(littrue(l,a) for l in c)
def hist(F,a):
 h=[0,0,0,0]
 for c in F:h[clause_true_count(c,a)]+=1
 return h

def targets(c,j):
 occ=[]; s={};u={}
 for t,l in enumerate(c):
  v=abs(l);p=l>0; s_val=int(p);u_val=1-s_val
  occ.append({'x_ij':f'x_{{{v},{j}}}','literal_offset':t,'signed_literal':l,'variable':v,'sign':'+' if p else '-',
              'S_local':s_val,'invert_S_is_U':1-s_val,'U_local':u_val,'invert_U_is_S':1-u_val})
  if v in s:assert False,'nonproper input'
  s[v]=s_val;u[v]=u_val
 return {'clause':j,'literals':list(c),'S_all_literals_true':s,'S_inversion_U':{i:1-v for i,v in s.items()},
        'U_all_literals_false':u,'U_inversion_S':{i:1-v for i,v in u.items()},'occurrences':occ}

def four_modes(C,D):
 first={abs(l):int(l>0) for l in C};second={abs(l):int(l>0) for l in D}
 shared=set(first)&set(second)
 same=sorted(i for i in shared if first[i]==second[i]);opp=sorted(i for i in shared if first[i]!=second[i])
 b=(not opp,not same,not same,not opp)
 # Independently enumerate all assignments to shared original variables, not independent indexed occurrences.
 source_vars=sorted(set(map(abs,C))|set(map(abs,D)))
 brute={k:False for k in ('SS','SU','US','UU')}
 for mask in range(1<<len(source_vars)):
  a={i:(mask>>k)&1 for k,i in enumerate(source_vars)}
  s=[sum(a[abs(l)]==int(l>0) for l in c) for c in (C,D)]
  if s[0] in (0,3) and s[1] in (0,3):brute[('S' if s[0]==3 else 'U')+('S' if s[1]==3 else 'U')]=True
 assert tuple(brute[k] for k in ('SS','SU','US','UU'))==b
 return {'same_shared':same,'opposite_shared':opp,'SS':b[0],'SU':b[1],'US':b[2],'UU':b[3]}

def triple_modes(F,inds):
 cs=[F[j] for j in inds]
 vs=sorted(set(abs(l) for c in cs for l in c))
 tested=[]
 for mm in range(8):
  modes=[('S' if (mm>>k)&1 else 'U') for k in range(3)]
  s={};contradict=False
  for c,mode in zip(cs,modes):
   for l in c:
    val=int(l>0) if mode=='S' else int(l<0)
    if abs(l) in s and s[abs(l)]!=val:contradict=True
    s[abs(l)]=val
  brute=False
  for mask in range(1<<len(vs)):
   a={v:(mask>>t)&1 for t,v in enumerate(vs)}
   if all(all(a[abs(l)]==(int(l>0) if mode=='S' else int(l<0)) for l in c) for c,mode in zip(cs,modes)):
    brute=True;break
  assert brute== (not contradict)
  tested.append({'modes':''.join(modes),'feasible':brute})
 return {'clauses':list(inds),'source_extremal_modes':tested}

def strict22(F):
 if len(F)*3!=4*nvars(F):return False
 if any(len(c)!=3 or len(set(map(abs,c)))!=3 for c in F):return False
 counts=collections.Counter(l for c in F for l in c)
 return all(counts[x]==2 and counts[-x]==2 for x in range(1,nvars(F)+1))

def source_connected(F):
 n=nvars(F);seen={1};stack=[1];clauses_seen=set()
 while stack:
  v=stack.pop()
  for j,c in enumerate(F):
   if any(abs(l)==v for l in c):
    clauses_seen.add(j)
    for l in c:
     if abs(l) not in seen:seen.add(abs(l));stack.append(abs(l))
 return len(seen)==n and len(clauses_seen)==len(F)

def signed_degrees(F):
 c=collections.Counter(l for clause in F for l in clause)
 return {v:{'+':c[v],'-':c[-v]} for v in range(1,nvars(F)+1)}

def signed_energy_coeffs(F):
 b=collections.Counter();w=collections.Counter();t=collections.Counter()
 for c in F:
  for l in c:b[abs(l)]+=1 if l>0 else -1
  for l,k in itertools.combinations(c,2):w[tuple(sorted((abs(l),abs(k))))]+=(1 if l>0 else -1)*(1 if k>0 else -1)
  if len(c)==3:t[tuple(sorted(map(abs,c)))]+=(-1 if sum(l<0 for l in c)%2 else 1)
 return {'B':dict(b),'W':dict(w),'T':dict(t)}

def fmt_coeff(dic):return [[list(key) if isinstance(key,tuple) else key,val] for key,val in sorted(dic.items())]

def raw_modes(F):
 pair=[]
 for j,k in itertools.combinations(range(len(F)),2):
  p=four_modes(F[j],F[k]);pair.append({'j':j,'k':k,**p})
 return pair

def find_resolvent(F):
 for j,k in itertools.combinations(range(len(F)),2):
  for pivot in sorted(set(map(abs,F[j]))&set(map(abs,F[k]))):
   a=next(l for l in F[j] if abs(l)==pivot)
   b=next(l for l in F[k] if abs(l)==pivot)
   if a!=-b:continue
   C=sorted(set(l for l in F[j]+F[k] if abs(l)!=pivot),key=lambda l:(abs(l),l))
   if any(-l in C for l in C):continue
   if len(C)>4:continue
   # If all resolvent literals false, the original parents force contradictory pivot values.
   cubes={abs(l):int(l<0) for l in C}
   tested=0
   for a_mask in range(1<<nvars(F)):
    if all(bool((a_mask>>(v-1))&1)==bool(z) for v,z in cubes.items()):
     tested+=1
     assert not (clause_sat(F[j],a_mask) and clause_sat(F[k],a_mask))
   return {'parents_original_jk':[j,k],'pivot_global_variable':pivot,'source_parent_clauses':[list(F[j]),list(F[k])],
           'resolvent':C,'forbidden_partial_cube':cubes,'full_assignments_independently_checked_in_cube':tested,
           'proof':'If every resolvent literal is false, parent j forces the pivot value making its original pivot literal true, while parent k forces the opposite; contradiction.'}
 return None

# Declared logical counters: each attempted literal evaluation and original clause read counts one.
# Other attempted operations (branch/probe etc) counted explicitly; these are not machine instructions.
class Meter:
 def __init__(self):self.k=collections.Counter()
 def bump(self,k,amount=1):self.k[k]+=amount
 def work(self):return sum(self.k.values())


def up(F,assignment,meter):
 # assignment is dict variable->0/1. Exhaustive deterministic UP. Output conflict clause or consistent assignment.
 alpha=dict(assignment)
 while True:
  changed=False
  for j,c in enumerate(F):
   meter.bump('source_clause_read')
   undec=[];hit=False
   for lit in c:
    meter.bump('literal_read')
    v=abs(lit)
    if v in alpha:
     if bool(alpha[v])==(lit>0):hit=True;break
    else:undec.append(lit)
   if hit:continue
   if not undec:
    meter.bump('UP_conflict')
    return alpha,j
   if len(undec)==1:
    l=undec[0];v=abs(l);val=int(l>0)
    if v in alpha and alpha[v]!=val:
     meter.bump('UP_conflict')
     return alpha,j
    if v not in alpha:
     alpha[v]=val;changed=True;meter.bump('UP_forced_assign')
  if not changed:return alpha,None

def dpll(F):
 n=nvars(F);meter=Meter();work_nodes=0;max_depth=0
 def rec(alpha,depth):
  nonlocal work_nodes,max_depth
  work_nodes+=1;meter.bump('node_entry');max_depth=max(max_depth,depth)
  a,conf=up(F,alpha,meter)
  if conf is not None:return {'contradiction_original_clause':conf}
  if len(a)==n:
   witness=sum((val<<(i-1)) for i,val in a.items())
   assert all(clause_sat(c,witness) for c in F)
   meter.bump('model_clause_verification',len(F))
   meter.bump('model_literal_verification',sum(map(len,F)))
   return {'witness_mask':witness}
  # all clauses may be already true with free vars; fix remaining false for complete witness
  if all(any(v in a and (bool(a[v])==(l>0)) for l in c for v in [abs(l)]) for c in F):
   witness=sum((a.get(i,0)<<(i-1)) for i in range(1,n+1))
   assert all(clause_sat(c,witness) for c in F)
   meter.bump('model_clause_verification',len(F));meter.bump('model_literal_verification',sum(map(len,F)))
   return {'witness_mask':witness}
  v=next(i for i in range(1,n+1) if i not in a)
  meter.bump('branch_decision')
  left=rec({**a,v:0},depth+1)
  if contains_witness(left):return {'branch_variable':v,'branch_zero':left,'branch_one':'skipped_after_SAT'}
  right=rec({**a,v:1},depth+1)
  return {'branch_variable':v,'branch_zero':left,'branch_one':right}
 proof=rec({},0)
 status='SAT' if contains_witness(proof) else 'UNSAT'
 return {'status':status,'nodes':work_nodes,'max_depth':max_depth,'selected_work':meter.work(),
         'events':dict(meter.k),'certificate':proof}

def contains_witness(node):
 if isinstance(node,str):return False
 if 'witness_mask' in node:return True
 if 'contradiction_original_clause' in node:return False
 return contains_witness(node['branch_zero']) or contains_witness(node['branch_one'])

def verify_certificate(F,node):
 # independent complete-tree checker only valid for UNSAT proof tree;
 # leaf contradiction may be reached from decisions via UP; branches cover both values.
 m=Meter();leaves=0
 def recurse(z,decisions):
  nonlocal leaves
  m.bump('proof_node')
  if 'contradiction_original_clause' in z:
   a,conf=up(F,decisions,m)
   assert conf is not None,'claimed contradiction leaf is satisfiable under decisions'
   leaves+=1
   return
  assert 'branch_variable' in z
  v=z['branch_variable'];assert v not in decisions
  assert z['branch_one']!='skipped_after_SAT'
  m.bump('proof_branch')
  recurse(z['branch_zero'],{**decisions,v:0})
  recurse(z['branch_one'],{**decisions,v:1})
 recurse(node,{})
 return {'validated':True,'leaves':leaves,'selected_checker_work':m.work(),'checker_events':dict(m.k)}

def e_only_endpoint_prepass(F):
 n=nvars(F);M=Meter();status='UNRESOLVED';witness=None
 # The exact E=N0+N3 complement theorem requires every ORIGINAL clause to have width 3.
 for c in F:
  M.bump('width_recognition_source_clause_read')
  if len(c)!=3 or len(set(map(abs,c)))!=3:
   return {'status':'UNRESOLVED','reason':'not_proper_width_three','witness_mask':None,'selected_work':M.work(),'events':dict(M.k)}
 # explicitly inspect both allzero, allone even though E same under complement
 for mask in (0,(1<<n)-1):
  M.bump('endpoint_examined')
  N=[0,0,0,0]
  for c in F:
   M.bump('source_clause_read')
   true_count=0
   for l in c:
    M.bump('literal_read');true_count+=littrue(l,mask)
   N[true_count]+=1
  E=N[0]+N[3]
  M.bump('E_comparison')
  if E<=1:
   # if E=1, choose the orientation with N0=0
   candidate=mask if N[0]==0 else mask^((1<<n)-1)
   if all(clause_sat(c,candidate) for c in F):
    M.bump('witness_clause_verification',len(F));M.bump('witness_literal_verification',sum(map(len,F)))
    status='SAT';witness=candidate;break
  # no UNSAT conclusion if E>=2
 return {'status':status,'witness_mask':witness,'selected_work':M.work(),'events':dict(M.k)}

def e_pair_greedy_probe(F):
 """Fully charged, bounded E-only strict-descent search, never declares UNSAT."""
 n=nvars(F);meter=Meter();edges=collections.Counter()
 for c in F:
  meter.bump('width_recognition_source_clause_read')
  if len(c)!=3 or len(set(map(abs,c)))!=3:
   return {'status':'UNRESOLVED','reason':'not_proper_width_three','selected_work':meter.work(),
           'events':dict(meter.k),'steps':0,'trace':[]}
  meter.bump('coefficient_source_clause_read')
  for l in c:meter.bump('coefficient_literal_read')
  for l,k in itertools.combinations(c,2):
   key=tuple(sorted((abs(l),abs(k))))
   edges[key]+=(1 if l>0 else -1)*(1 if k>0 else -1)
   meter.bump('coefficient_pair_update')
 edges={k:v for k,v in edges.items() if v}
 adj={i:[] for i in range(1,n+1)}
 for (i,j),w in edges.items():
  adj[i].append((j,w));adj[j].append((i,w))
  meter.bump('adjacency_edge_materialization',2)
 mask=0;s={i:-1 for i in range(1,n+1)}
 counts=[0,0,0,0]
 for c in F:
  meter.bump('initial_clause_read')
  t=0
  for l in c:meter.bump('initial_literal_read');t+=littrue(l,mask)
  counts[t]+=1
 E=counts[0]+counts[3];trace=[{'mask':mask,'E':E}]
 # Bounded, strict-decrease on exact NAE energy only.
 for step in range(min(n,len(F))):
  meter.bump('step_discovery')
  if E<=1:
   # E<=1 entails one of the complementary orientations is SAT, but check source.
   candidate=mask if counts[0]==0 else mask^((1<<n)-1)
   for c in F:
    meter.bump('witness_clause_verification')
    for l in c:meter.bump('witness_literal_verification')
   assert all(clause_sat(c,candidate) for c in F)
   return {'status':'SAT','witness_mask':candidate,'selected_work':meter.work(),
           'events':dict(meter.k),'steps':step,'trace':trace,'pair_edges':len(edges),
           'max_original_pair_degree':max(map(len,adj.values()),default=0)}
  best=(0,None)
  for i in range(1,n+1):
   meter.bump('candidate_probe')
   score=0
   for j,w in adj[i]:meter.bump('pair_weight_read');score+=w*s[j]
   diff=-(s[i]*score)//2 # strictly integer for width3 clause sum
   assert diff==-(s[i]*score)/2
   if diff<best[0]:best=(diff,i)
  if best[1] is None:break
  v=best[1];mask^=1<<(v-1);s[v]=-s[v];E+=best[0]
  meter.bump('global_variable_flip')
  # Update clause truth counters via the same global variable occurrence index.
  # For this compact probe store only 4-bucket counts, deriving old/new clause counts
  # from current coherent mask; all computational source accesses are charged.
  for c in F:
   if any(abs(l)==v for l in c):
    meter.bump('affected_clause_status_update')
    oldcount=0;newcount=0
    for l in c:
     meter.bump('update_literal_read',2)
     newcount+=littrue(l,mask)
     oldcount+=littrue(l,mask^(1<<(v-1)))
    counts[oldcount]-=1;counts[newcount]+=1
  assert counts[0]+counts[3]==E
  # Independent exhaustive sanity check is not a charged operation in this model:
  assert hist(F,mask)[0]+hist(F,mask)[3]==E
  trace.append({'mask':mask,'E':E,'flipped_variable':v,'delta_E':best[0]})
 if E<=1:
  candidate=mask if counts[0]==0 else mask^((1<<n)-1)
  for c in F:
   meter.bump('witness_clause_verification')
   for l in c:meter.bump('witness_literal_verification')
  assert all(clause_sat(c,candidate) for c in F)
  return {'status':'SAT','witness_mask':candidate,'selected_work':meter.work(),
          'events':dict(meter.k),'steps':len(trace)-1,'trace':trace,'pair_edges':len(edges),
          'max_original_pair_degree':max(map(len,adj.values()),default=0)}
 return {'status':'UNRESOLVED','selected_work':meter.work(),'events':dict(meter.k),
         'steps':len(trace)-1,'trace':trace,'pair_edges':len(edges),
         'max_original_pair_degree':max(map(len,adj.values()),default=0)}

def measured(callable_):
 tracemalloc.start();start=time.perf_counter()
 result=callable_()
 wall=time.perf_counter()-start
 current,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
 return result,{'wall_seconds':round(wall,7),'peak_tracemalloc_bytes':peak,
                'note':'instrumented separate same-input run; Python allocation tracking, NOT machine-independent peak bits'}

def ctrl_benchmark(F):
 base,base_machine=measured(lambda:dpll(F))
 pre=e_only_endpoint_prepass(F)
 greedy=e_pair_greedy_probe(F)
 # For each controller measure its own simultaneous peak Python allocation,
 # including fallback, without borrowing peak stats across separate executions.
 def ep_controller():
  p=e_only_endpoint_prepass(F)
  if p['status']=='SAT':return p
  return {'pre':p,'fallback':dpll(F)}
 def greedy_controller():
  p=e_pair_greedy_probe(F)
  if p['status']=='SAT':return p
  return {'probe':p,'fallback':dpll(F)}
 _,endpoint_machine=measured(ep_controller)
 _,greedy_machine=measured(greedy_controller)
 combined={'status':base['status'],'nodes':base['nodes'] if pre['status']=='UNRESOLVED' else 0,
           'selected_work':base['selected_work']+pre['selected_work'] if pre['status']=='UNRESOLVED' else pre['selected_work'],
           'prepass_work':pre['selected_work'],'fallback_work':base['selected_work'] if pre['status']=='UNRESOLVED' else 0,
           'prepass_status':pre['status'],'simultaneous_run_measurement':endpoint_machine}
 greedy_combined={'status':greedy['status'] if greedy['status']=='SAT' else base['status'],
          'selected_work':greedy['selected_work'] if greedy['status']=='SAT' else greedy['selected_work']+base['selected_work'],
          'probe_work':greedy['selected_work'],'fallback_work':0 if greedy['status']=='SAT' else base['selected_work'],
          'nodes':0 if greedy['status']=='SAT' else base['nodes'],'simultaneous_run_measurement':greedy_machine}
 proof=verify_certificate(F,base['certificate']) if base['status']=='UNSAT' else None
 return {'n':nvars(F),'m':len(F),'baseline':base,'baseline_simultaneous_run_measurement':base_machine,
         'E_prepass_plus_fallback':combined,
         'E_strict_descent_probe':greedy,'E_strict_descent_plus_fallback':greedy_combined,
         'independent_UNSAT_proof_checker':proof}

def run_primary(outdir):
 assert strict22(W1) and strict22(TW)
 assert source_connected(W1) and source_connected(TW)
 assert len(set(W1))==len(W1) and len(set(TW))==len(TW)
 assert all(set(map(abs,c))==set(map(abs,d)) for c,d in zip(W1,TW))
 assert [j for j,(c,d) in enumerate(zip(W1,TW)) if tuple(-l for l in c)==d]==list(SELECTED_CLAUSES)
 selected_balance={v:[sum((v in W1[j]) for j in SELECTED_CLAUSES),sum((-v in W1[j]) for j in SELECTED_CLAUSES)] for v in range(1,16)}
 assert all(x==[1,1] for x in selected_balance.values())
 eW=signed_energy_coeffs(W1);eT=signed_energy_coeffs(TW)
 assert eW['B']==eT['B'] and all(z==0 for z in eW['B'].values())
 assert eW['W']==eT['W']
 pairW=raw_modes(W1);pairT=raw_modes(TW)
 changes=[(p['j'],p['k']) for p,q in zip(pairW,pairT) if any(p[k]!=q[k] for k in ('SS','SU','US','UU'))]
 from collections import Counter
 ptag=lambda p:(p['SS'],p['SU'],p['US'],p['UU'])
 pairhistW=Counter(map(ptag,pairW));pairhistT=Counter(map(ptag,pairT))
 assert pairhistW==pairhistT
 # choose original 3-clause source triples; independently enumerate full global assignments over their union
 subset=[(0,1,2),(0,3,5),(2,4,6),(7,9,12),(12,14,16),(14,16,17)]
 multiW=[triple_modes(W1,tri) for tri in subset]
 multiT=[triple_modes(TW,tri) for tri in subset]
 Ehist=Counter();modelcounts=[0,0]; modelsT=[]; ModelW=[]; minE=999; argmin=[]
 # external exhaustive oracle used solely for finite verification, NOT used by solver
 for a in range(1<<15):
  p=hist(W1,a);q=hist(TW,a)
  comp=(1<<15)-1^a
  pco=hist(W1,comp);qco=hist(TW,comp)
  assert p==pco[::-1] and q==qco[::-1]
  E=p[0]+p[3]
  assert E==q[0]+q[3]
  if E<minE:minE=E;argmin=[a]
  elif E==minE:argmin.append(a)
  Ehist[E]+=1
  if p[0]==0:modelcounts[0]+=1;ModelW.append(a)
  if q[0]==0:modelcounts[1]+=1;modelsT.append(a)
 assert modelcounts==[0,270] and minE==2 and 26 in modelsT
 trail=[]
 for a in (0,2,10,26,26^((1<<15)-1),(1<<15)-1):
  p=hist(W1,a);q=hist(TW,a)
  trail.append({'complete_global_assignment_mask':a,'TRUE_variable_indices':[i for i in range(1,16) if a>>(i-1)&1],
                'W1_clause_true_literal_counts':[clause_true_count(c,a) for c in W1],
                'TW_clause_true_literal_counts':[clause_true_count(c,a) for c in TW],
                'W1_N0_N1_N2_N3':p,'TW_N0_N1_N2_N3':q,'E_both':p[0]+p[3]})
 forbidden=find_resolvent(TW)
 report={
  'status':'PASS','run':'NAE_ENERGY_TWIN246','date_local':'2026-10-30T02:36:00-07:00','seed':'deterministic no randomness',
  'source_W1':{'n':15,'m':20,'original_clauses':[list(c) for c in W1],
               'per_source_clause_S_U_and_inversions':[targets(c,j) for j,c in enumerate(W1)],
               'indexed_clause_pair_SS_SU_US_UU':pairW,'selected_triple_modes':multiW,
               'signed_occurrence_counts':signed_degrees(W1)},
  'source_TW':{'n':15,'m':20,'original_clauses':[list(c) for c in TW],
               'per_source_clause_S_U_and_inversions':[targets(c,j) for j,c in enumerate(TW)],
               'indexed_clause_pair_SS_SU_US_UU':pairT,'selected_triple_modes':multiT,
               'signed_occurrence_counts':signed_degrees(TW)},
  'selected_clause_literal_inversions_zero_based':list(SELECTED_CLAUSES),
  'selection_every_variable_has_exactly_one_positive_and_one_negative':selected_balance,
  'same_unsigned_clause_supports':True,'same_all_variable_signed_2plus_2minus_counts':True,
  'both_incidence_graphs_connected':True,'both_duplicate_free':True,
  'same_full_E_profile_for_each_of_32768_coherent_assignments':True,
  'same_quadratic_pair_coefficients':fmt_coeff(eW['W']),
  'linear_coefficients_all_zero':True,'triple_coefficients_changed':sum(eW['T'][k]!=eT['T'][k] for k in set(eW['T'])|set(eT['T'])),
  'same_pair_mode_aggregate_histogram':dict((str(k),v) for k,v in pairhistW.items()),
  'full_indexed_pair_mode_changes':changes,'full_indexed_pair_mode_changes_count':len(changes),
  'models':{'W1_unsat':modelcounts[0],'TW_sat':modelcounts[1],'TW_first_sat_masks':modelsT[:20],
            'TW_witness_26':26},'E_distribution_all_coherent_assignments':dict(Ehist),
  'min_E':minE,'min_E_count':len(argmin),
  'endpoints_intermediate_multiple_flip_trail':trail,
  'certified_forbidden_cube_direct_original_source_resolution':forbidden,
  'global_complement_checks':2*(1<<15),'pair_mode_checks':4*(len(pairW)+len(pairT)),
  'tested_triple_joint_modes':8*(len(multiW)+len(multiT)),
  'note':'Full indexed matrices differ; only E(a) and aggregate pair mode histograms match. External exhaustive assignments do not constitute polynomial-time solver.'
 }
 path=outdir/'LSPV4_NAE_ENERGY_TWIN246_primary_raw.json'
 path.write_text(json.dumps(report,indent=2,sort_keys=True))
 return {'file':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size,
         'models':modelcounts,'pair_modes_changed':len(changes),'min_E':minE,'E_dist':dict(Ehist),'full_assignment_checks':32768,'source_forbidden_cube':forbidden}

def run_benchmark(outdir):
 data={'status':'PASS','run':'NAE_ENERGY_TWIN246','benchmarks':{},'tests':len(CONTROLS)}
 for name,F in CONTROLS.items():
  d=ctrl_benchmark(F)
  data['benchmarks'][name]=d
 path=outdir/'LSPV4_NAE_ENERGY_TWIN246_benchmark_raw.json'
 path.write_text(json.dumps(data,indent=2,sort_keys=True))
 return {'file':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size,
         'summary':{name:{'status':b['baseline']['status'],'nodes':b['baseline']['nodes'],
                          'base_work':b['baseline']['selected_work'],
                          'prepass_work':b['E_prepass_plus_fallback']['prepass_work'],
                          'combined_work':b['E_prepass_plus_fallback']['selected_work'],
                          'E_strict_descent_trace':b['E_strict_descent_probe'].get('trace'),
                          'E_strict_descent_work':b['E_strict_descent_plus_fallback']['selected_work'],
                          'E_strict_descent_steps':b['E_strict_descent_probe'].get('steps'),
                          'baseline_peak_python_bytes':b['baseline_simultaneous_run_measurement']['peak_tracemalloc_bytes'],
                          'E_prepass_peak_python_bytes':b['E_prepass_plus_fallback']['simultaneous_run_measurement']['peak_tracemalloc_bytes'],
                          'E_descent_peak_python_bytes':b['E_strict_descent_plus_fallback']['simultaneous_run_measurement']['peak_tracemalloc_bytes'],
                          'independent_UNSAT_proof_checker_work':(b['independent_UNSAT_proof_checker'] or {}).get('selected_checker_work')}
                    for name,b in data['benchmarks'].items()}}

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--phase',required=True,choices=('primary','benchmark'))
 parser.add_argument('--outdir',default=os.path.dirname(os.path.abspath(__file__)))
 args=parser.parse_args();outdir=Path(args.outdir);outdir.mkdir(parents=True,exist_ok=True)
 start=time.perf_counter();r=run_primary(outdir) if args.phase=='primary' else run_benchmark(outdir)
 r['wall_seconds']=round(time.perf_counter()-start,3)
 print(json.dumps(r,sort_keys=True))
