# Living log: worst-case minimum-derivation-cost programme (W_R)

Target: W_R(N) = max_{F in UNSAT, |F|<=N} min_{pi: F |-_R bot} cost_R(pi).
Primary bridge sought: SAT in P  ==>  W_R(N) <= poly(N).   Status of P vs NP: **OPEN**.
Free choice of the optimal derivation is allowed (min over pi is not charged for search).

Statuses: PROVED/EXACT, KNOWN THEOREM, COMPUTATIONAL, CONDITIONAL, CANDIDATE, OPEN, FALSIFIED/RETIRED.

## 2026-11-06 run CLAUDE-WORSTCASE-0001
Report: research/agents/claude/2026-11-06_CLAUDE_WORSTCASE-0001.tex
- PROVED/EXACT (elementary): B(R) <=> (P != NP) OR (W_R poly). Hence for every R with a known superpolynomial
  lower bound (Res, Cutting Planes, bounded-depth Frege, PC/Nullstellensatz on suitable families) B(R) is
  *equivalent* to P != NP: the bridge is a restatement there, not a route.
- PROVED/EXACT: for a poly-time checkable R, "free best sequence" adds nothing: W_R is the usual proof-size
  function, so lower bounds on W_R for one R do NOT give NP != coNP (Cook-Reckhow needs all systems).
- KNOWN THEOREM/CONDITIONAL: the only non-trivial open window is R in {Frege, EF, stronger}. Pich-Santhanam
  (arXiv 2312.08163) give a conditional bridge of the right shape: EF lower bounds for a circuit-lower-bound family
  plus S^1_2-provability of the circuit lower bound => P != NP. Not unconditional.
- OBSTRUCTION identified (CANDIDATE diagnosis): SAT in P gives correctness of the *rejecting* answer only via
  a Pi_1-type statement "decider is sound on UNSAT"; R must prove it, which P = NP alone does not supply
  (P = NP could hold with an algorithm whose correctness is unprovable). So the bridge needs "provable P = NP"
  or an optimal proof system; existence of an optimal system is open (Krajicek-Pudlak).
- COMPUTATIONAL: exact-minimum-resolution harness research/worst-case/min_res.py written, but naive iterative-deepening
  DFS timed out on all samples; NO values reported. TODO: SAT-based (CEGAR/SAT-encoded) minimum DAG-resolution size.
- Next targets: (1) decide whether a natural multisign-hypergraph R is simulated by EF (then B(R) reduces to the
  EF window); (2) hard-family candidates for non-EF-simulated R; (3) rewrite min_res.py as SAT encoding.
- Red-team items: cost model must charge clause width in bits; check weakening/sharing assumptions.
