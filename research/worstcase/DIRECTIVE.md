# Shared worst-case derivation-complexity directive (2026-11-07)

Target quantity (all five roles: Lower-Bound Lead, Reduction Builder, Hypergraph/Certificates, Time-Space Auditor, Red Team):

    W_R(N) = max_{F in UNSAT, |F|<=N}  min_{pi : F |-_R bot}  cost_R(pi)

Optimal derivation is granted for free (strategy search is not charged).
Priority bridge:  SAT in P  ==>  W_R(N) <= poly(N).
Status: P vs NP, the lower bound, and the bridge are all OPEN. Nothing here asserts otherwise.
Living log: research/worstcase/LOG.md (append-only per run). Reports: research/agents/claude/.
Status labels: PROVED/EXACT, KNOWN THEOREM, COMPUTATIONAL, CONDITIONAL, CANDIDATE, OPEN, FALSIFIED/RETIRED.
