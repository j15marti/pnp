#!/usr/bin/env python3
"""Independent easy-class and malformed-grammar controls for MIX274."""
import json,itertools,sys
from pathlib import Path
B=Path(__file__).resolve().parent
D=json.loads((B/'fixtures271.json').read_text())

def check(c,a):return all(any((bool(a[abs(x)-1]) == (x>0)) for x in k) for k in c)
def exhaustive(c,n):return any(check(c,a) for a in itertools.product([0,1],repeat=n))
def horn(c):
 assert all(sum(l>0 for l in clause)<=1 for clause in c)
 positive=set()
 while True:
  changed=False
  for clause in c:
   # Every negative literal corresponds to an antecedent.
   ant=[-l for l in clause if l<0]
   conseq=[l for l in clause if l>0]
   if all(x in positive for x in ant):
    if not conseq:return False
    if conseq[0] not in positive:positive.add(conseq[0]);changed=True
  if not changed:break
 return True

def two_sat(c,n):
 assert all(len(z)<=2 for z in c)
 g={i:[] for i in range(-n,n+1) if i!=0}
 for clause in c:
  if len(clause)==1:g[-clause[0]].append(clause[0])
  elif len(clause)==2:
   a,b=clause;g[-a].append(b);g[-b].append(a)
  elif not clause:return False
 seen=set();order=[]
 def dfs(v):
  if v in seen:return
  seen.add(v)
  for w in g[v]:dfs(w)
  order.append(v)
 for x in g:dfs(x)
 rg={x:[] for x in g}
 for x in g:
  for y in g[x]:rg[y].append(x)
 comp={}
 def dfs2(v,k):
  if v in comp:return
  comp[v]=k
  for w in rg[v]:dfs2(w,k)
 for v in reversed(order):
  if v not in comp:dfs2(v,len(set(comp.values()))+1)
 return all(comp[x]!=comp[-x] for x in range(1,n+1))

def mutation_check(row):
 # Codepath-independent canonical mismatch test: swapping one E literal
 # creates a source whose verified H/E projection is no longer the same.
 arr=[list(c) for c in row['mixed']]
 pos=len(row['source']);arr[pos][0]=-arr[pos][0]
 n=row['source_n'];m=row['source_m']
 def valid(z):
  if len(z)!=13*m:return False
  for j in range(m):
   if z[j]!=[-(n+3*j+k+1) for k in range(3)]:return False
   for k in range(3):
    first=m+12*j+4*k
    q=z[first:first+4];t=n+3*m+3*j+k+1;y=n+3*j+k+1
    if q[0][2]!=t or q[1][2]!=t or q[2][2]!=-t or q[3][2]!=-t:return False
    if q[0][:2]!=q[2][:2] or q[1][:2]!=q[3][:2]:return False
    if q[0][1]!=y or q[1][1]!=-y:return False
    if q[1][0]!=-q[0][0]:return False
  return True
 assert valid(row['mixed']) and not valid(arr)
 return True

def main():
 vals={}
 for name in ('HORN_CHAIN_SAT','HORN_CHAIN_UNSAT','KROM_SAT','KROM_UNSAT'):
  source=D[name];c=source['original_clauses'];n=source['n']
  truth=exhaustive(c,n)
  result=horn(c) if name.startswith('HORN') else two_sat(c,n)
  assert result==truth
  vals[name]={'label':'SAT' if truth else 'UNSAT','detector':name.split('_')[0],'n':n,'m':len(c)}
 raw=json.loads((B/'raw274.json').read_text())
 for r in raw['rows']:assert mutation_check(r)
 (B/'easy_controls274.json').write_text(json.dumps(vals,indent=2))
 print(json.dumps({'controls':vals,'malformed_e_rejections':len(raw['rows'])},indent=2))
if __name__=='__main__':main()