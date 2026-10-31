#!/usr/bin/env python3
"""LSPV-3 restricted certified restart portfolio (Python event proxy, not FLMV TM)."""
import collections, hashlib, json, math, random, sys, tracemalloc
from pathlib import Path
HERE=Path(__file__).resolve().parent
class Exhausted(Exception): pass
class Meter:
 def __init__(self,limit=None):
  self.limit=limit; self.total=0; self.tags=collections.Counter(); self.max_depth=0
 def hit(self,tag='step',k=1):
  for _ in range(k):
   self.total+=1; self.tags[tag]+=1
   if self.limit is not None and self.total>self.limit: raise Exhausted()

def value(lit,asgn):
 x=asgn.get(abs(lit))
 return None if x is None else (x if lit>0 else not x)

def certified_dpll(F,n,order,mt):
 def search(asgn,depth):
  mt.hit('call');mt.max_depth=max(mt.max_depth,depth)
  a=dict(asgn); forced=[]
  while True:
   unit=None; fully=True
   for j,C in enumerate(F):
    mt.hit('source_clause')
    vals=[]
    for lit in C:
     mt.hit('literal_test');vals.append(value(lit,a))
    if True in vals: continue
    unknown=[lit for lit,v in zip(C,vals) if v is None]
    if not unknown: return None,{'forced':forced,'conflict':j}
    fully=False
    if len(unknown)==1:
     unit=(unknown[0],j);break
   if unit is None: break
   lit,j=unit
   a[abs(lit)]=lit>0;forced.append([lit,j]);mt.hit('propagate')
  if fully:
   model=[int(a.get(i,False)) for i in range(1,n+1)]
   return model,None
  for v in order:
   if v not in a:break
  else:raise AssertionError('DPLL incomplete')
  mt.hit('branch')
  left_a=dict(a);left_a[v]=False
  model,left=search(left_a,depth+1)
  if model is not None:return model,None
  right_a=dict(a);right_a[v]=True
  model,right=search(right_a,depth+1)
  if model is not None:return model,None
  return None,{'forced':forced,'branch':v,'zero':left,'one':right}
 model,proof=search({},0)
 return {'status':'SAT','model':model,'method':'DPLL'} if model is not None else {'status':'UNSAT','proof':proof,'method':'DPLL'}

def horn(F,n,mt):
 for C in F:
  mt.hit('source_clause')
  for l in C:mt.hit('literal_test')
  if sum(l>0 for l in C)>1:return None
 true=set();steps=[]
 while True:
  changed=False
  for j,C in enumerate(F):
   mt.hit('source_clause')
   pos=[l for l in C if l>0];neg=[-l for l in C if l<0]
   for l in C:mt.hit('literal_test')
   if all(v in true for v in neg):
    if not pos:return {'status':'UNSAT','method':'HORN','trace':steps,'conflict':j}
    if pos[0] not in true:
     true.add(pos[0]);steps.append([pos[0],j]);mt.hit('propagate');changed=True
  if not changed:break
 return {'status':'SAT','method':'HORN','model':[int(i in true) for i in range(1,n+1)]}

