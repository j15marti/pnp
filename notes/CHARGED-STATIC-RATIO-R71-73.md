CHARGED-STATIC-RATIO-R71-73

Small computational test (one short chunk): exact static demand ratios for the charged UNSAT transport permutation family at r=71,72,73.

Formulas (from Charged_UNSAT_Transport.md):
n=8r-1, m=10r, w=⌈log2(8r)⌉
N=3n+2+2⌊log2(m+1)⌋+3m(w+1)+w
D=6(r-2)(w+1)-1
h=log2(r!)
ratio=Dh/(N²/8)

Results (w=10 throughout):
r=71: N=25161, D=4553, h≈338.603012, ratio=0.019481511961131
r=72: N=25515, D=4619, h≈344.772938, ratio=0.019569510968838
r=73: N=25869, D=4685, h≈350.962762, ratio=0.019656280448180

All remain far below the asymptotic static ceiling ~0.05333. Confirms static distinguishability alone cannot force superpolynomial demand under the stated encoding. DYNAMIC-COMPATIBILITY-OBLIGATION1 remains OPEN. P vs NP OPEN.

Date: 2026-11-23 ~20:17 PT
