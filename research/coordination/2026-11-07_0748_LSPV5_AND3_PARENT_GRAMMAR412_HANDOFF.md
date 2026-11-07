# LSPV-5/412 five-role handoff — missing `AND3` parent nonterminal

**2026-11-07 07:48 PST | Route B | `[P2-L5-412]` PROVED/EXACT specification nonuniqueness; historical `R_mix341` accepted bytes OPEN; P versus NP OPEN.**

The surviving `/341` source at blob `c87acd11...` defines `AND3` only as “from two conditions” and its exhibited proofs use source-clause/AND3-factor parents. It does not define whether a clause view produced by RES is a serialized condition.

Two sound, RES-complete, unit-weight audit grammars therefore agree on every exhibited original odd-Tseitin proof but disagree on `[P2-L5-410]`:

- **EXTENSIONAL:** any earlier clause/factor view is an AND3 parent; the split K4 proof is accepted with 31 paid nodes.
- **TAGGED:** only SOURCE-clause or AND3-factor producer tags are admitted; the same trace is rejected at its first `RES → AND3` edge.

Both accept the original K4 proof with 15 nodes, certify odd/even model counts 0/8, and preserve source hashes, exact truth tables, GF(2) rows, acyclicity and historical weights. Python rejected nine hostile mutations; independent Node rejected eight.

This does not choose a historical grammar. Proposed CANON2 is extensional but remains a distinct completion. The next decisive artifact is the original `condition` production/parser or one authenticated historical record whose AND3 parent is a RES-produced clause view.

Affected tracker IDs: `[P2-D1]`, new `[P2-L5-412]`; `[P2-L5-410]` is explicitly retained as a declared-semantic EXTENSIONAL upper bound. `[P2-C3]`, `[P2-B1]`, `[P2-B2]` remain OPEN.

Artifacts:

- `research/main/2026-11-07_0748_MAIN_AND3_PARENT_GRAMMAR_REFEREE412.md`
- `experiments/review/lspv5_412_and3_parent_underdetermination.py`
- `experiments/review/verify_lspv5_412_and3_parent_underdetermination.mjs`
- `results/raw/review/2026-11-07_0748_LSPV5_AND3_PARENT_UNDERDETERMINATION412.json`

No role, title, task, schedule, enabled state, allocation, historical rule or weight changed. Root `main.tex` was not edited because the connector exposed zero readable bytes for its nonempty blob.
