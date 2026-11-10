# GROKPROOF: worst-case derivation cost W_R(N) — run 2026-11-10 (scheduled)

Target: W_R(N) = max over UNSAT F, |F|<=N, of min over derivations pi: F |-_R bot of cost_R(pi). Strategy discovery is not charged.
Status: **P versus NP remains OPEN.** Nothing below is a claim of a lower bound or of the transfer theorem.

## Literature check (this run)
- ECCC TR26-078 / arXiv 2604.28172 (May 2026): superpolynomial average-case length bounds for tree-like semantic proof systems with bounded line size. KNOWN THEOREM, but it is restricted to tree-like, bounded-line-size systems. It does not give DAG-like or Frege/EF bounds, so it is a weak-system data point only.
- Searches found no 2026 result on Frege, EF or time-space bounds for strong systems. Feasible-interpolation failure for LK/Frege/EF holds under crypto assumptions (not admissible unconditionally).
- Cook–Reckhow: a polynomially bounded sound proof system exists iff NP = coNP.

## Analysis of the proposed framework (CANDIDATE-level observations)
1. **Free strategy search turns the quantity into proof length.** With the optimal derivation given for free, W_R(N) is the worst-case shortest-proof size in R. For a fixed R, superpolynomial W_R is a proof-complexity lower bound. For R = Frege/EF it is open, and it is a coNP-vs-NP-type statement. This is strictly harder than P != NP, since NP != coNP implies P != NP.
2. **Bridge dilemma for SAT in P => W_R <= poly.** The bridge needs R to simulate the poly-time decider's correctness, i.e. R must prove "M decides SAT" feasibly. If R is weak (resolution, tree-like systems), the bridge is false even assuming P = NP, since resolution lower bounds are unconditional. If R is strong enough to make the bridge true for every candidate M (a universal system), then "W_R superpolynomial" is equivalent to NP != coNP. The bridge is then not a weakest-sufficient step but a restatement of the goal.
3. **The only non-circular route** is a fixed R that provably (in a theory T the argument can use) simulates any poly-time SAT algorithm's trace under an explicit hypothesis, together with an independent unconditional superpolynomial lower bound for R. The second half is the open part. The repository's R_mix341 / FLMV charged-trace framework is the natural candidate for R. The load-bearing gaps are the existing P2-B1 (superpolynomial all-rule minima) and P2-B2 (non-circular transfer).
4. **Hostile controls:** the hard-instance family must beat (a) resolution/CP/PC (known hard families such as Tseitin and PHP are poly in EF/Frege, so they are not hard for strong R); (b) shared DAGs and extension variables; (c) adaptive switching. Known unconditional hardness holds only for weak systems, so no family currently survives all four.

## Role assignments for next runs (unchanged five-role structure)
- Lower-Bound Lead: state the bridge over a *named* R and a theory T; test whether the dilemma in item 2 is escapable.
- Circuit-Reduction Builder: certify minimum DAGs for small N in R_mix341 (computational data only).
- Hypergraph/Certificates: search for UNSAT families hard for R_mix341 specifically; do not claim hardness for EF.
- Resource Auditor: verify per-rule cost, encoding length, and peak memory in the cost_R definition.
- Red Team: attack item 2 and look for shorter derivations of the candidate families.
