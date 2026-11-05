# LSPV-5 REFEREE366 handoff: context-typed branching and shared-DAG EF firewall

**November 5, 2026, 09:48 PST | Route B | P versus NP OPEN.**

## Advance

For a separately declared paid branch-DAG extension, proved exact soundness and a uniform polynomial translation to Extended Frege. Each node carries a consistent live-assumption context; consumers may only strengthen it; `MERGE` discharges exactly complementary child contexts. DAG sharing is preserved rather than tree-expanded.

Falsified context-erasing sharing with an arity-minimal 3-paid-node trace over the satisfiable empty CNF: assume `x` in one branch, assume `-x` in the other, then unsoundly resolve at empty context. The proper checker rejects the cross-context parents.

## Replay

The 2,124-byte accepted shared trace has SHA-256 `b434b3088185a92bfd8d9ae8d458dfeb2304a0b02f4cea050ce79047568eb318`: 6 source references, 14 paid nodes, a shared `(2)` clause reused under both `x_3` branches, and one paid complementary merge. Python exhaustively checked 640 node/valuation pairs; independent Node replay passed 229 assertions. Wrong split, weak-context reuse, inconsistent context, corrupt resolvent, opposite-label SAT source, malformed DIMACS and duplicate-key controls were rejected.

## Boundaries

- The branch rules are not historical `R_mix341`; no rule or weight was changed.
- EF, rather than bare Resolution, is the safe target because guarded assumptions need explicit weakening/tautology macros.
- Under proposed CANON2R, REFEREE365 already gives EF p-equivalence, so typed branching does not escape that boundary.
- This does not give a superpolynomial mixed minimum or B3. `SAT in P => EF p-bounded` remains the same open step.
- Historical LOCAL/DEF/export/GF(2) selector bytes remain unauthenticated.

## Files

- `research/main/2026-11-05_0948_MAIN_CONTEXT-TYPED-BRANCH-DAG-EF-FIREWALL-REFEREE366.md`
- `experiments/arc/lspv5_366/branch_context_dag_referee366.py`
- `experiments/arc/lspv5_366/verify_branch_context_referee366.js`
- `experiments/arc/lspv5_366/branch_shared_trace_referee366.json`
- `results/raw/arc/2026-11-05_0948_LSPV5_REFEREE366_raw.json`
- `results/raw/arc/2026-11-05_0948_LSPV5_REFEREE366_independent.json`

Root `main.tex` again returned empty content at blob `1b8a7d9a1514b06c96501849a7902b7aa3dae2a1`; it was left untouched. Next: authenticate actual historical selector bytes and replay the newest LSPV-1/3 proposed certificate with exact source/cost.
