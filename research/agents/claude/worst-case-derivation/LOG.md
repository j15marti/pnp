# Living log: worst-case minimum derivation cost W̄_R(N)

Target: W̄_R(N) = max over UNSAT F with |F| ≤ N of min over R-refutations π of cost_R(π).
Bridge B_R: SAT ∈ P ⇒ W̄_R(N) ≤ poly(N). P versus NP remains OPEN.

## 2026-11-14 — WR-BRIDGE-0001
- PROVED/EXACT: for any R with a known superpoly lower bound (Res, CP, PC, AC0-Frege), B_R ⇔ P ≠ NP. The bridge is a reformulation there, not progress.
- PROVED/EXACT (from KNOWN THEOREMS): B_R holds iff R p-simulates P_A for every correct poly-time SAT decider A. For R extending Frege, this means short R-proofs of A's soundness/reflection formulas.
- KNOWN THEOREM transfer: if PV proves A sound, then EF is polynomially bounded on refutations. So an EF lower bound gives only "no poly-time SAT decider is provably sound in PV". The gap to P ≠ NP is the unprovably-correct decider. Status: OPEN.
- COMPUTATIONAL: exact minimum tree-like resolution sizes for PHP (5, 21, 85) and Tseitin (55, 151, 255). Gaussian elimination refutes the same Tseitin formulas in V−1 row operations, so a Tseitin family hard for resolution is easy for algebra (hostile control).
- Next: find the weakest theory whose provable soundness follows from correctness, or a correct decider with unprovable soundness.
- Files: `2026-11-14_CLAUDE_WR-BRIDGE-0001.tex`, `wr_tree_exact.py`, `wr_tree_exact_results.json`.
