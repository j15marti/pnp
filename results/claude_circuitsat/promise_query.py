# Exact deterministic query complexity of SAT-decision under promise "f has 0 or >= s solutions", N=2^n points.
# State: (#queried points answered 0, found1). Brute-force minimax over subsets of {0,1}^n for n<=3 (N<=8).
import sys, json
from functools import lru_cache
def Q(N, s):
    # knowledge: bitmask of zero-points, bitmask of one-points
    @lru_cache(None)
    def go(zeros, ones):
        # decide: if ones nonempty -> SAT known. If |zeros|+... remaining r points: all-zero consistent iff ones empty.
        if ones: return 0
        r = N - bin(zeros).count("1")
        if r < s: return 0   # SAT impossible (needs >= s ones among r unqueried)
        # SAT possible iff r>=1 and s>=1 ; UNSAT possible always. So must query.
        best = N+1
        for p in range(N):
            if zeros>>p & 1: continue
            v = max(1+go(zeros|1<<p, 0), 1+go(zeros, 1<<p))
            best = min(best, v)
        return best
    return go(0,0)
out={}
for n in (1,2,3):
    N=2**n
    out[n]={s:Q(N,s) for s in range(1,N+1)}
    assert all(out[n][s]==N-s+1 for s in out[n]), out[n]
print(json.dumps(out))
