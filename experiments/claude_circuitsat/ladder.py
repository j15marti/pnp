"""Exact minimum fan-in-2 (B2 basis) gate counts of all n<=3-input Boolean functions,
and wire-ledger checks. Runs in a few seconds. Output: results/raw/claude_circuitsat/ladder.json"""
import json, itertools, sys
def tt_inputs(n):
    N=1<<n; M=(1<<N)-1
    xs=[]
    for i in range(n):
        v=0
        for a in range(N):
            if (a>>i)&1: v|=1<<a
        xs.append(v)
    return xs,M
OPS=[lambda a,b:a&b, lambda a,b:a|b, lambda a,b:a^b]  # AND,OR,XOR; negations absorbed via free-NOT closure below
def min_sizes(n, maxg):
    xs,M=tt_inputs(n)
    # free negation: B2 gates up to input/output negation = {AND,OR,XOR} on literals; size counted in gates.
    base=set()
    for v in xs: base|={v,v^M}
    base|={0,M}
    size={f:0 for f in base}
    # exact search via DP over circuits as sets of computed functions (DFS, iterative deepening)
    best={}
    def close(f): return (f,f^M)
    def dfs(avail,depth,limit):
        for f in avail:
            for g in close(f):
                if g not in best or best[g]>depth: best[g]=depth
        if depth==limit: return
        al=list(avail)
        for i in range(len(al)):
            for j in range(i,len(al)):
                for a in (al[i],al[i]^M):
                    for b in (al[j],al[j]^M):
                        for op in OPS:
                            h=op(a,b)
                            if h in avail or h in (0,M): continue
                            avail.add(h); dfs(avail,depth+1,limit); avail.discard(h)
    best={f:0 for f in base}
    dfs(set(xs),0,maxg)
    return best,M
res={}
for n in (1,2,3):
    best,M=min_sizes(n,{1:1,2:2,3:4}[n]) if n<3 else min_sizes(3,4)
    hist={}
    for f in range(M+1):
        hist.setdefault(best.get(f,None),0); hist[best.get(f,None)]+=1
    # all-variables-dependent functions: min size >= n-1
    def depends(f,i):
        N=1<<n
        return any(((f>>a)&1)!=((f>>(a^(1<<i)))&1) for a in range(N))
    viol=[f for f in range(M+1) if all(depends(f,i) for i in range(n)) and best.get(f,99)<n-1]
    xs,_=tt_inputs(n)
    andn=M
    for v in xs: andn&=v
    xorn=0
    for v in xs: xorn^=v
    maj=0
    if n==3: maj=(xs[0]&xs[1])|(xs[0]&xs[2])|(xs[1]&xs[2])
    res[n]={"histogram":{str(k):v for k,v in sorted(hist.items(),key=lambda t:(t[0] is None,t[0]))},
            "violations_of_n_minus_1":len(viol),"size_AND":best.get(andn),"size_XOR":best.get(xorn),"size_MAJ3":best.get(maj) if n==3 else None}
json.dump(res,open("results/raw/claude_circuitsat/ladder.json","w"),indent=1)
print(json.dumps(res,indent=1))
