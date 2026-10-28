"""Exact minimum gate count (fan-in 2, basis {AND,OR,XOR,NAND,NOR,XNOR,and-with-negations = all 10 nondegenerate binary ops},
inputs and constants free) for ALL n-variable Boolean functions, n=1..3, by BFS over sets of computed truth tables
(iterative deepening on gate count). Runtime ~ seconds. Wires = 2*gates (fan-in 2). Output JSON."""
import itertools, json, sys, time
def run(n, maxg):
    N=1<<n; full=(1<<N)-1
    inputs=[sum(1<<a for a in range(N) if (a>>i)&1) for i in range(n)]
    ops=[lambda a,b:a&b, lambda a,b:a|b, lambda a,b:a^b, lambda a,b:(~a)&b&full, lambda a,b:a&(~b)&full,
         lambda a,b:~(a&b)&full, lambda a,b:~(a|b)&full, lambda a,b:~(a^b)&full, lambda a,b:(~a|b)&full, lambda a,b:(a|~b)&full]
    best={0:0,full:0}
    for v in inputs: best[v]=0
    base=frozenset(set(inputs)|{0,full})
    frontier={base}; seen={base}
    for g in range(1,maxg+1):
        nxt=set()
        for S in frontier:
            L=list(S)
            for a,b in itertools.combinations(L,2):
                for op in ops:
                    r=op(a,b)
                    if r in S: continue
                    T=S|{r}
                    if T in seen: continue
                    seen.add(T); nxt.add(T)
                    if r not in best: best[r]=g
        frontier=nxt
        if len(best)==1<<N: break
    hist={}
    for f,c in best.items(): hist[c]=hist.get(c,0)+1
    return {"n":n,"functions":1<<N,"found":len(best),"max_gates":max(best.values()),"hist":hist}
if __name__=="__main__":
    t=time.time(); out=[run(1,2),run(2,3),run(3,6)]
    print(json.dumps(out,indent=1),time.time()-t,file=sys.stderr)
    json.dump(out,open("../../results/raw/claude_circuitsat/mincircuit_n123.json","w"),indent=1)
