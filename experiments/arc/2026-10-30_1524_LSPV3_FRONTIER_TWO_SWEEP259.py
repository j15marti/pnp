#!/usr/bin/env python3
"""Reproducible clause-frontier forward/reverse SAT DP with original-source certificates.
RUN ID LSPV3-FRONTIER-MARGINAL259. No SAT oracle or no-cost decomposition.
"""
import itertools,json,random,time,tracemalloc,hashlib,sys
from pathlib import Path
from collections import defaultdict

BASE=Path(__file__).resolve().parent
SEED=202610301524
W=[(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),(5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),(-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),(2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)]
SWAP=list(W);SWAP[9]=(-5,6,-15);SWAP[13]=(-3,-6,-15)

def variables(F):return sorted({abs(x) for c in F for x in c})
def eval_clause(c,a):return any(a.get(abs(x))==int(x>0) for x in c)
def eval_F(F,a):return all(eval_clause(c,a) for c in F)
def enum_models(F):
 V=variables(F);return [dict(zip(V,b)) for b in itertools.product((0,1),repeat=len(V)) if eval_F(F,dict(zip(V,b)))]

def prep(F,order):
 first={};last={};V=variables(F)
 for t,i in enumerate(order):
  for x in F[i]:v=abs(x);first.setdefault(v,t);last[v]=t
 B=[tuple()]
 for t in range(len(F)):
  B.append(tuple(v for v in V if first[v]<=t<last[v]))
 U=[tuple(sorted(set(B[t])|{abs(x) for x in F[order[t]]})) for t in range(len(F))]
 assert all(set(B[t+1]).issubset(set(U[t])) for t in range(len(F)))
 return B,U,max(map(len,B),default=0)

def greedy_order(F):
 # Completely source-visible greedy, not an optimal-decomposition oracle.
 remaining=set(range(len(F)));processed=set();counts=defaultdict(int)
 for c in F:
  for v in set(map(abs,c)):counts[v]+=1
 order=[];cost=0
 while remaining:
  ranked=[]
  for j in sorted(remaining):
   support=set(map(abs,F[j]));cost+=len(support)+len(counts)
   active_new={v for v in (processed|support) if counts[v]-(v in support)>0}
   ranked.append((len(active_new),j))
  _,j=min(ranked);remaining.remove(j);order.append(j)
  for v in set(map(abs,F[j])):counts[v]-=1
  processed.update(map(abs,F[j]));processed={v for v in processed if counts[v]>0}
 return order,cost

def encode(vals,keys):
 return sum(vals[v]<<i for i,v in enumerate(keys))
def decode(mask,keys):
 return {v:(mask>>i)&1 for i,v in enumerate(keys)}

def messages(F,order,forward=True,backward=True,cap=12):
 B,U,w=prep(F,order)
 if max(map(len,U),default=0)>cap:return {'status':'too_wide','width':w,'max_union':max(map(len,U),default=0),'trials':0,'live':0}
 m=len(order);counts={'row_trials':0,'clause_literal_checks':0,'lookups':0,'table_writes':0,'state_copy_ops':0,'transition_bits':0}
 left=[set() for _ in range(m+1)];right=[set() for _ in range(m+1)]
 parents=[{} for _ in range(m+1)]
 left[0].add(0)
 for t,j in enumerate(order):
  keys=U[t];outkeys=B[t+1];inkeys=B[t]
  for bits in range(1<<len(keys)):
   counts['row_trials']+=1; a=decode(bits,keys); counts['state_copy_ops']+=len(keys)
   mk=encode(a,inkeys);counts['lookups']+=1
   if mk not in left[t]:continue
   counts['clause_literal_checks']+=len(F[j]);
   if not eval_clause(F[j],a):continue
   out=encode(a,outkeys);counts['table_writes']+=1
   left[t+1].add(out);parents[t+1].setdefault(out,bits)
 right[m].add(0)
 for t in range(m-1,-1,-1):
  j=order[t];keys=U[t];outkeys=B[t+1];inkeys=B[t]
  for bits in range(1<<len(keys)):
   counts['row_trials']+=1;a=decode(bits,keys);counts['state_copy_ops']+=len(keys)
   counts['clause_literal_checks']+=len(F[j]);
   if not eval_clause(F[j],a):continue
   mk=encode(a,outkeys);counts['lookups']+=1
   if mk not in right[t+1]:continue
   key=encode(a,inkeys);right[t].add(key);counts['table_writes']+=1
 sat=0 in left[m];assert sat==(0 in right[0])
 support={v:set() for v in variables(F)}; patterns={j:set() for j in order};pattern_counters={'join_trials':0,'join_lookups':0,'join_writes':0}
 for t,j in enumerate(order):
  keys=U[t];inkeys=B[t];outkeys=B[t+1];vkeys=sorted(set(map(abs,F[j])))
  for bits in range(1<<len(keys)):
   pattern_counters['join_trials']+=1;a=decode(bits,keys)
   pattern_counters['join_lookups']+=1
   if encode(a,inkeys) not in left[t]:continue
   if not eval_clause(F[j],a):continue
   pattern_counters['join_lookups']+=1
   if encode(a,outkeys) not in right[t+1]:continue
   pattern=tuple(a[v] for v in vkeys);patterns[j].add(pattern)
   for v in vkeys:support[v].add(a[v]);pattern_counters['join_writes']+=1
 witness=None
 if sat:
  state=0;witness={}
  for t in range(m-1,-1,-1):
   bits=parents[t+1][state];a=decode(bits,U[t]);j=order[t]
   for x in F[j]:
    v=abs(x)
    if v in witness:assert witness[v]==a[v]
    witness[v]=a[v]
   state=encode(a,B[t])
  assert eval_F(F,witness)
 live_entries=sum(map(len,left))+sum(map(len,right))+sum(map(len,parents))
 return {'status':'done','SAT':sat,'width':w,'max_union':max(map(len,U),default=0),'trials':counts['row_trials'],'costs':counts,'join_costs':pattern_counters,'forward_states':list(map(len,left)),'reverse_states':list(map(len,right)),'live_entries':live_entries,'left_tables':[sorted(t) for t in left],'right_tables':[sorted(t) for t in right],'support':{str(v):sorted(s) for v,s in support.items()},'patterns':{str(j+1):sorted(map(list,patterns[j])) for j in order},'witness':witness,'order':[j+1 for j in order]}

