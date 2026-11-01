#!/usr/bin/env python3
"""LSPV-2 OVERLAP-FRONTIER296 (builds on COMPONENT-SYNDROME295): authenticated saturated-cycle templates,
fixed GF(2) projected coefficient matrix, one-time rank, prefix refutations,
and exact #SAT. Research tool, not an ARC or complexity separation proof.
Independent verifier is verify294.py (does not import this module).
"""
from __future__ import annotations
import math
from collections import Counter, defaultdict
from itertools import product, combinations
import ast, hashlib, json, pathlib
P=pathlib.Path(__file__).resolve().parent

POS9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
NEG9=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
F9=tuple(POS9)+tuple(tuple(-v for v in c) for c in NEG9)
P9={8:0,3:0,7:0,6:0,1:1,5:1}
POS6=((1,2,3),(1,4,5),(2,4,6),(3,5,6))
NEG6=((1,2,4),(1,3,6),(2,3,5),(4,5,6))
Y6=tuple(POS6)+tuple(tuple(-v for v in c) for c in NEG6)
POS15=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15))
NEG15=((1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),(4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15))
F15=tuple(POS15)+tuple(tuple(-v for v in c) for c in NEG15)
P15_U=dict(zip(range(7,16),(0,0,0,0,1,1,1,1,0)))
P15_S=dict(zip(range(7,16),(1,0,0,0,1,1,1,1,0)))
P5=((1,2),(2,3),(3,4),(4,5),(1,5))
Q5=tuple(e for e in combinations(range(1,6),2) if e not in P5)
F15K5=tuple((u,v,6+i) for i,(u,v) in enumerate(P5))+tuple((-u,-v,-11-i) for i,(u,v) in enumerate(Q5))+tuple((6+i,11+i,11+(i+1)%5) for i in range(5))+tuple((-(11+i),-(6+i),-(6+(i+1)%5)) for i in range(5))
P5_U={**{v:0 for v in range(6,11)},**{v:1 for v in range(11,16)}}
P5_S={**P5_U,6:1,15:0}

def source198():
 raw=''.join(s for s in (P/'U198.txt').read_text().splitlines() if not s.startswith('#'))
 u=tuple(tuple(c) for c in ast.literal_eval(raw))
 v=[list(c) for c in u]
 v[2][-1],v[44][-1]=v[44][-1],v[2][-1]
 return u,tuple(map(tuple,v))

def valid(F):
 if not F:return False
 try:n=max(abs(x) for c in F for x in c)
 except (TypeError,ValueError):return False
 if n<1 or len(F)*3!=4*n or n%3:return False
 degree=Counter(x for c in F for x in c)
 return (len({tuple(sorted(c)) for c in F})==len(F)
         and all(len(c)==3 and len({abs(x) for x in c})==3 and
                 (all(x>0 for x in c) or all(x<0 for x in c)) for c in F)
         and all(degree[x]==degree[-x]==2 for x in range(1,n+1)))

def satisfies(F,a):
 return all(any(a[abs(x)]==int(x>0) for x in c) for c in F)

def truths(F,a):
 return [sum(a[abs(x)]==int(x>0) for x in c) for c in F]

def source_gate(F,p):
 assert valid(F)
 n=max(abs(x) for c in F for x in c)
 assert all(1<=x<=n and v in (0,1) for x,v in p.items())
 free=[v for v in range(1,n+1) if v not in p]
 uncovered=[];covered=[];binary=[];pref=Counter();reads=0
 for j,c in enumerate(F):
  reads+=3
  if any(abs(x) in p and p[abs(x)]==int(x>0) for x in c):
   covered.append(j)
   for x in c:
    if abs(x) not in p:pref[abs(x),x>0]+=1
  else:
   r=[x for x in c if abs(x) not in p]
   if not r:return {'status':'EMPTY','source_clause':j,'source_literal_reads':reads}
   uncovered.append(j)
   if len(r)==2:binary.append((j,abs(r[0]),abs(r[1]),int(r[0]>0)))
 eta=sum(min(pref[v,True],pref[v,False]) for v in free)
 preferred={v: int(pref[v,False]>pref[v,True]) for v in free if pref[v,True]!=pref[v,False]}
 # Source ID multigraph, independently indexed. Only 3-edge simple triangles.
 pair=defaultdict(list);adj=defaultdict(set)
 for j,u,v,s in binary:
  pair[min(u,v),max(u,v)].append((j,s))
  adj[u].add(v);adj[v].add(u)
 triangles=[];candidate=0
 for u in sorted(adj):
  for v in sorted(q for q in adj[u] if q>u):
   for w in sorted(q for q in adj[u]&adj[v] if q>v):
    candidate+=1
    for e1,e2,e3 in product(pair[u,v],pair[u,w],pair[v,w]):
     triangles.append(tuple(sorted((e1[0],e2[0],e3[0]))))
 # Deterministic polynomial greedy edge-disjoint certificate.
 cycles=[];used=set()
 for c in sorted(set(triangles)):
  if not any(j in used for j in c):cycles.append(c);used.update(c)
 e=2*len(free)-len(uncovered)
 return {'status':'GATE','n':n,'free':free,'uncovered':uncovered,'covered':covered,
         'eta':eta,'e':e,'delta':e-eta-len(cycles),'nu':len(cycles),
         'preferred':preferred,'cycles':cycles,'binary_edges':binary,
         'source_literal_reads':reads,'triangle_candidate_checks':candidate,
         'triangle_choices_checked':len(triangles)}

