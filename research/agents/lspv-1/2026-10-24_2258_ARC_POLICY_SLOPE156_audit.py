#!/usr/bin/env python3
"""Exact-rational resource-envelope audit for ARC-POLICY-SLOPE156.
This checks only conditional arithmetic, not all-input SAT compiler correctness.
"""
import json
from fractions import Fraction as Q

C = Q(241,200)
BETA = Q(11642479,23232400)
BASE_A = Q(3,5)
BASE_RHO = Q(1,2)
R = Q(11,10)
P = Q(1,2)

def recur(t, s, rho, b, g=Q(0)):
    return max(R,BASE_A+BASE_RHO*t,b+g+rho*t), max(P,s/2,rho*s)

def fp(rho,b,g=Q(0)):
    if rho>=1:
        return None
    return max(R,Q(6,5),(b+g)/(1-rho))

def first_hit(seed,rho,b,g=Q(0),max_depth=10000):
    t=s=Q(seed)
    for step in range(max_depth+1):
        if t<C and s<BETA:
            return step,t,s
        t,s=recur(t,s,rho,b,g)
    return None

cases=[
    ("halfscale_standard",Q(1,2),Q(3,5)),
    ("halfscale_small_extra",Q(1,2),Q(601,1000)),
    ("halfscale_boundary_strict_fail",Q(1,2),Q(241,400)),
    ("halfscale_overrun",Q(1,2),Q(603,1000)),
    ("three_fifths_lazy",Q(3,5),Q(12,25)),
    ("three_quarters_lazy",Q(3,4),Q(3,10)),
    ("parent_scale_query",Q(1),Q(0)),
]
checks=0
rows=[]
for name,rho,b in cases:
    target=fp(rho,b)
    threshold=(C*(1-rho)) if rho<1 else Q(0)
    success=(target is not None and target<C and P<BETA)
    expected=(rho<1 and b<threshold)
    assert success==expected;checks+=1
    depths={}
    for seed in (2,5,20):
        hit=first_hit(seed,rho,b,max_depth=400)
        if success:
            assert hit is not None;checks+=1
            j,t,s=hit
            assert t<C and s<BETA;checks+=1
            if j>0:
                prev=Q(seed);ps=Q(seed)
                for _ in range(j-1):
                    prev,ps=recur(prev,ps,rho,b)
                assert prev>=C or ps>=BETA;checks+=1
            depths[str(seed)]={"steps":j,"time":str(t),"space":str(s)}
        else:
            assert hit is None;checks+=1
            depths[str(seed)]=None
    eager_space_ok=(max(P,rho)<BETA)
    rows.append({"case":name,"selector_query_scale":str(rho),"selector_fanout":str(b),
                 "time_fixed_point":None if target is None else str(target),
                 "strict_time_selector_threshold":str(threshold),
                 "joint_lazy_hit":success,"eager_selector_buffer_space_ok":eager_space_ok,
                 "depth_from_diagonals":depths})

assert BETA>Q(1,2); checks+=1
assert C*Q(1,2)-Q(3,5)==Q(1,400);checks+=1
assert fp(Q(1,2),Q(3,5))==Q(6,5);checks+=1
assert fp(Q(3,5),Q(12,25))==Q(6,5);checks+=1
assert fp(Q(3,4),Q(3,10))==Q(6,5);checks+=1

out={"run":"ARC-SELECTOR-SCALE156","mode":"exact rational arithmetic only",
     "claim_scope":"conditional max-affine query ledger, not all-input SAT compiler",
     "strict_box":{"t":str(C),"s":str(BETA)},"checks":checks,"cases":rows,
     "padded_solver_note":"Forced call to a padded N^K exact decider on a Theta(N) query gives Omega(N^K) time for that black-box wrapper; not a general separation."}
print(json.dumps(out,indent=2))
