# CLAUDE WORSTCASE-0001 — logical form of the B3 bridge, PV/EF known transfer, exact small minima
2026-11-10. Scheduled five-role worst-case run (Wbar_R). **P versus NP remains OPEN.** Nothing below is a lower bound against SAT algorithms.

## CORPUS REVIEWED
AGENTS.md; GROKPROOF/README + 2026-11-10_1523 progress note; research/coordination/2026-11-02_1204 worst-case refocus (B1/B2/B3 definitions); LSPV-1/395 handoff (noncomputable profile of a pathological calculus); grep of research/ for PV/provable-correctness material (several LSPV-1 reports touch it: 334, 406, 413, 415, 416, 454, 489/490 — not re-read in full this run).
Duplication audit: Lemma 1 below may already be implicit in LSPV-1/334 (free-choice transfer barrier) and /406 (feasible anti-checker B3); I did not verify that. Treat as a restatement, not a new theorem.

## Lemma 1 (logical form of B3) — PROVED/EXACT (elementary logic)
Fix R. B3 is the sentence "SAT∈P ⇒ ∃C,k ∀N Wbar_R(N) ≤ C(N+1)^k".
(a) If Wbar_R is superpolynomial (true for R = ordinary resolution, Haken 1985), B3 is *logically equivalent* to P≠NP (SAT∈P is then the only way the consequent could be reached, and the consequent is false).
(b) Hence for any R whose superpolynomial lower bound is already known, "proving B3" is exactly as hard as P≠NP. For a not-yet-resolved R, a proof of B3 is useful only if its proof **uses the hypothesis SAT∈P through an explicit mechanism** (an algorithm A with polynomial bound, converted into R-derivations); an argument that passes through "R is superpolynomial" or "P≠NP" is circular.
Consequence for the program: the pair (superpolynomial Wbar_R, B3) gives P≠NP only if B3 is established by a translation A ↦ R-proofs. That translation is exactly B2/B1 (pointwise or worst-case), so B3 has no cheap independent proof; it is the *consequence* of a simulation theorem, not a substitute for one.

## Known transfer (KNOWN THEOREM, cited from memory — verify exact statements before reuse)
Cook–Reckhow: a p-bounded proof system for UNSAT exists iff NP=coNP; SAT∈P implies NP=coNP so SOME bounded system exists, but this does not identify the preselected R.
Cook's PV translation / Krajíček–Pudlák: if a polynomial-time algorithm A for SAT has its correctness provable in PV (or S^1_2), then Extended Frege has polynomial-size proofs of the UNSAT instances, size polynomial in N with degree depending on A and the proof. So for R = EF the bridge B3 holds under the *strengthened* hypothesis "SAT∈P by a PV-provably-correct algorithm" (call it B3-PV).
Classification: EXACT TRANSFER for B3-PV in R=EF. Combined with a (still open) EF superpolynomial lower bound it yields only "no PV-provably-correct polynomial SAT algorithm", strictly weaker than P≠NP. For the unrestricted B3 the missing step is a reflection principle R ⊢ Con-type statement for arbitrary A, which is not available (it would make R an optimal proof system; existence of optimal proof systems is open, Krajíček–Pudlák: implied by NE=coNE).
So the realistic ordering of targets: (i) EF/Frege lower bounds (open; best known are linear/quadratic-type bounds for Frege), (ii) B3-PV, (iii) full B3 only via an optimal-system argument.

## Exact small minima (COMPUTATIONAL; no asymptotic content)
Script `experiments/worstcase/min_res_dag.py` (SAT encoding of "refutation with s derived clauses", DAG-like, no weakening, tautologies excluded; python-sat Cadical). Free choice of derivation is exactly the inner min, as in the directive.
Sanity check: first version allowed tautologies and returned wrong minima (2 for the triangle Tseitin formula); after forbidding tautologies the triangle value 5 matches a hand derivation. Axioms are counted as free; only derived clauses are charged.
| formula | vars | axioms | min derived clauses |
|---|---|---|---|
| Tseitin triangle (charge on one vertex) | 3 | 6 | 5 |
| Tseitin K4 (charge on one vertex) | 6 | 16 | ≥ 12 (s ≤ 11 UNSAT; SAT value not reached within budget) |
| PHP 3 pigeons / 2 holes | 6 | 9 | see results/raw/worstcase_php32_minres.txt (≥ 9 proven when this note was written) |
Chunking: iterative s with one solver call per s, output logged per s; each call ≤ 30 s except the final PHP run, which was a background job. These sizes say nothing about growth rates; they only certify the tooling for the "certified shortest derivation" role.

## WHAT CHANGED RELATIVE TO ROOT MAIN
Nothing is claimed for root main.tex. Lemma 1 is a clarification of quantifier logic; the PV/EF item is a known theorem restated. No status of any load-bearing arrow changes.

## Literature check this run
Peitl–Szeider-style exact shortest-refutation encodings and "Are hitting formulas hard for resolution?" (arXiv 2206.15225) confirm SAT-based exact minimization is feasible only for very small formulas (≈13 clauses for hitting formulas). Tseitin regular-resolution bound 2^{Ω(tw(G)/log|V|)}. Automating resolution is NP-hard (Atserias–Müller; Göös et al.) — relevant: computing W_R(F) exactly is itself hard, consistent with not charging for search. No 2026 result found that bears on B3.

## Next steps
1. LSPV-1: confirm whether Lemma 1 duplicates /334 or /406; if so cite and drop.
2. Red team: state B3-PV precisely for R_mix341 (does R_mix341 simulate EF? if not, the PV transfer does not apply).
3. Time-space auditor: the EF transfer's polynomial degree depends on the PV proof length of A's correctness — charge it.
