"""Exact min gate count over the full binary basis B2 (all 16 two-input ops) for all
Boolean functions on n<=3 inputs, plus the Circuit-SAT 'ladder' statistics.
Runs in a few seconds. Output: results/raw/claude_circuitsat/min_circuit_ladder.json"""
import json, itertools, sys
def run(n):
    N=1<<n; full=(1<<N)-1
    ins=[sum(1<<a for a in range(N) if (a>>i)&1) for i in range(n)]
    best={}   # function -> min gates
    def op(o,x,y):
        r=0
        for k in range(4):
            if (o>>k)&1:
                xs = x if (k&1) else full^x
                ys = y if (k&2) else full^y
                r|=xs&ys
        return r
    # iterative deepening DFS over straight-line programs
    found={0:0,full:0}
    for v in ins: found[v]=0; found[full^v]=0   # negation free (absorbed into B2)
    def dfs(sig,depth,maxd):
        for f in sig: 
            if f not in found or found[f]>len(sig)-n: 
                if f not in found: pass
        k=len(sig)-n
        if k==maxd: return
        L=len(sig)
        for i in range(L):
            for j in range(i+1,L):
                for o in range(16):
                    g=op(o,sig[i],sig[j])
                    if g not in found: found[g]=k+1
                    # canonical: avoid duplicates
                    if g in sig: continue
                    if k+1<maxd: dfs(sig+[g],depth+1,maxd)
    for md in range(1,8):
        before=len(found)
        dfs(list(ins),0,md)
        if len(found)==full+2 or len(found)==1<<N: break
        if len(found)==before and md>5: break
    return found
out={}
for n in (1,2,3):
    f=run(n)
    hist={}
    for v in f.values(): hist[v]=hist.get(v,0)+1
    N=1<<n
    out[n]={"num_functions":1<<N,"covered":len(f),"gate_histogram":dict(sorted(hist.items())),
            "max_gates":max(f.values()),
            "sat_functions":sum(1 for k in f if k!=0)}
    print(n,out[n])
json.dump(out,open("results/raw/claude_circuitsat/min_circuit_ladder.json","w"),indent=1)
