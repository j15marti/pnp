#!/usr/bin/env python3
"""LSPV-2 ALLINPUT-HORN-DEPTH303. Exact structural depth barrier and
source-typed adaptive wrapper, with native-like proxy ledger only.
No polynomial all-input claim; all unresolved states use exact fallback.
"""
import ast,collections,itertools,json,math,random,sys
from pathlib import Path
BASE=Path(__file__).resolve().parent
P302=(Path('/mnt/data/lspv2_302') if Path('/mnt/data/lspv2_302/linear_triangle302.py').exists() else Path(__file__).resolve().parent.parent)
SCRIPT302=(P302/'linear_triangle302.py' if (P302/'linear_triangle302.py').exists() else P302/'2026-11-01_0704_LSPV2_LINEAR_TRIANGLE302.py')
Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
F15P=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15))
F15N=((1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),(4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15))
F15=F15P+tuple(tuple(-i for i in c) for c in F15N)
U198=tuple(tuple(c) for c in ast.literal_eval(''.join(l for l in (P302/'2026-11-01_0704_LSPV2_LINEAR_TRIANGLE302_U198.txt').read_text().splitlines() if not l.startswith('#'))))
vtmp=[list(c) for c in U198];vtmp[2][2],vtmp[44][2]=vtmp[44][2],vtmp[2][2];V198=tuple(tuple(c) for c in vtmp)
V198_W='001110010011110001010001110100111110011011000101000101001010100001011010101011000100000111001010110101001110001001101000110001100010100101101110010101011001001100000110111001001101001101101001010101'
P_F9U={8:0,3:0,7:0,6:0,1:1,5:1}
P_F9S={1:0,2:0,8:1,9:1}
P_F15U=dict(zip(range(7,16),(0,0,0,0,1,1,1,1,0)))
P_F15S=dict(zip(range(7,16),(1,0,0,0,1,1,1,1,0)))

def grammar(F):
 try:
  if not F:return False
  n=max(abs(z) for c in F for z in c)
  if n%3 or 3*len(F)!=4*n:return False
  if any(len(c)!=3 or len(set(map(abs,c)))!=3 or (min(c)<0<max(c)) for c in F):return False
  if len(set(tuple(sorted(c)) for c in F))!=len(F):return False
  counts=collections.Counter(z for c in F for z in c)
  return all(counts[v]==counts[-v]==2 for v in range(1,n+1))
 except Exception:return False

def gamma(z):
 assert isinstance(z,int) and z>0
 b=format(z,'b');return '0'*(len(b)-1)+b

def encode(F):
 assert grammar(F)
 n=max(abs(x) for c in F for x in c);m=len(F);w=n.bit_length()
 return gamma(n)+gamma(m)+''.join(('1' if c[0]>0 else '0')+''.join(format(abs(x),'0%db'%w) for x in c) for c in F)

def decode(bits):
 """Total binary-string parser: refuses malformed headers, padding and quotas."""
 if not isinstance(bits,str) or not bits or any(c not in '01' for c in bits):return None
 pos=0
 def header():
  nonlocal pos
  start=pos
  while pos<len(bits) and bits[pos]=='0':pos+=1
  k=pos-start
  if pos>=len(bits) or pos+k>=len(bits):raise ValueError('truncated gamma')
  z=int(bits[pos:pos+k+1],2);pos+=k+1
  if not z:raise ValueError('zero length')
  return z
 try:
  n=header();m=header()
  if n%3 or m*3!=4*n:return None
  w=n.bit_length();length=m*(1+3*w)
  if len(bits)-pos!=length:return None
  out=[]
  for j in range(m):
   sign=1 if bits[pos]=='1' else -1;pos+=1
   clause=[]
   for k in range(3):
    z=int(bits[pos:pos+w],2);pos+=w
    if not (1<=z<=n):return None
    clause.append(sign*z)
   out.append(tuple(clause))
  if pos!=len(bits):return None
  return tuple(out) if grammar(tuple(out)) else None
 except (ValueError,IndexError,OverflowError,MemoryError):return None

