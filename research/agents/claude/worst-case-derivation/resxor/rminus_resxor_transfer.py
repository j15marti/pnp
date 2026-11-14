#!/usr/bin/env python3
"""WCD-RESXOR-0001: exact checks for the R^- -> Res(+) linear simulation and the
lifted-Tseitin family used to transfer the Itsykson-Podolskii-Shekhovtsov
(ECCC TR26-018, Thm 1.6/7.4) quadratic Res(+) size bound to Wbar_{R^-}.

Pure Python + itertools, single stage, designed to finish in well under 30 s.
Every semantic check is by exhaustive truth table. Output: JSON on stdout.
"""
import itertools, json, sys, time

T0 = time.time()

# ---------- linear clauses over n variables, truth tables as int bitmasks ----------
def tt_eq(n, mask, b):
    """truth table (bit x set iff <mask,x> = b over GF(2))"""
    t = 0
    for x in range(1 << n):
        if (bin(x & mask).count("1") & 1) == b:
            t |= 1 << x
    return t

def tt_line(n, line):
    t = 0
    for (m, b) in line:
        t |= tt_eq(n, m, b)
    return t

def full(n):
    return (1 << (1 << n)) - 1

class Checker:
    """Bottom-up Res(+) with the TR26-018 rules: resolution C v (f=0), D v (f=1) |- C v D
    on a linear form f, and semantic weakening C |- D whenever C |= D."""
    def __init__(self, n, axioms):
        self.n = n; self.lines = [frozenset(a) for a in axioms]; self.ax = len(axioms); self.steps = 0
    def weaken(self, i, D):
        D = frozenset(D)
        assert tt_line(self.n, self.lines[i]) & ~tt_line(self.n, D) & full(self.n) == 0, "bad weakening"
        self.lines.append(D); self.steps += 1; return len(self.lines) - 1
    def resolve(self, i, j, f):
        A, B = self.lines[i], self.lines[j]
        assert (f, 0) in A and (f, 1) in B, "bad pivot"
        C = (A - {(f, 0)}) | (B - {(f, 1)})
        self.lines.append(frozenset(C)); self.steps += 1; return len(self.lines) - 1

def lit(v, val):  # literal "x_v = val" as linear equation
    return (1 << v, val)

# ---------- Lemma A: XOR rule in 2 Res(+) lines, exhaustive for n<=4 ----------
def check_xor(nmax=4):
    cnt = 0; worst = 0
    for n in range(1, nmax + 1):
        for f in range(1, 1 << n):
            for g in range(1, 1 << n):
                if f == g: continue
                for a in (0, 1):
                    for b in (0, 1):
                        c = Checker(n, [[(f, a)], [(g, b)]])
                        h = f ^ g
                        # weaken (g=b) to (f=a+1) v (f+g=a+b); resolve with (f=a) on f
                        D = [(f, a ^ 1), (h, a ^ b)]
                        i = c.weaken(1, D)
                        # orient pivot: premise with (f,0) first
                        if a == 0: k = c.resolve(0, i, f)
                        else:      k = c.resolve(i, 0, f)
                        assert c.lines[k] == frozenset({(h, a ^ b)}), (n, f, g, a, b)
                        worst = max(worst, c.steps); cnt += 1
    return {"instances": cnt, "max_lines_per_XOR_node": worst}

# ---------- Lemma B: local derivations on <=3 variables ----------
V3 = 3
def maxterms(n, ftt):
    """full-width maxterm CNF of Boolean function with truth table ftt"""
    cls = []
    for x in range(1 << n):
        if not (ftt >> x) & 1:
            cls.append([lit(v, 1 - ((x >> v) & 1)) for v in range(n)])  # falsified exactly at x
    return cls

