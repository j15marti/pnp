# Exact minimal fan-in-2 circuit size (basis B2: all 16 binary gates, free constants/negation absorbed)
# for all n-input Boolean functions, by BFS over sets of computed truth tables.
import sys, json, itertools
n=int(sys.argv[1]); N=1<<n; M=(1<<N)-1
inputs=[sum(((x>>i)&1)<<x for x in range(N)) for i in range(n)]
def gates(a,b):
    out=set()
    for g in range(16):
        r=0
        for (u,v,bit) in ((0,0,0),(0,1,1),(1,0,2),(1,1,3)):
            if (g>>bit)&1:
                r|=(b if v else (~b&M)) & (a if u else (~a&M))
        out.add(r)
    return out
# normalise: f and ~f cost the same (negation free); keep functions as-is but identify via min(f,~f)
norm=lambda f:min(f,~f&M)
start=frozenset(norm(x) for x in inputs)|frozenset([0])
cost={}  # function(norm) -> min gates
level={start}
seen={start}
for f in start: cost[f]=0
k=0
while len(cost)<(1<<(N-1)) and k<8:
    k+=1; nxt=set()
    for S in level:
        L=list(S)
        for a,b in itertools.combinations(L,2):
            for r in gates(a,b):
                r=norm(r)
                if r in S: continue
                T=S|{r}
                if T not in seen:
                    seen.add(T); nxt.add(T)
                if r not in cost: cost[r]=k
    level=nxt
    print(k,len(level),len(cost),file=sys.stderr)
hist={}
for f,c in cost.items(): hist[c]=hist.get(c,0)+1
print(json.dumps({"n":n,"functions_up_to_negation":1<<(N-1),"found":len(cost),"hist":hist}))
