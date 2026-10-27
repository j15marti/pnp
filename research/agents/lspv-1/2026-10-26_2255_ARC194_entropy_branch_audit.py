#!/usr/bin/env python3
"""ARC194 source-authenticated prefix-entropy BRANCH/EMPTY audit.
No dependencies. Checks both exact integer entropy inequalities at every
prefix depth and independently replays actual UNSAT proof streams.
"""
import hashlib
import json
import random
from collections import Counter
from pathlib import Path

OUT = Path(__file__).resolve().parent
SEED = 202610262255
W1 = [
 (-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),
 (-4,-9,-11),(5,8,-14),(4,-8,-11),(1,7,13),
 (1,-7,10),(-5,-6,-15),(-2,-6,12),(-4,9,-10),
 (-2,5,-12),(-3,6,-15),(6,-7,11),(2,-9,11),
 (4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14),
]
G=[(1,2,3),(-1,-2,-3),(1,-2,3),(-1,2,-3)]
checks=0

def ensure(test,msg=''):
 global checks
 checks+=1
 if not test: raise AssertionError(msg)

def shift(clauses,offset):
 return [tuple((abs(l)+offset)*(1 if l>0 else -1) for l in c)
         for c in clauses]

def invert(clauses,var):
 return [tuple(-l if abs(l)==var else l for l in c) for c in clauses]

def serialize(clauses,n):
 source=f'p cnf {n} {len(clauses)}\n'.encode('ascii')
 offsets=[]
 for c in clauses:
  offsets.append(len(source))
  source+=(' '.join(map(str,c))+' 0\n').encode('ascii')
 return source,offsets

def decode_at(source,offset):
 ensure(0<offset<len(source),'pointer outside source')
 ensure(source[offset-1:offset]==b'\n','pointer not source-clause start')
 s=source[offset:source.index(b'\n',offset)].decode('ascii')
 ids=[int(a) for a in s.split()]
 ensure(len(ids)==4 and ids[-1]==0,'malformed clause')
 return tuple(ids[:-1])

def proper22(clauses,n):
 pos,neg=Counter(),Counter()
 for c in clauses:
  ensure(len(c)==3 and len({abs(x) for x in c})==3,'not proper ternary')
  for lit in c: (pos if lit>0 else neg)[abs(lit)]+=1
 for v in range(1,n+1):
  ensure(pos[v]==2 and neg[v]==2,'not signed exact (2,2)')
 ensure(3*len(clauses)==4*n,'incidence mismatch')

def false_clause(clause,path):
 return all(abs(l) in path and path[abs(l)]==(l<0) for l in clause)

def by_completion_depth(clauses,order):
 place={v:i for i,v in enumerate(order)}
 closed=[[] for _ in range(len(order)+1)]
 for i,c in enumerate(clauses):
  closed[1+max(place[abs(l)] for l in c)].append((i,c))
 return closed

