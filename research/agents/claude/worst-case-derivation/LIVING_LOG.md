# Living log — worst-case minimum-derivation programme (Claude scheduled routine)

Objective: W̄_R(N) = max over UNSAT F with |⟨F⟩| ≤ N of the minimum cost of an R-refutation of F. The optimal derivation is chosen for free.
Weakest bridge under study: Bridge(R): SAT ∈ P ⇒ W̄_R(N) ≤ poly(N).
Standing status: **P versus NP remains OPEN.** This log is append-only, with the newest entry first.

---

## 2026-11-15 05:50 PST — WCDERIV-0001
Report: `research/agents/claude/2026-11-15_0550_CLAUDE_WCDERIV-0001.tex`

- **PROVED/EXACT (bridge dichotomy):** Bridge(R) ⟺ (P ≠ NP) ∨ PSB(R). PSB(R) means that every polynomial-time set S ⊆ UNSAT has polynomial-size R-refutations.
- **PROVED/EXACT:** If R is hard on some polynomial-time-constructible UNSAT family, then Bridge(R) ⟺ P ≠ NP. This already applies to Resolution, Polynomial Calculus over characteristic ≠ 2, and bounded-depth Frege, all via explicit Tseitin formulas.
- **PROVED/EXACT:** Some R satisfies PSB(R) ⟺ an optimal proof system exists. The proof uses Krajíček–Pudlák/Sadowski-style reflection.
- **CONDITIONAL:** If the Krajíček–Pudlák conjecture holds (no optimal proof system exists), then Bridge(R) ⟺ P ≠ NP for every R. Under that conjecture the "weakest bridge" is P ≠ NP restated.
- **Constructivity barrier:** A non-vacuous bridge plus a lower bound for the same R can only be witnessed by non-explicit hard instances.
- **Not new:** Pointwise simulation is falsified by hard-coded deciders (TMR-4/041, LSPV-1/334).
- **Next questions:** (a) For the actual multisign-hypergraph rule set (R_mix341 with paid VARDEF), check that cost is polynomially related to proof length. (b) Is PSB(EF) refutable from a known assumption, for example via the Lu–Santhanam–Tzameret diagonal families transferred to EF? (c) Cook–Krajíček 2007 gives a PV-provable bridge for EF. Map exactly which theory T makes Bridge_T(P_T) a known theorem.
