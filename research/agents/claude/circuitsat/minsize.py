# Exact minimum B2 (all 2-input gates) circuit size for all n-var functions, n<=3, by BFS over sets of computed functions.
# Chunking: n=3 BFS finishes in a few seconds; each function = truth-table bitmask.
import itertools, json, sys
n=int(sys.argv[1]); N=1<<n; M=(1<<N)-1
xs=[sum(1<<a for a in range(N) if (a>>i)&1) for i in range(n)]
ops=[lambda a,b,t=t:sum(((t>>(2*((a>>k)&1)+((b>>k)&1)))&1)<<k for k in range(N)) for t in range(16)]
best={}  # function -> min gates
from functools import lru_cache
# iterative deepening over gate sequences: frontier of states (frozenset of available functions)
start=frozenset(xs+[0,M])
level={start}; seen_fn={f:0 for f in start}
for f in range(1<<N): pass
depth=0
while len(seen_fn)<(1<<N) and depth<8:
    depth+=1; nxt=set()
    for st in level:
        L=sorted(st)
        for a,b in itertools.combinations(L,2):
            for op in ops:
                g=op(a,b)
                if g in st: continue
                if g not in seen_fn: seen_fn[g]=depth
                nxt.add(st|{g})
    level=nxt
    print(depth,len(level),len(seen_fn),file=sys.stderr)
    if depth>=int(sys.argv[2]): break
from collections import Counter
byw={}
for f,d in seen_fn.items():
    byw.setdefault(bin(f).count('1'),[]).append(d)
print(json.dumps({"n":n,"max_size":max(seen_fn.values()),"funcs":len(seen_fn),
 "by_numsat_max":{k:max(v) for k,v in sorted(byw.items())}}))
