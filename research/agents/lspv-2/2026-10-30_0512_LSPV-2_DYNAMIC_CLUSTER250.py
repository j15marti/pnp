#!/usr/bin/env python3
"""DYNAMIC-CLUSTER250: source-preserving exact fixed-radius flip histograms.
Usage: python 2026-10-30_0512_LSPV-2_DYNAMIC_CLUSTER250.py --cases cases250.json --out raw250.json --radius 2
All random controls use fixed seed. Standard library only.
"""
import argparse,collections,itertools,json,math,random,time,tracemalloc
from fractions import Fraction

class Ledger:
 def __init__(self): self.v=collections.Counter()
 def tick(self,key,qty=1):self.v[key]+=qty
 def out(self):return dict(self.v)

def evaluate(clauses,a,ledger=None):
 t=[]
 for c in clauses:
  z=0
  for l in c:
   z+=(a[abs(l)-1]==(l>0))
   if ledger: ledger.tick('literal_reads')
  t.append(z)
 return t,tuple(t.count(r) for r in range(4))

def targets(clauses):
 out=[]
 for j,c in enumerate(clauses,1):
  rec=[]
  for l in c:
   s=int(l>0);u=1-s
   rec.append({'occurrence':f'x_{{{abs(l)},{j}}}','literal':l,'S':s,'invert_S_is_U':1-s,'U':u,'invert_U_is_S':1-u})
  out.append({'C_j':j,'literals':c,'S_occurrences':rec,'S':{str(abs(l)):int(l>0) for l in c},'U':{str(abs(l)):int(l<0) for l in c}})
 return out

def pairmatrix(clauses):
 out=[]
 for j,k in itertools.combinations(range(len(clauses)),2):
  s1={abs(l):int(l>0) for l in clauses[j]};s2={abs(l):int(l>0) for l in clauses[k]}
  shared=set(s1)&set(s2)
  same=sorted(i for i in shared if s1[i]==s2[i]);opp=sorted(i for i in shared if s1[i]!=s2[i])
  modes={'SS':not bool(opp),'SU':not bool(same),'US':not bool(same),'UU':not bool(opp)}
  # The mode check enumerates ONLY one coherent assignment per union support.
  for x,y in itertools.product(('S','U'),repeat=2):
   a={i:(v if x=='S' else 1-v) for i,v in s1.items()}
   feasible=all(a.get(i,(v if y=='S' else 1-v))==(v if y=='S' else 1-v) for i,v in s2.items())
   assert feasible==modes[x+y],(j,k,x,y)
  out.append({'j':j+1,'k':k+1,'same':same,'opposite':opp,'SS_SU_US_UU':modes})
 return out

def resolution_dag(clauses,n,max_nodes=10):
 nodes=[{'id':f'C{j+1}','clause':c[:],'original':True} for j,c in enumerate(clauses)]
 known={tuple(sorted(c)):f'C{j+1}' for j,c in enumerate(clauses)}
 deriv=[]
 # Stage 1: source-parent clauses; stage 2: previously derived clauses with source clauses.
 for stage in (0,1):
  roots=nodes[:] if stage else nodes[:len(clauses)]
  for p in roots:
   for q in nodes[:len(clauses)]:
    if p['id']==q['id']:continue
    for lit in p['clause']:
     if -lit not in q['clause']:continue
     new=set(p['clause']);new.remove(lit);new.update(v for v in q['clause'] if v!=-lit)
     if any(-v in new for v in new):continue
     key=tuple(sorted(new))
     if key in known or not key:continue
     nid=f'R{len(deriv)+1}';a={'id':nid,'clause':list(key),'original':False,
      'parent1':p['id'],'parent2':q['id'],'pivot_literal_from_parent1':lit}
     nodes.append(a);deriv.append(a);known[key]=nid
     if len(deriv)>=max_nodes:break
    if len(deriv)>=max_nodes:break
   if len(deriv)>=max_nodes:break
  if len(deriv)>=max_nodes:break
 # Independently replay every resolution pivot from its actual previous parents.
 seen={x['id']:x['clause'] for x in nodes[:len(clauses)]}
 for r in deriv:
  A=seen[r['parent1']];B=seen[r['parent2']];lit=r['pivot_literal_from_parent1']
  assert lit in A and -lit in B
  new=set(A)-{lit};new.update(set(B)-{-lit})
  assert not any(-v in new for v in new)
  assert sorted(new)==r['clause']
  r['forbidden_original_variable_cube']={str(abs(v)):int(v<0) for v in r['clause']}
  r['resolution_verified_by_independent_replay']=True
  seen[r['id']]=r['clause']
 return deriv