def dpll(F):
 # Source-indexed UP/DPLL refutation tree and selected-event ledger.
 V=variables(F);stats={'nodes':0,'clause_scans':0,'literal_checks':0,'propagations':0,'branches':0,'proof_nodes':0,'checks':0}
 def go(assum):
  stats['nodes']+=1
  status=None
  for i,c in enumerate(F):
   stats['clause_scans']+=1;free=[];valid=False
   for l in c:
    stats['literal_checks']+=1
    if abs(l) in assum:
     if assum[abs(l)]==int(l>0):valid=True;break
    else:free.append(l)
   if not valid and not free:
    stats['proof_nodes']+=1
    return False,{'type':'conflict','source':i+1}
   if not valid and len(free)==1:
    l=free[0];n=dict(assum);n[abs(l)]=int(l>0)
    stats['propagations']+=1;ans,tr=go(n)
    if ans:return ans,tr
    stats['proof_nodes']+=1
    return False,{'type':'unit','source':i+1,'literal':l,'child':tr}
  if all(eval_clause(c,assum) for c in F):
   found={v:assum.get(v,0) for v in V};assert eval_F(F,found)
   return found,None
  v=next(v for v in V if v not in assum);stats['branches']+=1
  a,proof0=go({**assum,v:0})
  if a:return a,None
  b,proof1=go({**assum,v:1})
  if b:return b,None
  stats['proof_nodes']+=1
  return False,{'type':'split','var':v,'zero':proof0,'one':proof1}
 ans,proof=go({})
 def verify(p,a):
  stats['checks']+=1;t=p['type']
  if t=='conflict':
   assert not eval_clause(F[p['source']-1],a)
  elif t=='unit':
   c=F[p['source']-1];l=p['literal'];uns=[]
   assert not any(abs(z) in a and a[abs(z)]==int(z>0) for z in c)
   assert (uns:=[z for z in c if abs(z) not in a])==[l]
   verify(p['child'],{**a,abs(l):int(l>0)})
  else:
   v=p['var'];assert v not in a
   verify(p['zero'],{**a,v:0});verify(p['one'],{**a,v:1})
 if ans is False:verify(proof,{})
 else:stats['checks']+=sum(map(len,F));assert eval_F(F,ans)
 stats['total_events']=sum(stats.values())
 return {'SAT':ans is not False,'witness':ans if ans is not False else None,'stats':stats,'proof':proof}

