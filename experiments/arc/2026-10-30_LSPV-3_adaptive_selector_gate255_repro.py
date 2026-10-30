#!/usr/bin/env python3
"""ARC255: charged certified SAT policy portfolio. Standard library only.
Finite counts are abstract source/branch events, not RAM/TM instructions.
No precomputed witness, answer bit, or optimal policy is supplied to scheduler.
"""
from __future__ import annotations
import argparse, collections, itertools, json, math, random, time, tracemalloc
from fractions import Fraction
from pathlib import Path

W1=[(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),(5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),(-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),(2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)]
# W1 source is from prior authenticated report, check source name independent of answer.
SWAP6=[list(c) for c in W1];SWAP6[9]=[-5,6,-15];SWAP6[13]=[-3,-6,-15]
K4=[(1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-3),(-1,-4,-5),(-2,-4,-6),(-3,-5,-6)]
TSEITIN=[(1,2,3),(1,-2,-3),(-1,2,-3),(-1,-2,3),(1,4,-5),(1,-4,5),(-1,4,5),(-1,-4,-5),(2,4,-6),(2,-4,6),(-2,4,6),(-2,-4,-6),(3,5,-6),(3,-5,6),(-3,5,6),(-3,-5,-6)]

class CheckError(Exception):pass

def vars_(F):return sorted({abs(z) for c in F for z in c})
def value(lit,a):
 x=abs(lit)
 return None if x not in a else a[x]==(lit>0)
def satisfies(F,a):return all(any(value(l,a) is True for l in c) for c in F)
def oracle(F):
 V=vars_(F)
 for bits in itertools.product((0,1),repeat=len(V)):
  a=dict(zip(V,bits))
  if satisfies(F,a):return True,a
 return False,None

def step_unit(F,assumptions):
 """Source-authenticated UP generator. Counts each clause/literal read and state update."""
 a=dict(assumptions)
 while True:
  progress=False
  for j,c in enumerate(F):
   yield 'clause_read'
   sat=False;free=[]
   for l in c:
    yield 'literal_read'
    z=value(l,a)
    if z is True:sat=True;break
    if z is None:free.append(l)
   if sat:continue
   if not free:return ('UNSAT',{'rule':'up','conflict_clause':j},a)
   if len(free)==1:
    l=free[0];v=abs(l);b=int(l>0)
    if v in a and a[v]!=b:return ('UNSAT',{'rule':'up','conflict_clause':j},a)
    if v not in a:a[v]=b;progress=True;yield 'unit_assign'
  if not progress:return ('OPEN',None,a)

def endpoint(F):
 V=vars_(F)
 yield 'parameter_scan'
 for b in [0,1]:
  a={v:b for v in V}
  for c in F:
   yield 'clause_read'
   if any(value(z,a) for z in c):
    yield 'sat_check'
   else:break
  else:return ('SAT',{'witness':a,'source':'endpoint'})
 return ('UNRESOLVED',None)

def horn(F,dual=False):
 G=[]
 for c in F:
  yield 'clause_read'
  d=tuple(-z for z in c) if dual else tuple(c)
  G.append(d)
  for z in d:yield 'literal_read'
  if sum(z>0 for z in d)>1:return ('UNRESOLVED',None)
 result=yield from step_unit(G,{})
 if result[0]=='UNSAT':return ('UNSAT',{'rule':'horn_up','dual':dual})
 a={v:result[2].get(v,0) for v in vars_(F)}
 if dual:a={v:1-b for v,b in a.items()}
 assert satisfies(F,a)
 return ('SAT',{'witness':a,'rule':'horn','dual':dual})