def cycle_templates(F,cycle,p):
 # Returns one uniquely determined complete assignment to all cycle vertices
 # per chosen source-clause edge. Includes an original-clause proof descriptor.
 triples=[]
 for j in cycle:
  rem=[x for x in F[j] if abs(x) not in p]
  assert len(rem)==2 and (rem[0]>0)==(rem[1]>0)
  triples.append((j,abs(rem[0]),abs(rem[1]),int(rem[0]>0)))
 templates=[]
 for chosen,u,v,s in triples:
  asg={u:s,v:s}; todo=True
  while todo:
   todo=False
   for j,x,y,sign in triples:
    if j==chosen:continue
    if x in asg and y not in asg:asg[y]=1-asg[x];todo=True
    if y in asg and x not in asg:asg[x]=1-asg[y];todo=True
  if len(asg)!=len({z for _,x,y,_ in triples for z in (x,y)}):
   raise AssertionError('not a simple connected odd cycle')
  for j,x,y,sign in triples:
   assert (asg[x]==asg[y]==sign) if j==chosen else (asg[x]!=asg[y])
  templates.append({'chosen_clause':chosen,'assignments':asg,'source_cycle_ids':tuple(cycle)})
 return templates

def parity(x):return x.bit_count()&1

class Projector:
 def __init__(self,F,g,p):
  self.F,self.g,self.p=F,g,p
  self.vertexset=set()
  self.templates=[]
  for cycle in g['cycles']:
   tt=cycle_templates(F,cycle,p)
   self.templates.append(tt)
   for item in tt:self.vertexset.update(item['assignments'])
  self.Cmask=sum(1<<(v-1) for v in self.vertexset)
  self.W=tuple(x for x in g['free'] if x not in self.vertexset)
  self.Wmask=sum(1<<(v-1) for v in self.W)
  cycle_clauses={j for cc in g['cycles'] for j in cc}
  self.rows=[]
  for j in g['uncovered']:
   if j in cycle_clauses:continue
   rem=[lit for lit in F[j] if abs(lit) not in p]
   mask=sum(1<<(abs(x)-1) for x in rem)
   rhs=1 if rem[0]>0 else 1^(len(rem)&1)
   self.rows.append((mask,rhs,('source_parity',j)))
  for v,b in g['preferred'].items():
   self.rows.append((1<<(v-1),b,('source_spill_preference',v)))
  # Row echelon basis in W only, with actual XOR combinations of input rows.
  self.basis={};self.null=[];self.row_xors=0
  for i,(mask,rhs,src) in enumerate(self.rows):
   m=mask&self.Wmask;comb=1<<i
   while m:
    pivot=m.bit_length()-1
    if pivot not in self.basis:
     self.basis[pivot]=(m,comb)
     break
    x,y=self.basis[pivot]
    m^=x;comb^=y;self.row_xors+=1
   if not m:self.null.append(comb)
  self.rank=len(self.basis)
  self.nullity=len(self.W)-self.rank
  # The row combinations defining the zero-left-side constraints on C.
  self.null_constraints=[]
  for comb in self.null:
   mask=0;rhs=0
   for i,(m,b,_) in enumerate(self.rows):
    if comb>>i&1:mask^=m&self.Cmask;rhs^=b
   self.null_constraints.append((mask,rhs,comb))
  self.metrics=Counter(precomp_rows=len(self.rows),precomp_row_xors=self.row_xors,
                       template_options=sum(len(x) for x in self.templates),
                       gaussian_factorizations=1)

 def solution(self,cmask):
  rhs_values=0
  for i,(mask,b,_) in enumerate(self.rows):
   self.metrics['row_rhs_substitutions']+=1
   z=b^parity(mask&cmask&self.Cmask)
   rhs_values|=z<<i
  y=0
  for pivot in sorted(self.basis):
   mask,comb=self.basis[pivot]
   rhs=parity(comb&rhs_values)
   val=rhs^parity(mask&y)
   y|=val<<pivot
  return y

 def evaluate(self,exhaustive=True):
  # DFS with early authenticated row-XOR and overlapping-cycle contradictions.
  compatible=[];count=0;witness=None
  self.metrics['cycles']=len(self.templates)
  def visit(k,assigned,ones,picks):
   nonlocal count,witness
   self.metrics['prefix_nodes']+=1
   # Null-row dependencies are entirely on cycle variables. Once their
   # supports have been assigned, inconsistency refutes the whole prefix.
   for mask,rhs,comb in self.null_constraints:
    self.metrics['prefix_null_tests']+=1
    if mask&~assigned==0 and parity(mask&ones)!=rhs:
     self.metrics['prefix_row_refutations']+=1
     if len(compatible)<8:compatible.append({'bad_prefix':picks,'row_combination':[self.rows[i][2] for i in range(len(self.rows)) if comb>>i&1]})
     return
   if k==len(self.templates):
    self.metrics['complete_branches']+=1
    y=self.solution(ones)
    a={**self.p,**{v:int(ones>>(v-1)&1) for v in self.vertexset},**{v:int(y>>(v-1)&1) for v in self.W}}
    assert satisfies(self.F,a),('unsound SAT',a,picks)
    self.metrics['original_clause_witness_checks']+=len(self.F)
    count+=1<<self.nullity
    self.metrics['consistent_branches']+=1
    if witness is None:witness=a
    return
   for t in self.templates[k]:
    self.metrics['choice_attempts']+=1
    bits=sum(1<<(v-1) for v in t['assignments'])
    newones=sum((1<<(v-1)) for v,vv in t['assignments'].items() if vv)
    if (ones&bits)!=(newones&assigned&bits):
     self.metrics['overlap_refutations']+=1
     continue
    aa=assigned|bits;zz=ones|newones
    visit(k+1,aa,zz,picks+(t['chosen_clause'],))
  visit(0,0,0,())
  return {'status':'SAT' if count else 'UNSAT_AFFINE_EXHAUSTED',
          'model_count':count,'rank_outside':self.rank,'nullity_outside':self.nullity,
          'witness':([witness[v] for v in range(1,self.g['n']+1)] if witness else None),
          'refutation_samples':compatible,'metrics':dict(self.metrics)}

