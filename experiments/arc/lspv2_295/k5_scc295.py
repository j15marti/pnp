#!/usr/bin/env python3
"""LSPV-2 K5-SOURCE-SCC295: source-certified bounded-degree K5 UNSAT gate.
No arbitrary-SAT lower bound, no native FLMV measurement. Python 3.10+ stdlib.
"""
from __future__ import annotations
from collections import Counter, defaultdict, deque
from itertools import combinations, product
import ast, json, pathlib, sys
HERE=pathlib.Path(__file__).resolve().parent
P5=((1,2),(2,3),(3,4),(4,5),(1,5))
Q5=tuple(e for e in combinations(range(1,6),2) if e not in P5)
K5=tuple((u,v,6+i) for i,(u,v) in enumerate(P5))+tuple((-u,-v,-11-i) for i,(u,v) in enumerate(Q5))+tuple((6+i,11+i,11+(i+1)%5) for i in range(5))+tuple((-(11+i),-(6+i),-(6+(i+1)%5)) for i in range(5))
Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
F9_POS=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
F9_NEG=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
F9=F9_POS+tuple(tuple(-v for v in c) for c in F9_NEG)
F15_POS=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15))
F15_NEG=((1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),(4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15))
F15=F15_POS+tuple(tuple(-v for v in c) for c in F15_NEG)
PU={**{v:0 for v in range(6,11)},**{v:1 for v in range(11,16)}}
PS={**PU,6:1,15:0}
P9={8:0,3:0,7:0,6:0,1:1,5:1}
F15PU=dict(zip(range(7,16),(0,0,0,0,1,1,1,1,0)))
F15PS=dict(zip(range(7,16),(1,0,0,0,1,1,1,1,0)))

def source198():
 raw=''.join(line for line in (HERE/'U198.txt').read_text().splitlines() if not line.startswith('#'))
 U=tuple(map(tuple,ast.literal_eval(raw)))
 V=[list(c) for c in U]
 V[2][-1],V[44][-1]=V[44][-1],V[2][-1]
 return U,tuple(map(tuple,V))

def valid(F):
 if not isinstance(F,(tuple,list)) or not F:return False
 if any(not isinstance(c,(tuple,list)) or len(c)!=3 or any(type(v)!=int or v==0 for v in c) for c in F):return False
 n=max(abs(x) for c in F for x in c)
 if 3*len(F)!=4*n:return False
 if len(set(tuple(sorted(c)) for c in F))!=len(F):return False
 counts=Counter(l for c in F for l in c)
 return all(len({abs(x) for x in c})==3 and (all(x>0 for x in c) or all(x<0 for x in c)) for c in F) and all(counts[v]==counts[-v]==2 for v in range(1,n+1))

def gamma(k):
 b=format(k,'b');return '0'*(len(b)-1)+b

def encode(F):
 if not valid(F):raise ValueError('malformed canonical source')
 n=max(abs(x) for c in F for x in c);w=n.bit_length()
 return gamma(n)+gamma(len(F))+''.join(('1' if c[0]>0 else '0')+''.join(format(abs(l),'0%db'%w) for l in c) for c in F)

def decode(bits):
 if not isinstance(bits,str) or not bits or any(b not in '01' for b in bits):raise ValueError('nonbinary')
 pos=0
 def number():
  nonlocal pos
  begin=pos
  while pos<len(bits) and bits[pos]=='0':pos+=1
  k=pos-begin
  if pos>=len(bits) or pos+k>=len(bits):raise ValueError('truncated gamma')
  n=int(bits[pos:pos+k+1],2);pos+=k+1
  return n
 n=number();m=number()
 if n<1 or 3*m!=4*n:raise ValueError('inconsistent source counts')
 w=n.bit_length();width=1+3*w
 if len(bits)-pos!=m*width:raise ValueError('incorrect body length')
 F=[]
 for _ in range(m):
  sign=1 if bits[pos]=='1' else -1;pos+=1
  ids=[int(bits[pos+i*w:pos+(i+1)*w],2) for i in range(3)];pos+=3*w
  F.append(tuple(sign*v for v in ids))
 if not valid(F):raise ValueError('invalid canonical grammar')
 return tuple(F)

def witness_ok(F,a):
 return all(any(a[abs(l)]==int(l>0) for l in c) for c in F)

