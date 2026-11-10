# Shared worst-case derivation directive (five roles)

Target: W_R(N) = max_{F in UNSAT, |<F>|<=N} min_{pi: F |-_R bot} cost_R(pi), over a *fixed* system R
(multisign DAG-hypergraph derivations; strategy discovery is NOT charged, since W_R is a min).
Priority 1: superpolynomial lower bound on W_R for a fixed, sufficiently strong R.
Priority 2 (weakest sufficient bridge): SAT in P  =>  W_R(N) <= poly(N).
Secondary: pointwise and worst-case simulation theorems. Test every hard family against resolution,
algebraic reasoning, circuit compression, shared DAGs, adaptive strategy switching.
Roles: (1) General SAT lower-bound lead; (2) SAT-circuit reduction builder (fixed combined system, certified shortest DAGs);
(3) hypergraph and proof certificates (hard UNSAT families); (4) time-space resource auditor; (5) independent red team.
Every run: check the literature for clues, append one entry to LOG.md. Status labels per AGENTS.md. P vs NP remains OPEN.
