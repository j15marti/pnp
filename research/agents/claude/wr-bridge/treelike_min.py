"""Exact minimum tree-like resolution refutation size (= min decision tree leaves)
for PHP^{n+1}_n and Tseitin-free controls. Each run < 30 s. Usage: python treelike_min.py N"""
import sys, json, time
from functools import lru_cache
def php(n):
    v=lambda i,j: i*n+j+1
    C=[tuple(v(i,j) for j in range(n)) for i in range(n+1)]
    for j in range(n):
        for a in range(n+1):
            for b in range(a+1,n+1): C.append((-v(a,j),-v(b,j)))
    return frozenset(frozenset(c) for c in C), (n+1)*n
def restrict(F,l):
    out=set()
    for c in F:
        if l in c: continue
        out.add(c-{-l})
    return frozenset(out)
@lru_cache(maxsize=None)
def L(F):
    if frozenset() in F: return 1
    vs={abs(x) for c in F for x in c}
    if not vs: raise ValueError("satisfiable")
    best=None
    for x in sorted(vs):
        a=L(restrict(F,x));
        if best is not None and a>=best: continue
        s=a+L(restrict(F,-x))
        if best is None or s<best: best=s
    return best
n=int(sys.argv[1]); F,nv=php(n); t=time.time(); leaves=L(F)
print(json.dumps({"family":"PHP","n":n,"vars":nv,"clauses":len(F),"min_leaves":leaves,"min_treelike_size":2*leaves-1,"secs":round(time.time()-t,2)}))
