# Living log: worst-case derivation cost  W_R(N)  (user directive 2026-11-09)

Target: W_R(N) = max over UNSAT F, |F|<=N, of min over derivations pi of F in R of cost_R(pi).
Weakest bridge sought: SAT in P  =>  W_R(N) <= poly(N).  Status of everything below: CANDIDATE/OPEN unless marked. P vs NP remains OPEN.

## Entry 1 (2026-11-09, scheduled run, single-agent pass)

Corpus note: repository is very large (hundreds of LSPV reports; ARC/FLMV, knot/link and abstract-interpretation handoffs are active). This entry did not re-survey all of it and adds no change to root main.tex or any role schedule.

### Quantifier audit of the bridge (analysis, not a new theorem claim)
1. **Bridge is circular for weak R.** For R = resolution, W_R(N) >= 2^{Omega(N^eps)} unconditionally (Haken; Ben-Sasson–Wigderson). So "SAT in P => W_R poly" is then equivalent to "SAT not in P". Proving it proves P != NP; it cannot be an independent step. Same for any R with a known superpolynomial lower bound.
2. **Bridge for strong R reduces to an open proof-complexity statement.** If SAT in P, then NP = coNP, so SOME proof system has poly-size proofs. For a FIXED R, poly-boundedness needs R to p-simulate that system, i.e. R must be (essentially) p-optimal. Existence of p-optimal/optimal propositional proof systems is a known open problem (Krajicek–Pudlak 1989: exists if E = NE; Cook–Krajicek: exists with one advice bit). So the bridge "for the fixed R we build" is at least as strong as an open optimality statement unless R is engineered to encode every poly-time algorithm.
3. **Soundness obstruction in engineering R.** Take R_alg = "trace of M_i accepting/rejecting F". It is a sound proof system only for the correct decider; correctness of M_i is not locally checkable, so no fixed polynomial-time-verifiable R contains all candidate deciders' traces. Needs provable correctness of the algorithm inside R (bounded-arithmetic style: Cook–Reckhow / Krajicek–Pudlak), which is not given by SAT in P alone.
4. **Free choice of optimal sequence is harmless but also does not help.** Minimizing over sequences only lowers the cost, so lower bounds on the minimum are stronger; but the minimum of cost over all derivations of F in R equals proof size in R (up to cost model), which is exactly the Cook–Reckhow program. The cost_R time-space charge (peak memory) is where a new ingredient could live: time-space tradeoffs for R-derivations are not a known route to bridge (2).
5. **Multisign DAG hypergraph.** Not yet formalised in this log. Needed: rule set, size/space measure, and a p-simulation of or by Frege/EF. Until then no claim that hard instances survive "algebraic reasoning, circuit compression, shared DAGs" (all of which are p-simulated by or equal to EF-type systems; circuit compression + shared DAG ~ extended Frege, where no superpolynomial lower bound is known).

### Consequence for the five roles (proposed, not yet adopted)
- Lower-Bound Lead: the weakest sufficient bridge must be stated for a class R* closed under "provably correct algorithm" (EF + reflection-style), not for a fixed weak R. State precisely which p-simulation hypothesis is assumed; that hypothesis is itself OPEN.
- Hypergraph/Certificates: any hard family must beat EF, otherwise it refutes nothing about SAT in P. Known barriers: no EF lower bounds; Razborov–Rudich-style natural-proof and feasible-interpolation limits for strong systems.
- Resource Auditor: define cost_R(pi) = (time, space) of a standard verifier and check closure under composition.
- Red Team: test item 1 (circularity) and item 3 (soundness) as candidate refutations of any proposed "transfer theorem".

### Literature check (this run)
Standard web search only. Found: p-optimal proof system existence is still listed as open; Egidy, arXiv:2602.02294 (Feb 2026, "SPARSE-Relativization Framework and Applications to Optimal Proof Systems") is a possibly relevant new preprint — abstract not read here; next run should read it. Also Characterizing p-simulation between theories, arXiv:2507.13576.
Sources: https://arxiv.org/abs/2602.02294v1 , https://arxiv.org/html/2507.13576v1 , https://en.wikipedia.org/wiki/Propositional_proof_system

### Status
No new theorem. P vs NP: OPEN. Load-bearing arrow (bridge) is conditional on an open p-optimality-type hypothesis, or circular for weak R.
