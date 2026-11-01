#!/usr/bin/env python3
"""LSPV-2 LINEAR TRIANGLE302: authenticated bounded-degree residual cycles.

Independent-output experiment, no claims about arbitrary SAT lower bounds.
Reads U198 from the original-source verified fixture, with local sha provenance.
Produces JSON and a compressed event-sourced output-tape record.
"""
import ast, gzip, hashlib, json, math, itertools, collections
from pathlib import Path
R=Path(__file__).resolve().parent
Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
F15P=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15))
F15N=((1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),(4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15))
F15=F15P+tuple(tuple(-x for x in c) for c in F15N)
UFILE=R/'2026-11-01_0704_LSPV2_LINEAR_TRIANGLE302_U198.txt'
U=tuple(tuple(c) for c in ast.literal_eval(''.join(line for line in UFILE.read_text().splitlines() if not line.startswith('#'))))
V=list(map(list,U));V[2][2],V[44][2]=V[44][2],V[2][2];V=tuple(map(tuple,V))
V_WITNESS='001110010011110001010001110100111110011011000101000101001010100001011010101011000100000111001010110101001110001001101000110001100010100101101110010101011001001100000110111001001101001101101001010101'
P_U=dict(zip(range(7,16),(0,0,0,0,1,1,1,1,0)))
P_S=dict(zip(range(7,16),(1,0,0,0,1,1,1,1,0)))
F9_U={8:0,3:0,7:0,6:0,1:1,5:1}
F9_S={1:0,2:0,8:1,9:1}

def valid(F):
 if not F:return False
 n=max(abs(x) for c in F for x in c)
 if n%3 or len(F)*3!=4*n:return False
 cs=collections.Counter((abs(x),x>0) for c in F for x in c)
 if len(set(tuple(sorted(c)) for c in F))!=len(F):return False
 for c in F:
  if len(c)!=3 or len({abs(x) for x in c})!=3 or not (all(x>0 for x in c) or all(x<0 for x in c)):return False
 return all(cs[v,True]==cs[v,False]==2 for v in range(1,n+1))

def status(F,p):
 free=set(range(1,max(abs(x) for c in F for x in c)+1))-p.keys()
 covered=[];uncovered=[];edges=[];s=collections.Counter()
 for j,c in enumerate(F):
  if any(abs(x) in p and p[abs(x)]==int(x>0) for x in c):
   covered.append(j)
   for x in c:
    if abs(x) in free:s[abs(x),x>0]+=1
  else:
   rem=[abs(x) for x in c if abs(x) in free]
   uncovered.append(j)
   if not rem:return {'empty':j}
   if len(rem)==2:edges.append((j,*rem))
 eta=sum(min(s[x,True],s[x,False]) for x in free)
 preferred={x:(0 if s[x,True]>s[x,False] else 1) for x in free if s[x,True]!=s[x,False]}
 return {'free':sorted(free),'covered':covered,'uncovered':uncovered,'edges':edges,'eta':eta,'preferred':preferred,'e':2*len(free)-len(uncovered)}

def bounded_degree_cycles(edges):
 # Indexed adjective: original-source clause-ID uniquely identifies each binary edge.
 adj=[[] for _ in range(1+max((max(u,v) for _,u,v in edges),default=0))]
 for j,u,v in edges:
  adj[u].append((j,v));adj[v].append((j,u))
 assert all(len(q)<=4 for q in adj),'canonical source degree violation'
 used=set();picked=[];total_triangles=0;pair_tests=0;source_edge_reads=0
 for j,u,v in edges: # original source order gives sorted j
  candidates=[]
  for a,w in adj[u]:
   if a<=j:continue
   for b,z in adj[v]:
    if b<=j:continue
    pair_tests+=1
    if w==z and a!=b:
     candidates.append(tuple(sorted((j,a,b))))
  # all triangles whose smallest source ID is j: at most nine candidates.
  total_triangles+=len(candidates)
  for triangle in sorted(candidates):
   if not any(k in used for k in triangle):
    picked.append(triangle);used.update(triangle)
  source_edge_reads+=1
 # Exact proxy that includes adjacency/source lookups and marked bitset changes.
 word_work=2*len(edges)+pair_tests+sum(len(v) for v in adj)+3*total_triangles+3*len(picked)
 return {'cycles':picked,'triangles':total_triangles,'pair_tests':pair_tests,
         'E':len(edges),'old_cubic_candidates':math.comb(len(edges),3) if len(edges)>=3 else 0,
         'degree_bound_ok':True,'max_degree':max((len(v) for v in adj),default=0),
         'indexed_word_ops_proxy':word_work,'adjacency_records':2*len(edges),
         'used_bit_writes':3*len(picked)}

