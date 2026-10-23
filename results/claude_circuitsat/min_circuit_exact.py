# Exact minimum B2-circuit size (fan-in 2, unbounded fan-out) for all n-input functions, n<=3.
# Method: BFS over sets of computed truth tables (size = #gates). Runs in a few seconds.
import itertools, json, sys
n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
N = 1 << n; FULL = (1 << N) - 1
inputs = [sum(((x >> i) & 1) << x for x in range(N)) for i in range(n)]
ops = [lambda a,b,t=t: sum((((t>>(2*((a>>x)&1)+((b>>x)&1)))&1)<<x) for x in range(N)) for t in range(16)]
# state = frozenset of available tables (inputs+gates); best[f] = min gates
best = {0:0, FULL:0}
for t in inputs: best[t]=0; best[FULL^t]=0   # constants/negations: free negation absorbed in B2 gates; count output negation as free
start = frozenset(inputs)
layer = {start}; seen={start}
size = 0
while len(best) < (1<<N) and size < 8:
    size += 1; nxt=set()
    for S in layer:
        L = sorted(S)
        for a,b in itertools.combinations(L,2):
            for op in ops:
                g = op(a,b)
                if g in S: continue
                T = S|{g}
                if T in seen: continue
                seen.add(T); nxt.add(T)
                for h in (g, FULL^g):
                    if h not in best: best[h]=size
    layer = nxt
    print("size",size,"states",len(layer),"covered",len(best),file=sys.stderr)
from collections import Counter
c = Counter(best.values())
print(json.dumps({"n":n,"basis":"B2 fan-in2, free output negation","count_by_min_gates":dict(sorted(c.items())),"max":max(best.values()),"wires_eq_2x_gates":True}))
