# Shared worst-case derivation-cost directive (created 2026-11-10)

Additive: changes no schedules, agent count, or role ownership. Results are CANDIDATE/OPEN. P vs NP remains OPEN.

## Objective (all five roles)
For a fixed Cook-Reckhow proof system R (poly-time verifier V_R):

    W_R(N) = max over UNSAT F, |F|<=N  of  min over pi : F |-_R bottom  of  cost_R(pi)

Strategy search is NOT charged (min over pi is free); this only makes the lower bound easier to state.
Target pair: (L) W_R superpolynomial, and (B) the bridge  SAT in P  =>  W_R <= poly(N).
(L) and (B) together give SAT not in P.  Either alone does not.

## Role questions
| Role | Next question |
|---|---|
| General SAT Lower-Bound Lead | Is (B) for R = EF equivalent to a feasible-provability statement (see LOG E1)? Which hypotheses I-II of Pich-Santhanam 2023 are needed and are they plausible? |
| SAT-Circuit Reduction Builder | Fix cost_R as DAG size x line width; give an explicit R containing EF + trace-evaluation and certify shortest DAGs for small n by exhaustive search. |
| Hypergraph & Proof Certificates | For each candidate hard family (random 3-CNF, Tseitin, PHP, XOR-lifted) record which of Res / PC / CP / BD-Frege / EF-with-Gauss-counting refutes it cheaply. Only families that survive all are interesting for (L). |
| Time-Space Resource Auditor | Cost = (size, line-space, bit-work). Check that "minimal reduced logical state" is clause-space (Esteban-Toran) and which size/space tradeoffs transfer. |
| Independent Proof Red Team | Attack E1-E3 in the LOG; search for a closed-form counterexample to any pointwise simulation theorem. |

## Standing rule
Every run: log literature checked, status labels (PROVED/EXACT, KNOWN, CANDIDATE, OPEN, FALSIFIED/RETIRED), and append to `LOG.md`.