def brute_cycles(edges):
 triples=[]
 for es in itertools.combinations(edges,3):
  d=collections.Counter(z for e in es for z in e[1:])
  if len(d)==3 and all(v==2 for v in d.values()):triples.append(tuple(sorted(e[0] for e in es)))
 used=set();result=[]
 for t in sorted(triples):
  if not used.intersection(t):result.append(t);used.update(t)
 return (result,len(triples))

def source_sat(F,ass):
 return all(any(ass[abs(l)]==int(l>0) for l in c) for c in F)

def gf2(rows,n):
 basis={};ops=0;proof=[]
 for mask,rhs,name in rows:
  provenance={name}; original=(mask,rhs)
  while mask:
   high=mask.bit_length()-1
   ops+=1
   if high not in basis:
    basis[high]=(mask,rhs,provenance)
    break
   mm,rr,pp=basis[high]
   mask^=mm;rhs^=rr;provenance.symmetric_difference_update(pp)
  if mask==0 and rhs:
   return {'ok':False,'rank':len(basis),'ops':ops,'sources':sorted(provenance)}
 bits=0
 for high in sorted(basis):
  mask,rhs,_=basis[high]
  value=rhs^((bits & mask).bit_count()&1)
  bits|=value<<high
 return {'ok':True,'rank':len(basis),'ops':ops,'bits':bits}

def exact_affine(F,p,g,cc,cap=5000):
 if g['e']-g['eta']-len(cc['cycles'])<0:return {'label':'UNSAT_GAP','count':0,'branches':0}
 if g['e']-g['eta']-len(cc['cycles'])!=0:return {'label':'UNRESOLVED','branches':0}
 base=[];labels={}
 for j in g['uncovered']:
  if any(j in cyc for cyc in cc['cycles']):continue
  rem=[l for l in F[j] if abs(l) not in p]
  mask=sum(1<<(abs(l)-1) for l in rem)
  rhs=1 if rem[0]>0 else 1^(len(rem)&1)
  label=('clause',j);base.append((mask,rhs,label));labels[label]=(mask,rhs)
 for x,b in g['preferred'].items():
  label=('preferred',x);base.append((1<<(x-1),b,label));labels[label]=(1<<(x-1),b)
 branches=math.prod(map(len,cc['cycles']))
 if branches>cap:return {'label':'UNRESOLVED_CAP','branches':branches}
 rank_counts=[];proofs=[];total=0;row_ops=0
 all_picks=itertools.product(*cc['cycles'])
 for picks in all_picks:
  rows=base.copy();local=labels.copy()
  for cyc in cc['cycles']:
   for j in cyc:
    rem=[abs(l) for l in F[j] if abs(l) not in p]
    if j in picks:
     for x in rem:
      label=('double',j,x);row=(1<<(x-1),int(F[j][0]>0),label)
      rows.append(row);local[label]=row[:2]
    else:
     label=('xor',j);row=((1<<(rem[0]-1))^(1<<(rem[1]-1)),1,label)
     rows.append(row);local[label]=row[:2]
  q=gf2(rows,max(g['free'],default=0));row_ops+=q['ops']
  if not q['ok']:
   assert q['sources']
   checksum=(0,0)
   for name in q['sources']:
    a,b=local[name];checksum=(checksum[0]^a,checksum[1]^b)
   assert checksum==(0,1),'row provenance must be authentically 0=1'
   proofs.append({'picks':picks,'sources':q['sources'],'zero_one':checksum})
  else:
   count=1<<(len(g['free'])-q['rank'])
   witness={x:((q['bits']>>(x-1))&1) for x in g['free']};witness.update(p)
   assert source_sat(F,witness),'GF2 witness must satisfy every original source clause'
   total+=count
   rank_counts.append({'picks':picks,'rank':q['rank'],'models':count,'witness':[witness[x] for x in range(1,max(abs(l) for c in F for l in c)+1)]})
 return {'label':'SAT' if total else 'UNSAT_AFFINE','count':total,'branches':branches,'row_ops':row_ops,'models':rank_counts[:5],'proofs':proofs[:5],'all_branches_refuted':len(proofs)==branches if not total else False}

