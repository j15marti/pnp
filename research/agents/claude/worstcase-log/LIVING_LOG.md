# Living log: worst-case minimum derivation cost  W_R(N) = max_{F in UNSAT,|F|<=N} min_{pi: F |-_R bot} cost_R(pi)

Append-only. Status labels: PROVED/EXACT, KNOWN THEOREM, CONDITIONAL, CANDIDATE, OPEN, FALSIFIED/RETIRED.
**P versus NP remains OPEN.** No lower bound on W_R and no bridge SAT in P => W_R <= poly has been proved.

## 2026-11-05 run (CLAUDE-WC-0001)
- Corpus surveyed: AGENTS.md, governance notes, LSPV-1/391 (B1/B2/B3 encoding invariance), REFEREE294/325 (Cook-Reckhow, island-compiler firewall), world ledger.
- New (elementary, PROVED/EXACT): B3(R) <=> (P != NP or W_R polynomial). So B3 is exactly the conditional statement "P = NP => R polynomially bounded" and carries no content beyond that.
- New (PROVED/EXACT): R optimal (every sound Cook-Reckhow system is polynomially simulated by R) => B3(R). Converse fails to be informative: B3(R) + P=NP => R poly-bounded.
- KNOWN: if a poly-time SAT algorithm is PV-provably correct, Extended Frege is polynomially bounded (Cook; Krajicek-Pudlak). So B3 for EF holds under "provable P=NP".
- Literature: Pich-Santhanam arXiv 2312.08163 (EF lower bounds -> P != NP, conditional optimality under small SAT circuits); no 2026 result found giving unconditional Frege/EF lower bounds or an unconditional optimal system.
- Full write-up: 2026-11-05_CLAUDE_WORSTCASE-BRIDGE-0001.md in the parent directory.
- Next target: find a sound system R with a conditional-simulation argument "P=NP => R simulates all decider-induced systems" that does not require provable correctness; otherwise the bridge reduces to the open optimal-proof-system question.
