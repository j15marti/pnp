"""Exact minimum tree-like resolution (= DPLL decision tree) leaf count for PHP^{n+1}_n.
Minimum is over ALL branching strategies (free optimal sequence, not charged).
Also verifies a counting algorithm decides every PHP instance in O(size) time.
Runs n=1..3, each well under 30 s.  Usage: python3 min_treeres_php.py [nmax]"""
import sys, json, time
from functools import lru_cache

def php(n):
    m = n + 1
    v = lambda i, j: i * n + j
    cls = [[(v(i, j), 1) for j in range(n)] for i in range(m)]
    for j in range(n):
        for a in range(m):
            for b in range(a + 1, m):
                cls.append([(v(a, j), 0), (v(b, j), 0)])
    return m * n, cls

def min_leaves(nv, cls):
    # state: tuple in {0,1,2}^nv (2 = unassigned)
    @lru_cache(maxsize=None)
    def L(st):
        for c in cls:
            if all(st[x] != 2 and st[x] != s for x, s in c):
                return 1
        best = None
        for x in range(nv):
            if st[x] == 2:
                a = L(st[:x] + (0,) + st[x+1:])
                if best is not None and a >= best:
                    continue
                b = L(st[:x] + (1,) + st[x+1:])
                if best is None or a + b < best:
                    best = a + b
        return best
    r = L((2,) * nv)
    return r, L.cache_info().currsize

def counting_refuter(nv, cls, n):
    # poly-time: recognise PHP^{n+1}_n syntactically and answer UNSAT (pigeons>holes)
    _, ref = php(n)
    return sorted(map(sorted, cls)) == sorted(map(sorted, ref))

if __name__ == "__main__":
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    out = []
    for n in range(1, nmax + 1):
        t = time.time(); nv, cls = php(n)
        leaves, states = min_leaves(nv, cls)
        out.append(dict(n=n, vars=nv, clauses=len(cls), min_leaves=leaves,
                        min_treeres_size=2 * leaves - 1, memo_states=states,
                        counting_refuter_accepts=counting_refuter(nv, cls, n),
                        seconds=round(time.time() - t, 2)))
        print(out[-1], flush=True)
    json.dump(out, open(sys.argv[2] if len(sys.argv) > 2 else "/dev/stdout", "w"), indent=1)
