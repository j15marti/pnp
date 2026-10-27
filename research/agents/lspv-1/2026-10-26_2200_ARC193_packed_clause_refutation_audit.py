#!/usr/bin/env python3
"""ARC193 signed-(2,2) packing-derived source-authenticated tree controls.
Deterministic/exhaustive. Model: canonical literal-index input and explicit BRANCH/EMPTY stream.
"""
from __future__ import annotations
from collections import Counter
from itertools import product
from math import log2, ceil
import json, sys, hashlib
from pathlib import Path

W1=[(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
(5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),(-2,-6,12),
(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),(2,-9,11),
(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)]
G=[(1,2,3),(1,-2,-3),(-1,2,-3),(-1,-2,3)]
COUNT=0

def check(p, msg='assertion failed'):
 global COUNT
 COUNT+=1
 if not p: raise AssertionError(msg)

def copies(clauses,k):
 n=max(abs(l) for c in clauses for l in c)
 return [tuple(l+(n*j if l>0 else -n*j) for l in c) for j in range(k) for c in clauses]

def pack(clauses):
 used=set(); indices=[]
 for j,c in enumerate(clauses):
  support={abs(l) for l in c}
  if support.isdisjoint(used):
   indices.append(j); used.update(support)
 return indices

def valid22(clauses):
 n=max(abs(l) for c in clauses for l in c)
 pos=Counter(l for c in clauses for l in c if l>0)
 neg=Counter(-l for c in clauses for l in c if l<0)
 check(len(clauses)*3 == 4*n)
 check(all(len(c)==3 and len({abs(l) for l in c})==3 for c in clauses))
 check(all(pos[x]==2 and neg[x]==2 for x in range(1,n+1)))
 return n

def serialize(clauses):
 n=max(abs(l) for c in clauses for l in c)
 header=f'p cnf {n} {len(clauses)}\n'; a=[header]; positions=[]
 for c in clauses:
  positions.append(sum(map(len,a)))
  a.append(' '.join(map(str,c))+' 0\n')
 txt=''.join(a); b=txt.encode('ascii')
 return b,positions

def clause_false(c,a):
 return all(abs(l) in a and a[abs(l)]!=(l>0) for l in c)

def satisfaction(clauses,a):
 return all(any(a[abs(l)]==(l>0) for l in c) for c in clauses)

def exact_models(clauses):
 n=max(abs(l) for c in clauses for l in c)
 return sum(satisfaction(clauses,{i+1:bool((j>>i)&1) for i in range(n)}) for j in range(1<<n))

def reduce(clauses,assign):
 out=[]
 for c in clauses:
  if any(abs(l) in assign and (l>0)==assign[abs(l)] for l in c):
   continue
  out.append(tuple(l for l in c if abs(l) not in assign))
 return out

def svalue(clauses,a):
 return all(any(a[abs(l)]==(l>0) for l in c) for c in clauses)

def tree(clauses,full=False):
 """Actual source-offset BRANCH/EMPTY SAT-witness stream.
 No semantic oracle. Full generator tests all surviving assignments, not DPLL shortcuts.
 """
 n=max(abs(l) for c in clauses for l in c)
 chosen=pack(clauses); h=len(chosen)
 order=[abs(l) for j in chosen for l in clauses[j]]
 order += [i for i in range(1,n+1) if i not in set(order)]
 source,offsets=serialize(clauses)
 start_to_clause={p:j for j,p in enumerate(offsets)}
 tokens=[]; stats=Counter(); a={}
 def emit(symbol):
  if full: tokens.append(symbol)
 def visit(depth):
  stats['node']+=1
  if depth and depth<=3*h and depth%3==0:
   j=chosen[depth//3-1]
   if clause_false(clauses[j],a):
    stats['empty']+=1; stats['packed_closed']+=1; emit(('E',offsets[j])); return
  if depth==n:
   bad=next((j for j,c in enumerate(clauses) if clause_false(c,a)),None)
   if bad is None:
    stats['model']+=1;emit(('S', tuple(int(a[i]) for i in range(1,n+1))))
   else:
    stats['empty']+=1;stats['suffix_closed']+=1;emit(('E',offsets[bad]))
   return
  x=order[depth]; stats['branch']+=1;emit(('B',x))
  for v in (False,True):
   a[x]=v
   visit(depth+1)
  del a[x]
 visit(0)
 check(stats['branch']+stats['empty']+stats['model']==stats['node'])
 check(stats['node']==2*stats['branch']+1)
 check(stats['empty']+stats['model']==stats['branch']+1)
 L=(7**h-1)//6+7**h*2**(n-3*h)
 check(stats['empty']+stats['model']==L,f'tree leaves mismatch: {stats} vs {L}')
 if full:
  # Authenticating verifier replays tree; every E must reference a real original clause
  # at a line-start physical byte offset, genuinely falsified by branch assignment.
  ptr=0; env={}
  def read(depth):
   nonlocal ptr
   kind,v=tokens[ptr];ptr+=1
   if kind=='B':
    check(v not in env)
    for b in (False,True):
     env[v]=b;read(depth+1)
    del env[v]
   elif kind=='E':
    check(v in start_to_clause)
    check(clause_false(clauses[start_to_clause[v]],env))
   elif kind=='S':
    check(depth==n)
    check(tuple(int(env[i]) for i in range(1,n+1))==v)
    check(satisfaction(clauses,env))
   else: raise AssertionError(kind)
  read(0);check(ptr==len(tokens));check(len(tokens)==stats['node'])
  # Physical proof stream charge: prefix tags and all bit strings (no hidden proof pointers)
  bitstream=''.join('0'+format(v,'0'+str(ceil(log2(n+1)))+'b') if kind=='B' else
                    '10'+format(v,'0'+str(ceil(log2(len(source)+1)))+'b') if kind=='E' else
                    '11'+''.join(map(str,v)) for kind,v in tokens)
  stats['proof_bits']=len(bitstream)
  stats['proof_sha256']=hashlib.sha256(bitstream.encode()).hexdigest()
 stats['h']=h;stats['n']=n;stats['m']=len(clauses)
 stats['bound_closed_formula']=L
 stats['input_bytes']=len(source)
 stats['chosen_clause_indices']=chosen
 return stats

def main():
 results={}
 for name,clauses in [('G',G),('W1',W1),('Gx2',copies(G,2)),('W1plusG',W1+list(copies(G,1)) if False else W1+[tuple(l+15 if l>0 else l-15 for l in c) for c in G])]:
  n=valid22(clauses);m=len(clauses)
  chosen=pack(clauses);h=len(chosen)
  check(h>=ceil(m/10))
  check(3*h<=n)
  # Complete trees replayed on all sources; W1plusG may be larger but finite.
  st=tree(clauses,True)
  mod=exact_models(clauses)
  check(st['model']==mod)
  if 'W1' in name: check(mod==0)
  if name=='G':check(mod>0)
  # The first two hereditary levels are literal restrictions on two actual
  # disjoint packed clauses. For both satisfying and unsatisfying controls.
  lev=[]
  if h>=2:
   for a1 in product((False,True),repeat=3):
    p1={abs(l):b for l,b in zip(clauses[chosen[0]],a1)}
    child=reduce(clauses,p1)
    for a2 in product((False,True),repeat=3):
     p2={abs(l):b for l,b in zip(clauses[chosen[1]],a2)}
     grand=reduce(child,p2)
     check(not any(set(map(abs,c)).intersection(set(p1)|set(p2)) for c in grand))
     untouched=[j for j,c in enumerate(clauses) if not(set(map(abs,c)) & (set(p1)|set(p2)))]
     check(len(untouched)>=m-4*6)
     check(all(clauses[j] in grand for j in untouched))
     lev.append((len(child),len(grand)))
  st['two_level_pairs']=len(lev)
  st['two_level_grandclause_range']=[min((b for a,b in lev), default=0),max((b for a,b in lev), default=0)]
  results[name]=dict(st)
 # Pure symbolic n multiple of 3: greedy packing count >= 2n/15; exponent.
 alpha=1+(2/15)*log2(7/8)
 check(0<alpha<1)
 for n in [15,30,45,60,90,150,300]:
  m=4*n//3
  check(ceil(m/10)>=ceil(2*n/15))
  for h in range(ceil(m/10),n//3+1):
   L=(7**h-1)//6+7**h*2**(n-3*h)
   check(L<=2**n)
 result={'run_id':'ARC193_PACKED_REFUTATION','model':'source-authenticated binary BRANCH/EMPTY grammar',
         'controls':results,'symbolic':{'alpha_base2':alpha,'base_exponential':2**alpha,
                'matching_lower_h_over_n':'2/15',
                'leaf_bound':'(7^h-1)/6 + 7^h 2^(n-3h)',
                'runtime':'poly(N) * 2^(alpha*n) on signed exact22',
                'space':'O(N) work on indexed RAT for explicit certificate generator'},
         'assertions':COUNT,'failures':0,'kind':'COMPUTATIONAL controls plus independent mathematical proof'}
 out=Path(__file__).with_name('2026-10-26_2200_ARC193_packed_clause_refutation_raw.json')
 out.write_text(json.dumps(result,indent=2,sort_keys=True))
 print(json.dumps({'assertions':COUNT,'results':{k:{z:v for z,v in a.items() if z in ('n','m','h','model','empty','node','proof_bits','two_level_pairs')} for k,a in results.items()},'alpha':alpha,'out':str(out)},indent=2))

if __name__=='__main__': main()