def scan_gate(F,p):
 """Linear number of adjacency operations after linear explicit-source scan.
 Source bit access, Python dict allocation, index head and peak space are NOT free.
 """
 ledger=Counter(grammar_literal_reads=3*len(F),policy_checks=1)
 if not valid(F):return {'status':'MALFORMED','ledger':dict(ledger)}
 n=max(abs(x) for c in F for x in c)
 if not isinstance(p,dict) or any(type(v)!=int or v<1 or v>n or type(b)!=int or b not in (0,1) for v,b in p.items()):return {'status':'MALFORMED_PIN','ledger':dict(ledger)}
 incident=defaultdict(list);edges={}
 for j,c in enumerate(F):
  ledger['source_clause_status_checks']+=1
  ledger['source_literal_reads']+=3
  if any(abs(x) in p and p[abs(x)]==int(x>0) for x in c):continue
  rest=[x for x in c if abs(x) not in p]
  if not rest:return {'status':'UNSAT_EMPTY','source_clause_id':j,'ledger':dict(ledger)}
  if len(rest)!=2:continue
  u,v=map(abs,rest)
  incident[u].append((j,v));incident[v].append((j,u))
  edges[j]=(u,v,int(c[0]>0))
 ledger['binary_edges']=len(edges)
 for u in range(1,n+1):
  if u not in incident:continue
  ledger['motif_candidate_vertices']+=1
  neighbors=incident[u]
  if len(neighbors)!=4 or len(set(v for _,v in neighbors))!=4:continue
  vertices=tuple(sorted((u,)+tuple(v for _,v in neighbors)))
  if u!=vertices[0]:continue
  ids=[]
  for a,b in combinations(vertices,2):
   ledger['motif_pair_probes']+=1
   found=[j for j,v in incident[a] if v==b]
   if len(found)!=1:break
   ids.append(found[0])
  if len(ids)!=10:continue
  # Each source variable has exactly its two positive and two negative
  # incidences inside the 10 records; each sign graph is a simple 5-cycle.
  plus=tuple(sorted(j for j in ids if edges[j][2]==1))
  minus=tuple(sorted(j for j in ids if edges[j][2]==0))
  if len(plus)!=5 or len(minus)!=5:raise AssertionError('source quota contradiction')
  paths=implication_paths(F,ids,vertices)
  return {'status':'UNSAT_K5','source_clause_ids':tuple(sorted(ids)),
          'vertices':vertices,'positive_cycle_clause_ids':plus,
          'negative_cycle_clause_ids':minus,'implication_paths':paths,'ledger':dict(ledger)}
 return {'status':'UNRESOLVED','ledger':dict(ledger)}

def implication_paths(F,ids,vertices):
 graph=defaultdict(list)
 for j in ids:
  rest=[lit for lit in F[j] if abs(lit) in vertices]
  assert len(rest)==2
  a,b=rest
  graph[-a].append((b,j));graph[-b].append((a,j))
 def walk(begin,end):
  todo=deque([begin]);parent={begin:None}
  while todo:
   v=todo.popleft()
   if v==end:break
   for w,j in sorted(graph[v]):
    if w not in parent:parent[w]=(v,j);todo.append(w)
  if end not in parent:return None
  path=[];v=end
  while v!=begin:
   u,j=parent[v];path.append([u,v,j]);v=u
  return list(reversed(path))
 for v in vertices:
  p=walk(v,-v);q=walk(-v,v)
  if p is not None and q is not None:return {'pivot':v,'positive_to_negative':p,'negative_to_positive':q}
 raise AssertionError('2SAT certificate missing for K5')

def dpll(F,p,cap=500):
 ledger=Counter();limit=[False]
 def rec(q):
  ledger['nodes']+=1
  if ledger['nodes']>cap:limit[0]=True;return None
  q=dict(q)
  while True:
   found_unit=None;complete=True
   for c in F:
    ledger['clause_checks']+=1
    remaining=[];hit=False
    for l in c:
     ledger['literal_checks']+=1
     if abs(l) not in q:remaining.append(l)
     elif q[abs(l)]==int(l>0):hit=True;break
    if hit:continue
    complete=False
    if not remaining:return False
    if len(remaining)==1:found_unit=remaining[0];break
   if found_unit is None:
    if complete:return True
    break
   q[abs(found_unit)]=int(found_unit>0)
   ledger['unit_assignments']+=1
  v=next(i for i in range(1,max(abs(x) for c in F for x in c)+1) if i not in q)
  for b in (0,1):
   ledger['branch_edges']+=1
   z=rec({**q,v:b})
   if z is True:return True
   if z is None:return None
  return False
 answer=rec(p)
 return {'status':'UNKNOWN_CAP' if answer is None else ('SAT' if answer else 'UNSAT'),'ledger':dict(ledger)}

