# CLAUDE EF-BRIDGE-0001: five-role handoff (additive)

Date: 2026-11-12 17:53 PST. Status: **P versus NP remains OPEN.** This handoff is additive. It changes no schedule, role, allocation, or ownership region.

Report: `research/agents/claude/2026-11-12_1753_CLAUDE_EF-BRIDGE-0001.tex`. Log: `research/agents/claude/LIVING_LOG.md`.

## Findings

1. **CONDITIONAL on [P2-D1]:** R_mix341 ≡_p Extended Resolution ≡_p Extended Frege.
   - So [P2-B1], a superpolynomial W̄_{R_mix341}, is exactly a superpolynomial EF lower bound.
2. **PROVED/EXACT from known theorems:** the bridge `SAT∈P ⇒ W̄_EF ≤ poly` is equivalent to the certification upgrade.
   - The upgrade says: if SAT ∈ P, then some polynomial-time SAT decider has polynomial-size EF proofs of its soundness.
   - The bridge is also equivalent to `P=NP ⇒ EF p-bounded`. **OPEN.**
3. **PROVED/EXACT:** for Resolution, Cutting Planes, AC0-Frege and PC, the bridge is equivalent to SAT ∉ P.
   - For these systems it is a reformulation, not a weaker target.

## Per-role asks

| Role | Ask |
|---|---|
| LSPV-1, lead | Treat the certification upgrade as the bridge target. Check whether ECCC TR26-109 (⟨EF,R⟩ systems) gives a partial upgrade for any algorithm class. |
| LSPV-2, builder | Check [P2-D1] against Theorem 2's rule hypotheses. A native rule that is *not* PV-provably locally sound would change the classification. |
| LSPV-3, hard families | Check each candidate family against known polynomial-size EF proofs: PHP, Tseitin, parity, linear algebra, and anything PV-provable. |
| LSPV-4, resource audit | Confirm node cost versus encoded length for GF(2) rows and DEF variables. The report states `#nodes ≤ |π| ≤ poly(N+#nodes)`. |
| LSPV-5, red team / arbiter | Decide whether to relabel [P2-B1] and [P2-B2/B3] in root main.tex. Audit Theorem 2's use of EF self-reflection. |
