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
