# Shared worst-case derivation-cost directive (additive; changes no schedules or allocations)

Common target for the five roles (General SAT Lower-Bound Lead; SAT-Circuit Reduction Builder;
Hypergraph & Proof Certificates; Time-Space Resource Auditor; Independent Proof Red Team):

    Wbar_R(N) = max_{F in UNSAT, |<F>|<=N}  min_{pi : F |-_R bot}  cost_R(pi)

* R must be a *Cook-Reckhow* system (fixed poly-time verifier V_R(F,pi)); see WC-0001 Thm 2 for why.
* Strategy search is free: min over pi is not charged for finding pi.
* Weakest sufficient bridge: Bridge(R) := [SAT in P  =>  Wbar_R(N) <= poly(N)].
* Test every hard family against: resolution, algebraic (PC/NS), circuit compression (extension variables),
  shared DAGs, adaptive switching between systems.
* Every run: literature check for clues to the *current* obstacle; append to LOG.md.
Status labels: PROVED/EXACT, KNOWN THEOREM, COMPUTATIONAL, CONDITIONAL, CANDIDATE, OPEN, FALSIFIED/RETIRED.
P vs NP remains OPEN.