def terminal(F,p):
 if not valid(F):return {'status':'MALFORMED'}
 if any(type(v)!=int or v not in (0,1) for v in p.values()):return {'status':'MALFORMED_PIN'}
 g=source_gate(F,p)
 if g['status']=='EMPTY':return {'status':'UNSAT_EMPTY','gate':g}
 if g['delta']<0:return {'status':'UNSAT_GAP','gate':g}
 if g['delta']!=0:return {'status':'UNRESOLVED','gate':g}
 proj=Projector(F,g,p)
 out=proj.evaluate()
 out['gate']={k:v for k,v in g.items() if k not in ('covered','uncovered','binary_edges')}
 return out

def brute_models(F,p):
 n=max(abs(x) for c in F for x in c)
 free=[v for v in range(1,n+1) if v not in p]
 for bits in product((0,1),repeat=len(free)):
  a=dict(p);a.update(zip(free,bits))
  if satisfies(F,a):yield a

def baseline(F,p,cap=3000):
 work=Counter()
 class Cap(Exception):pass
 def solve(q):
  work['dpll_nodes']+=1
  if work['dpll_nodes']>cap:raise Cap()
  q=q.copy()
  while True:
   allhit=True;forced=None
   for c in F:
    work['clause_scans']+=1
    unknown=[];hit=False
    for lit in c:
     work['literal_tests']+=1
     if abs(lit) not in q:unknown.append(lit)
     elif q[abs(lit)]==int(lit>0):hit=True;break
    if hit:continue
    allhit=False
    if not unknown:return False
    if len(unknown)==1:forced=unknown[0];break
   if forced is None:
    if allhit:return True
    break
   v=abs(forced);b=int(forced>0)
   if v in q and q[v]!=b:return False
   q[v]=b;work['unit_forces']+=1
  v=next(v for v in range(1,max(abs(l) for c in F for l in c)+1) if v not in q)
  for b in (0,1):
   work['branch_edges']+=1
   if solve({**q,v:b}):return True
  return False
 try:val=solve(p)
 except Cap:val=None
 return {'status':'UNKNOWN_CAP' if val is None else ('SAT' if val else 'UNSAT'),**dict(work)}



