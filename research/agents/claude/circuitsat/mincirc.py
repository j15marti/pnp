# Exact minimum fan-in-2 circuit size (gates; wires=2*gates) for all n-input functions,
# basis {AND} with free negations on wires (equiv. to AND/OR/NOT with free NOT).
# Method: BFS over sets of computed truth tables (frontier), n<=3. Runtime ~ seconds.
import itertools, json, sys
def run(n):
    N=1<<n; M=(1<<N)-1
    ins=[]
    for i in range(n):
        t=0
        for x in range(N):
            if (x>>i)&1: t|=1<<x
        ins.append(t)
    base=frozenset([0,M]+ins+[M^t for t in ins])
    best={}  # function -> min gates
    for f in base: best[f]=0
    # state: frozenset of available functions (closed under negation); level by gate count
    level={0:{frozenset(base)}}
    maxg=0
    allf=1<<N
    g=0
    while len(best)<allf and g<9:
        g+=1; level[g]=set()
        for S in level[g-1]:
            L=list(S)
            for a,b in itertools.combinations_with_replacement(L,2):
                h=a&b
                if h in S: continue
                S2=S|{h,M^h}
                level[g].add(frozenset(S2))
                for f in (h,M^h):
                    if f not in best: best[f]=g
        print(n,g,len(level[g]),len(best),file=sys.stderr)
    from collections import Counter
    return Counter(best.values()), len(best)
res={}
for n in (1,2,3):
    c,k=run(n); res[n]={'functions':k,'by_gates':dict(sorted(c.items()))}
print(json.dumps(res))
