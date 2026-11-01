#!/usr/bin/env python3
"""Compact independent-source F9 check for LSPV-3 GATE313.
Full 19,170-state / 835,905-pair census has a distinct no-import verifier
in the archived reproducibility bundle. This script is deliberately small.
"""
from itertools import combinations,product
from collections import Counter
import json
positive=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9)]
negative=[(4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9)]
F=[tuple(c) for c in positive]+[tuple(-x for x in c) for c in negative]
p={2:1,3:0,5:1,6:0,8:0}
q={2:0,3:1,5:1,6:1,8:0}
r={1:1,7:0}
assert len(F)==12 and len({tuple(sorted(c)) for c in F})==12
assert all(len(set(map(abs,c)))==3 and (all(z>0 for z in c) or all(z<0 for z in c)) for c in F)
assert all(sum(x in c for c in F)==2 and sum(-x in c for c in F)==2 for x in range(1,10))
def good(a):
    return all(any(((a>>(abs(z)-1))&1)==int(z>0) for z in clause) for clause in F)
models=[a for a in range(1<<9) if good(a)]
def count(pins):
    return sum(all((a>>(i-1)&1)==v for i,v in pins.items()) for a in models)
assert len(models)==70
free=sorted(set(range(1,10))-set(p))
marginals={str(i):[count({**p,i:0}),count({**p,i:1})] for i in free}
assert marginals=={str(i):[count({**q,i:0}),count({**q,i:1})] for i in free}
assert marginals=={'1':[3,1],'4':[1,3],'7':[2,2],'9':[2,2]}
assert [count(p),count(q),count({**p,**r}),count({**q,**r})]==[4,4,0,1]
assert any(a==317 and good(a) and all((a>>(i-1)&1)==v for i,v in {**q,**r}.items()) for a in models)
assert all(not all(abs(z) in {**p,**r} and {**p,**r}[abs(z)]!=int(z>0) for z in c) for c in F)
assert F[5]==(7,8,9) and F[10]==(-1,-2,-9)
compatibility=0
for i,j in combinations(range(12),2):
    for u,v in product('SU',repeat=2):
        want={}
        possible=True
        for cl,mode in ((F[i],u),(F[j],v)):
            for z in cl:
                val=int((z>0)==(mode=='S'))
                if abs(z) in want and want[abs(z)]!=val:possible=False
                want[abs(z)]=val
        # Independent check against every complete global assignment.
        brute=any(all(((a>>(abs(z)-1))&1)==int((z>0)==(mode=='S')) for cl,mode in ((F[i],u),(F[j],v)) for z in cl) for a in range(512))
        assert possible==brute
        compatibility+=1
assert compatibility==264
print(json.dumps({'run':'GATE313','F9_models':len(models),'pins_p':p,'pins_q':q,'future':r,
  'p_and_q_model_counts':[count(p),count(q)],
  'single_pin_marginals':marginals,'two_pin_models':[count({**p,**r}),count({**q,**r})],
  'UNSAT_source_UP':'C6 forces x9=1; C11 contradicts',
  'SAT_original_witness_bitmask':317,'SS_SU_US_UU_checked':compatibility,
  'P_vs_NP':'OPEN'},sort_keys=True,indent=2))
