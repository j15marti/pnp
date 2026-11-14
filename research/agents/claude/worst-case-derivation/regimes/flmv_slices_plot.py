#!/usr/bin/env python3
"""WCD-REGIMES-0001 figure: the FLMV-type excluded region for SAT in DTISP[L^c, L^s].

The frontier drawn is the k-level checkpoint scheme re-derived in WCD-TWOWORLDS-0001:
excluded iff c^(k-1) (c + (k-1) s) < k for some k >= 2.  Marked separately, not derived here:
Williams' endpoint 2cos(pi/7) at s = o(1), and the corpus FLMV box (governance ALL_ARC_REFOCUS3).
Panel A: the (s, c) plane.  Panel B: S held fixed, T sent from 0 to infinity.
Panel C: T held fixed, S sent from 0 to infinity.  Output: regimes/flmv_slices.png.
"""
import math, os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
EXCL, BOX, IMP = "#2a78d6", "#eb6834", "#b9b8b2"
KS = range(2, 40)

def cmax(s):
    best = 1.0
    for k in KS:
        lo, hi = 1.0, 3.0
        for _ in range(60):
            mid = (lo + hi) / 2
            if mid ** (k - 1) * (mid + (k - 1) * s) < k: lo = mid
            else: hi = mid
        best = max(best, lo)
    return best

def smax(c):
    return max(0.0, max((k / c ** (k - 1) - c) / (k - 1) for k in KS))

WILL, CBOX, SBOX = 2 * math.cos(math.pi / 7), 241 / 200, 11642479 / 23232400
CTOP, STOP = 2.4, 1.5