# NEW: exact overlap-aware cycle-frontier syndrome DP.  This section replaces
# the predecessor's exhaustive overlap-component enumeration.

def projected_echelon(P):
    """Rank-independent GF(2) rows on cycle vertices, carrying original-row
    XOR combinations, not a CNF resolution certificate by themselves.
    """
    basis={}; xors=0
    for mask,rhs,prov in P.null_constraints:
        while mask:
            k=mask.bit_length()-1
            if k not in basis:
                basis[k]=(mask,rhs,prov)
                break
            m,b,p=basis[k]
            mask^=m;rhs^=b;prov^=p;xors+=1
        if not mask and rhs:
            return None,{'contradiction_rows':[
                P.rows[i][2] for i in range(len(P.rows)) if (prov>>i)&1],
                'row_xors':xors}
    return [basis[k] for k in sorted(basis,reverse=True)],{'row_xors':xors}


def frontier_terminal(F,p,cap=100_000,keep_trace=False):
    """Sound, complete on signed-spill delta=0 states; UNRESOLVED otherwise.

    DP state (syndrome, live-overlap assignment) is *exact* across cycle
    prefixes.  Every original cycle vertex is charged to its first cycle,
    hence projected parity is counted exactly once even when cycles overlap.
    """
    met=Counter(policy_calls=1,source_literal_reads=0,failed_policy_trials=0)
    if not valid(F):return {'status':'MALFORMED','metrics':dict(met)}
    n=max(abs(x) for c in F for x in c)
    if not isinstance(p,dict) or any(type(k)!=int or not 1<=k<=n or type(v)!=int or v not in (0,1) for k,v in p.items()):
        return {'status':'MALFORMED_PIN','metrics':dict(met)}
    met['grammar_source_literal_reads']=3*len(F)
    g=source_gate(F,p)
    met['source_literal_reads']+=g['source_literal_reads']
    met['triangle_candidate_checks']+=g.get('triangle_candidate_checks',0)
    met['triangle_choices_checked']+=g.get('triangle_choices_checked',0)
    if g['status']=='EMPTY':return {'status':'UNSAT_EMPTY','source_clause':g['source_clause'],'metrics':dict(met)}
    met.update(delta=g['delta'],nu=g['nu'],free=len(g['free']),uncovered=len(g['uncovered']),eta=g['eta'])
    if g['delta']<0:return {'status':'UNSAT_GAP','metrics':dict(met)}
    if g['delta']!=0:
        met['failed_policy_trials']+=1
        return {'status':'UNRESOLVED','metrics':dict(met)}
    Pj=Projector(F,g,p)
    equations,info=projected_echelon(Pj)
    met.update(precomp_rows=len(Pj.rows),precomp_row_xors=Pj.row_xors if hasattr(Pj,'row_xors') else Pj.metrics['precomp_row_xors'],
               projected_row_xors=info['row_xors'],rank_W=Pj.rank,nullity_W=Pj.nullity,
               dense_matrix_bits_upper=(len(Pj.rows)+len(g['free'])+1)*(len(g['free'])+2),
               cycles=len(g['cycles']))
    if equations is None:return {'status':'UNSAT_PROJECTION','metrics':dict(met),'refutation':info}
    q=len(equations)
    met['projected_rank']=q
    templates=Pj.templates
    k=len(templates)
    vertices=[set(tt[0]['assignments']) for tt in templates]
    # Pay for component discovery.  A row couples every cycle containing
    # any of its variables, and a shared vertex couples its incident cycles.
    parent=list(range(k))
    def root(i):
        while parent[i]!=i:
            parent[i]=parent[parent[i]];i=parent[i]
        return i
    def join(i,j):
        a,b=root(i),root(j)
        if a!=b:parent[max(a,b)]=min(a,b)
    var_to_cycles=defaultdict(list)
    for i,vs in enumerate(vertices):
        for v in vs:var_to_cycles[v].append(i)
    for vv in var_to_cycles.values():
        for z in vv[1:]:join(vv[0],z);met['component_shared_variable_links']+=1
    row_support=[]
    for mask,_,_ in equations:
        supporting=set()
        for v in var_to_cycles:
            met['projection_row_support_checks']+=1
            if mask>>(v-1)&1:supporting.update(var_to_cycles[v])
        row_support.append(supporting)
        if len(supporting)>1:
            first=min(supporting)
            for z in supporting:join(first,z);met['component_row_links']+=1
    groups=defaultdict(list)
    for i in range(k):groups[root(i)].append(i)
    components=sorted(groups.values(),key=lambda c:c[0])
    met['component_count']=len(components)
    B=1;all_picks={};traces=[];peak=1
    for gidx,group in enumerate(components):
        sub_rows=[z for z,owners in enumerate(row_support) if owners and root(min(owners))==root(group[0])]
        for z,owners in enumerate(row_support):
            if not owners and equations[z][1]:
                return {'status':'UNSAT_PROJECTION','metrics':dict(met),
                        'refutation':{'type':'constant_projected_equation','index':z}}
        target_i=sum(equations[z][1]<<j for j,z in enumerate(sub_rows))
        group_vertices=[vertices[i] for i in group]
        owners={v:i for i,vs in enumerate(group_vertices) for v in vs if v not in {a for kk in range(i) for a in group_vertices[kk]}}
        future=[set() for _ in range(len(group)+1)]
        for i in range(len(group)-1,-1,-1):future[i]=future[i+1]|group_vertices[i]
        seen=set();frontier_before=set()
        dp={(0,0):(1,())};group_max=1;last_state_counts={}
        for local,ci in enumerate(group):
            tt=templates[ci];vs=group_vertices[local]
            owner_mask=sum(1<<(v-1) for v in vs if owners[v]==local)
            after_frontier=(seen|vs)&future[local+1]
            before_mask=sum(1<<(v-1) for v in frontier_before)
            after_mask=sum(1<<(v-1) for v in after_frontier)
            new=defaultdict(lambda:[0,None]);options=[]
            for op in tt:
                option_mask=sum(1<<(v-1) for v in op['assignments'])
                onebits=sum(1<<(v-1) for v,b in op['assignments'].items() if b)
                owner_onebits=onebits&owner_mask
                sig=sum(parity(equations[z][0]&owner_onebits)<<j for j,z in enumerate(sub_rows))
                options.append((op['chosen_clause'],option_mask,onebits,sig))
                met['option_syndrome_row_checks']+=len(sub_rows)
            for (old_sig,old_ones),(count,path) in dp.items():
                for clause_id,option_mask,onebits,sig in options:
                    met['dp_transitions_attempted']+=1
                    overlap=option_mask&before_mask
                    met['overlap_bit_tests']+=overlap.bit_count()
                    if (old_ones&overlap)!=(onebits&overlap):
                        met['overlap_rejections']+=1
                        continue
                    pair=(old_sig^sig,(old_ones|onebits)&after_mask)
                    new[pair][0]+=count
                    if new[pair][1] is None:new[pair][1]=path+(clause_id,)
                    if met['dp_transitions_attempted']>cap:
                        met['failed_policy_trials']+=1
                        return {'status':'UNRESOLVED_CAP','metrics':dict(met),'cap':cap}
            dp={key:(count,path) for key,(count,path) in new.items()}
            met['dp_state_insertions']+=len(dp)
            group_max=max(group_max,len(dp))
            met['dp_peak_retained_path_slots']=max(met['dp_peak_retained_path_slots'],(local+1)*len(dp))
            if keep_trace:traces.append({'component':gidx,'cycle_index':ci,'original_clause_cycle':g['cycles'][ci],
                  'frontier_before':sorted(frontier_before),'frontier_after':sorted(after_frontier),
                  'state_count':len(dp),'transition_work':met['dp_transitions_attempted'],
                  'syndrome_state_counts':{str(s):sum(ct for (sig,_),(ct,_) in dp.items() if sig==s)
                      for s in sorted({sig for sig,_ in dp})}})
            seen|=vs;frontier_before=after_frontier
        assert not frontier_before
        hit=dp.get((target_i,0))
        bi=0 if hit is None else hit[0]
        met['dp_peak_states']=max(met['dp_peak_states'],group_max)
        peak=max(peak,group_max)
        if bi:
            for ci,ch in zip(group,hit[1]):all_picks[ci]=ch
        B*=bi
        if not bi:met['zero_component_certificates']+=1
    met['accepted_choice_vectors']=B
    met['choice_count_upper']=math.prod(len(cc) for cc in g['cycles'])
    met['count_bit_length_upper']=len(g['free'])+1+sum(len(cc).bit_length() for cc in g['cycles'])
    met['output_decision_bits']=1
    out={'status':'SAT' if B else 'UNSAT_FRONTIER_EXHAUSTED',
         'model_count':B*(1<<Pj.nullity),'compatible_cycle_choices':B,
         'nullity_W':Pj.nullity,'metrics':dict(met),'trace':traces if keep_trace else None,
         'projection_rows':[{'mask':mask,'rhs':rhs,'original_row_xor':[
             str(Pj.rows[j][2]) for j in range(len(Pj.rows)) if (prov>>j)&1]}
             for mask,rhs,prov in equations]}
    if B:
        picks=tuple(all_picks[i] for i in range(k));ones=0;assigned={}
        for i,chosen in enumerate(picks):
            option=next(z for z in templates[i] if z['chosen_clause']==chosen)
            for v,b in option['assignments'].items():
                assert v not in assigned or assigned[v]==b
                assigned[v]=b
                if b:ones|=1<<(v-1)
        assert all(parity(mask&ones)==rhs for mask,rhs,_ in equations)
        Wbits=Pj.solution(ones)
        witness={**p,**assigned,**{v:Wbits>>(v-1)&1 for v in Pj.W}}
        assert len(witness)==n and satisfies(F,witness)
        met['source_witness_checks']=len(F)
        met['witness_reconstruction_writes']=len(g['free'])
        met['row_rhs_substitutions']=Pj.metrics['row_rhs_substitutions']
        out['metrics']=dict(met)
        out['selected_edges']=picks
        out['witness']=[witness[i] for i in range(1,n+1)]
    else:
        out['certified_no_accepting_dp_state']=True
        out['witness']=None
    return out


