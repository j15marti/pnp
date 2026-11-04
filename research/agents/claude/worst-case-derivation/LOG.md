# Living log: worst-case derivation cost W_R(N) (shared five-agent directive)
Entries are append-only, newest last. Status: P vs NP OPEN.

## 2026-11-04 WORSTCASE-0001 (Claude)
- Report: `2026-11-04_WORSTCASE-0001.tex`; code `min_res_dag.py`; data `min_res_dag_results.json`.
- PROVED: for R with a known superpolynomial lower bound (Resolution etc.), bridge B(R) is equivalent to SAT not in P — circular, no content.
- PROVED: for optimal R, W_R poly iff NP=coNP; the free-strategy program is exactly NP vs coNP (stronger than P vs NP).
- KNOWN: EF poly under P=NP if M's soundness is PV-provable; unprovable correctness is the open gap.
- Dichotomy: the chosen system must be >= EF-like for the bridge to be non-circular, but then no lower bound techniques exist.
- Computation: exact min DAG-Res sizes (Tseitin C3=5, C4=7); PHP_3_2 not certified within budget.
- Literature clues: Davis-Robere Res(log) (ECCC TR26-055), PAP NP-complete for EF (FOCS 2025), semantic tree-like Frege (arXiv 2604.28172).
- Next: place the multisign DAG-hypergraph system in the simulation order; SAT-encode proof-size search for PHP.