plt.rcParams.update({"font.size": 10, "text.color": INK, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.edgecolor": GRID})
fig, axes = plt.subplots(1, 3, figsize=(16, 5.6), facecolor=SURF)
for ax in axes:
    ax.set_facecolor(SURF)
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)

# ---------- Panel A: plane ----------
ax = axes[0]
ss = [i / 400 for i in range(0, 401)]
cs = [cmax(s) for s in ss]
ax.fill_between([0, STOP], 0, 1, color=IMP, alpha=0.45, lw=0)
ax.fill_between(ss, 1, cs, color=EXCL, alpha=0.35, lw=0)
ax.plot(ss, cs, color=EXCL, lw=2)
ax.plot([0, 0], [cmax(0), WILL], color=EXCL, lw=4, solid_capstyle="round")
ax.scatter([0], [WILL], s=60, color=EXCL, zorder=5, edgecolor=SURF, linewidth=2)
ax.add_patch(Rectangle((0, 1), SBOX, CBOX - 1, fill=False, ec=BOX, lw=2, ls="--"))
ax.text(0.75, 0.5, "impossible: time below L\ncannot read the input", ha="center", va="center", color=INK)
ax.annotate("excluded\n(checkpoint scheme)", xy=(0.15, 1.30), xytext=(0.62, 1.62), color=INK, fontsize=9,
            arrowprops=dict(arrowstyle="->", color=INK2))
ax.text(0.04, WILL + 0.04, "Williams 2cos(π/7) ≈ 1.80\n(space L^o(1) only)", va="bottom", color=INK, fontsize=9)
ax.text(0.62, 1.10, "dashed: corpus FLMV box (241/200, 0.5011);\nits corner sits above this curve\nand rests on sharper arguments", color=INK, fontsize=8.5, va="bottom")
ax.text(0.95, 1.85, "OPEN\nno lower bound known", ha="center", color=INK2)
ax.axvline(1, color=INK2, lw=1, ls=":")
ax.text(1.01, 0.08, "s = 1: space ≈ input,\nnothing excluded", color=INK2, fontsize=8.5)
ax.set_xlim(0, STOP); ax.set_ylim(0, CTOP)
ax.set_xlabel("space exponent s   (S = L^s;  s → 0 means space L^o(1))")
ax.set_ylabel("time exponent c   (T = L^c)")
ax.set_title("A. Where SAT ∈ DTISP[L^c, L^s] is ruled out", loc="left", color=INK, fontsize=11)
ax.annotate("", xy=(1.42, CTOP), xytext=(1.42, CTOP - 0.25),
            arrowprops=dict(arrowstyle="->", color=INK2))
ax.text(1.40, CTOP - 0.05, "c → ∞:\nbrute force\n2^n·poly(L)\nalways works", ha="right", va="top", color=INK2, fontsize=8)
ax.grid(color=GRID, lw=0.6)

# ---------- Panel B: S fixed, T from 0 to infinity ----------
ax = axes[1]
S_FIX = [0.0, 0.25, 0.5, 0.75, 1.0]
for i, s in enumerate(S_FIX):
    y = len(S_FIX) - 1 - i; cm = cmax(s)
    ax.barh(y, 1, left=0, height=0.55, color=IMP, alpha=0.6, lw=0)
    if cm > 1: ax.barh(y, cm - 1, left=1, height=0.55, color=EXCL, alpha=0.75, lw=0)
    ax.barh(y, CTOP - cm, left=cm, height=0.55, color=SURF, ec=GRID, lw=1)
    ax.text(cm + 0.03, y, f"open above c = {cm:.3f}" if cm > 1.0005 else "open above c = 1", va="center", color=INK, fontsize=9)
    if s == 0:
        ax.plot([cm, WILL], [y + 0.36, y + 0.36], color=EXCL, lw=2)
        ax.text(WILL + 0.03, y + 0.36, "Williams to 1.80", va="center", color=INK2, fontsize=8)
ax.set_yticks(range(len(S_FIX))); ax.set_yticklabels([f"s = {s}" for s in reversed(S_FIX)])
ax.set_xlim(0, CTOP); ax.set_xlabel("time exponent c, from → 0 to → ∞")
ax.set_title("B. Space held fixed, time swept", loc="left", color=INK, fontsize=11)
ax.text(0.5, -0.95, "gray: impossible (c < 1)   blue: excluded   white: open", ha="left", color=INK2, fontsize=8.5)
ax.set_ylim(-1.2, len(S_FIX) - 0.3)

# ---------- Panel C: T fixed, S from 0 to infinity ----------
ax = axes[2]
C_FIX = [1.05, 1.1, 1.2, 1.3, 1.44, 1.8]
for i, c in enumerate(C_FIX):
    y = len(C_FIX) - 1 - i; sm = min(1.0, smax(c))
    if sm > 0: ax.barh(y, sm, left=0, height=0.55, color=EXCL, alpha=0.75, lw=0)
    ax.barh(y, STOP - sm, left=sm, height=0.55, color=SURF, ec=GRID, lw=1)
    ax.text(sm + 0.03, y, f"excluded below s = {sm:.3f}" if sm > 0 else "nothing excluded by this scheme", va="center", color=INK, fontsize=9)
ax.set_yticks(range(len(C_FIX))); ax.set_yticklabels([f"c = {c}" for c in reversed(C_FIX)])
ax.set_xlim(0, STOP); ax.set_xlabel("space exponent s, from → 0 to → ∞")
ax.set_title("C. Time held fixed, space swept", loc="left", color=INK, fontsize=11)
ax.text(0.0, -0.95, "c = 1.8 row: Williams excludes it only at s = o(1), a single point", color=INK2, fontsize=8.5)
ax.set_ylim(-1.2, len(C_FIX) - 0.3)

fig.text(0.01, 0.005, "Frontier: k-level checkpoint scheme (WCD-TWOWORLDS-0001). Williams endpoint and corpus box are cited, not derived. "
         "L = input length. P versus NP remains OPEN.", color=INK2, fontsize=8.5)
fig.tight_layout(rect=(0, 0.03, 1, 1))
out = os.path.join(HERE, "flmv_slices.png")
fig.savefig(out, dpi=200, facecolor=SURF)
print(out, {s: round(cmax(s), 4) for s in S_FIX}, {c: round(min(1, smax(c)), 4) for c in C_FIX})