def gamma(k):
    assert k>0
    s=bin(k)[2:]
    return '0'*(len(s)-1)+s


def encode(F):
    assert valid(F)
    n=max(abs(x) for c in F for x in c);m=len(F);w=n.bit_length()
    return gamma(n)+gamma(m)+''.join(('0' if c[0]>0 else '1')+''.join(format(abs(x),f'0{w}b') for x in c) for c in F)


def decode(encoded):
    if not isinstance(encoded,str) or not encoded or set(encoded)-set('01'):return None
    pos=0
    def read_gamma():
        nonlocal pos
        q=0
        while pos<len(encoded) and encoded[pos]=='0':q+=1;pos+=1
        if pos>=len(encoded) or pos+q+1>len(encoded):raise ValueError('gamma')
        k=int(encoded[pos:pos+q+1],2);pos+=q+1
        return k
    try:
        n=read_gamma();m=read_gamma()
        if n<1 or m<1 or 3*m!=4*n:return None
        w=n.bit_length();r=1+3*w
        if len(encoded)-pos!=m*r:return None
        F=[]
        for j in range(m):
            bit=encoded[pos];pos+=1
            c=tuple((1 if bit=='0' else -1)*int(encoded[pos+i*w:pos+(i+1)*w],2) for i in range(3))
            pos+=3*w
            F.append(c)
        return tuple(F) if valid(tuple(F)) else None
    except (ValueError,AssertionError):return None


