# Independent brute-force check of ARC-INDEX34 Theorem 1 (core selector formulas, no filler/Tseitin).
import itertools
def A(X,h,m): return any(h) and all(not h[i] for i in range(m) if i not in X)
def B(j,h,m): return h[j] and all(not h[i] for i in range(m) if i!=j)
bad=0;cases=0
for m in range(2,9):
    for r in range(m-1):
        for rest in itertools.combinations(range(1,m),r):
            X=set((0,)+rest)
            Hs=list(itertools.product([False,True],repeat=m))
            # exact marginals total over a free var y: trivially total here since y absent; check A,B individually SAT
            assert any(A(X,h,m) for h in Hs)
            for j in range(1,m):
                assert any(B(j,h,m) for h in Hs)
                sat=any(A(X,h,m) and B(j,h,m) for h in Hs)
                cases+=1; bad+= (sat!=(j in X))
print("cases",cases,"violations",bad)