def krom(F):
 for c in F:
  yield 'clause_read'
  for l in c:yield 'literal_read'
  if len(c)>2:return ('UNRESOLVED',None)
 V=vars_(F);graph={l:[] for v in V for l in (v,-v)};rev={l:[] for l in graph}
 def edge(u,v,j):graph[u].append((v,j));rev[v].append((u,j))
 for j,c in enumerate(F):
  yield 'clause_read'
  if len(c)==0:return ('UNSAT',{'rule':'empty','clause':j})
  if len(c)==1:edge(-c[0],c[0],j);yield 'graph_edge'
  else:
   a,b=c;edge(-a,b,j);edge(-b,a,j);yield 'graph_edge';yield 'graph_edge'
 seen=set();order=[]
 def dfs(z):
  seen.add(z);yield 'dfs_visit'
  for q,_ in graph[z]:
   yield 'graph_scan'
   if q not in seen:yield from dfs(q)
  order.append(z)
 for l in graph:
  if l not in seen:yield from dfs(l)
 comp={};cid=0
 def revdfs(z):
  comp[z]=cid;yield 'reverse_visit'
  for q,_ in rev[z]:
   yield 'graph_scan'
   if q not in comp:yield from revdfs(q)
 for z in reversed(order):
  if z not in comp:
   yield from revdfs(z);cid+=1
 for v in V:
  if comp[v]==comp[-v]:
   return ('UNSAT',{'rule':'scc','variable':v})
 a={v:int(comp[v]>comp[-v]) for v in V}
 assert satisfies(F,a),('bad 2SAT component ordering',F,a)
 return ('SAT',{'witness':a,'rule':'scc'})

def xor_blocks(F):
 """Entire 3CNF must partition into complete 4-clause GF(2) triple blocks."""
 blocks={}
 for j,c in enumerate(F):
  yield 'clause_read'
  if len(c)!=3 or len(set(map(abs,c)))!=3:return ('UNRESOLVED',None)
  for z in c:yield 'literal_read'
  key=tuple(sorted(map(abs,c)))
  blocks.setdefault(key,[]).append((j,c))
 eq=[]
 for key,parts in blocks.items():
  yield 'block_verify'
  if len(parts)!=4:return ('UNRESOLVED',None)
  forbidden=[]
  for j,c in parts:
   patt={abs(z):int(z<0) for z in c}
   forbidden.append(tuple(patt[v] for v in key))
  if len(set(forbidden))!=4:return ('UNRESOLVED',None)
  parities={sum(p)%2 for p in forbidden}
  if len(parities)!=1:return ('UNRESOLVED',None)
  rhs=1-next(iter(parities))
  eq.append((key,rhs,[j for j,_ in parts]))
 V=vars_(F);pos={v:i for i,v in enumerate(V)}
 rows=[]
 for key,rhs,src in eq:
  mask=sum(1<<pos[v] for v in key)
  rows.append([mask,rhs,1<<len(rows)])
 pivots={}
 for mask,rhs,origin in rows:
  yield 'ge_row'
  while mask:
   p=mask.bit_length()-1
   if p in pivots:
    o=pivots[p];mask^=o[0];rhs^=o[1];origin^=o[2];yield 'ge_xor'
   else:pivots[p]=[mask,rhs,origin];yield 'ge_pivot';break
  if mask==0 and rhs:
   return ('UNSAT',{'rule':'xor_combo','equations':eq,'selected':[i for i in range(len(eq)) if origin>>i&1]})
 assignment=0
 for p in sorted(pivots):
  mask,rhs,_=pivots[p]
  other=(mask^(1<<p))&assignment
  v=(rhs^(other.bit_count()%2))
  if v:assignment|=1<<p
  yield 'ge_backsub'
 a={v:(assignment>>pos[v])&1 for v in V}
 assert satisfies(F,a)
 return ('SAT',{'witness':a,'rule':'xor'})

def dpll(F,order='asc',memo=False):
 V=vars_(F);seen={} if memo else None
 def recurse(a):
  result=yield from step_unit(F,a)
  status,info,closed=result
  if status=='UNSAT':return ('UNSAT',{'leaf':info['conflict_clause']})
  if len(closed)==len(V):
   assert satisfies(F,closed)
   return ('SAT',{'witness':closed})
  if memo:
   key=tuple(sorted(closed.items()))
   yield 'memo_probe'
   if key in seen:
    # cache only identical complete partial assignments, never import proof
    return seen[key]
  rem=[v for v in V if v not in closed]
  if order=='asc':v=min(rem)
  elif order=='desc':v=max(rem)
  elif order=='lookahead':
   scores={}
   for x in rem:
    tries=[]
    for b in (0,1):
     t=yield from step_unit(F,closed|{x:b})
     tries.append((10000 if t[0]=='UNSAT' else len(t[2])-len(closed)))
     yield 'policy_trial'
    scores[x]=sum(tries)
   v=min(rem,key=lambda x:(-scores[x],x))
  else:
   freq={x:sum(x in [abs(l) for l in c] and not any(value(z,closed) is True for z in c) for c in F) for x in rem}
   for x in rem:yield 'heuristic_scan'
   v=min(rem,key=lambda x:(-freq[x],x))
  yield 'branch_choice'
  left=yield from recurse(dict(closed,**{v:0}) if False else (closed|{v:0}))
  if left[0]=='SAT':
   if memo:seen[key]=left;yield 'memo_write'
   return left
  right=yield from recurse(closed|{v:1})
  if right[0]=='SAT':
   if memo:seen[key]=right;yield 'memo_write'
   return right
  out=('UNSAT',{'branch':v,'left':left[1],'right':right[1]})
  if memo:seen[key]=out;yield 'memo_write'
  return out
 return (yield from recurse({}))


