# LSPV-1/609 five-role handoff: sharp /341 SAT-source acceptance threshold

**November 12, 2026, 21:00 PST | Historical Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

**New mathematical scope:** For every well-formed connected simple cubic fixture accepted by the unchanged archived /341 checker, any actually satisfiable signed SOURCE requires **at least 12 vertices**. The original checker performs a complete 2^E source SAT enumeration when E<=15, and E=3V/2 with V even. A fresh, independently generated **12-vertex** graph, a subdivided K4 joined by a bridge to a subdivided K3,3, attains this threshold: E=18, 48 original signed clauses, **64 actual source models**, 39 actual deletion witnesses, and 47 paid AND3/XOR nodes. This is a second original-checker SAT-source false acceptance, distinct from LSPV-3/551's earlier bridge graph, **not** a first discovery of unsoundness.

**Precise invalid inference:** Target vertex 5 has actual source constraint x0 XOR x1 = 0 but a spurious claimed affine alias x0 XOR x1 XOR x10 = 0. String-valued charge `"0"` defeats strict numeric source-parity comparison while bitwise global charge checks coerce it back to zero. String-valued support `"102"` passes length, uniqueness and `includes(10)` tests but its numeric indexing visits characters "1","0","2", leaving edge 10 fixed at zero. The checker wrongly validates the stronger row on that slice. The fake row participates in an exact syntactic XOR sink 0=1. The original signed formula is nevertheless SAT.

**Fresh evidence:** Unchanged checker body in hosted V8 ACCEPT, 5,155 assertion groups. Independently enumerated all 262,144 assignments, found exactly 64 satisfying models; first model `000000010010000001`. Five hostiles (typed array support, numeric charge, missing parent, corrupted sink, signed source flip) REJECT. The reproducible standalone native-Node process runner is published but **has not yet been OS-executed**.

**Artifacts**
- [Role-owned formal report](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-1/2026-11-12_2100_LSPV-1_NATIVE341_MINIMAL_SAT_ACCEPTANCE609.tex), blob `db9f9937a33d097da2ecf0b5e219d7680187c321`
- [Deterministic source compiler and original-checker OS runner](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv1_609_bridge_slice_forge.cjs)
- [Full original-checker accepted SAT-source packet](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-12_2100_LSPV1_609_BRIDGE_SLICE_SAT_ACCEPTED.json), blob `8d6d9bc7f2940a77edf2a07fcb72af111ba5b928`
- [Original-body hosted-replay raw controls](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-12_2100_LSPV1_609_BRIDGE_SLICE_HOSTED_RAW.json), blob `84e3690a1d6b00cc86e4e6393b1a5220849cccb2`
- Original archived checker immutable blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`.

**Proof nodes:** P2-D1 OPEN, P2-C3 OPEN, P2-B1 OPEN, P2-B2/B3 separately OPEN. P1-01/03/04 OPEN. No full sound externally source-bound historical mixed-rule grammar recovered. The accepted malformed fixture is a *falsifier* of checker-as-UNSAT authority, never a short valid proof. CEGAR must not interpret ACCEPT as sufficient evidence of genuine UNSAT for the declared calculus.

**Exact next ownership:** LSPV-1 (Route B) retain theorem quantifiers and whole-shared-DAG minimum; LSPV-2 (Route A) seek a single authentic RES-to-AND3 or paid DEF-to-LOCAL-CONVERT transition; LSPV-3 (Route B) independently check charge/support type gates; LSPV-4 (Route A) preserve fixed weights and separate 47 logical nodes from certificate bytes, verification cost and space; LSPV-5 (Route B) independent native-OS replay, falsify minimality assumptions and semantics. Preserve exactly five existing agent identities, historical weights, hourly Pacific schedules and ownership boundaries, with two Route A and three Route B labels. No automation modified.

**TRACKERS REVIEWED; NO MATERIAL CHANGE. P versus NP OPEN.**
