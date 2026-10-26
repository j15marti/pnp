# Exact min gate count (fan-in-2, all 16 binary ops, free output negation implicit) for all functions on n<=3 inputs,
# and wire-edit sensitivity of the AND-chain. Runtime well under 30s.
import json, itertools, sys
def run(n, maxg):
    N=1<<n; full=(1<<N)-1
    ins=[sum(((x>>i)&1)<<x for x in range(N)) for i in range(n)]
    best={}
    for f in [0,full]+ins: best[f]=0
    best[0]=0; best[full]=0
    # BFS over circuits as frozenset-free DFS with iterative deepening, record min gates per realized function
    seen=set()
    def dfs(sigs,g):
        key=(tuple(sorted(sigs)),g)
        if key in seen: return
        seen.add(key)
        for f in sigs:
            if best.get(f,99)>g: best[f]=g
        if g==maxg: return
        L=list(sigs)
        for a,b in itertools.combinations(L,2):
            for op in range(16):
                r=0
                for x in range(N):
                    if (op>>(2*((a>>x)&1)+((b>>x)&1)))&1: r|=1<<x
                if r in sigs: continue
                dfs(sigs|{r},g+1)
    dfs(frozenset(ins),0)
    return best,N
out={}
for n,mg in [(1,0),(2,1),(3,4)]:
    best,N=run(n,mg)
    full=(1<<N)-1
    hist={}
    for f in range(1<<N):
        # function counted up to complement of output (free negation): min over f, ~f
        g=min(best.get(f,99),best.get(full^f,99))
        hist[g]=hist.get(g,0)+1
    out[f"n={n}"]=hist
    print(n,hist)
# Sensitivity of the unsat OR-of-contradictions instance U_n = OR_i (x_i AND NOT x_i).
# Gate list: gadget i = AND(x_i, x_i) with neg on 2nd wire; then OR chain (OR = NOT AND(NOT,NOT)).
# Edits: toggle the negation flag of a single wire (one wire-edit). Count edits that make U_n satisfiable.
def sens(n):
    # wires: 2 per gadget (neg flags a,b), OR-chain implemented as AND with all inputs and output negated: OR(g)=NOT AND(NOT g_i)
    # U_n(x) = OR_i (x_i ^ na) & (x_i ^ nb)  with base na=0, nb=1
    def sat(flags):
        return any(((x>>i)&1)^flags[i][0] and ((x>>i)&1)^flags[i][1] for i in range(n) for x in range(1<<n))
    flags=[[0,1] for _ in range(n)]
    assert not sat(flags)
    flip=0
    for i in range(n):
        for s_ in (0,1):
            flags[i][s_]^=1; flip+=sat(flags); flags[i][s_]^=1
    return dict(unsat_base=True,gadget_wires=2*n,flipping_toggles=flip,total_wires=4*n-2)
res={}
for n in range(1,9):
    res[n]=sens(n); print(n,res[n])
out["or_of_contradictions_sensitivity"]=res
json.dump(out,open("results/raw/claude_circuitsat/ladder_results.json","w"),indent=1)