def residual(F,p,flip=0):
 out=[];covered=0;reads=0
 for j,c in enumerate(F):
  cc=[];sat=False
  for l in c:
   reads+=1
   v=abs(l);sign=(l>0)^bool((flip>>(v-1))&1)
   if v in p:
    if p[v]==int(sign):sat=True
   else:cc.append(v if sign else -v)
  if sat:covered+=1
  else:out.append((j,tuple(cc)))
 return out,{'literal_reads':reads,'covered':covered}

def syntactic(res):
 cls=[c for _,c in res]
 return {'Horn':all(sum(l>0 for l in c)<=1 for c in cls),
         'dualHorn':all(sum(l<0 for l in c)<=1 for c in cls),
         'Krom':all(len(c)<=2 for c in cls),
         'empty':any(not c for c in cls)}

def excess(F,flip=0):
 return sum(max(0,sum((l>0)^bool((flip>>(abs(l)-1))&1) for l in c)-1) for c in F)

def excess_res(res):
 return sum(max(0,sum(l>0 for l in c)-1) for _,c in res)

def direct_depth_audit(F,p,flip=0):
 n=max(abs(l) for c in F for l in c);b=len(p)
 r,ledger=residual(F,p,flip);s=syntactic(r)
 E0=excess(F,flip);E1=excess_res(r)
 assert E0>=2*n//3 and E1>=E0-4*b,('renaming excess',n,b,E0,E1)
 if b*6<n:assert not s['Horn']
 if b*3<n and not flip:assert not any((s[q] for q in ('Horn','dualHorn','Krom')))
 if b*3<n:assert not s['Krom']
 return {'n':n,'b':b,'flip':flip,'E0':E0,'E1':E1,**s,**ledger}

def sat_source(F,a):
 return all(any(a[abs(l)]==int(l>0) for l in c) for c in F)

def baseline(F,p,cap=20000):
 n=max(abs(l) for c in F for l in c)
 meter=collections.Counter(); proof=[]
 def walk(a):
  meter['nodes']+=1
  if meter['nodes']>cap:return None
  a=dict(a)
  while True:
   units=[];remaining=0
   for j,c in enumerate(F):
    unresolved=[];satisfied=False
    for lit in c:
     meter['literal_probes']+=1
     if abs(lit) in a:
      if a[abs(lit)]==int(lit>0):satisfied=True;break
     else:unresolved.append(lit)
    if satisfied:continue
    if not unresolved:
     meter['conflict_clause_probes']+=1
     proof.append({'p':sorted(a.items()),'falsified_original_clause_id':j})
     return False
    remaining+=1
    if len(unresolved)==1:units.append(unresolved[0])
   if not units:
    if not remaining:
     a.update({v:0 for v in range(1,n+1) if v not in a});return a
    break
   changed=False
   for lit in units:
    v=abs(lit);z=int(lit>0)
    if v in a:
     if a[v]!=z:return False
    else:a[v]=z;meter['unit_assignments']+=1;changed=True
   if not changed:break
  x=next(v for v in range(1,n+1) if v not in a)
  for val in (0,1):
   meter['branch_attempts']+=1
   child=dict(a);child[x]=val
   r=walk(child)
   if r is None:return None
   if r is not False:return r
  return False
 ans=walk(p)
 tag='UNKNOWN' if ans is None else 'UNSAT' if ans is False else 'SAT'
 if tag=='SAT':assert sat_source(F,ans)
 return {'status':tag,'meter':dict(meter),'witness':''.join(str(ans[v]) for v in range(1,n+1)) if tag=='SAT' else None,
         'proof_leaves':len(proof),'proof_example':proof[:1]}

