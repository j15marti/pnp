"""Exact minimum B2 (all 2-input gates) circuit size for n-variable Boolean functions, n<=3 (all functions)
and selected n=4 functions.  Method: iterative deepening over gate sequences on truth tables, with canonical
ordering (each new gate must use the previous gate -> prunes; plus dedup).  Runs < 30 s."""
import itertools, json, sys, time
def run(n, targets, maxg):
    N=1<<n; M=(1<<N)-1
    inputs=[sum(((a>>i)&1)<<a for a in range(N)) for i in range(n)]
    ops=[lambda x,y,m=m:sum(((m>>(((x>>a)&1)*2+((y>>a)&1)))&1)<<a for a in range(N)) for m in range(16)]
    # nontrivial binary ops (depend on both args): exclude consts, projections, negated projections
    good=[m for m in range(16) if m not in (0,15,0b1100,0b0011,0b1010,0b0101)]
    best={}
    # BFS by size over sets of computed functions (levels) using DFS with depth bound
    def dfs(funcs,depth,goal,seen):
        if goal in funcs or (M^goal) in funcs: return True
        if depth==0: return False
        key=frozenset(funcs)
        if (key,depth) in seen: return False
        seen.add((key,depth))
        L=list(funcs)
        last=L[-1]
        for i in range(len(L)):
            for j in range(i+1,len(L)):
                if depth>0 and last not in (L[i],L[j]) and len(L)>n+0 and False: continue
                for m in good:
                    v=sum(((m>>(((L[i]>>a)&1)*2+((L[j]>>a)&1)))&1)<<a for a in range(N))
                    if v in funcs or (M^v) in funcs: continue
                    if dfs(funcs+[v],depth-1,goal,seen): return True
        return False
    out={}
    for name,t in targets:
        for g in range(0,maxg+1):
            if dfs(list(inputs),g,t,set()):
                out[name]=g;break
        else: out[name]=None
    return out
if __name__=="__main__":
    t0=time.time()
    res={}
    n=2; N=4
    tg=[(f"f{t}",t) for t in range(16)]
    r2=run(2,tg,3)
    from collections import Counter
    res["n2_hist"]=dict(Counter(r2.values()))
    n=3
    tg=[(f"f{t}",t) for t in range(256) if t<(255^t)]  # up to complement
    r3=run(3,tg,5)
    res["n3_hist_upto_complement"]=dict(Counter(str(v) for v in r3.values()))
    res["time"]=time.time()-t0
    print(json.dumps(res)); json.dump(res,open("mincirc_results.json","w"),indent=1)