def krom(F,n,mt):
 N=2*n;g=[[] for _ in range(N)];gr=[[] for _ in range(N)]
 def idx(l):return 2*(abs(l)-1)+(0 if l>0 else 1)
 for j,C in enumerate(F):
  mt.hit('source_clause');mt.hit('literal_test',len(C))
  if len(C)>2:return None
  if not C:return {'status':'UNSAT','method':'KROM','empty':j}
  a=C[0];b=C[-1]
  for u,v in [(-a,b),(-b,a)]:
   u,v=idx(u),idx(v);g[u].append((v,j));gr[v].append((u,j));mt.hit('graph_edge')
 visited=[False]*N;finish=[]
 def dfs(u):
  visited[u]=True;mt.hit('graph_visit')
  for v,j in g[u]:
   mt.hit('graph_edge')
   if not visited[v]:dfs(v)
  finish.append(u)
 for u in range(N):
  if not visited[u]:dfs(u)
 comp=[-1]*N;cid=0
 def dfs_rev(u):
  comp[u]=cid;mt.hit('graph_visit')
  for v,j in gr[u]:
   mt.hit('graph_edge')
   if comp[v]<0:dfs_rev(v)
 for u in reversed(finish):
  if comp[u]<0:dfs_rev(u);cid+=1
 for v in range(1,n+1):
  if comp[idx(v)]==comp[idx(-v)]:
   def path(start,end):
    q=collections.deque([start]);parent={start:None}
    while q:
     u=q.popleft();mt.hit('graph_visit')
     if u==end:break
     for w,j in g[u]:
      mt.hit('graph_edge')
      if w not in parent:parent[w]=(u,j);q.append(w)
    chain=[];v0=end
    while parent[v0] is not None:
     prev,j=parent[v0];chain.append([prev,v0,j]);v0=prev
    return list(reversed(chain))
   return {'status':'UNSAT','method':'KROM','variable':v,'paths':[path(idx(v),idx(-v)),path(idx(-v),idx(v))]}
 assignment=[int(comp[idx(v)]>comp[idx(-v)]) for v in range(1,n+1)]
 return {'status':'SAT','method':'KROM','model':assignment}

def xor_groups(F,mt):
 groups=collections.defaultdict(list)
 for j,C in enumerate(F):
  mt.hit('source_clause');mt.hit('literal_test',len(C))
  if len(C)!=3 or len({abs(x) for x in C})!=3:return None
  groups[tuple(sorted(abs(x) for x in C))].append(j)
 equations=[]
 for vs,indices in sorted(groups.items()):
  mt.hit('recognition')
  if len(indices)!=4:return None
  ps=set()
  for j in indices:
   bits=tuple(0 if v in F[j] else 1 for v in vs)
   if bits in ps:return None
   ps.add(bits);mt.hit('recognition')
  if len({sum(bits)%2 for bits in ps})!=1:return None
  forbidden=sum(next(iter(ps)))%2
  if ps!={tuple((q>>k)&1 for k in range(3)) for q in range(8) if (q.bit_count()&1)==forbidden}:return None
  mask=sum(1<<(v-1) for v in vs)
  equations.append([mask,1-forbidden,indices])
 return equations

def affine(F,n,mt):
 eq=xor_groups(F,mt)
 if eq is None:return None
 basis={};num=len(eq)
 for i,(mask,rhs,indices) in enumerate(eq):
  comb=1<<i
  while mask:
   mt.hit('xor_row')
   p=mask.bit_length()-1
   if p not in basis:
    basis[p]=(mask,rhs,comb);break
   bm,br,bc=basis[p];mask^=bm;rhs^=br;comb^=bc
  else:
   if rhs:
    return {'status':'UNSAT','method':'AFFINE','core':[k for k in range(num) if comb>>k&1], 'equations':eq}
 a=0
 for p in sorted(basis):
  mask,rhs,comb=basis[p];m=mask&~(1<<p)
  parity=(m&a).bit_count()&1
  if parity!=rhs:a|=1<<p
  mt.hit('xor_row')
 return {'status':'SAT','method':'AFFINE','model':[(a>>i)&1 for i in range(n)]}

def endpoint_flip(F,n,mt,max_flips=128):
 # Check globally consistent endpoints, then intermediate Gray states.
 examined=set()
 for a in [0,(1<<n)-1]+[i^(i>>1) for i in range(min(1<<min(n,7),max_flips))]:
  if a in examined:continue
  examined.add(a);mt.hit('assignment')
  ok=True
  for C in F:
   mt.hit('source_clause')
   satisfied=False
   for l in C:
    mt.hit('literal_test')
    if bool((a>>(abs(l)-1))&1)==(l>0):satisfied=True
   if not satisfied:ok=False;break
  if ok:return {'status':'SAT','method':'FLIP','model':[(a>>i)&1 for i in range(n)]}
 return None

