#!/usr/bin/env python3
"""Source-authenticated bounded-radius flip spectrum and derivative witness extraction.
LSPV-2 DERIVATIVE-WITNESS248, Python 3 standard library.
Run: python 2026-10-30_0412_LSPV-2_DERIVATIVE_WITNESS248.py OUT.json
No equity scores. Independent brute-force labels are checker-only.
"""
from collections import defaultdict,Counter
from fractions import Fraction
import itertools as it, json, math, sys, time, tracemalloc, hashlib, random

W1='-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'
S15='-1 -3 14;2 8 -9;-10 13 14;3 -7 -13;-4 9 -11;-5 -8 -14;4 -8 11;1 7 -13;1 -7 10;-5 -6 15;-2 6 -12;4 9 -10;-2 5 -12;3 6 -15;-6 7 11;2 -9 -11;-4 8 10;-3 12 15;5 12 -15;-1 13 -14'
def parse(s):return tuple(tuple(int(z) for z in c.split()) for c in s.split(';'))
def plateau(r):
 def v(j,i):return 6*(j%r)+i
 cs=[]
 for j in range(r):
  cs += [(v(j-1,1),v(j,3),v(j,5)),(v(j,1),-v(j,3),v(j,6)),(-v(j,1),v(j,4),v(j,5)),(-v(j,1),-v(j,4),v(j,6)),(v(j,2),v(j,3),-v(j,5)),(v(j,2),-v(j,3),-v(j,6)),(-v(j,2),v(j,4),-v(j,5)),(-v(j,2),-v(j,4),-v(j,6))]
 return tuple(cs)
def paired_k4():
    z=((1,2,3),(-1,4,5),(2,4,6),(3,5,6))
    return z+tuple(tuple(-x for x in c) for c in z)
def adversarial_relabel(F):
    n=nvars(F);perm={i:n+1-i for i in range(1,n+1)}
    return tuple(tuple((1 if z>0 else -1)*(-1 if abs(z)%3==0 else 1)*perm[abs(z)] for z in c) for c in reversed(F))
def phase_invert(F,bitstring):
    assert len(bitstring)==nvars(F)
    return tuple(tuple(-z if bitstring[abs(z)-1]=='1' else z for z in c) for c in F)
def parity3(even=True):
 return tuple(tuple(-(i+1) if b[i] else i+1 for i in range(3)) for b in it.product((0,1),repeat=3) if sum(b)%2!=int(even))
def littrue(z,assignment):return assignment[abs(z)]==int(z>0)
def counts(F,a):return tuple(sum(littrue(z,a) for z in c) for c in F)
def N4(F,a):
 c=Counter(counts(F,a));return tuple(c[i] for i in range(4))
def sat(F,a):return N4(F,a)[0]==0
def nvars(F):return max(abs(z) for c in F for z in c)
def exact22(F):
 n=nvars(F);count=Counter(z for c in F for z in c)
 return all(len(c)==3 and len(set(map(abs,c)))==3 for c in F) and all(count[i]==count[-i]==2 for i in range(1,n+1))
def connected(F):
 n=nvars(F);g={i:set() for i in range(1,n+1)}
 for c in F:
  for i,j in it.combinations(map(abs,c),2):g[i].add(j);g[j].add(i)
 seen={1};queue=[1]
 for i in queue:
  for j in sorted(g[i]-seen):seen.add(j);queue.append(j)
 return len(seen)==n

def extremes(F):
 rows=[]
 for j,c in enumerate(F,1):
  rows.append({'source_clause':j,'signed_literals':list(c),
      'occurrences':[{'x_i_j':[abs(z),j],'sign':1 if z>0 else -1,
       'S_literal_TRUE':int(z>0),'S_inverted_U':int(z<0),
       'U_literal_FALSE':int(z<0),'U_inverted_S':int(z>0)} for z in c],
      'S_j':{str(abs(z)):int(z>0) for z in c},
      'invert_S_j_U_j':{str(abs(z)):int(z<0) for z in c},
      'U_j':{str(abs(z)):int(z<0) for z in c},
      'invert_U_j_S_j':{str(abs(z)):int(z>0) for z in c}})
 return rows

