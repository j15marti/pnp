# Worst-case derivation-cost living log (append-only)

Target: W_R(N) = max over UNSAT |F|<=N of min over derivations cost_R; weakest bridge SAT in P => W_R(N) <= poly(N). P vs NP remains OPEN.

## 2026-11-05 CLAUDE BRIDGE-DICHOTOMY-0001
- Bridge is equivalent to SAT not in P for any R with a proved lower bound (Resolution etc.), so only meaningful for Frege/EF-strength R.
- Sufficient condition for EF: poly-size EF proofs of formalized correctness of a poly-time SAT algorithm.
- Literature: no new unconditional EF lower bound found (2026); PAP for EF NP-complete (arXiv 2506.16956); CCC 2026 constructive-lower-bound paper to audit.
- Report: research/agents/claude/2026-11-05_CLAUDE_BRIDGE-DICHOTOMY-0001.tex
- Open for next run: red-team feasible provability of SAT-algorithm correctness; price in bits/space.
