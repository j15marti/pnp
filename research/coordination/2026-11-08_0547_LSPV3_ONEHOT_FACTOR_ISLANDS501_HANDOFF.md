# LSPV-3/501 | Five-role handoff | 2026-11-08 05:47 PST

**Material [P2-L3-501]: PROVED/RESTRICTED typed factor-island obstruction.** Historical [P2-D1], [P2-C3], [P2-B1] and [P2-B2] remain OPEN; companion [P1-01], [P1-03], [P1-04] unchanged.

Exact original one-hot q=2 cubic Tseitin source (Pang arXiv:2610.00837v2 §7.1): 3h original indicators, 7h original clauses, UNSAT for odd charge. In a DISTINCT generic-source SOURCE/AND3(exact <=3 original support)/exact affine alias/XOR fragment, all factors decompose into isolated vertex singleton factors and edge one-hot pairs. The only GF(2) rows are each edge's complement relation a_e0 XOR a_e1=1. Those rows have a common model, so no proof DAG in this fragment can refute the original source. Complete closure has 17h/2 distinct factors and 3h/2 nonconstant rows. Proof permits all shared DAGs and repeated parents, not just trees.

Independent Python and Node closures agree for 28 graph/charge cases; 16 K4 charge sources each exhaustively tested over 4096 indicator assignments; five hostile JS controls. This is a **structural necessity for an additional typed inference**, not a hardness lower bound in complete historical R_mix341. LSPV-3/495's explicit 13h-node RES/CAST3/AND3/XOR upper bound in a different calculus remains a required countercontrol.

Artifacts:
- research/agents/lspv-3/2026-11-08_0547_LSPV3_ONEHOT_FACTOR_ISLANDS501.md
- experiments/arc/lspv3_501_onehot_factor_islands.js
- results/raw/arc/2026-11-08_0547_LSPV3_501_ONEHOT_FACTOR_ISLANDS.json

LSPV-1/5 Route B: test a **native authenticated-byte** original-source-to-factor conversion and challenge this obstruction under all historically legal rules, particularly RES, DEF facets and LOCAL-CONVERT. LSPV-2/4 Route A: only cross-review actual resource accounting if relevant; keep primary Route A allocation. All five roles, weights, schedules and enabled states unchanged. P versus NP OPEN.
