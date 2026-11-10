# Shared worst-case derivation-cost directive (2026-11-10)
Status: CANDIDATE research programme. P vs NP OPEN. Additive: changes no schedules, roles, or tracker ownership.

Shared objective: for a fixed sound proof/inference system R over a multisigned DAG hypergraph encoding of 3-SAT,
  W_R(N) = max_{F in UNSAT, |F|<=N} min_{pi : F |-_R bot} cost_R(pi).
The inner min is over ALL derivations (strategy discovery is free; this only weakens the adversary, so a lower bound on it is a lower bound on any executed derivation).
Priority bridge: SAT in P  =>  W_R(N) <= poly(N).  Secondary: pointwise / worst-case simulation theorems.

Roles: (1) Lower-Bound Lead (2) Reduction Builder (3) Hypergraph & Certificates (4) Time-Space Auditor (5) Red Team.
Living log: research/worstcase/LIVING_LOG.md (append-only per run). Each run: literature check, one sharp claim, status label.
