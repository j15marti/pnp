#!/usr/bin/env python3
"""Exhaustive signed two-variable strict Resolution shortest proofs and bit-prefix search.
Requires only Python standard library. This is finite exponential enumeration, not SAT in P.
Usage: python experiments/arc/lspv1_408_proof_search.py [raw_output_path]
"""
import json,sys,collections
U=((-1,),(1,),(-2,),(2,),(-1,-2),(-1,2),(1,-2),(1,2))
def key(a):return tuple(sorted(set(a),key=lambda x:(abs(x),x<0)))
def resolve(a,b):
 for p in (1,2):
  if (p in a and -p in b) or (-p in a and p):
   s=(set(a)|set(b))-{p,-p}
   if all(-x not in s for x in s):yield p,key(s)
def models(src):
 return [m for m in range(4) if all(any(bool(m&(1<<(abs(x)-1)))==(x>0) for x in c) for c in src)]
def encode(actions):
 return f'{len(actions):04b}'+''.join(f'{a:04b}{b:04b}{p-1:01b}' for a,b,p in actions)
def decode(bits):
 if not isinstance(bits,str) or len(bits)<4 or set(bits)-set('01'):return None
 q=int(bits[:4],2)
 if len(bits)!=4+9*q:return None
 return [(int(bits[4+9*j:8+9*j],2),int(bits[8+9*j:12+9*j],2),1+int(bits[12+9*j],2)) for j in range(q)]
def check(src,actions):
 if actions is None or not actions or len(actions)>9:return False
 nodes=list(src)
 for t,(a,b,p) in enumerate(actions):
  if a>=len(nodes) or b>=len(nodes) or a<0 or b<0 or a==b or p not in (1,2):return False
  z=dict(resolve(nodes[a],nodes[b])).get(p)
  if z is None or z in nodes:return False
  nodes.append(z)
  if z==():return t==len(actions)-1
 return False
def shortest(src):
 todo=collections.deque([(frozenset(),())]);seen={frozenset()};visits=0
 while todo:
  derived,trace=todo.popleft();visits+=1
  nodes=list(src)+[x[3] for x in trace]
  for a in range(len(nodes)):
   for b in range(len(nodes)):
    if a==b:continue
    for p,z in resolve(nodes[a],nodes[b]):
     if z in nodes:continue
     nxt=trace+((a,b,p,z),)
     if z==():return len(nxt),visits
     nd=derived|{z}
     if nd not in seen:seen.add(nd);todo.append((nd,nxt))
 return None,visits
def proof_codes(src,q):
 ans=set()
 def rec(nodes,trace):
  if len(trace)==q:
   if check(src,trace):ans.add(encode(trace))
   return
  for a in range(len(nodes)):
   for b in range(len(nodes)):
    if a==b:continue
    for p,z in resolve(nodes[a],nodes[b]):
     if z in nodes or ((z==())!=(len(trace)==q-1)):continue
     rec(nodes+[z],trace+((a,b,p),))
 rec(list(src),())
 return sorted(ans)
def greedy(cs):
 prefix='';queries=0
 for _ in range(len(cs[0])):
  queries+=1
  if any(x.startswith(prefix+'0') for x in cs):prefix+='0'
  else:
   queries+=1
   assert any(x.startswith(prefix+'1') for x in cs)
   prefix+='1'
 return prefix,queries
def main():
 sumry=dict(cases=0,sat=0,unsat=0,replay_ok=0,minimal_checked=0,prefix_queries=0,
            bad_rejections=10,max_q=0,enumerated_codes=0,bfs_states=0)
 rows=[]
 for mask in range(256):
  src=tuple(U[i] for i in range(8) if mask&(1<<i))
  m=models(src);q,visits=shortest(src);sumry['cases']+=1;sumry['bfs_states']+=visits
  assert bool(m)==(q is None)
  if m:
   sumry['sat']+=1
   rows.append(dict(mask=mask,label='SAT',models=len(m),bfs_states=visits))
   continue
  cs=proof_codes(src,q);assert cs
  best,queries=greedy(cs)
  assert best==cs[0] and check(src,decode(best))
  sumry['unsat']+=1;sumry['replay_ok']+=1;sumry['minimal_checked']+=1
  sumry['prefix_queries']+=queries;sumry['enumerated_codes']+=len(cs)
  sumry['max_q']=max(q,sumry['max_q'])
  rows.append(dict(mask=mask,label='UNSAT',q=q,bits=len(best),code=best,
                   candidate_proofs=len(cs),prefix_queries=queries,bfs_states=visits))
 src=((1,),(-1,));good='0001000000010'
 assert check(src,decode(good))
 bad=[good[:-1],good+'0',good[:4]+'1111'+good[8:],
      good[:8]+'0000'+good[12:],good[:12]+'1','111111','garbage','',None]
 for x in bad:assert not check(src,decode(x))
 assert not check(((1,),),decode(good))
 assert sumry['sat']==95 and sumry['unsat']==161
 payload=dict(model='strict_binary_resolution_two_variables',universe=[list(x) for x in U],
              summary=sumry,records=rows,seed=None,exhaustive=True,
              oracle_note='Prefix oracle implemented by finite exhaustive enumeration of all valid shortest certificates. It is NOT a polynomial-time SAT oracle.')
 target=sys.argv[1] if len(sys.argv)>1 else 'results/raw/arc/2026-11-04_1956_LSPV1_PROOF_SEARCH408_raw.json'
 with open(target,'w') as f:json.dump(payload,f,sort_keys=True,indent=2);f.write('\n')
 print(json.dumps({'output':target,'summary':sumry}))
if __name__=='__main__':main()
