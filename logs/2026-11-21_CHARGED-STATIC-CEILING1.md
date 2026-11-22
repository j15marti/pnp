# CHARGED-STATIC-CEILING1 note

**Date:** 2026-11-21 ~20:05 PT

Small computational check of the static separated-input ceiling from CHARGED-UNSAT-TRANSPORT1 Theorem 2 on the permutation family at r=6.

Parameters: n=47, m=60, w=6, N=1419, P=720, h=log2(P)≈9.49185, D=167.

Observed:
- Dh ≈ 1585.14 vs N²/8 ≈ 251695 → ratio 0.006298
- Dh² ≈ 15045.91 vs N³/27 ≈ 1.058e8 → ratio 0.000142

The family sits far below the static-method ceiling at this scale; the quadratic/cubic orders are attained only asymptotically as the relative block sizes approach the maximizing ratios. Confirms that static distinguishability alone cannot push past polynomial under the stated encoding.

P vs NP OPEN. DYNAMIC-COMPATIBILITY-OBLIGATION1 remains the active target.
