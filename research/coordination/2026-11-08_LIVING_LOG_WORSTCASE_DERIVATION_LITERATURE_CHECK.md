# Living log | worst-case minimum derivation cost | literature check, 2026-11-08

**Status: bookkeeping and literature check only. No new theorem. P versus NP OPEN. [P2-B2] (B3 bridge) and [P2-D1] remain OPEN.**

## Corpus reviewed
Directive `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`; 2026-11-08 handoffs of LSPV-1/500, LSPV-3/496, LSPV-5/430; the existing quantifier-firewall entries on B3.

## Duplication audit
The observation "B3 is vacuous if P != NP, and given a proved superpolynomial lower bound on Wbar_R, B3 is logically equivalent to SAT not in P" is already in the corpus (LSPV-5/409 and earlier firewall entries). It is NOT re-claimed here. Consequence stands: B3 may only be used if proved noncircularly by a rule-specific translation or invariant, not by appeal to P != NP.

## Literature clues (standard search; no extended search run)
- Cook-Reckhow: NP = coNP iff some proof system is polynomially bounded. P = NP therefore gives SOME bounded system, not the preselected R. Frege systems are all polynomially equivalent (Reckhow), so B3 for Frege/EF is a single statement; no source found proving it. Clue: B3 for a fixed R amounts to an R-simulation of the identity system Q_A (already LSPV-5/409), which connects to optimal-proof-system questions of Krajicek-Pudlak. Nothing found that discharges it.
- Alekseev, Theory of Computing 22 (2026), https://theoryofcomputing.org/articles/v022a004/ : exponential lower bound for polynomial calculus with a square-root rule (binary value principle), also Res-Lin. Relevant as a hardness source for algebraic-plus-resolution mixtures; whether it transfers to R_mix341 is untested (CANDIDATE, needs same-source compiler audit).
- Gryaznov, arXiv 2403.02275: random 3-CNF vs bounded-depth Frege, superpolynomial bounds still open.
- arXiv 2405.02232: if iEF is not polynomially bounded then #P not in FP/poly (conditional; different system).
- No 2026 result found giving random-3-CNF lower bounds for Res(PC) beyond the Pang preprint already used, nor any extended Frege lower bound.

## Suggested next obligations (unchanged allocation)
1. LSPV-1/3: test whether the Alekseev square-root-rule bound survives inside R_mix341 or only in restricted calculi (classify as FAMILY-FAILURE-safe or not).
2. LSPV-5: keep B3 explicitly labelled OPEN and load-bearing.

END_OF_LOG_ENTRY
