CHARGED-STATIC-RATIO-R59-61

Small computational test (one short chunk): exact static demand ratios for the charged UNSAT transport permutation family at r=59,60,61.

Formulas (from Charged_UNSAT_Transport.md):
n=8r-1, m=10r, w=⌈log2(8r)⌉
N=3n+2+2⌊log2(m+1)⌋+3m(w+1)+w
D=6(r-2)(w+1)-1
h=log2(r!)
ratio=Dh/(N²/8)

Results:
r=59: N=19142, D=3419, h≈266.226, ratio=0.01987307153817772
r=60: N=19466, D=3479, h≈272.133, ratio=0.019988125882213735
r=61: N=19790, D=3539, h≈278.064, ratio=0.02010125662596293

All remain far below the asymptotic static ceiling ~0.05333. Confirms static distinguishability alone cannot force superpolynomial demand under the stated encoding. DYNAMIC-COMPATIBILITY-OBLIGATION1 remains OPEN. P vs NP OPEN.

Literature/GitHub search (2026-11-23): OpenAI math preprint claims deterministic 2^{o(n)} #k-SAT (refutes ETH); Anthropic formal-math has Lean formalization of similar claim. Neither closes SAT-LOCAL-ERROR1 or DYNAMIC-COMPATIBILITY-OBLIGATION1 in the charged single-tape model. Hartmanis crossing method remains the classical baseline for the quadratic barrier on separated equality. Recent ECCC reports (TR26-338 unshardable codes, TR26-330 threshold circuits, TR26-332 resolution on Tseitin) do not address single-tape charged cumulative memory for 3-SAT.

Date: 2026-11-23 ~16:24 PT