def dpll(F,p,cap=500000):
 state={'nodes':0,'literal_probes':0,'branch_attempts':0,'status':'UNKNOWN'}
 def walk(a):
  state['nodes']+=1
  if state['nodes']>cap:return None
  while True:
   units=[];unresolved=False
   for c in F:
    found=False;un=[]
    for x in c:
     state['literal_probes']+=1
     if abs(x) in a:
      if a[abs(x)]==int(x>0):found=True;break
     else:un.append(x)
    if found:continue
    if not un:return False
    unresolved=True
    if len(un)==1:units.append(un[0])
   if not units:
    if not unresolved:return True
    break
   changed=False
   for l in units:
    v=abs(l);want=int(l>0)
    if v in a:
     if a[v]!=want:return False
    else:a[v]=want;changed=True
   if not changed:break
  v=next((x for x in range(1,max(abs(l) for c in F for l in c)+1) if x not in a),None)
  if v is None:return False
  for b in (0,1):
   state['branch_attempts']+=1
   q=walk({**a,v:b})
   if q is not False:return q
  return False
 result=walk(dict(p));state['status']='SAT' if result is True else 'UNSAT' if result is False else 'UNKNOWN'
 return state

def gamma(v):
 assert v>=1
 b=bin(v)[2:];return '0'*(len(b)-1)+b

def encode(F):
 n=max(abs(l) for c in F for l in c);m=len(F);w=n.bit_length()
 return gamma(n)+gamma(m)+''.join(('1' if c[0]>0 else '0')+''.join(format(abs(l),'0%db'%w) for l in c) for c in F)

def compose(A,B):
 n=max(abs(l) for c in A for l in c)
 return tuple(A)+tuple(tuple((1 if l>0 else -1)*(n+abs(l)) for l in c) for c in B)

def trace_child(A,label):
 parent=compose(A,Y6);child=A
 assert valid(parent) and valid(child)
 sp=encode(parent);sc=encode(child)
 assert sc==encode(A)
 # Parent encodes n+6,m+8; parsed metadata and authenticated trailing Y6 are paid.
 n=max(abs(l) for c in A for l in c);m=len(A)
 np=n+6;mp=m+8
 wp=np.bit_length();wc=n.bit_length()
 hp=len(gamma(np))+len(gamma(mp));hc=len(gamma(n))+len(gamma(m))
 rp=1+3*wp;rc=1+3*wc
 childheader=gamma(n)+gamma(m)
 assert len(sp)==hp+mp*rp and len(sc)==hc+m*rc
 idxw=len(sp).bit_length();idx=[0]*idxw;out=[0]*len(sc)
 totals=collections.Counter();events=[];changed_out=[];changed_register=[]
 # Explicit full parent scan, grammar and certified exact-Y6 suffix acquisition.
 # These operations run in Python outside the tape microtrace, so do not assert
 # a native FLMV end-to-end bound. Literal scans are separately recorded.
 totals['preflight_source_bits_scanned']=len(sp)
 totals['preflight_source_literals_scanned']=3*mp
 totals['preflight_source_clauses_scanned']=mp
 totals['certified_suffix_literals_checked']=24
 for j in range(len(sc)):
  if j<hc:
   address=None;bit=int(childheader[j]);totals['computed_header_bits']+=1
  else:
   d=j-hc;row=d//rc;off=d%rc
   if off==0:address=hp+row*rp
   else:
    vbit=off-1;slot=vbit//wc;b=vbit%wc
    address=hp+row*rp+1+slot*wp+(wp-wc)+b
   assert 0<=address<len(sp)
   bit=int(sp[address]);totals['mapped_source_reads']+=1
  # Explicit fixed-index-register write protocol before every mapped source read.
  if address is not None:
   desired=[(address>>k)&1 for k in range(idxw)]
   for k,new in enumerate(desired):
    before=idx[k];idx[k]=new;d=int(before!=new)
    totals['phys_xor']+=d;totals['index_bit_writes']+=1;totals['index_head_moves']+=k+1
    if d:changed_register.append(k)
    events.append(['INDEX',j,k,before,new,d])
   totals['source_reads']+=1;totals['indexed_jumps']+=1
   totals['read_bit_zero']+=1-bit
  before=out[j];new=bit;out[j]=new;d=int(before!=new)
  totals['output_bit_writes']+=1;totals['phys_xor']+=d
  if d:changed_out.append(j)
  events.append(['OUT',j,j,before,new,d])
 assert ''.join(map(str,out))==sc,'indexed source accessor must generate each actual child bit'
 endpoint=sum(idx)+sum(out)
 assert totals['phys_xor']>=endpoint
 file=R/('physical_'+label+'.jsonl.gz')
 with gzip.open(file,'wt') as fh:
  for event in events:fh.write(json.dumps(event,separators=(',',':'))+'\n')
 return {'parent_bits':len(sp),'child_bits':len(sc),'target_parent_valid':True,'target_child_valid':True,
         'sat_equivalence':'certified_Y6_SAT_disconnected_component',
         'physical_tape_content':dict(totals),'endpoint_phys_xor':endpoint,
         'changed_output_bit_positions':changed_out[:128],
         'changed_register_bit_positions':changed_register[:128],
         'event_file':file.name,'event_count':len(events),'event_stream_complete':len(events)==totals['index_bit_writes']+totals['output_bit_writes'],
         'output_changed_original_records':list(range(len(A),len(parent))),
         'index_head_moves_counted_separately':True,
         'python_state_peak_not_charged_to_model':True}

