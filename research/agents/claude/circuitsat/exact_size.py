"""Exact minimum fan-in-2 circuit size over the full binary basis B2, n=1..3.
Level-by-level BFS over sets of computed truth tables (inputs included).
Output: results_exact_size.json. Runs well under 30 s for n<=3."""
import json, itertools, sys, time
n=int(sys.argv[1]); N=1<<n; M=(1<<N)-1
inp=[sum(((x>>i)&1)<<x for x in range(N)) for i in range(n)]
# 10 nondegenerate binary ops as 4-bit tables t[a*2+b]
OPS=[t for t in range(16) if t not in (0,15,3,12,5,10)]
def ap(t,u,v):
    r=0
    for a in (0,1):
        for b in (0,1):
            if (t>>(a*2+b))&1:
                r|=(u if a else ~u&M)&(v if b else ~v&M)
    return r
best={0:0,M:0}
for f in inp: best[f]=0; best[~f&M]=0   # negation free
start=frozenset(inp); level={start}; seen={start}; k=0; t0=time.time()
while len(best)<(1<<N) and k<6:
    k+=1; nxt=set()
    for S in level:
        L=list(S)
        for u,v in itertools.combinations(L,2):
            for t in OPS:
                g=ap(t,u,v)
                if g in S or (~g&M) in S: continue
                T=S|{g}
                if T in seen: continue
                seen.add(T); nxt.add(T)
                for h in (g,~g&M):
                    if h not in best: best[h]=k
    level=nxt
    print(n,k,len(level),len(best),round(time.time()-t0,1),file=sys.stderr)
    if time.time()-t0>20: break
hist={}
for f,c in best.items(): hist[c]=hist.get(c,0)+1
# single-minterm functions (unique satisfying assignment)
mint=[best[1<<x] for x in range(N) if (1<<x) in best]
json.dump({"n":n,"covered":len(best),"of":1<<N,"hist":hist,"minterm_sizes":mint},open(f"results_exact_size_n{n}.json","w"))
print(n,hist,mint)
