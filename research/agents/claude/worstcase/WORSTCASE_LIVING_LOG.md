# Living log: worst-case free-choice derivation cost W̄_R(N)

Status labels follow AGENTS.md. **P versus NP remains OPEN.**

## 2026-11-14 14:48 PST — WORSTCASE-BRIDGE-0001
- Report: `research/agents/claude/2026-11-14_1448_CLAUDE_WORSTCASE-BRIDGE-0001.tex`
- PROVED/EXACT: B(R) ⇔ (SAT∉P) ∨ (W̄_R poly). For any R that has a known superpolynomial lower bound (Res, CP, bounded-depth Frege), the bridge is equivalent to P≠NP. A non-vacuous bridge must compile an arbitrary SAT algorithm into R-proofs. This duplicates main.tex ≈4464 for Resolution.
- KNOWN routes (already in the corpus): Cook 1975 PV→EF (needs PV-provable soundness); Krajíček–Pudlák optimal systems (whether one exists is OPEN); REFEREE296 relativization barrier.
- PROVED/EXACT: MU ⇒ W_Res ≥ m−1. EXACT W_Res(PHP^3_2)=10. Brackets: Tseitin K4 [15,27], PHP^4_3 [21,41], Tseitin prism [23,47], Tseitin K33 [23,59].
- Red team: the Tseitin and PHP families fail the algebraic, CP and ER survival tests. Random O(log n)-CNF is the only family here that survives Res, PC and CP.
- Next: an MU-specific encoding with symmetry breaking (Peitl–Szeider) to close the Tseitin K4 bracket; audit Li 2025 (ECCC TR25-187) for the PV-unprovability obstacle to the EF bridge.
