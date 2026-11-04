#!/usr/bin/env python3
"""LSPV4/382: finite independent check of two cut-width transfer counterexamples.
Stdlib only, deterministic; outputs a JSON summary. Proof-system hardness is not tested.
"""
import json,itertools
checks=0
def req(x,m):
 global checks
 checks+=1
 if not x: raise AssertionError(m)
def php(h,drop=False):
 p=lambda i,j:i*h+j+1
 f=[[p(i,j) for j in range(h)] for i in range(h+1)]
 f += [[-p(i,j),-p(k,j)] for j in range(h) for i in range(h+1) for k in range(i+1,h+1)]
 return (h*(h+1),f[1:] if drop else f)
def cnf(f,a):
 return all(any((bool((a>>(abs(l)-1))&1)==(l>0)) for l in c) for c in f)
def circuit(n,f):
 g=[]; add=lambda op,ins:(g.append((op,ins)),n+len(g))[1]
 roots=[]
 for c in f:
  t=[abs(l) if l>0 else add('NOT',[abs(l)]) for l in c]
  a=t[0]
  for b in t[1:]:a=add('OR',[a,b])
  roots.append(a)
 r=roots[0]
 for b in roots[1:]:r=add('AND',[r,b])
 one=add('ONE',[]);o=add('AND',[r,one])
 return g,r,o
def run(n,g,mask):
 v={i+1:(mask>>i)&1 for i in range(n)}
 for idx,(op,parents) in enumerate(g):
  q=[v[k] for k in parents]
  if op=='AND':v[n+idx+1]=q[0]&q[1]
  elif op=='OR':v[n+idx+1]=q[0]|q[1]
  elif op=='NOT':v[n+idx+1]=1-q[0]
  elif op=='ONE':v[n+idx+1]=1
  else:raise ValueError('bad op')
 return v
summary={'rank_one':[],'php':[]}
for w in [2,3,4,8,16,32,64]:
 for unsat in [False,True]:
  # Each z_i is a separate AND(x,x), each is actually fed to downstream.
  n=1;g=[('AND',[1,1]) for _ in range(w)];z=list(range(2,w+2));t=z[0]
  for a in z[1:]:
   g.append(('AND',[t,a]));t=n+len(g)
  if unsat:g.append(('NOT',[z[0]]));t2=n+len(g);g.append(('AND',[t,t2]))
  else:g.append(('ONE',[]));t2=n+len(g);g.append(('AND',[t,t2]))
  out=n+len(g);states=set();models=0
  for x in [0,1]:
   values=run(n,g,x);state=tuple(values[k] for k in z)
   req(state==(x,)*w,'alias states')
   states.add(state); models+=values[out]
  req(len(states)==2 and (models>0)==(not unsat),'two-label truth')
  summary['rank_one'].append({'w':w,'label':'UNSAT' if unsat else 'SAT','reachable':len(states),'naive':str(1<<w)})
for h in [1,2,3]:
 for deletion in [False,True]:
  n,f=php(h,deletion);g,root,out=circuit(n,f)
  req(out==n+len(g) and len(g)>1,'wrapper shape')
  sat=False
  for a in range(1<<n):
   cv=run(n,g,a)[out];want=cnf(f,a)
   req(bool(cv)==want,'all-input evaluator equality')
   sat |=want
  req(sat==deletion,'PHP/delete labels')
  summary['php'].append({'h':h,'deleted':deletion,'clauses':len(f),'literals':sum(map(len,f)),'upstream_gates':len(g)-2,'cut_width':1,'sat':sat})
# Deliberately damaged grammar record and invalid source controls.
bad=[('XOR',[1,1]),('AND',[1,999]),('NOT',[]),('ONE',[1])]
for op,parents in bad:
 valid=op in ('AND','OR','NOT','ONE') and len(parents)=={'AND':2,'OR':2,'NOT':1,'ONE':0}.get(op,-1) and all(0<x<2 for x in parents)
 req(not valid,'malformed gate rejection')
summary['assertion_groups']=checks
print(json.dumps(summary,sort_keys=True))
