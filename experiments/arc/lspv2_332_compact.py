#!/usr/bin/env python3
"""LSPV-2 POLARITY-DIRECTED-CIRCUIT-SAT332 self-contained original-source demo.
Python standard library only; complete two independent verifiers and optimized
matched-gate DAG data are provided in the user-facing reproducibility archive.
NOT a SAT decision-time lower bound.
"""
from collections import Counter
from itertools import product
Y6=[[1,2,3],[1,4,5],[2,4,6],[3,5,6],[-1,-2,-4],[-1,-3,-6],[-2,-3,-5],[-4,-5,-6]]
F9=[[1,5,6],[2,3,8],[1,3,5],[4,6,9],[2,4,7],[7,8,9],[-4,-6,-8],[-1,-6,-7],[-2,-3,-4],[-3,-5,-8],[-1,-2,-9],[-5,-7,-9]]
def valid(F,n):
 a=Counter(x for C in F for x in C)
 return 3*len(F)==4*n and len({tuple(sorted(C)) for C in F})==len(F) and all(len(C)==3 and len({abs(x) for x in C})==3 and all(x*C[0]>0 for x in C) for C in F) and all(a[i]==a[-i]==2 for i in range(1,n+1))
def compile_source(F,n):
 G=[];outputs=[]
 def gate(op,a,b):
  z=n+len(G)+1;G.append((op,a,b,z));return z
 for C in F:outputs.append(gate('OR',gate('OR',C[0],C[1]),C[2]))
 while len(outputs)>1:outputs=[gate('AND',outputs[k],outputs[k+1]) if k+1<len(outputs) else outputs[k] for k in range(0,len(outputs),2)]
 return G,outputs[0]
def pg(G,root):
 by={z:(op,a,b) for op,a,b,z in G};seen=set();queue=[root];T=[]
 while queue:
  z=queue.pop()
  if z in seen:continue
  seen.add(z);op,a,b=by[z]
  T.extend([(-z,a),(-z,b)] if op=='AND' else [(-z,a,b)])
  for q in (a,b):
   if abs(q) in by:queue.append(abs(q))
 T.append((root,));return T
def source(F,mask):
 return int(all(any(((mask>>(abs(q)-1))&1)==int(q>0) for q in C) for C in F))
def trace(G,mask,n):
 v={i:(mask>>(i-1))&1 for i in range(1,n+1)}
 for op,a,b,z in G:
  x=v[abs(a)] if a>0 else 1-v[-a]
  y=v[abs(b)] if b>0 else 1-v[-b]
  v[z]=x&y if op=='AND' else x|y
 return v
for name,F,n in [('Y6',Y6,6),('F9',F9,9)]:
 assert valid(F,n)
 G,root=compile_source(F,n);T=pg(G,root)
 assert len(G)==3*len(F)-1 and len(T)==4*len(F)-1
 for x in range(1<<n):
  v=trace(G,x,n)
  assert v[root]==source(F,x)
  if v[root]:assert all(any(v[abs(q)] if q>0 else 1-v[-q] for q in C) for C in T)
 print(name,'models',sum(source(F,x) for x in range(1<<n)),'gates',len(G),'PG clauses',len(T),'full Tseitin clauses',3*len(G)+1)
for b,expected in ((0,2),(1,0)):
 pins={1:b,3:0,5:1,6:0,7:0,8:0};count=0
 for x2,x4,x9 in product((0,1),repeat=3):
  a={**pins,2:x2,4:x4,9:x9}
  count+=source(F9,sum(a[i]<<(i-1) for i in range(1,10)))
 assert count==expected
 print('F9 same original pinned x1',b,'completions',count)
print('P versus NP OPEN')
