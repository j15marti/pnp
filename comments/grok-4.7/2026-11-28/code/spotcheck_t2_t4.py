#!/usr/bin/env python3
"""Spot-checks of new T2/T4 claims (2026-11-27 reports), exhaustive in the stated finite models."""
import itertools, json, random
out={}
# T2: translation periods of signed B4 (weight exactly 2 on 4 bits; signs = translation of the row set)
R=[w for w in itertools.product((0,1),repeat=4) if sum(w)==2]
ok=True
for sgn in itertools.product((0,1),repeat=4):
    Rs={tuple(a^b for a,b in zip(w,sgn)) for w in R}
    H=[d for d in itertools.product((0,1),repeat=4) if {tuple(a^b for a,b in zip(w,d)) for w in Rs}==Rs]
    ok&= H==[(0,0,0,0),(1,1,1,1)]
    # annihilator = even-weight masks (dim 3); image under L has exactly 3 codes
    L=[(1,1,0,0),(0,1,1,0),(0,0,1,1)]
    codes={tuple(sum(l[i]*w[i] for i in range(4))%2 for l in L) for w in Rs}
    ok&= len(codes)==3 and len(Rs)==6
    # x in Rs iff Lx in codes
    ok&= all((x in Rs)==(tuple(sum(l[i]*x[i] for i in range(4))%2 for l in L) in codes) for x in itertools.product((0,1),repeat=4))
out["T2_B4_periods_and_3_codes"]=ok
# T2: projecting one bit of weight-2/4 gives NAE3 on the other three
P={w[:3] for w in R}
out["T2_private_parity_projection_is_NAE3"]= P=={w for w in itertools.product((0,1),repeat=3) if 0<sum(w)<3}
# T2: global span of even-weight local annihilators on a connected random 4-uniform incidence = full even space
rng=random.Random(7); good=0; T=200
for _ in range(T):
    n=rng.randint(5,14); fac=[rng.sample(range(n),4) for _ in range(rng.randint(2,3*n))]
    # connectivity on occurring carriers
    occ=sorted(set(v for f in fac for v in f)); par={v:v for v in occ}
    def fd(x):
        while par[x]!=x: x=par[x]
        return x
    for f in fac:
        for v in f[1:]: par[fd(v)]=fd(f[0])
    comps=len({fd(v) for v in occ})
    rows=[]
    for f in fac:
        for a,b in zip(f,f[1:]): rows.append((1<<a)|(1<<b))
    basis=[]
    for r in rows:
        for b in basis: r=min(r,r^b)
        if r: basis.append(r)
    good+= len(basis)==len(occ)-comps
out["T2_global_rank_equals_carriers_minus_components"]=f"{good}/{T}"
# T4-02 Phi: worst-case change per successful pop, enumerated over t (deleted incidences) and s<=k-1
worst=max(-1-t+t+2*s-(2*k+1) for k in range(2,20) for t in range(1,5*k) for s in range(0,k))
out["T4_Phi_max_change_on_successful_pop"]=worst
json.dump(out,open("spotcheck_t2_t4.out.json","w"),indent=1); print(out)
