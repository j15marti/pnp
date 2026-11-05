"""Exact minimum DAG-resolution refutation size (number of derived clauses incl. empty clause)
for tiny CNFs, by level-wise BFS over sets of derived clauses with subsumption pruning.
Subsumption pruning is size-safe: replacing a derived clause C by a clause D subseteq C
yields (by induction) a derivation of no greater size ending in a subset of the old clause.
Chunked: each call is time-limited (default 20s) so it respects the 30s runtime rule."""
import itertools, json, random, sys, time

def resolvents(c1, c2):
    out = []
    for l in c1:
        if -l in c2:
            r = (c1 - {l}) | (c2 - {-l})
            if not any(-x in r for x in r):
                out.append(frozenset(r))
    return out

def min_refutation(clauses, cap=9, tlimit=20.0):
    t0 = time.time()
    ax = [frozenset(c) for c in clauses]
    level = {frozenset()}            # sets of derived clauses
    for k in range(1, cap + 1):
        nxt = set()
        for D in level:
            allc = ax + list(D)
            for a, b in itertools.combinations(allc, 2):
                for r in resolvents(a, b):
                    if any(x <= r for x in allc):
                        continue
                    if not r:
                        return k
                    nxt.add(D | {r})
            if time.time() - t0 > tlimit:
                return None
        level = nxt
        if not level:
            return None
    return None

def sat(clauses, n):
    for m in range(1 << n):
        if all(any((l > 0) == bool(m >> (abs(l) - 1) & 1) for l in c) for c in clauses):
            return True
    return False

def is_mus(cl, n):
    return (not sat(cl, n)) and all(sat(cl[:i] + cl[i+1:], n) for i in range(len(cl)))

def sample_mus(n, rng, tries=4000):
    allc = [tuple(s * v for s, v in zip(sg, vs)) for vs in itertools.combinations(range(1, n+1), 3)
            for sg in itertools.product((1, -1), repeat=3)]
    seen = set()
    for _ in range(tries):
        m = rng.randint(n + 3, 3 * n + 4)
        cl = rng.sample(allc, m)
        if sat(cl, n):
            continue
        i = 0
        while i < len(cl):                      # shrink to minimally unsatisfiable core
            if not sat(cl[:i] + cl[i+1:], n): cl.pop(i)
            else: i += 1
        key = frozenset(cl)
        if key not in seen:
            seen.add(key); yield cl

if __name__ == "__main__":
    n = int(sys.argv[1]); seed = int(sys.argv[2]); budget = float(sys.argv[3]) if len(sys.argv) > 3 else 25
    rng = random.Random(seed); t0 = time.time(); rows = []
    for cl in sample_mus(n, rng):
        if time.time() - t0 > budget: break
        w = min_refutation(cl, cap=9, tlimit=3.0)
        rows.append({"m": len(cl), "clauses": cl, "min_res": w})
    res = [r["min_res"] for r in rows if r["min_res"]]
    print(json.dumps({"n": n, "seed": seed, "instances": len(rows), "solved": len(res),
                      "max_min_res": max(res) if res else None,
                      "hist": {str(k): res.count(k) for k in sorted(set(res))}}))
    json.dump(rows, open(f"minres_n{n}_s{seed}.json", "w"))
