#!/usr/bin/env python3
"""Independent exhaustive checker, no imports from ARC-CUT-DEFECT297 producer."""
from itertools import product,combinations
from collections import Counter
from pathlib import Path
F=((-1,-2,-5),(-1,-3,-6),(1,4,7),(2,3,8),(-2,-4,-9),(3,4,10),
(6,14,16),(6,15,17),(12,18,13),(12,7,1),(5,11,8),(9,17,13),
(9,18,15),(11,5,10),(14,16,2),(-15,-8,-14),(-17,-10,-13),
(-15,-10,-9),(-16,-5,-12),(-18,-11,-8),(-17,-12,-6),
(-18,-14,-4),(-7,-3,-13),(-7,-16,-11))
assert len(F)==len(set(tuple(sorted(c)) for c in F))==24
count=Counter(x for c in F for x in c)
assert all(count[x]==count[-x]==2 for x in range(1,19))
assert all(len(c)==3 and len({abs(x) for x in c})==3
    and (all(x>0 for x in c) or all(x<0 for x in c)) for c in F)
def sat(a):
    return all(any(a[abs(x)-1]==(x>0) for x in c) for c in F)
w=(0,0,1,1,1,1,0,0,1,0,1,1,0,1,0,0,0,0)
assert sat(w)
pS=(-1,)*4+w[4:]
pU=pS[:13]+(0,)+pS[14:]
assert pS[13]==1 and pU[13]==0
def analyze(p):
    live={}
    spill={i:[0,0] for i in range(1,5)}
    for j,c in enumerate(F,1):
        if any(p[abs(l)-1]==int(l>0) for l in c):
            for l in c:
                if abs(l)<=4: spill[abs(l)][int(l<0)]+=1
        else:
            live[j]=tuple(l for l in c if p[abs(l)-1]<0)
    edges=[tuple(sorted(map(abs,live[i]))) for i in range(1,7)]
    assert set(edges)==set(combinations((1,2,3,4),2))
    defect=min(sum(bits[a-1]==bits[b-1] for a,b in edges)
               for bits in product((0,1),repeat=4))
    assert defect==2
    e=8-len(live);eta=sum(min(v) for v in spill.values())
    solutions=[bits for bits in product((0,1),repeat=4) if sat(bits+p[4:])]
    preferred={i:int(v[1]>v[0]) for i,v in spill.items() if v[0]!=v[1]}
    gap=e-eta-defect
    assert gap>=0 or not solutions
    for bits in solutions:
        for i,b in preferred.items():
            if abs(spill[i][0]-spill[i][1])>gap: assert bits[i-1]==b
    return e,eta,gap,len(solutions),set(live)-set(range(1,7))
assert analyze(pS)==(2,0,0,1,set())
assert analyze(pU)==(1,0,-1,0,{15})
# Original-source extreme compatibility by exact global assignment enumeration.
for i,j in combinations(range(24),2):
    a,b=F[i],F[j]
    common={abs(x) for x in a}&{abs(x) for x in b}
    opposed=any(x==-y for x in a for y in b)
    same=any(x==y for x in a for y in b)
    ss=(not opposed);su=(not same)
    assert ss==all(not any(x==-y for x in a for y in b) for _ in (0,))
    assert su==all(not any(x==y for x in a for y in b) for _ in (0,))
    # Exhaust over only the six clause positions, never an occurrence-as-variable oracle.
    v=sorted({abs(x) for x in a+b})
    feasible=[False]*4
    for assignment in product((0,1),repeat=len(v)):
        env=dict(zip(v,assignment))
        t1=sum(env[abs(x)]==int(x>0) for x in a)
        t2=sum(env[abs(x)]==int(x>0) for x in b)
        if t1==3 and t2==3: feasible[0]=True
        if t1==3 and t2==0: feasible[1]=True
        if t1==0 and t2==3: feasible[2]=True
        if t1==0 and t2==0: feasible[3]=True
    assert feasible==[ss,su,su,ss]
print({'status':'PASS','same_source_sat_and_unsat':True,'K4_defect':2,
       'original_compatibility_pairs':276,'full_endpoint_models':sat(w),
       'scope':'finite offline verification, ARC/FLMV OPEN'})
