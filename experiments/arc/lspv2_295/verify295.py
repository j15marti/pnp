#!/usr/bin/env python3
"""Independent no-producer-import verification of K5 SOURCE SCC295.
Reconstructs all sources and directly replays source-indexed physical event files.
"""
from collections import Counter, defaultdict, deque
from itertools import combinations,product
from pathlib import Path
import ast, gzip, json
R=Path(__file__).resolve().parent
A=json.loads((R/'results295.json').read_text());PH=json.loads((R/'physical295.json').read_text())
N=Counter()
def ck(q,msg):
 N['assertions']+=1
 if not q:raise AssertionError(msg)

P=((1,2),(2,3),(3,4),(4,5),(1,5))
Q=tuple(e for e in combinations(range(1,6),2) if e not in P)
K=tuple((u,v,6+i) for i,(u,v) in enumerate(P))+tuple((-u,-v,-11-i) for i,(u,v) in enumerate(Q))+tuple((6+i,11+i,11+(i+1)%5) for i in range(5))+tuple((-(11+i),-(6+i),-(6+(i+1)%5)) for i in range(5))
Y=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
P15=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15))
Q15=((1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),(4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15))
F15=P15+tuple(tuple(-l for l in c) for c in Q15)
PU={**{v:0 for v in range(6,11)},**{v:1 for v in range(11,16)}}
PS={**PU,6:1,15:0}
P9={8:0,3:0,7:0,6:0,1:1,5:1}
P15U=dict(zip(range(7,16),(0,0,0,0,1,1,1,1,0)))
P15S=dict(zip(range(7,16),(1,0,0,0,1,1,1,1,0)))
U=tuple(map(tuple,ast.literal_eval(''.join(line for line in (R/'U198.txt').read_text().splitlines() if not line.startswith('#')))))
V=[list(c) for c in U];V[2][2],V[44][2]=V[44][2],V[2][2];V=tuple(map(tuple,V))
W='001110010011110001010001110100111110011011000101000101001010100001011010101011000100000111001010110101001110001001101000110001100010100101101110010101011001001100000110111001001101001101101001010101'

def valid(f):
 counts=Counter(l for c in f for l in c)
 n=max(abs(l) for c in f for l in c)
 ck(len(f)*3==4*n,'m n constraint')
 ck(len(set(tuple(sorted(c)) for c in f))==len(f),'duplicate')
 for c in f:ck(len(c)==3 and len(set(map(abs,c)))==3 and (all(l>0 for l in c) or all(l<0 for l in c)),'monotone proper')
 for x in range(1,n+1):ck(counts[x]==counts[-x]==2,'balanced sign')
 return True

def sat(f,a):return all(any(a[abs(l)]==int(l>0) for l in c) for c in f)
def models(f,p):
 n=max(abs(l) for c in f for l in c);free=[v for v in range(1,n+1) if v not in p]
 return sum(sat(f,{**p,**dict(zip(free,b))}) for b in product((0,1),repeat=len(free)))

def certificate(f,p,rec):
 ck(rec['status']=='UNSAT_K5','correct status')
 vs=rec['vertices'];ids=rec['source_clause_ids']
 ck(len(vs)==5 and len(set(vs))==5 and len(ids)==10 and len(set(ids))==10,'motif size')
 incidence=Counter();pairs=set();pos=set();neg=set();arcs=set()
 for j in ids:
  c=f[j]
  ck(not any(abs(l) in p and p[abs(l)]==int(l>0) for l in c),'uncovered clause')
  r=[l for l in c if abs(l) not in p]
  ck(len(r)==2 and set(map(abs,r)).issubset(vs),'binary source row')
  x,y=r;a,b=sorted((abs(x),abs(y)))
  ck((a,b) not in pairs,'unique support pair')
  pairs.add((a,b));incidence[abs(x)]+=1;incidence[abs(y)]+=1
  if x>0:pos.add((a,b));ck(j in rec['positive_cycle_clause_ids'],'source sign plus')
  else:neg.add((a,b));ck(j in rec['negative_cycle_clause_ids'],'source sign minus')
  arcs.add((-x,y,j));arcs.add((-y,x,j))
 ck(pairs==set(combinations(vs,2)),'complete K5 source graph')
 ck(all(incidence[x]==4 for x in vs),'saturates original occurrence quotas')
 ck(all(sum(x in e for e in pos)==2 and sum(x in e for e in neg)==2 for x in vs),'both signs 2-regular')
 ck(len(pos)==len(neg)==5,'two distinct C5')
 # Independently check both C5s have no independent set of three.
 for sign_edges in (pos,neg):
  for three in combinations(vs,3):ck(any(set(e)<=set(three) for e in sign_edges),'5-cycle alpha2')
 paths=rec['implication_paths'];pivot=paths['pivot'];ck(pivot in vs,'pivot in motif')
 for key,start,end in [('positive_to_negative',pivot,-pivot),('negative_to_positive',-pivot,pivot)]:
  at=start;ck(len(paths[key])>0,'nonempty path')
  for u,v,j in paths[key]:ck(u==at and (u,v,j) in arcs,'source-indexed implication step');at=v
  ck(at==end,'path endpoint')
 for bits in product((0,1),repeat=5):
  a=dict(zip(vs,bits))
  ck(not all(any(a[abs(l)]==int(l>0) for l in f[j] if abs(l) in vs) for j in ids),'source K5 intrinsically UNSAT')
 return True

