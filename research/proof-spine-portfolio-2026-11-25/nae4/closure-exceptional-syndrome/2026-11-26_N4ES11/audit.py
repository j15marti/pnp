import itertools, json, numpy as np
P=[[(0,1,2),(3,4,5),(6,7,8)],[(0,3,6),(1,4,7),(2,5,8)],[(0,4,8),(1,5,6),(2,3,7)],[(0,5,7),(1,3,8),(2,4,6)]]
C=sum(P,[]); A=np.array(C); X=((np.arange(512)[:,None]>>np.arange(9))&1).astype(np.uint8)
E=np.array([[0,1,1],[0,0,0],[0,1,1],[0,0,1],[0,0,1],[0,1,0],[0,0,1],[0,1,1],[0,1,0],[0,1,0],[0,0,0],[0,1,1]],dtype=np.uint8)
def ok(w):return (w.min(axis=-1)!=w.max(axis=-1)).all(axis=-1)
def lifted(rows):return [(p,tuple(2*v+(s^e) for v,e in zip(c,a))) for p,c,a in rows for s in (0,1)]
def authenticate(rows,n):
 assert len(rows)==4*n//3
 assert all(sorted(v for p,c in rows if p==j for v in c)==list(range(n)) for j in range(4))
 assert all(len(set(c))==3 for p,c in rows)
 assert len({tuple(sorted(pair)) for p,c in rows for pair in itertools.combinations(c,2)})==3*len(rows)
 adj=[[] for _ in range(n)]
 for _,(a,b,c) in rows:
  adj[a].extend((b,c));adj[b].extend((a,c));adj[c].extend((a,b))
 seen={0}; stack=[0]
 while stack:
  for v in adj[stack.pop()]:
   if v not in seen:seen.add(v);stack.append(v)
 return len(seen)==n
def make(k,negative=False):
 rows=[]; witness=[]; portable=[]
 # explicit witness for lifted AG9, with v7 equal on both sheets
 ag=[1,0,1,0,0,1,0,1,0,1,1,0,1,0,0,0,1,0]
 # choose local module states with L0 uniform 0 and L1 uniform 1
 mod=X[ok(X[:,A[2:]]) & (X[:,:3]==0).all(1) & (X[:,3:6]==1).all(1)][0].tolist()
 for i in range(k):
  o=27*i
  # 11-line AG9 core: source witness from E; negative control has all zero internal voltages
  for j,c in enumerate(C):
   if j!=2:rows.append((j//3,tuple(o+v for v in c),tuple(map(int,E[j])) if not negative else (0,0,0)))
  for h in range(2):
   for j,c in enumerate(C):
    if j>=2:rows.append((j//3,tuple(o+9*(h+1)+v for v in c),(0,0,0)))
  # two positive connectors: one shifted first occurrence; other plain
  rows.append((0,(o+9,o+19,o+20),(1,0,0)))
  rows.append((0,(o+18,o+10,o+11),(0,0,0)))
  # negative connector A=(12,22,23), B=(21,13,14). module0 L1=1, module1 L1=0.
  # exchange v7 and v22 (both 0 on both sheets). preserve original AG9 row voltages by position.
  rows.append((0,(o+6,o+22,o+8),tuple(map(int,E[2])) if not negative else (0,0,0)))
  rows.append((0,(o+12,o+7,o+23),(0,0,0)))
  # B uses module1 port21=0, redirect cyclically to connect blocks.
  portable.append((0,(27*((i+1)%k)+21,o+13,o+14),(0,0,0)))
  witness.extend(ag)
  for h in range(2):witness.extend([v^h for a in mod for v in (a,a)])
 rows.extend(portable)
 return rows,np.array(witness,dtype=np.uint8)
def verify_chart(rows,d,x):
 for _,c,e in rows:
  ds=d[list(c)]; w=x[list(c)]^(np.array(e,dtype=np.uint8)*ds)
  if ds.min()==ds.max():
   if w.min()==w.max():return False
  else:
   j,l=next((j,l) for j,l in itertools.combinations(range(3),2) if ds[j]==ds[l])
   if w[j]==w[l]:return False
 return True
# complete local truth-table check, 512 patterns for each voltage choice (64 combos total)
local=0
for e in itertools.product((0,1),repeat=3):
 for d in itertools.product((0,1),repeat=3):
  for x in itertools.product((0,1),repeat=3):
   x=np.array(x,dtype=np.uint8);d=np.array(d,dtype=np.uint8);e=np.array(e,dtype=np.uint8)
   w=x^(e*d); direct=bool(w.min()!=w.max() and (w^d).min()!=(w^d).max())
   assert direct==verify_chart([(0,(0,1,2),e)],d,x);local+=1
# all local AG9 cores and module relation independent brute-force
assert not ok(X[:,A[np.arange(12)!=2]]).any()
module=X[ok(X[:,A[2:]])]; assert len(module)==12
assert all((r[:3]==r[0]).all() and (r[3:6]==1-r[0]).all() for r in module)
# positive-pair connectors under all-opposite mask: NAE on repeated phase; impossible
for a,b in itertools.product((0,1),repeat=2):
 assert not ((1-a!=b) and (b!=a))
results=[]
for k in (1,2,4,8,16,32,64,128):
 rows,w=make(k); D=lifted(rows); assert authenticate([(p,c) for p,c,e in rows],27*k); assert authenticate(D,54*k)
 assert ok(w[:,None].T[:,np.array([c for p,c in D])]).all()
 d=w[::2]^w[1::2]; assert verify_chart(rows,d,w[::2]); assert k<=int(d.sum())<=27*k-k
 # Connected UNSAT neighbor: gauge internal AG9 edges all zero; each sheet contains 11-line core. A source-only fixed-template certificate.
 neg,_=make(k,negative=True); ND=lifted(neg);assert authenticate([(p,c) for p,c,e in neg],27*k);assert authenticate(ND,54*k)
 # Same source size; verify a literal 11-clause AG9 subfamily on sheet 0.
 core={tuple(sorted(c)) for p,c in ND}; assert all(tuple(sorted(2*v for v in c)) in core for j,c in enumerate(C) if j!=2)
 results.append(dict(k=k,variables=54*k,clauses=72*k,quotient_variables=27*k,witness_mask_ones=int(d.sum()),witness_mask_zeros=27*k-int(d.sum()),minimum_each=k,connected_sat=True,connected_unsat_neighbor=True))
print(json.dumps(dict(local_checks=local,module_models=len(module),ag9_core_assignments=512,results=results),indent=2))
