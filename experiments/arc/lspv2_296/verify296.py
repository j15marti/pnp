#!/usr/bin/env python3
"""Independent no-producer-import audit of LSPV-2 overlap frontier DP 296.

Finite controls are directly enumerated from original clauses and independent
triangle/choice constructions.  Physical events replay from zeroed cell tapes.
This is not native FLMV-machine simulation or universal SAT proof.
"""
from itertools import product,combinations
from collections import Counter
from pathlib import Path
import json,ast,gzip,hashlib,math
R=Path(__file__).resolve().parent
RAW=json.loads((R/'results296.json').read_text())
Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
P9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
N9=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
F9=P9+tuple(tuple(-v for v in c) for c in N9)
P15=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15))
Q15=((1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),(4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15))
F15=P15+tuple(tuple(-v for v in c) for c in Q15)
P5=((1,2),(2,3),(3,4),(4,5),(1,5))
Q5=tuple(e for e in combinations(range(1,6),2) if e not in P5)
K5=tuple((u,v,6+i) for i,(u,v) in enumerate(P5))+tuple((-u,-v,-11-i) for i,(u,v) in enumerate(Q5))+tuple((6+i,11+i,11+(i+1)%5) for i in range(5))+tuple((-(11+i),-(6+i),-(6+(i+1)%5)) for i in range(5))
U=tuple(tuple(c) for c in ast.literal_eval(''.join(x for x in (R/'U198.txt').read_text().splitlines() if not x.startswith('#'))))
V=[list(c) for c in U];V[2][2],V[44][2]=V[44][2],V[2][2];V=tuple(map(tuple,V))
P9_PIN={8:0,3:0,7:0,6:0,1:1,5:1}
P15_U=dict(zip(range(7,16),(0,0,0,0,1,1,1,1,0)))
P15_S=dict(zip(range(7,16),(1,0,0,0,1,1,1,1,0)))
K5_U={**{v:0 for v in range(6,11)},**{v:1 for v in range(11,16)}}
K5_S={**K5_U,6:1,15:0}
checks=Counter()
def ck(z,msg):
 checks['assertions']+=1
 assert z,msg

def grammar(F):
 n=max(abs(l) for c in F for l in c)
 count=Counter(l for c in F for l in c)
 ck(3*len(F)==4*n,'global 2P2N count')
 ck(len(F)==len({tuple(sorted(c)) for c in F}),'duplicate clauses')
 for c in F:ck(len(c)==3 and len(set(map(abs,c)))==3 and (all(x>0 for x in c) or all(x<0 for x in c)),'proper clause')
 for v in range(1,n+1):ck(count[v]==count[-v]==2,'signed occurrences')
 return n

def sat(F,a):return all(any(a[abs(x)]==int(x>0) for x in c) for c in F)

def assignments(F,p):
 n=max(abs(v) for c in F for v in c)
 free=[v for v in range(1,n+1) if v not in p]
 for bits in product((0,1),repeat=len(free)):
  a={**p,**dict(zip(free,bits))}
  yield a

def choose_cycles(F,p):
 covered=set();uncovered=[];residual={}
 for j,c in enumerate(F):
  if any(abs(x) in p and p[abs(x)]==int(x>0) for x in c):covered.add(j)
  else:
   r=[x for x in c if abs(x) not in p]
   if not r:return None
   uncovered.append(j);residual[j]=r
 edges={j:tuple(map(abs,r)) for j,r in residual.items() if len(r)==2}
 tris=[]
 for cc in combinations(sorted(edges),3):
  deg=Counter(x for j in cc for x in edges[j])
  if len(deg)==3 and all(deg[x]==2 for x in deg):tris.append(cc)
 used=set();chosen=[]
 for cc in tris:
  if not any(j in used for j in cc):chosen.append(cc);used.update(cc)
 # Reconstruct signed-spill conservation delta independently.
 free=set(range(1,grammar(F)+1))-set(p)
 s=Counter()
 for j in covered:
  for x in F[j]:
   if abs(x) in free:s[abs(x),int(x>0)]+=1
 eta=sum(min(s[x,0],s[x,1]) for x in free)
 delta=2*len(free)-len(uncovered)-eta-len(chosen)
 return delta,chosen,uncovered