def signed_controls(F,limit_steps=16):
 n=max(abs(x) for c in F for x in c)
 extremes=[];pairs=[]
 for j,c in enumerate(F):
  sl=[{'literal':l,'variable':abs(l),'S':int(l>0),'invert_S_U':int(l<0),
       'U':int(l<0),'invert_U_S':int(l>0)} for l in c]
  extremes.append({'source_clause_id':j,'occurrences':sl})
 for j in range(len(F)):
  for k in range(j+1,len(F)):
   A=F[j];B=F[k]
   same=any(l in B for l in A);opp=any(-l in B for l in A)
   pairs.append({'source_clause_ids':[j,k], 'SS':not opp,'SU':not same,'US':not same,'UU':not opp})
 def cl_counts(bits):
  return [sum(((bits>>(abs(l)-1))&1)==int(l>0) for l in c) for c in F]
 def hist(vec):return [vec.count(i) for i in range(4)]
 def trajectory(gray):
  current=[0]*len(F);trace=[];acc=0
  for step in range(min(1<<n,limit_steps)):
   mask=step^(step>>1) if gray else step
   nxt=cl_counts(mask)
   change=[j for j in range(len(F)) if current[j]!=nxt[j]] if step>0 else []
   xor=sum((a^b).bit_count() for a,b in zip(current,nxt)) if step>0 else 0
   if step>0:acc+=xor
   trace.append({'step':step,'global_mask':mask,'histogram':hist(nxt),
                 'changed_clause_ids':change,'d_logic':xor})
   current=nxt
  return {'frames':trace,'sum_adjacent_d_logic':acc,'diagnostic_only':True}
 all0=cl_counts(0);all1=cl_counts((1<<n)-1)
 return {'n':n,'clauses':len(F),'original_S_U_inversions':extremes,'pair_compatibilities':pairs,
         'all_zero_hist':hist(all0),'all_one_hist':hist(all1),
         'binary_flip_trail':trajectory(False),'gray_flip_trail':trajectory(True)}

