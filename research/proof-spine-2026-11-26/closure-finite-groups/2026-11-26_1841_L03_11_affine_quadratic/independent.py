# Independent all-table evaluation span and guarded hostile DFS.
import itertools as it, json
from pathlib import Path
W=range(16)
def row_eval(w):
 x=[(w>>(3-i))&1 for i in range(4)]
 return sum(b<<j for j,b in enumerate([1]+x+[x[i]&x[j] for i,j in it.combinations(range(4),2)]))
E=[row_eval(w) for w in W]
def span_basis(rows):
 B={}
 for v in rows:
  while v:
   p=v.bit_length()-1
   if p in B:v^=B[p]
   else:B[p]=v;break
 return B
def in_span(v,B):
 while v:
  p=v.bit_length()-1
  if p not in B:return False
  v^=B[p]
 return True
checks=0
for size in range(1,5):
 for a in it.combinations(W,size):
  B=span_basis(E[i] for i in a)
  for w in W:
   assert in_span(E[w],B)==(w in a);checks+=1
r=json.loads(Path(__file__).with_name('results.json').read_text())['hostile']; k=4
R=[[tuple((w>>(3-i))&1 for i in range(4)) for w in a] for a in r['masks']]
def vkey(row,col,d):
 dr,dc=[(-1,0),(0,1),(1,0),(0,-1)][d]; rr,cc=row+dr,col+dc
 return tuple(sorted(((row,col),(rr,cc))))
P=[[vkey(a,b,d) for d in range(4)] for a in range(k) for b in range(k)]
init={vkey(a,b,d):int(d==2) for a in range(k) for b in range(k) for d in range(4) if (d==0 and a==0) or(d==1 and b==k-1)or(d==2 and a==k-1)or(d==3 and b==0)}
visits=0
def dfs(i,assignment):
 global visits
 if i==k*k:return True
 for w in R[i]:
  visits+=1
  if visits>100000:raise RuntimeError('cap')
  if all(e not in assignment or assignment[e]==b for e,b in zip(P[i],w)):
   if dfs(i+1,assignment|dict(zip(P[i],w))):return True
 return False
assert not dfs(0,init)
print(json.dumps({'local_tables':sum(len(list(it.combinations(W,s))) for s in range(1,5)),'evaluation_span_checks':checks,'hostile_dfs_NO':True,'hostile_dfs_attempts':visits,'cap':100000},indent=2))
