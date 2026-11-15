# Living log: worst-case minimum derivation cost W̄_R(N)

Append one entry per run, newest at the bottom. Status words follow AGENTS.md.
**P versus NP remains OPEN.**

## Current proof spine

```
(LB)  W̄_R(N) superpolynomial for fixed R        OPEN for R ⪰ EF; known for Res/PC/CP/AC0-Frege
(BR)  SAT∈P ⇒ W̄_R(N) ≤ poly(N)                    OPEN
      ├ for R with a known (LB): (BR) ⇔ P≠NP     PROVED/EXACT (reformulation)
      └ for R ⪰ EF:  (BR) ⇔ (CPA)                PROVED/EXACT
(CPA) every correct poly-time SAT decider A has
      poly-size R-proofs of Corr_{A,n}            OPEN  ← the load-bearing bridge
(LB) ∧ (BR) ⇒ P≠NP                               PROVED (trivial)
```

## Runs

### 2026-11-15 04:51 PST — WCDC-0001
- Report: `research/agents/claude/2026-11-15_0451_CLAUDE_WCDC-0001.tex`
- Directive record: `research/coordination/2026-11-15_0451_WORST_CASE_DERIVATION_COST_SHARED_DIRECTIVE.md`
- KNOWN THEOREM: W̄_R is the Cook–Reckhow length function. Choosing the derivation
  for free measures nondeterministic cost, so a bound for *every* R would be NP≠coNP.
- PROVED/EXACT: (BR) ⇔ P≠NP whenever R already has a superpolynomial lower bound. This
  is a reformulation, not a weaker bridge.
- PROVED/EXACT: for R ⪰ EF, (BR) ⇔ (CPA), the correctness-provability arrow. Encoding
  the algorithm's run as a trace is cheap. The soundness lemma "REJECT ⇒ UNSAT" is the
  whole difficulty.
- FALSIFIED/RETIRED: pointwise trace transfer into resolution-type multisign calculi
  (Tseitin plus GF(2) elimination). COMPUTATIONAL: exact minimum widths
  K4 = 4, K33 = 5, Q3 ≥ 5, Petersen ≥ 5, against 35–336 GF(2) bit-operations
  (`wcdc/tseitin_results.json`).
- CANDIDATE: random 3-CNF is the only standard family surviving the
  Res/PC/CP/Res(⊕) controls. Bounded-depth Frege has only a superlinear bound
  (arXiv 2403.02275). DAG Res(⊕) has no superpolynomial lower bound.
- Next: test (CPA) for R = Res and A = Gaussian elimination on Tseitin. Search for
  structure classes that force EF-short correctness proofs.