def pairmodes(F):
 rows=[];assertions=0
 for j,k in it.combinations(range(len(F)),2):
  pa={abs(z):int(z>0) for z in F[j]};pb={abs(z):int(z>0) for z in F[k]};shared=pa.keys()&pb.keys()
  same=sorted(i for i in shared if pa[i]==pb[i]);opp=sorted(i for i in shared if pa[i]!=pb[i]);test={'SS':not opp,'SU':not same,'US':not same,'UU':not opp}
  scope=sorted(pa.keys()|pb.keys());got=dict.fromkeys(test,False)
  for bits in it.product((0,1),repeat=len(scope)):
   a=dict(zip(scope,bits));u=sum(littrue(z,a) for z in F[j]);v=sum(littrue(z,a) for z in F[k])
   mode=('S' if u==len(F[j]) else 'U' if u==0 else 'M')+('S' if v==len(F[k]) else 'U' if v==0 else 'M')
   if mode in got:got[mode]=True
   assertions+=1
  assert got==test,(j,k,got,test)
  rows.append({'source_pair':[j+1,k+1],'same_sign_shared':same,'opposite_sign_shared':opp,'SS_SU_US_UU':test,'forced_middle':not any(test.values())})
 return rows,assertions

def fliptrail(F):
 n=nvars(F);rows={}
 for bit in [0,1]:
  a={i:bit for i in range(1,n+1)};events=[]
  seq=[('endpoint',None)]+[(f'flip_{i}',i) for i in range(1,min(n,4)+1)]+[('invert_all',-1)]
  for label,i in seq:
   if i==-1:a={v:1-val for v,val in a.items()}
   elif i is not None:a[i]^=1
   events.append({'event':label,'assignment':''.join(str(a[i]) for i in range(1,n+1)),'per_original_clause_t':list(counts(F,a)),'N0_N1_N2_N3':N4(F,a),'source_SAT':sat(F,a)})
  rows[str(bit)+'^n']=events
 return rows

def resolvent(F):
 for j,k in it.combinations(range(len(F)),2):
  for p in F[j]:
   if -p not in F[k]:continue
   R=tuple(sorted(set(F[j]+F[k])-{p,-p},key=lambda z:(abs(z),z<0)))
   if any(-z in R for z in R):continue
   cube={abs(z):int(z<0) for z in R}
   assert all(not littrue(z,cube) for z in R)
   return {'parent_clause_indices':[j+1,k+1],'pivot':abs(p),'resolvent':R,
     'prohibited_cube':cube,'proof':'Under cube R=false, parent clauses force pivot and its negation; R follows by source resolution.'}
 return None

ZERO=(0,0,0,0)
def vecadd(a,b):return tuple(x+y for x,y in zip(a,b))
def vecsub(a,b):return tuple(x-y for x,y in zip(a,b))
class Circuit:
 def __init__(self,n):
  self.nodes=[];self.constants={};self.vars={};self.n=n
  self.z=self.const(0);self.one=self.const(1)
  for i in range(1,n+1):self.vars[i]=self.node(('var',i))
 def node(self,val):self.nodes.append(val);return len(self.nodes)-1
 def const(self,value):
  value=Fraction(value)
  if value not in self.constants:self.constants[value]=self.node(('const',value))
  return self.constants[value]
 def plus(self,a,b):
  if a==self.z:return b
  if b==self.z:return a
  return self.node(('add',a,b))
 def times(self,a,b):
  if a==self.z or b==self.z:return self.z
  if a==self.one:return b
  if b==self.one:return a
  return self.node(('mul',a,b))
 def scale(self,a,v):return self.times(a,self.const(v))

# Exact local logarithm of the multiweighted generating function.
def mulpoly(a,b,r,h):
 result=defaultdict(Fraction)
 for (pa,da),ca in a.items():
  for (pb,db),cb in b.items():
   p=tuple(x+y for x,y in zip(pa,pb))
   if sum(p)>r:continue
   result[(p,vecadd(da,db))]+=ca*cb
 return {k:v for k,v in result.items() if v}
