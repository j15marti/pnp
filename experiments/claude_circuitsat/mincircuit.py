# Exact min number of fan-in-2 gates (all 16 binary ops) per Boolean function on n vars.
# Cost of f = min k s.t. some k-gate straight-line program computes f (inputs/constants free).
import json,sys
n=int(sys.argv[1]); N=1<<n; M=(1<<N)-1
base=[sum(((x>>i)&1)<<x for x in range(N)) for i in range(n)]
ops=[lambda a,b,t=t:sum((((t>>(2*((a>>x)&1)+((b>>x)&1)))&1)<<x) for x in range(N)) for t in range(16)]
best={}
for f in [0,M]+base: best[f]=0
def dfs(prog,k,limit):
    if k==limit: return
    for i in range(len(prog)):
        for j in range(i,len(prog)):
            for op in ops:
                g=op(prog[i],prog[j])
                if g in prog: continue
                if best.get(g,99)>k+1: best[g]=k+1
                dfs(prog+[g],k+1,limit)
limit=int(sys.argv[2])
dfs(list(set([0,M]+base)),0,limit)
from collections import Counter
c=Counter(best.values()); print(n,limit,len(best),dict(sorted(c.items())))
# cost of n-var AND-like / parity / majority
par=0
for x in range(N): par|=(bin(x).count('1')&1)<<x
print("parity",best.get(par),"and",best.get(base[0] if n==1 else __import__('functools').reduce(lambda a,b:a&b,base)))
json.dump({'n':n,'limit':limit,'hist':dict(c)},open(f'mincircuit_n{n}.json','w'))
