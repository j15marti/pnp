#!/usr/bin/env python3
"""Existential bitonic consistency circuit. Each mode: timeout 25s."""
import itertools,json,hashlib,signal,sys
from collections import Counter
from pathlib import Path
signal.alarm(24)
class Circuit:
 def __init__(self):self.n=0;self.cnf=[];self.gates=[];self.fixed={};self.inputs=[];self.blocks=[]
 def var(self):self.n+=1;return self.n
 def constant(self,v):
  z=self.var();self.fixed[z]=v;self.cnf.append((z if v else -z,));return z
 def gate(self,op,*xs):
  z=self.var();self.gates.append((z,op,xs))
  # Complete truth-table gate equivalence, with duplicate/tautological literals simplified.
  for bits in itertools.product((0,1),repeat=len(xs)):
   val=calc(op,bits)
   clause=tuple((-x if b else x) for x,b in zip(xs,bits))+(z if val else -z,)
   if not any(-x in clause for x in clause):self.cnf.append(tuple(dict.fromkeys(clause)))
  return z
 def trace(self,values):
  a=dict(self.fixed);a.update(zip(self.inputs,values))
  for z,op,xs in self.gates:a[z]=calc(op,[a[abs(x)] if x>0 else 1-a[-x] for x in xs])
  return a
def calc(op,b):
 if op=='and':return int(all(b))
 if op=='or':return int(any(b))
 if op=='eq':return int(b[0]==b[1])
 if op=='mux':return b[2] if b[0] else b[1]
 raise ValueError(op)
def holds(cnf,a):return all(any(a[abs(x)]==(x>0) for x in c) for c in cnf)
def build(F):
 m=len(F);L=3*m;P=1<<(L-1).bit_length();n=max(abs(x) for c in F for x in c);sentinel=n+1;w=sentinel.bit_length();C=Circuit();records=[]
 for i in range(P):
  key=abs(F[i//3][i%3]) if i<L else sentinel
  kb=[C.constant((key>>b)&1) for b in range(w-1,-1,-1)]
  if i<L:v=C.var();C.inputs.append(v)
  else:v=C.constant(0)
  records.append((kb,v))
 for j,c in enumerate(F):C.cnf.append(tuple(C.inputs[3*j+k]*(1 if x>0 else -1) for k,x in enumerate(c)))
 source_clauses=list(C.cnf)
 comparisons=0;k=2
 while k<=P:
  j=k//2
  while j:
   new=list(records)
   for i in range(P):
    other=i^j
    if other<i:continue
    start=len(C.cnf);left,right=records[i],records[other];eq=C.constant(1);gt=C.constant(0);asc=(i&k)==0
    for a,b in zip(left[0],right[0]):
     term=C.gate('and',a,-b) if asc else C.gate('and',-a,b)
     gt=C.gate('or',gt,C.gate('and',eq,term));eq=C.gate('and',eq,C.gate('eq',a,b))
    lo=[C.gate('mux',gt,a,b) for a,b in zip(left[0]+[left[1]],right[0]+[right[1]])]
    hi=[C.gate('mux',gt,b,a) for a,b in zip(left[0]+[left[1]],right[0]+[right[1]])]
    new[i]=(lo[:-1],lo[-1]);new[other]=(hi[:-1],hi[-1]);comparisons+=1;C.blocks.append((start,len(C.cnf)))
   records=new;j//=2
  k*=2
 constraints=[]
 for (ak,av),(bk,bv) in zip(records,records[1:]):
  eq=C.constant(1)
  for a,b in zip(ak,bk):eq=C.gate('and',eq,C.gate('eq',a,b))
  constraints.extend([(-eq,-av,bv),(-eq,av,-bv)])
 C.cnf.extend(constraints)
 return C,records,dict(m=m,records=P,key_bits=w,comparators=comparisons,variables=C.n,clauses=len(C.cnf),max_width=max(map(len,C.cnf)),max_occ=max(Counter(abs(x) for c in C.cnf for x in c).values())),constraints
def direct(F,vals):
 seen={}
 for i,v in enumerate(vals):
  x=abs(F[i//3][i%3])
  if x in seen and seen[x]!=v:return False
  seen[x]=v
 return all(any(vals[3*j+k]==(x>0) for k,x in enumerate(c)) for j,c in enumerate(F))
def audit(F,all_occ=False):
 C,records,meta,cons=build(F);N=3*len(F);checks=0;accepted=0
 samples=itertools.product((0,1),repeat=N) if all_occ else ([int(mask>>abs(x)-1&1) for c in F for x in c] for mask in range(1<<max(abs(x) for c in F for x in c)))
 for vals in samples:
  vals=list(vals);a=C.trace(vals);actual=holds(C.cnf,a);expected=direct(F,vals);assert actual==expected
  keys=[sum(a[v]<<(len(k)-1-b) for b,v in enumerate(k)) for k,_ in records];assert keys==sorted(keys)
  expected_pairs=sorted([(abs(x),vals[i]) for i,x in enumerate(x for c in F for x in c)]+[(max(abs(x) for c in F for x in c)+1,0)]*(len(records)-N))
  pairs=sorted(zip(keys,[a[v] for _,v in records]));assert pairs==expected_pairs
  checks+=1;accepted+=actual
 return dict(**meta,assignments=checks,accepted=accepted)
def gates():
 cases=0
 for op,arity in [('and',2),('or',2),('eq',2),('mux',3)]:
  for signs in itertools.product((-1,1),repeat=arity):
   C=Circuit();xs=[C.var() for _ in range(arity)];z=C.gate(op,*[s*x for s,x in zip(signs,xs)])
   for bits in itertools.product((0,1),repeat=arity):
    target=calc(op,[b if s>0 else 1-b for b,s in zip(bits,signs)])
    for out in (0,1):assert holds(C.cnf,dict(zip(xs,bits))|{z:out})==(out==target);cases+=1
 # Full gate constraints are necessary: drop gate definitions, keep keys, clauses and adjacency.
 F=list(itertools.product((-1,1),(-2,2),(-3,3)));C,records,meta,cons=build(F)
 a={v:0 for v in range(1,C.n+1)};a.update(C.fixed)
 for i,x in enumerate(x for c in F for x in c):a[C.inputs[i]]=int(x>0)
 assert holds(cons,a)
 assert all(any(a[C.inputs[3*j+k]]==(x>0) for k,x in enumerate(c)) for j,c in enumerate(F))
 assert not holds(C.cnf,a)
 return dict(gate_truth_checks=cases,unconstrained_sort_false_sat=True)
mode=sys.argv[1] if len(sys.argv)>1 else 'small'
if mode=='gates':result=gates()
elif mode=='small':result=[audit([(1,2,3)],True),audit([(1,2,3),(-1,-2,-3)],True),audit([(1,2,3),(1,-2,3)],True),audit([(1,2,3),(1,2,3)],True)]
elif mode=='controls':
 cs=list(itertools.product((-1,1),(-2,2),(-3,3)))
 result=[audit(cs),audit(cs[:-1]),audit([(1,2,3),(-1,-2,-3),(1,-2,-3),(-1,2,3)])]
elif mode=='scale':result=[build([(3*j+1,3*j+2,3*j+3) for j in range(m)])[2] for m in [1,2,4,8,16,32]]
else:raise ValueError(mode)
print(json.dumps(dict(status='PASS',mode=mode,code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),result=result),indent=2))
