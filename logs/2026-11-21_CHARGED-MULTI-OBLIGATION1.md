# CHARGED-MULTI-OBLIGATION1 note

**Date:** 2026-11-21 ~20:25 PT

Toward DYNAMIC-COMPATIBILITY-OBLIGATION1.

Observation: packing k independent map-equality instances into one input does not allow a single cached equality bit to collapse the remaining obligations. After the first equality bit is known, each subsequent independent map still requires a full ~h-bit description (or an independent transport of its own left/right blocks) unless the solver has already stored the second map or its comparison result in a form that can be reused without re-crossing.

On the single-tape model, storing k independent results still costs space and, more importantly, any result that is not yet computed must be obtained by head motion that crosses the relevant cuts. The static ceiling continues to apply per separated block; the ratio Dh/(N²/8) at r=200 is 0.024060 and continues to approach ~0.0533.

Candidate next construction: an ordered sequence of residuals in which each new residual re-uses the same physical variables but under a fresh, solver-unknown affine shift or permutation that is revealed only after the previous residual is answered. This forces the decoder side-information B_j to be updated dynamically and may prevent a single early comparison from answering all later U_j.

No unrestricted lower bound claimed. P vs NP OPEN.
