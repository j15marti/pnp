# TASK-008: SLICEDELTA-FINITE1

P versus NP remains OPEN. No monotone-circuit lower bound.

## Why this test

SLICEDELTA0-R1 (HEAD 424032ab, 2026-10-05) transfers Hajiaghayi--Sorkin to the exact slice and proves only

\[
\delta_-(q):=\Pr_{U_{M,\lfloor 3.5q\rfloor}}[\mathrm{UNSAT}]=o(1).
\]

It explicitly claims no finite-q rate. The collision conditioning step uses \(\binom{t}{2}/M=O(1/q)\), which is not small on the q where an exact scan finishes. This run records that missing number.

Free polynomial-dimensional attention, random access, exact Gaussian elimination, exact 2-SAT, and polynomial-depth global attention do not select the residual incompatibility witness on this slice. The quantity that still has to scale is synchronization of the exact-layer negative mass with a non-mixture approximator. This test does not produce that witness.

## Literature check

ESA 2025 (LIPIcs.ESA.2025.103) still cites \(r_3\ge 3.52\) as the best known random-3-SAT lower bound. arXiv:2504.11979 (2025-04-16) restates the same 3.52 floor and only identifies degrees of freedom below 3.145. ECCC TR26-220 (2026-09-28) derandomizes robust sunflowers for local independence and separates non-monotone arithmetic circuits from the radical of monotone circuits; it does not give a SAT-slice approximator. No newer result closes the finite rate or SAT-SUNFLOWER2-DIRECTIONAL.

## Test

Uniform exact-\(t\) samples of distinct proper 3-clauses, \(t=\lfloor 3.5q\rfloor\), seed 20261005, exhaustive assignment scan. Collision bound is \(\binom{t}{2}/M\). Collision rate is an independent with-replacement sample of the same size.

| q | M | t | coll bound | N | UNSAT | delta_- | coll rate |
|---|---|---|------------|---|-------|---------|-----------|
| 8 | 448 | 28 | 0.843750 | 800 | 46 | 0.057500 | 0.570000 |
| 10 | 960 | 35 | 0.619792 | 400 | 18 | 0.045000 | 0.465000 |
| 12 | 1760 | 42 | 0.489205 | 200 | 12 | 0.060000 | 0.360000 |
| 14 | 2912 | 49 | 0.403846 | 120 | 3 | 0.025000 | 0.258333 |

Wall time 0.148+0.243+0.428+0.849 seconds.

## Box

\[
\boxed{\delta_-(14)=3/120=0.025,\qquad \binom{49}{2}/M=0.403846.}
\]

The finite UNSAT mass is already small at q=14, but the with-replacement collision bound used in the transfer is still 0.404, so the o(1) conditioning argument is not yet in force on this window. BUDGETMIX1 still forbids closing the directional sum inside any SAT/UNSAT mixture. SAT-SUNFLOWER2-DIRECTIONAL, growing-order moment camouflage, and MATCHED-MUF2 stay OPEN.

Raw: `results/raw/monotone_slice/SLICEDELTA_FINITE1.txt`.
