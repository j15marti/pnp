# Shared worst-case derivation-complexity directive (WC-DIR)
Created 2026-11-10. Status: CANDIDATE research direction. P vs NP remains OPEN. Additive: no change to schedules, roles, agent count or the existing proof trackers.

## Objective
For a fixed inference system R and cost measure cost_R (size, plus time/space of executing the derivation):

  Wbar_R(N) = max_{F in UNSAT, |<F>|<=N}  min_{pi : F |-_R bot}  cost_R(pi)

The inner min is free: finding the optimal derivation is not charged. This only strengthens a lower bound.

Priority bridge (weakest sufficient transfer): SAT in P  ==>  Wbar_R(N) <= poly(N).
Secondary targets: pointwise and worst-case simulation theorems.

## Roles (existing five agents; roles are unchanged)
1. General SAT lower-bound lead: formalise Wbar_R and the weakest sufficient transfer.
2. SAT-circuit reduction builder: a fixed combined inference system and shortest-derivation DAG certificates.
3. Hypergraph and proof certificates: hard UNSAT families that survive alternative reasoning.
4. Time-space resource auditor: inference costs, encodings, peak memory.
5. Red team: counterexamples, shorter derivations, failures of transfer.

## Standing rules
- Each run: literature check for clues, then log the result in research/worst-case/LOG.md.
- Any statement equivalent to P=NP or P!=NP is a reformulation, not progress.
- Hard-instance claims must be tested against resolution, polynomial calculus, extension variables, shared DAGs, and adaptive rule switching.
- Status labels: PROVED/EXACT, KNOWN THEOREM, COMPUTATIONAL, CONDITIONAL, CANDIDATE, OPEN, FALSIFIED/RETIRED.
