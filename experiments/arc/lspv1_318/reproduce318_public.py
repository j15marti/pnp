#!/usr/bin/env python3
"""Reproduce LSPV-1 318 on one valid canonical source (stdlib only)."""
from itertools import product
from collections import Counter
import json
F=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
   (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9)]

def clause(c,a):return any(a[abs(x)]==int(x>0) for x in c)
def profile(p):
    w=[]; dead=[]
    for j,c in enumerate(F,1):
        if any(abs(x) in p and p[abs(x)]==int(x>0) for x in c):w.append(0)
        else:
            free=sum(abs(x) not in p for x in c)
            w.append(free)
            if free==0:dead.append(j)
    return w,dead

def models(p):
    free=[x for x in range(1,10) if x not in p];good=[];bad=[]
    for vals in product((0,1),repeat=len(free)):
        a={**p,**dict(zip(free,vals))}
        first=next((i for i,c in enumerate(F,1) if not clause(c,a)),None)
        if first is None:good.append(''.join(map(str,(a[x] for x in range(1,10)))))
        else:bad.append(first)
    return good,bad

p={2:0,3:0,6:1}
ans={}
for tag,q in [('parent',p),('SAT',{**p,7:1}),('UNSAT',{**p,7:0})]:
    w,dead=profile(q);good,bad=models(q)
    assert not dead
    ans[tag]={'models':len(good),'width_hist':dict(sorted(Counter(w).items())),
              'S':sum(w),'strict_private_gates':sum(w)-1,'witness':good[:1],
              'first_falsified_original_clause_ids':dict(Counter(bad)) if tag=='UNSAT' else {}}
assert ans['parent']['models']==1
assert (ans['SAT']['models'],ans['UNSAT']['models'])==(1,0)
assert ans['SAT']['width_hist']==ans['UNSAT']['width_hist']=={0:7,1:2,2:3}
assert ans['SAT']['strict_private_gates']==ans['UNSAT']['strict_private_gates']==7
assert ans['SAT']['witness']==['000011110']
assert sum(ans['UNSAT']['first_falsified_original_clause_ids'].values())==32
for x in range(1,10):
    for b in (0,1):
        w,dead=profile({x:b})
        assert not dead and Counter(w)==Counter({0:2,2:2,3:8})
        assert sum(w)-1==27
print(json.dumps({'status':'PASS','claim':'SHANNON-SOURCE-POTENTIAL318',
                  'F9_models':len(models({})[0]),'same_original':ans,
                  'all_first_cofactors_gates':27,'P_vs_NP':'OPEN'},indent=2,sort_keys=True))
