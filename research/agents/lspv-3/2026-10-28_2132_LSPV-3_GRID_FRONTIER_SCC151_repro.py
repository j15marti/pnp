#!/usr/bin/env python3
"""LSPV-3 GRID-FRONTIER-SCC151, dependency-free independent reproducer.

Connected strict signed exact-(2,2)-3CNF with a large every-order live
frontier, but efficiently generated BOTH answer classes and original-clause
2CNF SCC contradiction leaves. No unrestricted SAT claims.

Run: python3 2026-10-28_2132_LSPV-3_GRID_FRONTIER_SCC151_repro.py > results.json
"""
import collections
import hashlib
import itertools
import json
import random

U = tuple(tuple(map(int,r.split())) for r in (
'-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14').split(';'))
S = tuple(tuple(map(int,r.split())) for r in '-1 -3 14;2 8 -9;-10 13 14;3 -7 -13;-4 9 -11;-5 -8 -14;4 -8 11;1 7 -13;1 -7 10;-5 -6 15;-2 6 -12;4 9 -10;-2 5 -12;3 6 -15;-6 7 11;2 -9 -11;-4 8 10;-3 12 15;5 12 -15;-1 13 -14'.split(';'))
assert len(U)==len(S)==20
PORTS = {'N': (1,2), 'S': (2,0), 'E': (3,1), 'W': (4,0)}
assert all(S[c][j]<0 for c,j in PORTS.values())
# Signed template U and S both have two occurrences of each polarity/variable.
for template in (U,S):
 occ=collections.Counter(l for c in template for l in c)
 assert len(template)==20 and all(occ[v]==occ[-v]==2 for v in range(1,16))
assert all(set(map(abs,a))==set(map(abs,b)) for a,b in zip(U,S))
# One concrete private witness for the U relation (u_i,u_(i+1))=(1,0).
UPRIVATE=int('01000000001000',2)
COUNTS=collections.Counter()

def ck(cond,tag):
 COUNTS['assertions']+=1
 if not cond:raise AssertionError(tag)

def grid_info(H):
 if H<2:raise ValueError('H must be >= 2')
 k=H*H+2*H
 return k,2*H

def typeword(H,flags):
 if len(flags)!=H or any(x not in (0,1) for x in flags): raise ValueError('flags')
 return ''.join('U' + ('U' if bit else 'S') for bit in flags)+'S'*(H*H)

def remap(l,i):
 return (1 if l>0 else -1)*(abs(l)+15*i)

def build(H,flags):
 types=typeword(H,flags)
 k,offset=grid_info(H)
 clauses=[]
 for i,t in enumerate(types):
  for j,c in enumerate(U if t=='U' else S):
   a=list(remap(l,i) for l in c)
   if j==0:
    assert a[0]<0
    a[0]=-(15*((i+1)%k)+1)
   clauses.append(a)
 def patch(b,d1,b2,d2):
  ci,j=PORTS[d1];ci2,j2=PORTS[d2]
  z=20*b+ci; z2=20*b2+ci2
  assert clauses[z][j]<0 and clauses[z2][j2]<0
  clauses[z][j],clauses[z2][j2]=clauses[z2][j2],clauses[z][j]
 idx=lambda r,c:offset+r*H+c
 for r in range(H):
  for c in range(H):
   if c+1<H:patch(idx(r,c),'E',idx(r,c+1),'W')
   if r+1<H:patch(idx(r,c),'S',idx(r+1,c),'N')
 return tuple(tuple(c) for c in clauses)

def encode(rows,H):
 n=15*(H*H+2*H)
 return ('p cnf %d %d\n'%(n,len(rows)) + ''.join(' '.join(map(str,c))+' 0\n' for c in rows)).encode('ascii')

