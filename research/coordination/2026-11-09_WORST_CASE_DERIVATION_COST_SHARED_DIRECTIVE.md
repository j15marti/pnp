# Shared worst-case derivation-cost directive (2026-11-09, additive)

Status of everything below: **CANDIDATE/OPEN** unless tagged otherwise. P versus NP remains **OPEN**.
This directive is additive: it changes no schedules, agent count, or role ownership. Living log: `research/worst-case/LIVING_LOG.md`.

## Object
Fix a sound, poly-time-verifiable reduction/inference system R on multisign DAG hypergraphs of 3-CNF formulas
(vertices = variables, hyperedges = clauses carrying sign vectors; a derivation pi is a DAG of R-steps ending in the
empty clause / reduced state "bottom"). Define

    W_R(N) = max_{F in UNSAT, |<F>|<=N}  min_{pi : F |-_R bottom}  cost_R(pi).

cost_R is (a) step count, (b) total work = sum of bit-lengths of all intermediate states (time), (c) peak simultaneous
state size (space). The minimum is taken over derivations with the best sequence granted for free (search is not charged;
this can only lower W_R, so a lower bound on W_R is a lower bound on any real execution).

## Priority bridge
    B_R :  SAT in P  ==>  W_R(N) <= poly(N).
Secondary (not required): pointwise simulation and worst-case simulation theorems.

## Roles
| Role | Question |
|---|---|
| General SAT lower-bound lead | Prove the weakest sufficient transfer theorem for an R where B_R is not already equivalent to P != NP (see T2 in the log). |
| SAT-circuit reduction builder | Fix one combined system R (resolution + algebraic/XOR + extension/circuit-compression + shared DAG + strategy switching) and certify shortest derivation DAGs on small n by exhaustive/ILP search. |
| Hypergraph & proof certificates | Hard UNSAT families whose lower bound survives each sub-method of R, not just resolution. |
| Time-space resource auditor | Check cost_R accounting: encoding length of steps, per-step overhead, peak memory; match the model of the ARC/FLMV spine. |
| Independent proof red team | Look for short derivations of the proposed hard families and counterexamples to every transfer theorem; attack the T1-T3 observations. |

## Standing rules
Each run: search literature for clues bearing on the current obstacle; log in LIVING_LOG.md (append-only entries, newest last);
use only the status vocabulary of AGENTS.md; a lower bound for a *weak* R proves nothing about P vs NP (see T2).
