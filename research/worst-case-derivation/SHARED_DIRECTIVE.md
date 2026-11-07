# Shared worst-case derivation directive (created 2026-11-07 10:50 UTC)

Common target for all five roles (General SAT Lower-Bound Lead; SAT-Circuit Reduction Builder;
Hypergraph & Proof Certificates; Time-Space Resource Auditor; Independent Proof Red Team).
Additive: changes no schedules, agent count, or role ownership. **P versus NP remains OPEN.**

    W_R(N) = max_{F in UNSAT, |<F>|<=N}  min_{pi : F |-_R bottom}  cost_R(pi)

* The optimal derivation pi is chosen freely (no charge for strategy discovery).
* Priority bridge:  Bridge(R):  SAT in P  ==>  W_R(N) <= poly(N).
* Hard-instance candidates must be tested against resolution, algebraic (NS/PC), circuit
  compression, shared DAGs, adaptive strategy switching.
* Every run: check current literature for clues to the specific obstacle; log in
  `LIVING_LOG.md` (append only).
* Status labels: PROVED/EXACT, KNOWN THEOREM, COMPUTATIONAL, CONDITIONAL, CANDIDATE, OPEN, FALSIFIED/RETIRED.