def run():
 assert all(valid(F) for F in (Y6,F9,F15,U,V)), 'all five sources valid canonical originals'
 witness={i+1:int(b) for i,b in enumerate(V_WITNESS)}
 assert len(witness)==198 and source_sat(V,witness),'V198 original SAT witness'
 fixtures={'Y6':(Y6,{}),'F9_S':(F9,F9_S),'F9_U':(F9,F9_U),
   'F15_S':(F15,P_S),'F15_U':(F15,P_U),'U198':(U,{}),'V198':(V,{})}
 out={'id':'LINEAR_TRIANGLE302','status':'PROVED/EXACT restricted bounded-degree triangle enumeration','source_sha256':hashlib.sha256(UFILE.read_bytes()).hexdigest(),
   'tests':{},'census':{},'physical':{},'claims':{'P_vs_NP':'OPEN','arbitrary_ARC':'OPEN','FLMV_transport':'OPEN'}}
 for name,(F,p) in fixtures.items():
  sg=status(F,p)
  cc=bounded_degree_cycles(sg['edges']) if 'edges' in sg else {'cycles':[],'E':0}
  if cc['E']<=15:
   other,nt=brute_cycles(sg['edges']);assert other==cc['cycles'] and nt==cc['triangles'],(name,other,cc)
  result=exact_affine(F,p,sg,cc) if 'e' in sg else {'label':'UNSAT_EMPTY'}
  baseline=dpll(F,p,cap=15000 if name in ('U198','V198') else 100000)
  if name in ('U198','V198'):assert result['label']=='UNRESOLVED'
  out['tests'][name]={'n':max(abs(l) for c in F for l in c),'m':len(F),'p':p,
       'f':len(sg.get('free',[])),'u':len(sg.get('uncovered',[])),'eta':sg.get('eta'),
       'e':sg.get('e'),'delta':sg.get('e',0)-sg.get('eta',0)-len(cc['cycles']),
       'cycle_index':cc,'exact_terminal':result,'baseline':baseline,'source_label_provenance':
       'external_independent_384_interface_certificate' if name=='U198' else 'checked_full_witness' if name=='V198' else 'exhaustive_small_source_enumeration'}
 for name,F,roots in (('Y6',Y6,[{}]),('F15',F15,[P_U,P_S])):
  stats=collections.Counter()
  for root in roots:
   free=[v for v in range(1,max(abs(l) for c in F for l in c)+1) if v not in root]
   for states in itertools.product((-1,0,1),repeat=len(free)):
    p={**root,**{v:s for v,s in zip(free,states) if s!=-1}}
    sg=status(F,p)
    if 'empty' in sg:stats['empty']+=1;continue
    cc=bounded_degree_cycles(sg['edges'])
    slow,nt=brute_cycles(sg['edges'])
    assert cc['cycles']==slow and nt==cc['triangles'],'triangle set and ordering identical'
    stats['cubes']+=1;stats['fast_pair_tests']+=cc['pair_tests'];stats['old_comb_candidates']+=cc['old_cubic_candidates']
    stats['all_triangles']+=cc['triangles']
    if sg['e']-sg['eta']-len(cc['cycles'])==0:
     stats['saturated_cubes']+=1
     exact=exact_affine(F,p,sg,cc)
     assert exact['label'] in ('SAT','UNSAT_AFFINE'),exact
     freevs=sg['free'];recount=0
     for bits in itertools.product((0,1),repeat=len(freevs)):
      a={**p,**dict(zip(freevs,bits))};recount+=source_sat(F,a)
     assert recount==exact['count'],('rank #SAT',name,p,exact,recount)
     stats['saturated_models']+=recount
  out['census'][name]=dict(stats)
 # Large disjoint known-label sources with many residual binary edges and no overlapping cross components.
 repeated={}
 for name,F,p in [('F9_S',F9,F9_S),('F9_U',F9,F9_U)]:
  for t in (8,64):
   allF=[];allp={};n=len({abs(l) for c in F for l in c})
   for k in range(t):
    allF.extend(tuple((1 if x>0 else -1)*(k*n+abs(x)) for x in c) for c in F)
    allp.update({k*n+x:b for x,b in p.items()})
   Frep=tuple(allF)
   assert valid(Frep)
   sg=status(Frep,allp);cc=bounded_degree_cycles(sg['edges'])
   repeated[name+'x'+str(t)]={'n':len(Frep)*3//4,'E':cc['E'],'old_choose_3':cc['old_cubic_candidates'],
        'new_pair_tests':cc['pair_tests'],'new_index_word_ops':cc['indexed_word_ops_proxy'],
        'new_T':cc['triangles'],'greedy_nu':len(cc['cycles']),'adjacency_records':cc['adjacency_records']}
 out['products']=repeated
 out['signed_controls']={name:signed_controls(F) for name,F in [('Y6',Y6),('F9',F9),('F15',F15)]}
 for name,F in [('F9SAT',F9),('U198UNSAT',U),('V198SAT',V)]:out['physical'][name]=trace_child(F,name)
 (R/'results302.json').write_text(json.dumps(out,indent=2,sort_keys=True,default=list)+'\n')
 print(json.dumps({'cases':{k:{'E':v['cycle_index']['E'],'nu':len(v['cycle_index']['cycles']),'delta':v['delta'],'terminal':v['exact_terminal']['label'],'DPLL':v['baseline']['status']} for k,v in out['tests'].items()},
 'census':out['census'],'products':out['products'],'physical':{k:{'parent':v['parent_bits'],'child':v['child_bits'],'phys_xor':v['physical_tape_content']['phys_xor']} for k,v in out['physical'].items()}},indent=2))
if __name__=='__main__':run()