def gamma(n):
 b=bin(n)[2:];return '0'*(len(b)-1)+b

def encode(f):
 n=max(abs(l) for c in f for l in c);w=n.bit_length()
 return gamma(n)+gamma(len(f))+''.join(str(int(c[0]>0))+''.join(bin(abs(l))[2:].zfill(w) for l in c) for c in f)

def append(f):
 n=max(abs(l) for c in f for l in c)
 return tuple(f)+tuple(tuple((1 if l>0 else -1)*(n+abs(l)) for l in c) for c in Y)

def verify_trace(name,f):
 source=encode(append(f));child=encode(f);r=PH[name]
 ck(r['source_bits']==source and r['child_bits_string']==child,'independent source/child encoder')
 ni=max(abs(l) for c in append(f) for l in c);no=ni-6
 wp=ni.bit_length();wc=no.bit_length();mp=len(append(f));mc=len(f)
 hp=len(gamma(ni))+len(gamma(mp));hc=len(gamma(no))+len(gamma(mc))
 rp=1+3*wp;rc=1+3*wc
 ilen=max(1,(len(source)-1).bit_length());idx=[0]*ilen;out=[0]*len(child)
 ix=0;xor=0;unch=0;source_reads=0;sourcecl=set()
 with gzip.open(R/(name+'_physical_events295.jsonl.gz'),'rt') as g:
  def event(tape,cell,value):
   nonlocal ix,xor,unch
   record=json.loads(next(g));ar=idx if tape=='index' else out
   old=ar[cell];d=int(old!=value)
   ck(record==[tape,cell,old,value,d],'physical event exact replay and address check')
   ar[cell]=value;ix+=1;xor+=d;unch+=1-d
  for q,char in enumerate(child):
   if q<hc:b=int(char)
   else:
    rel=q-hc;j=rel//rc;k=rel%rc
    if k==0:address=hp+j*rp
    else:
     z=k-1;address=hp+j*rp+1+(z//wc)*wp+(wp-wc)+(z%wc)
    for t in range(ilen):event('index',t,(address>>t)&1)
    b=int(source[address]);source_reads+=1;sourcecl.add(j)
   ck(b==int(char),'output source-bit correctness')
   event('output',q,b)
  ck(g.read()=='','no extra physical event')
 ck(out==list(map(int,child)),'exact final child')
 ck(ix==r['physical_events'] and xor==r['dphys_sum'] and unch==r['unchanged_writes'],'exact event counts')
 ck(sum(idx)+sum(out)==r['dphys_endpoint'],'physical endpoint XOR')
 ck(source_reads==r['source_bit_reads'] and sourcecl==set(r['changed_original_clause_ids']),'exact original source ID use')
 return {'event_records':ix,'cumulative_xor':xor,'endpoint_xor':sum(idx)+sum(out)}

def verify_logical(name,f):
 source=json.loads((R/'logical295.json').read_text())[name]
 n=max(abs(x) for c in f for x in c)
 a=[0]*n
 def state(mode):
  packed=a[:]
  for c in f:
   q=sum(a[abs(l)-1]==int(l>0) for l in c)
   v=q^(q//2) if mode=='gray' else q
   packed.extend(((v//2)%2,v%2,int(q>0)))
  return packed
 before={mode:state(mode) for mode in ('binary','gray')}
 total={'binary':0,'gray':0}
 ck(source['step_count']==2*n,'full 0->1->0 trail')
 for z,step in enumerate(source['traces']):
  v=step['flipped_original_variable'];ck(v==(z+1 if z<n else 2*n-z),'variable flip order')
  expected_ids=[j for j,c in enumerate(f) if any(abs(l)==v for l in c)]
  ck(expected_ids==step['changed_source_clause_ids'] and len(expected_ids)==4,'source-indexed changed clauses')
  a[v-1]^=1
  for mode in ('binary','gray'):
   after=state(mode);count=sum(x!=y for x,y in zip(before[mode],after))
   ck(count==step['delta'][mode],'full aligned XOR between checkpoints')
   before[mode]=after;total[mode]+=count
 ck(all(v==0 for v in a),'restored initial assignment')
 ck(total==source['total_adjacent_logical_XOR'],'logical adjacent sums')
 ck(source['endpoint_logical_XOR']=={'binary':0,'gray':0},'restored endpoint zero')
 return total

def dpll(f,p,stats):
 stats['nodes']+=1;pin=p.copy()
 while True:
  unit=None;allhit=True;active=[]
  for c in f:
   rest=[];hit=False
   for l in c:
    stats['literal_tests']+=1
    if abs(l) not in pin:rest.append(l)
    elif pin[abs(l)]==int(l>0):hit=True;break
   if hit:continue
   allhit=False;active.append(rest)
   if not rest:return False
   if len(rest)==1:unit=rest[0];break
  if unit is None:
   if allhit:return True
   break
  pin[abs(unit)]=int(unit>0)
 x=abs(min(active,key=len)[0])
 return dpll(f,{**pin,x:0},stats) or dpll(f,{**pin,x:1},stats)

def main():
 for f in (K,Y,F9,F15,U,V):valid(f)
 cases={'K5_bad_cube':(K,PU),'K5_nearby_SAT_cube':(K,PS),'K5_full_SAT_root':(K,{}),
        'F9_bad_cube':(F9,P9),'Y6_root':(Y,{}),'F15_bad':(F15,P15U),'F15_SAT':(F15,P15S),'U198_UNSAT':(U,{}),'V198_SAT':(V,{})}
 for name,(f,p) in cases.items():
  claimed=A['cases'][name]
  if claimed['gate']['status']=='UNSAT_K5':certificate(f,p,claimed['gate'])
  if len(f)<25:ck(models(f,p)==claimed['models'],'independent same-source model count')
  ck(len(encode(f))==claimed['source_bits'],'binary source length')
 # Root SAT remains SAT despite a K5-pinned UNSAT branch.
 ck(models(K,{})==770 and models(K,PU)==0 and models(K,PS)==2,'SAT branch issue')
 # The full U source UNSAT proof is a conjunction of 64 boundary checked modules.
 root=U[:2];allowed=set()
 for bits in range(64):
  pin={193+i:(bits>>i)&1 for i in range(6)}
  if all(any(pin[abs(l)]==int(l>0) for l in c) for c in root):allowed.add(bits)
 queries=0;work=Counter()
 for block in range(6):
  b=U[2+42*block:2+42*(block+1)]
  ck(len(b)==42,'exact original U module size')
  possible=set()
  for bits in range(64):
   pin={193+i:(bits>>i)&1 for i in range(6)}
   queries+=1
   if dpll(b,pin,work):possible.add(bits)
  allowed&=possible
 ck(not allowed and queries==384,'original-source U198 UNSAT proof')
 ck(len(W)==198 and sat(V,{i+1:int(b) for i,b in enumerate(W)}),'V198 complete original witness')
 logical={label:verify_logical(label,f) for label,f in [('Y6',Y),('F9',F9),('F15K5',K),('U198',U),('V198',V)]}
 physical={label:verify_trace(label,f) for label,f in [('Y6plusY6_SAT',Y),('U198plusY6_UNSAT',U),('V198plusY6_SAT',V)]}
 ck(physical['U198plusY6_UNSAT']['cumulative_xor']==physical['V198plusY6_SAT']['cumulative_xor'],'matched opposite labels same XOR')
 # Independent strict-2P2N (nonmonotone) adversary: regular tournament.
 mutated=[list(c) for c in K]
 for j,c in enumerate(mutated[:10]):
  a,b=sorted(map(abs,c[:2]));sign_plus=a if (b-a)%5 in (1,2) else b
  mutated[j][:2]=[sign_plus,-(b if sign_plus==a else a)]
 mutated=tuple(map(tuple,mutated));cnt=Counter(l for c in mutated for l in c)
 ck(all(cnt[i]==cnt[-i]==2 for i in range(1,16)),'hostile strict22 quotas')
 witness={**PU,**{i:0 for i in range(1,6)}}
 ck(sat(mutated,witness),'hostile mixed-sign K5 must be SAT')
 verdict={'status':'PASS','assertions':N['assertions'],'K5_source_certificate':True,
  'original_U198_UNSAT_proof':True,'U198_boundary_queries':queries,
  'U198_DPLL_nodes':work['nodes'],'V198_witness':True,
  'root_K5_models':770,'K5_cube_models':0,'strict22_broader_SAT_adversary':True,
  'physical':physical,'logical':logical,'P_vs_NP':'OPEN'}
 (R/'independent295.json').write_text(json.dumps(verdict,indent=2,sort_keys=True)+'\n')
 print(json.dumps(verdict,indent=2))
if __name__=='__main__':main()
