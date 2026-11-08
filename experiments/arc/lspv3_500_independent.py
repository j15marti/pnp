from itertools import product
from pathlib import Path
import hashlib, json

# Independent finite original-variable semantic controls for LSPV-3/500.
# Not a historical R_mix341 checker.
def block(a, positions):
    return tuple(-i if a[i-1] else i for i in positions)

def P(a): return (a[0] & a[1]) ^ a[2] == 0
def Q(a): return a[2] ^ a[1] == 0
def C(a): return (a[0] & a[1]) ^ a[1] == 0
def sat(c,a):
    return any(a[abs(i)-1] == (1 if i>0 else 0) for i in c)

A=list(product((0,1),repeat=3))
Pcls={block(a,(1,2,3)) for a in A if not P(a)}
Qcls={block(a,(2,3)) for a in A if not Q(a)}
Ccls={block(a,(1,2)) for a in A if not C(a)}
assert len(Pcls)==4 and len(Qcls)==2 and Ccls=={(1,-2)}
base=Pcls|Qcls
full=base|{(-1,),(2,)}
assert sorted(''.join(map(str,a)) for a in A if all(sat(c,a) for c in base)) == ['000','100','111']
assert not [a for a in A if all(sat(c,a) for c in full)]
assert all(not (P(a) and Q(a)) or C(a) for a in A)
for t,source,other in [(0,Qcls,Pcls),(1,Pcls,Qcls)]:
    a=(0,1,t)
    assert not C(a) and any(not sat(c,a) for c in source)
    assert all(sat(c,a) for c in other)
assert (1,-2,-3) in Pcls and (-2,3) in Qcls
assert (1,-2) == tuple(sorted((set((1,-2,3))-{3})|(set((1,-2,-3))-{-3}),key=abs))
assert any(not C(a) and all(sat(c,a) for c in base-{(-2,3)}) for a in A)
assert any(not C(a) and all(sat(c,a) for c in base-{(1,-2,-3)}) for a in A)
output={'status':'PASS','independent':'Python truth-table checker; no JS module import',
'original_variables':3,'P_clauses':4,'Q_clauses':2,'projected_C_clauses':1,
'base_models':['000','100','111'],'full_unsat':True,
'mandatory_Q_branch':'010','mandatory_P_branch':'011',
'original_source_clauses':8,'WEAKEN':1,'RES':3,'paid_nodes':4,
'scope':'distinct canonical-support bounded-cone GF2 macro only'}
print(json.dumps(output,sort_keys=True,indent=2))