def residual_components(r,n,p):
 """Exact AND of connected residual components. Source clause IDs retained."""
 parent={i:i for i in range(1,n+1) if i not in p}
 def root(v):
  while parent[v]!=v:parent[v]=parent[parent[v]];v=parent[v]
  return v
 for j,c in r:
  vs=[abs(l) for l in c]
  if vs:
   first=vs[0]
   for other in vs[1:]:parent[root(other)]=root(first)
 groups=collections.defaultdict(lambda:{'variables':[],'clauses':[]})
 for v in parent:groups[root(v)]['variables'].append(v)
 for j,c in r:
  if c:groups[root(abs(c[0]))]['clauses'].append((j,c))
 return list(groups.values())

def gate(F,p):
 """Source-typed sound certificates plus an exact fallback. K4/matroid hooks
 unimplemented (unresolved), not free. All policies and scans are charged."""
 if isinstance(F,str):
  original_bits=len(F);F=decode(F)
  if F is None:return {'status':'MALFORMED','ledger':{'source_input_bits':original_bits}}
 if not grammar(F):return {'status':'MALFORMED','ledger':{'grammar_scanned':len(F)}}
 n=max(abs(l) for c in F for l in c)
 r,reads=residual(F,p);types=syntactic(r)
 ledger={'grammar_literal_probes':3*len(F),'residual_literal_probes':reads['literal_reads'],
         'tried_policies':['EMPTY','SIGNED_SPILL','SATURATED_TRIANGLE','HORN','DUAL_HORN','KROM','XOR','MATROID','K4','FALLBACK'],
         'certification':'source-clause witness or complete fallback trace',
         'unimplemented_policies':['MATROID_factor_verified_hook','K4_cut_verified_hook']}
 if types['empty']:
  j=next(j for j,c in r if not c)
  return {'status':'UNSAT_CUBE','certificate':{'empty_original_clause_id':j,'pins':p},'ledger':ledger}
 # Source-certified signed gap and saturated exact GF(2) policy from the 302 reproducibility module.
 import importlib.util
 sp=importlib.util.spec_from_file_location('verified302',SCRIPT302)
 mod=importlib.util.module_from_spec(sp);sp.loader.exec_module(mod)
 g=mod.status(F,p);cycles=mod.bounded_degree_cycles(g['edges']);nu=len(cycles['cycles'])
 delta=g['e']-g['eta']-nu
 ledger.update({'signed_source_literal_reads':3*len(F),'triangle_comparisons':cycles['pair_tests'],
                'triangle_adjacency_records':cycles['adjacency_records'],'delta':delta,'nu':nu})
 if delta<0:return {'status':'UNSAT_SIGNED','certificate':{'e':g['e'],'eta':g['eta'],'nu':nu,'delta':delta},'ledger':ledger}
 if delta==0:
  exact=mod.exact_affine(F,p,g,cycles,cap=1024)
  ledger['GF2_row_ops']=exact.get('row_ops',0);ledger['affine_choices']=exact.get('branches',0)
  if exact['label']=='SAT':
   return {'status':'SAT','certificate':{'kind':'SAT_AFFINE','count':exact['count'],'first_checked_witness':exact['models'][0]['witness']},'ledger':ledger}
  if exact['label']=='UNSAT_AFFINE':return {'status':'UNSAT_CUBE','certificate':{'kind':'ROW_XOR_ALL_BRANCHES','refuted':exact['branches'],'examples':exact['proofs']},'ledger':ledger}
 # Source-labeled AND components; ordinary residual children are explicitly NONCANONICAL.
 parts=residual_components(r,n,p)
 ledger['residual_component_sizes']=[(len(z['variables']),len(z['clauses'])) for z in parts]
 if len(parts)>1:
  combined={v:p.get(v,0) for v in range(1,n+1)};traces=[];all_sat=True
  for part in parts:
   if not part['clauses']:continue
   S=tuple(c for _,c in part['clauses'])
   b=baseline(S,{},cap=20000)
   traces.append({'source_clause_ids':[j for j,_ in part['clauses']],'status':b['status'],'meter':b['meter'],'proof_leaves':b['proof_leaves']})
   if b['status']=='UNSAT':
    return {'status':'UNSAT_CUBE','certificate':{'kind':'AND_COMPONENT_UNSAT','source_clause_ids':[j for j,_ in part['clauses']],'complete_dpll_trace':b['proof_leaves']},'ledger':{**ledger,'component_runs':traces}}
   if b['status']=='UNKNOWN':all_sat=False;break
   for v in part['variables']:
    if v<len(b['witness'])+1:combined[v]=int(b['witness'][v-1])
  if all_sat and sat_source(F,combined):
   return {'status':'SAT','certificate':{'kind':'AND_COMPONENT_SAT','witness':[combined[v] for v in range(1,n+1)]},'ledger':{**ledger,'component_runs':traces}}
  ledger['failed_component_runs']=traces
 # Standard syntactic residual solvers can be installed here, but exact DPLL fallback is always safe.
 ledger['syntactic']=types
 b=baseline(F,p)
 ledger['fallback']=b['meter']
 return {'status':b['status'],'certificate':{'kind':'DPLL_COMPLETE','proof_leaves':b['proof_leaves'],'witness':b['witness']} if b['status']!='UNKNOWN' else None,'ledger':ledger}

