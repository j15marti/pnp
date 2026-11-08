# Shared worst-case derivation directive (WCD-1), 2026-11-08

Additive research directive from the user. It creates no tasks and changes no schedules. **P versus NP remains OPEN.** This is a refinement of strategy, not a claim that the lower bound or the transfer theorem is established.

Objective (all five roles):

    W_R(N) = max_{F in UNSAT, |<F>|<=N}  min_{pi : F |-_R bot}  cost_R(pi)

Strategy discovery is NOT charged (free optimal derivation). Priorities:
1. Superpolynomial lower bound on W_R in a fixed, sufficiently strong system R.
2. Weakest sufficient bridge B(R): SAT in P  =>  W_R(N) <= poly(N).
3. Stress hard instances against resolution, algebraic (PC/Res(lin)), circuit compression, shared DAGs, adaptive switching.
Stronger pointwise / worst-case simulation theorems are secondary.

| Role | Responsibility |
|---|---|
| General SAT Lower-Bound Lead | formalize W_R, prove weakest transfer theorem |
| SAT-Circuit Reduction Builder | fixed combined inference system, certified shortest DAGs |
| Hypergraph & Proof Certificates | hard UNSAT families surviving alternative reasoning |
| Time-Space Resource Auditor | inference cost, encodings, overhead, peak memory |
| Independent Proof Red Team | counterexamples, shorter derivations, failures of transfer |

Living log: `research/agents/claude/worst-case/LIVING_LOG.md` (append-only entries, newest last).
Every run: search literature for clues on the specific obstacle and record it in the log.
