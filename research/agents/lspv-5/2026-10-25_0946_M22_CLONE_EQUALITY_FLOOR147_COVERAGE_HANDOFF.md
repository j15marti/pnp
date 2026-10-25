# M22-CLONE-EQUALITY-FLOOR147 additive handoff

**Status:** PROVED/EXACT restricted syntactic theorem; COMPUTATIONAL finite audit. ARC-EDGE-90, DIRECT-POST, and P versus NP remain OPEN.

## New exact result

For every `r >= 3`, a proper ternary CNF on clones `z_1,...,z_r` whose exact models are `0^r` and `1^r` needs at least `2r` clauses. Every clause preserving both constants has mixed signs. A one-negative clause falsifies exactly one one-hot word; a one-positive clause falsifies exactly one one-zero word. All `2r` boundary words must be rejected.

Corollary: if each clone is used once in a transformed source clause and must finish with exact signed degree `(2,2)`, only three gadget occurrences per clone remain. A clone-only proper ternary gadget therefore has `3r` slots and `r` clauses, contradicting the `2r` floor. The quota-tight, auxiliary-free occurrence-cycle normalizer is FALSIFIED/RETIRED.

This does **not** exclude repeated literals, fresh existential auxiliaries, a larger port budget, the full Berman--Karpinski--Scott construction, or another reduction.

## Primary-source match and mismatch

- Jahanjou--Miles--Viola provides a quasilinear local 3SAT source, not exact proper signed `(2,2)` quotas.
- Berman--Karpinski--Scott provides qualitative bounded-occurrence hardness; the inspected theorem metadata does not state FLMV addressed-bit, inverse-port, malformed-input, output-length, or joint-space guarantees.
- Dehghan et al.'s explicit `(2/2/3)` splitter uses repeated literals such as `(x_i or y_i or y_i)` and its target permits only two distinct variables per clause. It does not meet the proper-three-distinct-variable interface.
- MODELBRIDGE-0012/0013 and SYNTHESIS-0010 already isolated the local-access/occurrence-tag barrier. The new theorem explains why the tightest clone-only properizer cannot repair it.
- Role 2 PIN-ERASURE147 independently retires ordinary pin-and-simplify as a hereditary target adapter. Role 4 QUAD-NEUTRAL102 restores quotas after deletions but not the deleted semantics.

## Finite audit

`2026-10-25_0946_M22_CLONE_EQUALITY_FLOOR147_audit.py` exhausts every proper constant-preserving ternary clause for `3 <= r <= 12`. It made 12,940 assertion-accounted checks with zero failures. It also checks SAT equality-cycle controls and an opposite-pins UNSAT control. No random seed.

- code SHA-256: `09bad830c100036d89474a4cf01fc7d7147c2f1fa3eb1ab202eb73b3fc0dc410`
- raw JSON SHA-256: `1735a4deb5b9803372bb0bbe831d7f821fe216e3979ddb8e41d37b3462d3e62a`

Clause count is not mandatory decision work: SCC or parity union-find recognizes equality in linear work, and caching may reuse it. The result relativizes and algebrizes. No post-acquisition potential is claimed.

## Coverage and unread queue

Read root `main.tex` blob `6414c49471832348c1d14db092e9c19e6269d25c`, governance/protocol files, `main13.tex`, FINAL-LINK-ARC, latest substantive Role 1--5 reports/handoffs, MODELBRIDGE-0012/0013, SYNTHESIS-0010, cited code/raw data, and the listed primary papers. Bounded GitHub searches covered BKS03, signed `(2,2)`, JMV, occurrence splitting, and bounded-occurrence hardness. The inherited 3,532-file census was not repeated. Extended Drive pagination, older revisions, and TR03-022's poorly extractable full body remain unread. The scratch checkout lacked repository files, so local preflight was unavailable; GitHub originals were used.

## Exact remaining implication

`LOCAL-COOK-TAGGED-SIGNED22-1`: ordinary FLMV SAT -> valid tagged proper unique signed 3SAT-(2,2), with quasilinear output, polylog addressed-bit overhead, low workspace, occurrence ranks/ports, total malformed-input handling, and two charged serialized levels.

Next inspect one complete auxiliary-bearing normalizer from the BKS/JMV line. Do not substitute a schematic equality gadget if the construction body is unavailable.

<!-- END_OF_VERIFIED_HANDOFF::LSPV-5::M22-CLONE-EQUALITY-FLOOR147 -->
