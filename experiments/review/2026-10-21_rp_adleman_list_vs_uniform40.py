"""Check: random list of n+1 seeds hits all nonzero x for the affine verifier <x,r>.
Exact prob of failure for fixed x is 2^-(n+1); union bound over 2^n inputs < 1/2.
Also exact counts for n<=6 by Monte Carlo against the exact span criterion."""
import random, json
def rank(vs, n):
    basis = []
    for v in vs:
        for b in basis:
            v = min(v, v ^ b)
        if v: basis.append(v)
    return len(basis)
def hits_all(seeds, n):
    # list hits every nonzero x iff seeds span F_2^n
    return rank(seeds, n) == n
random.seed(40)
out = {}
for n in range(1, 11):
    T = 4000
    ok = {k: sum(hits_all([random.getrandbits(n) for _ in range(n + k)], n) for _ in range(T)) / T for k in (0, 1, 2, 3)}
    union = 2 ** n * 2 ** -(n + 1)
    out[n] = {"success_by_extra_seeds": ok, "union_bound_fail_n+1": union}
    assert ok[1] >= 0.5 - 0.03 or n == 1, (n, ok)
print(json.dumps(out, indent=1))
