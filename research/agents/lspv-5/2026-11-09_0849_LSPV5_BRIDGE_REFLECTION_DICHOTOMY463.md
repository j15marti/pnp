<!-- LSPV-5 REPORT::BRIDGE_REFLECTION_DICHOTOMY463::2026-11-09T08:49-08:00 -->
# LSPV-5/463: the bridge SAT∈P ⇒ W̄_R ≤ poly — reflection dichotomy

**2026-11-09 08:49 PST | Route B red team | KNOWN THEOREM + PROVED/RESTRICTED logical lemmas | P versus NP remains OPEN**

Target: the user's weakest sufficient bridge `SAT∈P ⇒ W̄_R(N) ≤ poly(N)` where `W̄_R(N)=max_{F∈UNSAT,|F|≤N} min_{π:F⊢_R⊥} cost_R(π)`; free choice of the optimal π, no search charge.

## Obstacles
(1) The bridge is a statement about a *fixed* R and an *arbitrary* polynomial SAT decider A; (2) a derivation in R must be sound without trusting A.

## Results
**L1 (bridge is vacuous-equivalent to P≠NP for any R with a known lower bound). PROVED/RESTRICTED.** If R has a proven superpolynomial W̄_R (Resolution: Haken 1985; Tseitin/expander; PHP; R in the Cook–Reckhow sense), the conclusion `W̄_R ≤ poly` is false, so the bridge ⇔ `SAT∉P`. Proving the bridge for such R *is* proving P≠NP; it adds no progress (reformulation, cf. world-ledger rule). The bridge is meaningful only for R with no known lower bound (Frege, EF, and R_mix341 insofar as it simulates them) — consistent with the open [P2-B1]/[P2-B2] status.

**L2 (trace systems are unsound). PROVED/EXACT (logic).** Define R_tr by "π = (A, 1^t, rejecting run of A on F)". Then W̄_{R_tr} ≤ poly under SAT∈P trivially, but R_tr is not a Cook–Reckhow system: its verifier cannot check that A is correct, so acceptance does not imply F∈UNSAT. Restricting to correct A makes verification non-polynomial (coNP-type statement). So "free trivial bridge via machine traces" fails; this matches the standing LOCAL-CONVERT/soundness-reflection gap in [P2-L5-459].

**L3 (the honest weakest bridge is a reflection hypothesis). KNOWN THEOREM + restricted lemma.** Cook 1975 / Krajíček–Pudlák 1989: if PV (or S¹₂) proves the correctness of a polynomial SAT decider A, then the propositional translations have polynomial-size EF proofs, hence `W̄_EF ≤ poly`. Thus for R ⊇ EF:
`T_R := "∃ poly A deciding SAT whose instance-wise correctness has poly-size R-proofs"`; `W̄_R ≥ superpoly ⇒ ¬T_R`. This yields P≠NP only with the extra step `P=NP ⇒ T_R`, which is itself equivalent to `W̄_R ≤ poly` (the instance-wise correctness formulas are exactly UNSAT instances). The bridge is therefore *circular at the level of a single fixed R* unless supplied with an independent argument that a P=NP algorithm can be chosen/ reflected inside R. NP=coNP ⇔ some p-bounded system exists (Cook–Reckhow) shows the non-circular statement quantifies over *all* systems, not one fixed R.

**Consequence for the programme (recommendation).** Do not spend effort on proving the bridge for one fixed R as a standalone lemma. Two non-circular routes remain: (a) a lower bound for *every* R in a closed class together with a uniform-simulation theorem (the [P2-C3] shared-work simulation) and a statement that P=NP gives a member of the class (the [P2-B2] B3 obligation, still OPEN); (b) the conditional route "P=NP ⇒ SAT algorithm with R-provable correctness" as an explicit *CONDITIONAL* theorem, which a lower bound for EF would refute (a strictly weaker conclusion than P≠NP, labelled so).

## Literature check (this run)
- Cook–Reckhow: NP=coNP ⇔ ∃ p-bounded proof system. KNOWN. Frege best lower bound is only Ω(n²) (survey, Lin/Pitassi-Urquhart style; unchanged). KNOWN.
- Pich–Santhanam, arXiv 2312.08163: P≠NP follows if EF cannot prove circuit lower bounds for certain hard functions (plus conditions). Analogy/CANDIDATE: another reflection-flavoured bridge; requires reading before use (only abstract-level seen this run).
- arXiv 2406.10476 (single-author claim that Frege is not p-bounded): unverified, **not used**; treat as CANDIDATE-at-best, no status change.
- Krajíček–Pudlák bounded-reflection material: cited from memory as KNOWN; primary-source recheck pending.

## Audit entries
CORPUS REVIEWED: AGENTS.md, 2026-11-09 abstract-interpretation refocus, LSPV-5 459/462, LSPV-1 376 (root quotient), proof tracker headings. DUPLICATION: W̄_R notation and [P2-B1/B2/C3] already present; L1–L3 as stated are new framing only. WHAT CHANGED RELATIVE TO ROOT MAIN: nothing edited — root `main.tex` has no `LSPV-5 OWNED` markers locally (grep empty), so structural initialisation is left alone per policy. STALE/OVERSTATED: none found. No tracker node promoted; no schedules/roles changed. Predecessor LSPV-4 (07:50) report 522 present and substantive.

Status: **P versus NP remains OPEN.** The bridge is not proved; L1–L3 show it cannot be a free-standing lemma for one fixed R.
<!-- END_OF_VERIFIED_REPORT::LSPV-5::BRIDGE_REFLECTION_DICHOTOMY463 -->
