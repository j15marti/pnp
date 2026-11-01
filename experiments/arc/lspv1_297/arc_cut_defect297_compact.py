#!/usr/bin/env python3
"""ARC-CUT-DEFECT297 compact source-authenticated canonical SAT/UNSAT verifier.
A local certificate module, not a complete polynomial solver or native FLMV machine.
"""
from itertools import product,combinations
from collections import Counter
import json
F=((-1,-2,-5),(-1,-3,-6),(1,4,7),(2,3,8),(-2,-4,-9),(3,4,10),
   (6,14,16),(6,15,17),(12,18,13),(12,7,1),(5,11,8),(9,17,13),
   (9,18,15),(11,5,10),(14,16,2),(-15,-8,-14),(-17,-10,-13),
   (-15,-10,-9),(-16,-5,-12),(-18,-11,-8),(-17,-12,-6),
   (-18,-14,-4),(-7,-3,-13),(-7,-16,-11))
A=(0,0,1,1,1,1,0,0,1,0,1,1,0,1,0,0,0,0)
P_S=(-1,-1,-1,-1)+A[4:]
P_U=P_S[:13]+(0,)+P_S[14:]
K4_IDS=(1,2,3,4,5,6)

def grammar():
    occ=Counter(l for c in F for l in c)
    return (len(F)==24 and len({tuple(sorted(c)) for c in F})==24
       and all(len(c)==3 and len(set(map(abs,c)))==3 and
               (all(l>0 for l in c) or all(l<0 for l in c)) for c in F)
       and all(occ[x]==occ[-x]==2 for x in range(1,19)))

def residual(p):
    r={};covered={x:[0,0] for x,v in enumerate(p,1) if v<0};work=Counter()
    for j,c in enumerate(F,1):
        work['source_clause_reads']+=1
        hit=False
        for l in c:
            work['source_literal_reads']+=1
            hit|=p[abs(l)-1]==int(l>0)
        if hit:
            for l in c:
                if p[abs(l)-1]<0:
                    covered[abs(l)][int(l<0)]+=1
                    work['covered_free_occurrences']+=1
        else:r[j]=tuple(l for l in c if p[abs(l)-1]<0)
    return r,covered,work

def truth(a):
    return all(any(a[abs(l)-1]==int(l>0) for l in c) for c in F)

def gate(p):
    r,s,work=residual(p)
    chosen=[r[j] for j in K4_IDS if j in r and len(r[j])==2]
    pairs={tuple(sorted(map(abs,c))) for c in chosen}
    assert len(chosen)==6 and pairs==set(combinations(range(1,5),2))
    # Check every 2-coloring: K4 has at least two equal-endpoint edges.
    q=min(sum(a[u-1]==a[v-1] for u,v in pairs) for a in product((0,1),repeat=4))
    assert q==2
    e=2*p.count(-1)-len(r)
    eta=sum(min(v) for v in s.values())
    delta=e-eta-q
    prefs={x:int(v[1]>v[0]) for x,v in s.items() if v[0]!=v[1]}
    weights={x:abs(v[0]-v[1]) for x,v in s.items() if v[0]!=v[1]}
    forced={x:b for x,b in prefs.items() if delta>=0 and weights[x]>delta}
    sol=[]
    for bits in product((0,1),repeat=4):
        a=bits+p[4:]
        if truth(a):sol.append(a)
    assert delta>=0 or not sol
    assert all(all(a[x-1]==v for x,v in forced.items()) for a in sol)
    return {'f':p.count(-1),'u':len(r),'e':e,'eta':eta,'K4_defect':q,
       'delta':delta,'forced':forced,'source_models':len(sol),
       'K4_original_clause_ids':K4_IDS,
       'other_unsatisfied_clause_ids':sorted(set(r)-set(K4_IDS)),
       'work':dict(work)}

def main():
    assert grammar() and truth(A)
    sat=gate(P_S);unsat=gate(P_U)
    assert (sat['e'],sat['delta'],sat['source_models'])==(2,0,1)
    assert sat['forced']=={1:0,2:0,3:1,4:1}
    assert (unsat['e'],unsat['delta'],unsat['source_models'])==(1,-1,0)
    assert unsat['other_unsatisfied_clause_ids']==[15]
    assert residual(P_U)[0][15]==(2,)
    print(json.dumps({'status':'PASS','target':'proper duplicate-free Monotone 3-SAT-(2,2)',
       'source_n':18,'source_m':24,'SAT':sat,'UNSAT':unsat,
       'universal_ARC_and_FLMV':'OPEN'},indent=2,sort_keys=True))
if __name__=='__main__':main()
