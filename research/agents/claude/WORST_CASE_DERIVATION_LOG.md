# Living log — worst-case minimum derivation cost W̄_R(N)

Append-only. Newest entry on top. P versus NP remains **OPEN**.

## 2026-11-15 15:00 UTC — WRBRIDGE-0001
- Report: `research/agents/claude/2026-11-15_1500_CLAUDE_WRBRIDGE-0001.tex`
- **PROVED/EXACT (folklore):** Bridge(R) ⇔ (P=NP ⇒ R p-optimal).
- **PROVED/EXACT:** for any R with a known superpolynomial lower bound (Resolution, CP, AC0-Frege, PC, Res(k)), Bridge(R) ⇔ P≠NP. A resolution-type multisign hypergraph calculus gives no shortcut.
- **PROVED/EXACT:** for strong R, the lower-bound half implies NP≠coNP. The plan factors through NP≠coNP.
- **KNOWN THEOREM / CONDITIONAL:** Bridge(EF) holds for SAT deciders with a PV-provable soundness proof (Cook 1975; Krajíček–Pudlák). The weakest sufficient transfer theorem is "every P-time SAT decider is PV-provably sound" (OPEN).
- **COMPUTATIONAL:** exact minimum tree-resolution size against fixed-order DPLL. PHP m=1..3 gives 5/21/85 against 5/29/197; random 3-CNF with n≤10 shows gaps up to 9×. Data in `results/raw/claude_wr/`.
- Next: (1) determine whether the multisign DAG calculus includes extension (≥ EF); if it does not, it is resolution-strength and Cor. 1 applies. (2) Look for any P-time decider class whose soundness is PV-provable but which is not R-transcript-based.
