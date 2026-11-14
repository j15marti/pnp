#!/usr/bin/env python3
"""WCD-ACCESS-0001: the disjointness family under three input-access models.

Family (WCD-DENSE-0001): Left_X  C  P  Right_Z, clause D_t kills triple t; SAT iff X u Z misses a triple.
Lists are in sorted triple order.  Units below are clause slots.
1. Two heads: a merge of the two sorted lists decides the family in one sweep with O(log N) bits.
   Checked against the truth on all 4900 pairs for g = 2.  => the one-head bound does not transfer.
2. One head, a move over distance D costs D^alpha (alpha = 1 sequential, 0 unit-cost random access).
   Lower bound shape: every Left<->Right traversal costs >= |P|^alpha and >= N/(S+log) traversals are needed.
   A concrete chunk strategy is simulated and its cost compared with that shape (tightness on the family).
3. Jump budget: J unit-cost jumps plus sequential moves; J + T/|P| >= N/(S+log).
Single stage, pure Python.
"""
import itertools, json, math, os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))

def two_head_merge(Xs, Zs, U):
    """heads i (Left), j (Right) only move forward; memory: the next expected triple index (log N bits)."""
    i = j = steps = 0
    for t in U:
        hit = False
        if i < len(Xs) and Xs[i] == t: i += 1; steps += 1; hit = True
        if j < len(Zs) and Zs[j] == t: j += 1; steps += 1; hit = True
        steps += 1
        if not hit: return True, steps            # triple t survives: satisfiable
    return False, steps

def chunk_strategy_cost(N, lenL, lenP, lenR, S, alpha):
    """Carry S bits per round trip. Lists sorted, so each chunk reads a contiguous run: total scan = lenL + lenR.
    Each round trip: jump Left->Right and back, distance >= lenP each way."""
    trips = math.ceil(N / S)
    return lenL + lenR + trips * 2 * (lenP ** alpha), trips

def main():
    out = {"id": "WCD-ACCESS-0001"}
    g = 2; U = list(itertools.product(range(g), repeat=3)); N = len(U)
    halves = [sorted(c) for c in itertools.combinations(U, N // 2)]
    wrong = 0; mx = 0
    for X in halves:
        for Z in halves:
            sat, st = two_head_merge(X, Z, U); mx = max(mx, st)
            if sat != (len(set(X) | set(Z)) < N): wrong += 1
    out["two_heads_g2"] = {"pairs": len(halves) ** 2, "wrong": wrong, "max_steps": mx, "list_slots": 2 * (N // 2) + N}
    rows = []
    for g in (8, 16, 32, 64):
        N = g ** 3; lenL = lenR = N // 2; lenP = N
        for alpha in (1.0, 0.5, 1 / 3, 0.0):
            for S in (int(math.log2(N)) * 2, g, g * g):
                Sp = S + math.ceil(math.log2(N))
                lower = (N / Sp) * (lenP ** alpha)
                cost, trips = chunk_strategy_cost(N, lenL, lenP, lenR, S, alpha)
                rows.append({"g": g, "N": N, "alpha": round(alpha, 3), "S": S, "lower_shape": round(lower),
                             "strategy_cost": round(cost), "ratio": round(cost / max(lower, lenL + lenR), 2)})
    out["distance_cost"] = rows
    out["max_ratio_strategy_over_max(lower,read)"] = max(r["ratio"] for r in rows)
    out["exponents"] = {str(round(a, 3)): {"TS_in_n": round(3 + 3 * a, 2), "TS_in_L": round(1 + a, 3),
                                           "S_gt_n_for_tau_below": round(2 + 3 * a, 2)} for a in (1, 0.5, 1 / 3, 0)}
    json.dump(out, open(os.path.join(HERE, "access_results.json"), "w"), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "distance_cost"}, indent=1))

    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
    COLS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]; NL = "#52514e"
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=SURF); ax.set_facecolor(SURF); ax.grid(color=GRID, lw=0.6)
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    labs = ["α = 1: sequential head  (T·S ≥ n⁶)", "α = 1/2: planar layout  (T·S ≥ n^4.5)",
            "α = 1/3: 3-D layout  (T·S ≥ n⁴)", "α = 0: unit-cost random access  (T·S ≥ n³, trivial)"]
    for a, col, lab in zip((1, 0.5, 1 / 3, 0), COLS, labs):
        top = 3 * a; ts = [3 + i / 100 for i in range(0, int(top * 100) + 1)] or [3]
        ax.plot(ts, [3 + 3 * a - t for t in ts], color=col, lw=2.2, label=lab)
        ax.scatter([3], [3 * a], color=col, s=42, zorder=5, edgecolor=SURF, linewidth=1.5)
    ax.axhline(1, color=NL, lw=1.2, ls="--"); ax.text(6.4, 1.04, "S = n: one assignment", color=INK, fontsize=9, ha="right")
    ax.text(3.08, 0.12, "two sequential heads:\nlinear time, log space\non this family", color=INK, fontsize=9)
    ax.set_xlim(2.9, 6.5); ax.set_ylim(-0.08, 3.4)
    ax.set_xlabel("time exponent τ   (T = n^τ;  τ = 3 is linear in the input)")
    ax.set_ylabel("proved floor on space exponent σ   (S ≥ n^σ)")
    ax.set_title("Disjointness family: space floor when moving the input head a distance D costs D^α", loc="left", color=INK, fontsize=10.5)
    ax.legend(loc="upper right", fontsize=8.5, frameon=False)
    fig.text(0.01, 0.01, "One input head. Logarithmic factors dropped. Dots mark linear time. P versus NP remains OPEN.", color=INK2, fontsize=8)
    fig.tight_layout(rect=(0, 0.035, 1, 1)); fig.savefig(os.path.join(HERE, "access_models.png"), dpi=200, facecolor=SURF)

if __name__ == "__main__": main()
