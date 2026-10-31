"""Exact min B2 circuit size (2-input gates, all 16 ops) for all n-var functions, n<=3.
BFS over sets of computed functions (inputs given free). Usage: mincirc.py n maxdepth"""
import sys, itertools, json
n=int(sys.argv[1]); D=int(sys.argv[2]); R=2**n; M=(1<<R)-1
inp=[sum(1<<a for a in range(R) if (a>>i)&1) for i in range(n)]
ops=[lambda x,y,t=t:(((t>>0&1)*(~x&~y))|((t>>1&1)*(~x&y))|((t>>2&1)*(x&~y))|((t>>3&1)*(x&y)))&M for t in range(16)]
best={}
for f in (0,M)+tuple(inp): best[f]=0
for i in inp: best[M^i]=1  # NOT = 1 gate
best[0]=0;best[M]=0
level={frozenset(inp)}
seen={frozenset(inp):0}
for d in range(1,D+1):
    nxt=set()
    for S in level:
        L=list(S)
        for x,y in itertools.combinations(L,2):
            for t in range(1,15):
                v=ops[t](x,y)
                if v in S: continue
                T=S|{v}
                if T in seen: continue
                seen[T]=d; nxt.add(T)
                if v not in best or best[v]>d: best[v]=d
    level=nxt
    print("depth",d,"states",len(level),"funcs found",len(best),"of",2**R,flush=True)
from collections import Counter
# constants and negated inputs: size 0 / treat NOT as gate with fan-in 2 op
c=Counter(best.values())
print(sorted(c.items()))
json.dump({"n":n,"maxdepth":D,"found":len(best),"total":2**R,"hist":sorted(c.items())},open(f"mincirc_n{n}.json","w"))
