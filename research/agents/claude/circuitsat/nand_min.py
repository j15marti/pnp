# Exact minimum NAND-gate (fan-in 2, fan-out unbounded) circuit size per truth table, n inputs.
# Wires = 2*gates (each gate has 2 in-wires). Level-by-level BFS over sets of computed functions.
import sys, json, itertools
n=int(sys.argv[1]); N=1<<n; M=(1<<N)-1
inp=[sum(1<<a for a in range(N) if (a>>i)&1) for i in range(n)]
best={}  # function -> min gates
start=frozenset(inp)
for f in inp: best[f]=0
level={start}; seen={start}
g=0
while level and g<int(sys.argv[2]):
    g+=1; nxt=set()
    for S in level:
        L=list(S)
        for a,b in itertools.combinations_with_replacement(L,2):
            h=M^(a&b)
            if h in S: continue
            T=S|{h}
            if T not in seen: seen.add(T); nxt.add(T)
            if h not in best: best[h]=g
    level=nxt
    print("gates",g,"states",len(nxt),"funcs",len(best),file=sys.stderr)
# table: by satisfying-assignment count k, min gates
tab={}
for f,c in best.items():
    k=bin(f).count("1")
    tab[k]=min(tab.get(k,99),c)
print(json.dumps({"n":n,"maxgates":g,"covered":len(best),"of":1<<N,"min_gates_by_#sat":dict(sorted(tab.items()))}))
