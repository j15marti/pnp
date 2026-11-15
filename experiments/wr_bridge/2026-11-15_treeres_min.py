"""Exact minimum tree-like Resolution refutation size via the
falsified-clause decision-tree characterization:
  min #leaves of a tree-like Resolution refutation of F
  = min #leaves of a decision tree solving Search(F)
(each leaf labelled by a clause of F falsified by the path).
Tree size (nodes) = 2*leaves - 1.  Exact memoised search over partial
assignments; each instance is one bounded (<30 s) stage.
"""
import itertools, json, sys, time
from functools import lru_cache

def php(n):  # n+1 pigeons, n holes
    v = lambda p,h: p*n+h+1
    C = [tuple(v(p,h) for h in range(n)) for p in range(n+1)]
    for h in range(n):
        for p,q in itertools.combinations(range(n+1),2):
            C.append((-v(p,h),-v(q,h)))
    return (n+1)*n, C

def tseitin_k4():  # K4, odd charge on one vertex -> UNSAT, 6 edge vars
    E = list(itertools.combinations(range(4),2))
    C=[]
    for x in range(4):
        inc=[i+1 for i,e in enumerate(E) if x in e]
        par = 1 if x==0 else 0
        for signs in itertools.product([0,1],repeat=len(inc)):
            if sum(signs)%2 != par:   # forbid this assignment
                C.append(tuple(-l if s else l for l,s in zip(inc,signs)))
    return 6, C

def mintree(nv, C):
    @lru_cache(maxsize=None)
    def dt(pos, neg):
        P = pos; N = neg
        for c in C:
            if all((l>0 and (N>>l)&1) or (l<0 and (P>>-l)&1) for l in c):
                return 1
        best = None
        for x in range(1, nv+1):
            if not ((P>>x)&1 or (N>>x)&1):
                a = dt(P|(1<<x), N)
                if best is not None and a >= best: continue
                b = dt(P, N|(1<<x))
                if best is None or a+b < best: best = a+b
        return best
    return dt(0,0)

out={}
for name,(nv,C) in [("PHP_3_2",php(2)),("Tseitin_K4",tseitin_k4()),("PHP_4_3",php(3))]:
    t=time.time(); L=mintree(nv,C)
    out[name]={"vars":nv,"clauses":len(C),"min_leaves":L,"min_tree_size":2*L-1,"seconds":round(time.time()-t,2)}
    print(name,out[name],flush=True)
# Independent cross-check without pruning on the two 6-variable instances.
def mintree_plain(nv,C):
    @lru_cache(maxsize=None)
    def dt(P,N):
        if any(all((l>0 and (N>>l)&1) or (l<0 and (P>>-l)&1) for l in c) for c in C): return 1
        return min(dt(P|(1<<x),N)+dt(P,N|(1<<x)) for x in range(1,nv+1) if not((P>>x)&1 or (N>>x)&1))
    return dt(0,0)
for name,(nv,C) in [("PHP_3_2",php(2)),("Tseitin_K4",tseitin_k4())]:
    out[name]["crosscheck_no_pruning"]=mintree_plain(nv,C)
    assert out[name]["crosscheck_no_pruning"]==out[name]["min_leaves"]
print("crosscheck ok")
json.dump(out,open(sys.argv[1],"w"),indent=1)
