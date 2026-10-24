# Adaptive (state-parameterized) DP: at each residual state choose the branching
# variable that minimizes the subtree. Exact optimum of tree-like adaptive search
# (= tree-like resolution size for UNSAT) via memoization over residual formulas.
# Compared with the ordered-merging optimum from dp_width.py. Each run < 30 s.
import sys, json
from functools import lru_cache
sys.setrecursionlimit(10000)
from dp_width import php, rand3, brute_sat, widths, bottleneck
def residual(F, v, val):
    out=[]
    for cl in F:
        if (v,val) in cl: continue
        nc=tuple(l for l in cl if l[0]!=v)
        if not nc: return None
        out.append(nc)
    return frozenset(out)
@lru_cache(maxsize=None)
def tree(F, early_exit):
    if F is None: return 1          # dead leaf (falsified clause)
    if not F: return 1              # satisfied leaf
    vs={l[0] for cl in F for l in cl}
    best=None
    for v in vs:
        for first in (0,1):  # adaptive: also choose which branch to try first
            R=residual(F,v,first); a=tree(R,early_exit)
            if early_exit and sat(R): c=1+a  # solution found on first branch: stop
            else: c=1+a+tree(residual(F,v,1-first),early_exit)
            best=c if best is None else min(best,c)
    return best
@lru_cache(maxsize=None)
def sat(F):
    if F is None: return False
    if not F: return True
    v=next(iter(F))[0][0]
    return sat(residual(F,v,0)) or sat(residual(F,v,1))
if __name__=="__main__":
    k=sys.argv[1]
    n,C=php(int(sys.argv[2])) if k=="php" else rand3(int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]))
    F=frozenset(tuple(sorted(cl)) for cl in C)
    W=widths(n,C); b,t,_=bottleneck(n,W)
    print(json.dumps({"inst":sys.argv[1:],"models":brute_sat(n,C),"ordered_merge_total":t,"ordered_merge_maxwidth":b,
       "adaptive_tree_opt":tree(F,True),"distinct_residuals_explored":tree.cache_info().currsize}))
