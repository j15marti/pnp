"""Exact minimum fan-in-2 circuit size (AND/OR gates, free negation on wires and output)
for ALL Boolean functions of n<=3 variables, by BFS over sets of computed functions.
Size = number of gates; wires = 2*gates (+ output wire). Runs well under 30 s."""
import json, itertools, sys
def run(n):
    N=1<<n; M=(1<<N)-1
    var=[sum(1<<x for x in range(N) if (x>>i)&1) for i in range(n)]
    lits=set(var)|{v^M for v in var}|{0,M}
    # best[f]=min gates; do iterative deepening on sets of available functions
    best={f:0 for f in lits}
    # normalise up to negation: f and ~f same cost
    def closure(avail):
        out=set()
        L=list(avail)
        for a in L:
            for b in L:
                out.add(a&b); out.add((a^M)&b); out.add(a&(b^M)); out.add((a^M)&(b^M))
        return out
    # DFS with budget k: states = frozenset of available functions (literals + gates)
    sys.setrecursionlimit(10000)
    seen={}
    def search(avail,k,found):
        # record every function reachable with exactly (len gates used)
        pass
    frontier={frozenset(lits)}
    level=0
    allf=set(lits)
    while len(best)<2**N:
        level+=1
        nxt=set()
        for S in frontier:
            for g in closure(S):
                if g in S: continue
                T=frozenset(S|{g,g^M})
                if T in nxt: continue
                nxt.add(T)
                for h in (g,g^M):
                    if h not in best: best[h]=level
        frontier=nxt
        if level>8: break
    return best
res={}
for n in (1,2,3):
    b=run(n)
    from collections import Counter
    c=Counter(b.values())
    N=1<<n
    # functions satisfiable with exactly one model (unique-SAT) and the min gates among them
    uniq=[f for f in b if bin(f).count('1')==1]
    res[n]={"num_functions":len(b),"size_histogram":dict(sorted(c.items())),
            "max_size":max(b.values()),
            "unique_sat_min":min(b[f] for f in uniq),"unique_sat_max":max(b[f] for f in uniq)}
    print(n,res[n])
json.dump(res,open('min_circuit_results.json','w'),indent=1)
