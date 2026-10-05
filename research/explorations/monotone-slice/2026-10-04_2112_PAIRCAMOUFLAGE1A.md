# PAIR-CAMOUFLAGE1A

Date: 2026-10-04. Status: COMPUTATIONAL. P versus NP remains OPEN.

At exact density t=3.5q, all unordered clause pairs were classified by (s,h), where s is shared-variable count and h is opposite-sign count.

Fresh deterministic run, 4000 formulas per q:
q=20, seed 91020, UNSAT=82.
q=24, seed 91024, UNSAT=57.

Values below are (mean_UNSAT - mean_SAT)/sd_SAT.

| orbit | q=20 | q=24 |
|---|---:|---:|
| (0,0) | -0.320 | -0.284 |
| (1,0) | -0.507 | -0.615 |
| (1,1) | +0.783 | +0.880 |
| (2,0) | -0.552 | -0.470 |
| (2,1) | +0.766 | +0.544 |
| (2,2) | -0.065 | +0.232 |
| (3,1) | +0.296 | +0.066 |
| (3,2) | +0.033 | +0.048 |
| (3,3) | -0.058 | +0.168 |

COMPUTATIONAL interpretation only: the repeated finite-size direction is excess opposite-sign overlap, especially (1,1), with a deficit in same-sign (1,0). A weaker repeated effect occurs at (2,1) versus (2,0). This refines the scalar T signal from INTERMEDIATE1.

No asymptotic claim follows. By LOCALPATTERN-GUARD, fixed thresholds on these pair counts have polynomial-size monotone circuits, so a candidate lower-bound distribution must hide them.

Next target: PAIR-CAMOUFLAGE1B. Learn a complete pair-orbit typical window from an independent SAT training sample, condition both classes on that same window, evaluate held-out survivors, then test order-3 signed-overlap counts and multiple deletion orders for smaller MUFs.

Literature status remains: Hajiaghayi-Sorkin gives the rigorous 3.52 satisfiable lower bound; Scott-Sorkin leaves the intermediate rare-UNSAT regime open; Ahmadi et al. quiet planting is an analogy for low-order camouflage, not a monotone-circuit transfer theorem.

Controls retained: XOR-SLICE-EASY, LOCALPATTERN-GUARD, P/poly positive-family barrier, SLICELIFT2 local obstruction, and the withdrawn switching-lemma report remains RETIRED.
