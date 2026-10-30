"""Exact minimum circuit size (gates, fan-in 2, basis B2 = all 16 binary gates,
free negation) for all Boolean functions on n<=3 inputs, plus minimum formula
leaves L(f).  Wires = 2*gates (gate in-edges); output wire not counted.
Run: python3 mincircuit.py   (finishes in a few seconds)."""
import itertools, json
def run(n, maxg=7):
    N = 1 << n; M = (1 << N) - 1
    ins = []
    for i in range(n):
        t = 0
        for x in range(N):
            if (x >> i) & 1: t |= 1 << x
        ins.append(t)
    # normalised binary ops (AND-type with negations, XOR); constants/projections useless
    def ops(a, b):
        na, nb = M ^ a, M ^ b
        r = {a & b, na & b, a & nb, na & nb}
        r |= {M ^ v for v in list(r)}
        r.add(a ^ b); r.add(M ^ (a ^ b))
        return r
    trivial = {0, M} | set(ins) | {M ^ t for t in ins}
    best = {}  # function -> min gates
    for t in trivial: best[t] = 0
    # iterative deepening over sets of computed functions (up to negation)
    def canon(t): return min(t, M ^ t)
    level = {frozenset(canon(t) for t in ins)}
    seen_best = {canon(t): 0 for t in trivial}
    for g in range(1, maxg + 1):
        nxt = set()
        for S in level:
            L = list(S) + [0]
            full = [x for s in S for x in (s, M ^ s)]
            for a, b in itertools.combinations(full, 2):
                for r in ops(a, b):
                    c = canon(r)
                    if c in S or c in trivial: continue
                    if c not in seen_best: seen_best[c] = g
                    nxt.add(S | {c})
        level = nxt
        print(n, g, len(level), len(seen_best), flush=True)
        if len(seen_best) == (1 << N) // 2: break
    return {t: seen_best[canon(t)] for t in range(M + 1)}, N
def formula_leaves(n):
    N = 1 << n; M = (1 << N) - 1
    F = {}
    for i in range(n):
        t = sum(1 << x for x in range(N) if (x >> i) & 1)
        F[t] = 1; F[M ^ t] = 1
    k = 1
    while len(F) < M + 1 - 2:  # constants excluded
        new = {}
        for k1 in range(1, k // 2 + 1):
            k2 = k - k1
            A = [a for a, v in F.items() if v == k1]; B = [b for b, v in F.items() if v == k2]
            for a in A:
                for b in B:
                    for r in (a & b, a | b, a ^ b, (M ^ a) & b, a & (M ^ b), M ^ (a ^ b), M ^ (a & b), M ^ (a | b), (M ^ a) | b, a | (M ^ b)):
                        if r not in F and r not in new and r not in (0, M): new[r] = k
        F.update(new); k += 1
        if k > 20: break
    return F
if __name__ == "__main__":
    out = {}
    for n in (1, 2, 3):
        C, N = run(n)
        Lf = formula_leaves(n)
        rows = {}
        for t, g in C.items():
            rows.setdefault(g, 0); rows[g] += 1
        out[n] = {"gate_histogram": rows, "max_gates": max(C.values()),
                  "max_leaves": max(Lf.values()),
                  "AND": C[int(''.join('1' if x == N-1 else '0' for x in reversed(range(N))), 2)] if False else None}
        # named functions
        def tt(f): return sum(1 << x for x in range(N) if f(x))
        pc = lambda x: bin(x).count('1')
        named = {"AND": lambda x: pc(x) == n, "OR": lambda x: pc(x) > 0, "XOR": lambda x: pc(x) % 2 == 1,
                 "MAJ": lambda x: 2 * pc(x) > n, "THR2": lambda x: pc(x) >= 2, "EXACT1": lambda x: pc(x) == 1}
        out[n]["named"] = {k: {"gates": C[tt(f)], "leaves": Lf.get(tt(f), 0 if tt(f) in (0, N) else None)} for k, f in named.items()}
        out[n].pop("AND")
    json.dump(out, open("mincircuit_results.json", "w"), indent=1)
    print(json.dumps(out, indent=1))