def triple_modes(clauses,n,limit=6):
 out=[]
 for ids in list(itertools.combinations(range(len(clauses)),3))[:limit]:
  modes={}
  support=sorted(set(abs(l) for j in ids for l in clauses[j]))
  for mode in itertools.product(('S','U'),repeat=3):
   req={};good=True
   for j,ext in zip(ids,mode):
    for lit in clauses[j]:
     v=int(lit>0) if ext=='S' else int(lit<0)
     if abs(lit) in req and req[abs(lit)]!=v:good=False
     req[abs(lit)]=v
   found=False
   for bits in itertools.product((0,1),repeat=len(support)):
    a={k:v for k,v in zip(support,bits)}
    if all(sum(a[abs(l)]==(l>0) for l in clauses[j])==(3 if ext=='S' else 0)
      for j,ext in zip(ids,mode)):
     found=True;break
   assert found==good
   modes[''.join(mode)]=good
  out.append({'original_clause_indices':[i+1 for i in ids],'modes':modes})
 return out

def recognize_special(clauses):
 horn=all(sum(l>0 for l in c)<=1 for c in clauses)
 dual_horn=all(sum(l<0 for l in c)<=1 for c in clauses)
 two_sat=all(len(c)<=2 for c in clauses)
 by_support=collections.defaultdict(set)
 for c in clauses:
  if len(c)==3:
   ids=sorted(abs(l) for l in c)
   mask=tuple(int(next(l for l in c if abs(l)==i)<0) for i in ids)
   by_support[tuple(ids)].add(mask)
 xorblocks=[]
 for support,masks in by_support.items():
  for parity in (0,1):
   P={a for a in itertools.product((0,1),repeat=3) if sum(a)%2==parity}
   if P<=masks:xorblocks.append({'support':support,'excluded_sign_parity':parity,
      'certified_semantics':'The four clauses exclude all assignments with their literal signs matching the listed masks.'})
 return {'source_Horn':horn,'source_dual_Horn':dual_horn,'source_two_SAT':two_sat,'complete_XOR3_encoding_blocks':xorblocks}

def source_checks(clauses,n,trail):
 assert all(len(c)==3 and len({abs(v) for v in c})==3 for c in clauses)
 local=targets(clauses);pairs=pairmatrix(clauses)
 paths={}
 for bit in (0,1):
  a=[bit]*n;states=[]
  for x in [None]+trail:
   if x is not None:a[x]^=1
   t,N=evaluate(clauses,a)
   states.append({'flip_source_variable':None if x is None else x+1,'a':a[:], 't_j':t,'N0_N1_N2_N3':N,'source_SAT':N[0]==0})
   comp=[1-y for y in a];ct,cN=evaluate(clauses,comp)
   assert ct==[3-h for h in t] and cN==tuple(reversed(N))
  paths[str(bit)+'^n']=states
 return {'local_extremes_and_inverses':local,'pair_modes':pairs,'triple_modes':triple_modes(clauses,n), 'globally_coherent_endpoint_and_flip_trails':paths,'source_resolution_DAG':resolution_dag(clauses,n),'syntactic_tractable_structure':recognize_special(clauses)}

def strict22(clauses,n):
 occ=[collections.Counter() for _ in range(n)]
 for c in clauses:
  for l in c:occ[abs(l)-1]['p' if l>0 else 'n']+=1
 return all(x['p']==2 and x['n']==2 for x in occ)

def adjacency(clauses,n):
 out=[set() for _ in range(n)];inc=[[] for _ in range(n)]
 for j,c in enumerate(clauses):
  vs=[abs(l)-1 for l in c]
  for i in vs:
   inc[i].append(j);out[i].update(v for v in vs if v!=i)
 return out,inc

def connected_sets(adj,r):
 seen=set()
 for v in range(len(adj)):
  todo=[frozenset([v])]
  while todo:
   t=todo.pop()
   if t in seen:continue
   seen.add(t)
   if len(t)<r:
    for v in t:
     for nb in adj[v]-t:todo.append(t|{nb})
 return tuple(sorted(seen,key=lambda s:(len(s),tuple(sorted(s)))))

def submasks(T):
 arr=sorted(T)
 for k in range(len(arr)+1):
  yield from (frozenset(c) for c in itertools.combinations(arr,k))

