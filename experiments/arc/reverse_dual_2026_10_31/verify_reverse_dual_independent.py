#!/usr/bin/env python3
"""Independent bitmask verifier: no imports from reverse_dual_exact.py."""
from itertools import product
from collections import Counter
import json

C=((1,2,3),(1,4,5),(2,4,6),(3,5,6),
   (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
def satisfies(mask):
    for clause in C:
        if not any(bool(mask & (1<<(abs(lit)-1))) == (lit>0) for lit in clause):
            return False
    return True
models={a for a in range(64) if satisfies(a)}
assert len(models)==20
assert not satisfies(0) and not satisfies(63)
# Precompute compatible complete assignments using a separate integer-mask encoding.
def admissible(mask,p):
    return all(v==-1 or bool(mask & (1<<i))==bool(v)
               for i,v in enumerate(p))
truth={}
for p in product((-1,0,1),repeat=6):
    truth[p]=any(admissible(a,p) for a in models)
assert Counter(truth.values())=={True:529,False:200}
checked=0
for p,val in truth.items():
    for i in range(6):
        if p[i]!=-1:continue
        q=p[:i]; tail=p[i+1:]
        x,y=truth[q+(0,)+tail],truth[q+(1,)+tail]
        assert val==(x or y)
        assert (not val)==((not x) and (not y))
        checked+=1
assert checked==1458
unsat=(-1,0,1,0,0,-1)
sat=(-1,0,1,0,1,-1)
assert not truth[unsat] and truth[sat]
# The source constraints surviving the two cubes, verified clause-by-clause.
def live(p):
    out=[]
    for j,c in enumerate(C,1):
        if any(p[abs(l)-1]==int(l>0) for l in c): continue
        out.append((j,tuple(l for l in c if p[abs(l)-1]==-1)))
    return out
assert live(unsat)==[(2,(1,)),(3,(6,)),(6,(-1,-6))]
assert live(sat)==[(3,(6,)),(6,(-1,-6))]
# SAT source copy with x1=0 has exactly 10 models.
fixed0=sum(1 for a in models if (a&1)==0)
assert fixed0==10
print(json.dumps({"status":"PASS","independent":True,"all_models":20,
   "SAT_residuals":529,"UNSAT_residuals":200,
   "cofactor_tests":checked,"SAT_cube":list(sat),
   "UNSAT_cube":list(unsat),"gadget_x1_0_models":fixed0,
   "two_copy_gadget_models":20*fixed0},sort_keys=True))
if __name__=="__main__": pass
