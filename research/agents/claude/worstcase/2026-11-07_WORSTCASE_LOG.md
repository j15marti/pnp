<!-- WORST-CASE DERIVATION LOG::WC-0001::2026-11-07 -->
# Living log: worst-case derivation cost  W_R(N) = max_{F in UNSAT,|F|<=N} min_{pi: F |-_R bot} cost_R(pi)

Status of P vs NP: **OPEN**. Nothing below proves a lower bound. Labels follow AGENTS.md status discipline.
Note: no standalone "shared worst-case research directive" file existed in the repo at this run; this log is its first anchor.
Literature below is cited from memory (no web search in this run); verify before relying on it.

## WC-0001 (2026-11-07) — what the "free optimal sequence" convention implies

**Claim 1 (KNOWN THEOREM, Cook–Reckhow 1979).** If R is a propositional proof system (derivations checkable in
poly time, complete for UNSAT), then  W_R(N) <= poly(N) for all N  iff  UNSAT has poly-size R-proofs.
Hence "W_R poly for some such R" is equivalent to NP = coNP.

**Consequence A (EXACT, from Claim 1).** Because strategy-search is not charged, W_R is a *nondeterministic*
(certificate-size) measure, not a deterministic-time measure. A superpolynomial W_R for a *universal* R
(one that p-simulates every Cook–Reckhow system) would prove NP != coNP, which is strictly stronger than
P != NP. So the program as stated is at least as hard as the Cook–Reckhow program, not an easier route.

**Consequence B (the bridge SAT in P => W_R <= poly).**
- For a *fixed* R that is not p-optimal the bridge is FALSE-or-unknown: SAT in P does not give poly R-proofs
  unless R can p-simulate the correctness proof of the P algorithm. Resolution is the standard counterexample
  to the bridge's *hypothesis being usable*: exponential resolution lower bounds (Haken 1985, Urquhart 1987,
  Ben-Sasson–Wigderson 2001) hold unconditionally, and they do **not** refute SAT in P (DPLL/CDCL traces are not resolution-poly).
  Such an unconditional lower bound would contradict the bridge, so the bridge cannot hold for resolution (KNOWN, trivially).
- For the bridge to hold, R must be "as strong as the algorithm's own correctness proof". Known form
  (Krajicek–Pudlak 1989; Cook's PV; Buss S^1_2): if SAT in P *with correctness provable in S^1_2*, then
  Extended Frege has poly-size proofs of UNSAT. The unconditional version of the bridge for Frege/EF is
  therefore CONDITIONAL on feasible provability of the algorithm. Status: CONDITIONAL.
- Existence of a p-optimal proof system (which would make the bridge unconditional for that R) is OPEN
  (Krajicek–Pudlak 1989 relate it to NE=coNE-type hypotheses).

**Consequence C (what a non-vacuous formulation must do).** To get SAT not in P from a lower bound, cost_R must
be a *deterministic-time-like* measure on a model where one UNIFORM small description generates the derivation
(i.e., charge for the program/rule-schedule, or restrict R so strategy is a poly-time function of F). The
"free optimal sequence" relaxation then *removes* exactly the content that distinguishes P from NP.
Candidate repair (CANDIDATE, unproved): define R as derivation DAGs produced by a fixed uniform deterministic
generator G(F) and take W_R = max over F of |G(F)| — this makes SAT in P => W_R poly true by construction but
the lower bound is then equivalent to SAT not in P itself (no progress, a reformulation).
Per the world ledger rule: a statement equivalent to P != NP is a reformulation, not progress.

## Role assignments for next run (suggested; no schedule changes)
- Lower-Bound Lead: decide whether a *non-nondeterministic* cost (uniform generator, charged description) can avoid the reformulation trap; else retire the free-sequence W_R as equivalent to NP vs coNP.
- Circuit/Reduction Builder: test whether any fixed R with hypergraph-DAG states is p-equivalent to Frege/EF (then lower bounds = open Frege lower bounds).
- Hypergraph/Certificates: hard-UNSAT families vs known barriers (Frege lower bounds open; resolution/PC/cutting planes known).
- Time-Space Auditor: tie to ARC/FLMV spine only if a deterministic-time cost is chosen.
- Red Team: attack Consequence B (find an R for which bridge is provable unconditionally) and Consequence A (is there a weakening making W_R deterministic?).

<!-- END_OF_WORST_CASE_LOG::WC-0001 -->
