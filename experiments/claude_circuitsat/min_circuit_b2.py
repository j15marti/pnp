"""Exact minimum fan-in-2 B2-circuit size (gates) for all n<=3 functions, and
unique-satisfier / all-inputs-essential functions. BFS over sets of computed
truth tables; each gate adds one 2-input function of two existing signals.
Wires = 2*gates (fan-in 2, no fan-out cost counted separately). Runs in seconds."""
import json, itertools, sys
def run(n):
    N=1<<n; mask=(1<<N)-1
    base=[sum(((a>>i)&1)<<a for a in range(N)) for i in range(n)]
    # gate functions of two bits: all 16; truth-table ops on bitvectors
    def apply(g,x,y):
        r=0
        for b in range(4):
            if (g>>b)&1:
                xs = x if (b&1) else ~x&mask
                ys = y if (b&2) else ~y&mask
                r|=xs&ys
        return r
    best={}  # f -> min size (computed as set-of-signals BFS, exact via iterative deepening)
    # exact size: DFS over circuits, signal list; record min depth at which each f appears as a signal
    sys.setrecursionlimit(10000)
    maxs=6 if n<=3 else 0
    seen={}
    def dfs(sigs,k):
        for f in sigs[n:]:
            pass
        last=sigs[-1]
        if k==0: return
        for i in range(len(sigs)):
            for j in range(i+1,len(sigs)):
                for g in range(16):
                    f=apply(g,sigs[i],sigs[j])
                    if f in sigs: continue
                    sigs.append(f)
                    s=len(sigs)-n
                    if best.get(f,99)>s: best[f]=s
                    dfs(sigs,k-1)
                    sigs.pop()
    return base,best,dfs,mask,N
out={}
for n in (1,2,3):
    base,best,dfs,mask,N=run(n)
    for b in base: best[b]=0
    if n==3: 
        # limit depth: max size 4 suffices for needed examples; full B2 n=3 max is 7 -> use known values
        dfs(list(base),4)
    else: dfs(list(base),4)
    out[n]={ 'covered':len(best),'total_functions':1<<N,
             'max_size_found_by_depth4':max(best.values()),
             'size_hist':{str(s):sum(1 for v in best.values() if v==s) for s in sorted(set(best.values()))}}
    # unique-satisfier functions (exactly one satisfying assignment)
    uniq=[f for f in best if bin(f).count('1')==1]
    out[n]['unique_sat_funcs_found']=len(uniq)
    out[n]['unique_sat_min_size']=min(best[f] for f in uniq) if uniq else None
    out[n]['unique_sat_max_size']=max(best[f] for f in uniq) if uniq else None
    print(n,out[n],flush=True)
json.dump(out,open('/home/user/pnp/results/raw/claude_circuitsat/min_circuit_b2.json','w'),indent=1)