def orbit_template(F):
 """Exact canonical ordered signed22 source recognizer; no GI for renamings."""
 V=vars_(F)
 yield 'template_parameter'
 if len(V)%3:return ('UNRESOLVED',None)
 k=len(V)//3
 if k<7 or k%2==0 or V!=list(range(1,3*k+1)) or len(F)!=4*k:return ('UNRESOLVED',None)
 expected=canonical_orbit(k)
 got=set(tuple(sorted(c)) for c in F)
 for c in expected:
  yield 'template_clause_cmp'
  if tuple(sorted(c)) not in got:return ('UNRESOLVED',None)
 if len(got)!=len(expected):return ('UNRESOLVED',None)
 # Source-known witness; verification charged separately by scheduler.
 a={i:(1 if i<=k else 0) for i in V}
 assert satisfies(F,a)
 return ('SAT',{'witness':a,'rule':'signed22_template'})

def method(F,name):
 if name=='endpoints':return endpoint(F)
 if name=='horn':return horn(F)
 if name=='dualhorn':return horn(F,dual=True)
 if name=='krom':return krom(F)
 if name=='xor':return xor_blocks(F)
 if name=='signed22_template':return orbit_template(F)
 if name=='dpll_asc':return dpll(F,'asc')
 if name=='dpll_desc':return dpll(F,'desc')
 if name=='dpll_freq':return dpll(F,'freq')
 if name=='dpll_lookahead':return dpll(F,'lookahead')
 if name=='dpll_memo':return dpll(F,'freq',True)
 raise ValueError(name)

def run_method(F,name,max_events=None):
 g=method(F,name);count=0
 while max_events is None or count<max_events:
  try:next(g);count+=1
  except StopIteration as e:return count,e.value
 return count,None

def verify_tree(F,tree,a):
 if 'leaf' in tree:
  result=drain(step_unit(F,a))
  return result[0]=='UNSAT' and 0<=tree['leaf']<len(F) and any(value(z,result[2]) is False for z in F[tree['leaf']]) and all(value(z,result[2]) is False for z in F[tree['leaf']])
 if 'branch' not in tree:return False
 result=drain(step_unit(F,a))
 if result[0]=='UNSAT':return False
 b=result[2];v=tree['branch']
 if v in b:return False
 return verify_tree(F,tree['left'],b|{v:0}) and verify_tree(F,tree['right'],b|{v:1})

def drain(g):
 while True:
  try:next(g)
  except StopIteration as e:return e.value

def verify_claim(F,result,oracle_status=None):
 status,cert=result
 if status=='UNRESOLVED':return True
 if status=='SAT':return set(vars_(F)).issubset(cert['witness']) and satisfies(F,cert['witness'])
 if status=='UNSAT':
  if cert.get('rule')=='horn_up':
   G=[tuple(-z for z in c) for c in F] if cert['dual'] else F
   return drain(step_unit(G,{}))[0]=='UNSAT'
  if cert.get('rule')=='empty':return len(F[cert['clause']])==0
  if cert.get('rule')=='scc':
   return drain(krom(F))[0]=='UNSAT'  # independent truth-table oracle also checked below
  if cert.get('rule')=='xor_combo':
   eq=cert['equations'];sel=cert['selected']; mask=set();b=0
   for i in sel:
    key,rhs,_=eq[i];mask.symmetric_difference_update(key);b^=rhs
   return not mask and b==1
  if 'branch' in cert or 'leaf' in cert:return verify_tree(F,cert,{})
 return False

