"""Minimum gate counts (circuits with sharing) for Boolean functions on n<=3 inputs.
Basis: {AND,OR} fan-in 2 with free negation on wires.  Wires = 2*gates (fan-out free).
BFS over sets of computed functions up to depth cap D; functions not reached have min gates > D.
Runtime well under 30 s."""
import json, sys, itertools
def run(n, D):
    N = 1 << n; full = (1 << N) - 1
    v = [sum(1 << a for a in range(N) if (a >> i) & 1) for i in range(n)]
    best = {0: 0, full: 0}
    for f in v: best[f] = 0; best[f ^ full] = 0
    rep = lambda f: min(f, f ^ full)
    start = frozenset(rep(f) for f in v)
    frontier = {start}; seen = {start}
    for g in range(1, D + 1):
        nxt = set()
        for S in frontier:
            for x, y in itertools.combinations(sorted(S), 2):
                for a in (x, x ^ full):
                    for b in (y, y ^ full):
                        for h in (a & b, a | b):
                            r = rep(h)
                            if r in S or r == 0: continue
                            S2 = S | {r}
                            if S2 in seen: continue
                            seen.add(S2); nxt.add(S2)
                            for f in (h, h ^ full): best.setdefault(f, g)
        frontier = nxt
    return best
if __name__ == '__main__':
    out = {}
    for n, D in ((1, 1), (2, 3), (3, 5)):
        best = run(n, D)
        hist = {}
        for g in best.values(): hist[g] = hist.get(g, 0) + 1
        uniq = sorted({g for f, g in best.items() if bin(f).count('1') == 1})
        out[f'n{n}'] = dict(depth_cap=D, functions_reached=len(best), total=1 << (1 << n), hist=dict(sorted(hist.items())), unique_solution_min_gates=uniq)
    json.dump(out, open(sys.argv[1], 'w'), indent=1); print(json.dumps(out))