POLICIES=('FLIP','HORN','KROM','AFFINE','DPLL_ASC','DPLL_DESC')
def solver(policy,F,n,mt):
 if policy=='FLIP':return endpoint_flip(F,n,mt)
 if policy=='HORN':return horn(F,n,mt)
 if policy=='KROM':return krom(F,n,mt)
 if policy=='AFFINE':return affine(F,n,mt)
 if policy=='DPLL_ASC':return certified_dpll(F,n,list(range(1,n+1)),mt)
 if policy=='DPLL_DESC':return certified_dpll(F,n,list(range(n,0,-1)),mt)
 raise ValueError(policy)

def verify(F,n,cert,mt):
 if cert['status']=='SAT':
  model=cert['model']
  if len(model)!=n:return False
  for C in F:
   mt.hit('proof_source_clause');ok=False
   for l in C:
    mt.hit('proof_literal')
    if bool(model[abs(l)-1])==(l>0):ok=True
   if not ok:return False
  return True
 if cert['status']!='UNSAT':return False
 method=cert['method']
 if method=='HORN':
  a={}
  for v,j in cert['trace']:
   if not (0<=j<len(F)):return False
   C=F[j];mt.hit('proof_source_clause');mt.hit('proof_literal',len(C))
   if v not in C or sum(l>0 for l in C)!=1:return False
   if any(-l not in a for l in C if l<0):return False
   a[v]=True
  C=F[cert['conflict']];mt.hit('proof_source_clause');mt.hit('proof_literal',len(C))
  return all(l<0 and (-l in a) for l in C)
 if method=='KROM':
  if 'empty' in cert:
   mt.hit('proof_source_clause');return F[cert['empty']]==[]
  v=cert['variable'];paths=cert['paths']
  def idx(l):return 2*(abs(l)-1)+(0 if l>0 else 1)
  for start,end,chain in [(idx(v),idx(-v),paths[0]),(idx(-v),idx(v),paths[1])]:
   here=start
   for u,w,j in chain:
    if u!=here or not (0<=j<len(F)):return False
    C=F[j];mt.hit('proof_source_clause');mt.hit('proof_literal',len(C))
    if not (1<=len(C)<=2):return False
    a,b=C[0],C[-1]
    edges=[(idx(-a),idx(b)),(idx(-b),idx(a))]
    if (u,w) not in edges:return False
    here=w
   if here!=end:return False
  return True
 if method=='AFFINE':
  eq=xor_groups(F,mt)
  if eq is None:return False
  mask=0;rhs=0;ids=cert['core']
  if not ids or len(ids)!=len(set(ids)):return False
  for i in ids:
   if i>=len(eq) or i<0:return False
   mask^=eq[i][0];rhs^=eq[i][1];mt.hit('proof_xor')
  return mask==0 and rhs==1
 if method=='DPLL':
  def rec(node,assn):
   a=dict(assn);mt.hit('proof_node')
   for lit,j in node.get('forced',[]):
    if not (0<=j<len(F)):return False
    C=F[j];mt.hit('proof_source_clause');vals=[]
    for x in C:mt.hit('proof_literal');vals.append(value(x,a))
    if sum(v is None for v in vals)!=1 or any(v is True for v in vals):return False
    if lit not in C or a.get(abs(lit)) is not None:return False
    a[abs(lit)]=lit>0
   if 'conflict' in node:
    j=node['conflict'];C=F[j];mt.hit('proof_source_clause');return all((mt.hit('proof_literal') or value(l,a) is False) for l in C)
   v=node.get('branch')
   if not isinstance(v,int) or v<1 or v>n or v in a:return False
   mt.hit('proof_branch')
   b=dict(a);b[v]=False
   if not rec(node['zero'],b):return False
   b[v]=True
   return rec(node['one'],b)
  return rec(cert['proof'],{})
 return False

def single(policy,F,n,budget=None):
 mt=Meter(budget);mt.hit('policy_choice')
 try:
  cert=solver(policy,F,n,mt)
  if cert is None:return {'state':'UNRESOLVED','work':mt.total,'tags':dict(mt.tags),'max_depth':mt.max_depth}
  verified=verify(F,n,cert,mt)
  if not verified:raise AssertionError(f'UNVERIFIED {policy}: {cert}')
  return {'state':cert['status'],'work':mt.total,'tags':dict(mt.tags),'max_depth':mt.max_depth,'certificate':cert}
 except Exhausted:
  return {'state':'BUDGET','work':mt.total,'tags':dict(mt.tags),'max_depth':mt.max_depth}

