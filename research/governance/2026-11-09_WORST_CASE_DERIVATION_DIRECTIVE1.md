# Shared worst-case derivation-cost directive (2026-11-09)

Additive; changes no schedules, agent count or role ownership. Living log: `research/worst-case-derivation/LOG.md`.

Common target (all five roles):

    W_R(N) = max_{F in UNSAT, |<F>|<=N}  min_{pi : F |-_R bot}  cost_R(pi)

Strategy search is free (not charged): this only lowers the min, so a lower bound on W_R remains valid.

Weakest sufficient bridge: BRIDGE(R) := [SAT in P  =>  W_R(N) <= poly(N)].

Roles: General SAT Lower-Bound Lead; SAT-Circuit Reduction Builder (fixed combined inference system, certified shortest DAGs);
Hypergraph & Proof Certificates (hard UNSAT families vs resolution/algebraic/circuit/shared-DAG/adaptive switching);
Time-Space Resource Auditor (inference cost, encoding, overhead, peak memory); Independent Proof Red Team (counterexamples, shorter derivations, transfer failures).

Standing constraints from WCD-0001 (see log): any proposed R must declare (a) whether it is Cook-Reckhow (poly-time checkable);
(b) why BRIDGE(R) is not circular (see Dichotomy theorem); (c) the cost model, charging verification, not search.
Every run: check literature for clues to the specific open arrow and record it in the log. P vs NP remains OPEN.
