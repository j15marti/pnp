#!/usr/bin/env python3
"""WCD-DENSE-0001: a denser hard family for sequential-input machines, built on set disjointness.

Variables y[r][i], r in 0..2, i in 0..g-1 (three groups).  A fixed block C forces exactly one zero per group
(ladder encoding, all clauses padded to exactly three literals with fresh variables).  So the surviving
assignments are the N = g^3 triples t = (i, j, l).  The positive clause (y0_i v y1_j v y2_l) kills exactly triple t.
  F_{X,Z} = Left_X  C  P  Right_Z ,  Left_X = clauses of the triples in X,  Right_Z likewise,  P = padding.
Claim: F_{X,Z} is satisfiable iff X u Z != all triples.
Checks (g = 2, N = 8, |X| = |Z| = 4): all 70 x 70 = 4900 pairs by DPLL; one encoded length; the 70 pairs
(X, complement of X) form a fooling set.  Then sizes for growing g and the figure.
Single stage, pure Python.
"""
import itertools, json, math, os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))

class Vars:
    def __init__(self): self.n = 0
    def new(self): self.n += 1; return self.n

def pad3(cl, V):
    cl = list(cl)
    if len(cl) == 3: return [tuple(cl)]
    if len(cl) == 2: z = V.new(); return [tuple(cl + [z]), tuple(cl + [-z])]
    u, v = V.new(), V.new(); l = cl[0]
    return [(l, u, v), (l, u, -v), (l, -u, v), (l, -u, -v)]

def build(g, X, Z, pad_clauses):
    V = Vars()
    y = [[V.new() for _ in range(g)] for _ in range(3)]
    C = []
    for r in range(3):
        s = [V.new() for _ in range(g + 1)]
        raw = [(-s[0],), (s[g],)]
        for i in range(1, g + 1):
            yi = y[r][i - 1]
            raw += [(yi, s[i]), (-s[i - 1], s[i]), (yi, -s[i - 1]), (-s[i], s[i - 1], -yi)]
        for cl in raw: C += pad3(cl, V)
    pv = []
    while math.comb(len(pv), 3) < pad_clauses: pv.append(V.new())
    P = [t for _, t in zip(range(pad_clauses), itertools.combinations(pv, 3))]
    tri = lambda t: (y[0][t[0]], y[1][t[1]], y[2][t[2]])
    return [tri(t) for t in X], C, P, [tri(t) for t in Z], V.n

def encode_len(clauses, nvars):
    return len(clauses) * 3 * (1 + max(1, math.ceil(math.log2(nvars + 1))))

def dpll(clauses, assign=None):
    assign = dict(assign or {})
    changed = True
    while changed:
        changed = False
        for cl in clauses:
            if any(assign.get(abs(l)) == (l > 0) for l in cl): continue
            free = [l for l in cl if abs(l) not in assign]
            if not free: return False
            if len(set(free)) == 1: assign[abs(free[0])] = free[0] > 0; changed = True
    for cl in clauses:
        if not any(assign.get(abs(l)) == (l > 0) for l in cl):
            v = abs([l for l in cl if abs(l) not in assign][0])
            return dpll(clauses, {**assign, v: True}) or dpll(clauses, {**assign, v: False})
    return True

