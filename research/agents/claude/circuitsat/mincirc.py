# Exact min B2-circuit size (2-input gates, all 16 gate types) for all n-var functions, n<=3.
# Wires = 2*gates (fan-in 2). Iterative deepening over gate sequences, truth tables as ints.
import sys, itertools, json
n=int(sys.argv[1]); N=1<<n; M=(1<<N)-1
vars_=[sum(((x>>i)&1)<<x for x in range(N)) for i in range(n)]
def ops(a,b):
    na,nb=a^M,b^M
    return {a&b,a&nb,na&b,na&nb,a|b,a|nb,na|b,na|nb,a^b,a^b^M}  # nondegenerate gates
best={}
for v in vars_: best[v]=0; best[v^M]=0   # free negation of inputs? no: count as size 0 only for var itself
best={v:0 for v in vars_}; best[0]=0; best[M]=0
level=[tuple(vars_)]
seen={}
def dfs(circ,depth,limit,found):
    if depth==limit:
        return
    for i in range(len(circ)):
        for j in range(i+1,len(circ)):
            for f in ops(circ[i],circ[j]):
                if f in circ: continue
                g=depth+1
                if best.get(f,99)>g: best[f]=g
                dfs(circ+(f,),g,limit,found)
limit=int(sys.argv[2])
dfs(tuple(vars_),0,limit,None)
from collections import Counter
c=Counter(best.get(f,99) for f in range(M+1))
print(n,dict(sorted(c.items())))
