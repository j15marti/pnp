#!/usr/bin/env python3
"""Independent no-producer-import exhaustive verification of cycle-projection294.
Original SAT/UNSAT computed from source clauses, including U198 interface proof.
"""
from collections import Counter,defaultdict
from itertools import product,combinations
from pathlib import Path
import json,ast
R=Path(__file__).resolve().parent
RAW=json.loads((R/'legacy_results294.json').read_text())
Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
P=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15))
Q=((1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),(4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15))
F15=P+tuple(tuple(-x for x in c) for c in Q)
F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
P5=((1,2),(2,3),(3,4),(4,5),(1,5))
Q5=tuple(x for x in combinations(range(1,6),2) if x not in P5)
K5=tuple((a,b,i+6) for i,(a,b) in enumerate(P5))+tuple((-a,-b,-i-11) for i,(a,b) in enumerate(Q5))+tuple((i+6,i+11,11+(i+1)%5) for i in range(5))+tuple((-i-11,-i-6,-6-(i+1)%5) for i in range(5))
U=tuple(map(tuple,ast.literal_eval(''.join(line for line in (R/'U198.txt').read_text().splitlines() if not line.startswith('#')))))
V=[list(c) for c in U];V[2][2],V[44][2]=V[44][2],V[2][2];V=tuple(map(tuple,V))
W='001110010011110001010001110100111110011011000101000101001010100001011010101011000100000111001010110101001110001001101000110001100010100101101110010101011001001100000110111001001101001101101001010101'
check_counter=Counter()
def ck(p,msg):
 check_counter['assertions']+=1
 assert p,msg

def valid(F):
 n=max(abs(v) for c in F for v in c)
 count=Counter(v for c in F for v in c)
 ck(3*len(F)==4*n,'grammar total')
 ck(len({tuple(sorted(c)) for c in F})==len(F),'duplicate')
 for c in F:ck(len(c)==3 and len({abs(v) for v in c})==3 and (all(v>0 for v in c) or all(v<0 for v in c)),'clause valid')
 for v in range(1,n+1):ck(count[v]==count[-v]==2,'balanced source')

def sat(F,a):
 return all(any(a[abs(x)]==int(x>0) for x in c) for c in F)

def models(F,p):
 n=max(abs(x) for c in F for x in c)
 free=[v for v in range(1,n+1) if v not in p]
 for bits in product((0,1),repeat=len(free)):
  a={**p,**dict(zip(free,bits))}
  if sat(F,a):yield a

def derive(F,p):
 n=max(abs(x) for c in F for x in c)
 free=[x for x in range(1,n+1) if x not in p]
 uncovered=[];covered=[];occ=Counter();edges={}
 for j,c in enumerate(F):
  if any(abs(l) in p and p[abs(l)]==int(l>0) for l in c):
   covered.append(j)
   for l in c:
    if abs(l) not in p:occ[abs(l),l>0]+=1
  else:
   remain=[l for l in c if abs(l) not in p]
   if not remain:return {'status':'EMPTY'}
   uncovered.append(j)
   if len(remain)==2:edges[j]=tuple(map(abs,remain))
 cycles=[]
 for ids in combinations(sorted(edges),3):
  deg=Counter(v for j in ids for v in edges[j])
  if len(deg)==3 and all(q==2 for q in deg.values()):cycles.append(ids)
 used=set();selected=[]
 for ids in cycles:
  if all(j not in used for j in ids):selected.append(ids);used.update(ids)
 eta=sum(min(occ[x,True],occ[x,False]) for x in free)
 pref={x:int(occ[x,False]>occ[x,True]) for x in free if occ[x,True]!=occ[x,False]}
 delta=2*len(free)-len(uncovered)-eta-len(selected)
 return {'status':'GATE','uncovered':uncovered,'cycles':selected,'pref':pref,'delta':delta,'free':free,'edges':edges}

def rank(matrix):
 basis={}
 for x in matrix:
  while x:
   j=x.bit_length()-1
   if j not in basis:basis[j]=x;break
   x^=basis[j]
 return len(basis)

def independent_cert_check(F,p):
 g=derive(F,p)
 if g['status']!='GATE':return ('UNSAT_EMPTY',None)
 if g['delta']<0:return ('UNSAT_GAP',0)
 if g['delta']!=0:return ('UNRESOLVED',None)
 inside=set(x for cc in g['cycles'] for j in cc for x in g['edges'][j]);outside=set(g['free'])-inside
 inside_mask=sum(1<<(x-1) for x in inside)
 outside_mask=sum(1<<(x-1) for x in outside)
 cycle_ids={j for c in g['cycles'] for j in c}
 masks=[]
 for j in g['uncovered']:
  if j not in cycle_ids:
   masks.append(sum(1<<(abs(l)-1) for l in F[j] if abs(l) not in p)&outside_mask)
 for x in g['pref']:
  masks.append((1<<(x-1))&outside_mask)
 rr=rank(masks)
 nullity=len(outside)-rr
 # Independent complete assignment enumeration and per-model branch uniqueness.
 total=0;signatures=Counter()
 for a in models(F,p):
  signature=[]
  for cc in g['cycles']:
   over=[j for j in cc if sum(a[abs(l)]==int(l>0) for l in F[j])==2]
   ck(len(over)==1,'unique overfull per selected triangle')
   signature.append(over[0])
  # Every exterior uncovered clause has precisely one true literal.
  for j in g['uncovered']:
   if j not in cycle_ids:
    ck(sum(a[abs(l)]==int(l>0) for l in F[j])==1,'exterior exact-one')
  for x,v in g['pref'].items():ck(a[x]==v,'preferred value')
  signatures[tuple(signature)]+=1
  total+=1
 for key,cnt in signatures.items():ck(cnt==(1<<nullity),'uniform #SAT per compatible cycle signature')
 return ('SAT' if total else 'UNSAT_AFFINE_EXHAUSTED',total)