def addto(x,other,k=1):
 for h,v in other.items():
  x[h]+=k*v
  if not x[h]:del x[h]

def multiply(P,Q,r,ledger):
 out=collections.defaultdict(Fraction)
 for (a,da),va in P.items():
  for (b,db),vb in Q.items():
   ledger.tick('laurent_pair_multiply')
   if a+b<=r:out[(a+b,tuple(x+y for x,y in zip(da,db)))]+=va*vb
 return {k:v for k,v in out.items() if v}

class Dynamic:
 def __init__(self,clauses,n,base,r=2):
  self.c=[list(x) for x in clauses];self.n=n;self.a=base[:];self.r=r;self.Ledger=Ledger()
  self.adj,self.inc=adjacency(self.c,n)
  self.balanced=all(sum(l==i+1 for c in self.c for l in c)==sum(l==-(i+1) for c in self.c for l in c) for i in range(n))
  self.dim=2 if self.balanced else 4;self.zero=(0,)*self.dim
  self.ts,self.N=evaluate(self.c,self.a,self.Ledger)
  self.Ts=connected_sets(self.adj,r)
  self.support_index=[set() for _ in range(n)]
  for T in self.Ts:
   for i in T:self.support_index[i].add(T)
  self.W={};self.L=[collections.defaultdict(Fraction) for _ in range(r+1)]
  for T in self.Ts:self._replace(T)
  self.E=self._recover()
 def _delta(self,S):
  affected=set(j for i in S for j in self.inc[i]);cnt=[0]*4
  for j in affected:
   t=self.ts[j];d=0
   for l in self.c[j]:
    if abs(l)-1 in S:d+=1 if self.a[abs(l)-1]!=(l>0) else -1
    self.Ledger.tick('local_source_literal_scan')
   assert 0<=t+d<=3
   cnt[t]-=1;cnt[t+d]+=1
  self.Ledger.tick('local_subset_clause_reads',len(affected))
  return (cnt[0],cnt[3]) if self.balanced else tuple(cnt)
 def _log(self,U):
  A={}
  for S in submasks(U):
   if not S:continue
   k=(len(S),self._delta(S));A[k]=A.get(k,0)+1
  out=collections.defaultdict(Fraction);term={(0,self.zero):Fraction(1)}
  for p in range(1,self.r+1):
   term=multiply(term,A,self.r,self.Ledger)
   for key,val in term.items():out[key]+=Fraction((-1)**(p+1),p)*val
  return {k:v for k,v in out.items() if v}
 def _support(self,T):
  w=collections.defaultdict(Fraction)
  for U in submasks(T):
   if not U:continue
   d=(-1)**(len(T)-len(U));addto(w,self._log(U),d)
  return dict(w)
 def _replace(self,T):
  if T in self.W:
   for (k,shift),coef in self.W[T].items():
    key=shift;self.L[k][key]-=coef
    if not self.L[k][key]:del self.L[k][key]
  w=self._support(T);self.W[T]=w
  for (k,shift),coef in w.items():
   self.L[k][shift]+=coef
   if not self.L[k][shift]:del self.L[k][shift]
  self.Ledger.tick('connected_support_recalculations')
 def _recover(self):
  E=[{self.zero:Fraction(1)}]
  for k in range(1,self.r+1):
   F=collections.defaultdict(Fraction)
   for j in range(1,k+1):
    for a,ca in self.L[j].items():
     for b,cb in E[k-j].items():
      self.Ledger.tick('recovery_multiplications')
      F[tuple(x+y for x,y in zip(a,b))]+=j*ca*cb
   E.append({p:c/k for p,c in F.items() if c})
   assert all(c.denominator==1 and c>=0 for c in E[-1].values()),('coefficient invalid',k,E[-1])
   assert sum(E[-1].values())==math.comb(self.n,k),(self.n,k,sum(E[-1].values()))
  return E
 def flip(self,x):
  assert 0<=x<self.n
  self.a[x]^=1
  for j in self.inc[x]:
   old=self.ts[j];l=next(l for l in self.c[j] if abs(l)==x+1)
   new=old+(1 if self.a[x]==(l>0) else -1)
   self.N=list(self.N);self.N[old]-=1;self.N[new]+=1;self.N=tuple(self.N)
   self.ts[j]=new;self.Ledger.tick('incremental_source_clause_status_updates')
  hit=self.adj[x]|{x}
  changed=set().union(*(self.support_index[i] for i in hit))
  self.Ledger.tick('source_index_support_reads',sum(len(self.support_index[i]) for i in hit))
  for T in changed:self._replace(T)
  self.E=self._recover()
  return len(changed)
 def histogram(self,k):
  hist=collections.Counter()
  for d,v in self.E[k].items():
   if self.balanced:
    n0=self.N[0]+d[0];n3=self.N[3]+d[1];m=len(self.c)
    z=(n0,m//2-2*n0+n3,m//2+n0-2*n3,n3)
   else:z=tuple(x+y for x,y in zip(self.N,d))
   hist[z]+=int(v)
  return hist

def dpll(clauses,n):
 led=Ledger();nodes=0;leaves=0
 def go(rho):
  nonlocal nodes,leaves
  nodes+=1
  while True:
   change=False
   for j,c in enumerate(clauses):
    free=[];sat=False
    for l in c:
     led.tick('DPLL_literal_reads')
     v=abs(l)-1
     if v in rho:
      if rho[v]==(l>0):sat=True;break
     else:free.append(l)
    if sat:continue
    if not free:leaves+=1;return None
    if len(free)==1:
     v=abs(free[0])-1;val=free[0]>0
     if v in rho and rho[v]!=val:leaves+=1;return None
     if v not in rho:rho[v]=val;change=True;led.tick('DPLL_unit_assignments');break
   if not change:break
  if len(rho)==n:
   a=[int(rho[i]) for i in range(n)];return a if evaluate(clauses,a)[1][0]==0 else None
  var=next(x for x in range(n) if x not in rho)
  for val in (False,True):
   ans=go({**rho,var:val})
   if ans is not None:return ans
  return None
 witness=go({});return {'sat':witness is not None,'witness':witness,'nodes':nodes,'leaves':leaves,**led.out()}

def hybrid_controller(clauses,n,r=2,flip_budget=5):
 """Uniform deterministic prepass: full source retained; no answer advice."""
 ledger=Ledger()
 B=Dynamic(clauses,n,[0]*n,r);witness=None;source_queries=0
 flip_path=([0,1,2,0,3] if n>=4 else ([0,1,0] if n>=2 else [0]))[:flip_budget]
 for ix in [None]+flip_path:
  if ix is not None:B.flip(ix)
  # No free answer bit: exact histogram is computed from original clause semantics.
  possible=[k for k in range(r+1) if any(v[0]==0 for v in B.histogram(k))]
  ledger.tick('histogram_queries',r+1)
  if not possible:continue
  for k in possible:
   for S in itertools.combinations(range(n),k):
    ledger.tick('witness_source_flip_candidates')
    a=B.a[:]
    for i in S:a[i]^=1
    cnt,N=evaluate(clauses,a,ledger)
    if N[0]==0:witness=a;break
   if witness is not None:break
  if witness is not None:break
 if witness is not None:
  assert evaluate(clauses,witness)[1][0]==0
  ans={'sat':True,'witness':witness,'backend_DPLL_nodes':0,'backend_DPLL_literal_reads':0}
 else:
  back=dpll(clauses,n)
  ans={'sat':back['sat'],'witness':back['witness'],'backend_DPLL_nodes':back['nodes'],
       'backend_DPLL_literal_reads':back.get('DPLL_literal_reads',0),'backend_DPLL_leaves':back.get('leaves',0)}
 ans['prepass_ledger']=B.Ledger.out()
 ans['branch_and_verification_ledger']=ledger.out()
 return ans

def make_audit(item,r=2,max_flips=5):
 c=item['clauses'];n=item['n'];name=item['name'];flips=([0,1,2,0,3] if n>=4 else ([0,1,0] if n>=2 else [0]))[:max_flips]
 t0=time.perf_counter();tracemalloc.start()
 baseline=dpll(c,n)
 bsec=time.perf_counter()-t0;bpk=tracemalloc.get_traced_memory()[1];tracemalloc.stop()
 t0=time.perf_counter();tracemalloc.start()
 B=Dynamic(c,n,[0]*n,r);initial_supports=len(B.Ts)
 trace=[];snapshot=[]
 for x in [None]+flips:
  affected=None if x is None else B.flip(x)
  H={str(k):{','.join(map(str,q)):int(v) for q,v in B.histogram(k).items()} for k in range(r+1)}
  trace.append({'source_flip_variable':None if x is None else x+1,'global_base_assignment':B.a[:],
   'global_base_N':B.N,'changed_connected_supports':affected,'all_exact_radius_histograms':H})
  snapshot.append((B.a[:],[B.histogram(k) for k in range(r+1)]))
 dynamic_seconds=time.perf_counter()-t0;dynamic_peak=tracemalloc.get_traced_memory()[1];tracemalloc.stop()
 t0=time.perf_counter();tracemalloc.start()
 fresh_supports=[];fresh_total_work=collections.Counter()
 for a,H in snapshot:
  fresh=Dynamic(c,n,a,r)
  assert [fresh.histogram(k) for k in range(r+1)]==H
  fresh_supports.append(len(fresh.Ts));fresh_total_work.update(fresh.Ledger.out())
 fresh_seconds=time.perf_counter()-t0;fresh_peak=tracemalloc.get_traced_memory()[1];tracemalloc.stop()
 # Independent enumerative verification is NOT part of any solver or compiler time above.
 checks=0
 for aa,H in snapshot:
  for k in range(r+1):
   brute=collections.Counter()
   for S in itertools.combinations(range(n),k):
    a=aa[:]
    for i in S:a[i]^=1
    _,v=evaluate(c,a)
    brute[v]+=1;checks+=1
   assert brute==H[k],(name,k,brute,H[k])
  _,N=evaluate(c,aa);assert N==H[0].most_common(1)[0][0]
 t0=time.perf_counter();tracemalloc.start()
 hybrid=hybrid_controller(c,n,r,flip_budget=max_flips)
 hybrid_seconds=time.perf_counter()-t0;hybrid_peak=tracemalloc.get_traced_memory()[1];tracemalloc.stop()
 assert hybrid['sat']==baseline['sat'],(name,hybrid,baseline)
 audit=source_checks(c,n,flips)
 return {'family':name,'n':n,'m':len(c),'strict22':strict22(c,n),'source_origin':item['source_origin'],
  'source_clauses':c,'source_extreme_audit':audit,'hybrid_solver':{'result':hybrid,'seconds':hybrid_seconds,'traced_peak_bytes':hybrid_peak},'baseline_DPLL':{'result':baseline,'seconds':bsec,'traced_peak_bytes':bpk},
  'fresh_compiler':{'seconds_including_all_restarts':fresh_seconds,'traced_peak_bytes':fresh_peak,'ledger':dict(fresh_total_work)},
  'dynamic_compiler':{'radius':r,'seconds_including_initialization_and_updates':dynamic_seconds,'traced_peak_bytes':dynamic_peak,
   'initial_source_connected_supports':initial_supports,'ledger':B.Ledger.out(),'coherent_flips':trace,
   'external_bruteforce_radius_states_verified':checks}}

def main():
 p=argparse.ArgumentParser();p.add_argument('--cases',default='cases250.json');p.add_argument('--out',default='raw250.json');p.add_argument('--radius',type=int,default=2);p.add_argument('--limit',type=int,default=10);a=p.parse_args()
 cases=json.load(open(a.cases));rows=[]
 for c in cases[:a.limit]:
  t=time.perf_counter();row=make_audit(c,r=min(a.radius,c['n']),max_flips=5);row['elapsed_seconds']=time.perf_counter()-t
  print(c['name'],'dynamic',round(row['dynamic_compiler']['seconds_including_initialization_and_updates'],4),'DPLL nodes',row['baseline_DPLL']['result']['nodes'],'time',round(row['elapsed_seconds'],3),flush=True)
  rows.append(row)
 width2=[]
 for name,formula,n in [('2SAT_SAT',[[1,2],[-1,2],[-2,3]],3),
                         ('2SAT_UNSAT',[[1,2],[-1,2],[1,-2],[-1,-2]],2)]:
  got=dpll(formula,n);exhaustive=any(all(any((bits[abs(l)-1]==(l>0)) for l in c) for c in formula)
    for bits in itertools.product((0,1),repeat=n))
  assert got['sat']==exhaustive
  width2.append({'name':name,'n':n,'clauses':formula,'source_S_U_targets':targets(formula),
   'source_SS_SU_US_UU_pair_modes':pairmatrix(formula),'decision':got,'independent_full_oracle_sat':exhaustive})
 with open(a.out,'w') as f:json.dump({'run_id':'DYNAMIC-CLUSTER250','seed':'deterministic, no random samples',
 'cases':rows,'width2_controls':width2,'model':'Python exact Fraction; benchmark tracemalloc excludes brute-force source verification'},f,indent=2)
 print('WROTE',a.out)
if __name__=='__main__':main()