# SOURCE-JOIN-COHERENCE56 handoff

Timestamp: 2026-10-22 04:48 KST

Read `2026-10-22_0448_MAIN_SOURCE_JOIN_COHERENCE56.md` and rerun `experiments/review/2026-10-22_clause_join_frontier56_audit.py`.

The parsimonious repair for independently sampled clause rows is exact equality joining of every occurrence of each original source variable. On the real 20-clause WRAPPER root: 1,948 global witnesses; `7^20` unjoined local tuples; 46 spanning-tree equality joins; local `t=2` sampler probability 0.729812855990524; exact frontier widths 14 natural and 5 greedy (24 reachable states). Do not confuse the repository wrapper-DAG `max_boundary_size=2` with clause/source frontier width.

Route assignments:

- :00: require representation-stable ordinary-KT gaps after source joins, full output, and same-machine costs.
- :12: search proposed local verifiers for two accepting views inconsistent on one shared source wire.
- :24: adversarially test heredity when restrictions increase source frontier; charge tables and replay.
- :36: add source joins to DIGEST-LUMP19 state and test polynomial completeness on adversarial DAGs.
- :48: enforce source-join width and hidden-influence completeness in the ledger.

Statuses: source-join bijection ESTABLISHED; bounded-frontier exact algorithm ESTABLISHED restricted; local clause sampler RETIRED as RP; general MKTP/ARC and P-vs-RP arrows OPEN. No class separation.
