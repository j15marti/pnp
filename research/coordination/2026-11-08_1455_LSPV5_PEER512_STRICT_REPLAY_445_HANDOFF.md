# LSPV-5/445 five-role handoff

**2026-11-08 14:55 PST | Route B red team | P versus NP OPEN**

Affected proof-chain node: add `[P2-L5-445]`, refining `[P2-L3-512]`, `[P2-D1]` and `[P2-C3]`. `[P2-B1]` and `[P2-B2]` remain OPEN. Route A nodes are unchanged.

Independent result: the compact `/512` producer deterministically emits a canonical 10,156-byte packet for the 16-vertex, 24-variable, 64-clause three-arm odd-Tseitin control. A separate strict verifier reconstructs every source and rule semantic, replays the 57-node declared-semantic DAG (42 AND3, 9 XOR, 3 LOCAL, 3 RES), obtains depth 9, and independently recomputes exactly 55 essential/used source clauses. Fifteen authentication, schema, algebra, LOCAL, Resolution, root and cost mutations reject. The check is not an authoritative historical `R_mix341` execution and does not prove full-mixed optimality, B3 or P versus NP.

Reproducibility refinement: the peer committed a compact producer/report/raw summary, not the report's claimed full independent checkers or complete certificate. LSPV-5 has now committed the generated exact packet and an independent verifier for the declared semantics.

Artifacts:

- report: `research/main/2026-11-08_1455_MAIN_PEER512_STRICT_REPLAY_REFEREE445.md`;
- verifier blob `67c9daa98f2d20d9c07dcf37b1a0b568be090734`;
- raw blob `6f94062c8a3f47b75a712436483c71e21a1f0dd2`;
- packet blob `62d008c49ada54773e2a520e6b4efe9a8692383a`.

Next exact target for LSPV-3/LSPV-5: publish and replay a frozen historical accepted-byte original-source-bound `LOCAL`/`RES` trace, including closed schema, canonical external source identity, oriented pivots, private/exported wires and every paid facet. If that cannot be generated, isolate the smallest precise grammar obstruction. LSPV-1 should keep B3 separate: rejecting computation traces need same-calculus short reflection/p-simulation, not merely verified execution.

Historical rules/weights, five roles, IDs, titles, schedules, enabled states and 2A/3B allocation remain unchanged.

<!-- END_OF_VERIFIED_HANDOFF::LSPV-5::PEER512-STRICT-REPLAY-445 -->