def local_log(F,base,H,r,incident):
 H=tuple(H);tbase=counts(F,base);clauses=set(j for i in H for j in incident[i]);V={}
 for mask in range(1,1<<len(H)):
  flip={H[i] for i in range(len(H)) if mask>>i&1}
  alpha=tuple(int(i in flip) for i in H);delta=[0]*4
  for j in clauses:
   t=tbase[j]
   for z in F[j]:
    if abs(z) in flip:t+=1-2*int(littrue(z,base))
   old=tbase[j]
   if old!=t:delta[t]+=1;delta[old]-=1
  V[(alpha,tuple(delta))]=Fraction(1)
 power=V;answer=defaultdict(Fraction)
 for p in range(1,r+1):
  if p>1:power=mulpoly(power,V,r,H)
  sign=Fraction(1 if p%2 else -1,p)
  for (alpha,delta),coeff in power.items():
   if all(alpha):answer[(alpha,delta)]+=sign*coeff
 return {k:v for k,v in answer.items() if v}

def connected_supports(F,r):
 n=nvars(F);nei={i:set() for i in range(1,n+1)}
 for c in F:
  for i,j in it.combinations(map(abs,c),2):nei[i].add(j);nei[j].add(i)
 sets={frozenset((i,)) for i in range(1,n+1)};layer=sets.copy()
 for k in range(2,r+1):
  nxt=set()
  for S in layer:
   for v in S:
    for u in nei[v]-S:nxt.add(S|{u})
  sets|=nxt;layer=nxt
 return sorted((tuple(sorted(s)) for s in sets),key=lambda t:(len(t),t)), max(map(len,nei.values()))

def compiler(F,r,base=None):
 n=nvars(F);base=base or {i:0 for i in range(1,n+1)}
 assert all(len(c)==3 and len(set(map(abs,c)))==3 for c in F)
 C=Circuit(n);incident={i:[] for i in range(1,n+1)}
 for j,c in enumerate(F):
  for z in c:incident[abs(z)].append(j)
 supports,maxdegree=connected_supports(F,r)
 B=[defaultdict(lambda:C.z) for _ in range(r+1)]
 monomials={}
 for H in supports:
  local=local_log(F,base,H,r,incident)
  for (powers,delta),coefficient in local.items():
   degree=sum(powers)
   key=tuple((i,k) for i,k in zip(H,powers) if k)
   if key not in monomials:
    node=C.one
    for i,k in key:
     for _ in range(k):node=C.times(node,C.vars[i])
    monomials[key]=node
   term=C.scale(monomials[key],coefficient)
   B[degree][delta]=C.plus(B[degree][delta],term)
 E=[defaultdict(lambda:C.z) for _ in range(r+1)];E[0][ZERO]=C.one
 for k in range(1,r+1):
  for j in range(1,k+1):
   for d1,u in B[j].items():
    for d2,v in E[k-j].items():
     dest=vecadd(d1,d2)
     E[k][dest]=C.plus(E[k][dest],C.scale(C.times(u,v),Fraction(j,k)))
 nbase=N4(F,base)
 target=C.z
 for delta,node in E[r].items():
  if delta[0]+nbase[0]==0:target=C.plus(target,node)
 return C,target,{'connected_supports':len(supports),'max_degree':maxdegree,'circuit_nodes':len(C.nodes),'states_at_radius':len(E[r]),'baseline_N4':nbase,'target_nodes':sum(1 for d in E[r] if d[0]+nbase[0]==0)}