def choices_for_cycle(F,p,cycle):
 edges=[]
 for j in cycle:
  r=[x for x in F[j] if abs(x) not in p]
  ck(len(r)==2,'cycle only binary')
  edges.append((j,abs(r[0]),abs(r[1]),int(r[0]>0)))
 opts=[]
 for selected,u,v,sign in edges:
  assignments={u:sign,v:sign};change=True
  while change:
   change=False
   for j,a,b,z in edges:
    if j==selected:continue
    if a in assignments and b not in assignments:
     assignments[b]=1-assignments[a];change=True
    if b in assignments and a not in assignments:
     assignments[a]=1-assignments[b];change=True
  ck(all(a in assignments and b in assignments for _,a,b,_ in edges),'cycle fully assigned')
  ck(all((assignments[a]==assignments[b]==z) if j==selected else (assignments[a]!=assignments[b]) for j,a,b,z in edges),'unique overfull')
  opts.append((selected,assignments))
 return opts

def direct_choice_count(F,p):
 gate=choose_cycles(F,p)
 if gate is None:return None
 delta,cycles,uncovered=gate
 if delta!=0:return None
 # Strict exhaustive cycle-choice independent of DP and projection method.
 options=[choices_for_cycle(F,p,c) for c in cycles]
 valid_signatures=Counter();bad_overlap=0
 for combination in product(*options):
  assigned=dict(p);correct=True
  for chosen,extension in combination:
   for var,val in extension.items():
    if var in assigned and assigned[var]!=val:correct=False;break
    assigned[var]=val
   if not correct:break
  if not correct:bad_overlap+=1;continue
  free=[v for v in range(1,grammar(F)+1) if v not in assigned]
  for bits in product((0,1),repeat=len(free)):
   complete={**assigned,**dict(zip(free,bits))}
   if sat(F,complete):valid_signatures[tuple(selected for selected,_ in combination)]+=1
 return sum(valid_signatures.values()),len(valid_signatures),bad_overlap,len(cycles)

def gam(k):
 s=bin(k)[2:]
 return '0'*(len(s)-1)+s

def encode(F):
 n=max(abs(x) for c in F for x in c);w=n.bit_length()
 return gam(n)+gam(len(F))+''.join(('0' if c[0]>0 else '1')+''.join(format(abs(x),f'0{w}b') for x in c) for c in F)

def physical_replay(F,child,name):
 src=encode(F);target=encode(child)
 files=R/(name+'_canonical_emit_events296.jsonl.gz')
 reg={'source_address':[0]*max(1,(max(len(src),len(target))+1).bit_length()),
      'output_cursor':[0]*max(1,(max(len(src),len(target))+1).bit_length()),
      'output':[0]*len(target)}
 ones=0;events=0;source_reads=0;writes=0
 with gzip.open(files,'rt') as f:
  for line in f:
   z=json.loads(line);events+=1
   ck(z['step']==events,'contiguous recorded events')
   if z.get('kind')=='read_only_source':
    idx=z['source_index'];ck(0<=idx<len(src),'source range')
    ck(sum(bit<<i for i,bit in enumerate(reg['source_address']))==idx,'source address register')
    ck(z['d_phys']==0,'read-only source does not write')
    source_reads+=1;continue
   tape=z['tape'];idx=z['cell'];before=z['before'];after=z['after']
   ck(reg[tape][idx]==before,'actual old stored bit')
   ck(z['d_phys']==int(before!=after),'actual adjacent physical XOR')
   reg[tape][idx]=after;ones+=z['d_phys'];writes+=1
 ck(''.join(map(str,reg['output']))==target,'exact output tape')
 ck(source_reads==len(src),'exact source reads')
 truth=RAW['cases'][name]['child']['physical']
 ck(truth['physical_xor_sum']==ones and truth['endpoint_physical_xor']==sum(map(sum,reg.values())),'physical replay aggregates')
 ck(truth['total_events']==events and truth['register_write_events']+truth['output_writes']==writes,'physical full event count')
 return {'event_count':events,'changed_bits':ones,'endpoint':sum(map(sum,reg.values())),'source_bits':source_reads,'output_bits':len(target)}