def physical_emission_event_trace(source_bits,child_bits,filepath=None):
    """Declared fixed-layout *emission-phase* Python simulator: binary source
    read-address register, output-cursor register, output tape initially zero.
    All cell overwrites and physical XOR are emitted, but original machine
    syntax validation, solver matrix, and native FLMV jumps are NOT simulated.
    Source remains read-only. No head-movement lower bound inferred.
    """
    import gzip
    width=max(1,(max(len(source_bits),len(child_bits))+1).bit_length())
    reg={'source_address':[0]*width,'output_cursor':[0]*width,
         'output':[0]*len(child_bits)}
    stats=Counter();stream=[];steps=0
    def setbits(tape,target):
        nonlocal steps
        for i in range(width):
            val=(target>>i)&1;old=reg[tape][i]
            reg[tape][i]=val;steps+=1
            stats['register_write_events']+=1
            if old!=val:stats['physical_xor_sum']+=1
            if filepath is not None:stream.append({'step':steps,'tape':tape,'cell':i,'before':old,'after':val,'d_phys':int(old!=val)})
    # Source-indexed sequential validation scan; each source bit is read once.
    for j,bit in enumerate(source_bits):
        setbits('source_address',j)
        stats['source_bit_reads']+=1;stats['source_read_bits_one']+=int(bit=='1')
        steps+=1
        if filepath is not None:stream.append({'step':steps,'kind':'read_only_source','source_index':j,'d_phys':0})
    for j,bit in enumerate(child_bits):
        setbits('output_cursor',j)
        old=reg['output'][j];b=int(bit)
        reg['output'][j]=b;steps+=1
        stats['output_writes']+=1
        if old!=b:stats['physical_xor_sum']+=1
        if filepath is not None:stream.append({'step':steps,'tape':'output','cell':j,'before':old,'after':b,'d_phys':int(old!=b)})
    endpoint=sum(sum(c) for c in reg.values())
    stats['endpoint_physical_xor']=endpoint;stats['total_events']=steps
    stats['tape_cells']=len(child_bits)+2*width
    stats['reported_writable_peak_bits_lower']=len(child_bits)+2*width
    assert stats['physical_xor_sum']>=stats['endpoint_physical_xor']
    if filepath is not None:
        with gzip.open(filepath,'wt',encoding='utf-8') as z:
            for item in stream:z.write(json.dumps(item,sort_keys=True)+'\n')
    return dict(stats)


