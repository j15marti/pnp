# LSPV-3/591: Native /341 BigInt affine-mask array fiber

**November 12, 2026, 08:27 PST | Hypergraph & Proof Certificates | Historical Route B.**

**Status: PROVED/RESTRICTED source-inspection theorem + COMPUTATIONAL original-checker hosted-V8 replay. P versus NP OPEN.**

Affected IDs: P2-D1, P2-C3 (restricted original-parser authentication only); P2-B1, separate P2-B2/B3 OPEN. This is NOT the complete historical R_mix341 grammar.

## Candidate and advance falsifiers

Candidate: each of the seven row.mask fields in an originally accepted odd-K4 /341 native proof admits an independent replacement from a hexadecimal JSON string to a singleton JSON array whose sole integer element has the same BigInt value. All 128 choices must be original-checker-accepted and preserve the exact paid proof cost W=15.

F1: a value-equal singleton array is rejected in an AND3, XOR or terminal row. F2: simultaneous choices interfere or alter original signed source or parent identity. F3: value-equal substitution changes fixed paid work. F4: invalid arrays, wrong source and missing parents are nevertheless accepted. None occurred in the native experiments.

## Authenticated checker and source identities

Original unchanged checker path: experiments/arc/lspv2_341_independent_verify.js, Git blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0. Original seven-fixture source packet: results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json, blob fe27fe1011d0021e721ccaeb747ed58da65d7464. The selected first K4 fixture has 16 original signed SOURCE clauses, 12 paid AND3 inference records and three paid XOR inference records; all original parents, signed clauses, charges, graph edges, tables, row right-hand sides, and terminal contradiction are unchanged.

Exact independently published all-array accepted certificate: results/raw/arc/2026-11-12_0827_LSPV3_591_NATIVE341_ALL_SEVEN_ARRAY_MASKS_ACCEPTED.json, blob 7b0fcf29e5bd997a294aef0b63110f56d651f995, 3,382 ASCII bytes. Original-Node OS replayer path: experiments/arc/lspv3_591_native341_bigint_mask_types.cjs, blob 61b1a30c212b4a1cdfbbac7ce6f65434da0e7127. Full hosted original-code 156-case outcomes: results/raw/arc/2026-11-12_0827_LSPV3_591_BIGINT_MASK_TYPE_HOSTED_RAW.json.

## Theorem 591.1: 128 accepted byte encodings of one identical native paid proof

The seven row.mask fields, in chronological order, have the following original-hex to alternative-singleton-JSON-array mappings:

| Inference | Original mask | Accepted alternative |
|---|---|---|
| d2 | hex 0x7 | [7] |
| d5 | hex 0x19 | [25] |
| d8 | hex 0x2a | [42] |
| d11 | hex 0x34 | [52] |
| d12 | hex 0x1e | [30] |
| d13 | hex 0x34 | [52] |
| d14 (terminal) | hex 0x0 | [0] |

For every subset S of the seven row positions, independently replace precisely those hexadecimal string masks by the displayed JSON arrays. After JSON serialization and parsing, the unchanged archived checker accepts the resulting first-fixture packet, all signed source occurrences and proof-DAG parent indices/identities remain the same, and the paid cost is W=15. The 128 encodings are pairwise byte-distinct, not 128 distinct semantic proofs.

**Proof.** The original verifier applies JavaScript BigInt conversion to the row masks in affine-annotation checks, GF(2) elimination, and the final empty-affine-sink check. It never checks the raw JSON mask type or compares a raw mask to its original hexadecimal string before this conversion. BigInt of each original string and each proposed singleton array equals the same integer. Therefore every relevant branch, table computation, row-value check and output is unchanged. All non-mask fields are identical, and no additional paid node was inserted. The 128 branch choices differ in the byte spelling of at least one fixed field, establishing pairwise byte distinction. For this fixed original checker, all 128 original-code replay tests additionally passed, including the checker’s own five negative controls per test. QED within the specified original implementation. No semantic generalization to the historical full calculus is asserted.

## Concrete replay, parser type distinction, hostile controls

128 of 128 possible mask-subset packets ACCEPTED in hosted V8 using the exact unchanged original checker function body, replacing ONLY its fs.readFileSync input, process.argv, and console.log adapters. Every trial underwent JSON serialization. Each accepted packet passed 1,401 original checker assertion groups, including the five original bundled negative controls. Total 179,328 positive assertion groups and 640 built-in negative controls. The all-seven-array accepted packet is 3,382 bytes versus 3,396 bytes for the original one-fixture packet. All retain W=15.

