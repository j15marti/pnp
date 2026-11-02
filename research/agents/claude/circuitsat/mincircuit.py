"""Exact min #gates (fan-in 2, all 16 binary ops, fan-out free) for all f:{0,1}^n->{0,1}, n<=3.
Iterative-deepening over gate sequences; runs in a few seconds. Wires = 2*gates (+1 output wire)."""
import itertools, json, sys
n=int(sys.argv[1]) if len(sys.argv)>1 else 3
N=1<<n; FULL=(1<<N)-1
ins=[sum(((x>>i)&1)<<x for x in range(N)) for i in range(n)]
def ops(a,b):
    na,nb=FULL^a,FULL^b
    return {a&b,a&nb,na&b,na&nb,a|b,a|nb,na|b,na|nb,a^b,FULL^(a^b)}  # nontrivial ops
best={0:0,FULL:0}
for t in ins: best[t]=0; best[FULL^t]=0   # free negation/constants handled: constants & literals cost 0
# BFS by number of gates: level sets of reachable "computed-set" states is big; use DFS depth<=D
def dfs(cur,g,D):
    for a,b in itertools.combinations(range(len(cur)),2):
        for t in ops(cur[a],cur[b]):
            if t in cur: continue
            if best.get(t,99)>g+1: best[t]=g+1
            if g+1<D: dfs(cur+[t],g+1,D)
for D in range(1,5 if n==3 else 4):
    dfs(list(ins),0,D)
    print("depth",D,"functions with size<=",D,":",sum(1 for v in best.values() if v<=D),"/",1<<N,file=sys.stderr)
from collections import Counter
c=Counter(best.values()); print(n,dict(sorted(c.items())),"unresolved",(1<<N)-len(best))