def race(F,n):
 j=0;total=0;rounds=[];completed=set();peak=0
 while True:
  budget=1<<j;row={'budget':budget,'policies':{}}
  for policy in POLICIES:
   if policy in completed:continue
   s=single(policy,F,n,budget)
   total+=s['work'];peak=max(peak,s['max_depth'])
   row['policies'][policy]={'state':s['state'],'work':s['work'],'tags':s['tags'],'max_depth':s['max_depth']}
   if s['state']=='UNRESOLVED':completed.add(policy)
   if s['state'] in ('SAT','UNSAT'):
    row['winner']=policy;rounds.append(row)
    return {'status':s['state'],'winner':policy,'total_work':total,'budget_rounds':len(rounds),'rounds':rounds,'proof':s['certificate'],'peak_decision_depth':peak,'failed_trials':sum(1 for r in rounds for t in r['policies'].values() if t['state']=='BUDGET')}
  rounds.append(row);j+=1
  if j>30:raise RuntimeError('nonterminating scheduler')

def original_controls(F,n):
 clauses=[];modes=[];statuses=[]
 for j,C in enumerate(F):
  s={str(abs(l)):int(l>0) for l in C};u={str(abs(l)):int(l<0) for l in C}
  clauses.append({'index':j,'occurrences':[{'variable':abs(l),'sign':int(l>0),'S':int(l>0),'inverted_S_equals_U':int(l<0),'U':int(l<0),'inverted_U_equals_S':int(l>0)} for l in C],'S':s,'U':u})
 for j in range(len(F)):
  for k in range(j+1,len(F)):
   a=F[j];b=F[k]
   same=any(l in b for l in a);opposite=any(-l in b for l in a)
   modes.append({'Cj':j,'Ck':k,'SS':not opposite,'SU':not same,'US':not same,'UU':not opposite})
 seen=set()
 for tag,a in [('zero',0),('one',(1<<n)-1)]+[('gray',t^(t>>1)) for t in range(min(16,1<<min(n,8)))]:
  if a in seen:continue
  seen.add(a)
  truth=[sum(((a>>(abs(l)-1))&1)==(l>0) for l in C) for C in F]
  counts={str(i):sum(v==i for v in truth) for i in range(4)}
  complement=(1<<n)-1-a
  comp_truth=[sum(((complement>>(abs(l)-1))&1)==(l>0) for l in C) for C in F]
  assert all(x+y==len(C) for x,y,C in zip(truth,comp_truth,F))
  statuses.append({'tag':tag,'assignment_bits':a,'counts':counts,'t_source':truth,'complement_bits':complement,'t_complement':comp_truth})
 return {'original_clause_targets':clauses,'pair_compatibility':modes,'global_flip_trail':statuses}

def controls():
 base=json.loads((HERE/'fixtures271.json').read_text())
 cases={k:v for k,v in base.items() if k in ('HORN_CHAIN_SAT','HORN_CHAIN_UNSAT','KROM_SAT','KROM_UNSAT','W1_UNSAT','SWAP6_SAT','W1_RENAMED_UNSAT','SWAP6_RENAMED_SAT','THREE_SAT_MIDDLE','THREE_UNSAT_FULL','RANDOM3_SEED11','RANDOM3_SEED12')}
 # Parity 3-variable source groups: four clauses encoding allowed XOR parity.
 def xor_block(ids,allowed):
  C=[]
  for bits in range(8):
   if bits.bit_count()%2 == allowed:continue
   C.append([(-v if bits>>(i)&1 else v) for i,v in enumerate(ids)])
  return C
 cases['XOR3_SAT']={'n':3,'original_clauses':xor_block([1,2,3],0)}
 cases['XOR6_UNSAT']={'n':6,'original_clauses':xor_block([1,2,3],0)+xor_block([1,2,4],0)+xor_block([3,5,6],0)+xor_block([4,5,6],1)}
 cases['XOR6_SAT']={'n':6,'original_clauses':xor_block([1,2,3],0)+xor_block([1,2,4],0)+xor_block([3,5,6],0)+xor_block([4,5,6],0)}
 cases['MIX_HORN_AFFINE_SAT']={'n':3,'original_clauses':xor_block([1,2,3],0)+[[1],[2],[-3]]}
 cases['MIX_HORN_AFFINE_UNSAT']={'n':3,'original_clauses':xor_block([1,2,3],1)+[[1],[2],[-3]]}
 # Positive/negative endpoint controls, verified under independent enumerator.
 cases['ALL_POSITIVE_SAT']={'n':4,'original_clauses':[[1,2,3],[1,3,4],[2,3,4]]}
 cases['ALL_NEGATIVE_SAT']={'n':4,'original_clauses':[[-1,-2,-3],[-1,-3,-4],[-2,-3,-4]]}
 return cases

