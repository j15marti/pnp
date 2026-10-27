"""Exact min #gates (fan-in 2, all 16 binary gate types, unbounded fan-out) per truth table.
Wires = 2*gates (each gate has 2 incoming connections). n<=3 exhaustive; n=4 up to size 4.
Chunked: run `python min_wires.py N MAXG`."""
import sys, json, itertools
n=int(sys.argv[1]); G=int(sys.argv[2]); M=1<<n; FULL=(1<<M)-1
inputs=[sum(1<<x for x in range(M) if (x>>i)&1) for i in range(n)]
def gates(a,b):
    na,nb=FULL^a,FULL^b
    for p,q in ((a,b),(na,b),(a,nb),(na,nb)):
        yield p&q; yield FULL^(p&q)   # AND-type (8 of 16, with output neg)
    yield a^b; yield FULL^(a^b)
    # remaining: constants, projections/negations (degenerate, not new info)
best={}  # function -> min gates
def dfs(wires,g):
    for f in wires[-1:]:   # record only latest
        pass
    if g==G: return
    L=len(wires)
    for i in range(L):
        for j in range(i+1,L):
            for h in set(gates(wires[i],wires[j])):
                if h in wires: continue
                if best.get(h,99)>g+1: best[h]=g+1
                # canonical order pruning: new gate must use the previous gate unless g==0 (reduces reorderings)
                if g>0 and i<L-1 and j<L-1 and False: continue
                dfs(wires+[h],g+1)
for x in inputs: best[x]=0; best[FULL^x]=0
best[0]=0; best[FULL]=0
dfs(inputs[:],0)
by={}
for f,g in best.items(): by[g]=by.get(g,0)+1
pts=[g for f,g in best.items() if bin(f).count('1')==1]
print(json.dumps({"n":n,"maxgates":G,"count_by_size":by,"point_fn_min_gates":sorted(set(pts)),"npoint_found":len(pts),"funcs_found":len(best),"total_funcs":1<<M}))
