# Exhaustive min #fan-in-2 gates (full basis B2, free constants/negation via B2) for
# functions on n inputs with exactly one satisfying assignment (circuit-SAT "unique witness").
# BFS over sets of computed truth tables; each run well under 30s (chunked by n).
import sys, json, itertools
def run(n, maxg):
    N=1<<n; full=(1<<N)-1
    vars_=[sum(((a>>i)&1)<<a for a in range(N)) for i in range(n)]
    B2=range(16)
    def ap(op,x,y):
        r=0
        for a in range(N):
            xb=(x>>a)&1; yb=(y>>a)&1
            if (op>>(xb*2+yb))&1: r|=1<<a
        return r
    best={}
    level={frozenset(vars_)}
    seen={frozenset(vars_)}
    for g in range(0,maxg+1):
        for st in level:
            for f in st:
                if bin(f).count('1')==1 and f not in vars_ and (f not in best): best[f]=g
        if g==maxg: break
        nxt=set()
        for st in level:
            L=sorted(st)
            for i in range(len(L)):
                for j in range(i+1,len(L)):
                    for op in B2:
                        z=ap(op,L[i],L[j])
                        if z in st: continue
                        ns=st|{z}
                        if ns not in seen: seen.add(ns); nxt.add(ns)
        level=nxt
    return {"n":n,"max_gates_searched":maxg,"min_gates_unique_sat":(min(best.values()) if best else None),
            "num_unique_sat_functions_reached":len(best)}
n=int(sys.argv[1]); maxg=int(sys.argv[2])
print(json.dumps(run(n,maxg)))
