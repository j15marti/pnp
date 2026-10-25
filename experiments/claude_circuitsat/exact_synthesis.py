"""Exact minimum B2-circuit size C(f) for all n-input Boolean functions, n<=3.
Normalized (f(0..0)=0) search; any function g has C(g)=C(g xor 1 if g(0)=1) (output negation is free in B2).
Usage: python3 exact_synthesis.py N  -> prints/writes JSON. Designed to finish in <30s for N<=3."""
import sys, json, itertools
n=int(sys.argv[1]); R=1<<n; FULL=(1<<R)-1
inputs=[sum(((a>>i)&1)<<a for a in range(R)) for i in range(n)]
# normal binary ops on truth tables (value 0 at (0,0)): and, x&~y, ~x&y, xor, or
ops=[lambda x,y:x&y, lambda x,y:x&~y&FULL, lambda x,y:~x&y&FULL, lambda x,y:x^y, lambda x,y:x|y]
cost={0:0}
for x in inputs: cost[x]=0
level={frozenset(inputs)}
k=0
total=(1<<(R-1))
while len(cost)<total and k<7:
    k+=1; nxt=set()
    for st in level:
        L=sorted(st)
        for i in range(len(L)):
            for j in range(i+1,len(L)):
                for op in ops:
                    g=op(L[i],L[j])
                    if g and g not in st:
                        nxt.add(st|{g})
                        if g not in cost: cost[g]=k
    level=nxt
    print(f"level {k}: states={len(level)} normal fns found={len(cost)}/{total}",file=sys.stderr)
hist={}
for f,c in cost.items(): hist[c]=hist.get(c,0)+1
# full count over all 2^R functions: each normal f and its complement share cost
print(json.dumps({"n":n,"max_cost":max(cost.values()),"histogram_normal":hist,
  "histogram_all":{c:2*v for c,v in hist.items()}, "complete":len(cost)==total},sort_keys=True))
