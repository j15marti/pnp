# Probe: clause/source-bit replication for variable-block static cones on random 3-SAT (runtime << 30 s).
import random, json, sys
def run(n, alpha, seed, ratio=4.26):
    rnd = random.Random(seed); m = int(ratio*n)
    s = max(1, round(n**alpha)); blk = lambda v: v//s
    clauses = [tuple(rnd.sample(range(n), 3)) for _ in range(m)]
    reps = [len({blk(v) for v in c}) for c in clauses]
    nreg = -(-n//s)
    cone = [0]*nreg
    for c in clauses:
        for b in {blk(v) for v in c}: cone[b]+=1
    return dict(n=n, alpha=alpha, s=s, regions=nreg, max_rep=max(reps), mean_rep=sum(reps)/m,
                max_cone=max(cone), mean_cone=sum(cone)/nreg, total_incidence=sum(reps))
out=[run(n,a,sd) for n in (1000,10000,100000) for a in (0.4,0.6) for sd in (0,1)]
json.dump(out, open(sys.argv[1],'w'), indent=1)
for r in out: print(r)