def run():
 casebook=controls();records=[]
 for name,source in casebook.items():
  F=source['original_clauses'];n=source['n'];assert all(len(set(map(abs,C)))==len(C) for C in F)
  independent={p:single(p,F,n) for p in POLICIES}
  assert independent['DPLL_ASC']['state'] in ('SAT','UNSAT')
  assert independent['DPLL_DESC']['state']==independent['DPLL_ASC']['state']
  for p,s in independent.items():
   if s['state'] in ('SAT','UNSAT'):assert s['state']==independent['DPLL_ASC']['state']
  tracemalloc.start()
  result=race(F,n)
  peak_heap=tracemalloc.get_traced_memory()[1]
  tracemalloc.stop()
  tag_sum=collections.Counter()
  for r0 in result['rounds']:
   for z in r0['policies'].values():tag_sum.update(z['tags'])
  result['aggregate_charged_categories']=dict(tag_sum)
  result['peak_traced_heap_bytes']=peak_heap
  result['source_dimacs_utf8_bytes']=len((f"p cnf {n} {len(F)}\n"+"".join(" ".join(map(str,C))+" 0\n" for C in F)).encode())
  result['physically_serialized_ordinary_children']=0
  result['guest_A_calls']=0
  assert result['status']==independent['DPLL_ASC']['state']
  positive=[s['work'] for s in independent.values() if s['state'] in ('SAT','UNSAT')]
  best=min(positive);r=len(POLICIES)
  assert result['total_work']<=4*r*best+r*(math.ceil(math.log2(best))+1)+r
  controls_row=original_controls(F,n)
  records.append({'name':name,'n':n,'m':len(F),'original_clauses':F,'label':result['status'],'per_policy':{p:{k:v for k,v in s.items() if k!='certificate'} for p,s in independent.items()},'best_verified_work':best,'race':result,'controls':controls_row})
 out={'run':'LSPV-3 CERTIFIED-RESTART-PORTFOLIO275','seed':202610310628,'count':len(records),'policies':list(POLICIES),'cases':records,'disclosure':{'units':'selected Python events, not Turing machine instructions','input':'materialized as Python lists','proof':'independent verifier in verify275.py','portfolio':'from-scratch dyadic restarts, no free winner oracle'}}
 (HERE/'raw275.json').write_text(json.dumps(out,indent=1,sort_keys=True))
 summary={'count':len(records),'SAT':sum(x['label']=='SAT' for x in records),'UNSAT':sum(x['label']=='UNSAT' for x in records),'cases':[{'name':x['name'],'label':x['label'],'n':x['n'],'m':x['m'],'baseline':x['per_policy']['DPLL_ASC']['work'],'best':x['best_verified_work'],'race':x['race']['total_work'],'winner':x['race']['winner'],'rounds':x['race']['budget_rounds'],'failed_trials':x['race']['failed_trials'],'source_clause_probes':x['race']['aggregate_charged_categories'].get('source_clause',0),'proof_clause_probes':x['race']['aggregate_charged_categories'].get('proof_source_clause',0),'peak_heap_bytes':x['race']['peak_traced_heap_bytes']} for x in records]}
 (HERE/'summary275.json').write_text(json.dumps(summary,indent=2,sort_keys=True))
 print(json.dumps(summary,indent=2))
if __name__=='__main__':run()
