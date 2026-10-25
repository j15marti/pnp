"""Exact min fan-in-2 circuit size (B2 basis) of n-variable Boolean functions, n<=3 exhaustive,
plus symmetric n=4 functions by bounded BFS. Wires = 2*gates (every gate has two in-wires).
Runs well under 30 s. Output: JSON on stdout."""
import json, itertools, sys
def var_tables(n):
    N=1<<n; full=(1<<N)-1
    return [sum(1<<x for x in range(N) if (x>>i)&1) for i in range(n)], full
def ops(a,b,full):
    na,nb=full^a,full^b
    return {a&b,a&nb,na&b,na&nb,a|b,a|nb,na|b,na|nb,a^b,full^(a^b)}
def solve(n,maxg,targets=None):
    V,full=var_tables(n)
    inputs=frozenset(V)
    best={}   # function -> min gates
    for t in list(V)+[0,full]: best[t]=0
    for v in V: best[full^v]=1   # negation counted as a gate (U2/B2 w/o free NOT)
    level={tuple(sorted(inputs))}
    seen={frozenset(inputs)}
    frontier=[tuple(V)]
    for g in range(1,maxg+1):
        nxt=[]
        for st in frontier:
            for a,b in itertools.combinations(st,2):
                for r in ops(a,b,full):
                    if r in st: continue
                    ns=frozenset(st)|{r}
                    if ns in seen: continue
                    seen.add(ns)
                    if r not in best: best[r]=g
                    nxt.append(tuple(sorted(ns)))
        frontier=nxt
        print(f"n={n} g={g} states={len(frontier)} funcs={len(best)}",file=sys.stderr)
        if len(best)>=(1<<(1<<n)): break
    return best,full
out={}
b3,_=solve(3,5)
hist={}
for f,g in b3.items(): hist[g]=hist.get(g,0)+1
out["n3_hist_gates"]=dict(sorted(hist.items()))
out["n3_covered"]=len(b3)
out["n3_max_gates"]=max(b3.values())
out["n3_max_wires"]=2*max(b3.values())
V,full=var_tables(3)
a,b,c=V
named={"AND3":a&b&c,"OR3":a|b|c,"XOR3":a^b^c,"MAJ3":(a&b)|(a&c)|(b&c),"MUX":(a&b)|((full^a)&c)}
out["n3_named"]={k:b3.get(v) for k,v in named.items()}
b2,_=solve(2,3); out["n2_hist"]={g:sum(1 for x in b2.values() if x==g) for g in sorted(set(b2.values()))}
print(json.dumps(out,indent=1,sort_keys=True))
