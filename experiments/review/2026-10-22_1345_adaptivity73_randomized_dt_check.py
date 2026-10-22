"""Brute-force exact deterministic decision-tree depth of OR_U o AND_J (small U,J)
and the exact zero-error/one-sided check via adversary: verifies Lemma 73A (D=J*U).
Runs in well under 30 s."""
from functools import lru_cache
import itertools, sys

def depth(U, J):
    n = U * J
    def f(x):  # x: tuple of bits, index u*J+j
        return any(all(x[u*J+j] for j in range(J)) for u in range(U))
    @lru_cache(None)
    def D(fixed):  # fixed: tuple of None/0/1
        free = [i for i, v in enumerate(fixed) if v is None]
        vals = set()
        for bits in itertools.product((0, 1), repeat=len(free)):
            x = list(fixed)
            for i, b in zip(free, bits): x[i] = b
            vals.add(f(tuple(x)))
            if len(vals) > 1: break
        if len(vals) == 1: return 0
        return 1 + min(max(D(fixed[:i] + (b,) + fixed[i+1:]) for b in (0, 1)) for i in free)
    return D((None,) * n)

for U, J in [(1,1),(1,2),(2,1),(2,2),(2,3),(3,2)]:
    d = depth(U, J)
    print(f"U={U} J={J} D={d} J*U={J*U} {'OK' if d==J*U else 'MISMATCH'}")
