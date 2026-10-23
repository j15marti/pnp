# Exhaustive minimum B2 circuit size (fan-in-2, all 16 gates) for all n-var Boolean functions.
# Level-k states = sets of k distinct gate outputs (inputs free). Usage: minsize_b2.py n maxlevel
import sys, json, itertools
n=int(sys.argv[1]); L=int(sys.argv[2]); N=1<<n; FULL=(1<<N)-1
ins=[sum(1<<a for a in range(N) if a>>i&1) for i in range(n)]
def gates(x,y):
    nx,ny=FULL^x,FULL^y
    return {x&y,x&ny,nx&y,nx&ny,x|y,x|ny,nx|y,nx|ny,x^y,FULL^(x^y)}  # nontrivial gates
seen_best={f:None for f in range(1<<N)}
base=frozenset(ins); known={0,FULL,*ins}
for f in known: seen_best[f]=0
for f in list(seen_best):               # negations of inputs/consts cost 0 wires in B2 absorbed by next gate; count as cost 1 gate
    pass
frontier={frozenset()}
for k in range(1,L+1):
    new=set()
    for S in frontier:
        pool=list(base|S)
        for x,y in itertools.combinations(pool,2):
            for g in gates(x,y):
                if g in base or g in S or g in (0,FULL): continue
                new.add(S|{g})
    frontier=new
    for S in frontier:
        for g in S:
            if seen_best[g] is None: seen_best[g]=k
    cnt=sum(1 for v in seen_best.values() if v is not None)
    print(n,k,len(frontier),cnt,"/",1<<N,flush=True)
    if cnt==1<<N: break
from collections import Counter
# output negation is free in B2: cost(f)=min(cost f, cost ~f)
for f in range(1<<N):
    a,b=seen_best[f],seen_best[FULL^f]
    if a is None or (b is not None and b<a): seen_best[f]=b
print(sorted(Counter(v for v in seen_best.values()).items(),key=lambda t:(t[0] is None,t[0])))
json.dump({"n":n,"hist":sorted(Counter(str(v) for v in seen_best.values()).items())},open(f"minsize_b2_n{n}.json","w"))