def main():
 U,V=source198()
 cases=[('K5_bad_cube',K5,PU),('K5_nearby_SAT_cube',K5,PS),('K5_full_SAT_root',K5,{}),
        ('F9_bad_cube',F9,P9),('Y6_root',Y6,{}),('F15_bad',F15,F15PU),('F15_SAT',F15,F15PS),
        ('U198_UNSAT',U,{}),('V198_SAT',V,{})]
 results={'run':'LSPV-2_K5_SOURCE_SCC295','status':'PROVED/EXACT restricted motif lemma, independent verification pending','canonical_target':'Döcker duplicate-free proper M3SAT(2,2)','cases':{},'exhaustive':{},'malformed':{},'P_vs_NP':'OPEN'}
 for name,F,p in cases:
  assert valid(F) and decode(encode(F))==F
  gate=scan_gate(F,p);base=dpll(F,p,cap=1000 if len(F)<=20 else 150)
  models=None
  if len(F)<=20:
   free=[v for v in range(1,max(abs(l) for c in F for l in c)+1) if v not in p]
   models=sum(witness_ok(F,{**p,**dict(zip(free,b))}) for b in product((0,1),repeat=len(free)))
   assert not gate['status'].startswith('UNSAT') or models==0
  results['cases'][name]={'n':max(abs(x) for c in F for x in c),'m':len(F),'source_bits':len(encode(F)),'gate':gate,'baseline':base,'models':models}
 # Every coherent partial state of Y6 and fixed 6-variable windows in F15.
 for label,F,roots in [('Y6',Y6,[{}]),('F15',F15,[F15PU,F15PS])]:
  tested=0;hit=0;fail=0
  for root in roots:
   free=[v for v in range(1,max(abs(l) for c in F for l in c)+1) if v not in root]
   for states in product((-1,0,1),repeat=len(free)):
    p={**root,**{v:b for v,b in zip(free,states) if b!=-1}}
    r=scan_gate(F,p);tested+=1
    if r['status']=='UNSAT_K5':
     hit+=1
     remaining=[v for v in range(1,max(abs(l) for c in F for l in c)+1) if v not in p]
     if any(witness_ok(F,{**p,**dict(zip(remaining,b))}) for b in product((0,1),repeat=len(remaining))):fail+=1
  results['exhaustive'][label]={'coherent_cubes':tested,'K5_certificates':hit,'false_UNSAT':fail}
 # All 12 possible edge 2-factorizations of K5, each 32 assignment states.
 all_pairs=set(combinations(range(1,6),2));tally=Counter()
 for sel in combinations(sorted(all_pairs),5):
  if any(sum(v in e for e in sel)!=2 for v in range(1,6)):continue
  neg=all_pairs-set(sel)
  assert all(sum(v in e for e in neg)==2 for v in range(1,6))
  tally['sign_partitions']+=1
  for bits in product((0,1),repeat=5):
   a=dict(zip(range(1,6),bits));tally['binary_assignments']+=1
   assert not (all(a[u] or a[v] for u,v in sel) and all((not a[u]) or (not a[v]) for u,v in neg))
 results['exhaustive']['K5_sign_partitions']=dict(tally)
 bad=[(),((1,2,3),),((1,1,2),),((1,2,-3),),K5+K5[:1],((1,2,3),(-1,-2,-3))]
 for j,b in enumerate(bad):assert scan_gate(b,{})['status']=='MALFORMED'
 validbits=encode(Y6)
 for variant in ('','0','2',validbits[:-1],validbits+'0',validbits[:4]+'2'+validbits[5:]):
  try:decode(variant)
  except ValueError:tally['invalid_binary_rejected']+=1
  else:raise AssertionError('malformed binary source accepted')
 results['malformed']={'tuple_sources_rejected':len(bad),'binary_encodings_rejected':tally['invalid_binary_rejected']}
 # Hostile strict-(2,2) comparison: orient every K5 edge as a mixed clause.
 # The cyclic regular tournament gives each free variable two positive and
 # two negative occurrences, while all-free-zero satisfies every edge.
 mutable=[list(c) for c in K5]
 for j,c in enumerate(mutable[:10]):
  u,v=sorted(abs(z) for z in c[:2])
  positive=u if (v-u)%5 in (1,2) else v
  mutable[j][:2]=[positive,-(v if positive==u else u)]
 nonmonotone=tuple(tuple(c) for c in mutable)
 assert not valid(nonmonotone)
 assert len(set(tuple(sorted(c)) for c in nonmonotone))==len(nonmonotone)
 deg=Counter(l for c in nonmonotone for l in c)
 assert all(deg[v]==deg[-v]==2 for v in range(1,16))
 comparison_witness={**PU,**{v:0 for v in range(1,6)}}
 assert witness_ok(nonmonotone,comparison_witness)
 results['comparative_strict22']={'nonmonotone_valid_broader_grammar':True,'canonical_rejects':True,
   'all_free_zero_is_SAT':True,'sat_witness':[comparison_witness[v] for v in range(1,16)],
   'changed_first_ten_original_ids':list(range(10))}
 (HERE/'results295.json').write_text(json.dumps(results,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'cases':{k:{'gate':v['gate']['status'],'models':v['models'],'baseline':v['baseline']['status']} for k,v in results['cases'].items()},'exhaustive':results['exhaustive'],'malformed':results['malformed']},indent=2))
if __name__=='__main__':main()