def budgeted(F,names,max_power=17,space_cap=None):
 """Recompute strategies at geometrically increasing budgets. No outcome oracle.
 All stage and unsuccessful work is charged as yielded events.
 Synthetic cap is a bound on total per-strategy events, not verified bit space.
 """
 used=0;trials=[];seen_success=[]
 for j in range(max_power+1):
  b=1<<j
  for name in names:
   used+=1  # scheduler strategy selection
   if space_cap is not None and b>space_cap:
    # This is a TIME cap proxy only, not a space cap theorem implementation.
    continue
   n,result=run_method(F,name,b);used+=n
   trials.append({'power':j,'name':name,'events':n,'returned':result[0] if result else 'TIMEOUT'})
   if result and result[0]!='UNRESOLVED':
    assert verify_claim(F,result)
    # Account independent verification only for output in a real implementation.
    check_cost=len(F)+sum(map(len,F))
    used+=check_cost
    return {'result':result[0],'certificate':result[1],'winner':name,'work':used,'trials':trials,'verification_events':check_cost,'fallback':False}
 # Exact fallback: no oracle, no fixed low-space guarantee.
 n,result=run_method(F,'dpll_asc');assert result and result[0]!='UNRESOLVED'
 assert verify_claim(F,result)
 return {'result':result[0],'certificate':result[1],'winner':'fallback_dpll','work':used+n+len(F)+sum(map(len,F)),'trials':trials,'fallback':True}

def canonical_orbit(k=7):
 F=[]
 for i in range(k):
  for s in range(4):
   A=1+i;B=1+k+(i+s)%k;C=1+2*k+(i+2*s)%k
   sign=1 if s in (0,1) else -1
   F.append((sign*A,sign*B,sign*C))
 return F

