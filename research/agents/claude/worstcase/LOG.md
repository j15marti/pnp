# Worst-case derivation-cost programme — living log (append only)

Directive: `research/governance/2026-11-05_WORST_CASE_DERIVATION_DIRECTIVE1.md`. Status of P vs NP: **OPEN**.

## 2026-11-05 — run WORSTCASE-0001 (Claude)

**Corpus.** Surveyed repo tree, AGENTS.md, governance notes, world-ledger (rows on proof-system status), no prior repo file defines W̄_R; the directive referenced in the task did not exist and was created (additive).

**Proved / exact (self-contained, report §2–4):**
1. W̄_R poly for some Cook–Reckhow R ⇔ NP = coNP. So "∀R superpoly" ⇔ NP ≠ coNP (⇒ P ≠ NP). Fixed-R lower bounds are strictly weaker.
2. Bridge dichotomy (above): for R with known unconditional lower bound, B(R) ⇔ SAT ∉ P (pure logic, "equivalent of P ≠ NP" in the world-ledger taxonomy). Not progress.
3. Reflective bridge: T ⊢ "A solves SAT in poly time" ⇒ W̄_{R_T} ≤ poly. Needs the correctness proof inside T; unusable unconditionally.
4. Free strategy discovery is harmless for the lower bound but also removes all computational content: the quantity is a certificate-size measure and cannot see the time to *find* π. Any transfer to SAT ∉ P must therefore use an automatability-type step (search ≤ poly(cost)), which is the opposite direction from the stated bridge.

**Computational (small, exact).** SAT-encoded minimum DAG-resolution refutation size (`minres_sat.py`; sanity: all-8-clauses on 3 variables = 7 resolutions, matches independent BFS `minres.py`). Random minimally-unsatisfiable 3-CNFs on n=4 (4 seeds, ≈40 instances solved): minimum 7–9 resolution steps (hist 7:5, 8:24, 9:8 over solved ones; raw rows in `minres_n4_s*.json`), n=6 one instance 8. Chunking: ≤25 s per invocation, one seed each. Finite data say nothing about asymptotics.

**Literature (searched; secondary summaries, primary texts not verified):**
- Cook–Reckhow: p-bounded proof system ⇔ NP = coNP.
- Krajíček–Pudlák: optimal proof system ⇔ fast consistency prover; existence open; non-existence ⇒ NE ≠ coNE.
- Papamakarios (CCC 2024): depth-d Frege not automatable unless P = NP (the automatability direction: lower-bounds-on-search from P ≠ NP, not the reverse).
- Iwama / later: deciding "refutation with ≤ k steps" is NP-complete; no constant-factor approximation unless P = NP (so the *minimum itself* is hard to compute even though we grant it free).
- Davis–Robere, ECCC 2026/055: Res(log) proves bounded-depth Frege lower bounds (recent clue on stronger-than-resolution systems; abstract only seen).
- "Computing Shortest Resolution Proofs" (SAT-based, iterative K): the method used here.

**Red-team verdict on the stated plan.** The weakest sufficient bridge is not weak: for every R where a lower bound can currently be proved it is equivalent to the conclusion; for every R where it would be non-trivial both halves (lower bound, bridge) are open and independent. Recommended next targets, in order: (a) find any *unconditional* theorem of the form "P = NP ⇒ W̄_R ≤ poly" for a natural R (candidates: R = Extended Frege, or R given by DAG-hypergraph rules with extension); a non-trivial negative result (oracle / relativized world with P = NP and R not p-bounded, for R with oracle-free local rules) would retire the programme; (b) measure state/space (clause space, width) rather than size: lower bounds exist but are again unconditional-and-irrelevant to P vs NP.

Next run: attempt (a) relativized negative result for local-rule R.
