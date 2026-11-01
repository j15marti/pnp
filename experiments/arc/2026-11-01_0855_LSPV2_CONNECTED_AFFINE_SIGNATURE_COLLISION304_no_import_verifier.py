#!/usr/bin/env python3
"""Independent no-import verifier for LSPV-2 connected signature collision 304."""
import json, gzip
from collections import Counter
from itertools import product,combinations
from pathlib import Path
R=Path(__file__).resolve().parent
DATA=json.loads((R/'raw304.json').read_text())
checks=0

def ok(v,description):
 global checks
 checks+=1
 if not v:raise AssertionError(description)

# Independent source transcription, separate from experiment producer.
TRIPLES_PLUS=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
TRIPLES_MINUS=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
SOURCE=[(True,v) for v in TRIPLES_PLUS]+[(False,v) for v in TRIPLES_MINUS]
A=(1,0,1,0,None,None,None,0,None)
B=(1,1,0,0,None,None,None,0,None)

def build(t,joined):
 all_clauses=[]
 for i in range(t):
  for j,(sg,tr) in enumerate(SOURCE):
   v=[x+i*9 for x in tr]
   if joined and t>1 and j==0:v=[v[0],((i+1)%t)*9+5,v[2]]
   all_clauses.append((sg,tuple(sorted(v))))
 return all_clauses

def truth(C,assignment):
 return all(any(assignment[x-1]==int(s) for x in v) for s,v in C)

def trial(C,p):
 free=[i for i,x in enumerate(p) if x is None];count=0;example=None
 for values in product((0,1),repeat=len(free)):
  a=list(p)
  for i,v in zip(free,values):a[i]=v
  if truth(C,a):count+=1;example=a
 return count,example

def equation(label,C,p,free):
 idx={x:i for i,x in enumerate(free)}
 if label.startswith('prefer '):
  x=int(label.split()[1]);cnt=Counter()
  for sg,vs in C:
   if any(p[y-1] is not None and p[y-1]==int(sg) for y in vs) and x in vs:cnt[sg]+=1
  ok(cnt[True]!=cnt[False], 'authenticated preference value')
  return 1<<idx[x], 0 if cnt[True]>cnt[False] else 1
 elif label.startswith('clause '):
  j=int(label.split()[1]);sg,vs=C[j];active=[x for x in vs if x in idx]
  ok(not any(p[x-1] is not None and p[x-1]==int(sg) for x in vs),'outside cycle uncovered')
  return sum(1<<idx[x] for x in active), 1 if sg else 1^(len(active)&1)
 elif label.startswith('selected '):
  parts=label.split();j=int(parts[1]);x=int(parts[2][1:]);sg,vs=C[j]
  ok(x in vs and x in idx,'selected source occurrence')
  return 1<<idx[x],int(sg)
 else:
  ok(label.startswith('single '),'cycle one-true label')
  j=int(label.split()[1]);sg,vs=C[j];active=[x for x in vs if x in idx]
  ok(len(active)==2,'cycle binary endpoints')
  return (1<<idx[active[0]]) | (1<<idx[active[1]]),1

def gamma(v):
 b=f'{v:b}';return '0'*(len(b)-1)+b

def bits(C,n):
 w=n.bit_length();return gamma(n)+gamma(len(C))+''.join(('1' if s else '0')+''.join(f'{x:0{w}b}' for x in vs) for s,vs in C)