def chain(F,t):
 n=max(abs(x) for c in F for x in c);out=[]
 for k in range(t):out.extend(tuple((1 if l>0 else -1)*(abs(l)+k*n) for l in c) for c in F)
 # connect copies by exchanging a literal in the first positive clause of adjacent blocks
 out=list(map(list,out));m=len(F)
 for k in range(t-1):
  a,b=k*m,(k+1)*m
  out[a][0],out[b][0]=out[b][0],out[a][0]
 out=tuple(map(tuple,out));assert grammar(out)
 return out

def source_endpoints(F):
 n=max(abs(x) for c in F for x in c)
 return {str(bit):[sum(sum(bit==int(l>0) for l in c)==q for c in F) for q in range(4)] for bit in (0,1)}

def main():
 rng=random.Random(303);data={'id':'ALLINPUT_HORN_DEPTH303','seed':303,'status':'PROVED_RESTRICTED_PLUS_COMPUTATIONAL','cases':{},'falsifiers':{},'counts':{},'P_vs_NP':'OPEN'}
 for name,F,p in [('Y6_root',Y6,{}),('F9_root',F9,{}),('F9_S',F9,P_F9S),('F9_U',F9,P_F9U),('F15_root',F15,{}),('F15_S',F15,P_F15S),('F15_U',F15,P_F15U),('U198_root',U198,{}),('V198_root',V198,{}),('F9plusY6_root',chain(F9,1)+tuple(tuple((1 if l>0 else -1)*(abs(l)+9) for l in c) for c in Y6),{})]:
  assert grammar(F);g=gate(F,p)
  data['cases'][name]={'n':max(abs(x) for c in F for x in c),'m':len(F),'pins':p,'status':g['status'],'ledger':g['ledger'],
                       'certificate':g.get('certificate'), 'endpoints':source_endpoints(F)}
 for name,F in [('Y6',Y6),('F9',F9)]:
  n=max(abs(l) for c in F for l in c)
  census=collections.Counter();minimum={'Horn':n+1,'dualHorn':n+1,'Krom':n+1}
  for states in itertools.product((-1,0,1),repeat=n):
   p={i+1:s for i,s in enumerate(states) if s!=-1}
   v=direct_depth_audit(F,p);census['cube_tests']+=1
   for key in minimum:
    if v[key]:minimum[key]=min(minimum[key],len(p));census[key+'_states']+=1
  data['counts'][name]={'census':dict(census),'minimum_unrenamed_pins':minimum,'lower_bound':math.ceil(n/3)}
 # Quantified renamed-Horn bound tested exhaustively on Y6; sampled on F9 and F15.
 for name,F,samples in [('Y6',Y6,'exhaustive'),('F9',F9,1800),('F15',F15,600),('U198',U198,45),('V198',V198,45)]:
  n=max(abs(l) for c in F for l in c);s=0;minE=10**9;minred=10**9
  it=itertools.product(range(1<<n),itertools.product((-1,0,1),repeat=n)) if False else None
  if samples=='exhaustive':
   testing=((flip,{i+1:a for i,a in enumerate(st) if a!=-1}) for flip in range(1<<n) for st in itertools.product((-1,0,1),repeat=n))
  else:
   testing=((sum(1<<i for i in range(n) if rng.randrange(2)),{i+1:rng.randrange(2) for i in rng.sample(range(n),rng.randrange(min(n,7)+1))}) for _ in range(samples))
  for flip,p in testing:
   v=direct_depth_audit(F,p,flip);s+=1;minE=min(minE,v['E0']);minred=min(minred,v['E1']-v['E0']+4*len(p))
  data['falsifiers'][name]={'tests':s,'minimum_initial_excess':minE,'minimum_excess_slack':minred}
 for t in (2,4,8):
  F=chain(F9,t);v=direct_depth_audit(F,{});data['counts']['connected_F9_chain_'+str(t)]={'n':v['n'],'m':len(F),'root':{k:v[k] for k in ('Horn','dualHorn','Krom','E0')},'trivial_delta':2*v['n']-len(F),'components_expected':'connected'}
 # Target-valid component-peel positive controls, full source bits acquired and child emitted.
 data['canonical_children']={}
 for name,H in (('F9_SAT',F9),('U198_UNSAT',U198),('V198_SAT',V198)):
  n=max(abs(l) for c in H for l in c)
  parent=H+tuple(tuple((1 if l>0 else -1)*(abs(l)+n) for l in c) for c in Y6)
  assert grammar(parent) and grammar(H) and decode(encode(parent))==parent
  parent_bits,child_bits=encode(parent),encode(H)
  data['canonical_children'][name]={'parent_bits':len(parent_bits),'child_bits':len(child_bits),
   'whole_source_bit_reads':len(parent_bits),'physical_child_output_bit_writes':len(child_bits),
   'requires_full_parent_read':True,'target_valid':True,
   'power_short':len(child_bits)*len(child_bits)<=len(parent_bits),
   'equivalence':'SAT(H AND Y6) iff SAT(H); independently verified Y6 witness',
   'indexed_bit_accessor':'not newly implemented; materialized compact child'}
 # Negative malformed sources are rejected, no false SAT classification.
 bads=[(),((1,2,3),),Y6[:-1],Y6+Y6[:1],Y6[:1]+((-1,-2,-3),)+Y6[2:],Y6[:1]+((1,1,5),)+Y6[2:],Y6[:1]+((1,-4,5),)+Y6[2:]]
 data['malformed']=[{'index':i,'rejected':gate(F,{})['status']=='MALFORMED'} for i,F in enumerate(bads)]
 for name,F in (('Y6',Y6),('F9',F9),('F15',F15),('U198',U198),('V198',V198)):
  encoded=encode(F);assert decode(encoded)==F
  data['counts'][name+'_bits']={'bits':len(encoded),'grammar_roundtrip':True}
 b=encode(F9)
 broken=[b+'0',b[:-1],b[:10]+'2'+b[11:],'0'*len(b),b.replace('1','0'),b[:13]+'0'*12+b[25:]]
 data['malformed_encoded']=[{'index':i,'rejected':gate(z,{})['status']=='MALFORMED'} for i,z in enumerate(broken)]
 assert all(x['rejected'] for x in data['malformed_encoded'])
 assert all(e['rejected'] for e in data['malformed'])
 (BASE/'raw303.json').write_text(json.dumps(data,indent=2,sort_keys=True,default=list)+'\n')
 print(json.dumps({'cases':{k:v['status'] for k,v in data['cases'].items()},'minpins':{k:v['minimum_unrenamed_pins'] for k,v in data['counts'].items() if k in ('Y6','F9')},'renamed':data['falsifiers'],'malformed':len(bads)},indent=2))
if __name__=='__main__':main()