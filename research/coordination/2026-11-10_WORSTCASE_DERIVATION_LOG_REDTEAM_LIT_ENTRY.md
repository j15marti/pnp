# Worst-case minimum-derivation living log: red-team / literature entry, 2026-11-10

**Status: CANDIDATE/OPEN bookkeeping plus one KNOWN-THEOREM audit. No new lower bound. P versus NP OPEN.**
Governing directive: `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`. Latest peer handoff read: LSPV-3/547 (flat DAG, logspace checker); `proof2.txt` tail read through [P2-L3-549]. Not a full corpus preflight, and no tracker or `main.tex` edit was made.

## Audit: what the bridge "SAT in P implies W_R(N) <= poly(N)" can and cannot be
1. **Known-lower-bound systems (KNOWN THEOREM, Haken 1985 and successors).** For Resolution, W_R(N) is superpolynomial, so the bridge has a false conclusion. It then holds only if SAT is not in P, so it is equivalent to P != NP. It is a restatement of the goal, not a weaker sufficient bridge. The same applies to every system with a proven superpolynomial lower bound, including bounded-depth Frege. The bridge is informative only for systems with no known lower bound (Frege, Extended Frege, and the project's R_mix341).
2. **Strong systems (KNOWN THEOREM, Cook-Reckhow 1979).** W_EF(N) polynomial iff NP = coNP. SAT in P gives NP = coNP semantically, but the bridge needs a polynomial-size R-proof of each UNSAT instance. That needs R to prove the correctness of the polynomial algorithm, a reflection step (Krajicek-Pudlak line of work; recalled from background and not re-verified this run). This matches the project's existing B3 reflection firewall. The bridge for strong R therefore reduces to a provable-correctness hypothesis and is not derivable from SAT in P alone. Classification: **EXACT consequence of known results; no new transfer.**
3. **Free choice of derivation (user clarification).** Granting the optimal pi for free does not trivialise the bound. The min over pi is exactly proof size, which is what the Cook-Reckhow program lower-bounds, so the free-strategy convention is sound but adds nothing beyond classical proof complexity.

## Literature check this run (one standard search; two items fetched only as search snippets)
- Pich and Sokolov, CCC 2026: constructivity of lower bounds. Existing lower bounds, e.g. constant-depth Frege for PHP, yield efficient algorithms for the adversary's winning strategies. A constructive EF lower bound for succinct-circuit-lower-bound formulas is argued to meet a barrier if EF can prove the relevant properties. Relevance: a **useful structural analogy / barrier** for any W_R lower-bound proof that is itself formalisable in R. It needs a new transfer theorem for R_mix341. https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CCC.2026.8
- Davis and Robere, ECCC TR26-055 (2026): depth-d Frege upper bounds on Prf(PHP) implementable in Res(log). Relevance: **FAILED TRANSFER** for full Frege (self-proving only for bounded depth). https://eccc.weizmann.ac.il/report/2026/055
- Bokov, 2026 (Steklov): nontrivial length lower bound for a specific Frege system over {and, or, not}; scope not seen. Treat as **unverified lead**; do not cite as a Frege lower bound until read.
- Background: no superpolynomial Frege or EF lower bound is known. This was not independently re-verified beyond the search snippet.

## Red-team action items (suggestions only; no task changes)
- Before any claim about R_mix341, state whether the lower-bound argument is formalisable inside R_mix341 and test it against the Pich-Sokolov barrier.
- Classify any candidate hard family as lying in a system with a known lower bound (the bridge then equals the goal) or in a system without one (reflection hypothesis required).

Open load-bearing arrows unchanged: [P2-D1], [P2-C3], [P2-B1], [P2-B2], [P1-01], [P1-03], [P1-04]. P versus NP remains OPEN.
