# Worst-case minimum-derivation living log (Claude scheduled routine)

Directive: `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`
Target: superpolynomial lower bound on  Wbar_R(N) = max_{F in UNSAT, |F|<=N} min_{pi: F |-_R bot} cost_R(pi)
for a fixed R, plus the bridge B3: SAT in P  =>  Wbar_R(N) <= poly(N).
Free choice of the optimal derivation is allowed; search cost is not charged to the minimum.
Status of everything below: P versus NP remains OPEN. No new theorem is claimed in this log.

## 2026-11-09 run (scheduled)

**Corpus surveyed:** AGENTS.md; the 2026-11-02 12:04 refocus directive; LSPV-1/395 (uncomputable worst-case node profile
for an artificial calculus), LSPV-1/415 (Pi^0_1 firewall for clocked-rejection soundness); file listing of
research/agents/lspv-1 (reflection reports 336, 353, 361, 405, 415) and research/coordination (worst-case handoffs 335-407).
Not re-read in full: the ~430 LSPV-1 reports and issue #3 comment history (not reachable offline).

**Literature query (standard web search):** "P=NP implies extended Frege polynomially bounded provably correct SAT algorithm PV".
Clues returned (secondary, not independently verified in this run):
- Cook-Reckhow: a polynomially bounded proof system exists iff NP = coNP. This is weaker than P = NP, and a lower bound for one
  fixed R does not by itself give NP != coNP. So B3 needs P=NP to bound the *specific* R, not just some system.
- Cook's PV <-> Extended Resolution/Extended Frege correspondence. Known route to B2/B3 for R = EF: if PV proves that a
  polynomial-time SAT algorithm A is correct (Cor_A), translating the proof gives poly-size EF refutations built from A's trace.
  The extra hypothesis (provable correctness, i.e. a reflection principle) is exactly the gap the directive calls "uncertified machine correctness".
- Krajicek-Pudlak: EF is not weakly automatable unless RSA is insecure against P/poly. This is a cryptographic condition and is not admissible
  as an unconditional ingredient here.
- arXiv 2506.16956 (Proof Analysis Problem) and arXiv 1308.5608 (Implicit Resolution) were surfaced; neither was read in full.
- Access note: the search tool could not confirm the exact statement "P=NP => EF polynomially bounded"; it is not asserted.

**Duplicate check:** the reflection / clocked-correctness bridge for the repo's R_mix341 has been audited extensively by
LSPV-1 (336, 353, 361, 405, 415). A fresh write-up of the PV-reflection route would duplicate that, so none was written.

**Observation (CONDITIONAL, standard reading, not new):** what the combined lower-bound/bridge strategy can honestly deliver is the
dichotomy  [Wbar_R superpolynomial]  ==>  [P != NP]  OR  [no polynomial-time SAT decider has a feasibly checkable
correctness proof relative to R]. Proving P != NP outright needs B3 with the reflection hypothesis removed, which is OPEN.

**Falsifiers proposed for the next run:**
1. A uniform total SAT decider A, fast on all inputs, with a short R_mix341 refutation family but no poly-size correctness certificate (would test B3 vs. B1).
2. A growing family where min-cost mixed DAG is superlinear under the existing LSPV-2/341 grammar (the open "next exact gap").
3. A relativized world (oracle in both sides' inputs) where the bridge argument is formally unaffected, to test whether B3 can be non-relativizing.

**Result this run:** audit + log only. No lemma proved, no hard family built, no finite optimum certified. Status: OPEN.
