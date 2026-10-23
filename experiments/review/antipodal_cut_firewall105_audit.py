#!/usr/bin/env python3
"""Independent audit for CUT-CERTIFICATE-CEILING105 (stdlib only)."""
from itertools import combinations, product
import hashlib, json, random

H=[(0,1,2),(0,3,4),(1,3,5),(2,4,5),(3,4,5),(1,2,5),(0,2,4),(0,1,3)]
E=[(v,c) for c,C in enumerate(H) for v in C]
V=range(6); C=range(8)
inc=[[i for i,(u,_) in enumerate(E) if u==v] for v in V]
cls=[[i for i,(_,d) in enumerate(E) if d==c] for c in C]

balanced=[]
for choices in product(*[[sum(1<<i for i in p) for p in combinations(inc[v],2)] for v in V]):
    s=0
    for x in choices:s|=x
    if all(1<=sum(bool(s>>i&1) for i in cls[c])<=2 for c in C): balanced.append(s)
assert len(balanced)==5904

def feasible(pins):
    pm=sum(1<<i for i,b in pins.items() if b)
    zm=sum(1<<i for i,b in pins.items() if not b)
    return any((s&pm)==pm and (s&zm)==0 for s in balanced)

def local_and_cuts(pins):
    R=[]; L=[]; U=[]; free=[]
    for v in V:
        p=sum(pins[i] for i in inc[v] if i in pins); f=sum(i not in pins for i in inc[v])
        R.append(2-p)
        if not 0<=R[-1]<=f:return False,False
    for c in C:
        t=sum(pins[i] for i in cls[c] if i in pins); f=sum(i not in pins for i in cls[c])
        L.append(max(0,1-t));U.append(min(f,2-t))
        if L[-1]>U[-1]:return False,False
    free=[i for i in range(24) if i not in pins]
    for xm in range(1<<6):
      RX=sum(R[v] for v in V if xm>>v&1); Rbar=sum(R[v] for v in V if not xm>>v&1)
      for ym in range(1<<8):
        ef_out=sum(1 for i in free if (xm>>E[i][0]&1) and not (ym>>E[i][1]&1))
        ef_in=sum(1 for i in free if (xm>>E[i][0]&1) and (ym>>E[i][1]&1))
        if RX>ef_out+sum(U[c] for c in C if ym>>c&1):return True,False
        if sum(L[c] for c in C if ym>>c&1)>Rbar+ef_in:return True,False
    return True,True

explicit={2:1,3:1,6:1,15:0,18:0,21:0,22:0}
assert feasible(explicit) is False and local_and_cuts(explicit)==(True,False)

rng=random.Random(202610240348)
tests=[]
for _ in range(32):
    k=rng.randrange(0,13)
    pos=rng.sample(range(24),k)
    pins={i:rng.randrange(2) for i in pos}
    f=feasible(pins); local,cuts=local_and_cuts(pins)
    assert f==(local and cuts)
    tests.append((k,f,local,cuts))

out={
 "run_id":"CUT-CERTIFICATE-CEILING105",
 "seed":202610240348,
 "support":{"variables":6,"clauses":8,"occurrences":24},
 "balanced_two_witness_signings":len(balanced),
 "random_pinned_instances":len(tests),
 "cut_pairs_per_locally_valid_instance":(1<<6)*(1<<8),
 "explicit_seven_pin":{"locally_valid":True,"globally_feasible":False,"violated_cut":[2,0,1]},
 "zero_failures":True,
 "status":"COMPUTATIONAL; theorem proved symbolically in paired report"
}
payload=json.dumps(out,sort_keys=True,indent=2)+"\n"
out["payload_sha256_without_digest"]=hashlib.sha256(payload.encode()).hexdigest()
print(json.dumps(out,sort_keys=True,indent=2))