def dual_ad(C,target,T):
 """Exact mixed partial D_T(P), all D_i D_T(P) in one forward/reverse circuit sweep."""
 T=tuple(T);q=len(T);length=1<<q;index={i:j for j,i in enumerate(T)}
 vals=[];opcounts=Counter()
 for gate in C.nodes:
  tag=gate[0];arr=[Fraction(0)]*length
  if tag=='const':arr[0]=gate[1]
  elif tag=='var':
   arr[0]=Fraction(1)
   if gate[1] in index:arr[1<<index[gate[1]]]=Fraction(1)
  elif tag=='add':
   a,b=gate[1:];arr=[x+y for x,y in zip(vals[a],vals[b])];opcounts['sum']+=length
  elif tag=='mul':
   a,b=gate[1:]
   for m in range(length):
    s=m
    while True:
     arr[m]+=vals[a][s]*vals[b][m^s];opcounts['mul']+=1
     if s==0:break
     s=(s-1)&m
  vals.append(arr)
 full=length-1;conditional_count=vals[target][full]
 adj=[[Fraction(0)]*length for _ in C.nodes];adj[target][full]=Fraction(1)
 for p in range(len(C.nodes)-1,-1,-1):
  gate=C.nodes[p];tag=gate[0]
  if tag=='add':
   a,b=gate[1:]
   for m in range(length):adj[a][m]+=adj[p][m];adj[b][m]+=adj[p][m]
  if tag=='mul':
   a,b=gate[1:]
   for m in range(length):
    s=m
    while True:
     adj[a][s]+=adj[p][m]*vals[b][m^s]
     adj[b][m^s]+=adj[p][m]*vals[a][s]
     opcounts['reverse_mul']+=2
     if s==0:break
     s=(s-1)&m
 gradients={i:adj[v][0] for i,v in C.vars.items()}
 return conditional_count,gradients,dict(opcounts)

def extract(C,node,F,r,base):
 chosen=[];passes=[]
 for k in range(r):
  q,g,cost=dual_ad(C,node,chosen)
  eligible=[i for i in range(1,nvars(F)+1) if i not in chosen and g[i]>0]
  passes.append({'selected_before':chosen[:],'source_confirmed_target_extensions':str(q),
   'positive_gradient_variables':eligible,'selected_work':cost})
  if not eligible:
   assert q==0
   return None,passes
  chosen.append(eligible[0])
 a=base.copy()
 for i in chosen:a[i]^=1
 assert sat(F,a),(chosen,N4(F,a))
 assert len(chosen)==r
 return chosen,passes

def forward_count(C,target,T,excluded):
    """One original weighted-circuit conditional-feasibility replay (without reverse AD)."""
    T=tuple(T);index={i:j for j,i in enumerate(T)};size=1<<len(T)
    vals=[];events=0
    for gate in C.nodes:
        tag=gate[0];arr=[Fraction(0)]*size
        if tag=='const':arr[0]=gate[1]
        elif tag=='var':
            arr[0]=Fraction(0 if gate[1] in excluded else 1)
            if gate[1] in index:arr[1<<index[gate[1]]]=Fraction(1)
        elif tag=='add':
            a,b=gate[1:];arr=[x+y for x,y in zip(vals[a],vals[b])];events+=size
        elif tag=='mul':
            a,b=gate[1:]
            for m in range(size):
                v=m
                while True:
                    arr[m]+=vals[a][v]*vals[b][m^v];events+=1
                    if v==0:break
                    v=(v-1)&m
        vals.append(arr)
    return vals[target][-1],events

def replay_extract(C,target,F,r,base):
    """Prior style: up to n independent conditioned queries of the same compiled circuit."""
    chosen=[];excluded=set();calls=0;events=0
    for i in range(1,nvars(F)+1):
        if len(chosen)==r:break
        c,work=forward_count(C,target,chosen,excluded|{i})
        calls+=1;events+=work
        if c>0:excluded.add(i)
        else:chosen.append(i)
    if len(chosen)!=r:return None,{'calls':calls,'selected_ops':events}
    a=base.copy()
    for i in chosen:a[i]^=1
    assert sat(F,a)
    return chosen,{'calls':calls,'selected_ops':events}

def brute(F,r,base):
 n=nvars(F);freq=Counter();freq_target=Counter()
 for S in it.combinations(range(1,n+1),r):
  a=base.copy()
  for i in S:a[i]^=1
  freq[N4(F,a)]+=1
  if sat(F,a):freq_target[S]+=1
 return freq,freq_target

