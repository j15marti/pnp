# Living log: worst-case derivation complexity W_R(N)

Directive: W_R(N) = max over UNSAT F (|F|<=N) of min derivation cost; free choice of derivation.
Halves: (LB) superpoly W_R for a natural R; (BR) SAT in P => W_R <= poly. (LB)+(BR) => P != NP.

## 2026-11-10 WCD-0001
- Report: `2026-11-10_WCD-0001_BRIDGE_CRITERION.tex`
- PROVED/EXACT (standard): bridge holds for R>=EF if poly-size R-proofs of soundness tautologies Snd_A(n) exist for some poly-time SAT decider A (Cook translation route).
- Dichotomy: trivial system R_A makes (BR) tight but is a reformulation of P != NP; natural weak systems have (LB) but not (BR); EF has plausible (BR) but (LB) is the open Cook-Reckhow conjecture.
- EF-easy families (exclude as hard instances): PHP, Tseitin. Remaining candidate: random ~4.3 ratio 3-CNF (EF-hardness OPEN).
- Literature: Pich-Santhanam STOC'21 (PV can't prove strong coNP-circuit lower bounds), Li-Oliveira, EF proof-search NP-complete (2025).
- Next: Reduction Builder exhaustive minimal-DAG calibration n<=6; Red Team relativized separation of (BR) attempt.
- Status: P vs NP OPEN. Root main.tex untouched.
