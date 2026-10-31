# Exact min gate count (basis B2, free negation) for n<=3, restricted to circuits of <=3 gates (functions needing more are "not reached"). Runtime <30 s.
# Also counts #functions by min size and #satisfying assignments. Runtime << 30 s.
import itertools, json, sys
def run(n):
    N=1<<n; M=(1<<N)-1
    xs=[sum(((a>>i)&1)<<a for a in range(N)) for i in range(n)]
    gates=range(16)
    def ap(g,u,v):
        r=0
        for b in range(4):
            if (g>>b)&1:
                uu = u if (b&1) else (~u&M); vv = v if (b&2) else (~v&M)
                r|=uu&vv
        return r
    best={0:0,M:0}
    for x in xs: best[x]=0; best[M^x]=0
    # level-wise: reach[k]=set of frozensets? use DFS with depth limit, record min size per function (last gate output)
    def dfs(wires,k,limit):
        for i in range(len(wires)):
            for j in range(i+1,len(wires)):
                for g in gates:
                    f=ap(g,wires[i],wires[j])
                    if f not in best or best[f]>k+1:
                        best[f]=k+1
                    if k+1<limit: dfs(wires+[f],k+1,limit)
    limit=3
    dfs(list(xs),0,limit)
    return best,N
out={}
for n in (1,2,3):
    best,N=run(n)
    hist={}
    for f,c in best.items(): hist[c]=hist.get(c,0)+1
    # unique-sat functions
    uniq=[c for f,c in best.items() if bin(f).count('1')==1]
    out[n]={"known_functions":len(best),"of":1<<N,"hist":hist,"unique_sat_min_gates":sorted(set(uniq))}
print(json.dumps(out,indent=1))
