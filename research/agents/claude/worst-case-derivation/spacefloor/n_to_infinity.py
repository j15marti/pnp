#!/usr/bin/env python3
"""WCD-NLIMIT-0001: the proved impossible regions for 3-SAT as n grows, in actual resource sizes.

Sparse inputs (m ~ n clauses, L ~ n log2 n bits).  Constants in the lower bounds are not explicit in their
sources; they are set to 1 here, so the curves show shape, not certified numbers.
Panel A: log2 of time.  Panel B: space in bits.  Writes n_to_infinity.png and n_to_infinity.json.
"""
import json, math, os
HERE = os.path.dirname(os.path.abspath(__file__))

def frontier_s(c, KS=range(2, 40)):
    return max(0.0, min(1.0, max((k / c ** (k - 1) - c) / (k - 1) for k in KS)))

def main():
    ns = [10 ** (1 + i / 50) for i in range(0, 351)]          # 10 .. 10^8
    L = lambda n: n * math.log2(n)
    lg = math.log2
    A = {  # log2 of time
        "read the input: T >= L": [lg(L(n)) for n in ns],
        "sequential, S = log n: T >= L^2/(log L)^2": [2 * lg(L(n)) - 2 * lg(lg(L(n))) for n in ns],
        "random access, S = L^o(1): T >= L^1.80": [2 * math.cos(math.pi / 7) * lg(L(n)) for n in ns],
        "brute force (achievable): T = 2^n L": [n + lg(L(n)) for n in ns],
    }
    B = {  # space in bits
        "every algorithm: S >= log L": [lg(L(n)) for n in ns],
        "sequential, T = L^1.5: S >= L^0.5/log L": [L(n) ** 0.5 / lg(L(n)) for n in ns],
        "sequential, T = L^1.2: S >= L^0.8/log L": [L(n) ** 0.8 / lg(L(n)) for n in ns],
        "random access, T = L^1.2: S >= L^0.467": [L(n) ** frontier_s(1.2) for n in ns],
        "one assignment: S = n (brute force space)": [float(n) for n in ns],
    }
    marks = {}
    for n in (10 ** 2, 10 ** 4, 10 ** 6):
        marks[str(n)] = {"log2_T_min_read": round(lg(L(n)), 1), "log2_T_brute": round(n + lg(L(n)), 1),
                         "gap_factor_in_log2T_seq_vs_brute": round((n + lg(L(n))) / (2 * lg(L(n)) - 2 * lg(lg(L(n)))), 1),
                         "S_min_bits_any": round(lg(L(n)), 1), "S_seq_T1.5": round(L(n) ** 0.5 / lg(L(n)), 1)}
    json.dump({"id": "WCD-NLIMIT-0001", "checkpoints": marks}, open(os.path.join(HERE, "n_to_infinity.json"), "w"), indent=1)
    print(json.dumps(marks, indent=1))

    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
    COL = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]
    IMP = "#b9b8b2"
    fig, axes = plt.subplots(1, 2, figsize=(15, 6.2), facecolor=SURF)
    for ax in axes:
        ax.set_facecolor(SURF); ax.grid(color=GRID, lw=0.6, which="major")
        for sp in ("top", "right"): ax.spines[sp].set_visible(False)
        ax.set_xscale("log"); ax.set_yscale("log")
    ax = axes[0]
    keys = list(A)
    ax.fill_between(ns, 1, A[keys[0]], color=IMP, alpha=0.45, lw=0)
    for i, kname in enumerate(keys):
        ax.plot(ns, A[kname], color=COL[i], lw=2, label=kname)
    ax.fill_between(ns, A[keys[2]], A[keys[3]], color=COL[0], alpha=0.06, lw=0)
    ax.text(3e1, 2.2, "impossible for every algorithm", color=INK, fontsize=9)
    ax.text(3e5, 2.5e2, "OPEN gap:\nno algorithm known,\nnone ruled out", color=INK, fontsize=9, ha="center")
    ax.set_ylim(1, 2e8); ax.set_xlim(10, 1e8)
    ax.set_xlabel("number of variables n"); ax.set_ylabel("log2 of running time")
    ax.set_title("A. Time: what is ruled out as n → ∞", loc="left", color=INK, fontsize=11)
    ax.legend(loc="upper left", fontsize=8, frameon=False)
    ax = axes[1]
    keys = list(B)
    ax.fill_between(ns, 0.5, B[keys[0]], color=IMP, alpha=0.45, lw=0)
    for i, kname in enumerate(keys):
        ax.plot(ns, B[kname], color=COL[i], lw=2, label=kname, ls="--" if i == 4 else "-")
    ax.text(3e1, 1.0, "impossible for every algorithm", color=INK, fontsize=9)
    ax.set_ylim(0.5, 5e9); ax.set_xlim(10, 1e8)
    ax.set_xlabel("number of variables n"); ax.set_ylabel("space in bits")
    ax.set_title("B. Space: what each time budget forces as n → ∞", loc="left", color=INK, fontsize=11)
    ax.legend(loc="upper left", fontsize=8, frameon=False)
    fig.text(0.01, 0.01, "Sparse 3-CNF, L = n·log2 n bits. Lower-bound constants are not explicit in their sources and are set to 1: shapes, not certified values. "
             "Each colored bound rules out the region below it, for its own time or space budget. P versus NP remains OPEN.", color=INK2, fontsize=8)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(os.path.join(HERE, "n_to_infinity.png"), dpi=200, facecolor=SURF)

if __name__ == "__main__": main()
