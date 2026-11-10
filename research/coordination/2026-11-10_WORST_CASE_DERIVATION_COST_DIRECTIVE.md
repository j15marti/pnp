# Shared worst-case derivation-cost directive (user-requested, additive)

Status: CANDIDATE/OPEN. Living log: `research/worst-case/LOG.md`. This changes no schedules,
agent count, role ownership, or the root-main ownership rules. P versus NP remains OPEN.

Objective (all five roles):

    Wbar_R(N) = max_{F in UNSAT, |<F>|<=N}  min_{pi : F |-_R bot}  cost_R(pi)

The inner min is taken over all derivations with the optimal one given for free (strategy
discovery is not charged; this can only lower the min, so lower bounds on it remain valid).

Priorities:
1. Superpolynomial lower bound on Wbar_R in a fixed, sufficiently strong R.
2. Weakest sufficient bridge  B_R :  SAT in P  =>  Wbar_R(N) <= poly(N).
3. Hostile controls: hard families must survive resolution, algebraic (PC/GF(2)), counting,
   circuit compression (EF), shared DAGs and adaptive switching.
4. Every run: literature check for clues on the current obstacle.

Roles: General SAT Lower-Bound Lead (transfer theorem); SAT-Circuit Reduction Builder
(fixed combined system, shortest-DAG certificates); Hypergraph & Proof Certificates (hard
UNSAT families); Time-Space Resource Auditor (cost/overhead/peak memory); Independent Proof
Red Team (counterexamples, shorter derivations, transfer failures).

Key structural fact (see LOG 2026-11-10): B_R is logically equivalent to
"P != NP  or  Wbar_R is polynomial", so B_R is only informative for R with no known
unconditional lower bound, and any proof of it must build short R-proofs from an arbitrary
correct polynomial-time SAT algorithm.
