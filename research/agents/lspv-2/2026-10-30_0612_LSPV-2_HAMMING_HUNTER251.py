#!/usr/bin/env python3
"""LSPV-2 HAMMING-HUNTER251: source-indexed extrema and rigorous
Hamming-layer Hunter (1976) SAT-certificate/witness construction.
Python 3.11+, standard library only. Run --help, --out FILE.
EXACT finite experiment; no claim of unrestricted SAT speedup.
"""
import argparse, collections, itertools, json, math, random, time, tracemalloc

CASES={
 'STRICT22_N9_HUNTER':('5 -3 6;4 -9 -8;-2 -9 -3;2 7 1;-4 -6 -8;-5 -4 -7;4 -1 -6;9 3 8;8 1 2;3 6 -7;-5 7 9;-2 -1 5',9),
 'STRICT22_W1_UNSAT':('-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14',15),
 'STRICT22_K4_SAT':('1 2 3;-1 4 5;2 4 6;3 5 6;-1 -2 -3;1 -4 -5;-2 -4 -6;-3 -5 -6',6),
 'AFFINE_XOR3_SAT':('1 2 3;1 -2 -3;-1 2 -3;-1 -2 3',3),
 'AFFINE_XOR3_UNSAT':('1 2 3;1 -2 -3;-1 2 -3;-1 -2 3;1 2 -3;1 -2 3;-1 2 3;-1 -2 -3',3),
 'HORN_SAT':('-1 -2 3;-3 4 5;-4 -5 6',6),
 '2SAT_UNSAT':('1 2;-1 2;1 -2;-1 -2',2),
}

def parse(name):
 s,n=CASES[name];return [tuple(map(int,c.split())) for c in s.split(';')],n
class Work:
 def __init__(self):self.events=collections.Counter()
 def add(self,k,v=1):self.events[k]+=v
 def data(self):return dict(sorted(self.events.items()))

def truth(c,a):return sum(((a>>(abs(z)-1))&1)==(z>0) for z in c)
def status(F,a):
 ts=[truth(c,a) for c in F];return {'mask':a,'t':ts,'N':[ts.count(i) for i in range(4)],'sat':0 not in ts}
def validate(F,n,strict=False):
 assert all(1<=abs(z)<=n for c in F for z in c)
 assert all(len({abs(z) for z in c})==len(c) for c in F)
 if strict:
  assert all(len(c)==3 for c in F) and len(F)*3==n*4
  counts=collections.Counter(z for c in F for z in c)
  assert all(counts[i]==counts[-i]==2 for i in range(1,n+1))
  graph={i:set() for i in range(1,n+1)}
  for c in F:
   for a,b in itertools.combinations((abs(z) for z in c),2):graph[a].add(b);graph[b].add(a)
  seen={1};stack=[1]
  while stack:
   v=stack.pop()
   for u in graph[v]-seen:seen.add(u);stack.append(u)
  assert len(seen)==n

def extrema(F):
 out=[]
 for j,c in enumerate(F,1):
  occ=[]
  for k,z in enumerate(c,1):
   S=int(z>0);U=1-S
   occ.append({'occurrence':f'x_{{{abs(z)},{j}}}','position':k,'literal':z,'sign':'+' if z>0 else '-',
               'S_local':S,'invert_S_is_U':1-S,'U_local':U,'invert_U_is_S':1-U})
  out.append({'clause_id':j,'original_literals':list(c),'S':{str(abs(z)):int(z>0) for z in c},
              'U':{str(abs(z)):int(z<0) for z in c},'occurrences':occ})
 return out

def pair_modes(F):
 result=[];checked=0
 for j,k in itertools.combinations(range(len(F)),2):
  sj={abs(z):int(z>0) for z in F[j]};sk={abs(z):int(z>0) for z in F[k]};shared=set(sj)&set(sk)
  same=sorted(v for v in shared if sj[v]==sk[v]);opp=sorted(v for v in shared if sj[v]!=sk[v])
  mode={'SS':not opp,'SU':not same,'US':not same,'UU':not opp}
  # Exhaustively check coherent assignments to the original shared source variables.
  vars_=sorted(set(sj)|set(sk));observed=set()
  for b in itertools.product((0,1),repeat=len(vars_)):
   a=dict(zip(vars_,b));vj=sum(a[abs(z)]==int(z>0) for z in F[j]);vk=sum(a[abs(z)]==int(z>0) for z in F[k]);checked+=1
   if vj in (0,len(F[j])) and vk in (0,len(F[k])):
    observed.add(('S' if vj==len(F[j]) else 'U')+('S' if vk==len(F[k]) else 'U'))
  assert observed=={key for key,val in mode.items() if val},(j,k,mode,observed)
  result.append({'j':j+1,'k':k+1,'shared_same':same,'shared_opposite':opp,'SS_SU_US_UU':mode})
 return result,checked

