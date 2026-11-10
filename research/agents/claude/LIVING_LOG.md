# Claude routine — living log (worst-case derivation directive)

Append-only. Newest entry at the bottom. Status labels follow AGENTS.md.

## 2026-11-10 11:51 PST — WORSTCASE-BRIDGE-0001
- Report: `2026-11-10_1151_CLAUDE_WORSTCASE-BRIDGE-0001.tex`; code and data: `worstcase-bridge/`.
- PROVED/EXACT, elementary (bridge-collapse dichotomy): for any proof system R with a known superpolynomial lower bound (Res, CP, PC, bounded-depth Frege), the bridge SAT∈P ⟹ W̄_R ≤ poly is equivalent to P≠NP. For R that p-simulates EF, such as R_mix341, proving the lower bound is at least as hard as proving an EF lower bound.
- KNOWN chain: a superpolynomial W̄_{R_mix341} implies that PV does not prove P=NP (Cook translation plus Cook–Krajíček). This is a milestone, but it is not P≠NP.
- Scope of the free-best-sequence principle: it is a sound lower bound only for algorithms whose runs convert into R-proofs, such as DPLL and CDCL. For arbitrary algorithms, that conversion is the bridge itself.
- COMPUTATIONAL: exact minimum tree-like Res sizes are 5, 21 and 85 for PHP^2_1, PHP^3_2 and PHP^4_3. These are a sanity baseline only.
- Duplicates adopted: the oracle barrier (LSPV-1/360), the conditional PV→EF bridge (LSPV-1/357), and the MUS quotient (LSPV-1/350).
- Next target: identify a candidate EF-strength hard family. Random 3-CNF is the only family listed that survives Res, CP and PC. Test whether the R_mix341 DEF rule shortens tiny random-UNSAT refutations compared with plain Res. This needs an exact DAG-size solver (OPEN).
- P versus NP: OPEN.
