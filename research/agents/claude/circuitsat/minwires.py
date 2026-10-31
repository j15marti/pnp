# Exact minimum gate count (hence wires=2*gates, fan-in 2) over full binary basis B2,
# and over the AND/OR basis with free negations (U2-like, "De Morgan"), for ALL n<=3 functions.
# Method: BFS on the set of reachable truth-table sets is too big; use iterative DFS over gate sequences.
import itertools, json, sys, time
def run(n, basis, maxg):
    N=1<<n; full=(1<<N)-1
    ins=[sum(1<<a for a in range(N) if (a>>i)&1) for i in range(n)]
    consts=[0,full]
    if basis=="B2": ops=[lambda a,b:a&b,lambda a,b:a|b,lambda a,b:a^b,lambda a,b:a&~b&full,lambda a,b:(~a&b)&full,lambda a,b:~(a&b)&full,lambda a,b:~(a|b)&full,lambda a,b:~(a^b)&full]
    else: ops=[lambda a,b:a&b,lambda a,b:a|b,lambda a,b:a&~b&full,lambda a,b:(~a&b)&full,lambda a,b:~(a&b)&full,lambda a,b:~(a|b)&full,lambda a,b:(~a|b)&full,lambda a,b:(a|~b)&full]
    best={}
    # level sets: wires list; dfs with canonical ordering to limit duplicates
    def dfs(wires,g):
        for f in wires:
            for h in (f,(~f)&full):
                if h not in best or best[h]>g: pass
        # record
        for f in wires:
            if f not in best or best[f]>g: best[f]=g
        if g==maxg: return
        key=frozenset(wires)
        if (key,g) in memo: return
        memo.add((key,g))
        seen=set(wires)
        L=len(wires)
        for i in range(L):
            for j in range(i+1,L):
                for op in ops:
                    v=op(wires[i],wires[j])
                    if v in seen: continue
                    dfs(wires+[v],g+1)
    memo=set()
    dfs(ins[:],0)
    return best
res={}
for n,maxg,basis in [(2,3,"B2"),(2,3,"U2"),(3,4,"B2"),(3,4,"U2")]:
    t=time.time(); b=run(n,basis,maxg)
    N=1<<n; full=(1<<N)-1
    funcs=1<<N
    # normalise: negation free in B2 (output negation), count functions found
    found={}
    for f,g in b.items(): found[f]=min(found.get(f,99),g)
    hist={}
    for f in range(funcs):
        g=min(found.get(f,99),found.get((~f)&full,99)) if basis=="B2" else found.get(f,99)
        hist[g]=hist.get(g,0)+1
    res[f"n{n}_{basis}"]=dict(maxg_searched=maxg,hist=hist,secs=round(time.time()-t,1))
    print(n,basis,hist,round(time.time()-t,1),flush=True)
json.dump(res,open("minwires_results.json","w"),indent=1)