def dpll(F):
 n=nvars(F);stats=Counter();leaves=[]
 def recur(a):
  stats['nodes']+=1
  while True:
   change=False
   for j,c in enumerate(F,1):
    stats['source_literal_reads']+=len(c)
    if any(littrue(z,a) for z in c if abs(z) in a):continue
    u=[z for z in c if abs(z) not in a]
    if not u:stats['contradiction_leaves']+=1;leaves.append({'source_conflict_clause':j,'partial_assignment':dict(a)});return None
    if len(u)==1:
     z=u[0];a[abs(z)]=int(z>0);stats['unit_propagations']+=1;change=True;break
   if not change:break
  if len(a)==n:return a if sat(F,a) else None
  i=next(i for i in range(1,n+1) if i not in a)
  for b in (0,1):
   t=dict(a);t[i]=b
   out=recur(t)
   if out is not None:return out
  return None
 answer=recur({})
 return answer,dict(stats),leaves

def profile(fun):
 tracemalloc.start();t=time.perf_counter();res=fun();sec=time.perf_counter()-t;peak=tracemalloc.get_traced_memory()[1];tracemalloc.stop();return res,sec,peak

def full_hybrid(F,r):
    """Complete adaptive solver, charges endpoint failure, compilation, AD, and full DPLL fallback."""
    n=nvars(F);source_reads=sum(len(c) for c in F);a={i:0 for i in range(1,n+1)}
    if sat(F,a):return {'answer':'SAT','route':'all_zero','source_scans':source_reads,'DPLL_nodes':0}
    ones={i:1 for i in range(1,n+1)};source_reads+=sum(len(c) for c in F)
    if sat(F,ones):return {'answer':'SAT','route':'all_one','source_scans':source_reads,'DPLL_nodes':0}
    C,P,meta=compiler(F,r,a)
    count,_,_=dual_ad(C,P,[])
    if count>0:
        flips,_=extract(C,P,F,r,a)
        assert flips is not None
        source_reads+=sum(len(c) for c in F)
        return {'answer':'SAT','route':'derivative_radius_'+str(r),'source_scans':source_reads,
            'source_checked_flips':flips,'DPLL_nodes':0,'arithmetic_nodes':meta['circuit_nodes']}
    ans,stats,leaves=dpll(F)
    if ans is not None:
        assert sat(F,ans);source_reads+=sum(len(c) for c in F)
    return {'answer':'SAT' if ans is not None else 'UNSAT','route':'complete_DPLL_fallback',
        'DPLL_nodes':stats['nodes'],'source_scans':source_reads,
        'arithmetic_nodes':meta['circuit_nodes'],'DPLL_proof_leaves':len(leaves)}

def two_sat_scc(F,n=None):
    """Known implication-graph SCC algorithm for original clauses of length <=2."""
    if any(len(c)>2 for c in F):return {'applicable':False}
    n=n or nvars(F);g={i:set() for i in range(-n,n+1) if i};rev={i:set() for i in g}
    for c in F:
        if len(c)==0:return {'applicable':True,'SAT':False}
        pairs=((-c[0],c[0]),) if len(c)==1 else ((-c[0],c[1]),(-c[1],c[0]))
        for a,b in pairs:g[a].add(b);rev[b].add(a)
    seen=set();order=[]
    def visit(v):
        seen.add(v)
        for w in g[v]:
            if w not in seen:visit(w)
        order.append(v)
    for v in g:
        if v not in seen:visit(v)
    labels={}
    def assign(v,k):
        labels[v]=k
        for w in rev[v]:
            if w not in labels:assign(w,k)
    for v in reversed(order):
        if v not in labels:assign(v,len(set(labels.values())))
    return {'applicable':True,'SAT':all(labels[i]!=labels[-i] for i in range(1,n+1))}

def horn_forward(F):
    if any(sum(z>0 for z in c)>1 for c in F):return {'applicable':False}
    v=set()
    while True:
        more=False
        for c in F:
            negative=[-z for z in c if z<0];head=next((z for z in c if z>0),None)
            if set(negative)<=v:
                if head is None:return {'applicable':True,'SAT':False}
                if head not in v:v.add(head);more=True
        if not more:break
    return {'applicable':True,'SAT':True,'least_true_variables':sorted(v)}

