"""DERIVED-SUBCUBE-MERGE75: exact source-aware merge of forbidden-row blocks.
Block B_a forbids row a in {0,1}^k. A set T of rows is merged by repeated
resolution (subcube merge, Quine-McCluskey step) into prime forbidden cubes.
Checks (a) exactness vs brute force, (b) size of merged child vs block count,
(c) hostile controls: random row subsets, where merging need not compress.
Runtime: seconds."""
import itertools, json, random

def merge(cubes):
    # cube = (mask, val): fixed bits mask; free elsewhere. Pairwise resolution to fixpoint.
    cubes = set(cubes)
    while True:
        new = set(); used = set()
        L = list(cubes)
        d = {}
        for c in L: d.setdefault(c[0], set()).add(c[1])
        for mask, vals in d.items():
            for v in vals:
                for b in range(mask.bit_length()):
                    if mask >> b & 1:
                        w = v ^ (1 << b)
                        if w in vals:
                            new.add((mask & ~(1 << b), v & ~(1 << b))); used.add((mask, v)); used.add((mask, w))
        if not new: return cubes
        cubes = (cubes - used) | new

def forbids(cubes, k):
    out = set()
    for s in range(1 << k):
        if any((s & m) == v for m, v in cubes): out.add(s)
    return out

res = {"exact_checks": 0, "failures": 0, "full_cover": {}, "random_density": {}}
rng = random.Random(75)
for k in range(1, 11):
    full = (1 << k) - 1
    T = [(full, a) for a in range(1 << k)]
    M = merge(T)
    ok = forbids(M, k) == set(range(1 << k)) and M == {(0, 0)}
    res["full_cover"][k] = {"blocks": 1 << k, "merged_cubes": len(M), "unsat_empty_clause": ok}
    res["exact_checks"] += 1; res["failures"] += (not ok)
    # every proper subtree (prefix subcube) merges to ONE clause of k-j literals, exactly
    for j in range(k + 1):
        for p in range(1 << j):
            rows = [(full, (p << (k - j)) | r) for r in range(1 << (k - j))]
            M = merge(rows)
            exp = {(((1 << j) - 1) << (k - j), p << (k - j))}
            res["exact_checks"] += 1; res["failures"] += (M != exp)
for k in (6, 8, 10):
    for dens in (0.25, 0.5, 0.75, 0.9, 0.99):
        sizes = []
        for _ in range(5):
            rows = [a for a in range(1 << k) if rng.random() < dens]
            M = merge([((1 << k) - 1, a) for a in rows])
            f = forbids(M, k); exact = f == set(rows)
            res["exact_checks"] += 1; res["failures"] += (not exact)
            sizes.append((len(rows), len(M), sum(bin(m).count("1") for m, _ in M)))
        res["random_density"][f"k{k}_d{dens}"] = sizes
print(json.dumps({k: v for k, v in res.items() if k != "random_density"}, indent=0)[:1500])
for key, v in res["random_density"].items():
    print(key, "rows,cubes,literals:", v[0], v[-1])
json.dump(res, open("results/raw/synthesis/2026-10-22_derived_subcube_merge75.json", "w"))