def endpoint_extremes(F):
 V=variables(F);n=len(V);a0={v:0 for v in V};a1={v:1 for v in V}
 def counts(a):
  t=[sum(a[abs(l)]==int(l>0) for l in c) for c in F]
  return {'N':[t.count(q) for q in range(4)],'t':t,'satisfied':[j+1 for j,x in enumerate(t) if x>0],'falsified':[j+1 for j,x in enumerate(t) if x==0]}
 s=[]
 for j,c in enumerate(F):
  ss={abs(l):int(l>0) for l in c};uu={v:1-b for v,b in ss.items()}
  s.append({'clause':j+1,'occurrences':[{'literal':l,'S_value':int(l>0),'inverse_U_value':int(l<0),'U_value':int(l<0),'inverse_S_value':int(l>0)} for l in c],'S_target':ss,'S_inverted_U':uu,'U_target':uu,'U_inverted_S':ss})
 modes={}
 for j in range(len(F)):
  for k in range(j+1,len(F)):
   modes[f'{j+1}-{k+1}']={}
   for p in 'SU':
    for q in 'SU':
     target1={abs(l):(int(l>0) if p=='S' else int(l<0)) for l in F[j]}
     target2={abs(l):(int(l>0) if q=='S' else int(l<0)) for l in F[k]}
     compatible=all(v not in target2 or b==target2[v] for v,b in target1.items())
     modes[f'{j+1}-{k+1}'][p+q]=compatible
     # direct logically independent enumeration of assignments for at most 6 vars
     vs=sorted(set(target1)|set(target2));brute=any(all(dict(zip(vs,a))[v]==b for v,b in list(target1.items())+list(target2.items())) for a in itertools.product((0,1),repeat=len(vs)))
     assert brute==compatible
 trail=[]
 base=a0.copy();flips=[[],[V[0]]] if V else [[]]
 if len(V)>=2:flips+=[[V[0],V[1]]]
 if len(V)>=3:flips+=[[V[0],V[2]]]
 flips.append(V)
 for ids in flips:
  a={v:(1 if v in ids else 0) for v in V};row=counts(a)
  b={v:1-a[v] for v in V};rev=counts(b)
  assert all(rev['t'][i]==len(F[i])-row['t'][i] for i in range(len(F)))
  trail.append({'flip_variables':ids,'N':row['N'],'complement_N':rev['N'],'false_clause_indices':row['falsified'],'true_clause_indices':row['satisfied']})
 return {'per_clause':s,'pair_modes':modes,'zero':counts(a0),'one':counts(a1),'flip_trail':trail}

def parity3(xs,bit):
 return [tuple((-v if ((mask>>t)&1) else v) for t,v in enumerate(xs)) for mask in range(8) if (3-bin(mask).count('1'))%2!=bit]

def chain(n,unsat=False):
 # XOR x_i xor x_(i+1) xor x_(i+2)=b_i, plus opposed final equation for UNSAT.
 F=[]
 for i in range(1,n-1):F+=parity3((i,i+1,i+2),i%2)
 if unsat:F+=parity3((n-2,n-1,n),1-((n-2)%2))
 return F

def easy_signed22(k=7):
 assert k%2==1 and k>=7
 F=[]
 for i in range(k):
  for s in range(4):
   sg=1 if s<=1 else -1
   F.append((sg*(1+i),sg*(1+k+(i+s)%k),sg*(1+2*k+(i+2*s)%k)))
 assert len(F)==4*k
 witness={v:int(v<=k) for v in range(1,3*k+1)}
 assert eval_F(F,witness)
 return F,witness

def control_sources():
 Fcases={'strict22_W1_UNSAT':W,'strict22_SWAP6_SAT':SWAP,'chain_XOR_8_SAT':chain(8),'chain_XOR_8_UNSAT':chain(8,True),
 'chain_XOR_12_SAT':chain(12),'chain_XOR_12_UNSAT':chain(12,True),
 'Horn_easy_SAT':[(-1,2,3),(-2,3,4),(-3,4,5)],
 'Krom_easy_UNSAT':[(1,2),(-1,2),(1,-2),(-1,-2)],
 'opposite_endpoints_SAT':[(1,2,3),(-1,-2,-3)]}
 # random explicit source controls up to 7 variables
 rng=random.Random(SEED)
 # A dense adversarial control that is easy for an explicit source-known witness,
 # but may have broad clause frontier. No answer labels are given to the controller.
 dense=[];plant={v:(v%2) for v in range(1,15)}
 for j in range(44):
  while True:
   vs=rng.sample(range(1,15),3)
   c=tuple(v*rng.choice((-1,1)) for v in vs)
   if eval_clause(c,plant):break
  dense.append(c)
 Fcases['dense_planted14_SAT']=dense
 Fcases['dense14_UNSAT']=dense+[(1,2,3),(-1,2,3),(1,-2,3),(-1,-2,3),(1,2,-3),(-1,2,-3),(1,-2,-3),(-1,-2,-3)]
 for i in range(16):
  n=rng.randrange(3,8);m=rng.randrange(2,12);F=[]
  for _ in range(m):
   vs=rng.sample(range(1,n+1),3)
   F.append(tuple(v*rng.choice((-1,1)) for v in vs))
  Fcases[f'PRNG_{i:02d}']=F
 return Fcases

