"""Exact minimum B2 circuit size (gates; wires = 2*gates, fan-in 2) for all n-input functions, n=2,3.
Iterative deepening DFS over gate sequences; each gate = any of 16 binary ops on two earlier nodes.
Run: python3 min_circuit.py  (<30s)"""
import sys, json, itertools
def run(n, maxg):
    N=1<<n; full=(1<<N)-1
    inputs=[]
    for i in range(n):
        v=0
        for a in range(N):
            if (a>>i)&1: v|=1<<a
        inputs.append(v)
    best={}   # function -> min gates
    def ops(a,b):
        na,nb=full^a,full^b
        # all 16 ops via minterm combos
        m=[na&nb,na&b,a&nb,a&b]
        for k in range(16):
            r=0
            for j in range(4):
                if (k>>j)&1: r|=m[j]
            yield r
    # BFS by gate count over sets of nodes (frozenset of node tuples), prune by dedup
    level={tuple(inputs)}
    for f in list(inputs)+[0,full]: best[f]=0
    for g in range(1,maxg+1):
        nxt=set()
        for st in level:
            seen=set(st)
            for i in range(len(st)):
                for j in range(i+1,len(st)):
                    for r in ops(st[i],st[j]):
                        if r in seen: continue
                        if r not in best: best[r]=g
                        nxt.add(tuple(sorted(st+(r,))))
        level=nxt
        print(f"n={n} g={g} states={len(level)} funcs={len(best)}/{1<<N}",flush=True)
        if len(best)==1<<N: break
    return best
if __name__=="__main__":
    out={}
    for n,mg in ((2,3),(3,4)):
        b=run(n,mg)
        hist={}
        for f,g in b.items(): hist[g]=hist.get(g,0)+1
        out[n]=hist
    print(json.dumps(out)); json.dump(out,open("min_circuit_results.json","w"))
