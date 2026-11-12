"""Control for CLAUDE B3-RELATIVIZATION-0001.
Exact minimum Resolution DAG refutation length (number of derived clauses)
for every UNSAT CNF over n=2 variables (all clause sets) and a seeded sample
of UNSAT 3-CNFs over n=3, versus a 1-query oracle decider.  Illustrates that
decision cost (oracle model) and the free-strategy minimum W_Res are
different quantities.  Finite control only; no asymptotic claim.
Runtime target < 30 s.  Usage: python3 min_res_vs_oracle.py out.json"""
import itertools, json, random, sys, time
def lits(n): return [v for i in range(1, n+1) for v in (i, -i)]
def clauses(n, w):
    out = []
    for k in range(1, w+1):
        for vs in itertools.combinations(range(1, n+1), k):
            for s in itertools.product((1, -1), repeat=k):
                out.append(frozenset(v*t for v, t in zip(vs, s)))
    return out
def sat(F, n):
    return any(all(any((l > 0) == a[abs(l)-1] for l in C) for C in F)
               for a in itertools.product((False, True), repeat=n))
def resolvents(S):
    S = list(S); out = set()
    for i in range(len(S)):
        for j in range(i+1, len(S)):
            A, B = S[i], S[j]
            piv = [l for l in A if -l in B]
            if len(piv) == 1:
                R = (A | B) - {piv[0], -piv[0]}
                out.add(frozenset(R))
    return out
def min_res(F, cap=9):
    F = frozenset(F)
    if frozenset() in F: return 0
    for d in range(1, cap+1):
        seen = set()
        def dfs(S, k):
            if frozenset() in S: return True
            if k == 0 or (S, k) in seen: return False
            seen.add((S, k))
            for R in resolvents(S):
                if R not in S and dfs(S | {R}, k-1): return True
            return False
        if dfs(F, d): return d
    return None
def main(out):
    t0 = time.time(); rec = {"n2_all": [], "n3_sample": []}
    C2 = clauses(2, 2)
    for r in range(1, len(C2)+1):
        for F in itertools.combinations(C2, r):
            if not sat(F, 2):
                rec["n2_all"].append(min_res(F))
    rng = random.Random(20261112); C3 = clauses(3, 3); tried = 0
    while len(rec["n3_sample"]) < 40 and time.time()-t0 < 20:
        F = rng.sample(C3, rng.randint(4, 9)); tried += 1
        if not sat(F, 3):
            m = min_res(F)
            if m is not None: rec["n3_sample"].append({"F": [sorted(c) for c in F], "min_res": m})
    full3 = [frozenset(v*s for v, s in zip((1, 2, 3), sg)) for sg in itertools.product((1, -1), repeat=3)]
    res = {"n2_unsat_count": len(rec["n2_all"]), "n2_min_res_max": max(rec["n2_all"]),
           "n2_min_res_hist": {str(k): rec["n2_all"].count(k) for k in sorted(set(rec["n2_all"]))},
           "n3_sample_count": len(rec["n3_sample"]), "n3_tried": tried,
           "n3_min_res_max": max(x["min_res"] for x in rec["n3_sample"]),
           "complete_3var_min_res": min_res(full3),
           "oracle_decider_queries_per_instance": 1,
           "seconds": round(time.time()-t0, 2), "samples": rec["n3_sample"]}
    assert res["complete_3var_min_res"] == 7
    json.dump(res, open(out, "w"), indent=1); print({k: v for k, v in res.items() if k != "samples"})
if __name__ == "__main__": main(sys.argv[1])
