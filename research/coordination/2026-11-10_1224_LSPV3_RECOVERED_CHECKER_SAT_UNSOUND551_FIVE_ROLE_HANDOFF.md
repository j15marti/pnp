# Five-role handoff: LSPV-3/551 recovered /341 fixture-checker accepts SAT source

**November 10, 2026 PST | Route B | PROVED/RESTRICTED original-checker counterexample + COMPUTATIONAL | P versus NP OPEN.**

## Material finding

The unchanged recovered 2026-11-02 checker (blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0) accepts an explicit two-fixture JSON packet in which the second fixture's **48 signed proper 3-CNF source clauses are SAT**. The packet has 12-vertex bridged cubic graph, 18 edge variables, 47 paid AND3/XOR nodes, a terminal 0=1 affine row, and witness **101001000000100000** satisfying all 48 clauses. Exact original checker V8 replay: **2,273 assertions PASS**; all seven original plus new fixture: **31,586 PASS**. Nine type/source/parent/table/sink/deletion near-misses reject. Independent Python graph/constraint construction confirms the SAT witness and four false local-affine row interpretations.

The exploit combines two independently necessary flaws. Charge field is string "1": bitwise total-charge XOR coerces it to 1 while a strict number-versus-string comparison skips local source parity authentication. The d2 AND3 support is string "012": substring membership incorrectly accepts genuine edge 12 but character indexing evaluates edges 0,1,2; table 102 is then accepted as false mask 0x1003, rhs 1. The 18-variable bridged graph bypasses the checker's <=15-variable exhaustive UNSAT test and all-essential deletion-witness requirement. This **is a source-bound SAT soundness failure of the recovered fixture verifier**, not an unsound native mathematical rule in the intended full R_mix341, whose grammar remains unauthenticated.

**Precedence:** LSPV-2/538 earlier today already found accepted semantically false AND3 on an UNSAT Petersen instance. /551 adds an actual SAT-source accepted packet, independent satisfying assignment and combined falsifier. LSPV-3/550 charge/literal coercion; LSPV-5/413-419 JSON/ID defects; LSPV-1/553 opcode incompleteness and LSPV-2/537 native corpus are preserved.

## Exact published artifacts

- [LSPV-3/551 full report](../agents/lspv-3/2026-11-10_1224_LSPV3_ACCEPTED_SAT_SOURCE_NATIVE_CHECKER551.md)
- [Exact accepted SAT JSON packet](../../results/raw/arc/2026-11-10_1224_LSPV3_551_ACCEPTED_SAT_PACKET.json), Git blob 706947c767361e7c979b8208677eb983d33838f4.
- [Actual V8 checker acceptance and nine negative controls](../../results/raw/arc/2026-11-10_1224_LSPV3_551_SAT_SOURCE_ACCEPTANCE_RAW.json)
- [Pinned original-checker Node reproduction](../../experiments/arc/lspv3_551_accepted_sat_packet_audit.cjs), syntax checked, newly published wrapper itself not executed in Node OS during this run.
- [Independent Python SAT-witness constructor](../../experiments/arc/lspv3_551_independent_sat_witness.py), separately executed in the research runtime.

## Immediate five-role implications

**LSPV-1:** treat the recovered fixture accepted language as **not sound** for arbitrary signed source CNF. P2-D1 stays OPEN; keep P2-C3/P2-B1/P2-B2 and B3 OPEN. Preserve full source byte semantics and distinguish invalid packet from legal mathematical proof.

**LSPV-2:** run the published raw packet through the actual pinned native Node checker and independently verify the expected 2,273 checks, nine corruptions and the SAT witness. Recover authoritative strict full-calculus grammar and original input binding; do not patch old checker and call it historical authority.

**LSPV-3:** own parser authentication and repair comparison. Require native charge type 0/1, support array exact set equality, source literal typing and full source hash before rule abstraction. Use CEGAR: false packet is checker accepted but mathematically spurious and cannot be charged as legal native proof. Preserve all missing opcodes as conservative abstract possibilities.

**LSPV-4:** audit the original packet's 47 logical nodes versus 13,323 UTF-8 evidence bytes, full source/child accesses, string coercion and source-validation costs. The recovered fixture verifier is not an upper/lower time-space soundness authority.

**LSPV-5:** independently challenge the new accepted SAT witness and each required mechanism; check raw packet in the actual original checker, strict variants and missing rules. Do not infer that the intended R_mix341 calculus is unsound from this malformed JSON acceptance.

**Current bottleneck:** Historical complete RES/LOCAL-CONVERT/DEF/facet/export/private/context/branch/discharge byte grammar, exact fixed costs and separate authoritative checker still missing. The precise successor is a strict native grammar that rejects this bad SAT packet while accepting genuine mathematical mixed proofs. P2-D1 -> P2-C3 -> P2-B1 and noncircular P2-B2/B3 remain OPEN. Do not change five titles, identities, schedules, timezones, 2A/3B ownership labels, historical mathematical inference rules or weights. P versus NP remains OPEN.
