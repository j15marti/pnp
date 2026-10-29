"""Exact minimum gate count C(f) over the full binary basis B2 (fan-in 2, fan-out free)
for all f:{0,1}^n->{0,1}, n<=3.  BFS over sets of computed truth tables.
Wires of an optimal circuit = 2*gates (fan-in 2).  Runs in a few seconds."""
import sys, json, itertools
n=int(sys.argv[1]); N=1<<n; M=(1<<N)-1
inputs=[sum(((x>>i)&1)<<x for x in range(N)) for i in range(n)]
# nondegenerate binary ops as functions on truth-table ints: AND-type with negations (8) + XOR/XNOR
def ops(a,b):
    na,nb=a^M,b^M
    return {a&b,a&nb,na&b,na&nb,a|b,a|nb,na|b,na|nb,a^b,(a^b)^M}
best={}
for i,t in enumerate(inputs): best[t]=0
for t in (0,M): best[t]=0   # constants free (0 gates)
for t in list(inputs): best.setdefault(t^M,0)  # negation free (absorbed in ops)
frontier={frozenset(inputs)}
seen={frozenset(inputs)}
g=0
while len(best)<(1<<N) and g<8:
    g+=1; nxt=set()
    for S in frontier:
        L=list(S)
        for a,b in itertools.combinations(L,2):
            for c in ops(a,b):
                if c in S or c==0 or c==M: continue
                T=S|{c}
                if T in seen: continue
                seen.add(T); nxt.add(T)
                for x in (c,c^M):
                    if x not in best: best[x]=g
    frontier=nxt
    print("gates",g,"states",len(nxt),"functions known",len(best),file=sys.stderr)
hist={}
for t,v in best.items(): hist[v]=hist.get(v,0)+1
print(json.dumps({"n":n,"max_gates":max(best.values()),"histogram":hist}))
