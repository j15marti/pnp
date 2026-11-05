# Shared worst-case derivation directive (2026-11-05 17:00 UTC)

Additive; changes no schedules, agent counts or other allocations. Status: P vs NP OPEN.

Common target (all five roles):

    Wbar_R(N) = max_{F in UNSAT, |F|<=N}  min_{pi : F |-_R bot}  cost_R(pi)

Strategy discovery is NOT charged (min over derivations is a legitimate lower-bound quantity).

Priorities
1. Superpolynomial lower bound on Wbar_R for a fixed, sufficiently strong R.
2. Weakest sufficient bridge  Bridge(R): SAT in P  =>  Wbar_R(N) <= poly(N).
3. Hard UNSAT families surviving resolution, algebraic, circuit-compression, shared-DAG, adaptive-switching reasoning.
4. Time/space audit: proof encoding, per-rule cost, peak memory (pebbling of the derivation DAG).

Roles: General SAT LB Lead; SAT-Circuit Reduction Builder; Hypergraph & Proof Certificates;
Time-Space Resource Auditor; Independent Proof Red Team.

Living log: research/worst-case-derivation/LOG.md  (append one dated entry per run).
Every run: literature check for clues on the current obstacle; strict status labels.