def recognize_xor(F):
    """Only exact 4-clause parity-of-three source blocks, no promise of general closure."""
    groups=defaultdict(list)
    if any(len(c)!=3 for c in F):return {'applicable':False}
    for c in F:groups[tuple(sorted(map(abs,c)))].append(c)
    equations=[]
    for ids,cs in groups.items():
        if len(cs)!=4:return {'applicable':False}
        models=[]
        for bits in it.product((0,1),repeat=3):
            a=dict(zip(ids,bits))
            if all(any(littrue(z,a) for z in c) for c in cs):models.append(bits)
        if len(models)!=4:return {'applicable':False}
        parities={sum(bs)%2 for bs in models}
        if len(parities)!=1:return {'applicable':False}
        equations.append((ids,parities.pop()))
    # Gaussian elimination GF(2) with original support rows.
    pivots={}
    for ids,rhs in equations:
        row=sum(1<<(i-1) for i in ids)
        while row:
            pivot=row.bit_length()-1
            if pivot in pivots:
                prow,prhs=pivots[pivot];row^=prow;rhs^=prhs
            else:
                pivots[pivot]=(row,rhs);break
        if row==0 and rhs:return {'applicable':True,'SAT':False,'equations':[(list(i),b) for i,b in equations]}
    return {'applicable':True,'SAT':True,'equations':[(list(i),b) for i,b in equations]}

def ancillary_controls():
    cases={'2SAT_yes':((1,2),(-1,2),(1,-2)),
       '2SAT_no':((1,2),(-1,2),(1,-2),(-1,-2)),
       'Horn_yes':((1,-2,-3),(-1,2,-3),(-1,-2,3)),
       'XOR3_even':parity3(True),
       'XOR3_odd_and_even':parity3(True)+parity3(False)}
    rows=[]
    for name,F in cases.items():
        n=nvars(F);truth=sum(all(any(littrue(z,dict(zip(range(1,n+1),bs))) for z in c) for c in F) for bs in it.product((0,1),repeat=n))
        analyses={'2SAT':two_sat_scc(F),'Horn':horn_forward(F),'XOR_GF2':recognize_xor(F)}
        for v in analyses.values():
            if v['applicable']:assert v['SAT']==(truth>0),(name,v,truth)
        rows.append({'name':name,'original_signed_clauses':F,'n':n,'SAT':truth>0,'models':truth,'recognition':analyses})
    return rows

def one(name,F,r,checks=True):
 n=nvars(F);assert all(len(c)==3 and len(set(map(abs,c)))==3 for c in F)
 audit={'original_extreme_occurrences':extremes(F)}
 audit['pair_modes'],audit['independently_enumerated_pair_states']=pairmodes(F)
 audit['coherent_endpoints_and_flip_trails']=fliptrail(F)
 audit['source_parent_prohibited_cube']=resolvent(F)
 base={i:0 for i in range(1,n+1)}
 def combined():
  C,target,meta=compiler(F,r,base)
  count,grad,ops=dual_ad(C,target,[])
  selected,passes=extract(C,target,F,r,base) if count>0 else (None,[])
  return meta, C, target, count, grad, ops, selected, passes
 (meta,C,target,count,grad,ops,selected,passes),ct,peak=profile(combined)
 (dres,ds,dpeak)=profile(lambda:dpll(F))
 (hybrid,hybrid_sec,hybrid_peak)=profile(lambda:full_hybrid(F,r))
 assert hybrid['answer']==('SAT' if dres[0] is not None else 'UNSAT')
 if count>0:
  (replay_selected,replay_stats),replay_sec,replay_peak=profile(lambda:replay_extract(C,target,F,r,base))
 else:
  replay_selected=None;replay_stats={'calls':0,'selected_ops':0};replay_sec=0.;replay_peak=0
 assert (replay_selected is None)==(selected is None)
 oracle_freq,oracle_targets=brute(F,r,base)
 assert int(count)==len(oracle_targets),(name,count,len(oracle_targets))
 for i in range(1,n+1):assert int(grad[i])==sum(i in S for S in oracle_targets),(name,i,grad[i])
 assert (selected is not None)==(len(oracle_targets)>0)
 if selected:assert tuple(selected) in oracle_targets
 assert (dres[0] is not None)==bool(any(sat(F,dict(zip(range(1,n+1),bs))) for bs in it.product((0,1),repeat=n))) if checks and n<=12 else True
 return {'source_name':name,'source_CNF':[list(c) for c in F],'n':n,'m':len(F),'r':r,
  'strict22':exact22(F),'connected':connected(F),
  'audit':audit,'recognition':{'2SAT':two_sat_scc(F),'Horn':horn_forward(F),'XOR_GF2':recognize_xor(F)},'compiler':meta,'target_count':int(count),'gradient_by_original_variable':{str(i):int(v) for i,v in grad.items()},
  'selected_flips':selected,'selected_source_checked_witness':{'assignment':(''.join(str((base[i]^(i in selected))) for i in range(1,n+1)) if selected else None),'original_clause_N4':(N4(F,{i:int(i in selected) for i in range(1,n+1)}) if selected else None)},
  'derivative_passes':passes,'unconditioned_AD_ops':ops,
  'replay_selected_flips':replay_selected,'replay_stats':replay_stats,'replay_seconds':replay_sec,'replay_peak_bytes':replay_peak,
  'compiler_seconds':ct,'compiler_peak_bytes':peak,'baseline_dpll_seconds':ds,'baseline_dpll_peak_bytes':dpeak,
  'baseline_dpll':dres[1],'baseline_witness':dres[0],
  'complete_hybrid':hybrid,'complete_hybrid_seconds':hybrid_sec,'complete_hybrid_peak_bytes':hybrid_peak,
  'oracle_radius_masks_checked':math.comb(n,r),'oracle_target_count':len(oracle_targets),
  'oracle_target_flip_masks':list(map(list,oracle_targets))[:15],
  'radius_hist_distinct_vectors':len(oracle_freq),
  'radius_hist_counts':{'/'.join(map(str,k)):v for k,v in oracle_freq.items()}}

