#!/usr/bin/env python3
"""GATE328 compact paid cross-tractable implication, pure Python standard library.
Complete continuation truth tables are OFFLINE assertions, not a solver oracle.
Full independent verifier and resource ledger supplied in GATE328 run archive.
"""
import collections,json
F=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
Z=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-3),(-1,-4,-5),(-2,-4,-6),(-3,-5,-6))
def good(f,n):
 if n%3 or 3*len(f)!=4*n:return False
 count=collections.Counter()
 for cl in f:
  if len(cl)!=3 or len(set(map(abs,cl)))!=3 or not(all(x>0 for x in cl) or all(x<0 for x in cl)) or any(not 1<=abs(x)<=n for x in cl):return False
  for x in cl:count[abs(x),x>0]+=1
 return len(set(tuple(sorted(cl)) for cl in f))==len(f) and all(count[v,s]==2 for v in range(1,n+1) for s in (True,False))
def restrict(f,p):
 out=[]
 for cl in f:
  if any(abs(x) in p and p[abs(x)]==int(x>0) for x in cl):continue
  d=tuple(x for x in cl if abs(x) not in p)
  if not d:return ((),)
  out.append(d)
 return tuple(out)
def kind(r):
 if () in r:return 'FALSE'
 if all(len(c)<=2 for c in r):return '2SAT'
 if all(sum(x>0 for x in c)<=1 for c in r):return 'HORN'
 if all(sum(x<0 for x in c)<=1 for c in r):return 'DUAL'
 return 'GENERAL'
def sat(r,k):
 if () in r:return False
 if not r:return True
 if k in ('HORN','DUAL'):
  rules=[]
  for clause in r:
   c=tuple(-x for x in clause) if k=='DUAL' else clause
   pos=[x for x in c if x>0];assert len(pos)<=1
   rules.append(({abs(x) for x in c if x<0},pos[0] if pos else None))
  forced=set()
  while True:
   change=False
   for antecedents,head in rules:
    if antecedents<=forced:
     if head is None:return False
     if head not in forced:forced.add(head);change=True
   if not change:return True
 if k=='2SAT':
  adj=collections.defaultdict(list);vs=set()
  for c in r:
   if not c:return False
   assert len(c)<=2
   vs.update(map(abs,c))
   if len(c)==1:adj[-c[0]].append(c[0])
   else:
    a,b=c;adj[-a].append(b);adj[-b].append(a)
  seen={};low={};stack=[];on=set();comp={};idx=0;cid=0
  def dfs(v):
   nonlocal idx,cid
   seen[v]=low[v]=idx;idx+=1;stack.append(v);on.add(v)
   for w in adj[v]:
    if w not in seen:dfs(w);low[v]=min(low[v],low[w])
    elif w in on:low[v]=min(low[v],seen[w])
   if low[v]==seen[v]:
    while True:
     w=stack.pop();on.remove(w);comp[w]=cid
     if w==v:break
    cid+=1
  for v in vs:
   for z in (v,-v):
    if z not in seen:dfs(z)
  return all(comp[v]!=comp[-v] for v in vs)
 raise ValueError('unrecognized antecedent')
def entail_clause(r,k,c):
 assumptions={}
 for x in c:
  v=abs(x);z=int(x<0)
  if v in assumptions and assumptions[v]!=z:return True
  assumptions[v]=z
 return not sat(restrict(r,assumptions),k)
def survey(f,n):
 assert good(f,n)
 truth=[all(any(((a>>(abs(x)-1))&1)==int(x>0) for x in c) for c in f) for a in range(1<<n)]
 counts=collections.Counter()
 for S in range(1<<n):
  pv=[v for v in range(1,n+1) if S>>(v-1)&1];fv=[v for v in range(1,n+1) if not S>>(v-1)&1]
  states=[]
  for b in range(1<<len(pv)):
   p={v:(b>>i)&1 for i,v in enumerate(pv)}
   r=restrict(f,p);k=kind(r)
   covered=sum(1<<i for i,c in enumerate(f) if any(abs(x) in p and p[abs(x)]==int(x>0) for x in c))
   co=0
   for y in range(1<<len(fv)):
    a=sum(p[v]<<(v-1) for v in pv)+sum(((y>>i)&1)<<(v-1) for i,v in enumerate(fv))
    if truth[a]:co|=1<<y
   states.append((r,k,covered,co))
  target={c for r,k,b,co in states for c in r}
  cache=[({c for c in target if entail_clause(r,k,c)} if k!='GENERAL' else None) for r,k,b,co in states]
  for i,(pr,pk,pb,pc) in enumerate(states):
   for qr,qk,qb,qc in states:
    counts['pairs']+=1
    if pk=='GENERAL':continue
    counts['eligible']+=1
    yes=all(c in cache[i] for c in qr)
    assert yes==((pc&~qc)==0)
    source=(() in pr) or (() not in qr and (pb&~qb)==0)
    counts['additional']+=yes and not source
    counts['nonzero_additional']+=yes and not source and pc!=0 and qc!=0
    counts['nonzero_to_general']+=yes and not source and pc!=0 and qc!=0 and qk=='GENERAL'
 return {'models':sum(truth),**counts}
z=survey(Z,6);f=survey(F,9)
assert (z['additional'],z['nonzero_additional'])==(1614,642)
assert (f['additional'],f['nonzero_additional'],f['nonzero_to_general'])==(187141,24983,503)
print(json.dumps({'Z6':z,'F9':f,'theorem':'paid 2SAT/Horn/dual-Horn antecedent; offline exhaustive check; P vs NP OPEN'},indent=2))