def derive_target(n, S, target, target_vars):
    """Derive linear clause `target` (implied by CNF S) with a decision tree over
    variables not in target_vars; returns (ok, lines used)."""
    c = Checker(n, S)
    U = [v for v in range(n) if v not in target_vars]
    ttS = full(n)
    for C in S: ttS &= tt_line(n, C)
    ttT = tt_line(n, target)
    assert ttS & ~ttT & full(n) == 0
    def rec(rho):  # rho: dict v->val over prefix of U ; returns line index of target v not(rho)
        neg = [lit(v, 1 - val) for v, val in rho.items()]
        goal = list(target) + neg
        if len(rho) == len(U):
            # find premise implying goal (exists when target_vars cover all of target's vars, or tautology)
            gt = tt_line(n, goal)
            for idx in range(c.ax):
                if tt_line(n, c.lines[idx]) & ~gt & full(n) == 0:
                    if c.lines[idx] == frozenset(goal): return idx
                    return c.weaken(idx, goal)
            raise AssertionError("no premise")
        v = U[len(rho)]
        i0 = rec({**rho, v: 0}); i1 = rec({**rho, v: 1})
        # i0 contains (x_v = 1) [negation of x_v=0]; i1 contains (x_v=0)
        return c.resolve(i1, i0, 1 << v)
    k = rec({})
    ok = tt_line(n, c.lines[k]) == ttT and c.lines[k] == frozenset(target)
    return ok, c.steps

def check_local():
    n = V3; worst_clause = 0; worst_row = 0; cnt = 0
    for ftt in range(1 << (1 << n)):
        S = maxterms(n, ftt)
        if not S: continue          # f == True: nothing to derive
        if ftt == 0:                # f == False: empty clause derivable, counted below
            pass
        # every implied clause on <=3 vars
        for signs in itertools.product((None, 0, 1), repeat=n):
            T = [lit(v, s) for v, s in enumerate(signs) if s is not None]
            ttT = tt_line(n, T)
            if ftt & ~ttT & full(n): continue
            ok, st = derive_target(n, S, T, [v for v, s in enumerate(signs) if s is not None])
            assert ok; worst_clause = max(worst_clause, st); cnt += 1
        # every implied single GF(2) row (annotation / LOCAL-CONVERT to equation)
        for m in range(1, 1 << n):
            for b in (0, 1):
                ttR = tt_eq(n, m, b)
                if ftt & ~ttR & full(n): continue
                ok, st = derive_target(n, S, [(m, b)], [])
                assert ok; worst_row = max(worst_row, st); cnt += 1
    return {"derivations": cnt, "max_lines_implied_clause": worst_clause,
            "max_lines_implied_row": worst_row}

# ---------- gadget and lifted Tseitin ----------
def maj(bits): return 1 if sum(bits) >= 2 else 0

def check_stifling():
    # 1-stifling: for each a and each choice of l-1=2 variables there is an assignment to them fixing g=a
    for a in (0, 1):
        for free in range(3):
            fixed = [v for v in range(3) if v != free]
            ok = False
            for vals in itertools.product((0, 1), repeat=2):
                outs = set()
                for z in (0, 1):
                    x = [0] * 3
                    for v, val in zip(fixed, vals): x[v] = val
                    x[free] = z; outs.add(maj(x))
                if outs == {a}: ok = True
            if not ok: return False
    return True

def tseitin(edges, nv, charge):
    """clauses as lists of (edge_index, sign) ; sign 1 = positive literal"""
    inc = [[] for _ in range(nv)]
    for e, (u, w) in enumerate(edges): inc[u].append(e); inc[w].append(e)
    cls = []
    for v in range(nv):
        es = inc[v]
        for z in itertools.product((0, 1), repeat=len(es)):
            if (sum(z) & 1) != charge[v]:           # forbidden pattern z
                cls.append([(e, 1 - zi) for e, zi in zip(es, z)])
    return cls

def lift_maj3(cls):
    """y_e -> MAJ(x_{e,0..2}); literal y_e (sign1) -> CNF (a v b)(a v c)(b v c) on positive x;
    literal not y_e -> same on negative x. Clause of width k -> 3^k clauses of width 2k."""
    out = []
    for C in cls:
        parts = []
        for (e, s) in C:
            parts.append([[(3 * e + i, s), (3 * e + j, s)] for i, j in ((0, 1), (0, 2), (1, 2))])
        for combo in itertools.product(*parts):
            out.append([l for p in combo for l in p])
    return out

