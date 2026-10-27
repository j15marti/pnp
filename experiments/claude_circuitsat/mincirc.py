"""Exact minimum fan-in-2 circuit size (all 16 binary gates, free constants/negation via gate choice)
for every Boolean function on n<=3 inputs. Iterative-deepening over gate sequences; truth tables as ints.
Runs well under 30s. Output: JSON summary to stdout."""
import json, itertools, sys
def run(n):
    N=1<<n; M=(1<<N)-1
    xs=[sum(((a>>i)&1)<<a for a in range(N)) for i in range(n)]
    ops=[]
    for t in range(16):
        ops.append(lambda x,y,t=t:(((t&1)*(~x&~y))|(((t>>1)&1)*(~x&y))|(((t>>2)&1)*(x&~y))|(((t>>3)&1)*(x&y)))&M)
    best={}
    for x in xs: best[x]=0
    best[0]=0; best[M]=0
    # level k = set of functions first reachable with k gates (BFS over circuits as ordered lists, pruned by set-of-computed)
    frontier={tuple(sorted(xs))}
    seen_states=set(frontier)
    k=0
    while len(best)<(1<<N) and k<8:
        k+=1; nxt=set()
        for st in frontier:
            for i,a in enumerate(st):
                for b in st[i+1:]:
                    for op in ops:
                        v=op(a,b)
                        if v in st: continue
                        ns=tuple(sorted(st+(v,)))
                        if ns in seen_states: continue
                        seen_states.add(ns); nxt.add(ns)
                        if v not in best: best[v]=k
        frontier=nxt
    return best
def deps(f,n):
    N=1<<n; d=0
    for i in range(n):
        if any(((f>>a)&1)!=((f>>(a^(1<<i)))&1) for a in range(N)): d+=1
    return d
out={}
for n in (1,2,3):
    best=run(n); hist={}; full={}
    for f,k in best.items():
        hist[k]=hist.get(k,0)+1
        if deps(f,n)==n: full[k]=full.get(k,0)+1
    out[n]={"functions":len(best),"hist_by_gates":dict(sorted(hist.items())),"hist_depends_on_all_inputs":dict(sorted(full.items())),"max_gates":max(best.values())}
print(json.dumps(out,indent=1))
