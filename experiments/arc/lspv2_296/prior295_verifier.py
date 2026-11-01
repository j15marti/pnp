#!/usr/bin/env python3
"""LSPV-2 COMPONENT-SYNDROME295: authenticated saturated-cycle templates,
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


# The component-syndrome terminal below builds on the fully specified,
# source-authenticated CYCLE-FIXED-MATRIX294 code above. DP cost is charged.

def projected_echelon(projector):
    """Independent parity constraints on the cycle vertices with source
    provenance. A zero-mask 1 RHS is an authenticated linear contradiction.
    """
    basis={};steps=0
    for mask,rhs,prov in projector.null_constraints:
        mask=int(mask);rhs=int(rhs);prov=int(prov)
        while mask:
            bit=mask.bit_length()-1
            if bit not in basis:
                basis[bit]=(mask,rhs,prov)
                break
            mm,bb,pp=basis[bit]
            mask^=mm;rhs^=bb;prov^=pp;steps+=1
        if mask==0 and rhs:
            return None,{'error':'projected_zero_equals_one','provenance':[projector.rows[i][2] for i in range(len(projector.rows)) if prov>>i&1],'row_xors':steps}
    eqs=[basis[k] for k in sorted(basis,reverse=True)]
    return eqs,{'rank_projection':len(eqs),'row_xors':steps,'provenance_masks':[e[2] for e in eqs]}

class DSU:
    def __init__(self,n):self.parent=list(range(n))
    def find(self,x):
        while self.parent[x]!=x:
            self.parent[x]=self.parent[self.parent[x]];x=self.parent[x]
        return x
    def join(self,a,b):
        a=self.find(a);b=self.find(b)
        if a!=b:self.parent[max(a,b)]=min(a,b)

def component_syndrome_terminal(F,p,cap=1000000):
    """Exact delta-zero original-source SAT/#SAT terminal with overlap-aware
    projected row components, GF2 syndrome DP and authenticated source models.
    An over-budget terminal returns UNRESOLVED, not UNSAT.
    """
    if not valid(F):return {'status':'MALFORMED','metrics':{}}
    n=max(abs(x) for c in F for x in c)
    if not isinstance(p,dict) or any(type(k)!=int or not 1<=k<=n or type(v)!=int or v not in (0,1) for k,v in p.items()):
        return {'status':'MALFORMED_PIN','metrics':{}}
    g=source_gate(F,p)
    scan={'source_literal_reads':g.get('source_literal_reads',0),
          'triangle_candidate_checks':g.get('triangle_candidate_checks',0),
          'triangle_choices_checked':g.get('triangle_choices_checked',0),
          'recognition_scans':len(F),'source_grammar_literal_reads':3*len(F),'policy_selections':1,'failed_policy_trials':0}
    if g['status']=='EMPTY':return {'status':'UNSAT_EMPTY','metrics':scan,'source_clause':g['source_clause']}
    scan.update(delta=g['delta'],nu=g['nu'],eta=g['eta'],f=len(g['free']),u=len(g['uncovered']))
    if g['delta']<0:return {'status':'UNSAT_GAP','metrics':scan}
    if g['delta']!=0:
        scan['failed_policy_trials']=1
        return {'status':'UNRESOLVED','metrics':scan}
    Pj=Projector(F,g,p)
    eqs,provenance=projected_echelon(Pj)
    scan.update(precomp_rows=Pj.metrics['precomp_rows'],
                precomp_row_xors=Pj.metrics['precomp_row_xors'],
                projected_row_xors=provenance['row_xors'],
                rank_outside=Pj.rank,nullity_outside=Pj.nullity,
                dense_matrix_bits_upper=len(Pj.rows)*(len(g['free'])+2),
                projection_rank=provenance.get('rank_projection',0))
    if eqs is None:
        return {'status':'UNSAT_PROJECTION','metrics':scan,'refutation':provenance}
    k=len(Pj.templates);m=len(eqs)
    dsu=DSU(k);var_owners=defaultdict(set)
    for i,options in enumerate(Pj.templates):
        for v in options[0]['assignments']:var_owners[v].add(i)
    for owners in var_owners.values():
        for j in list(owners)[1:]:dsu.join(min(owners),j)
    row_owners=[]
    for mask,rhs,pr in eqs:
        owners={i for v in var_owners if mask>>(v-1)&1 for i in var_owners[v]}
        row_owners.append(owners)
        if len(owners)>1:
            first=min(owners)
            for j in owners:dsu.join(first,j)
    components=defaultdict(list)
    for i in range(k):components[dsu.find(i)].append(i)
    grouped=sorted(components.values(),key=lambda ls:ls[0]);row_groups=defaultdict(list)
    for idx,owners in enumerate(row_owners):
        if not owners:
            if eqs[idx][1]:
                return {'status':'UNSAT_PROJECTION','metrics':scan,
                        'refutation':{'error':'constant_projected_row','source_rows':[Pj.rows[j][2] for j in range(len(Pj.rows)) if eqs[idx][2]>>j&1]}}
        else:row_groups[dsu.find(min(owners))].append(idx)
    metrics=Counter(scan);metrics['component_count']=len(grouped)
    group_reports=[];full_ones=0;full_assigned=0;options_product=1
    for grp in grouped:
        croot=dsu.find(grp[0]);indices=row_groups[croot]
        supports=set()
        for i in grp:supports.update(Pj.templates[i][0]['assignments'])
        overlap=sum(len(var_owners[v])>1 for v in supports)
        q=len(indices)
        target=sum(eqs[row][1]<<a for a,row in enumerate(indices))
        model_count=0;selection=None
        # Each group is an independent component of the projected constraint
        # hypergraph. If cycles share vertices, we enumerate *this component*
        # and reject incompatible templates. Otherwise, DP in GF(2)^q.
        if not overlap:
            table={0:1};paths={0:()};transitions=0;maxstates=1
            for ci in grp:
                new=Counter();newpaths={}
                for op in Pj.templates[ci]:
                    sig=sum((parity(eqs[row][0]&sum(1<<(v-1) for v,b in op['assignments'].items() if b))<<j)
                            for j,row in enumerate(indices))
                    for old_s,ways in table.items():
                        key=old_s^sig;new[key]+=ways;transitions+=1
                        if key not in newpaths:newpaths[key]=paths[old_s]+((ci,op['chosen_clause']),)
                table=dict(new);paths=newpaths;maxstates=max(maxstates,len(table))
                if transitions>cap:
                    metrics['failed_policy_trials']+=1
                    return {'status':'UNRESOLVED_CAP','metrics':dict(metrics),'cap':cap}
            model_count=table.get(target,0);selection=paths.get(target)
            metrics['dp_transitions']+=transitions
            metrics['dp_peak_states']=max(metrics['dp_peak_states'],maxstates)
            group_reports.append({'cycles':grp,'rows':indices,'q':q,'overlap':False,'method':'syndrome_dp',
                                  'target':target,'last_state_counts':dict(sorted(table.items())),
                                  'compatible_options':model_count,'transitions':transitions,
                                  'peak_states':maxstates})
        else:
            # Overlap grouping is a correctness firewall, not free. Branches
            # are charged and cap is enforced before exhaustive enumeration.
            attempts=math.prod(len(Pj.templates[i]) for i in grp)
            if attempts>cap:
                metrics['failed_policy_trials']+=1
                return {'status':'UNRESOLVED_CAP','metrics':dict(metrics),'cap':cap,'overlap_attempts':attempts}
            for choices in product(*(Pj.templates[i] for i in grp)):
                metrics['overlap_choice_attempts']+=1
                assignments={};consistent=True
                for op in choices:
                    for v,b in op['assignments'].items():
                        if v in assignments and assignments[v]!=b:
                            consistent=False;break
                        assignments[v]=b
                    if not consistent:break
                if not consistent:
                    metrics['overlap_conflicts']+=1;continue
                bits=sum(1<<(v-1) for v,b in assignments.items() if b)
                if all(parity(bits&eqs[row][0])==eqs[row][1] for row in indices):
                    model_count+=1
                    if selection is None:selection=tuple((ci,choices[j]['chosen_clause']) for j,ci in enumerate(grp))
            group_reports.append({'cycles':grp,'rows':indices,'q':q,'overlap':True,'method':'overlap_enumeration',
                                  'target':target,'compatible_options':model_count,'attempts':attempts})
        if not model_count:
            metrics['failed_choice_groups']+=1
            return {'status':'UNSAT_SYNDROME_EXHAUSTED','metrics':dict(metrics),'groups':group_reports,
                    'projected_rows':[{'mask':mm,'rhs':rhs,'source_row_xor':[Pj.rows[j][2] for j in range(len(Pj.rows)) if prov>>j&1]} for mm,rhs,prov in eqs],
                    'witness':None}
        options_product*=model_count
        for ci,chosen in selection:
            op=next(t for t in Pj.templates[ci] if t['chosen_clause']==chosen)
            for v,b in op['assignments'].items():
                if full_assigned>>(v-1)&1:assert (full_ones>>(v-1)&1)==b
                else:
                    full_assigned|=1<<(v-1)
                    if b:full_ones|=1<<(v-1)
    # All authenticated cycle vertices have been assigned. Check projected
    # constraints and reconstruct the W solution using one factored matrix.
    assert all(parity(mask&full_ones)==rhs for mask,rhs,_ in eqs)
    y=Pj.solution(full_ones)
    a={**p,**{v:full_ones>>(v-1)&1 for v in Pj.vertexset},
       **{v:y>>(v-1)&1 for v in Pj.W}}
    assert satisfies(F,a),('source SAT witness mismatch',a)
    metrics['source_witness_clause_checks']=len(F)
    metrics['witness_restore_ops']=len(g['free'])
    metrics['row_rhs_substitutions']=Pj.metrics['row_rhs_substitutions']
    count=options_product*(1<<Pj.nullity)
    metrics['compatible_cycle_choices']=options_product
    return {'status':'SAT','model_count':count,'witness':[a[v] for v in range(1,n+1)],
            'metrics':dict(metrics),'groups':group_reports,
            'projected_rows':[{'mask':mm,'rhs':rhs,'source_row_xor':[Pj.rows[j][2] for j in range(len(Pj.rows)) if prov>>j&1]} for mm,rhs,prov in eqs]}


def rename(F,p,perm):
    return tuple(tuple((1 if lit>0 else -1)*perm[abs(lit)] for lit in c) for c in F),{perm[v]:b for v,b in p.items()}

def complement(F,p):
    return tuple(tuple(-x for x in c) for c in F),{v:1-b for v,b in p.items()}

def test_run():
    U,V=source198()
    cases=[('F9_UNSAT_CUBE',F9,P9),('Y6_ROOT',Y6,{}),('F15_UNSAT',F15,P15_U),
           ('F15_SAT',F15,P15_S),('K5_SAT_OVERLAP',F15K5,P5_S),
           ('U198_UNSAT_ROOT',U,{}),('V198_SAT_ROOT',V,{})]
    rep={'run':'LSPV2_COMPONENT_SYNDROME295','status':'restricted conditional algebra, computational finite tests',
         'P_vs_NP':'OPEN','cases':{},'exhaustive':{},'falsifiers':{},'encoding':{},'cost_model':'literal/triangle/row/GF2 transition counts are Python logical proxy; no native FLMV bound'}
    for name,F,p in cases:
        res=component_syndrome_terminal(F,p)
        base=baseline(F,p,cap=1500)
        actual=sum(1 for _ in brute_models(F,p)) if len(F)<25 else None
        if res['status']=='SAT':assert res['model_count']==actual
        elif res['status'].startswith('UNSAT') and actual is not None:assert actual==0
        rep['cases'][name]={'label':('SAT' if actual else 'UNSAT') if actual is not None else ('UNSAT_CERTIFIED_PREVIOUS' if name=='U198_UNSAT_ROOT' else 'SAT_CERTIFIED_PREVIOUS'),
           'gate':res['status'],'model_count':res.get('model_count'),
           'delta':res['metrics'].get('delta'),'nu':res['metrics'].get('nu'),
           'metrics':res['metrics'],'groups':res.get('groups',[]),'projected_rows':res.get('projected_rows',[]),'refutation':res.get('refutation',{}),
           'baseline':base,'witness':res.get('witness')}
    stats=Counter();extras=Counter()
    for Fname,F,roots in [('Y6',Y6,[{}]),('F15',F15,[P15_U,P15_S])]:
        for root in roots:
            free=[v for v in range(1,max(abs(x) for c in F for x in c)+1) if v not in root]
            for seq in product((-1,0,1),repeat=len(free)):
                p={**root,**{v:b for v,b in zip(free,seq) if b!=-1}}
                a=component_syndrome_terminal(F,p)
                actual=sum(1 for _ in brute_models(F,p))
                if a['status']=='SAT':assert a['model_count']==actual
                elif a['status'].startswith('UNSAT'):assert actual==0
                stats[Fname,a['status']]+=1
                if a['status'] in ('SAT','UNSAT_SYNDROME_EXHAUSTED','UNSAT_PROJECTION'):
                    extras[Fname,'saturated']+=1
                    extras[Fname,'dp_transitions']+=a['metrics'].get('dp_transitions',0)
                    extras[Fname,'overlap_choice_attempts']+=a['metrics'].get('overlap_choice_attempts',0)
                    extras[Fname,'sat_extensions']+=actual
    rep['exhaustive']={k:{**{status:val for (name,status),val in stats.items() if name==k},
                          **{what:val for (name,what),val in extras.items() if name==k}} for k in ['Y6','F15']}
    # A disconnected product is only an EASY performance control: strict
    # target-valid formulas still have correct 2P2N occurrences and no copies.
    # Each SAT-complete F15_S cube belongs to one original F15 component.
    blocks=[]
    for copies in (1,2,4,8):
        F=tuple(tuple((1 if v>0 else -1)*(abs(v)+15*j) for v in c) for j in range(copies) for c in F15)
        pin={v+15*j:b for j in range(copies) for v,b in P15_S.items()}
        z=component_syndrome_terminal(F,pin)
        assert z['status']=='SAT' and z['model_count']==2**copies
        blocks.append({'copies':copies,'variables':15*copies,'nu':z['metrics']['nu'],
                       'group_count':z['metrics']['component_count'],'count':z['model_count'],
                       'dp_transitions':z['metrics']['dp_transitions'],
                       'naive_cycle_choice_bound':3**z['metrics']['nu'],'projection_rank':z['metrics']['projection_rank']})
    rep['product_controls']=blocks
    for name,F,p in [('F9',F9,P9),('F15',F15,P15_S),('K5',F15K5,P5_S)]:
        perm={v:len(set(abs(x) for c in F for x in c))+1-v for v in range(1,max(abs(x) for c in F for x in c)+1)}
        ff,pp=rename(F,p,perm);aa=component_syndrome_terminal(ff,pp)
        bb=component_syndrome_terminal(F,p)
        assert aa['status']==bb['status'] and aa.get('model_count')==bb.get('model_count')
        ff,pp=complement(F,p);cc=component_syndrome_terminal(ff,pp)
        assert cc['status']==bb['status'] and cc.get('model_count')==bb.get('model_count')
    rep['falsifiers']['overlap_K5']={k:rep['cases']['K5_SAT_OVERLAP']['metrics'].get(k,0) for k in ('overlap_choice_attempts','overlap_conflicts')}
    rep['falsifiers']['parity_only_F9']='UNSAT_SYNDROME_EXHAUSTED despite outside-cycle parity consistency'
    rep['falsifiers']['unbounded_nu']='component decomposition handles disjoint products; worst-case exponential remains'
    rep['falsifiers']['all_inputs']='U198/V198 roots δ=132, correctly UNRESOLVED'
    # Retain 0^n/1^n, S/U compatibility as original-source controls.
    for name,F,p in cases:
        n=max(abs(x) for c in F for x in c)
        zz=truths(F,{v:0 for v in range(1,n+1)})
        oo=truths(F,{v:1 for v in range(1,n+1)})
        assert all(x+y==3 for x,y in zip(zz,oo))
        rep['encoding'][name]={'zero_hist':[zz.count(i) for i in range(4)],'one_hist':[oo.count(i) for i in range(4)]}
    for name in ('F9_UNSAT_CUBE','F15_SAT','K5_SAT_OVERLAP'):
        case=rep['cases'][name]
        z=case['metrics']
        z['counted_gate_work_proxy']=sum(z.get(k,0) for k in ('source_grammar_literal_reads','source_literal_reads','triangle_candidate_checks','triangle_choices_checked','precomp_rows','precomp_row_xors','projected_row_xors','dp_transitions','overlap_choice_attempts','overlap_conflicts','source_witness_clause_checks','witness_restore_ops','row_rhs_substitutions','policy_selections','failed_policy_trials'))
    rep['falsifiers']['provenance']='projected rows each carry XOR of authenticated outside-cycle source parity/preference row IDs; preconditions require checked delta=0 and original M22 grammar'
    (P/'results295.json').write_text(json.dumps(rep,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'cases':{k:(v['gate'],v['model_count'],v['delta'],v['nu']) for k,v in rep['cases'].items()},
                      'exhaustive':rep['exhaustive'],'products':blocks},indent=2))

if __name__=='__main__':test_run()
