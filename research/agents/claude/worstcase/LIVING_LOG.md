# Worst-case derivation complexity — living log (P vs NP remains OPEN)

Target: W_R(N) = max_{F in UNSAT, |F|<=N} min_{pi: F |-_R bot} cost_R(pi); weakest bridge: SAT in P => W_R(N) <= poly(N).
Newest entries on top. Status labels: PROVED/EXACT, KNOWN THEOREM, COMPUTATIONAL, CONDITIONAL, CANDIDATE, OPEN, FALSIFIED/RETIRED.

## 2026-11-08 run WCD-0001  (report: 2026-11-08_WCD-0001_BRIDGE_TRIVIALITY.tex)
- PROVED/EXACT: Bridge(R) is equivalent to SAT not in P for every R with an unconditional superpolynomial bound (Res, bounded-depth Frege, CP-restricted...). So the bridge is never easier than the goal for known-hard R.
- PROVED/EXACT: for R = ZFC/T-reflection system, bridge <=> "if SAT in P via M then T proves Cor(M)" -- a provability principle, not a simulation; LB for it is a Pi_1-independence-flavoured statement, not P != NP.
- PROVED/EXACT: free-strategy minimisation is nondeterministic, so W_R superpoly for ONE R implies nothing (Cook-Reckhow needs all R); only the bridge links it to SAT in P.
- PROVED/EXACT: portfolios/adaptive switching cost at most additive size in a shared-DAG system; combined systems need translation rules and component LBs do not transfer.
- CANDIDATE next target: restricted bridges Bridge_C(R): "SAT solvable by algorithm class C => W_R poly" (DPLL/tree-Res, CDCL-with-restarts/Res, Groebner/PC, SOS/SOS). Instances are known theorems; the open task is a class C containing every polynomial algorithm.
- COMPUTATIONAL: exact min resolution steps, n=3 width-3 axioms: 7 (minres.py). n=4 BFS timed out (not completed; no claim).
- Literature: optimal/p-optimal proof systems open (Krajicek-Pudlak; P=NP => exist); CDCL simulates Res with restarts (Atserias-Fichte-Thurley, Pipatsrisawat-Darwiche). No clue closing the bridge found.