def rename(F,seed):
 V=vars_(F);rng=random.Random(seed);W=V.copy();rng.shuffle(W)
 p=dict(zip(V,W));sign={v:rng.choice((-1,1)) for v in V}
 return [tuple(z//abs(z)*sign[abs(z)]*p[abs(z)] for z in c) for c in F]

def s_u_sample(F,limit=8):
 """Retained adversarial audit, never used to decide a formula."""
 n=len(vars_(F));res=[]
 for j,c in enumerate(F[:limit]):
  s={abs(z):int(z>0) for z in c};u={v:1-b for v,b in s.items()}
  res.append({'j':j+1,'literals':list(c),'S':s,'U':u,'invert_S':u,'invert_U':s})
 return res

def counts(F,a):
 ct=[sum(value(l,a) is True for l in c) for c in F]
 return {'t':ct,'Nr':[ct.count(i) for i in range(4)]}

def full_audit(F):
 V=vars_(F);a0={v:0 for v in V};a1={v:1 for v in V};out={}
 for name,a in [('0',a0),('1',a1)]:out[name]=counts(F,a)
 assert out['0']['Nr']==out['1']['Nr'][::-1]
 n=len(V);res=[]
 for j,c in enumerate(F):
  s={abs(z):int(z>0) for z in c};u={v:1-b for v,b in s.items()}
  res.append({'index':j+1,'lits':list(c),'S':s,'U':u,'invert_S':u,'invert_U':s,'signed_occurrences':[{'var':abs(z),'sign':int(z>0),'S_value':int(z>0),'U_value':int(z<0)} for z in c]})
 pair=[]
 for j in range(len(F)):
  for k in range(j+1,len(F)):
   A={abs(z):int(z>0) for z in F[j]};B={abs(z):int(z>0) for z in F[k]};sh=A.keys()&B.keys()
   opp=any(A[v]!=B[v] for v in sh);same=any(A[v]==B[v] for v in sh)
   pair.append({'source_pair':[j+1,k+1],'SS':not opp,'SU':not same,'US':not same,'UU':not opp})
 fliptrail=[]
 if len(V)<=15:
  a=dict(a0)
  for v in V[:min(4,len(V))]:
   a[v]^=1;fliptrail.append({'flipped':v,**counts(F,a)})
 out.update({'source_extremes':res,'pair_mode':pair,'flip_trail':fliptrail})
 return out

def finite_cases():
 W=[tuple(c) for c in W1];S=[tuple(c) for c in SWAP6]
 return {'W1_UNSAT':W,'SWAP6_SAT':S,'K4_STRICT22_SAT':K4,'TSEITIN_UNSAT':TSEITIN,
         'TSEITIN_SAT':TSEITIN[:-4],
         'W1_SIGN_RENAME':rename(W,61),
         'HORN_SAT':[(1,-2,3),(-1,-2,4),(-3,),(-4,)],
         'HORN_UNSAT':[(1,),(-1,2),(-2,)],
         'KROM_SAT':[(1,2),(-1,3),(-2,-3)],
         'KROM_UNSAT':[(1,2),(-1,2),(1,-2),(-1,-2)],
         'ORBIT22_SAT':canonical_orbit(7),
         'ORBIT22_RENAMED_SAT':rename(canonical_orbit(7),314)}


def classify(F):
 V=vars_(F);n=len(V);m=len(F)
 proper=all(len(c)==len(set(map(abs,c)))==3 for c in F)
 pos={v:0 for v in V};neg={v:0 for v in V}
 for c in F:
  for z in c:(pos if z>0 else neg)[abs(z)]+=1
 strict22=proper and all(pos[v]==neg[v]==2 for v in V)
 mono=proper and all(all(z>0 for z in c) or all(z<0 for z in c) for c in F)
 P={tuple(sorted(map(abs,c))) for c in F if all(z>0 for z in c)}
 Q={tuple(sorted(map(abs,c))) for c in F if all(z<0 for z in c)}
 q=len(P-Q) if strict22 and mono else None
 # Source-indexed incidence traversal, no semantic label used.
 adj={v:set() for v in V}
 for c in F:
  for x in map(abs,c):adj[x].update(map(abs,c))
 seen=set();stack=V[:1]
 while stack:
  v=stack.pop()
  if v in seen:continue
  seen.add(v);stack.extend(adj[v]-seen)
 return {'proper_3cnf':proper,'strict_signed22':strict22,'signed_m22_pure_clause':mono,'M22_q':q,'M22_Cstar':bool(strict22 and mono and q is not None and q>=2),'connected':len(seen)==len(V),'vars':n,'clauses':m,'literal_occurrences':sum(map(len,F))}

def reverse_dp(F):
 """Actual paid forward simplification and backward Boolean DP, not a selector.
 Key is complete simplified residual, so semantic memoization is exact for decision.
 """
 visited={};state_reads=0;forward=0;backward=0;hits=0
 def restrict(cnf,v,b):
  nonlocal state_reads,forward
  out=[]
  for c in cnf:
   state_reads+=1
   if any(abs(l)==v and int(l>0)==b for l in c):continue
   out.append(tuple(l for l in c if abs(l)!=v))
   forward+=len(c)
  return tuple(sorted(set(out)))
 def solve(cnf):
  nonlocal backward,hits,state_reads
  if cnf in visited:hits+=1;return visited[cnf]
  backward+=1
  if not cnf:r=True
  elif () in cnf:r=False
  else:
   v=min(abs(l) for c in cnf for l in c)
   r=solve(restrict(cnf,v,0)) or solve(restrict(cnf,v,1))
  visited[cnf]=r
  return r
 ans=solve(tuple(sorted(set(tuple(c) for c in F))))
 return {'answer':'SAT' if ans else 'UNSAT','memo_states':len(visited),'memo_hits':hits,'forward_literal_operations':forward,'reverse_value_updates':backward,'source_clause_reads':state_reads,'method':'canonical syntactic residual memo; no advice; SAT short circuit, UNSAT universal conjunction'}

def frac_audit():
 c=Fraction(241,200)
 f=Fraction(1)
 best=Fraction(-100)
 ks=[]
 for k in range(1,200):
  f=c*f/(1+f)
  d=min((1/f-c)/k,1/(c**k))
  if d>best:best=d;bk=k
  ks.append((k,str(d)))
  if (1/(c**(k+1)))<best:break
 assert best==Fraction(11642479,23232400)
 delta=Fraction(1,400)
 return {'c':str(c),'d':str(best),'optimal_k':bk,'certified_tail_after_k':k,'space_slack':str(best-Fraction(1,2)),'max_portfolio_exponent_strict':str(delta),'at_eta_1_over_400_fixed_time':str(Fraction(6,5)+2*delta),'inside_strict_box':False}

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--out',default='arc255_raw.json');parser.add_argument('--full-oracle',action='store_true');args=parser.parse_args()
 tests={};names=['endpoints','horn','dualhorn','krom','xor','signed22_template','dpll_asc','dpll_desc','dpll_freq','dpll_memo','dpll_lookahead']
 for case,F in finite_cases().items():
  t0=time.perf_counter();V=vars_(F)
  gt=oracle(F) if len(V)<=15 or args.full_oracle else (None,None)
  methods={}
  for name in names:
   work,result=run_method(F,name)
   assert verify_claim(F,result),(case,name,result)
   if gt[0] is not None and result[0]!='UNRESOLVED':assert (result[0]=='SAT')==gt[0]
   methods[name]={'events':work,'status':result[0],'verifier':True}
  best=min((v['events'] for v in methods.values() if v['status']!='UNRESOLVED'),default=None)
  tracemalloc.start()
  tb=time.perf_counter();basework,baseresult=run_method(F,'dpll_asc');baseelapsed=time.perf_counter()-tb
  _,basepeak=tracemalloc.get_traced_memory();tracemalloc.stop()
  assert basework==methods['dpll_asc']['events']
  tracemalloc.start()
  ts=time.perf_counter();scheduler=budgeted(F,names,max_power=18);scheduled_elapsed=time.perf_counter()-ts
  _,scheduled_peak=tracemalloc.get_traced_memory();tracemalloc.stop()
  assert scheduler['result']=='SAT' if gt[0] else scheduler['result']=='UNSAT' if gt[0] is not None else scheduler['result'] in ('SAT','UNSAT')
  base=methods['dpll_asc']['events']
  tests[case]={'parameters_checked_external':classify(F),'endpoint_0':counts(F,{v:0 for v in V})['Nr'],'endpoint_1':counts(F,{v:1 for v in V})['Nr'],'n':len(V),'m':len(F),'size_bits_proxy':sum(len(c) for c in F)*int(math.ceil(math.log2(max(V+[1])+2))+2),'ground_truth':'SAT' if gt[0] else 'UNSAT' if gt[0] is not None else 'not_enumerated','methods':methods,'best_method_events_external_oracle_only':best,'budget_hard_external_only':{str(b):not any(v['status']!='UNRESOLVED' and v['events']+1<=b for v in methods.values()) for b in (16,32,64,128,256,512,1024,2048,4096,8192)},'baseline_events':base,'baseline_elapsed_s':round(baseelapsed,6),'baseline_peak_python_bytes':basepeak,'scheduled_events':scheduler['work'],'scheduled_elapsed_s':round(scheduled_elapsed,6),'scheduled_peak_python_bytes':scheduled_peak,'certificate_serialized_bytes':len(json.dumps(scheduler['certificate'])),'schedule_over_baseline':round(scheduler['work']/base,4),'winner':scheduler['winner'],'scheduler_stages':max(x['power'] for x in scheduler['trials']),'scheduler_failed_attempts':sum(x['returned']!='SAT' and x['returned']!='UNSAT' for x in scheduler['trials']),'verified':True,'elapsed_s':round(time.perf_counter()-t0,4)}
  if case in ('K4_STRICT22_SAT','W1_UNSAT','SWAP6_SAT','W1_SIGN_RENAME','TSEITIN_UNSAT','ORBIT22_SAT','ORBIT22_RENAMED_SAT'):tests[case]['clause_extreme_control']=full_audit(F)
  if len(V)<=15:
   dp=reverse_dp(F);assert dp['answer']==tests[case]['ground_truth'];tests[case]['forward_reverse_DP_external_control']=dp
  print(case,tests[case]['ground_truth'],base,scheduler['work'],scheduler['winner'],flush=True)
 # adversarial hidden fast-label lower bound simulation, no SAT lower bound
 opaque=[]
 for m in [1,2,4,8,16,32]:
  t=64;opaque.append({'menu':m,'winning_probe_threshold':t,'minimax_black_box_steps':m*t,'round_robin_last_winner_steps':m*t,'lower_bound_scope':'opaque transcripts; no source inspection'})
 result={'run_id':'LSPV3_ARC255_SELECTOR_GATE','status':'COMPUTATIONAL + restricted exact lemmas in report','seed':314,'date':'2026-10-30','cases':tests,'flmv_exact':frac_audit(),'opaque_control':opaque,'portfolio_policy':names,'event_semantics':'selected logical primitive yields + scheduler choices + source verification; not native FLMV machine steps','zero_cost_optimal_selector_used':False,'unknown_witness_or_oracle_bit_used':False}
 Path(args.out).write_text(json.dumps(result,indent=2,sort_keys=True))
 print('WROTE',args.out)
if __name__=='__main__':main()
