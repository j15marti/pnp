"""Exact minimum tree-like Resolution refutation leaf count for PHP^{n+1}_n
(n=1..3) via falsified-clause decision-tree DP, plus a polynomial counting
decider on the same family (hostile control). Deterministic; < 30 s."""
import json, sys, time, itertools, hashlib
from functools import lru_cache

def php(n):
    m = n + 1
    var = {(i, j): i * n + j for i in range(m) for j in range(n)}
    cls = [[(var[i, j], 1) for j in range(n)] for i in range(m)]
    for j in range(n):
        for a, b in itertools.combinations(range(m), 2):
            cls.append([(var[a, j], 0), (var[b, j], 0)])
    return m * n, cls

def min_leaves(nv, cls):
    # state: tuple of length nv over {0,1,2}; 2 = unassigned
    def falsified(st):
        return any(all(st[v] != 2 and st[v] != s for v, s in c) for c in cls)
    @lru_cache(maxsize=None)
    def L(st):
        if falsified(st):
            return 1
        best = None
        for v in range(nv):
            if st[v] == 2:
                a = L(st[:v] + (0,) + st[v+1:])
                if best is not None and a >= best:
                    continue
                b = L(st[:v] + (1,) + st[v+1:])
                if best is None or a + b < best:
                    best = a + b
        return best
    r = L((2,) * nv)
    return r, L.cache_info().currsize

def counting_decider_steps(n):
    # Decide the PHP^{n+1}_n *family member* by structure check + counting:
    # recognise the family encoding (O(size)) and answer UNSAT since m>n.
    nv, cls = php(n)
    steps = sum(len(c) for c in cls)  # one pass over the encoding
    return steps

out = {"family": "PHP^{n+1}_n", "rows": []}
for n in (1, 2, 3):
    t = time.time()
    nv, cls = php(n)
    leaves, states = min_leaves(nv, cls)
    out["rows"].append({"n": n, "vars": nv, "clauses": len(cls),
        "encoding_literals": sum(len(c) for c in cls),
        "min_treelike_leaves": leaves,
        "min_treelike_size_2L_minus_1": 2 * leaves - 1,
        "dp_states": states,
        "counting_decider_steps": counting_decider_steps(n),
        "seconds": round(time.time() - t, 3)})
src = open(__file__, "rb").read()
out["code_sha256"] = hashlib.sha256(src).hexdigest()
json.dump(out, sys.stdout, indent=1)
