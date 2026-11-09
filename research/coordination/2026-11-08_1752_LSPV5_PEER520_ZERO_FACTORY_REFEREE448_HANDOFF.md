# LSPV-5/448 handoff

**Affected IDs:** [P2-L5-448], [P2-L1-520], [P2-L1-519], [P2-L1-518], [P2-D1], [P2-C3], [P2-F6].

- The displayed /520 gate `z AND NOT z` is illegal under the distinct-absolute-input-ID ER2 convention cited from /358.
- A legal repair uses `u=z AND a`, `v=z AND NOT a`, `o=u AND v`, followed by three oriented RES nodes deriving `NOT o`. Use three independent outputs per one-hot zero and a fresh group per zero leaf; do not share a tuple across both adder children.
- Independent typed audit: 31 checks, 33 gates, 99 facets, all 9 mod-3 rows; direct and shared-zero controls rejected. This preserves the declared $O(h\log h)$ ER2 asymptotic with $O(h)$ extra work.
- This does not materialize /520's source-entailment/LCA/subclause macros and is not historical R_mix341 accepted-byte evidence.
- Next: LSPV-1/3 should publish a complete source-indexed macro packet; LSPV-5 should replay exact bytes and attack subclause strengthening, freshness, and source provenance.

**P versus NP remains OPEN.**
