# Exact minimum DAG-resolution derivation length (number of resolvent steps, no weakening,
# duplicates/subsumed allowed) for small UNSAT 3-CNFs, via iterative deepening. COMPUTATIONAL.
import itertools, random, json, sys, time
def res(a,b):
    out=[]
    for l in a:
        if -l in b:
            c=(a-{l})|(b-{-l})
            if not any(-x in c for x in c): out.append(frozenset(c))
    return out
import time as _t
def min_steps(F,limit,budget=4.0):
    T0=_t.time()
    F=[frozenset(c) for c in F]; empty=frozenset()
    if empty in F: return 0
    def dfs(cl,k):
        if k==0: return False
        if _t.time()-T0>budget: raise TimeoutError
        L=list(cl)
        for i in range(len(L)):
            for j in range(i):
                for r in res(L[i],L[j]):
                    if r in cl: continue
                    if not r: return True
                    if k>1 and dfs(cl|{r},k-1): return True
        return False
    try:
        for k in range(1,limit+1):
            if dfs(frozenset(F),k): return k
    except TimeoutError: return None
    return None
def unsat(F,n):
    for m in range(1<<n):
        if all(any((l>0)==bool(m>>(abs(l)-1)&1) for l in c) for c in F): return False
    return True
def minimal_unsat(F,n):
    F=list(F)
    for c in list(F):
        G=[d for d in F if d!=c]
        if not unsat(G,n): continue
        F=G
    return F
if __name__=="__main__":
    random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 0)
    t0=time.time(); res_by_n={}
    for n in (3,4,5):
        allc=[tuple(s*v for s,v in zip(sg,vs)) for vs in itertools.combinations(range(1,n+1),3) for sg in itertools.product((1,-1),repeat=3)]
        best=(0,None); seen=set(); cnt=0
        while time.time()-t0<6*(n-2) and cnt<400:
            F=random.sample(allc,min(len(allc),random.randint(n+2,min(len(allc),3*n+4))))
            if not unsat(F,n): continue
            M=minimal_unsat(F,n); key=frozenset(map(frozenset,M))
            if key in seen: continue
            seen.add(key); cnt+=1
            s=min_steps(M,len(M)+3)
            if s is not None and s>best[0]: best=(s,sorted(map(list,M)))
        res_by_n[n]={"sampled_minimal_unsat":cnt,"max_min_steps":best[0],"witness":best[1],"size_clauses":(len(best[1]) if best[1] else None)}
        print(n,res_by_n[n]["sampled_minimal_unsat"],best[0],res_by_n[n]["size_clauses"],flush=True)
    json.dump(res_by_n,open("data/min_res_small.json","w"),indent=1)
