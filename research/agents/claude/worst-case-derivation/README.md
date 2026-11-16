# Claude worst-case derivation living log

Role-owned additive log for the user's shared directive on
`W̄_R(N) = max_{F UNSAT, |F|≤N} min_{π: F ⊢_R ⊥} cost_R(π)` and
`Bridge(R): SAT ∈ P ⇒ W̄_R(N) ≤ poly(N)`. Does not edit TMR manuscripts.
Living paper: `LIVING_WORST_CASE_DERIVATION.tex`. P versus NP remains OPEN.

## 2026-11-16 run

- PROVED/EXACT (elementary): the multisign DAG hypergraph reduction system is resolution; the minimal reduced state of every UNSAT F is {⊥}, so all information is in the work, and W̄_H = W̄_Res.
- KNOWN THEOREM: W̄_Res(N) ≥ 2^{Ω(N/log N)} on random 3-CNF.
- PROVED/EXACT (bridge collapse): for any R with a known superpolynomial lower bound, Bridge(R) ⇔ P ≠ NP. The decomposition gives no leverage for Res, Res(k), PC, bounded-depth Frege or regular Res(⊕).
- KNOWN/CONDITIONAL: Bridge holds for an optimal proof system, but there the lower bound ⇔ NP ≠ coNP. For EF, Bridge(EF) ⇐ premise U, "P=NP via a complete algorithm whose UNSAT-soundness PV can prove" (reflection: Cook 1975; Krajíček–Pudlák 1990).
- COMPUTATIONAL control: `treelike_vs_gf2.py` gives the exact minimum tree-like Res size against GF(2) row operations on small Tseitin/PHP instances. Raw output: `results/raw/2026-11-16_claude_treelike_vs_gf2.json`, 9.8 s, deterministic.
- Literature clues checked: ECCC TR26-109 (EF-provable FP reductions), arXiv:2609.23015 (Res(⊕) bit-PHP lower bound, not reviewed), ECCC TR25-096, arXiv:1703.02469.
- Validation not run: no LaTeX build (pdflatex not installed in this container), no independent review, no repo preflight.
- Next lemma: decide premise U (a separating model, or a proof).

## 2026-11-16 02:50 PST run (branch ccr-1695bd63-o6urne, merges run-1 branch ccr-1695bd63-7dks8r)

- Literature: Krajíček, "A note on SAT algorithms and proof complexity" (Theorem 2.1, class Alg(P)) — the lower bound on W̄_R reaches exactly the algorithms whose soundness R proves in poly size.
- PROVED/EXACT (immediate, unreviewed): for decent R, Bridge(R) ⇔ [P=NP ⇒ some complete poly-time decider is in Alg(R)] ⇔ [P=NP ⇒ every one is].
- PROVED/EXACT (unreviewed): premise U ⇔ Bridge(EF). This closes run 1's next lemma negatively for leverage: U is not a weaker target. Proof: under Bridge(EF) and P=NP, prefix-search for a p(n)-size EF refutation and accept only after the EF checker passes; PV proves its soundness through EF reflection, whatever subroutine is used.
- COMPUTATIONAL: `reflection_restriction_check.py` checks the D1/D4 restriction core of the clause-selector encoding exhaustively. 79,107 formulas and 700,568 assignments, 0 failures. Raw: `results/raw/2026-11-16_claude_reflection_restriction_check.json`. A harness bug (tautological slots) on the first execution is disclosed in the raw file.
- Not run: LaTeX build (no pdflatex), external review, repository preflight. Frege variant CONDITIONAL (VNC^1 reflection not checked).
- Next lemma: decide whether Bridge(Frege) ⇔ Bridge(EF).

## 2026-11-16 run 3 (branch ccr-1695bd63-bveg4t; merges o6urne and o1klgo lineages)

- PROVED/EXACT (elementary, unreviewed): Bridge(Frege) ⇔ Bridge(EF) ∧ Q, where Q = [P=NP ∧ EF p-bounded ⇒ Frege poly-proves Con_EF]. The proof uses Buss 1991.
- PROVED (sketch): the self-certifying A_Fr is in Alg(Frege) under Bridge(Frege).
- OPEN: Q. All known evidence that Frege does not simulate EF is cryptographic, and so is void under P=NP.
- RETIRED: SR(A) for the DPLL-style class (uninformative).
- Report: `2026-11-16_FREGE_EF_BRIDGE_GAP.md`. No code was executed this run.
- Next lemma: a non-cryptographic consequence of Q.
