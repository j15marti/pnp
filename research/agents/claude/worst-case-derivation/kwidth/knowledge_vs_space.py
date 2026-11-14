#!/usr/bin/env python3
"""WCD-KWIDTH-0001: a correct O(log)-space machine whose knowledge is wide.

Class. G = K4 (h = 4 vertices, 6 edges). Each edge e has 3 variables; y_e = MAJ3 of them.
Slot v holds TOP, or the lifted parity constraint "XOR of y_e over edges at v = c" for c in {0,1}.
Machine M0: one pass; state = (slots read, all present so far?, parity of charges). Rejects iff all
present and total charge odd. State space: 4 * 2 * 2 values.
Checks (all exhaustive, assignments as bitmasks over 2^18 points):
  1. M0 is correct on all 3^4 = 81 inputs.
  2. The reachability labelling I_{C,t} satisfies the bridge lemma on every UNSAT input.
  3. Fourier sparsity of the midway label, lifted and unlifted. Parity-decision depth d forces
     sparsity <= 4^d, so depth >= log4(sparsity).
Single stage, pure Python. JSON on stdout.
"""
import itertools, json, math, sys, time
T0 = time.time()
E = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]; H = 4

def build(lift):
    nv = 3 * len(E) if lift else len(E); N = 1 << nv; FULL = (1 << N) - 1
    def var_tt(v):
        block = 1 << v; pat = ((1 << block) - 1) << block; t = 0
        for k in range(0, N, block << 1): t |= pat << k
        return t
    X = [var_tt(v) for v in range(nv)]
    if lift:
        Y = [(X[3*e] & X[3*e+1]) | (X[3*e] & X[3*e+2]) | (X[3*e+1] & X[3*e+2]) for e in range(len(E))]
    else: Y = X
    par = []
    for v in range(H):
        t = 0
        for e, (a, b) in enumerate(E):
            if v in (a, b): t ^= Y[e]
        par.append(t)                       # truth table of XOR of y_e at v
    sym = lambda v, s: FULL if s == 2 else (par[v] if s == 1 else FULL ^ par[v])   # s: 0,1 charge; 2 TOP
    return nv, N, FULL, sym

def run(F):                                 # configs (t, allpresent, parity)
    c = (0, True, 0); out = [c]
    for v in range(H):
        s = F[v]; c = (v + 1, c[1] and s != 2, c[2] ^ (s if s != 2 else 0)); out.append(c)
    return out
rejects = lambda c: c[1] and c[2] == 1

def sparsity(tt, nv):
    N = 1 << nv
    a = [1 - 2 * ((tt >> i) & 1) for i in range(N)]
    h = 1
    while h < N:
        for i in range(0, N, h << 1):
            for j in range(i, i + h):
                u, w = a[j], a[j + h]; a[j], a[j + h] = u + w, u - w
        h <<= 1
    return sum(1 for z in a if z != 0)

def main():
    out = {"id": "WCD-KWIDTH-0001", "state_values": H * 2 * 2 + 4}
    for lift in (False, True):
        nv, N, FULL, sym = build(lift)
        inputs = list(itertools.product((0, 1, 2), repeat=H))
        satset = {}
        for F in inputs:
            t = FULL
            for v in range(H): t &= sym(v, F[v])
            satset[F] = t
        wrong = sum(1 for F in inputs if rejects(run(F)[-1]) != (satset[F] == 0))
        # strongest labelling: I[(C)] = OR over inputs reaching C of AND of the slots read so far
        I = {}
        for F in inputs:
            cfgs = run(F); acc = FULL
            for t in range(H + 1):
                I[cfgs[t]] = I.get(cfgs[t], 0) | acc
                if t < H: acc &= sym(t, F[t])
        fails = 0; steps = 0; unsat = 0
        for F in inputs:
            if satset[F]: continue
            unsat += 1; cfgs = run(F)
            assert I[cfgs[0]] == FULL and I[cfgs[H]] == 0
            for t in range(H):
                steps += 1
                if I[cfgs[t]] & sym(t, F[t]) & ~I[cfgs[t + 1]] & FULL: fails += 1
        Fodd = (1, 0, 0, 0); mid = I[run(Fodd)[2]]
        sp = sparsity(mid, nv)
        out["lifted" if lift else "unlifted"] = {
            "variables": nv, "inputs": len(inputs), "incorrect_inputs": wrong, "unsat_inputs": unsat,
            "lemma_steps": steps, "lemma_failures": fails, "midway_label_fourier_sparsity": sp,
            "parity_decision_depth_lower_bound": math.ceil(math.log(sp, 4))}
    out["seconds"] = round(time.time() - T0, 2)
    json.dump(out, sys.stdout, indent=1, sort_keys=True); print()
if __name__ == "__main__": main()