def main():
 F1=plateau(1);F2=plateau(2)
 rng=random.Random(248)
 # proper, width-three dense hostile source, not exact22
 dense=tuple(tuple((i if rng.randrange(2) else -i) for i in rng.sample(range(1,7),3)) for _ in range(14))
 cases=[('H1_strict22_SAT',F1,2),('H1_strict22_SAT_r3',F1,3),
        ('H2_strict22_SAT',F2,2),('H2_strict22_SAT_r3',F2,3),('W1_strict22_UNSAT',parse(W1),2),('W1_strict22_UNSAT_r3',parse(W1),3),
        ('S15_strict22_SAT',parse(S15),2),
        ('S15_phase_endpoint_fail_SAT',phase_invert(parse(S15),'110011101010111'),2),('S15_strict22_SAT_r3',parse(S15),3),
        ('H2_signed_relabel',adversarial_relabel(F2),3),('K4_strict22_SAT',paired_k4(),2),
        ('XOR3_even_SAT',parity3(True),2),('XOR3_contradiction_UNSAT',parity3(True)+parity3(False),2),
        ('Horn_SAT',((1,-2,-3),(-1,2,-3),(-1,-2,3)),2),('dense_random',dense,2)]
 rows=[]
 for name,F,r in cases:
  t=time.perf_counter();out=one(name,F,r)
  print(name,'n',out['n'],'r',r,'target',out['target_count'],'nodes',out['compiler']['circuit_nodes'],'s',round(out['compiler_seconds'],4),'wall',round(time.perf_counter()-t,3),flush=True)
  rows.append(out)
 data={'run':'LSPV-2_DERIVATIVE_WITNESS248','seed':248,'math_status':'PROVED/EXACT restricted, independent referee pending','ancillary_controls':ancillary_controls(),'cases':rows}
 path=sys.argv[1] if len(sys.argv)>1 else 'DERIVATIVE_WITNESS248_raw.json'
 with open(path,'w') as f:json.dump(data,f,indent=2)
 print('PASS',len(rows),'cases','source-clauses',sum(z['m'] for z in rows),'source-pairs',sum(len(z['audit']['pair_modes']) for z in rows),'SHA256',hashlib.sha256(open(path,'rb').read()).hexdigest())
if __name__=='__main__':main()