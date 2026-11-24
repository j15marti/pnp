CHARGED-STATIC-RATIO-R62-64

Small computational test (one short chunk): exact static demand ratios for the charged UNSAT transport permutation family at r=62,63,64.

Formulas (from Charged_UNSAT_Transport.md):
n=8r-1, m=10r, w=⌈log2(8r)⌉
N=3n+2+2⌊log2(m+1)⌋+3m(w+1)+w
D=6(r-2)(w+1)-1
h=log2(r!)
ratio=Dh/(N²/8)

Results:
r=62: N=20114, D=3599, h≈284.018, ratio=0.020212526346698
r=63: N=20438, D=3659, h≈289.995, ratio=0.020321994636719
r=64: N=20762, D=3719, h≈295.995, ratio=0.020429718289369

All remain far below the asymptotic static ceiling ~0.05333. Confirms static distinguishability alone cannot force superpolynomial demand under the stated encoding. DYNAMIC-COMPATIBILITY-OBLIGATION1 remains OPEN. P vs NP OPEN.

Literature/GitHub search (2026-11-23): OpenAI math preprint claims deterministic 2^{o(n)} #k-SAT (refutes ETH); Anthropic formal-math has Lean formalization of similar claim. Neither closes SAT-LOCAL-ERROR1 or DYNAMIC-COMPATIBILITY-OBLIGATION1 in the charged single-tape model. Hartmanis crossing method remains the classical baseline for the quadratic barrier on separated equality. Recent ECCC reports do not address single-tape charged cumulative memory for 3-SAT. Google Research has no relevant crossing-sequence or charged CM SAT lower-bound work.

Date: 2026-11-23 ~17:28 PT
