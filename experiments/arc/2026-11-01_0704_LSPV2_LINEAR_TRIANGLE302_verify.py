#!/usr/bin/env python3
"""No-import independent verifier for LSPV-2 LINEAR-TRIANGLE302.
Verifies source grammar, every small cube, exact triangle order, SAT witnesses,
all U198 interface assignments and V198 witness, and physical tape-event replay.
"""
import ast,collections,gzip,itertools,json,math,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent
RAW=json.loads((R/'results302.json').read_text())
A6=[(1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6)]
A9=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9)]
A15=[(1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15),(-1,-2,-11),(-2,-3,-11),(-1,-3,-12),(-4,-5,-13),(-5,-6,-14),(-4,-6,-15),(-7,-8,-12),(-8,-9,-13),(-9,-10,-14),(-10,-7,-15)]
U=[tuple(t) for t in ast.literal_eval(''.join(t for t in (R/'2026-11-01_0704_LSPV2_LINEAR_TRIANGLE302_U198.txt').read_text().splitlines() if not t.startswith('#')))]
V=[list(t) for t in U];V[2][2],V[44][2]=V[44][2],V[2][2];V=[tuple(t) for t in V]
W='001110010011110001010001110100111110011011000101000101001010100001011010101011000100000111001010110101001110001001101000110001100010100101101110010101011001001100000110111001001101001101101001010101'
PU=dict(zip(range(7,16),(0,0,0,0,1,1,1,1,0)))
PS=dict(zip(range(7,16),(1,0,0,0,1,1,1,1,0)))
F9U={8:0,3:0,7:0,6:0,1:1,5:1};F9S={1:0,2:0,8:1,9:1}
CHECK=collections.Counter()
def ck(condition,label):
 CHECK['checks']+=1
 if not condition:raise AssertionError(label)

def valid(F):
 try:
  if not F:return False
  n=max(abs(x) for c in F for x in c)
  if 3*len(F)!=4*n or n%3:return False
  d=collections.Counter(x for c in F for x in c)
  if len(set(tuple(sorted(c)) for c in F))!=len(F):return False
  if any(len(c)!=3 or len(set(map(abs,c)))!=3 or (any(x<0 for x in c) and any(x>0 for x in c)) for c in F):return False
  return all(d[v]==2 and d[-v]==2 for v in range(1,n+1))
 except Exception:return False

def source_true(F,a):
 return all(any(a[abs(v)]==int(v>0) for v in c) for c in F)

def source_models(F,p):
 n=max(abs(x) for c in F for x in c)
 free=[x for x in range(1,n+1) if x not in p]
 out=[]
 for vals in itertools.product((0,1),repeat=len(free)):
  a={**p,**dict(zip(free,vals))}
  if source_true(F,a):out.append(a)
 return out

def slow_greedy(F,p):
 edges=[];remaining=[];covered=[];inc=collections.Counter();fvs=[v for v in range(1,max(abs(x) for c in F for x in c)+1) if v not in p]
 for j,c in enumerate(F):
  if any(abs(x) in p and p[abs(x)]==int(x>0) for x in c):
   covered.append(j)
   for x in c:
    if abs(x) in fvs:inc[(abs(x),x>0)]+=1
  else:
   remaining.append(j)
   r=[abs(x) for x in c if abs(x) not in p]
   if not r:return None
   if len(r)==2:edges.append((j,r[0],r[1]))
 alltri=[]
 for trip in itertools.combinations(edges,3):
  ids=tuple(t[0] for t in trip)
  deg=collections.Counter(v for t in trip for v in t[1:])
  if len(deg)==3 and set(deg.values())=={2}:alltri.append(ids)
 used=set();chosen=[]
 for tri in sorted(alltri):
  if set(tri).isdisjoint(used):chosen.append(tri);used.update(tri)
 eta=sum(min(inc[v,True],inc[v,False]) for v in fvs)
 return {'cycles':[list(x) for x in chosen],'triangles':len(alltri),'e':2*len(fvs)-len(remaining),'eta':eta,'E':len(edges)}

