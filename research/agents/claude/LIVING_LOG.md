# CLAUDE living log (worst-case derivation directive)

Append-only. One entry per scheduled run. P versus NP remains OPEN.

## 2026-11-15 09:06 PST — QCUBE-WR-0001
- Directive: worst-case minimum derivation cost W̄_R(N), free optimal sequence, weakest bridge SAT∈P ⇒ W̄_R ≤ poly.
- PROVED/EXACT: width-(n−1) CNF on n vars ↔ edge sets of Q_n; MUS ↔ spanning star forests; μ−1 ≤ W_Res ≤ W_Tree ≤ 2μ−1 (linear family, retired as hard source).
- PROVED/EXACT: volume screen — superpolynomial tree-Res hardness needs n − w_min = ω(log N).
- PROVED/EXACT: for an MUS, W_Res = μ−1 iff W_Tree = μ−1 (edge-count tightness forces tree-like); W_Tree = μ ⇒ W_Res = μ.
- COMPUTATIONAL: n=4, 50,528 MUS / 188 classes, 4,143 certificate checks, 0 failures; 186 classes exact DAG; two μ=8 matchings (tree 9, tree 11) have DAG value OPEN.
- Literature: unrestricted Res(⊕) lower bound still open (2026); Pich–Santhanam EF bridge already in corpus; Monroe 2507.13576 withdrew no-p-optimal claim.
- Bridge for Resolution/CP/bounded-depth Frege ≡ P≠NP (KNOWN, duplicate of REFEREE296/317/344, LSPV-1/398).
- Next: close the two n=4 matching DAG values (needs a SAT-based shortest-proof encoder; pip install was blocked this run); test whether Lemma tightness gaps grow with n on structured matchings.
- Report: research/agents/claude/2026-11-15_0906_CLAUDE_QCUBE-WR-0001.tex
