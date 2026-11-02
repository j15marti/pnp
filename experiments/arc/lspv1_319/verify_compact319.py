"""LSPV-1 319 independent no-producer-import bitmask truth-table verifier."""
from itertools import product
from collections import Counter
import json
F9=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9)]
Y6=[(1,2,3),(1,4,5),(2,4,6),(3,5,6),
(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6)]
H=F9+[tuple(v+9 if v>0 else v-9 for v in c) for c in Y6]

def truth(F,z):
 return all(any((z[abs(v)]!=0)==(v>0) for v in c) for c in F)

def counts(F,n,x,p):
 free=[v for v in range(1,n+1) if v!=x and v not in p]
 out=[0,0,0]
 for b in product((0,1),repeat=len(free)):
  z={**p,**dict(zip(free,b))}
  z[x]=0;u=truth(F,z)
  z[x]=1;v=truth(F,z)
  out[0]+=u;out[1]+=v;out[2]+=(u!=v)
 return out
ps={1:0,3:0,5:1,6:0,7:0,8:0};pu={**ps,1:1}
checks={
 'Y6':counts(Y6,6,1,{}),
 'F9':counts(F9,9,1,{}),
 'F9_forward_reverse':counts(F9,9,7,{2:0,3:0,6:1}),
 'H15':counts(H,15,10,{}),
 'H15_S':counts(H,15,10,ps),
 'H15_U':counts(H,15,10,pu)}
assert checks=={'Y6':[10,10,12],'F9':[40,30,46],
 'F9_forward_reverse':[0,1,1],'H15':[700,700,840],
 'H15_S':[20,20,24],'H15_U':[0,0,0]}
assert checks['H15'][2]==70*checks['Y6'][2]
assert checks['H15_S'][2]==2*checks['Y6'][2]
assert checks['H15_U'][2]==0
assert 3*len(F9)==4*9 and 3*len(Y6)==4*6 and 3*len(H)==4*15
print(json.dumps({'independent_source_truth_tables':'PASS','counts':checks,
 'assertions':'all 6 full suffix truth tables and disjoint-product factors verified'},indent=2,sort_keys=True))
