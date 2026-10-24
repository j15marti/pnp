"""Exact minimum B2 (fan-in-2, all 16 gate types) circuit size for all n-input functions, n<=3,
by iterative-deepening DFS over gate lists. Runtime < 30 s per n (chunked by n).
Wires = 2*gates (each gate has two incoming wires); outputs are gates (or inputs/constants)."""
import sys, json, itertools
n = int(sys.argv[1]); MAXG = int(sys.argv[2])
N = 1 << n; FULL = (1 << N) - 1
ins = []
for i in range(n):
    t = 0
    for x in range(N):
        if (x >> i) & 1: t |= 1 << x
    ins.append(t)
# nondegenerate binary ops up to complement of output closure: use the 10 two-var-essential ops
ops = [lambda a,b:a&b, lambda a,b:a&~b&FULL, lambda a,b:~a&b&FULL, lambda a,b:~(a|b)&FULL,
       lambda a,b:a|b, lambda a,b:(a|~b)&FULL, lambda a,b:(~a|b)&FULL, lambda a,b:~(a&b)&FULL,
       lambda a,b:a^b, lambda a,b:~(a^b)&FULL]
best = {0:0, FULL:0}
for t in ins: best[t]=0; best[~t&FULL]=0
def dfs(wires, g, limit):
    for i in range(len(wires)):
        for j in range(i+1, len(wires)):
            a, b = wires[i], wires[j]
            for op in ops:
                v = op(a, b)
                if v in wires: continue
                for u in (v, ~v & FULL):
                    if u not in best or best[u] > g+1: best[u] = g+1
                if g+1 < limit: dfs(wires+[v], g+1, limit)
dfs(list(ins), 0, MAXG)
from collections import Counter
cnt = Counter(best.values())
res = {"n":n,"maxgates_searched":MAXG,"functions_covered":len(best),"of":1<<N,
       "histogram_gates":dict(sorted(cnt.items()))}
# named functions
def tt(f):
    t=0
    for x in range(N):
        if f([(x>>i)&1 for i in range(n)]): t|=1<<x
    return t
named = {"AND":lambda b:all(b),"OR":lambda b:any(b),"XOR":lambda b:sum(b)%2==1,
         "MAJ":lambda b:2*sum(b)>n,"EXACT1":lambda b:sum(b)==1,"EXACT2":lambda b:sum(b)==2,
         "MUX":lambda b:(b[1] if b[0] else b[2]) if n>=3 else False}
res["named"] = {k: best.get(tt(f)) for k,f in named.items() if not (k=="MUX" and n<3)}
print(json.dumps(res))
