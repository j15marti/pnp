# Living log: worst-case minimum derivation cost W̄_R(N) and the bridge SAT∈P ⟹ W̄_R ≤ poly

Scheduled Claude routine. The newest entry is first. This log records the status of each run's work. **P versus NP remains OPEN.**

Shared target: W̄_R(N) = max over UNSAT F with |<F>| ≤ N of the minimum R-refutation cost. The minimum over derivation sequences is free: strategy discovery is not charged.

## Current status table

| Item | Status |
|---|---|
| B(R) ⟺ (SAT∈P ⟹ R p-bounded) ⟺ R simulates every clocked solver system Q_A | PROVED/EXACT (elementary), unreviewed |
| Complementarity: a proven W̄_R superpolynomial bound gives B(R) ⟺ P≠NP (Res, CP, PC, AC0-Frege) | PROVED/EXACT (elementary), unreviewed |
| Seesaw: R1 ≤_p R2 ⟹ (B(R1) ⟹ B(R2)) and (LB(R2) ⟹ LB(R1)) | PROVED/EXACT (elementary), unreviewed |
| B(EF) ⟺ [SAT∈P ⟹ ∃A with poly-size EF proofs of Corr_{A,n}] | KNOWN THEOREM; duplicates LSPV-1/361 and /336 (no priority claimed) |
| W̄_EF superpolynomial | OPEN (major open problem) |
| Feasible UNSAT-soundness premise under SAT∈P | OPEN |
| R_mix341 ≡_p EF: W_R ≤ W_E ≤ poly(M + W_R) | PROVED/EXACT (standard, sketch level), unreviewed; local lemmas COMPUTATIONAL |
| LB target = EF not p-bounded; bridge = (EF not p-bounded ⟹ P≠NP) | Both OPEN; bridge conditional in Pich–Santhanam (abstract only read) |
| Reproduce Pich–Santhanam bridge in project notation | DONE (paper §1.1.1 read; Thm 1/Cor 2 KNOWN THEOREM) |
| Localization: A correct ⟺ Loc_{A,n}; EF ⊢ Loc_{A,n} → Sound_{A,n} in poly size; B(EF) ⟺ [SAT∈P ⟹ ∃A, Loc_{A,n} poly EF-provable] | PROVED/EXACT (sketch), unreviewed, likely folklore |
| H_sound (witness-free, length-tolerant localized witnessing) ⟹ B(EF) | PROVED/EXACT (sketch), unreviewed |
| PS uniform witnessing (self-reduction search) ⟹ H_sound | PROVED (sketch), unreviewed; converse unknown |
| H_sound itself; OPEN lemma SR (self-referential false-UNSAT case) | OPEN, **next lemma** |

## Entries

### 2026-11-16, third pass (branch ccr-1695bd63-vp7fgl, base f9f4d90c)
- Report: `2026-11-16_LOCALIZED_WITNESSING_BRIDGE.md`; code `local_consistency_check.py` (v2), raw `local_consistency_check_raw.json`.
- Consolidation: this log and the earlier jady22 files were imported unchanged onto this branch. Earlier routine branches are not merged; files from ps9gxt (`wbar/`) and vw499c (`CONSOLIDATED_LIVING_LOG.md`) remain only on those branches.
- Literature: Pich–Santhanam arXiv 2312.08163 §1.1.1 read in full (Thm 1, Cor 1–2, Prop 1); ACKPS ICALP 2024 read at abstract level; GST 2007 and BTW 2010 checked via the PS references.
- Result: the bridge only needs short EF proofs of the *local* three-point consistency of the restriction hypergraph (Lemma 1). The PS witnessing hypothesis can drop the satisfying assignment and the exact-length requirement (Theorem 3, Lemma 4).
- Residual obstruction: deciders that wrongly answer UNSAT on their own error-existence formula Φ_n(A) (lemma SR).
- Finite check passed: 2880 perturbed deciders plus 24 adversarial path-hiding cases. The witness-free search needed up to 429 queries, against 3v+1 for the walk with a witness. Not reviewed; nothing asymptotic.
- Next: settle lemma SR, or give an oracle construction showing H_sound is not relativizingly provable.

### 2026-11-16, second pass (base 9ae84900)
- Report: `2026-11-16_RMIX341_EF_COLLAPSE.md`; code `xor_step_local_check.py`, raw `xor_step_local_check_raw.json`.
- Result: Extended Frege simulates every rule of the repo's fixed mixed calculus R_mix341 with polynomial overhead, so the calculus is polynomially equivalent to EF and to its RES+VARDEF fragment E.
- Consequence: a hard family for the mixed calculus must be hard for EF (PHP, Tseitin, clique–coloring are all easy); the bridge is exactly "EF not p-bounded ⟹ P≠NP".
- Corrections to the first report: its Theorem 3 duplicates LSPV-1/361; its Pich–Santhanam wording was wrong and is fixed in the new report.
- Finite check of the constant-size XOR-step lemmas passed (512 cases, plus 2000 random trials, seed 20261116). No proof object was machine-checked.
- Next: reproduce the Pich–Santhanam conditional bridge in project notation (paper body not yet read).

### 2026-11-16 (base 4cbb8b29)
- Report: `2026-11-16_WR_BRIDGE_REFLECTION_REDUCTION.md`.
- Result: the "weakest sufficient bridge" has no weaker form. It is exactly "SAT∈P ⟹ R polynomially bounded".
- For any system with a known lower bound, the bridge is equivalent to P≠NP.
- For EF, the bridge reduces to feasible proofs of the UNSAT-side correctness of one polynomial-time solver.
- Adding inference power (algebraic rules, circuit compression, shared DAGs, switching) weakens the bridge and hardens the lower bound monotonically.
- Literature checked: Cook 1975, Krajíček–Pudlák, Pudlák arXiv 2007.14835, Pich–Santhanam arXiv 2312.08163, Li ECCC 25-187, Lu–Santhanam–Tzameret ECCC 25-134, arXiv 2408.07408.
- No code was executed. Not independently reviewed.
- Next: define R_H and decide R_H ≤_p EF.
