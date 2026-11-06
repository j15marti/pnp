"""Exact minimum DAG-resolution refutation size for tiny UNSAT 3-CNFs (W_Res small cases).
Cost = number of resolution steps (derived clauses, shared DAG). Iterative deepening over
sets of derived clauses; each run is time-boxed (<30s)."""
import itertools, random, sys, time, json
def clauses(n,k=3):
    out=[]
    for vs in itertools.combinations(range(1,n+1),k):
        for sg in itertools.product((1,-1),repeat=k):
            out.append(frozenset(v*s for v,s in zip(vs,sg)))
    return out
def sat(F,n):
    for m in range(1<<n):
        if all(any(((m>>(abs(l)-1))&1)==(l>0) for l in c) for c in F): return True
    return False
def res(a,b):
    r=[]
    for l in a:
        if -l in b:
            c=(a|b)-{l,-l}
            if not any(-x in c for x in c): r.append(frozenset(c))
    return r
def minsize(F,limit,deadline):
    """Exact: BFS over sets of derived clauses (deduplicated); returns min #resolution steps."""
    start=frozenset(F); level={start}; seen={start}
    for k in range(1,limit+1):
        nxt=set()
        for S in level:
            if time.time()>deadline: raise TimeoutError
            L=list(S)
            for i in range(len(L)):
                for j in range(i+1,len(L)):
                    for c in res(L[i],L[j]):
                        if c in S: continue
                        T=S|{c}
                        if c==frozenset(): return k
                        if T not in seen: seen.add(T); nxt.add(T)
        level=nxt
    return None
if __name__=="__main__":
    n=int(sys.argv[1]); trials=int(sys.argv[2]); random.seed(int(sys.argv[3]))
    U=clauses(n); best=(0,None); t0=time.time(); cnt=0; hist={}
    while time.time()-t0<22 and cnt<trials:
        m=random.randint(len(U)//2,len(U)); F=random.sample(U,m)
        if sat(F,n): continue
        # make irredundant: drop clauses while still unsat
        for c in list(F):
            G=[d for d in F if d!=c]
            if not sat(G,n): F=G
        try: s=minsize(F,12,time.time()+3)
        except TimeoutError: continue
        cnt+=1; hist[s]=hist.get(s,0)+1
        if s and s>best[0]: best=(s,[sorted(c) for c in F])
    print(json.dumps({"n":n,"unsat_irredundant_tested":cnt,"hist":hist,"max_min_steps":best[0],"witness":best[1]}))
