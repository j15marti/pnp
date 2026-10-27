"""Exact minimum AIG size (AND gates, free edge negation) of all n-input functions, n<=3.
Level-by-level BFS over *sets of available truth tables* is too big, so we use
iterative-deepening DFS with canonical gate ordering. Wires = 2*gates (+1 if output
edge counted separately; we report gates and fan-in wires)."""
import sys, json, itertools, time
n=int(sys.argv[1]); maxg=int(sys.argv[2])
N=1<<n; M=(1<<N)-1
inputs=[sum(1<<i for i in range(N) if (i>>j)&1) for j in range(n)]
best={}  # func -> min gates
def canon(f): return min(f,M^f)
def dfs(tabs,k,limit,seen):
    # tabs: list of tables available; record every table (and complement) reached with k gates
    for t in tabs[n:]:
        c=canon(t)
        if c not in best or best[c]>k: best[c]=k
    if k==limit: return
    key=(tuple(sorted(tabs[n:])),)
    L=len(tabs)
    lits=[]
    for t in tabs: lits+= [t,M^t]
    last=tabs[-1] if k>0 else None
    for a,b in itertools.combinations(range(len(lits)),2):
        g=lits[a]&lits[b]
        if g in tabs or (M^g) in tabs or g in (0,M): continue
        if k>0 and (g,)<(0,) : pass
        # canonical order: new gate must use the previous gate OR be larger than previous (avoid permutations)
        uses_last = (tabs[-1]==lits[a] or tabs[-1]==lits[b] or M^tabs[-1]==lits[a] or M^tabs[-1]==lits[b]) if k>0 else True
        if k>0 and not uses_last and canon(g)<canon(tabs[-1]): continue
        dfs(tabs+[g],k+1,limit,seen)
t0=time.time()
for c in inputs: best[canon(c)]=0
best[0]=0
dfs(list(inputs),0,maxg,set())
tot=(1<<(N-1))  # classes up to complement
hist={}
for f in range(M+1):
    if canon(f)==f:
        v=best.get(f, '>%d'%maxg)
        hist[str(v)]=hist.get(str(v),0)+1
print(json.dumps({"n":n,"maxg":maxg,"classes_up_to_negation":tot,"hist_min_gates":hist,"sec":round(time.time()-t0,1)}))
