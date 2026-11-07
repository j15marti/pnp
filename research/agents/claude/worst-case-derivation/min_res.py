"""Exact minimum DAG-resolution refutation length (number of derived clauses,
no weakening) for tiny UNSAT CNFs, by iterative deepening over SETS of derived
clauses.  Free choice of derivation is built in: we minimise over all of them.
Chunking: each formula is an independent run, capped at 20s, result JSON."""
import json, time, itertools, sys
def res(c1,c2):
    out=[]
    for l in c1:
        if -l in c2:
            r=(c1-{l})|(c2-{-l})
            if not any(-x in r for x in r): out.append(frozenset(r))
    return out
def minlen(F,cap=20.0,maxk=14):
    F=[frozenset(c) for c in F]; t0=time.time()
    base=frozenset(F)
    if frozenset() in base: return 0
    for k in range(1,maxk+1):
        seen=set(); 
        def dfs(cl,d):
            if time.time()-t0>cap: raise TimeoutError
            if d==k: return frozenset() in cl
            key=cl
            if (key,d) in seen: return False
            seen.add((key,d))
            L=sorted(cl,key=lambda c:(len(c),sorted(c)))
            for a,b in itertools.combinations(L,2):
                for r in res(a,b):
                    if r in cl: continue
                    if d==k-1 and r!=frozenset(): continue
                    if dfs(cl|{r},d+1): return True
            return False
        try:
            if dfs(base,0): return k
        except TimeoutError: return None
    return None
def php(p,h):
    v=lambda i,j:i*h+j+1
    C=[[v(i,j) for j in range(h)] for i in range(p)]
    for j in range(h):
        for a in range(p):
            for b in range(a+1,p): C.append([-v(a,j),-v(b,j)])
    return C
def xor_cycle(n):  # Tseitin on n-cycle, odd total charge: edge e_i vars 1..n
    C=[]
    for i in range(n):
        a,b=i+1,(i+1)%n+1; ch=1 if i==0 else 0
        for sa in (0,1):
            for sb in (0,1):
                if (sa^sb)!=ch:  # forbid assignments with wrong parity
                    C.append([(-a if sa else a),(-b if sb else b)])
    return C
tests={"PHP_2^3":php(3,2),"unsat_all_2var":[[1,2],[1,-2],[-1,2],[-1,-2]],
 "tseitin_cycle3":xor_cycle(3),"tseitin_cycle4":xor_cycle(4),"tseitin_cycle5":xor_cycle(5)}
res_={}
for n,F in tests.items():
    t=time.time(); m=minlen(F); res_[n]={"clauses":len(F),"min_len":m,"sec":round(time.time()-t,2)}; print(n,res_[n],flush=True)
json.dump(res_,open("min_res_results.json","w"),indent=1)