def main():
 corpus={'F9_BAD_CUBE':(F9,P9_PIN),'Y6_ROOT':(Y6,{}),'F15_PIN_U':(F15,P15_U),'F15_PIN_S':(F15,P15_S),
         'K5_PIN_U':(K5,K5_U),'K5_PIN_S':(K5,K5_S),'U198_ROOT':(U,{}),'V198_ROOT':(V,{})}
 out={'verifier':'independent_no_producer_import_original_source_full_enumeration','controls':{},'cube_checks':{},'physical':{},'status':'PASS','P_vs_NP':'OPEN'}
 for name,(F,p) in corpus.items():
  n=grammar(F)
  ck(hashlib.sha256(encode(F).encode()).hexdigest()==RAW['source_hashes'][name],'source bytes identical')
  terminal=RAW['cases'][name]
  if n<=15:
   c=sum(sat(F,a) for a in assignments(F,p))
   if terminal['terminal_status']=='SAT':ck(terminal['models']==c,'source extension count')
   if terminal['terminal_status'].startswith('UNSAT'):ck(c==0,'UNSAT means zero extensions')
   if terminal['witness'] is not None:
    w={i+1:v for i,v in enumerate(terminal['witness'])}
    ck(sat(F,w) and all(w[i]==b for i,b in p.items()),'source checked witness')
   direct=direct_choice_count(F,p)
   if direct is not None:
    ck(direct[0]==c,'independent cycle-choice exact count')
    out['controls'][name]={'source_sat_models':c,'cycle_signatures':direct[1],
                           'overlap_rejections':direct[2],'cycles':direct[3]}
   else:out['controls'][name]={'source_sat_models':c,'exact_gate_not_applicable':True}
   if name=='K5_PIN_S':ck(direct[2]==4,'overlap rejects four choices')
  else:out['controls'][name]={'source_status':'certified by separate U198 boundary/V198 witness replay'}
 stats=Counter()
 for name,F,roots in [('Y6',Y6,[{}]),('F15',F15,[P15_U,P15_S])]:
  for root in roots:
   free=[v for v in range(1,grammar(F)+1) if v not in root]
   for seq in product((-1,0,1),repeat=len(free)):
    p={**root,**{v:b for v,b in zip(free,seq) if b!=-1}}
    gate=choose_cycles(F,p)
    if gate is None:continue
    if gate[0]!=0:continue
    oracle=sum(sat(F,a) for a in assignments(F,p))
    got=direct_choice_count(F,p)
    ck(got is not None and got[0]==oracle,'disjoint signed-source affine union on every saturated cube')
    stats[name,'saturated']+=1;stats[name,'models']+=oracle
  ck(stats[name,'saturated']==RAW['exhaustive'][name]['saturated'],'same source saturated count')
 out['cube_checks']={x:{'saturated_cubes':stats[x,'saturated'],'source_models':stats[x,'models']} for x in ('Y6','F15')}
 for name,child in [('F9_BAD_CUBE',U),('F15_PIN_S',Y6),('K5_PIN_S',Y6),('U198_ROOT',U),('V198_ROOT',Y6),('Y6_ROOT',Y6)]:
  out['physical'][name]=physical_replay(corpus[name][0],child,name)
 # Grammar and complement controls on every stored small source.
 for name,(F,p) in corpus.items():
  n=grammar(F)
  zero={v:0 for v in range(1,n+1)};one={v:1 for v in range(1,n+1)}
  for c in F:
   ck(sum(zero[abs(x)]==int(x>0) for x in c)+sum(one[abs(x)]==int(x>0) for x in c)==3,'complement true-literal counts')
  for j,k in combinations(range(len(F)),2):
   A,B=F[j],F[k];same=bool(set(A)&set(B));opp=bool(set(A)&{-x for x in B})
   for s,t in product((0,1),repeat=2):
    wants={};possible=True
    for c,b in ((A,s),(B,t)):
     for lit in c:
      val=int(lit>0) if b else int(lit<0)
      if abs(lit) in wants and wants[abs(lit)]!=val:possible=False
      wants[abs(lit)]=val
    ck(possible==(not opp if s==t else not same),'four-way original S/U extreme compatibility')
 out['assertions']=checks['assertions']
 (R/'independent296.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':main()