def run(name,clauses,n,order,make_proof=False):
 proper22(clauses,n)
 ensure(sorted(order)==list(range(1,n+1)),'invalid variable order')
 source,offsets=serialize(clauses,n)
 for i,off in enumerate(offsets):
  ensure(decode_at(source,off)==clauses[i],'source-offset mismatch')
 closed=by_completion_depth(clauses,order)
 counts=[0]*(n+1)
 nodes=0; failed=0; models=0; path={}

 def explore(depth):
  nonlocal nodes,failed,models
  nodes+=1
  for i,c in closed[depth]:
   if false_clause(c,path):
    ensure(decode_at(source,offsets[i])==c,'false clause from wrong byte')
    failed+=1
    return
  counts[depth]+=1
  if depth==n:
   models+=1
   ensure(all(not false_clause(c,path) for c in clauses),'fake model')
   return
  x=order[depth]
  for bit in (False,True):
   path[x]=bit
   explore(depth+1)
  del path[x]

 explore(0)
 ensure(nodes==1+2*sum(counts[:-1]),'node identity')
 ensure(failed+models==(nodes+1)//2,'leaf identity')
 ensure(3*(nodes-1)<=8*7**(n//3),'node entropy bound')
 prefix=[]
 for k,p in enumerate(counts):
  prefix_set=set(order[:k])
  full=sum(all(abs(l) in prefix_set for l in c) for c in clauses)
  ensure(len(clauses)-full<=4*(n-k),'unfinished incidence bound')
  ensure(p**4*8**full<=2**(4*k)*7**full,'integer Shearer bound')
  ensure(p*7**(n-k)<=7**(n//3)*4**(n-k),'integer prefix bound')
  prefix.append({'depth':k,'surviving_prefixes':p,'completed_clauses':full})
 transcript=None
 if make_proof:
  ensure(models==0,'never emit purported UNSAT proof from SAT')
  filename=OUT/(name+'_source_auth.proof')
  emitted=0
  with open(filename,'wt',encoding='ascii') as f:
   def write(depth):
    nonlocal emitted
    emitted+=1
    for i,c in closed[depth]:
     if false_clause(c,path):
      f.write(f'E {offsets[i]}\n')
      return
    ensure(depth<n,'proof reached SAT full assignment')
    x=order[depth]
    f.write(f'B {x}\n')
    for b in (False,True):
     path[x]=b
     write(depth+1)
    del path[x]
   write(0)
  ensure(emitted==nodes,'proof construction mismatch')
  lines=iter(filename.read_text(encoding='ascii').splitlines())
  replay=0
  def verify(depth):
   nonlocal replay
   replay+=1
   kind,arg=next(lines).split()
   if kind=='E':
    clause=decode_at(source,int(arg))
    ensure(false_clause(clause,path),'forged source leaf')
    return
   ensure(kind=='B' and depth<n and int(arg)==order[depth],
          'bad branch token')
   for b in (False,True):
    path[order[depth]]=b
    verify(depth+1)
   del path[order[depth]]
  verify(0)
  ensure(replay==nodes,'bad replay nodes')
  ensure(next(lines,None) is None,'trailing proof garbage')
  raw=filename.read_bytes()
  transcript={'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),
              'replayed_nodes':replay,'name':filename.name}
 return {'name':name,'n':n,'m':len(clauses),'N_source_bytes':len(source),
         'order':order,'models':models,'false_leaves':failed,'nodes':nodes,
         'full_count_upper_7_n_over_3':7**(n//3),'prefix':prefix,
         'transcript':transcript}

def main():
 random.seed(SEED)
 cases=[
  ('G_SAT',G,3,[1,2,3],False),
  ('G_SAT_REVERSE',G,3,[3,2,1],False),
  ('G2_SAT',G+shift(G,3),6,list(range(1,7)),False),
  ('W1_UNSAT',W1,15,list(range(1,16)),True),
  ('W1_UNSAT_REVERSE',W1,15,list(range(15,0,-1)),False),
  ('W1_UNSAT_SIGNFLIP',invert(W1,1),15,list(range(1,16)),False),
  ('W1_G_UNSAT',W1+shift(G,15),18,list(range(1,19)),True),
  ('G_W1_UNSAT',G+shift(W1,3),18,list(range(1,19)),False),
 ]
 data=[run(*args) for args in cases]
 expected={'G_SAT':4,'G_SAT_REVERSE':4,'G2_SAT':16,
   'W1_UNSAT':0,'W1_UNSAT_REVERSE':0,'W1_UNSAT_SIGNFLIP':0,
   'W1_G_UNSAT':0,'G_W1_UNSAT':0}
 for item in data:
  ensure(item['models']==expected[item['name']],'wrong SAT label')
 result={'run_id':'ARC-ENTROPY-SOURCE-BRANCH194','seed':SEED,
         'n_models':len(data),'assertion_groups':checks,'failures':0,
         'status':'COMPUTATIONAL finite checks; symbolic theorem in report',
         'cases':data}
 outfile=OUT/'2026-10-26_2255_ARC194_entropy_branch_raw.json'
 outfile.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'checks':checks,'cases':[
  {'name':r['name'],'nodes':r['nodes'],'models':r['models']}
  for r in data]},indent=2))

if __name__=='__main__': main()