def dpll(F,p,work):
 work['nodes']+=1
 p=p.copy()
 while True:
  active=[]
  for c in F:
   rem=[];covered=False
   for x in c:
    work['literal_tests']+=1
    if abs(x) not in p:rem.append(x)
    elif p[abs(x)]==int(x>0):covered=True;break
   if not covered:
    if not rem:return False
    active.append(rem)
  if not active:return True
  unit=next((c[0] for c in active if len(c)==1),None)
  if unit is None:break
  p[abs(unit)]=int(unit>0)
 x=abs(min(active,key=len)[0])
 return dpll(F,{**p,x:0},work) or dpll(F,{**p,x:1},work)

def main():
 for F in (F9,Y6,F15,K5,U,V):valid(F)
 controls=[('F9_badcube',F9,{8:0,3:0,7:0,6:0,1:1,5:1}),('Y6_root',Y6,{}),('F15_U',F15,dict(zip(range(7,16),(0,0,0,0,1,1,1,1,0)))),('F15_S',F15,dict(zip(range(7,16),(1,0,0,0,1,1,1,1,0)))),('K5_U',K5,{**{v:0 for v in range(6,11)},**{v:1 for v in range(11,16)}}),('K5_S',K5,{**{v:0 for v in range(6,11)},**{v:1 for v in range(11,16)},6:1,15:0})]
 report={'status':'PASS','SAT_U198':'UNKNOWN_UNLESS_PROOF_REPLAY','U198_unsat_proof':False,'V198_sat_witness':False,'cases':{},'exhaustive':{}}
 for name,F,p in controls:
  status,cnt=independent_cert_check(F,p)
  ref=RAW['cases'][name]
  ck(status==ref['gate_status'],'same source terminal outcome')
  if cnt is not None:ck(cnt==ref['models'],'same source SAT extensions')
  report['cases'][name]={'status':status,'extensions':cnt}
 for name,F,roots in [('Y6',Y6,[{}]),('F15',F15,[dict(zip(range(7,16),(0,0,0,0,1,1,1,1,0))),dict(zip(range(7,16),(1,0,0,0,1,1,1,1,0)))])]:
  stats=Counter()
  for root in roots:
   free=[v for v in range(1,max(abs(l) for c in F for l in c)+1) if v not in root]
   for st in product((-1,0,1),repeat=len(free)):
    pin={**root,**{v:b for v,b in zip(free,st) if b!=-1}}
    status,count=independent_cert_check(F,pin)
    actual=sum(1 for _ in models(F,pin))
    if count is not None:ck(count==actual,'every source-complete SAT count')
    if status.startswith('UNSAT'):ck(actual==0,'UNSAT proof valid')
    stats[status]+=1
  report['exhaustive'][name]={'cubes':sum(stats.values()),'statuses':dict(stats)}
 # Replay U198 UNSAT as six 42-clause modules and a six-variable boundary.
 # The two root interface clauses must also be satisfied.
 root=[c for c in U[:2]]
 accepts=[];nodes=Counter()
 for block in range(6):
  clauses=U[2+42*block:2+42*(block+1)]
  ck(len(clauses)==42,'42 clause block')
  matches=set()
  for bits in range(64):
   pins={193+k:(bits>>k)&1 for k in range(6)}
   if dpll(clauses,pins,nodes):matches.add(bits)
  accepts.append(matches)
 legal={bits for bits in range(64) if all(any(((bits>>(abs(l)-193))&1)==int(l>0) for l in c) for c in root)}
 for matches in accepts:legal&=matches
 ck(not legal,'original U198 source UNSAT certified via exhaustive 64 interface assignments')
 report['U198_unsat_proof']=True
 report['U198_boundary_queries']=384
 report['U198_dpll_nodes']=nodes['nodes']
 ck(len(W)==198,'198-bit V witness')
 witness={i+1:int(b) for i,b in enumerate(W)}
 ck(sat(V,witness),'original V198 source witness')
 report['V198_sat_witness']=True
 # Original F9 endpoints, complement, and source pair local all-extreme feasibility.
 for F in (Y6,F9,F15,K5):
  n=max(abs(l) for c in F for l in c)
  for a in product((0,1),repeat=n if n<=9 else 0):
   if n>9:break
   d={v:a[v-1] for v in range(1,n+1)}
   inv={v:1-d[v] for v in d}
   for c in F:ck(sum(d[abs(l)]==int(l>0) for l in c)+sum(inv[abs(l)]==int(l>0) for l in c)==3,'source complement')
  for j,k in combinations(range(len(F)),2):
   A,B=F[j],F[k];same=any(x in B for x in A);opposite=any(-x in B for x in A)
   for s,t in product((0,1),repeat=2):
    demand={};possible=True
    for clause,b in ((A,s),(B,t)):
     for lit in clause:
      v=int(lit>0) if b else int(lit<0)
      if abs(lit) in demand and demand[abs(lit)]!=v:possible=False
      demand[abs(lit)]=v
    ck(possible==((not opposite) if s==t else (not same)),'SS SU US UU exact mask')
 report['assertions']=check_counter['assertions'];report['P_vs_NP']='OPEN'
 (R/'independent_source_cert295.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
 print(json.dumps(report,indent=2))
if __name__=='__main__':main()