#!/usr/bin/env python3
"""Stdlib independent spotchecker of LSPV-2 CORRIDORS241.
Full experiment, source-indexed raw and benchmark live in downloadable ZIP.
This small checker verifies source satisfiability, exact occurrence quotas,
minimum hitting-set size, 2SAT implication certificates, and complement
partition. It does not claim an unrestricted SAT running-time lower bound.
"""
import itertools,collections
W1='-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'
S='-1 -3 14;2 8 -9;-10 13 14;3 -7 -13;-4 9 -11;-5 -8 -14;4 -8 11;1 7 -13;1 -7 10;-5 -6 15;-2 6 -12;4 9 -10;-2 5 -12;3 6 -15;-6 7 11;2 -9 -11;-4 8 10;-3 12 15;5 12 -15;-1 13 -14'
M='1 3 14;2 -8 -9;-10 -13 -14;3 -7 -13;4 9 11;-5 -8 14;4 8 11;-1 7 13;-1 7 -10;-5 6 15;-2 6 -12;-4 9 10;2 5 12;-3 -6 -15;-6 -7 -11;-2 -9 -11;-4 8 10;-3 12 15;5 -12 -15;1 13 -14'
def parse(s):return tuple(tuple(map(int,x.split())) for x in s.split(';'))
def cyc(n):
 return tuple((i+1,(i+1)%n+1,-((i+2)%n+1)) for i in range(n))+tuple(tuple(-(3*j+t+1) for t in range(3)) for j in range(n//3))
def sat(F,a):return all(any(a[abs(x)]==int(x>0) for x in c) for c in F)
def check_original(n,F):
 assert all(len(c)==3 and len({abs(x) for x in c})==3 for c in F)
 count=collections.Counter(x for c in F for x in c)
 assert len(F)==4*n//3 and all(count[x]==count[-x]==2 for x in range(1,n+1))
 graph={i:set() for i in range(1,n+1)}
 for c in F:
  for a,b in itertools.combinations(map(abs,c),2):graph[a].add(b);graph[b].add(a)
 seen={1};queue=[1]
 for v in queue:
  for w in graph[v]-seen:seen.add(w);queue.append(w)
 assert len(seen)==n
 # Original occurrence indexed targets, no made-up occurrence variables.
 for j,c in enumerate(F,1):
  for x in c:
   Sp=int(x>0);Up=int(x<0)
   assert Sp==1-Up and int(1-Sp)==Up and int(1-Up)==Sp
 for j,k in itertools.combinations(range(len(F)),2):
  a={abs(x):int(x>0) for x in F[j]}
  b={abs(x):int(x>0) for x in F[k]}
  same=any(a[v]==b[v] for v in set(a)&set(b))
  opposite=any(a[v]!=b[v] for v in set(a)&set(b))
  expected=(not opposite,not same,not same,not opposite)
  vals=[]
  variables=sorted(set(a)|set(b))
  for u,v in ((3,3),(3,0),(0,3),(0,0)):
   exists=False
   for bits in itertools.product((0,1),repeat=len(variables)):
    z=dict(zip(variables,bits))
    if (sum(z[abs(x)]==int(x>0) for x in F[j])==u and
        sum(z[abs(x)]==int(x>0) for x in F[k])==v):
     exists=True;break
   vals.append(exists)
  assert tuple(vals)==expected
def min_hit(n,F):
 for k in range(n+1):
  for B in itertools.combinations(range(1,n+1),k):
   if all(set(B)&set(map(abs,c)) for c in F):return B
def key(x):return 2*(abs(x)-1)+int(x<0)
def unkey(v):return (v//2+1)*(1 if v%2==0 else -1)
def path(g,start,end):
 q=collections.deque([key(start)]);prev={key(start):None}
 while q:
  v=q.popleft()
  if v==key(end):break
  for w,j in g[v]:
   if w not in prev:prev[w]=(v,j);q.append(w)
 assert key(end) in prev
 out=[];u=key(end)
 while u!=key(start):
  v,j=prev[u];out.append((unkey(v),unkey(u),j));u=v
 return list(reversed(out))
def twosat(F,n,pin):
 g=[[] for _ in range(2*n)];r=[[] for _ in range(2*n)];active=[]
 def edge(a,b,j):
  g[key(a)].append((key(b),j));r[key(b)].append((key(a),j))
 for j,c in enumerate(F,1):
  if any(abs(x) in pin and pin[abs(x)]==int(x>0) for x in c):continue
  live=[x for x in c if abs(x) not in pin]
  assert len(live)<=2
  if not live:return False,('source_false',j)
  active.append(j)
  if len(live)==1:edge(-live[0],live[0],j)
  else:a,b=live;edge(-a,b,j);edge(-b,a,j)
 # Kosaraju with loop stack to avoid recursion limit.
 used=set();order=[]
 for i in range(2*n):
  stack=[(i,0)]
  while stack:
   v,phase=stack.pop()
   if phase:order.append(v);continue
   if v in used:continue
   used.add(v);stack.append((v,1))
   for w,_ in g[v]:
    if w not in used:stack.append((w,0))
 component=[-1]*(2*n);cc=0
 for i in reversed(order):
  if component[i]>=0:continue
  q=[i];component[i]=cc
  while q:
   v=q.pop()
   for w,_ in r[v]:
    if component[w]<0:component[w]=cc;q.append(w)
  cc+=1
 for v in range(1,n+1):
  if v in pin:continue
  if component[key(v)]==component[key(-v)]:
   p=path(g,v,-v);q=path(g,-v,v)
   for chain in (p,q):
    for a,b,j in chain:
     c=F[j-1]
     assert not any(abs(x) in pin and pin[abs(x)]==int(x>0) for x in c)
     live=[x for x in c if abs(x) not in pin]
     assert ((len(live)==1 and (a,b)==(-live[0],live[0])) or
             (len(live)==2 and (a,b) in ((-live[0],live[1]),(-live[1],live[0]))))
   return False,('two_source_paths',v,p,q)
 a=dict(pin)
 for v in range(1,n+1):
  if v not in a:a[v]=int(component[key(v)]>component[key(-v)])
 assert sat(F,a)
 return True,a
def run(label,F):
 n=15;check_original(n,F)
 B=min_hit(n,F);assert len(B)==5
 outcome={};retained={}
 for mask in range(32):
  pin={v:mask>>i&1 for i,v in enumerate(B)}
  outcome[mask],cert=twosat(F,n,pin)
  retained[mask]={j for j,c in enumerate(F) if not any(abs(x) in pin and pin[abs(x)]==int(x>0) for x in c)}
  assert len(retained[mask])==10
 for i in range(16):
  assert not retained[i]&retained[31-i] and len(retained[i]|retained[31-i])==20
 models=sum(sat(F,{i+1:(mask>>i)&1 for i in range(n)}) for mask in range(1<<n))
 assert (models!=0)==any(outcome.values())
 print(label,'B',B,'model_count',models,'SAT_pins',sum(outcome.values()),
       'complement_outcome_disagreements',sum(outcome[i]!=outcome[31-i] for i in range(16)))
 return outcome
if __name__=='__main__':
 w=run('W1 UNSAT',parse(W1));assert not any(w.values())
 s=run('S SAT',parse(S));assert sum(s.values())==32
 m=run('balanced mutation SAT',parse(M));assert sum(m.values())==30 and not m[10] and m[21]
 c=run('cyclic SAT',cyc(15));assert sum(c.values())==32
 print('ALL STRICT22 SOURCE, EXTREME, SCC AND COMPLEMENT CHECKS PASS; P-vs-NP OPEN')
