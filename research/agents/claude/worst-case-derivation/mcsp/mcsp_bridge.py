#!/usr/bin/env python3
"""WCD-MCSP-0001: the bridge lemma on a toy minimum-formula-size problem.

Measure: De Morgan formula size = number of leaves (literals and constants cost 1; AND/OR binary).
EASY(k,s) = truth tables on k inputs with formula size <= s.  Problem: given an N = 2^k bit table, is it easy?
Checks:
  1. Bridge lemma, exact form. For a machine M and a hard table f, let
       A_t = { easy g : M on g is in the same configuration at time t as M on f }.
     Then A_0 = EASY, A_L = empty, and A_t & {g : g(p_t) = f(p_t)} is contained in A_{t+1}.
     Verified for a one-pass machine and for a two-pass machine that forgets and re-reads (k = 3).
  2. Certificate size: least number of table positions that separates a hard f from every easy g (k = 3).
  3. One-pass space: number of distinguishable prefixes at each cut (Myhill-Nerode classes), k = 3 and 4.
     Any one-pass machine needs at least log2 of that many states at that cut.
Single stage, pure Python, a few seconds. JSON on stdout.
"""
import itertools, json, math, sys, time
T0 = time.time()

def by_size(k, smax):
    N = 1 << k; full = (1 << N) - 1
    lits = set([0, full])
    for v in range(k):
        t = sum(1 << a for a in range(N) if (a >> v) & 1); lits |= {t, full ^ t}
    size = {t: 1 for t in lits}; layers = {1: set(lits)}
    for s in range(2, smax + 1):
        new = set()
        for i in range(1, s // 2 + 1):
            for a in layers[i]:
                for b in layers[s - i]:
                    for c in (a & b, a | b):
                        if c not in size: new.add(c)
        for c in new: size[c] = s
        layers[s] = new
    return size

def bit(f, p): return (f >> p) & 1

# ---- machines on N-bit tables: run(f) -> list of (config, queried position or None) ----
def run_onepass(f, N):
    cfgs = [(0, 0)]; ps = []
    for p in range(N): ps.append(p); cfgs.append((p + 1, f & ((1 << (p + 1)) - 1)))
    return cfgs, ps
def run_twopass(f, N):                      # pass 1 keeps only the number of ones; pass 2 stores the table
    cfgs = [("a", 0, 0)]; ps = []; cnt = 0
    for p in range(N): ps.append(p); cnt += bit(f, p); cfgs.append(("a", p + 1, cnt))
    acc = 0
    for p in range(N): ps.append(p); acc |= bit(f, p) << p; cfgs.append(("b", p + 1, cnt, acc))
    return cfgs, ps

def check_bridge(runf, N, easy, hard):
    runs_easy = {g: runf(g, N)[0] for g in easy}
    steps = fails = 0
    for f in hard:
        cfgs, ps = runf(f, N); L = len(ps)
        A = [frozenset(g for g in easy if runs_easy[g][t] == cfgs[t]) for t in range(L + 1)]
        assert len(A[0]) == len(easy) and len(A[L]) == 0
        for t in range(L):
            steps += 1
            if not all(g in A[t + 1] for g in A[t] if bit(g, ps[t]) == bit(f, ps[t])): fails += 1
    return {"hard_inputs": len(hard), "steps": steps, "failures": fails, "time": L}

def certificates(N, easy, hard):
    hist = {}
    masks = sorted(range(1, 1 << N), key=lambda m: bin(m).count("1"))
    proj = {}
    for m in masks: proj[m] = {g & m for g in easy}
    for f in hard:
        for m in masks:
            if (f & m) not in proj[m]:
                c = bin(m).count("1"); hist[c] = hist.get(c, 0) + 1; break
    return hist

def nerode(N, easyset):
    out = {}
    for t in range(0, N + 1):
        lowmask = (1 << t) - 1; res = {}
        for g in easyset: res.setdefault(g & lowmask, set()).add(g >> t)
        classes = {frozenset(v) for v in res.values()}
        n = len(classes) + (1 if len(res) < (1 << t) else 0)       # plus the dead class
        out[t] = n
    return out

def main():
    out = {"id": "WCD-MCSP-0001"}
    k, s = 3, 4; N = 1 << k
    size = by_size(k, 6)
    easy = sorted(t for t, v in size.items() if v <= s); hard = [f for f in range(1 << N) if f not in set(easy)]
    out["k3"] = {"threshold": s, "easy_tables": len(easy), "hard_tables": len(hard),
                 "bridge_one_pass": check_bridge(run_onepass, N, easy, hard),
                 "bridge_two_pass_forgetful": check_bridge(run_twopass, N, easy, hard),
                 "certificate_size_histogram": certificates(N, easy, hard),
                 "one_pass_classes_by_cut": nerode(N, set(easy))}
    k, s = 4, 5; N = 1 << k
    size4 = by_size(k, s); easy4 = set(size4)
    nd = nerode(N, easy4)
    out["k4"] = {"threshold": s, "easy_tables": len(easy4), "one_pass_classes_by_cut": nd,
                 "one_pass_space_lower_bound_bits": round(math.log2(max(nd.values())), 2), "table_bits": N}
    out["seconds"] = round(time.time() - T0, 2)
    json.dump(out, sys.stdout, indent=1, sort_keys=True); print()
if __name__ == "__main__": main()
