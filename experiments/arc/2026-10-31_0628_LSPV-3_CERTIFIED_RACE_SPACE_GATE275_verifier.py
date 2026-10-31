#!/usr/bin/env python3
"""Independent from-source verifier for run275; imports NO producer functions."""
import collections, copy, hashlib, json, math, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
raw=json.loads((HERE/'raw275.json').read_text())
checks=collections.Counter()
def ck(b,label):
 checks[label]+=1
 if not b:raise AssertionError(f'verification failed: {label}')
def source_true_clause(C,a):return any(((a>>(abs(l)-1))&1)==int(l>0) for l in C)
def formula_sat(F,a):return all(source_true_clause(C,a) for C in F)
def partial_value(lit,A):
 if abs(lit) not in A:return None
 return A[abs(lit)] if lit>0 else not A[abs(lit)]
def independent_ground(F,n):
 any_sat=False;num_sat=0
 for a in range(1<<n):
  if formula_sat(F,a):num_sat+=1;any_sat=True
  checks['exhaustive_complete_assignments']+=1
 return 'SAT' if any_sat else 'UNSAT',num_sat

def verify_cert(F,n,c):
 if c['status']=='SAT':
  a=sum(int(bit)<<i for i,bit in enumerate(c['model']))
  return len(c['model'])==n and formula_sat(F,a)
 if c['status']!='UNSAT':return False
 if c['method']=='HORN':
  forced=set()
  for v,j in c['trace']:
   if j<0 or j>=len(F):return False
   C=F[j]
   if v not in C or sum(l>0 for l in C)!=1:return False
   if any(-l not in forced for l in C if l<0):return False
   forced.add(v)
   checks['horn_proof_steps']+=1
  if not 0<=c['conflict']<len(F):return False
  return all(l<0 and (-l in forced) for l in F[c['conflict']])
 if c['method']=='KROM':
  if 'empty' in c:return 0<=c['empty']<len(F) and F[c['empty']]==[]
  v=c['variable']
  if not (1<=v<=n):return False
  def encode(l):return 2*(abs(l)-1)+int(l<0)
  for source,target,steps in [(encode(v),encode(-v),c['paths'][0]),(encode(-v),encode(v),c['paths'][1])]:
   current=source
   for a,b,j in steps:
    if current!=a or j<0 or j>=len(F):return False
    C=F[j]
    if not 1<=len(C)<=2:return False
    x,y=C[0],C[-1]
    if (a,b) not in ((encode(-x),encode(y)),(encode(-y),encode(x))):return False
    current=b;checks['krom_proof_edges']+=1
   if current!=target:return False
  return True
 if c['method']=='AFFINE':
  by_support=collections.defaultdict(list)
  for C in F:
   if len(C)!=3 or len({abs(x) for x in C})!=3:return False
   key=tuple(sorted(abs(x) for x in C))
   by_support[key].append(C)
  equations=[]
  for key,clauses in sorted(by_support.items()):
   if len(clauses)!=4:return False
   excluded=set()
   for C in clauses:
    excluded.add(tuple(int((-v) in C) for v in key))
   if len(excluded)!=4:return False
   parity={sum(a)&1 for a in excluded}
   if len(parity)!=1:return False
   forbidden=parity.pop()
   expected={tuple((i>>j)&1 for j in range(3)) for i in range(8) if i.bit_count()%2==forbidden}
   if excluded!=expected:return False
   equations.append((sum(1<<(v-1) for v in key),1-forbidden))
  mask=0;rhs=0
  if not c['core'] or len(c['core'])!=len(set(c['core'])):return False
  for j in c['core']:
   if not 0<=j<len(equations):return False
   mask^=equations[j][0];rhs^=equations[j][1];checks['affine_xor_proof_rows']+=1
  return mask==0 and rhs==1
 if c['method']=='DPLL':
  def valid(node,partial):
   cur=dict(partial)
   checks['dpll_proof_nodes']+=1
   for lit,j in node.get('forced',[]):
    if not 0<=j<len(F):return False
    C=F[j];tr=[partial_value(x,cur) for x in C]
    if True in tr or sum(t is None for t in tr)!=1:return False
    if lit not in C or lit in cur or abs(lit) in cur:return False
    if tr[C.index(lit)] is not None:return False
    cur[abs(lit)]=lit>0
   if 'conflict' in node:
    j=node['conflict']
    return 0<=j<len(F) and all(partial_value(l,cur) is False for l in F[j])
   v=node.get('branch')
   if not isinstance(v,int) or v<1 or v>n or v in cur:return False
   left=dict(cur);left[v]=False
   right=dict(cur);right[v]=True
   return valid(node['zero'],left) and valid(node['one'],right)
  return valid(c['proof'],{})
 return False