def resolution(F,n,limit=12):
 out=[]
 for i,j in itertools.combinations(range(len(F)),2):
  for piv in F[i]:
   if -piv not in F[j]:continue
   res=set(F[i])|set(F[j]);res.discard(piv);res.discard(-piv)
   if any(-z in res for z in res):continue
   r=sorted(res,key=lambda z:(abs(z),z))
   cube={abs(z):int(z<0) for z in r}
   # Every extension of the cube makes at least one of its source parents false.
   unset=[v for v in range(1,n+1) if v not in cube]
   if len(unset)<=12:
    for bits in itertools.product((0,1),repeat=len(unset)):
     a=sum((val<<(v-1)) for v,val in {**cube,**dict(zip(unset,bits))}.items())
     assert truth(F[i],a)==0 or truth(F[j],a)==0
   out.append({'parents':[i+1,j+1],'pivot':piv,'resolvent':r,'forbidden_cube':{str(v):val for v,val in cube.items()},
               'proof':'Falsifying R forces pivot and its negation via the two source clauses.'})
   if len(out)>=limit:return out
 return out

def count_constraints(n,anchor,r,req,pins=None,w=None):
 # req maps original variables v(1-based) -> original value required by source U event.
 assigned={} if pins is None else dict(pins)
 if w is not None:w.add('constraint_merge',len(req))
 for v,val in req.items():
  flip=val^((anchor>>(v-1))&1)
  if v in assigned and assigned[v]!=flip:return 0
  assigned[v]=flip
 rem=n-len(assigned);needed=r-sum(assigned.values())
 if w is not None:w.add('binomial_evaluation')
 return math.comb(rem,needed) if 0<=needed<=rem else 0

def required_false(c):return {abs(z):int(z<0) for z in c}
def merge_required(a,b):
 x=dict(a)
 for v,val in b.items():
  if v in x and x[v]!=val:return None
  x[v]=val
 return x

def count_pair(F,n,anchor,r,i,j,w):
 a=merge_required(required_false(F[i]),required_false(F[j]))
 if a is None:return 0
 return count_constraints(n,anchor,r,a,w=w)

def maximum_overlap_tree(F,n,anchor,r,w):
 m=len(F);p=[count_constraints(n,anchor,r,required_false(c),w=w) for c in F]
 den=math.comb(n,r);w.add('source_literal_read',sum(len(c) for c in F))
 scores=[]
 for i in range(m):
  for j in range(i+1,m):
   w.add('pair_inspection')
   scores.append((count_pair(F,n,anchor,r,i,j,w),i,j))
 scores.sort(key=lambda t:(-t[0],t[1],t[2]));w.add('sort_comparisons_proxy',len(scores)*max(1,len(scores).bit_length()))
 parent=list(range(m))
 def root(z):
  while parent[z]!=z:parent[z]=parent[parent[z]];z=parent[z]
  return z
 tree=[]
 for count,i,j in scores:
  w.add('union_find_probe',2)
  pi,pj=root(i),root(j)
  if pi!=pj:
   parent[pi]=pj;tree.append((i,j,count))
   if len(tree)==m-1:break
 upper=sum(p)-sum(z for _,_,z in tree)
 assert len(tree)==max(0,m-1)
 return {'denominator':den,'union_numerator':sum(p),'hunter_numerator':upper,'per_clause':p,
         'tree':tree,'certificate':upper<den}

def weighted_count(F,n,anchor,r,tree,pins,w):
 # Fixed rooted-tree upper bound scaled by number of compatible layer assignments.
 sums=0
 for c in F:
  w.add('source_literal_read',len(c));sums+=count_constraints(n,anchor,r,required_false(c),pins,w)
 for i,j,_ in tree:
  w.add('pair_inspection')
  req=merge_required(required_false(F[i]),required_false(F[j]))
  if req is not None:sums-=count_constraints(n,anchor,r,req,pins,w)
 den=count_constraints(n,anchor,r,{},pins,w)
 assert 0<=sums or den==0,(sums,den)
 return sums,den

def construct(F,n,anchor,r,bound,w):
 assert bound['certificate']
 tree=bound['tree'];pins={};logs=[]
 num=bound['hunter_numerator'];den=bound['denominator']
 for v in range(1,n+1):
  cand=[]
  for flip in (0,1):
   p={**pins,v:flip};x,d=weighted_count(F,n,anchor,r,tree,p,w)
   if d>0:cand.append((x,d,flip))
  assert cand
  assert sum(x for x,d,f in cand)==num and sum(d for x,d,f in cand)==den
  # Compare exactly, avoiding floating-point proof dependencies.
  chosen=min(cand,key=lambda z:(0 if z[0]*den<=num*z[1] else 1,z[2]))
  assert chosen[0]*den<=num*chosen[1]
  pins[v]=chosen[2];num,den=chosen[0],chosen[1]
  logs.append({'variable':v,'chosen_flip':chosen[2],'weighted_hunter_numerator':num,'remaining_layer_size':den})
 assert den==1 and num==0
 flipmask=sum(f<<(v-1) for v,f in pins.items());assert flipmask.bit_count()==r
 witness=anchor^flipmask
 w.add('final_witness_clause_read',sum(len(c) for c in F))
 assert all(truth(c,witness) for c in F)
 return witness,logs

