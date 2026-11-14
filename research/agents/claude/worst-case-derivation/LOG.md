# Living log: worst-case minimum-derivation program (W̄_R)

Scheduled Claude routine. Target: superpolynomial lower bound on W̄_R(N) = max over UNSAT F with |F| ≤ N of the minimum cost of a refutation π: F ⊢_R ⊥, together with the bridge SAT ∈ P ⇒ W̄_R(N) ≤ poly(N). **P versus NP remains OPEN.** Newest entries at top.

## 2026-11-14: WCDERIV-0001
Report: `research/agents/claude/2026-11-14_CLAUDE_WCDERIV-0001.tex`

- **PROVED/EXACT (Thm 1).** If the lower bound (LB) is already a theorem for R (resolution, cutting planes, PC, AC0-Frege), then the bridge (BR) for R is *equivalent* to P≠NP. A multisign hypergraph calculus without extension variables therefore gives no reduction in difficulty.
- **PROVED/EXACT (Thm 2).** The fixed system R_T is EF plus T-proofs of clocked UNSAT-soundness, with the clock paid in the proof. If some polynomial-time SAT decider is T-provably UNSAT-sound, then W̄_{R_T} is polynomial. So BR(R_T) ⇐ PROV_T. This refines, without contradicting, the LSPV-1 Gödel trap: the bridge needs one provably sound decider, not all of them.
- **Dichotomy.** Weak R: LB known, BR ≡ P≠NP. Strong R_T: BR reduces to PROV_T, but LB lies beyond the EF frontier, where the best unrestricted Frege bounds are only quadratic.
- **COMPUTATIONAL.** Exact minimum tree-like resolution sizes: PHP m=1..3 give 5, 21, 85; odd Tseitin on K3..K5 gives 11, 55, 463. PHP leaf counts follow L_{m+1} = 4L_m − 1 for m ≤ 3 (finite observation only). PHP m=4 and Tseitin K6 exceeded the 30 s chunk limit.
- **Literature.** Cook–Reckhow 1979; Krajíček–Pudlák 1989; Haken 1985; Ben-Sasson–Wigderson 2001; Håstad 2025; Lu–Santhanam–Tzameret ECCC TR25-134; de Rezende et al. arXiv:2604.28172.
- **Next.** Test whether Thm 2 survives with T = S^1_2 or V^0, which would reduce BR(EF) to bounded-arithmetic provable soundness (Pich–Santhanam 2023 link).
