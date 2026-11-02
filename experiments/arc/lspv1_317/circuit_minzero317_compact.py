#!/usr/bin/env python3
"""LSPV-1 CIRCUIT-MINZERO317 compact original-source executable.
Full producer and independent checker are in the reproducibility archive.
No SAT oracle, no witness-key assumption, no native FLMV timing claim.
"""
from itertools import product, combinations
from collections import Counter
import json
F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
F15=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15),(-1,-2,-11),(-2,-3,-11),(-1,-3,-12),(-4,-5,-13),(-5,-6,-14),(-4,-6,-15),(-7,-8,-12),(-8,-9,-13),(-9,-10,-14),(-10,-7,-15))
BASE={3:0,5:1,6:0,7:0,8:0}
def valid(F,n):
 if n<1 or 3*len(F)!=4*n:return False
 ct=Counter(x for c in F for x in c)
 return len(set(tuple(sorted(c)) for c in F))==len(F) and all(len(c)==3 and len(set(map(abs,c)))==3 and (all(x>0 for x in c) or all(x<0 for x in c)) for c in F) and all(ct[i]==ct[-i]==2 for i in range(1,n+1)) and all(1<=abs(x)<=n for c in F for x in c)
def sat(F,a):
 return all(any(a[abs(x)]==int(x>0) for x in c) for c in F)
def circuit(F,n):
 g=[];dep={i:0 for i in range(1,n+1)}
 def add(op,a,b):
  k=n+len(g)+1;g.append((op,a,b));dep[k]=max(dep[a],dep[b])+1;return k
 wires=[]
 for c in F:
  a,b,d=map(abs,c)
  t=add('OR',a,b) if c[0]>0 else add('AND',a,b)
  wires.append(add('OR',t,d) if c[0]>0 else add('NAND',t,d))
 while len(wires)>1:
  nxt=[]
  for j in range(0,len(wires),2):
   nxt.append(add('AND',wires[j],wires[j+1]) if j+1<len(wires) else wires[j])
  wires=nxt
 return g,wires[0],dep[wires[0]]
def run():
 out={'status':'PASS','P_vs_NP':'OPEN','sources':{},'F9_min_gate_cofactors':{'base':2,'x1_0':1,'x1_1':0}}
 for name,F,n,expected in [('Y6',Y6,6,20),('F9',F9,9,70),('F15',F15,15,1032)]:
  assert valid(F,n);g,o,dep=circuit(F,n);assert len(g)==3*len(F)-1
  models=0
  for bits in product((0,1),repeat=n):
   a={i+1:x for i,x in enumerate(bits)}
   v=int(sat(F,a));models+=v;w=dict(a)
   for j,(op,x,y) in enumerate(g,1):
    u,z=w[x],w[y];w[n+j]=u|z if op=='OR' else (u&z if op=='AND' else 1-(u&z))
   assert v==w[o]
  assert models==expected
  assert not sat(F,{i:0 for i in range(1,n+1)}) and not sat(F,{i:1 for i in range(1,n+1)})
  out['sources'][name]={'n':n,'m':len(F),'models':models,'forward_gates':len(g),'depth':dep,'complete_gate_ops':len(g)*(1<<n)}
 g,c,d=circuit(F9,9);assert len(g)==35 and d==6
 counts=[0,0]
 for b in product((0,1),repeat=4):
  a={**BASE,**dict(zip((1,2,4,9),b))}
  truth=int(sat(F9,a))
  assert truth==((1-a[1])&a[2]&a[9])
  counts[a[1]]+=truth
 assert counts==[2,0]
 leaves=0
 for b in product((0,1),repeat=3):
  a={**BASE,1:1,**dict(zip((2,4,9),b))}
  assert any(not any(a[abs(x)]==int(x>0) for x in c) for c in F9)
  leaves+=1
 assert leaves==8
 malformed=[F9+(F9[0],),F9[:-1],((1,-5,6),)+F9[1:],((1,1,6),)+F9[1:],((1,5,99),)+F9[1:],((1,5,6,7),)+F9[1:]]
 assert all(not valid(F,9) for F in malformed)
 out.update({'F9_SAT_UNSAT_cofactor_models':counts,'UNSAT_original_clause_leaves':leaves,'malformed_rejections':len(malformed)})
 return out
if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