def example_run():
    U,V=source198()
    cases=[('F9_BAD_CUBE',F9,P9),('Y6_ROOT',Y6,{}),('F15_PIN_U',F15,P15_U),
           ('F15_PIN_S',F15,P15_S),('K5_PIN_U',F15K5,P5_U),
           ('K5_PIN_S',F15K5,P5_S),('U198_ROOT',U,{}),('V198_ROOT',V,{})]
    result={'result':'OVERLAP_FRONTIER_SYNDROME296','model':'source-authenticated source M22; word-operation proxy not native FLMV','P_vs_NP':'OPEN',
            'theorem':'exact overlap-aware frontier DP, conditioned on signed-spill saturation','cases':{},'exhaustive':{},'controls':{},'source_hashes':{},'falsifiers':{}}
    for name,F,p in cases:
        R=frontier_terminal(F,p,keep_trace=True)
        B=baseline(F,p,cap=1500)
        oracle=sum(1 for _ in brute_models(F,p)) if len(F)<32 else None
        if oracle is not None:
            if R['status']=='SAT':assert R['model_count']==oracle
            elif R['status'].startswith('UNSAT'):assert oracle==0
        result['cases'][name]={'terminal_status':R['status'],'models':R.get('model_count'),
          'oracle':oracle,'gate_delta':R['metrics'].get('delta'),'nu':R['metrics'].get('nu'),
          'projection_rank':R['metrics'].get('projected_rank'),
          'frontier_max':max([len(fr['frontier_after']) for fr in R.get('trace',[])],default=0),
          'metrics':R['metrics'],'states':R.get('trace',[]),
          'baseline':B,'witness':R.get('witness'),
          'saturated_refutation':R.get('certified_no_accepting_dp_state',False)}
        result['source_hashes'][name]=hashlib.sha256(encode(F).encode()).hexdigest()
    # Original source cube oracle from Y6 all 3^6, F15 both 3^6 windows.
    for name,F,roots in [('Y6',Y6,[{}]),('F15',F15,[P15_U,P15_S])]:
        counters=Counter()
        for root in roots:
            free=[v for v in range(1,max(abs(x) for c in F for x in c)+1) if v not in root]
            for states in product((-1,0,1),repeat=len(free)):
                pins={**root,**{v:states[i] for i,v in enumerate(free) if states[i]!=-1}}
                C=frontier_terminal(F,pins)
                actual=sum(1 for _ in brute_models(F,pins))
                if C['status']=='SAT':assert C['model_count']==actual
                elif C['status'].startswith('UNSAT'):assert actual==0
                else:counters['unresolved']+=1
                counters[C['status']]+=1
                counters['cubes']+=1
                if C['metrics'].get('delta')==0:counters['saturated']+=1
                counters['dp_transitions']+=C['metrics'].get('dp_transitions_attempted',0)
                counters['overlap_rejections']+=C['metrics'].get('overlap_rejections',0)
        result['exhaustive'][name]=dict(counters)
    for copies in (1,2,4,8,16,32):
        F=tuple(tuple((1 if x>0 else -1)*(abs(x)+15*j) for x in c) for j in range(copies) for c in F15)
        pin={v+15*j:b for j in range(copies) for v,b in P15_S.items()}
        R=frontier_terminal(F,pin,cap=1_000_000)
        assert R['status']=='SAT' and R['model_count']==(2**copies)
        result['controls']['product'+str(copies)]={'n':15*copies,'delta':R['metrics']['delta'],
             'nu':R['metrics']['nu'],'models':R['model_count'],'states_peak':R['metrics']['dp_peak_states'],
             'transition_work':R['metrics']['dp_transitions_attempted'],
             'nominal_choices':R['metrics']['choice_count_upper'],
             'input_bits':len(encode(F)),'terminal_child_bits':len(encode(Y6)),
             'terminal_child_power_short':len(encode(Y6))**2<=len(encode(F))}
    # Direct substitution and grammar tests.
    for name,F,p in [('F9',F9,P9),('F15',F15,P15_S),('K5',F15K5,P5_S)]:
        rr=frontier_terminal(F,p)
        perm={i:max(abs(x) for c in F for x in c)+1-i for i in range(1,max(abs(x) for c in F for x in c)+1)}
        rf=tuple(tuple((1 if x>0 else -1)*perm[abs(x)] for x in c) for c in F)
        rp={perm[i]:v for i,v in p.items()}
        zz=frontier_terminal(rf,rp)
        ff=tuple(tuple(-x for x in c) for c in F)
        pc={i:1-v for i,v in p.items()}
        cc=frontier_terminal(ff,pc)
        assert rr['status']==zz['status']==cc['status'] and rr.get('model_count')==zz.get('model_count')==cc.get('model_count')
    malformed=['','0','101','000101','1110','011011100','abc','111111',encode(Y6)+'1']
    assert all(decode(s) is None for s in malformed)
    assert all(decode(encode(F))==F for _,F,_ in cases)
    result['falsifiers']['F9_parity_only']='F9 delta0 exterior parity consistent but cycle-choice frontier has no accepting syndrome'
    result['falsifiers']['overlap_K5']='At least one conflicting overlap template, and exact result matches original-source enumeration'
    result['falsifiers']['fixed_q_small_b']='With q+b O(log N), source-certified DP is polynomial; not all valid instances satisfy this'
    result['falsifiers']['canonical_NO_roundtrip']='U198 is fixed canonical NO. Requires a certified UNSAT decision before emission, so no free compression.'
    # Emission tape traces for a same-canonical-language semantic child: only
    # pin-residual query equivalence, not global F equivalence when p!=empty.
    for name,F,p,expected_child in [('F15_PIN_S',F15,P15_S,Y6),('F9_BAD_CUBE',F9,P9,U),
                                    ('K5_PIN_S',F15K5,P5_S,Y6),('Y6_ROOT',Y6,{},None)]:
        r=result['cases'][name]
        if expected_child is None:continue
        child_bits=encode(expected_child);parent_bits=encode(F)
        trace_path=P/(name+'_canonical_emit_events296.jsonl.gz')
        phys=physical_emission_event_trace(parent_bits,child_bits,trace_path)
        r['child']={'valid_target':bool(valid(expected_child)),'child_bits':len(child_bits),
             'parent_bits':len(parent_bits),'power_short':len(child_bits)**2<=len(parent_bits),
             'scope':'original pinned residual query, not whole parent formula','physical':phys,
             'trace_file':trace_path.name}
    (P/'results296.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'cases':{n:{k:v[k] for k in ('terminal_status','models','gate_delta','nu','frontier_max')} for n,v in result['cases'].items()},
                      'exhaustive':result['exhaustive'],'products':result['controls']},indent=2))

if __name__=='__main__':example_run()