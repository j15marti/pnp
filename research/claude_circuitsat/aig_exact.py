"""Exact min AIG size (AND gates, free edge negation) for all n-variable functions, n<=3.
Method: layered BFS over sets of computed truth tables is too big; instead iterative-deepening
DFS per target with canonical ordering (gate truth tables strictly increasing in discovery order not enforced; dedupe by set).
Wires counted = 2 per AND gate (+1 output edge)."""
import sys, itertools, json, time
n=int(sys.argv[1]); N=1<<n; M=(1<<N)-1
vars_=[sum(1<<i for i in range(N) if (i>>v)&1) for v in range(n)]
def lits(tts):
    out=set()
    for t in tts: out.add(t); out.add(M^t)
    return out
def solve(maxk):
    # best[f]=min gates; DFS over sets of gate functions, record every function reachable at depth k
    best={}
    for t in [0,M]+vars_+[M^v for v in vars_]: best[t]=0
    seen=set()
    def dfs(gates,k):
        cur=[0]+vars_+gates
        L=sorted(lits(cur))
        for t in L:
            if t not in best or best[t]>k: best[t]=min(best.get(t,99),k)
        if k==maxk: return
        key=frozenset(gates)
        if key in seen: return
        seen.add(key)
        for a,b in itertools.combinations_with_replacement(L,2):
            g=a&b
            if g in lits(cur): continue
            dfs(gates+[g],k+1)
    dfs([],0)
    return best
t0=time.time()
maxk=int(sys.argv[2])
best=solve(maxk)
tot=1<<N
from collections import Counter
c=Counter(best.values())
print("n",n,"maxk",maxk,"functions reached",len(best),"of",tot,"hist",sorted(c.items()),"time",round(time.time()-t0,1))
json.dump({"n":n,"maxk":maxk,"reached":len(best),"total":tot,"hist":sorted(c.items())},open(f"aig_n{n}_k{maxk}.json","w"))