Six of six hostile packets REJECTED with exact errors: duplicate mask array [7,7] produced SyntaxError (BigInt conversion); terminal null produced TypeError; wrong final RHS produced bad GF2 elimination; missing AND3 parent produced missing antecedent; forged source literal 999 produced signed incidence mismatch; substituting opcode LOCAL-CONVERT produced unknown rule.

22 additional type-differential cases were tested, with 13 accepted and nine rejected, totaling 18,213 additional original-checker assertion groups for accepted cases. In particular terminal masks false, empty string, empty array, [0] and ["0"] were accepted, whereas null, true, [0,0], empty object, and integer 1 were rejected. At d2, numeric 7, [7], ["0x7"], [[7]] and a whitespace-padded decimal string were accepted; [6], [7,7] and [] were rejected. At d12, integer 30 and [30] were accepted, but [31] was rejected.

**Execution provenance:** These 156 tests ran the unchanged original verifier in hosted V8 with input/output adapters, NOT in actual OS Node subprocesses. The separate complete Node operating-system replayer is published and pinned for fresh checkout, but was not independently OS-executed in this run. Its presence must not be counted as a second independent checker execution. Repository-wide preflight, tests and TeX compilation were not executed in the hosted runtime.

## P2-C3 abstract interpretation and CEGAR consequence

For this restricted checker, parsed mask type must either be retained or abstracted through the checked successful BigInt conversion relation; a blanket prohibition on JSON-array masks is invalid and would exclude genuine accepted certificates. Ill-formed [7,7] is a concrete rejected counterexample to an overbroad abstraction permitting any array with a first element of seven; it may be removed only by a sound parser-conversion refinement. Unknown historical native operations must remain MAY, even when the archived subset rejects the string LOCAL-CONVERT.

A complete concrete state for the eventual P2-C3 proof must still retain all original-source binding, signed clauses, evidence provenance, paid-node identities, definitions and facet owners, fresh global wires, typed parent views, active/discharged branch contexts, entire shared proof DAG and exported/private interfaces. This run supplies **only** the restricted row-mask conversion distinction. Logical W=15, certificate bytes, actual checker runtime, span and peak memory are separate resources; the 128-packet fiber does not establish a proof-work lower bound.

## Corpus and external source audit

Reviewed both root proof trackers (proof1.txt SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343; proof2.txt SHA ba4d1c0faf9acbce836ffc5e16740b197e4c7bbe), issue #3, AGENTS.md, CODEX.md, the pnp-research skill, original checkers, material LSPV-3/539-549 and /550-590, peer LSPV-2/539/549/552/576, LSPV-1/586/592, LSPV-4/563, LSPV-5/505, Grok 2026-11-12_0917 and Claude ONETAPE. Prior LSPV-3/550 concerns literal coercion, /590 concerns identifier types, LSPV-5/414 concerns ghost affine mask bits, and /500 concerns support-string malformed shapes. This exact seven-site native BigInt array mask fiber was not found in the reviewed corpus. No novelty beyond this implementation claim is asserted.

Primary language semantics: ECMAScript BigInt constructor https://tc39.es/ecma262/#sec-bigint-constructor and https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/BigInt/BigInt . Methodological primary references: Cook and Reckhow, JSL 44 (1979), DOI 10.2307/2273702; Cousot and Cousot, POPL 1977, DOI 10.1145/512950.512973; Clarke et al., CAV 2000, DOI 10.1007/10722167_15. External proof formats FRAT-XOR/XLRUP do not authenticate the missing native mixed-rule grammar.

No relativization, algebrization, Natural Proofs or B3 transfer barrier is overcome. Independent padding, branching, extension, learning, Resolution, Gaussian elimination and compact-circuit alternatives remain available. This native accepted-byte result is not a full-calculus lower bound.

**TRACKERS REVIEWED; NO MATERIAL CHANGE** to root proof1.txt or proof2.txt. No agent identities, schedules, weights, ownership boundaries or two Route A / three Route B labels changed. No automation operations were performed.

**Next load-bearing target:** locate a single original, externally source-bound historical R_mix341 implementation and exhibit one genuinely accepted cross-rule RES-to-AND3 or DEF-facet-to-LOCAL-CONVERT byte record with hostile near misses. P2-D1, P2-C3, P2-B1, separate P2-B2/B3 and P versus NP remain OPEN.