def main():
 results={};total_assertions=0
 for name,F in control_sources().items():
  n=len(variables(F));m=len(F)
  original=list(range(m));pw0=prep(F,original)[2]
  if pw0<=4:
   greedy=original;discovery=0;pwg=pw0
  else:greedy,discovery=greedy_order(F);pwg=prep(F,greedy)[2]
  # Select only the measured better order. Full original source scan and all attempted
  # policy acquisition are charged; no free optimal separator or answer oracle.
  chosen=greedy if pwg<pw0 else original
  select_cost=sum(map(len,F))+discovery
  tracemalloc.start();t0=time.perf_counter()
  dp=messages(F,chosen,cap=9)
  tdp=time.perf_counter()-t0;_,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
  t0=time.perf_counter();baseline=dpll(F);base_seconds=time.perf_counter()-t0
  sat=baseline['SAT'];exact=enum_models(F)
  assert sat==bool(exact)
  if dp['status']=='done':
   assert dp['SAT']==sat
   for v,values in dp['support'].items():
    assert values==sorted({model[int(v)] for model in exact})
    total_assertions+=1
   for j,p in dp['patterns'].items():
    cs=F[int(j)-1];vs=sorted(set(map(abs,cs)))
    truth=sorted({tuple(model[v] for v in vs) for model in exact})
    assert sorted(map(tuple,p))==truth
    total_assertions+=1
   total_assertions+=1
  if n<=15:
   ext=endpoint_extremes(F)
   total_assertions+=4* (m*(m-1)//2)+m
  else:ext={}
  results[name]={'n':n,'m':m,'is_SAT':sat,'model_count':len(exact),'source':F,'input_order_width':pw0,'greedy_width':pwg,
                 'selection_events':select_cost,'policy':'greedy' if chosen==greedy and greedy!=original else 'original',
                 'dp':dp,'dp_seconds':tdp,'dp_python_peak':peak,'baseline':{'decision':sat,'stats':baseline['stats'],'seconds':base_seconds},'extreme_audit':ext}
 # explicit adversarial semantic trap: opposite endpoints both false but formula is SAT
 a=results['opposite_endpoints_SAT'];assert a['is_SAT'] and a['extreme_audit']['zero']['N'][0]>0 and a['extreme_audit']['one']['N'][0]>0
 # Source-known witness high-frontier strict22 controls; don't enumerate 2^(3k).
 orbit={}
 for k in (7,9,11):
  F,a=easy_signed22(k);g,c=greedy_order(F);v=variables(F)
  counts={p:[0,0] for p in v}
  for clause in F:
   for lit in clause:counts[abs(lit)][int(lit>0)]+=1
  assert all(pair==[2,2] for pair in counts.values())
  baseline=dpll(F)
  assert baseline['SAT'] and eval_F(F,a)
  orbit[str(k)]={'n':len(v),'m':len(F),'input_width':prep(F,list(range(len(F))))[2],
                 'greedy_width':prep(F,g)[2],'policy_acquisition_events':c,
                 'strict_signed22':True,'source_known_witness':a,
                 'DPLL_events':baseline['stats']['total_events'],'DPLL_nodes':baseline['stats']['nodes']}
 # exactness of chain constraints and no-free width
 print(json.dumps({'seed':SEED,'cases':len(results),'assertion_groups':total_assertions,'orbit':orbit,
                   'summaries':{k:{'n':v['n'],'m':v['m'],'SAT':v['is_SAT'],'models':v['model_count'],'width_input':v['input_order_width'],'width_greedy':v['greedy_width'],'policy':v['policy'],'discovery':v['selection_events'],'DP_status':v['dp']['status'],'DP_rows':v['dp'].get('trials'),'DP_live':v['dp'].get('live_entries'),'DP_join':v['dp'].get('join_costs',{}).get('join_trials'),'DP_sec':round(v['dp_seconds'],4),'DPLL_nodes':v['baseline']['stats']['nodes'],'DPLL_events':v['baseline']['stats']['total_events']} for k,v in results.items()}},indent=2))
 with open(BASE/'raw.json','w') as g:json.dump({'run':'FRONTIER_TWO_SWEEP259','seed':SEED,'assertions':total_assertions,'cases':results,'orbit':orbit},g,sort_keys=True,indent=2)
if __name__=='__main__':main()