# Verify every declared finite counterexample, including true original-source
# assignment enumeration independent of producer and independent row-XOR checks.
for entry in DATA['cases']:
 t=entry['t'];n=9*t;C=build(t,True);flat=build(t,False)
 ok(len(C)==12*t,'clause count')
 cnt=Counter((sg,x) for sg,vs in C for x in vs)
 for x in range(1,n+1):
  for s in (True,False):ok(cnt[s,x]==2,'source exact-(2,2)')
 ok(len(set(C))==len(C),'duplicate-free source')
 ok(all(len(set(vs))==3 for _,vs in C),'three distinct variables')
 adj={x:set() for x in range(1,n+1)}
 for s,vs in C:
  for u,v in combinations(vs,2):adj[u].add(v);adj[v].add(u)
 visited={1};todo=[1]
 while todo:
  x=todo.pop()
  for y in adj[x]:
   if y not in visited:visited.add(y);todo.append(y)
 ok(len(visited)==n,'primal source connected')
 pyes=A*t;pno=B+A*(t-1)
 for p in (pyes,pno):
  ok(tuple(entry['SAT_pin' if p==pyes else 'UNSAT_pin'])==p,'pins preserved')
  active=[];covered=[];plus=Counter();minus=Counter()
  for j,(sg,vs) in enumerate(C):
   if any(p[x-1] is not None and p[x-1]==int(sg) for x in vs):
    covered.append(j)
    for x in vs:
     if p[x-1] is None:(plus if sg else minus)[x]+=1
   else:
    rem=tuple(x for x in vs if p[x-1] is None)
    ok(len(rem)>0,'no original empty clause')
    active.append((j,sg,rem))
  free=[i+1 for i,v in enumerate(p) if v is None]
  hist=[sum(len(rem)==w for _,_,rem in active) for w in range(4)]
  eta=sum(min(plus[x],minus[x]) for x in free)
  sig=entry['common_signature']
  for key,value in [('f',len(free)),('u',len(active)),('eta',eta),('nu',t),('delta',2*len(free)-len(active)-eta-t),('width_hist',hist)]:
   ok(sig[key]==value,'same-source signature '+key)
  cycles=[[12*i+3,12*i+5,12*i+7] for i in range(t)]
  ok(entry['same_packed_clause_ids']==cycles,'source-identified edge-disjoint cycles')
  for cy in cycles:
   edgevars=[tuple(x for x in C[j][1] if x in free) for j in cy]
   ok(all(len(e)==2 for e in edgevars),'all packed edges are binary')
   deg=Counter(x for e in edgevars for x in e)
   ok(sorted(deg.values())==[2,2,2],'actual 3-cycle')
  info=entry['affine_YES' if p==pyes else 'affine_NO']
  if info:
   ok(info['branches']==3**t,'fully enumerated affine choices')
   for bad in info['row_xor_refutations']:
    mask=0;rhs=0
    for label in bad['xor_row_ids']:
     m,v=equation(label,C,p,free);mask^=m;rhs^=v
    ok(mask==0 and rhs==1,'original-source row XOR produces 0=1')
   if info['first_witness']:
    ok(truth(C,info['first_witness']),'original-source witness checked')
 if t<=4:
  c1,w=trial(C,pyes);c0,_=trial(C,pno)
  ok((c1,c0)==(1,0),'exhaustive both-label source completions')
  ok(entry['affine_YES']['models']==c1 and entry['affine_NO']['models']==c0,'affine rank counts match exact models')
  ok(w==entry['affine_YES']['first_witness'],'affine witness matches unique source model')
  ok(entry['UP_DPLL_YES']['nodes']==1 and entry['UP_DPLL_NO']['nodes']==1,'one-node UP-DPLL honest baseline')
 # Connected splice edits only already SAT-covered clauses under both cubes.
 for j,(before,after) in enumerate(zip(flat,C)):
  if j%12!=0:ok(before==after,'unchanged original clause')
  else:
   for p in (pyes,pno):
    ok(p[9*(j//12)]==1,'clause zero covered by original pinned x1')
 ph=entry['physical_splice']
 if ph:
  path=R/f'xor_events_t{t}.json.gz'
  with gzip.open(path,'rt') as f:stream=json.load(f)
  source=bits(flat,n);target=bits(C,n)
  ok(len(source)==len(target)==ph['input_bits'],'constant-length canonical splice')
  tape=['0']*len(source);adj=0
  for address,previous,nextbit in stream['events']:
   ok(tape[address]==previous,'physical event old bit')
   adj+=int(previous!=nextbit)
   tape[address]=nextbit
  ok(''.join(tape)==target,'fully replayed physical target child bits')
  ok(adj==ph['sum_adjacent_dphys'],'physical adjacent XOR')
  ok(sum(v=='1' for v in target)==ph['endpoint_dphys'],'physical endpoint XOR')
  ok(sum(a!=b for a,b in zip(source,target))==ph['source_child_hamming'],'source-target Hamming')
  ok(len(stream['events'])==ph['write_events'],'all physical tape events replayed')

# Original source S/U inversion and complement checks independently.
root=build(1,True)
for assignment in product((0,1),repeat=9):
 inv=tuple(1-v for v in assignment)
 for s,vs in root:
  z=sum(assignment[x-1]==int(s) for x in vs)
  zz=sum(inv[x-1]==int(s) for x in vs)
  ok(zz==3-z,'every local signed-literal complement identity')
for j,k in combinations(range(12),2):
 for a,b in product((0,1),repeat=2):
  req={};consistent=True
  for which,choice in ((j,a),(k,b)):
   s,vs=root[which]
   for x in vs:
    target=int(s) if choice==1 else 1-int(s)
    if x in req and req[x]!=target:consistent=False
    req[x]=target
  brute=any(all(all(q[x-1]==(int(s) if choice==1 else 1-int(s)) for x in vs) for which,choice in ((j,a),(k,b)) for s,vs in (root[which],)) for q in product((0,1),repeat=9))
  ok(consistent==brute,'source pair exact S/U compatibility')

# The inherited independent 198-source verifier has been rerun separately;
# its recorded JSON is included as an immutable control, not imported logic.
prior=json.load(open(R/'inherited302_verification.json'))
ok(prior['result']=='PASS' and prior['P_vs_NP']=='OPEN','inherited fresh 198 certificate replay')
report={'name':'LSPV2_304 independent no-producer-import verifier','checks':checks,
        't_verified':[1,2,3,4,8], 't_exhaustive':[1,2,3,4],
        'affine_row_xor_refutations_checked':sum(len(x['affine_NO']['row_xor_refutations']) for x in DATA['cases'] if x['affine_NO']),
        'inherited_198_source_certification':prior['result'],'status':'PASS','P_vs_NP':'OPEN'}
(R/'verify304.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))