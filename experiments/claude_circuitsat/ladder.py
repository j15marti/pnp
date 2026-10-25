"""Exact min B2-circuit size (gates, fan-in 2, all 16 binary gates) per Boolean function, n<=3,
via layered closure; plus SAT-hardness data. Runs in seconds."""
import json, itertools, sys
def run(n):
    N=1<<n; mask=(1<<N)-1
    ins=[]
    for i in range(n):
        t=0
        for x in range(N):
            if (x>>i)&1: t|=1<<x
        ins.append(t)
    # size-k sets: BFS over sets of computed truth tables (circuit = set of nodes). state=frozenset of tables.
    gates=range(16)
    def ap(g,a,b):
        r=0
        # g bit (2*va+vb)
        for (va,vb,bit) in ((0,0,0),(0,1,1),(1,0,2),(1,1,3)):
            if (g>>bit)&1:
                A=a if va else (~a&mask); B=b if vb else (~b&mask)
                r|=A&B
        return r
    best={}
    start=frozenset(ins)|{0,mask}
    frontier={start}; seen={start}
    for f in start: best.setdefault(f,0)
    k=0
    while len(best)<(1<<N) and k<8:
        k+=1; nxt=set()
        for S in frontier:
            L=list(S)
            for a,b in itertools.combinations_with_replacement(L,2):
                for g in gates:
                    r=ap(g,a,b)
                    if r in S: continue
                    T=S|{r}
                    if T not in seen: seen.add(T); nxt.add(T)
                    best.setdefault(r,k)
        frontier=nxt
        print(n,k,len(frontier),len(best),file=sys.stderr)
    return best
out={}
for n in (1,2,3):
    b=run(n); 
    hist={}
    for v in b.values(): hist[v]=hist.get(v,0)+1
    out[n]={"max_size":max(b.values()),"hist":hist,"num_functions":len(b)}
# SAT-specific: AND_n family exact formula values
out["AND_n"]={str(n):{"gates":n-1,"wires":2*(n-1)+1} for n in range(1,9)}
json.dump(out,open("../../results/raw/claude_circuitsat_ladder.json","w"),indent=1)
print(out)
