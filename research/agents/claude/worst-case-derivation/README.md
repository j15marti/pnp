# Exact worst-case minimum DAG-resolution cost on few variables (WBAR-0001)
- `wbar_exact.py n [k K]`: enumerates MU formulas on n variables, reduces them up to renaming and sign flips, and finds the exact minimum refutation cost per class (BFS with subsumption pruning). Writes `wbar_n{n}_chunk{k}of{K}.json`.
- `small_m_n4.py M`: does the same for all MU formulas over ≤4 variables with ≤M clauses (M=5 took 46 s).
- `verify_independent.py files...`: independent re-check that shares no code with the producer. It brute-forces UNSAT and MU, checks each proof, and runs an unpruned search to confirm that no proof with W−1 derived clauses exists.
Report: `../2026-11-11_0348_CLAUDE_WBAR-0001.tex`. Log: `LIVING_LOG.md`.
