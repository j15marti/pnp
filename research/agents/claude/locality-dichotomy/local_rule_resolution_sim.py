"""Check of Lemma 2 (local-rule simulation) in
2026-11-12_1300_CLAUDE_WORSTCASE-BRIDGE-0001.tex.

For random k-tuples of width<=w clauses over V variables and every sound
consequence C (any clause on those variables implied by the premises), verify
that the resolution closure of the premises contains a clause D subseteq C,
and record the closure size, compared with the bound 3^{|vars|}.
Runs in a few seconds; fixed seed; writes JSON next to this file.
"""
import itertools, json, random, os, time

def implied(prem, C, vs):
    # C implied iff every assignment satisfying all premises satisfies C
    for bits in itertools.product([0, 1], repeat=len(vs)):
        a = dict(zip(vs, bits))
        sat = lambda cl: any((a[abs(l)] == 1) == (l > 0) for l in cl)
        if all(sat(p) for p in prem) and not sat(C):
            return False
    return True

def closure(prem):
    S = set(frozenset(p) for p in prem)
    while True:
        new = set()
        for A, B in itertools.combinations(S, 2):
            for l in A:
                if -l in B:
                    R = (A - {l}) | (B - {-l})
                    if not any(-x in R for x in R) and R not in S:
                        new.add(frozenset(R))
        if not new:
            return S
        S |= new

def main(seed=20261112, trials=300, V=6, w=3, kmax=3):
    rng = random.Random(seed); t0 = time.time()
    stats = {"trials": 0, "consequences_checked": 0, "failures": 0, "max_closure": 0, "max_bound": 0}
    for _ in range(trials):
        k = rng.randint(2, kmax)
        prem = []
        for _ in range(k):
            vs = rng.sample(range(1, V + 1), rng.randint(1, w))
            prem.append(tuple(v if rng.random() < .5 else -v for v in vs))
        vs = sorted({abs(l) for p in prem for l in p})
        cl = closure(prem)
        stats["max_closure"] = max(stats["max_closure"], len(cl))
        stats["max_bound"] = max(stats["max_bound"], 3 ** len(vs))
        assert len(cl) <= 3 ** len(vs)
        for size in range(0, len(vs) + 1):
            for sub in itertools.combinations(vs, size):
                for signs in itertools.product([1, -1], repeat=size):
                    C = frozenset(s * v for s, v in zip(signs, sub))
                    if implied(prem, C, vs):
                        stats["consequences_checked"] += 1
                        if not any(D <= C for D in cl):
                            stats["failures"] += 1
        stats["trials"] += 1
    stats["seconds"] = round(time.time() - t0, 2)
    stats["params"] = {"seed": seed, "V": V, "w": w, "kmax": kmax}
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "local_rule_resolution_sim_results.json")
    json.dump(stats, open(out, "w"), indent=1)
    print(json.dumps(stats))

if __name__ == "__main__":
    main()