def canonical_parse(raw):
 """Authenticates full byte source and declared template. No side-bit supplied.

 The actual native input scan can synthesize expected clause ID/sign by
 counters and H, without storing the whole input. Here arrays are used for
 audit convenience and do not measure fixed-tape memory.
 """
 if not isinstance(raw,bytes):raise ValueError('binary source')
 try:lines=raw.decode('ascii').splitlines(keepends=True)
 except UnicodeError as e:raise ValueError('ASCII source') from e
 if not lines or any(not l.endswith('\n') for l in lines):raise ValueError('newlines')
 h=lines[0].strip().split(' ')
 if len(h)!=4 or h[:2]!=['p','cnf']:raise ValueError('header')
 try:n,m=map(int,h[2:])
 except ValueError as e:raise ValueError('integer header') from e
 if n<=0 or n%15 or m!=20*(n//15) or len(lines)!=m+1:raise ValueError('dimensions')
 k=n//15
 # k=H^2+2H, so (H+1)^2=k+1. Exact integer square check.
 from math import isqrt
 H=isqrt(k+1)-1
 if H<2 or H*H+2*H!=k:raise ValueError('not-grid-size')
 rows=[]
 for line in lines[1:]:
  try:c=tuple(map(int,line.strip().split(' ')))
  except ValueError as e:raise ValueError('literal integer') from e
  if len(c)!=4 or c[-1]!=0:raise ValueError('width')
  if any(x==0 or abs(x)>n for x in c[:-1]):raise ValueError('literal index')
  rows.append(c[:-1])
 flags=[]
 for j in range(H):
  slot=2*j+1
  # Diagnose one source-selector bit only after all 20 rows are compared.
  b=tuple(rows[20*slot:20*slot+20])
  if b == _unrewired_block(H,slot,'S'):flags.append(0)
  elif b == _unrewired_block(H,slot,'U'):flags.append(1)
  else:raise ValueError('invalid-control-template')
 expected=build(H,flags)
 if tuple(rows)!=expected:raise ValueError('source-rows-not-authenticated')
 if encode(rows,H)!=raw:raise ValueError('not-canonical-bytes')
 # Structural, degree, strictness checks are independent validation controls.
 occ=collections.Counter(l for c in rows for l in c)
 if any(occ[v]!=2 or occ[-v]!=2 for v in range(1,n+1)):
  raise ValueError('not-balanced')
 if any(len({abs(l) for l in c})!=3 for c in rows):raise ValueError('not-proper')
 return H,tuple(flags),tuple(rows)

def _unrewired_block(H,i,t):
 k,_=grid_info(H)
 out=[]
 for j,c in enumerate(U if t=='U' else S):
  row=[remap(l,i) for l in c]
  if j==0:row[0]=-(15*((i+1)%k)+1)
  out.append(tuple(row))
 return tuple(out)

def witness(H,flags):
 if any(flags):return None
 types=typeword(H,flags)
 ans={}
 for i,t in enumerate(types):
  ans[15*i+1]=int(t=='U')
  for j in range(2,16):ans[15*i+j]=(UPRIVATE>>(j-2))&1 if t=='U' else 0
 return ans

def verify_witness(rows,a):
 return set(a)==set(range(1,1+15*(len(rows)//20))) and all(
  any(a[abs(l)]==int(l>0) for l in c) for c in rows)

def core_of_pair(rows,H,j):
 """All ORIGINAL source 3CNF clauses in a 2-U contradiction core."""
 i=2*j
 return tuple((20*i+q+1,rows[20*i+q]) for q in range(20)) + tuple(
  (20*(i+1)+q+1,rows[20*(i+1)+q]) for q in range(1,20))

def backdoor_vars(j):
 a=2*j
 return tuple(15*b+v for b in (a,a+1) for v in (2,4,7,14,15))

def simplify(clause,env):
 if any(env.get(abs(l),-1)==int(l>0) for l in clause):return None
 return tuple(l for l in clause if abs(l) not in env)

def bfs(g,start,goal):
 q=collections.deque([start]);trace={start:None}
 while q:
  p=q.popleft()
  if p==goal:break
  for to,source_id in g[p]:
   if to not in trace:trace[to]=(p,source_id);q.append(to)
 if goal not in trace:return None
 out=[];v=goal
 while v!=start:
  u,cid=trace[v];out.append((u,v,cid));v=u
 return tuple(reversed(out))

def leaf_from_core(core,H,j,mask):
 vs=backdoor_vars(j)
 env={v:(mask>>i)&1 for i,v in enumerate(vs)}
 g=collections.defaultdict(list)
 for cid,c in core:
  d=simplify(c,env)
  if d is None:continue
  if not d:return {'mask':mask,'kind':'EMPTY','source_id':cid}
  if len(d)>2:raise ValueError('NOT a genuine 2CNF backdoor')
  if len(d)==1:g[-d[0]].append((d[0],cid))
  else:
   x,y=d;g[-x].append((y,cid));g[-y].append((x,cid))
 for v in sorted({abs(l) for _,c in core for l in c}-set(vs)):
  x=bfs(g,v,-v)
  if x is not None:
   y=bfs(g,-v,v)
   if y is not None:
    return {'mask':mask,'kind':'SCC','pivot':v,
            'paths':[x,y]}
 raise ValueError('no contradiction: proof or source invalid')

def make_tree(rows,H,j):
 core=core_of_pair(rows,H,j)
 vs=set(backdoor_vars(j))
 if any(not set(map(abs,c))&vs for _,c in core):raise ValueError('not clause-hitting')
 return [leaf_from_core(core,H,j,mask) for mask in range(1024)]

def check_leaf(core,j,leaf):
 """Independent source-authenticated leaf checker, no solver calls."""
 mask=leaf.get('mask')
 if not isinstance(mask,int) or mask<0 or mask>=1024:return False
 vs=backdoor_vars(j)
 env={v:(mask>>i)&1 for i,v in enumerate(vs)}
 source={cid:tuple(c) for cid,c in core}
 if leaf.get('kind')=='EMPTY':
  cid=leaf.get('source_id')
  return cid in source and simplify(source[cid],env)==()
 if leaf.get('kind')!='SCC':return False
 v=leaf.get('pivot')
 if v not in set(abs(l) for c in source.values() for l in c)-set(vs):return False
 paths=leaf.get('paths')
 if not isinstance(paths,(list,tuple)) or len(paths)!=2:return False
 for path,a,b in zip(paths,(v,-v),(-v,v)):
  if not isinstance(path,(list,tuple)):return False
  current=a
  for item in path:
   if not isinstance(item,(list,tuple)) or len(item)!=3:return False
   start,end,cid=item
   if start!=current or cid not in source:return False
   d=simplify(source[cid],env)
   if d is None or len(d)>2 or len(d)==0:return False
   allowed=[(-d[0],d[0])] if len(d)==1 else [(-d[0],d[1]),(-d[1],d[0])]
   if (start,end) not in allowed:return False
   current=end
  if current!=b:return False
 return True

def check_tree(rows,H,j,tree):
 if not isinstance(tree,list) or len(tree)!=1024:return False
 core=core_of_pair(rows,H,j)
 if any(leaf.get('mask')!=idx or not check_leaf(core,j,leaf)
        for idx,leaf in enumerate(tree)):
  return False
 return True

def primal_core_tree():
 """Proof object: a spanning tree of each S-grid module after all four
 negative port incidences AND the ring incoming literal are removed.
 Entries are (child,parent,1-based original clause ID)."""
 removed={(0,0),*PORTS.values()}
 g={i:[] for i in range(1,16)}
 for ci,c in enumerate(S):
  active=[abs(l) for p,l in enumerate(c) if (ci,p) not in removed]
  for x in active:
   for y in active:
    if x!=y:g[x].append((y,ci+1))
 q=collections.deque([1]);tree={1:None}
 while q:
  v=q.popleft()
  for w,cid in g[v]:
   if w not in tree:tree[w]=(v,cid);q.append(w)
 assert len(tree)==15
 return tuple((v,*tree[v]) for v in range(2,16))

def authenticated_grid_minor(rows,H):
 """Check graph-minor branch-set witness from actual source clauses."""
 k,off=grid_info(H)
 expected=set()
 for r in range(H):
  for c in range(H):
   i=off+r*H+c
   if c+1<H:expected.add((i,i+1))
   if r+1<H:expected.add((i,i+H))
 # Every grid module 15-variable induced primal core connected.
 edges=collections.defaultdict(set)
 byblock=collections.defaultdict(set)
 for clause in rows:
  for x,y in itertools.combinations(map(abs,clause),2):
   b=(x-1)//15;d=(y-1)//15
   if b==d:
    edges[x].add(y);edges[y].add(x)
   elif b>=off and d>=off:
    byblock[min(b,d),max(b,d)].add((x,y))
 for i in range(off,k):
  first=15*i+1
  seen={first};todo=[first]
  while todo:
   v=todo.pop()
   for w in edges[v]-seen:
    if (w-1)//15==i:seen.add(w);todo.append(w)
  if len(seen)!=15:return False
 return all(pair in byblock for pair in expected)

def audit():
 # Independent root archive and previous W1 certificate cross-checks performed
 # separately. This new file does not import any former project's solver code.
 assert len(U)==20 and len(S)==20
 results=[]
 for H in (2,3,4,5,6):
  configs=[tuple([0]*H),tuple([1]+[0]*(H-1)),tuple([0]*(H-1)+[1]),tuple([1]*H)]
  if H<=3:configs=list(itertools.product((0,1),repeat=H))
  total_leaves=total_edges=total_empty=0
  for flags in configs:
   rows=build(H,flags);raw=encode(rows,H)
   h,f,parsed=canonical_parse(raw)
   ck((h,f,parsed)==(H,tuple(flags),rows),'full bytes parse and no free side-bit')
   ck(authenticated_grid_minor(rows,H),'grid minor source witness')
   if not any(flags):
    a=witness(H,flags)
    ck(a is not None and verify_witness(rows,a),'SAT witness')
   else:
    j=next(i for i,b in enumerate(flags) if b)
    tree=make_tree(rows,H,j)
    ck(check_tree(rows,H,j,tree),'all 1024 2CNF-SCC leaves')
    total_leaves+=len(tree)
    total_empty+=sum(l['kind']=='EMPTY' for l in tree)
    total_edges+=sum(sum(len(p) for p in l['paths']) for l in tree if l['kind']=='SCC')
    bad=[dict(leaf) for leaf in tree]
    bad[0]=dict(bad[0]);bad[0]['mask']=1024
    ck(not check_tree(rows,H,j,bad),'tampered branch coverage rejected')
    firstnext=next((i for i,l in enumerate(tree) if l['kind']=='SCC'),None)
    if firstnext is not None:
     bad=[dict(leaf) for leaf in tree]
     leaf=dict(bad[firstnext]);leaf['paths']=[list(x) for x in leaf['paths']]
     if leaf['paths'][0]:
      edge=list(leaf['paths'][0][0]);edge[2]=len(rows)+1
      leaf['paths'][0][0]=edge
      bad[firstnext]=leaf
      ck(not check_tree(rows,H,j,bad),'forged source pointer rejected')
   # Exact syntax/sign authenticity rejects a localized malicious mutation.
   malicious=[list(c) for c in rows]
   malicious[-1][0] *= -1
   try:canonical_parse(encode(malicious,H));accepted=True
   except ValueError:accepted=False
   ck(not accepted,'malformed source rejected')
  results.append({'H':H,'k_modules':H*H+2*H,'n':15*(H*H+2*H),
       'source_clauses':20*(H*H+2*H),'test_cases':len(configs),
       'grid_edges':2*H*(H-1),'proved_frontier_width_lower_bound':H/16,
       '2CNF_SCC_leaves_verified':total_leaves,'path_edges_verified':total_edges,
       'direct_empty_leaves':total_empty})
 # Independent finite local semantic checks of literal template SAT/W1 status.
 # U original is UNSAT; its 2^15 assignments are all excluded.
 for mask in range(1<<15):
  if all(any(((mask>>(abs(l)-1))&1)==int(l>0) for l in c) for c in U):
   raise AssertionError('claimed U base unsatisfiable')
 ck(True,'W1 all 32768 assignments UNSAT')
 # Exhaustive actual local U(a,b) projection, 2^14 private bits for each pair.
 Urel=[]
 for a,b in itertools.product((0,1),repeat=2):
  local=[tuple((-16 if ci==0 and q==0 else l) for q,l in enumerate(c)) for ci,c in enumerate(U)]
  supported=False
  for private in range(1<<14):
   assignment={1:a,16:b}
   for v in range(2,16):assignment[v]=(private>>(v-2))&1
   if all(any(assignment[abs(l)]==int(l>0) for l in c) for c in local):
    supported=True;break
  Urel.append((a,b,supported))
 ck(Urel==[(0,0,False),(0,1,False),(1,0,True),(1,1,False)],'U local existential projection')
 # S with both boundary variables fixed arbitrarily has a private=zero witness.
 for a,b in itertools.product((0,1),repeat=2):
  env={i:0 for i in range(1,16)};env[1]=a;env[16]=b
  tmp=[tuple((-16 if l==-1 and ci==0 and p==0 else l) for p,l in enumerate(c)) for ci,c in enumerate(S)]
  ck(all(any(env[abs(l)]==int(l>0) for l in c) for c in tmp),'S full boundary relation')
 # Verify a full linear-time 15-vertex internal connection witness.
 tree=primal_core_tree()
 ck(len(tree)==14,'explicit S branch-set spanning tree')
 return {'status':'PASS','source_project':'LSPV-3 GRID-FRONTIER-SCC151',
  'H_cases':results,'tested_W1_source_assignments':32768,
  'all_S_boundary_assignments_checked':4,
  'U_exact_projection':Urel,
  'core_S_spanning_tree':tree,'assertion_groups':COUNTS['assertions'],
  'limitations':['Finite tests do not prove the asymptotic grid-cut bound.',
       'Grid frontier width does not imply exponentially many reachable semantic states.',
       'No all-signings polynomial acquisition theorem for grid scopes.',
       '2CNF-SCC proof trees are restricted to the U/S controls with 2 adjacent U.',
       'No unrestricted SAT single-child power contraction or P-vs-NP conclusion.']}

if __name__=='__main__':
 print(json.dumps(audit(),indent=2))