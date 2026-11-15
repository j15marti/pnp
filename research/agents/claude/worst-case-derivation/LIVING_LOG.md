# Living log: worst-case minimum derivation cost (W̄_R) routine

Target: superpolynomial W̄_R(N) for a fixed R, plus the bridge B3: SAT∈P ⇒ W̄_R ≤ poly.
Shared directive: research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md.
**P versus NP remains OPEN.**

## 2026-11-15 — WR-BRIDGE-PINCER-0001
- Report: `2026-11-15_WR_BRIDGE_PINCER-0001.tex` (this folder).
- PROVED/EXACT (elementary): B3(R) ⇔ P≠NP ∨ R p-bounded. So **for every system with a known superpolynomial lower bound (Res, CP, PC, AC0-Frege, regular/depth-restricted Res(⊕)), B3 is equivalent to P≠NP**, and the bridge is no weaker than the goal.
- PROVED/EXACT: monotone pincer. Lower bounds move down the simulation order, B3 moves up. The route needs a system whose lower bound is currently unknown.
- PROVED/EXACT: under P=NP and polynomially related weights, p-bounded ⇔ p-optimal.
- With Krajíček–Pudlák (KNOWN THEOREM): B3(EF) ⇔ [P=NP ⇒ EF has short proofs of reflection for *some* fast SAT algorithm] ⇔ the same for *every* fast SAT algorithm. A B3 proof cannot rely on the structure of a special algorithm.
- Literature: unrestricted Res(⊕) lower bounds are still open (Efremenko–Itsykson 2025). Depth-restricted bounds: arXiv 2507.23008, arXiv 2511.20023, ECCC TR25-118, CCC 2026. ECCC TR26-109 covers reflection and implicit proof systems.
- Next: Res(⊕) or bit-weighted Rmix341 as the pincer point. Prove a lower bound for a family that is not explicitly generated, or show that B3 is unattainable there.
