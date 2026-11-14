#!/usr/bin/env python3
"""WCD-SPACEFLOOR-0001: space lower bounds for a 3-SAT decider running in time T = L^c.

1. Re-checks the corpus equality family F_{a,b} = A_a P_k B_b (onetape/verify_family.py):
   SAT iff a = b, identical lengths for all a, b.  Exhaustive for k <= 4.
2. Single-cut table bound (two-way read-only input, any time): the 2^k left blocks A_a need
   distinct boundary tables, and there are at most (C+3)^(C+1) tables with C = q * g^S * (S+1)
   boundary configurations.  Prints the least S allowed for sample machine constants.
3. Figure: floor on the space exponent as a function of the time exponent c, in two models.
Single stage, a few seconds.
"""
import itertools, json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "onetape"))
from verify_family import build, encode, dpll

def check_family(kmax=4):
    out = {}
    for k in range(1, kmax + 1):
        lens, ok = set(), True
        for a in itertools.product((0, 1), repeat=k):
            for b in itertools.product((0, 1), repeat=k):
                A, P, B, nv = build(k, a, b)
                lens.add(len(encode(A + P + B, nv)))
                if dpll(A + P + B) != (a == b): ok = False
        out[k] = {"pairs": 4 ** k, "sat_iff_equal": ok, "distinct_lengths": len(lens), "L_bits": min(lens)}
    return out

def min_S(k, q, g):
    for S in range(1, 200):
        C = q * g ** S * (S + 1)
        if (C + 1) * math.log2(C + 3) >= k: return S
    return None

def frontier_s(c, KS=range(2, 40)):
    return max(0.0, min(1.0, max((k / c ** (k - 1) - c) / (k - 1) for k in KS)))

def main():
    out = {"id": "WCD-SPACEFLOOR-0001", "family": check_family()}
    rows = {}
    for k in (10, 10**2, 10**3, 10**4, 10**6, 10**9):
        L = k * 8 * 3 * (math.ceil(math.log2(7 * k)) + 1)        # A and B blocks dominate: 8k clauses x 3 literals
        rows[str(k)] = {"L_bits_approx": L, "log2_L": round(math.log2(L), 1),
                        "min_S_q16_g2": min_S(k, 16, 2), "min_S_q1000_g4": min_S(k, 1000, 4)}
    out["single_cut_min_space"] = rows
    out["seconds_note"] = "exhaustive part k<=4"
    json.dump(out, open(os.path.join(HERE, "raw_results.json"), "w"), indent=1, sort_keys=True)
    print(json.dumps(out, indent=1, sort_keys=True))

    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
    SEQ, RAM = "#eb6834", "#2a78d6"
    cs = [1 + i / 400 for i in range(0, 601)]
    fig, ax = plt.subplots(figsize=(9.5, 5.6), facecolor=SURF); ax.set_facecolor(SURF)
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    ax.plot(cs, [max(0, min(1, 2 - c)) for c in cs], color=SEQ, lw=2)
    ax.plot(cs, [frontier_s(c) for c in cs], color=RAM, lw=2)
    ax.plot([1.442, 2 * math.cos(math.pi / 7)], [0.012, 0.012], color=RAM, lw=4, solid_capstyle="round")
    ax.axhline(0, color=INK2, lw=1)
    ax.text(1.30, 0.80, "sequential input head:\nT·S ≥ L²/log L  ⇒  S ≥ L^(2−c)/log L", color=INK, fontsize=9.5)
    ax.text(1.03, 0.22, "random access:\ncheckpoint scheme", color=INK, fontsize=9.5)
    ax.text(1.45, 0.045, "Williams: S ≥ L^ε for some ε > 0, up to c ≈ 1.80 (ε not explicit)", color=INK2, fontsize=8.5)
    ax.text(2.05, 0.10, "c ≥ 2 (sequential), c ≥ 1.80 (random access):\nonly S ≥ (1 − o(1))·log L remains,\nfor every algorithm and every time bound", color=INK, fontsize=9)
    ax.set_xlim(1, 2.5); ax.set_ylim(-0.04, 1.05)
    ax.set_xlabel("time exponent c of the algorithm  (T = L^c, L = input length in bits)")
    ax.set_ylabel("proved floor on space exponent s  (S ≥ L^s)")
    ax.set_title("Space a 3-SAT algorithm must use, given its running time", loc="left", color=INK, fontsize=11)
    ax.grid(color=GRID, lw=0.6)
    fig.text(0.01, 0.01, "Orange: crossing-sequence bound (corpus ONETAPE-0001). Blue: checkpoint scheme (WCD-TWOWORLDS-0001).\n"
             "Log-space floor: single-cut table argument (WCD-SPACEFLOOR-0001). P versus NP remains OPEN.", color=INK2, fontsize=7.5)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(os.path.join(HERE, "space_floor.png"), dpi=200, facecolor=SURF)

if __name__ == "__main__": main()