def main():
    g = 2; U = list(itertools.product(range(g), repeat=3)); N = len(U)
    halves = [frozenset(c) for c in itertools.combinations(U, N // 2)]
    bad = 0; lens = set(); nsat = 0
    for X in halves:
        for Z in halves:
            L_, C, P, R_, nv = build(g, sorted(X), sorted(Z), 4)
            F = L_ + C + P + R_; lens.add(encode_len(F, nv))
            sat = dpll(F); nsat += sat
            if sat != (len(X | Z) < N): bad += 1
    fool_ok = all((len(X | (frozenset(U) - Y)) == N) == (X == Y) or True for X in halves for Y in halves)
    cross = sum(1 for X in halves for Y in halves if X != Y and
                len(X | (frozenset(U) - Y)) == N and len(Y | (frozenset(U) - X)) == N)
    out = {"id": "WCD-DENSE-0001",
           "g2": {"N": N, "pairs": len(halves) ** 2, "wrong": bad, "satisfiable_pairs": nsat,
                  "distinct_lengths": len(lens), "fooling_set_size": len(halves),
                  "fooling_violations": cross, "log2_fooling": round(math.log2(len(halves)), 2)}}
    rows = []
    for g in (4, 8, 16, 32):
        N = g ** 3; X = list(itertools.islice(itertools.product(range(g), repeat=3), N // 2))
        L_, C, P, R_, nv = build(g, X, X, N)
        Lbits = encode_len(L_ + C + P + R_, nv); Pbits = encode_len(P, nv)
        rows.append({"g": g, "n": nv, "N": N, "L_bits": Lbits, "P_bits": Pbits,
                     "TS_lower_shape": Pbits * N, "ratio_TS_over_L2": round(Pbits * N / Lbits ** 2, 4),
                     "ratio_N_over_n": round(N / nv, 2)})
    out["growth"] = rows
    a, b = rows[0], rows[-1]
    out["fits"] = {"N_vs_n_exponent": round(math.log(b["N"] / a["N"]) / math.log(b["n"] / a["n"]), 3),
                   "TS_vs_n_exponent": round(math.log(b["TS_lower_shape"] / a["TS_lower_shape"]) / math.log(b["n"] / a["n"]), 3)}
    json.dump(out, open(os.path.join(HERE, "raw_results.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))

    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
    COL = {"eq1": "#eb6834", "eq3": "#eda100", "dj": "#2a78d6"}; NL = "#1baf7a"
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=SURF); ax.set_facecolor(SURF); ax.grid(color=GRID, lw=0.6)
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    def line(e, d, col, lab):
        t0 = max(e, d); ts = [t0 + i / 100 for i in range(0, int((e + d - t0) * 100) + 1)]
        ax.plot(ts, [e + d - t for t in ts], color=col, lw=2.2); ax.scatter([t0], [e + d - t0], color=col, s=40, zorder=5, edgecolor=SURF, linewidth=1.5)
        ax.text(t0 + 0.05, e + d - t0 + 0.06, lab, color=INK, fontsize=9, va="bottom")
    line(1, 1, COL["eq1"], "equality, m ≈ n\n(T·S ≥ n²)")
    line(1, 3, COL["eq3"], "equality, m ≈ n³  (T·S ≥ n⁴)")
    line(3, 3, COL["dj"], "disjointness, m ≈ n³  (T·S ≥ n⁶): linear time needs S ≈ n³ ≈ input length")
    ax.axhline(1, color=NL, lw=1.6, ls="--"); ax.text(6.4, 1.05, "S = n: one assignment", color=INK, fontsize=9, ha="right")
    ax.fill_between([3, 5], 1, [3, 1], color=COL["dj"], alpha=0.10, lw=0)
    ax.text(3.55, 1.35, "forced space\nexceeds one\nassignment", color=INK, fontsize=9, ha="center")
    ax.set_xlim(1, 6.5); ax.set_ylim(-0.05, 3.6)
    ax.set_xlabel("time exponent τ   (T = n^τ;  each line starts where reading the input is possible)")
    ax.set_ylabel("proved floor on space exponent σ   (S ≥ n^σ)")
    ax.set_title("Sequential-input 3-SAT: space floors in units of n, three families", loc="left", color=INK, fontsize=11)
    fig.text(0.01, 0.01, "Crossing-sequence bounds; logarithmic factors dropped. Sequential two-way input head only: no transfer to random access. "
             "P versus NP remains OPEN.", color=INK2, fontsize=8)
    fig.tight_layout(rect=(0, 0.035, 1, 1)); fig.savefig(os.path.join(HERE, "dense_floors.png"), dpi=200, facecolor=SURF)

if __name__ == "__main__": main()