def up(F,n,assigned,w):
 # Source-level implication provenance: each forced original-variable value records its source clause ID.
 implied=[]
 while True:
  forced=None
  for j,c in enumerate(F,1):
   alive=False;missing=[]
   for z in c:
    w.add('source_literal_read')
    v=abs(z)
    if v not in assigned:missing.append(z)
    elif assigned[v]==int(z>0):alive=True;break
   if alive:continue
   if not missing:return None,implied,j
   if len(missing)==1:forced=(missing[0],j);break
  if forced is None:return assigned,implied,None
  z,j=forced;v=abs(z);val=int(z>0)
  if v in assigned:
   if assigned[v]!=val:return None,implied,j
  else:assigned[v]=val;implied.append((v,val,j));w.add('unit_assignment')

def dpll(F,n,w,branch_assign=None):
 branch_assign={} if branch_assign is None else branch_assign
 w.add('DPLL_nodes')
 assigned,imp,clause=up(F,n,dict(branch_assign),w)
 if clause is not None:
  w.add('DPLL_conflict_leaves');return None,{'unit':imp,'conflict_clause':clause}
 if len(assigned)==n:
  mask=sum(z<<(v-1) for v,z in assigned.items())
  w.add('final_witness_clause_read',sum(len(c) for c in F))
  assert all(truth(c,mask)>0 for c in F)
  return mask,{'unit':imp,'witness':mask}
 v=min(set(range(1,n+1))-set(assigned));w.add('branch_selection',n-len(assigned))
 children=[]
 for val in (0,1):
  a,child=dpll(F,n,w,{**assigned,v:val})
  children.append((val,child))
  if a is not None:return a,{'unit':imp,'branch':v,'children':children}
 return None,{'unit':imp,'branch':v,'children':children}

def verify_tree(F,n,node,branch=None):
 branch={} if branch is None else dict(branch)
 for v,val,j in node.get('unit',[]):
  assert v not in branch
  # The original source clause must be unit under current partial assignment.
  c=F[j-1];alive=False;miss=[]
  for z in c:
   if abs(z) not in branch:miss.append(z)
   elif branch[abs(z)]==int(z>0):alive=True
  assert not alive and len(miss)==1 and abs(miss[0])==v and int(miss[0]>0)==val
  branch[v]=val
 if 'conflict_clause' in node:
  assert all(abs(z) in branch and branch[abs(z)]!=int(z>0) for z in F[node['conflict_clause']-1]);return False
 if 'witness' in node:
  a=node['witness'];assert len(branch)==n and all(branch[v]==((a>>(v-1))&1) for v in branch)
  assert all(truth(c,a) for c in F);return True
 v=node['branch'];assert v not in branch
 children=node['children'];assert [x for x,_ in children] in ([0],[0,1])
 results=[verify_tree(F,n,ch,{**branch,v:val}) for val,ch in children]
 if len(children)==1:assert results[0] # short-circuited SAT
 if len(children)==2:assert results[0] is False
 return any(results)

def measured(call):
 w=Work();tracemalloc.start();t=time.perf_counter()
 try:r=call(w)
 finally:
  secs=time.perf_counter()-t;_,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
 return r,{'seconds':round(secs,6),'peak_traced_bytes':peak,'events':w.data(),
           'selected_operations':sum(w.events.values())}

def audit(name,F,n,mini=True):
 strict=name.startswith('STRICT22');validate(F,n,strict)
 full=[status(F,0),status(F,(1<<n)-1)]
 pairs,checks=pair_modes(F)
 for j,c in enumerate(F):
  for a in [0,(1<<n)-1]:
   assert truth(c,a)+truth(c,((1<<n)-1)^a)==len(c)
 masks=[0]+[1<<i for i in range(min(3,n))]+[(1<<min(3,n))-1,(1<<n)-1]
 trail=[status(F,a) for a in masks]
 for a in masks:
  if all(len(c)==3 for c in F):
   x=status(F,a)['N'];z=status(F,a^((1<<n)-1))['N'];assert x==list(reversed(z))
 return {'name':name,'n':n,'m':len(F),'strict22':strict,'local_targets':extrema(F),
         'pair_matrix':pairs if mini else [x for x in pairs if x['shared_same'] or x['shared_opposite']],
         'pair_complete_support_assignments':checks,'endpoints':full,'flip_trail':trail,
         'resolvent_proofs':resolution(F,n,8)}

