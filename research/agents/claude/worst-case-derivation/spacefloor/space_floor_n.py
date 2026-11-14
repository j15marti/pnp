#!/usr/bin/env python3
"""WCD-SPACEFLOOR-0002: the space floors of WCD-SPACEFLOOR-0001 re-expressed in the number of variables n.

Density families. F^(d)_{a,b} = A_a  P^(d)  B_b, where P^(d) consists of m_P = k^d distinct all-positive 3-clauses
on p fresh variables (p minimal with C(p,3) >= k^d).  Then n = Theta(k), L = Theta(k^d log k) for d in {1,2,3},
and the ONETAPE crossing-sequence argument over the boundaries inside P^(d) gives T*S >= Omega(k * |P^(d)|).
Check 1 (exhaustive, k <= 3, d = 1..3): satisfiable iff a = b, one length per (k, d).
Check 2: n and L for growing k, fitted exponents.
Figure: panel A in L-units with the line S = n overlaid; panel B in n-units.
Single stage, a few seconds.
"""
import itertools, json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "onetape"))
from verify_family import build, encode, dpll
sys.dont_write_bytecode = True

def dense_family(k, d, a, b):
    A, P, B, nv = build(k, a, b)                 # P from the corpus is k clauses on 3k fresh vars; replace it
    base = nv - 3 * k                            # drop corpus padding variables
    mP = k ** d; p = 3
    while math.comb(p, 3) < mP: p += 1
    pads = list(range(base + 1, base + p + 1))
    P2 = [t for _, t in zip(range(mP), itertools.combinations(pads, 3))]
    return A, P2, B, base + p

def sizes(k, d):
    a = (0,) * k
    A, P, B, nv = dense_family(k, d, a, a)
    w = math.ceil(math.log2(nv + 1)) + 1
    return nv, (len(A) + len(P) + len(B)) * 3 * w, len(P) * 3 * w

def frontier_s(c, KS=range(2, 40)):
    return max(0.0, min(1.0, max((kk / c ** (kk - 1) - c) / (kk - 1) for kk in KS)))

def main():
    out = {"id": "WCD-SPACEFLOOR-0002", "exhaustive": {}, "growth": {}}
    for d in (1, 2, 3):
        for k in (1, 2, 3):
            lens, ok = set(), True
            for a in itertools.product((0, 1), repeat=k):
                for b in itertools.product((0, 1), repeat=k):
                    A, P, B, nv = dense_family(k, d, a, b)
                    lens.add(len(encode(A + P + B, nv)))
                    if dpll(A + P + B) != (a == b): ok = False
            out["exhaustive"][f"d{d}_k{k}"] = {"sat_iff_equal": ok, "distinct_lengths": len(lens)}
        rows = []
        for k in (16, 32, 64, 128):
            n, L, LP = sizes(k, d); rows.append((k, n, L, LP))
        fitn = math.log(rows[-1][1] / rows[0][1]) / math.log(rows[-1][0] / rows[0][0])
        fitL = math.log(rows[-1][2] / rows[0][2]) / math.log(rows[-1][1] / rows[0][1])
        out["growth"][f"d{d}"] = {"rows_k_n_L_LP": rows, "n_vs_k_exponent": round(fitn, 3), "L_vs_n_exponent": round(fitL, 3)}
    json.dump(out, open(os.path.join(HERE, "raw_results_n.json"), "w"), indent=1, sort_keys=True)
    print(json.dumps({k: v for k, v in out.items() if k != "growth"}, indent=1),
          {d: (g["n_vs_k_exponent"], g["L_vs_n_exponent"]) for d, g in out["growth"].items()})

    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
    SEQ, RAM, NLINE = "#eb6834", "#2a78d6", "#1baf7a"
    fig, axes = plt.subplots(1, 2, figsize=(15, 6), facecolor=SURF)
    for ax in axes:
        ax.set_facecolor(SURF); ax.grid(color=GRID, lw=0.6)
        for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    # Panel A: L-units
    ax = axes[0]; cs = [1 + i / 400 for i in range(0, 601)]
    for d, ls in ((1, "-"), (2, "--"), (3, ":")):
        ax.plot(cs, [max(0, 1 + 1 / d - c) for c in cs], color=SEQ, lw=2, ls=ls)
        ax.axhline(1 / d, color=NLINE, lw=1.6, ls=ls)
        ax.text(2.48, 1 / d + 0.015, f"S = n  (m ≈ n^{d})", color=INK, fontsize=8.5, ha="right", va="bottom")
        ax.text(1 + 1 / d + 0.01, 0.015, f"d={d}", color=INK2, fontsize=8.5)
    ax.plot(cs, [frontier_s(c) for c in cs], color=RAM, lw=2)
    ax.text(1.02, 1.82, "orange: sequential input, family with m ≈ n^d clauses:\n  S ≥ L^(1+1/d−c)   (solid d=1, dashed d=2, dotted d=3)\n"
            "blue: random access, any input of length L (FLMV regime has n ≈ L)\ngreen: S = n, enough to hold one assignment", color=INK, fontsize=8.5, va="top")
    ax.set_xlim(1, 2.5); ax.set_ylim(-0.03, 1.9)
    ax.set_xlabel("time exponent c   (T = L^c)"); ax.set_ylabel("space exponent s   (S = L^s)")
    ax.set_title("A. In input-length units, with S = n overlaid", loc="left", color=INK, fontsize=11)
    # Panel B: n-units, tau = time exponent in n
    ax = axes[1]; taus = [1 + i / 200 for i in range(0, 601)]
    for d, ls in ((1, "-"), (2, "--"), (3, ":")):
        xs = [t for t in taus if t >= d]
        ax.plot(xs, [max(0, d + 1 - t) for t in xs], color=SEQ, lw=2, ls=ls)
        ax.text(d + 0.03, 1.06 + 0.09 * (d - 1), f"m ≈ n^{d}: starts at τ = {d} (reading the input)", color=INK2, fontsize=8, va="bottom")
    ax.plot(taus, [frontier_s(t) for t in taus], color=RAM, lw=2)
    ax.axhline(1, color=NLINE, lw=1.6)
    ax.text(3.95, 0.95, "S = n: one assignment", color=INK, fontsize=8.5, ha="right", va="top")
    ax.text(2.05, 0.03, "below the lines: floor log n only, for every algorithm", color=INK2, fontsize=8.5)
    ax.set_xlim(1, 4); ax.set_ylim(-0.03, 1.45)
    ax.set_xlabel("time exponent τ   (T = n^τ, n = number of variables)"); ax.set_ylabel("space exponent σ   (S = n^σ)")
    ax.set_title("B. In variable units: no floor rises above S = n", loc="left", color=INK, fontsize=11)
    fig.text(0.01, 0.01, "Sequential floors: crossing sequences over the padding block (ONETAPE-0001 argument, padding densified here). "
             "Random-access floor: checkpoint scheme, sparse inputs. Logs dropped. P versus NP remains OPEN.", color=INK2, fontsize=8)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(os.path.join(HERE, "space_floor_n.png"), dpi=200, facecolor=SURF)

if __name__ == "__main__": main()
