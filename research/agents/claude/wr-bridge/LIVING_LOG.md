# Living log — shared worst-case W̄_R(N) directive (Claude routine)

Status: **P versus NP OPEN.** Both load-bearing arrows remain OPEN:
- LB(R): W̄_R superpolynomial, for an EF-like R.
- Bridge(R): SAT ∈ P ⇒ W̄_R ≤ poly.

## 2026-11-12 07:00 UTC — WR-BRIDGE-0001
- Report: `research/agents/claude/2026-11-12_0700_CLAUDE_WR-BRIDGE-0001.tex`
- PROVED/EXACT: Bridge(R) ⇔ (SAT∉P ∨ R p-bounded). So for Resolution, Cutting Planes, AC0-Frege, PC and NS the bridge *is* P≠NP, and the decomposition into lower bound plus bridge saves nothing.
- PROVED/EXACT (EF-like R): Bridge(R) ⇔ [SAT∈P ⇒ some polynomial-time decider A has polynomial-size R-proofs of its correctness tautologies Corr_A^n]. This sharpens LSPV-1/337 into a two-way propositional equivalence.
- KNOWN THEOREM, Cook–Krajíček 2007, new to the corpus: PV ⊢ P=NP iff PV defines a polynomial-time function that outputs a satisfying assignment or an EF refutation. An EF lower bound therefore gives only *consistency* of P≠NP with PV.
- Red team: granting the optimal sequence for free helps the lower bound only. The bridge's obstacle is verifying a decider's soundness, not searching for the proof.
- COMPUTATIONAL: exact minimum tree-like resolution refutations of PHP^{n+1}_n have 3, 11 and 43 leaves for n = 1, 2, 3 (`treelike_min.py`, `results.jsonl`).
- Next: decide whether R_mix341 (with VARDEF) p-simulates EF, then route it through the matching theorem.
