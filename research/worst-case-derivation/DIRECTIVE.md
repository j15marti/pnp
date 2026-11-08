# Shared worst-case derivation directive (WCD)

Objective (all five roles): study
  W_R(N) = max_{F in UNSAT, |F|<=N} min_{pi : F |-_R bot} cost_R(pi)
for a FIXED inference system R, with the optimal pi chosen for free (strategy search is not charged;
this only makes the lower bound stronger, so it is legitimate).
Priority bridge B(R):  SAT in P  ==>  W_R(N) <= poly(N).
Secondary: pointwise / worst-case simulation theorems.

Roles: (1) General SAT lower-bound lead; (2) SAT-circuit reduction builder (fixed combined system, shortest DAGs);
(3) hypergraph & proof certificates (hard UNSAT families); (4) time-space resource auditor; (5) red team.

Status: all of this is OPEN. P vs NP remains OPEN. Log: LOG.md (append-only, newest last).
