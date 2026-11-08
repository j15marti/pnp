"""Exact minimum DAG-resolution refutation size (# derived clauses incl. empty) for tiny UNSAT CNFs.
Iterative deepening; each step adds a non-tautological resolvent of two existing clauses.
Clause = frozenset of nonzero ints. Each run capped by wall clock (<30s). Free choice of strategy (min over all)."""
import itertools, sys, time, json
def res(a,b):
    out=[]
    for l in a:
        if -l in b:
            r=(a-{l})|(b-{-l})
            if not any(-x in r for x in r): out.append(frozenset(r))
    return out
def minref(F, cap=12, tlim=25):
    F=[frozenset(c) for c in F]; t0=time.time()
    def dfs(S,k):
        if time.time()-t0>tlim: raise TimeoutError
        if frozenset() in S: return True
        if k==0: return False
        L=list(S); seen=set()
        for a,b in itertools.combinations(L,2):
            for r in res(a,b):
                if r in S or r in seen: continue
                # subsumed by existing clause -> useless (monotone): skip if some clause subset of r
                if any(c<=r for c in S): continue
                seen.add(r)
                if dfs(S|{r},k-1): return True
        return False
    for k in range(1,cap+1):
        try:
            if dfs(frozenset(F),k): return k
        except TimeoutError: return f">={k}(timeout)"
    return f">{cap}"
def full3():  return [tuple(s*v for s,v in zip(sg,(1,2,3))) for sg in itertools.product((1,-1),repeat=3)]
def php(p,h):
    v=lambda i,j:i*h+j+1
    C=[tuple(v(i,j) for j in range(h)) for i in range(p)]
    C+=[(-v(i,j),-v(k,j)) for j in range(h) for i in range(p) for k in range(i+1,p)]
    return C
def tseitin_k4():
    # K4 edges 0..5, charge odd on one vertex, even others => UNSAT (sum odd)
    E=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]; C=[]
    for v in range(4):
        inc=[i+1 for i,e in enumerate(E) if v in e]; ch=1 if v==0 else 0
        for sg in itertools.product((1,-1),repeat=len(inc)):
            # forbid assignments with wrong parity: clause falsified by assignment x_i = (sg_i==-1)
            if (sum(1 for s in sg if s==-1)%2)!=ch:
                C.append(tuple(s*i for s,i in zip(sg,inc)))
    return C
out={}
for name,F in [("full3(3 vars,8 clauses)",full3()),("PHP_2^3",php(3,2)),("Tseitin_K4",tseitin_k4())]:
    t=time.time(); out[name]={"clauses":len(F),"min_derived":minref(F),"sec":round(time.time()-t,1)}; print(name,out[name],flush=True)
json.dump(out,open("min_res_dag_results.json","w"),indent=1)