def gamma(n):
 b=f'{n:b}';return '0'*(len(b)-1)+b

def encoding(F):
 n=max(abs(l) for c in F for l in c);m=len(F);w=n.bit_length()
 return gamma(n)+gamma(m)+''.join(str(int(c[0]>0))+''.join(format(abs(v),f'0{w}b') for v in c) for c in F)

def compose(F):
 n=max(abs(l) for c in F for l in c)
 return list(F)+[tuple((1 if x>0 else -1)*(abs(x)+n) for x in c) for c in A6]

def replay(name,F):
 meta=RAW['physical'][name]
 P=compose(F);old=encoding(P);expected=encoding(F)
 ck(meta['target_parent_valid'] and valid(P),'parent grammar')
 ck(meta['target_child_valid'] and valid(F),'child grammar')
 ck(len(old)==meta['parent_bits'] and len(expected)==meta['child_bits'],'reported bit lengths')
 iw=len(old).bit_length();index=[0]*iw;output=[0]*len(expected);pos=0;changes=0;writes=0;jumps=0;zero=0;hC=len(gamma(max(abs(x) for c in F for x in c)))+len(gamma(len(F)))
 n=max(abs(x) for c in F for x in c);m=len(F);wp=(n+6).bit_length();wc=n.bit_length()
 hp=len(gamma(n+6))+len(gamma(m+8));rP=1+3*wp;rC=1+3*wc
 with gzip.open(R/meta['event_file'],'rt') as fd:
  for record in fd:
   lane,j,cell,before,after,d=json.loads(record);writes+=1
   ck(d==int(before!=after),'independent adjacent XOR')
   if lane=='INDEX':
    ck(index[cell]==before,'index source state match')
    index[cell]=after
   elif lane=='OUT':
    ck(output[cell]==before and cell==j,'output state match')
    output[cell]=after
    if j<hC:want=int((gamma(n)+gamma(m))[j]);address=None
    else:
     q=j-hC;row=q//rC;off=q%rC
     address=hp+row*rP if off==0 else hp+row*rP+1+((off-1)//wc)*wp+(wp-wc)+((off-1)%wc)
     want=int(old[address]);jumps+=1;zero+=int(want==0)
     ck(sum(b<<k for k,b in enumerate(index))==address,'indexed address exactly source bit')
    ck(after==want,'emitted bit must come from authenticated source bit or gamma header')
   else:raise AssertionError('illegal event lane')
   changes+=d
 ck(''.join(map(str,output))==expected,'fully reconstructed target bitstring')
 ck(writes==meta['event_count'],'event stream completeness')
 ck(changes==meta['physical_tape_content']['phys_xor'],'physical XOR sum')
 ck(jumps==meta['physical_tape_content']['source_reads'],'source reads')
 ck(zero==meta['physical_tape_content']['read_bit_zero'],'zero reads')
 ck(sum(index)+sum(output)==meta['endpoint_phys_xor'],'endpoint aligned physical XOR')
 return {'events':writes,'physical_xor':changes,'source_reads':jumps,'verified':True}

def dpll(F,p,work):
 work['nodes']+=1
 a=dict(p)
 while True:
  active=[]
  for c in F:
   und=[];covered=False
   for x in c:
    work['literal_visits']+=1
    if abs(x) not in a:und.append(x)
    elif a[abs(x)]==int(x>0):covered=True;break
   if not covered:
    if not und:return False
    active.append(und)
  if not active:return True
  singleton=next((c[0] for c in active if len(c)==1),None)
  if singleton is None:break
  a[abs(singleton)]=int(singleton>0)
 pivot=abs(min(active,key=len)[0])
 return dpll(F,{**a,pivot:0},work) or dpll(F,{**a,pivot:1},work)

def certify_U198():
 ck(valid(U) and valid(V),'U and V canonical originals')
 checked=0;works=collections.Counter();supports=[]
 for k in range(6):
  block=U[2+42*k:2+42*(k+1)]
  ck(len(block)==42,'U198 each authenticated module has 42 clauses')
  supports.append(set())
  for bits in range(64):
   pin={193+v:(bits>>v)&1 for v in range(6)}
   if dpll(block,pin,works):supports[-1].add(bits)
   checked+=1
 legal=[]
 for bits in range(64):
  a={193+v:(bits>>v)&1 for v in range(6)}
  if all(any(a[abs(x)]==int(x>0) for x in c) for c in U[:2]):legal.append(bits)
 for s in supports:legal=[k for k in legal if k in s]
 ck(not legal,'U198 exhaustive six-way boundary proof')
 ck(len(W)==198 and source_true(V,{j+1:int(b) for j,b in enumerate(W)}),'V198 full source SAT witness')
 return {'boundary_queries':checked,'local_dpll_nodes':works['nodes'],'local_dpll_literal_visits':works['literal_visits'],'U198':'UNSAT','V198':'SAT'}

def extremes(F):
 counter=0
 for j,k in itertools.combinations(range(len(F)),2):
  c,d=F[j],F[k]
  for satA,satB in itertools.product((0,1),repeat=2):
   demands={};ok=True
   for clause,extreme in ((c,satA),(d,satB)):
    for l in clause:
     v=abs(l);val=int(l>0) if extreme else int(l<0)
     if v in demands and demands[v]!=val:ok=False
     demands[v]=val
   same=any(l in d for l in c);opp=any(-l in d for l in c)
   prediction=not (opp if satA==satB else same)
   ck(ok==prediction,'independent SS/SU/US/UU original compatibility')
   counter+=1
 return counter

def main():
 for name,F in [('Y6',A6),('F9',A9),('F15',A15),('U198',U),('V198',V)]:ck(valid(F),name+' grammar')
 for malformed in [[],[(1,1,2)],[(1,2,3),(1,2,3)],[(1,-2,3)],[(1,2,3)],[(1,2,3),(-1,-2,-3)]]:ck(not valid(malformed),'malformed rejected')
 cases={};n_cubes=0
 controls={'Y6':(A6,{}),'F9_S':(A9,F9S),'F9_U':(A9,F9U),'F15_S':(A15,PS),'F15_U':(A15,PU),'U198':(U,{}),'V198':(V,{})}
 for name,(F,p) in controls.items():
  sg=slow_greedy(F,p)
  if sg is not None:
   logged=RAW['tests'][name];cc=logged['cycle_index'];ck(sg['cycles']==[list(x) for x in cc['cycles']],'greedy source triangle identity')
   ck(sg['E']==cc['E'] and sg['triangles']==cc['triangles'],'triangle counts')
   ck(sg['e']-sg['eta']-len(sg['cycles'])==logged['delta'],'saturation score')
  if len(F)<=20:
   a=source_models(F,p)
   if RAW['tests'][name]['exact_terminal']['label'] in ('SAT','UNSAT_AFFINE','UNSAT_GAP'):
    ck(len(a)==RAW['tests'][name]['exact_terminal']['count'],'source-model count')
   cases[name]={'models':len(a),'label':'SAT' if a else 'UNSAT'}
 # Independent all-assignment source model count and pair extremes, complement tests.
 expected={'Y6':20,'F9':70,'F15':1032}
 ssus={};endpoints={}
 for name,F in [('Y6',A6),('F9',A9),('F15',A15)]:
  ck(len(source_models(F,{}))==expected[name],'full canonical source models')
  ssus[name]=extremes(F)
  signed=RAW['signed_controls'][name]
  ck(len(signed['original_S_U_inversions'])==len(F),'one record for each original clause')
  for j,c in enumerate(F):
   rec=signed['original_S_U_inversions'][j]
   ck(rec['source_clause_id']==j,'original clause index unchanged')
   for v,l in zip(rec['occurrences'],c):
    ck(v['literal']==l and v['S']==int(l>0) and v['U']==int(l<0) and v['invert_S_U']==v['U'] and v['invert_U_S']==v['S'],'source-indexed local extrema')
  ck(len(signed['pair_compatibilities'])==len(F)*(len(F)-1)//2,'pair list complete')
  for j,k in itertools.combinations(range(len(F)),2):
   item=signed['pair_compatibilities'][j*(2*len(F)-j-1)//2+(k-j-1)]
   ck(item['source_clause_ids']==[j,k],'original pair IDs')
   for A,B in itertools.product(('S','U'),repeat=2):
    demand={};can=True
    for c,ext in ((F[j],A),(F[k],B)):
     for l in c:
      v=abs(l);b=int(l>0) if ext=='S' else int(l<0)
      if v in demand and demand[v]!=b:can=False
      demand[v]=b
    ck(item[A+B]==can,'every original pair compatibility mode')
  for mode in ('binary_flip_trail','gray_flip_trail'):
   last=None;total=0
   for frame in signed[mode]['frames']:
    mask=frame['global_mask']
    ts=[sum(((mask>>(abs(l)-1))&1)==int(l>0) for l in c) for c in F]
    histogram=[ts.count(r) for r in range(4)]
    ck(histogram==frame['histogram'],'actual globally consistent status profile')
    if last is not None:
     ids=[j for j,(a,b) in enumerate(zip(last,ts)) if a!=b]
     d=sum((a^b).bit_count() for a,b in zip(last,ts))
     ck(ids==frame['changed_clause_ids'] and d==frame['d_logic'],'original flip trail and logical XOR')
     total+=d
    last=ts
   ck(total==signed[mode]['sum_adjacent_d_logic'],'logical XOR sum over checkpoints')
  n=max(abs(l) for c in F for l in c)
  end=[]
  for bit in (0,1):
   a={i:bit for i in range(1,n+1)}
   H=collections.Counter(sum(a[abs(l)]==int(l>0) for l in c) for c in F)
   end.append([H[r] for r in range(4)])
  ck(end[0][r]==end[1][3-r] for r in range(4)) if False else None
  ck(all(end[0][r]==end[1][3-r] for r in range(4)),'literal complement counts')
  endpoints[name]=end
 # Independent exhaustive triangle and model count census for small cubes.
 for name,F,roots in [('Y6',A6,[{}]),('F15',A15,[PU,PS])]:
  stats=collections.Counter()
  for root in roots:
   free=[v for v in range(1,max(abs(x) for c in F for x in c)+1) if v not in root]
   for choices in itertools.product((-1,0,1),repeat=len(free)):
    p={**root,**{v:b for v,b in zip(free,choices) if b!=-1}}
    sg=slow_greedy(F,p)
    if sg is None:stats['empty']+=1;continue
    stats['cubes']+=1;stats['all_triangles']+=sg['triangles']
    stats['old_comb_candidates']+=math.comb(sg['E'],3) if sg['E']>=3 else 0
    if sg['e']-sg['eta']-len(sg['cycles'])==0:
     stats['saturated_cubes']+=1;stats['saturated_models']+=len(source_models(F,p))
    n_cubes+=1
  ref=RAW['census'][name]
  for k,v in stats.items():ck(ref[k]==v,f'census {name} {k}')
 physical={name:replay(name,F) for name,F in [('F9SAT',A9),('U198UNSAT',U),('V198SAT',V)]}
 proof=certify_U198()
 data={'verifier':'no_producer_import_independent_source_logic_and_tape_replay','assertions':CHECK['checks'],
  'cases':cases,'endpoints':endpoints,'ssus':ssus,'independent_cubes':n_cubes,
  'physical':physical,'198_cert':proof,'result':'PASS','P_vs_NP':'OPEN'}
 (R/'independent302.json').write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
 print(json.dumps(data,indent=2)[:5500])
if __name__=='__main__':main()