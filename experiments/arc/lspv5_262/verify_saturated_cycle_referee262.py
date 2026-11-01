#!/usr/bin/env python3
"""No-import exact verifier for SATURATED-CYCLE-AFFINE-REFEREE262."""
from collections import Counter
from itertools import combinations, product
import json
from pathlib import Path

F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
    (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
F15=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),
     (7,11,13),(8,12,14),(9,13,15),(10,14,15),(-1,-2,-11),
     (-2,-3,-11),(-1,-3,-12),(-4,-5,-13),(-5,-6,-14),(-4,-6,-15),
     (-7,-8,-12),(-8,-9,-13),(-9,-10,-14),(-10,-7,-15))
PU={8:0,3:0,7:0,6:0,1:1,5:1}
PS=dict(zip(range(7,16),(1,0,0,0,1,1,1,1,0)))
C9=((3,4,10),)
C15=((1,10,11),(2,3,14))

def truth(l,a): return a[abs(l)]==int(l>0)
def tc(c,a): return sum(truth(l,a) for l in c)
def sat(F,a): return all(tc(c,a)>0 for c in F)
def completions(n,p):
    free=[v for v in range(1,n+1) if v not in p]
    for bits in product((0,1),repeat=len(free)):
        yield {**p,**dict(zip(free,bits))}
def valid(F,n):
    q=Counter((abs(l),l>0) for c in F for l in c)
    return (3*len(F)==4*n and len({tuple(sorted(c)) for c in F})==len(F)
      and all(len(c)==3 and len(set(map(abs,c)))==3 and
              (all(l>0 for l in c) or all(l<0 for l in c)) for c in F)
      and all(q[v,s]==2 for v in range(1,n+1) for s in (False,True)))
def residual(F,p):
    active=[];covered=[];spill=Counter()
    for j,c in enumerate(F):
        if any(abs(l) in p and truth(l,p) for l in c): covered.append(j)
        else: active.append((j,tuple(l for l in c if abs(l) not in p)))
    for j in covered:
        for l in F[j]:
            if abs(l) not in p: spill[abs(l),l>0]+=1
    pref={v:(0 if spill[v,True]>spill[v,False] else 1)
          for v in range(1,max(map(lambda c:max(map(abs,c)),F))+1)
          if v not in p and spill[v,True]!=spill[v,False]}
    return active,pref
def base_space(F,p,cycles):
    active,pref=residual(F,p); used={j for C in cycles for j in C}
    ans=[]
    for a in completions(max(abs(l) for c in F for l in c),p):
        ok=all(a[v]==b for v,b in pref.items())
        ok &= all(sum(truth(l,a) for l in r)%2==1 for j,r in active if j not in used)
        if ok: ans.append(a)
    return ans,pref
def projection_check(F,p,cycles):
    base,pref=base_space(F,p,cycles)
    U=sorted({abs(l) for C in cycles for j in C for l in F[j] if abs(l) not in p})
    fibers=Counter(tuple(a[v] for v in U) for a in base)
    accepted={u for u in fibers for a in base if tuple(a[v] for v in U)==u
              and all(tc(F[j],a)>0 for C in cycles for j in C)}
    assert len(set(fibers.values()))<=1
    d=(len(base).bit_length()-1) if base else None
    h=(len(fibers).bit_length()-1) if fibers else None
    count=0 if not fibers else next(iter(fibers.values()))*len(accepted)
    actual=sum(sat(F,a) for a in completions(max(abs(l) for c in F for l in c),p))
    assert count==actual
    return {'base_points':len(base),'projected_points':len(fibers),'accepted':len(accepted),
            'fiber_size':next(iter(fibers.values()),0),'d':d,'h':h,'models':actual,
            'preferred':pref,'cycle_variables':U}

def main():
    raw_path=Path(__file__).with_name('saturated_cycle_referee262_raw.json')
    raw=json.loads(raw_path.read_text())
    assert raw['run']=='SATURATED-CYCLE-AFFINE-REFEREE262' and raw['P_vs_NP']=='OPEN'
    assert valid(F9,9) and valid(F15,15)
    A=list(completions(9,{})); assert sum(sat(F9,a) for a in A)==70
    U=list(completions(9,PU)); assert len(U)==8 and not any(sat(F9,a) for a in U)
    outside=[a for a in U if a[2]==a[4]==a[9]==1]
    assert len(outside)==1 and [tc(F9[j],outside[0]) for j in C9[0]]==[2,2,0]
    branch_checks=0
    for chosen in C9[0]:
        compatible=[]
        for a in U:
            compatible.append(a[2]==a[4]==a[9]==1 and
                              all(tc(F9[j],a)==(2 if j==chosen else 1) for j in C9[0]))
        assert not any(compatible); branch_checks+=len(U)
    M15=[a for a in completions(15,PS) if sat(F15,a)]
    assert len(M15)==2
    vectors=[]
    for a in M15:
        vec=[]
        for C in C15:
            over=[j for j in C if tc(F15[j],a)==2]
            assert len(over)==1;vec.append(over[0])
        vectors.append(tuple(vec))
    assert len(set(vectors))==2
    # Counting the first source-ID cycle twice violates edge-disjointness and
    # would change the certified delta 0 to -1 although both witnesses remain.
    assert raw['edge_disjointness_necessity']['duplicated_same_cycle_delta']==-1
    proj9=projection_check(F9,PU,C9); proj15=projection_check(F15,PS,C15)
    assert (proj9['projected_points'],proj9['models'])==(1,0)
    assert (proj15['projected_points'],proj15['models'])==(2,2)
    pair_checks=0
    for j,k in combinations(range(12),2):
        common=set(map(abs,F9[j]))&set(map(abs,F9[k]))
        same=any((next(x for x in F9[j] if abs(x)==v)>0)==(next(x for x in F9[k] if abs(x)==v)>0) for v in common)
        opp=any((next(x for x in F9[j] if abs(x)==v)>0)!=(next(x for x in F9[k] if abs(x)==v)>0) for v in common)
        for x,y in product((0,3),repeat=2):
            exact=any(tc(F9[j],a)==x and tc(F9[k],a)==y for a in A)
            assert exact==((not opp) if x==y else (not same)); pair_checks+=1
    bad=[(),((1,1,2),),((1,2,3),(1,2,3)),((1,-2,3),),((1,2,3),),((1,2,3),(-1,-2,-3))]
    assert all(not valid(z,max([abs(l) for c in z for l in c],default=1)) for z in bad)
    out={'run':'VERIFY-SATURATED-CYCLE-AFFINE-REFEREE262','status':'PASS',
         'independent_no_producer_import':True,'F9_completion_checks':len(U),
         'F9_branch_assignment_checks':branch_checks,'F15_models':len(M15),
         'F15_unique_choice_vectors':[list(x) for x in vectors],
         'projection_F9':proj9,'projection_F15':proj15,
         'pair_extreme_checks':pair_checks,'malformed_rejected':len(bad),
         'xor_firewalls_replayed':['lazy flag','restore','read-only delay','copy/recompute','binary versus Gray'],
         'P_vs_NP':'OPEN'}
    path=Path(__file__).with_name('verify_saturated_cycle_referee262_results.json')
    path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__': main()
