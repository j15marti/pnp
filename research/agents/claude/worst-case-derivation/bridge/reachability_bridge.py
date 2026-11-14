#!/usr/bin/env python3
"""WCD-REACH-0001: exhaustive check of the reachability bridge lemma on toy SAT machines.

Model. Input = m slots, each holding a symbol: TOP or a clause of width <= 2 over n variables.
A machine queries one slot per step (the slot is a function of its configuration).
For a fixed UNSAT input F with run C_0..C_L and queried slots p_0..p_{L-1}:
  Q(C,t)   = slots queried before time t on SOME input that reaches (C,t)
  R_t      = Q(C_t,t) & {p_u : u >= t}                (the re-read set)
  I_t(x)   = exists F' reaching (C_t,t), every slot of F' satisfied by x, F' = F on R_t
Lemma:  I_0 = true,  I_L = false,  and
        I_t(x) and x |= F[q] for all q in ({p_t} | R_{t+1}) - R_t   implies   I_{t+1}(x).
The control replaces R_t by the empty set and counts failures of the step.
Pure Python, single stage, well under 30 s. JSON on stdout.
"""
import itertools, json, sys, time
T0 = time.time()

def symbols(n):
    syms = [None]                                   # TOP
    lits = [(v, s) for v in range(n) for s in (0, 1)]
    syms += [(l,) for l in lits]
    syms += [c for c in itertools.combinations(lits, 2) if c[0][0] != c[1][0]]
    return syms
def sat(sym, x): return sym is None or any(((x >> v) & 1) == s for v, s in sym)

# ---- machines: (init, query(cfg)->slot or None, step(cfg,sym)->cfg, rejects(cfg)) ----
def alive_after(alive, sym, n): return frozenset(x for x in alive if sat(sym, x))

def machine_A(n, m):                                # one pass, keeps the set of surviving assignments
    init = (0, frozenset(range(1 << n)))
    return (init, lambda c: c[0] if c[0] < m else None,
            lambda c, s: (c[0] + 1, alive_after(c[1], s, n)), lambda c: not c[1])

def machine_B(n, m):                                # pass 1: parity of non-TOP slots; pass 2: as A
    init = (0, 0, frozenset(range(1 << n)))
    def q(c): return c[0] % m if c[0] < 2 * m else None
    def st(c, s):
        i, par, al = c
        return (i + 1, par ^ (s is not None), al) if i < m else (i + 1, par, alive_after(al, s, n))
    return (init, q, st, lambda c: not c[2])

def machine_C(n, m):
    """pass 1 reads slots 0,1 and keeps only c = b(s0) xor b(s1), b = 'mentions variable 0 positively';
    pass 2 as A, recomputing b0,b1; a mismatch with c (impossible on real inputs) forces 'accept'."""
    b = lambda s: int(s is not None and (0, 1) in s)
    init = (0, 0, frozenset(range(1 << n)), 0)
    def q(c):
        i = c[0]
        if i < 2: return i
        return i - 2 if i < 2 + m else None
    def st(c, s):
        i, cc, al, d = c
        if i < 2: return (i + 1, cc ^ b(s), al, d)
        j = i - 2
        return (i + 1, cc, alive_after(al, s, n), d ^ (b(s) if j < 2 else 0))
    return (init, q, st, lambda c: (not c[2]) and c[1] == c[3])

def analyse(name, n, m, mk):
    syms = symbols(n); init, query, step, rejects = mk(n, m)
    X = range(1 << n)
    runs = {}; reach = {}; Q = {}
    for F in itertools.product(range(len(syms)), repeat=m):
        c = init; cfgs = [c]; ps = []
        while query(c) is not None:
            p = query(c); ps.append(p); c = step(c, syms[F[p]]); cfgs.append(c)
        runs[F] = (cfgs, ps)
        seen = set()
        for t, cf in enumerate(cfgs):
            reach.setdefault((t, cf), []).append(F); Q.setdefault((t, cf), set()).update(seen)
            if t < len(ps): seen.add(ps[t])
    satmask = {F: [all(sat(syms[s], x) for s in F) for x in X] for F in runs}
    # correctness on every input
    for F, (cfgs, ps) in runs.items():
        assert rejects(cfgs[-1]) == (not any(satmask[F])), (name, F)
    stats = {"n": n, "m": m, "inputs": len(runs), "unsat_inputs": 0, "steps_checked": 0,
             "max_reread_set": 0, "lemma_failures": 0, "control_R_empty_failures": 0, "max_time": 0}
    def I(F, t, cf, R, x):
        return any(satmask[G][x] and all(G[q] == F[q] for q in R) for G in reach[(t, cf)])
    for F, (cfgs, ps) in runs.items():
        if any(satmask[F]): continue
        stats["unsat_inputs"] += 1; L = len(ps); stats["max_time"] = max(stats["max_time"], L)
        Rs = [Q[(t, cfgs[t])] & set(ps[t:]) for t in range(L + 1)]
        stats["max_reread_set"] = max(stats["max_reread_set"], max(len(r) for r in Rs))
        for x in X:
            assert I(F, 0, cfgs[0], Rs[0], x) and not I(F, L, cfgs[L], Rs[L], x)
            for t in range(L):
                stats["steps_checked"] += 1
                need = ({ps[t]} | Rs[t + 1]) - Rs[t]
                if I(F, t, cfgs[t], Rs[t], x) and all(sat(syms[F[q]], x) for q in need):
                    if not I(F, t + 1, cfgs[t + 1], Rs[t + 1], x): stats["lemma_failures"] += 1
                if I(F, t, cfgs[t], set(), x) and sat(syms[F[ps[t]]], x):
                    if not I(F, t + 1, cfgs[t + 1], set(), x): stats["control_R_empty_failures"] += 1
    return stats

def main():
    out = {"id": "WCD-REACH-0001", "machines": {}}
    for name, mk in (("A_one_pass", machine_A), ("B_two_pass_parity", machine_B), ("C_lossy_summary_reread", machine_C)):
        out["machines"][name] = analyse(name, 2, 3, mk)
    out["machines"]["A_one_pass_n3"] = analyse("A3", 3, 2, machine_A)
    out["machines"]["C_lossy_summary_reread_n3"] = analyse("C3", 3, 2, machine_C)
    out["seconds"] = round(time.time() - T0, 2)
    json.dump(out, sys.stdout, indent=1, sort_keys=True); print()
if __name__ == "__main__": main()
