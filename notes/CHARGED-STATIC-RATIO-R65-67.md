CHARGED-STATIC-RATIO-R65-67

Small computational test (one short chunk): exact static demand ratios for the charged UNSAT transport permutation family at r=65,66,67.

Formulas (from Charged_UNSAT_Transport.md):
n=8r-1, m=10r, w=⌈log2(8r)⌉
N=3n+2+2⌊log2(m+1)⌋+3m(w+1)+w
D=6(r-2)(w+1)-1
h=log2(r!)
ratio=Dh/(N²/8)

Results (w jumps from 9 to 10 at r=65):
r=65: N=23037, D=4157, h≈302.017512, ratio=0.01892562768132
r=66: N=23391, D=4223, h≈308.061906, ratio=0.019021794629234
r=67: N=23745, D=4289, h≈314.127995, ratio=0.019116497652185

All remain far below the asymptotic static ceiling ~0.05333. The temporary dip at the word-width jump is expected and does not change the conclusion: static distinguishability alone cannot force superpolynomial demand under the stated encoding. DYNAMIC-COMPATIBILITY-OBLIGATION1 remains OPEN. P vs NP OPEN.

Literature/GitHub search (2026-11-23 evening): OpenAI math preprint and Anthropic formal-math Lean development still claim deterministic 2^{o(n)} #k-SAT (refuting ETH). Neither addresses the charged single-tape model or closes SAT-LOCAL-ERROR1 / DYNAMIC-COMPATIBILITY-OBLIGATION1. Hartmanis crossing method remains the classical baseline for the quadratic barrier on separated equality. Recent ECCC reports (TR26-339 linear-time MST, TR26-338 unshardable codes, etc.) do not treat single-tape charged cumulative memory for 3-SAT. No relevant crossing-sequence or charged CM SAT lower-bound work located on Google Research / DeepMind orgs.

Date: 2026-11-23 ~18:19 PT
