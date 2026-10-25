"""Exact deterministic leaf-query complexity of SAT for AND of k literals over n vars.
Brute-force minimax over partial leaf reads. Runs in seconds for k<=4,n<=4."""
import itertools, json, functools, sys
def run(k, n):
    lits = [(v, s) for v in range(n) for s in (0, 1)]
    inputs = list(itertools.product(lits, repeat=k))
    sat = lambda x: len({(v, s) for v, s in x if True}) == len(set(v for v, _ in x)) 
    def f(x):
        d = {}
        for v, s in x:
            if d.setdefault(v, s) != s: return 0
        return 1
    @functools.lru_cache(None)
    def D(partial):
        cons = [x for x in inputs if all(p is None or x[i] == p for i, p in enumerate(partial))]
        if len({f(x) for x in cons}) <= 1: return 0
        best = 99
        for i, p in enumerate(partial):
            if p is None:
                worst = 0
                for l in lits:
                    q = partial[:i] + (l,) + partial[i+1:]
                    if any(all(pp is None or x[j] == pp for j, pp in enumerate(q)) for x in inputs):
                        worst = max(worst, D(q))
                best = min(best, 1 + worst)
        return best
    return D((None,) * k)
res = {}
for k in range(1, 5):
    for n in range(1, 5):
        res[f"k={k},n={n}"] = run(k, n)
print(json.dumps(res, indent=1))
json.dump(res, open("and_leaf_query_results.json", "w"), indent=1)