def controls():
 # Deterministic nontrivial strict22 control, known source with 9 variables and 12 distinct clauses.
 primary=[]
 for name in CASES:
  F,n=parse(name)
  a=audit(name,F,n,mini=name=='STRICT22_N9_HUNTER')
  anchors=[(0,3)] if name=='STRICT22_N9_HUNTER' else [(0,min(3,n)),((1<<n)-1,min(3,n))]
  def base(w):
   sol,pr=dpll(F,n,w);assert verify_tree(F,n,pr)==(sol is not None)
   w.add('UNSAT_proof_or_SAT_witness_replay',len(F)*(n+1))
   return {'sat':sol is not None,'witness':sol,'DPLL_nodes':w.events['DPLL_nodes'],'DPLL_conflict_leaves':w.events['DPLL_conflict_leaves']}
  b,bt=measured(base)
  def controller(w):
   for anchor,r in anchors:
    w.add('strategy_choice')
    bound=maximum_overlap_tree(F,n,anchor,r,w)
    if bound['certificate']:
     sol,log=construct(F,n,anchor,r,bound,w)
     w.add('witness_proof_audit',len(F)*3)
     return {'sat':True,'witness':sol,'anchor':anchor,'radius':r,'bound':bound,'conditional_steps':log,'used_fallback':False,'DPLL_nodes':0}
   sol,pr=dpll(F,n,w);assert verify_tree(F,n,pr)==(sol is not None)
   w.add('UNSAT_proof_or_SAT_witness_replay',len(F)*(n+1))
   return {'sat':sol is not None,'witness':sol,'used_fallback':True,'DPLL_nodes':w.events['DPLL_nodes'],'last_bound':bound}
  h,ht=measured(controller)
  assert b['sat']==h['sat'],name
  if n<=15:
   oracle=[i for i in range(1<<n) if all(truth(c,i) for c in F)]
   assert bool(oracle)==b['sat']
   if b['witness'] is not None:assert b['witness'] in oracle
   if h['witness'] is not None:assert h['witness'] in oracle
   a['exhaustive_model_count']=len(oracle)
   if name=='STRICT22_N9_HUNTER':
    rr=h['radius'];anchor=h['anchor'];a['radius_model_count']=sum((z^anchor).bit_count()==rr for z in oracle)
  a['baseline']={'result':b,'resources':bt}
  a['hunter_controller']={'result':h,'resources':ht}
  if name=='STRICT22_N9_HUNTER':
   assert not a['endpoints'][0]['sat'] and not a['endpoints'][1]['sat']
   assert h['bound']['union_numerator']>=h['bound']['denominator']
   assert h['bound']['hunter_numerator']<h['bound']['denominator']
   assert h['bound']['hunter_numerator']==83 and h['bound']['denominator']==84
  if name.endswith('UNSAT'):assert not b['sat']
  primary.append(a)
 return primary

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',default='HAMMING_HUNTER251_raw.json');args=p.parse_args()
 cases=controls();res={'method':'Hamming-layer Hunter (1976) spanning tree + exact conditional expectation',
  'claim':'A source-verified strict22 distinct-clause n=9 instance has Hamming radius 3 SAT certificate 83<84, where uncorrected union count is 126>=84',
  'machine':'CPython 3 integer arithmetic; wall time and tracemalloc per controller exclude external oracle/audit; selected-op proxy includes graph sort, scan, failed probes, source check',
  'sources':{'github_issue':'https://github.com/j15marti/pnp/issues/3','hunter_primary':'https://doi.org/10.2307/3212481',
   'kullmann_primary':'https://doi.org/10.1007/978-3-540-24605-3_32'},
  'cases':cases}
 with open(args.out,'w') as fh:json.dump(res,fh,indent=2)
 for c in cases:
  x=c['hunter_controller']['result'];b=c['baseline']['resources'];h=c['hunter_controller']['resources']
  print(c['name'], 'SAT' if x['sat'] else 'UNSAT','models',c.get('exhaustive_model_count'),
       'Hunter',x.get('bound',x.get('last_bound',{})).get('hunter_numerator'),'/',
       x.get('bound',x.get('last_bound',{})).get('denominator'), 'fallback',x['used_fallback'],
       'nodes',c['baseline']['result']['DPLL_nodes'],x['DPLL_nodes'],
       'time',b['seconds'],h['seconds'],'ops',b['selected_operations'],h['selected_operations'])
 print('ALL INDEPENDENT SOURCE, EXTREME, PAIR MATRIX, HUNTER, WITNESS, UNSAT PROOF AND EXHAUSTIVE CHECKS PASSED')