def sat_count(nvars, cls):
    # bit-parallel: for each clause compute falsifying assignment set via integer bitmasks
    N = 1 << nvars
    allm = (1 << N) - 1
    var_tt = []
    for v in range(nvars):
        t = 0; block = 1 << v
        pat = ((1 << block) - 1) << block      # bits where x_v = 1 within period 2*block
        period = block << 1
        rep = 0
        for k in range(0, N, period): rep |= pat << k
        var_tt.append(rep)
    sat = allm
    for C in cls:
        ct = 0
        for (v, s) in C: ct |= var_tt[v] if s == 1 else (allm ^ var_tt[v])
        sat &= ct
        if sat == 0: return 0
    return bin(sat).count("1")

def bisection_e(edges, nv):
    best = None
    for r in range(1, nv):
        if not (nv / 3 <= r <= 2 * nv / 3): continue
        for S in itertools.combinations(range(nv), r):
            Ss = set(S); cut = sum((u in Ss) != (w in Ss) for u, w in edges)
            best = cut if best is None else min(best, cut)
    return best

GRAPHS = {
    "K4": (4, [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]),
    "K33": (6, [(0,3),(0,4),(0,5),(1,3),(1,4),(1,5),(2,3),(2,4),(2,5)]),
    "prism": (6, [(0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(0,3),(1,4),(2,5)]),
    "cube": (8, [(0,1),(1,3),(3,2),(2,0),(4,5),(5,7),(7,6),(6,4),(0,4),(1,5),(2,6),(3,7)]),
    "Petersen": (10, [(0,1),(1,2),(2,3),(3,4),(4,0),(0,5),(1,6),(2,7),(3,8),(4,9),(5,7),(7,9),(9,6),(6,8),(8,5)]),
}

def main():
    out = {"id": "WCD-RESXOR-0001"}
    out["xor_simulation"] = check_xor()
    out["local_simulation"] = check_local()
    loc = out["local_simulation"]
    # per-node constant K: AND3 = <=8 maxterm weakenings + 1 row annotation; LOCAL-CONVERT <= 8 clauses
    K_and3 = 8 + loc["max_lines_implied_row"]
    K_lc = 8 * max(loc["max_lines_implied_clause"], loc["max_lines_implied_row"])
    out["K"] = {"RES": 1, "XOR": out["xor_simulation"]["max_lines_per_XOR_node"],
                "AND3": K_and3, "LOCAL_CONVERT_support3": K_lc,
                "K": max(1, 2, K_and3, K_lc)}
    out["MAJ3_1_stifling"] = check_stifling()
    fam = {}
    for name, (nv, E) in GRAPHS.items():
        odd = [1] + [0] * (nv - 1); even = [0] * nv
        base = tseitin(E, nv, odd); lifted = lift_maj3(base)
        rec = {"h": nv, "edges": len(E), "base_clauses": len(base), "lifted_clauses": len(lifted),
               "lifted_vars": 3 * len(E), "lifted_width": max(len(C) for C in lifted),
               "e_G_bisection": bisection_e(E, nv)}
        w = rec["e_G_bisection"]  # BSW: resolution width >= e(G) (KNOWN THEOREM)
        rec["IPS_size_LB_w(w+1)/2"] = w * (w + 1) // 2
        K = out["K"]["K"]
        rec["implied_Wbar_Rminus_LB"] = max(0, -(-(w * (w + 1) // 2 - len(lifted)) // K))
        if 3 * len(E) <= 18:
            rec["lifted_odd_models"] = sat_count(3 * len(E), lifted)
            rec["lifted_even_models_control"] = sat_count(3 * len(E), lift_maj3(tseitin(E, nv, even)))
            rec["base_odd_models"] = sat_count(len(E), base)
        fam[name] = rec
    out["families"] = fam
    # asymptotic crossover: |F'| = 108 h for cubic graphs; with e(G) >= c h the bound is positive once
    # c^2 h^2 / 2 > 108 h, i.e. h > 216 / c^2. Record for c = 0.1 (random cubic bisection ~0.101h).
    out["crossover_h_for_c_0.1"] = 216 / 0.01
    out["seconds"] = round(time.time() - T0, 2)
    json.dump(out, sys.stdout, indent=1, sort_keys=True); print()

if __name__ == "__main__":
    main()
