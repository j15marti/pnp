# Exact min gate count (fan-in-2 AND/OR/XOR, free negation) over all functions on n inputs, n<=3.
# Iterative deepening over sets of available truth tables; chunking: n<=3 finishes in seconds.
import sys, json, itertools
def run(n):
    N=1<<n; M=(1<<N)-1
    ins=[sum(1<<a for a in range(N) if (a>>i)&1) for i in range(n)]
    base={0,M}; 
    for v in ins: base.add(v)
    def close(S): return S|{M^x for x in S}
    best={}
    def rec(S,k,maxk):
        for f in S:
            if f not in best or best[f]>k: best[f]=k
        if k==maxk: return
        L=sorted(S)
        for a,b in itertools.combinations(L,2):
            for g in (a&b,a|b,a^b):
                if g not in S:
                    rec(close(S|{g}),k+1,maxk)
    # BFS-ish DFS with memo on frozenset
    seen={}
    def dfs(S,k,maxk):
        key=frozenset(S)
        if seen.get(key,99)<=k: return
        seen[key]=k
        for f in S:
            if f not in best or best[f]>k: best[f]=k
        if k==maxk: return
        L=sorted(S)
        for a,b in itertools.combinations(L,2):
            for g in (a&b,a|b,a^b):
                if g not in S: dfs(close(S|{g}),k+1,maxk)
    dfs(close(base),0,int(sys.argv[2]))
    return best,N
n=int(sys.argv[1]); best,N=run(n)
hist={}
for f,k in best.items(): hist[k]=hist.get(k,0)+1
M=(1<<N)-1
minterm=[best[f] for f in best if bin(f).count('1')==1]
print(json.dumps({"n":n,"covered":len(best),"of":1<<N,"hist":hist,"unique_sat_min":sorted(set(minterm))}))
