# Living log: worst-case derivation cost program (append-only)

## 2026-11-05 run 1 (CLAUDE-WC-0001)
Status: OPEN. New structural results (KNOWN-THEOREM-level arguments, written up in
`2026-11-05_CLAUDE_WC-0001_bridge_dilemma.md`):
1. Weak R (Resolution, cutting planes, PC, bounded-depth Frege): W_R is exponential unconditionally,
   so the bridge "SAT in P => W_R poly" is *equivalent to* SAT not in P. Proving the bridge = proving P != NP. Useless as a route.
2. Strong R: the bridge needs R to p-simulate whatever proof system a hypothetical P algorithm induces.
   With an optimal proof system O the bridge is a theorem (SAT in P => NP=coNP => O p-bounded), but then
   "W_O superpolynomial" is *equivalent* to NP != coNP, strictly stronger than P != NP. Existence of O is open.
3. Free strategy choice = nondeterminism. With poly-time-checkable derivations, W_R poly <=> UNSAT has
   poly certificates in R. So the program as posed targets NP vs coNP, not P vs NP, unless cost_R is
   not merely verifiable length (then verification-cost / space must carry the load).
Literature check: no 2026 Frege/EF lower bound found; Alekseev (ToC 22, 2026) subset-sum lower bound
for an EF-simulating algebraic system (CCC'21). Frege/EF lower bounds remain open.
Next: (a) define cost_R with space so W_R can be small only if SAT in P (non-verifiable cost); (b) Red Team: check that
such cost does not collapse to proof length; (c) auditor: peak-memory accounting for DAG-like derivations.