def extreme_controls(F,n,c):
 ck(len(c['original_clause_targets'])==len(F),'original_clause_count')
 for j,C in enumerate(F):
  row=c['original_clause_targets'][j]
  ck(row['index']==j and len(row['occurrences'])==len(C),'local_extreme_source')
  s={str(abs(l)):int(l>0) for l in C}
  u={str(abs(l)):int(l<0) for l in C}
  ck(row['S']==s and row['U']==u,'S_U_inverse')
  for signed,occ in zip(C,row['occurrences']):
   ck((occ['variable'],occ['sign'],occ['S'],occ['U'])==(abs(signed),int(signed>0),int(signed>0),int(signed<0)),'signed_occurrence')
   ck(occ['inverted_S_equals_U']==occ['U'] and occ['inverted_U_equals_S']==occ['S'],'local_inversion')
 index={(x['Cj'],x['Ck']):x for x in c['pair_compatibility']}
 ck(len(index)==len(F)*(len(F)-1)//2,'pair_count')
 for j in range(len(F)):
  for k in range(j+1,len(F)):
   a,b=F[j],F[k];vs=sorted(set(map(abs,a+b)))
   actual={tag:False for tag in ('SS','SU','US','UU')}
   for bits in range(1<<len(vs)):
    assn=dict(zip(vs,[(bits>>i)&1 for i in range(len(vs))]))
    ta=sum(assn[abs(l)]==(l>0) for l in a)
    tb=sum(assn[abs(l)]==(l>0) for l in b)
    for x,y,t in ((len(a),len(b),'SS'),(len(a),0,'SU'),(0,len(b),'US'),(0,0,'UU')):
     if ta==x and tb==y:actual[t]=True
   for mode in actual:ck(index[j,k][mode] is actual[mode],'exact_pair_enumeration')
 for t in c['global_flip_trail']:
  a=t['assignment_bits'];b=t['complement_bits']
  ck(b==((1<<n)-1)^a,'global_complement')
  source=[sum(((a>>(abs(l)-1))&1)==int(l>0) for l in C) for C in F]
  comp=[sum(((b>>(abs(l)-1))&1)==int(l>0) for l in C) for C in F]
  ck(source==t['t_source'] and comp==t['t_complement'],'global_coherent_counts')
  ck(all(x+y==len(C) for x,y,C in zip(source,comp,F)),'clause_complement')
  for i in range(4):ck(t['counts'][str(i)]==sum(x==i for x in source),'N_categories')

policies=raw['policies'];verified=[]
for case in raw['cases']:
 F=case['original_clauses'];n=case['n'];label=case['label']
 ground,models=independent_ground(F,n)
 ck(ground==label,'ground_label');ck(case['race']['status']==ground,'portfolio_label')
 ck(verify_cert(F,n,case['race']['proof']),'race_certificate')
 extreme_controls(F,n,case['controls'])
 baseline=case['per_policy']['DPLL_ASC'];ck(baseline['state']==ground,'baseline_exact')
 for policy,entry in case['per_policy'].items():
  ck(entry['state'] in ('SAT','UNSAT','UNRESOLVED'),'policy_termination')
  if entry['state']!='UNRESOLVED':ck(entry['state']==ground,'policy_soundness')
 # Independently replay all from-scratch dyadic restart clocks from terminal profiles.
 total=0;completed=set();winner=None
 for round_j,row in enumerate(case['race']['rounds']):
  B=1<<round_j
  ck(row['budget']==B,'budget_doubling')
  for policy in policies:
   if policy in completed:continue
   source=case['per_policy'][policy];observed=row['policies'].get(policy)
   ck(observed is not None,'scheduled_policy_present')
   expected_state='BUDGET' if source['work']>B else source['state']
   expected_work=B+1 if expected_state=='BUDGET' else source['work']
   ck(observed['state']==expected_state and observed['work']==expected_work,'restart_replay')
   ck(sum(observed['tags'].values())==observed['work'],'full_charged_tags')
   total+=observed['work']
   if expected_state=='UNRESOLVED':completed.add(policy)
   if expected_state in ('SAT','UNSAT'):
    winner=policy;break
  if winner:break
 ck(winner==case['race']['winner'] and total==case['race']['total_work'],'winner_and_work')
 best=min(p['work'] for p in case['per_policy'].values() if p['state'] in ('SAT','UNSAT'))
 ck(case['best_verified_work']==best,'best_complete_cost')
 J=math.ceil(math.log2(best))
 ck(total<=len(policies)*(4*best+J+1),'portfolio_competitive_bound')
 ck(case['race']['physically_serialized_ordinary_children']==0 and case['race']['guest_A_calls']==0,'no_arc_child_claim')
 verified.append({'name':case['name'],'label':ground,'models':models,'race':total,'baseline':baseline['work']})
# Deliberate malicious proof controls against verifier, not producer-produced corrupted records.
case=next(c for c in raw['cases'] if c['name']=='SWAP6_SAT');bad=copy.deepcopy(case['race']['proof'])
# Make a complete assignment falsify the first original clause.
for lit in case['original_clauses'][0]:bad['model'][abs(lit)-1]=int(lit<0)
ck(not verify_cert(case['original_clauses'],case['n'],bad),'reject_corrupt_sat_model')
case=next(c for c in raw['cases'] if c['name']=='W1_UNSAT');bad=copy.deepcopy(case['race']['proof'])
bad['proof']['branch']=0
ck(not verify_cert(case['original_clauses'],case['n'],bad),'reject_corrupt_dpll_branch')
case=next(c for c in raw['cases'] if c['name']=='XOR6_UNSAT');bad=copy.deepcopy(case['race']['proof'])
bad['core']=bad['core']+[bad['core'][0]]
ck(not verify_cert(case['original_clauses'],case['n'],bad),'reject_corrupt_xor_core')
case=next(c for c in raw['cases'] if c['name']=='HORN_CHAIN_UNSAT');bad=copy.deepcopy(case['race']['proof'])
bad['trace'][0][0]=999
ck(not verify_cert(case['original_clauses'],case['n'],bad),'reject_corrupt_horn_trace')
case=next(c for c in raw['cases'] if c['name']=='KROM_UNSAT');bad=copy.deepcopy(case['race']['proof'])
bad['paths'][0][0][1]=999
ck(not verify_cert(case['original_clauses'],case['n'],bad),'reject_corrupt_krom_path')
result={'passed':True,'cases':len(verified),'SAT':sum(z['label']=='SAT' for z in verified),'UNSAT':sum(z['label']=='UNSAT' for z in verified),'checks_by_type':dict(checks),'total_independent_checks':sum(checks.values()),'invalid_certificates_rejected':5,'cases_detail':verified}
(HERE/'verification275.json').write_text(json.dumps(result,indent=2,sort_keys=True))
print(json.dumps({k:v for k,v in result.items() if k!='cases_detail'},indent=2))
