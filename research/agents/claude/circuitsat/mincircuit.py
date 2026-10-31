# Exact min gate count over B2 (all 16 binary gates, fan-in 2) for all functions of n<=3 vars.
# Iterative-deepening DFS over straight-line programs. Wires = 2*gates (each gate has two in-wires).
import sys, itertools, json
n=int(sys.argv[1]); N=1<<n; M=(1<<N)-1
inputs=[sum(1<<x for x in range(N) if (x>>i)&1) for i in range(n)]
def ops(a,b):
    na,nb=M^a,M^b
    s={a&b,a&nb,na&b,na&nb,a|b,a|nb,na|b,na|nb,a^b,M^(a^b),a,b,na,nb,0,M}
    return s
best={}
def dfs(funcs,k,depth):
    # record min gates to reach each function
    for f in funcs:
        if f not in best or best[f]>k: best[f]=k
    if k==depth: return
    L=len(funcs); seen=set(funcs)
    for i in range(L):
        for j in range(i+1,L):
            for r in ops(funcs[i],funcs[j]):
                if r not in seen and r not in (0,M) and r not in inputs:
                    dfs(funcs+[r],k+1,depth)
for d in range(0,{2:3,3:4}[n]+1):
    dfs(list(inputs),0,d)
    print("depth",d,"funcs reached",len(best),file=sys.stderr)
from collections import Counter
c=Counter(best[f] for f in best)
print(json.dumps({"n":n,"hist_gates":dict(sorted(c.items())),"total_nonconst":len(best)}))
