# Independent spot-check of bc04b91 "exact first-pivot BVE no-growth refusal" counts
# for the smallest case d=2 (blocks of 5 bits), equality path M1=M2, M2=M3, all signs +.
from itertools import combinations
d=2; b=2*d+1
blk=lambda i:[(i,t) for t in range(b)]
def maj_lits(i,pos):  # CNF of M_i (pos) or !M_i (neg): all (d+1)-subsets
    s=1 if pos else -1
    return [frozenset((v,s) for v in S) for S in combinations(blk(i),d+1)]
def lift(phase):       # phase clause = list of (block, sign)
    out=[set()]
    for (i,pos) in phase:
        out=[c|S for c in out for S in maj_lits(i,pos)]
    return [frozenset(c) for c in out]
phase=[[(1,False),(2,True)],[(1,True),(2,False)],[(2,True),(3,False)],[(2,False),(3,True)]]
F=set()
for P in phase: F|=set(lift(P))
p=(2,0)
pos=[c for c in F if (p,1) in c]; neg=[c for c in F if (p,-1) in c]
res=set(); pairs=0
for a in pos:
    for c in neg:
        pairs+=1
        r=(a-{(p,1)})|(c-{(p,-1)})
        if any((v,-s) in r for (v,s) in r): continue
        res.add(frozenset(r))
# subsumption among resolvents / by remaining clauses
rest=[c for c in F if (p,1) not in c and (p,-1) not in c]
subs=sum(1 for r in res if any(c<=r for c in rest))
ws={len(r) for r in res}
print("clauses",len(F),"pivot pos/neg",len(pos),len(neg),"pairs",pairs)
print("distinct non-taut resolvents",len(res),"removed",len(pos)+len(neg),"widths",ws,"subsumed-by-rest",subs)
print("predicted 2*H*K*K =",2*6*10*10,"ratio",len(res)/(len(pos)+len(neg)))
