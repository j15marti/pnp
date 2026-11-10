# LSPV-2/540: Native /341 JSON accepted-byte key shadow and lexical aliasing

**November 10, 2026, approximately 13:12 PST | SAT-Circuit Reduction Builder, historical Route A | PROVED/RESTRICTED JSON-parser lemma + COMPUTATIONAL checker replay | P versus NP OPEN**

## IDEA, four precommitted falsifiers

Candidate: The recovered historical /341 SOURCE/AND3/XOR **fixture** verifier uses JavaScript `JSON.parse` and therefore accepts raw UTF-8 certificates that contain *duplicate decoded keys*, even when the earlier value falsely claims a different original proof/source/parent. This creates an accepted-byte/source-binding hazard for a future native replayer. It does **not** authenticate the missing full mixed calculus.

F1: checker rejects duplicate JSON members; F2: checker distinguishes a Unicode-escaped key from its decoded equivalent; F3: checker requires canonical decimal literals and rejects equivalent exponent notation; F4: a first-key lexical reader and the actual checker select the same value despite duplicate conflicting keys. All four falsified by original-source replay and the explicit accepted/rejected direction controls.

## Source authentication and original exact checker

Original /341 producer `experiments/arc/lspv2_341_mixed_tseitin_min_dag.js`, Git blob `4081022e8a3841d79f751a3d3a7a10decbb026da`; historical fixture checker `experiments/arc/lspv2_341_independent_verify.js`, blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`. The new role-owned program is `experiments/arc/lspv2_540_json_shadow_native.cjs`, blob `568591d174e3f4ed527343643b84c54956cdf70e`. It pins both old Git blobs before executing their original bodies, and publishes a **separate** JSON lexical duplicate-key scanner. The scanner is NOT the native verifier, and is NOT a new accepted R_mix341 grammar.

Recovered full seven-fixture regression: **ACCEPT, 30,714 verifier checks**. One original K4 fixture: **16 strict signed source clauses, 15 paid AND3/XOR records, 3,396 UTF-8 bytes**, **ACCEPT, 1,401 verifier checks**. Source is internal to the historical fixture; a genuine independently supplied source-binding interface remains missing.

## Exact differential results

**14 deterministic packets, 10 accepted, 4 rejected.** Accepted ones include **four with duplicate object keys**: two top-level `fixtures` collisions (one using a Unicode-escaped first key), one `parents` collision, and one `literals` collision. Specifically:

| Packet | Original verifier | Byte observation |
| --- | --- | --- |
| Baseline K4 | ACCEPT 1,401 | 3,396 bytes |
| `ROOT_DUP_BAD_GOOD` | ACCEPT 1,401 | First `fixtures` has broken data, second has good fixture |
| `ROOT_DUP_GOOD_BAD` | REJECT | Exact converse order; last `fixtures` is broken |
| `ROOT_DUP_ESCAPED_BAD_GOOD` | ACCEPT 1,401 | `fixt\\u0075res` and `fixtures` decode to same key |
| `PARENT_DUP_BAD_GOOD` | ACCEPT 1,401 | First parents missing, last parents valid |
| `PARENT_DUP_GOOD_BAD` | REJECT | Reverse order fails ancestry validation |
| `SOURCE_DUP_BAD_GOOD` | ACCEPT 1,401 | First `literals` invalid, last literals valid |
| `ROOT_ESCAPED_KEY`, `SOURCE_ESCAPED_KEY`, `SOURCE_ESCAPED_ID` | ACCEPT | JSON escapes reconstruct same property/ID |
| `EXPONENT_LITERAL`, `WHITESPACE` | ACCEPT | Different raw bytes, same parsed proof |
| Two malformed JSON controls | REJECT | Trailing token and truncated final object |

The V8-replayed original verifier was unchanged apart from file/stdout adapters. Independently, Python `json.loads(..., object_pairs_hook=...)` reproduced decoded-key duplicate detection and last-key values on four matched lexical controls. The committed Node program includes actual SHA-256 hashing, but **no actual SHA-256 results were claimed from this V8 run**, which used a stubbed digest adapter solely to execute the audit; raw results exclude those fields. No full local Node checkout/preflight, historical all-rule checker, or FLMV machine execution is claimed.

## Theorem 540.1: raw-byte identity is not parsed-proof identity (PROVED/RESTRICTED)

Let `parse` be standard ECMAScript `JSON.parse`, and let `Check` be any deterministic consumer whose only access to certificate text is through its parsed value `parse(b)`. If a JSON object member `"k":v` is preceded by a syntactically valid earlier duplicate decoded key `"k":w` in the same object, then

$$
\operatorname{parse}(b_{w,v})=\operatorname{parse}(b_v)
$$

for the value of that member and all other unchanged parsed fields. Hence

$$
\operatorname{Check}(b_{w,v})=\operatorname{Check}(b_v).
$$

The earlier key can be spelled using JSON Unicode escapes that decode to the same string. The original checker meets the stated parser-only hypothesis as verified in its source. Raw byte strings, lengths and SHA-256 values can nevertheless differ. This proves a lexical equivalence class of accepted certificates, **not** a new inference rule or shortened mixed proof. A byte-only first-occurrence scanner may authenticate the wrong field, despite native checker acceptance of the last value.

## P2-C3 abstract transition and CEGAR guard

For the recovered subset, a concrete configuration must include both raw input bytes `b` and exact ECMAScript parsed value `p=parse(b)`, plus original signed source commitment, shared proof DAG, globally distinct paid IDs, and rule semantics. Let `alpha(b,D)` record the parsed semantic object and validated typed nodes, while retaining the raw digest/length *separately* for certificate size and provenance. The concretization contains **all** syntactic aliases with the same parsed value. All actual accepted checker's transitions remain represented at unchanged paid-node charges, including duplicate-key packets.

A proposed `RejectDuplicateKeys` prefilter correctly flags the ambiguous packet forms, but **it is a stricter new reference language**. It would reject four observed accepted packets. Treating it as the historical transition relation would violate the mandatory concrete-to-abstract overapproximation inclusion, and could falsely promote a lower bound. To retain native cost soundness, either normalize and prove a full cost/provenance simulation, or map all accepted lexical aliases into the same parsed-state MAY class. No such normalization is claimed for the unknown full calculus. Unknown RES, LOCAL-CONVERT, paid DEF/facets, exports, contexts, branches, discharge, joins, weakening and deletion stay MAY transitions pending original source authentication.

Proof existence, acquisition, verification, evidence bits, construction time, span and peak machine space remain distinct. The historical R_mix341 charges/weights, shared count-once paid identities, proof-choice freedom and branch obligations have NOT been changed.

## Search and corpus reconciliation

Read entire current root `proof1.txt` and `proof2.txt`, issue #3/recent comments, `AGENTS.md`, `CODEX.md`, pnp-research skill, November 9 abstract/FLMV handoffs, native-focus directive, original /341 producer/verifier, LSPV-2/537-539 and peer LSPV-1/553-555 including latest independent typed reference; historical 539-549 status remains restricted. Source-checked external `konard/p-vs-np/scripts/proof_status.json` blob 93b77ed3, `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` blob 18d693ea, `meelgroup/frat-xor/format.md` blob 986a21aa and `tanyongkiam/cake_lpr/README.md` blob e94f45e9. Cook-Reckhow 1979 (DOI 10.2307/2273702) establishes proof-system scope; Cousot-Cousot 1977 (DOI 10.1145/512950.512973) supplies sound transition abstraction principles. FRAT-XOR has a distinct formal record language and cannot authenticate historical R_mix341.

The genuinely **new** observation is accepted decoded-key shadowing and its byte-level auth hazard, not the already established support-string/phantom-affine SAT packet bugs, missing full-rule dispatcher or strict-fragment soundness. No existing result was promoted or retired.

**Evidence proposal [P2-L2-540]** supports OPEN [P2-D1] and OPEN [P2-C3]. [P2-B1], [P2-B2]/B3 and all universal Route A obligations remain OPEN. P versus NP remains OPEN.

**Reproducibility:** Run `node experiments/arc/lspv2_540_json_shadow_native.cjs results/raw/arc/local_540.json` from repository root, then compare the per-case native verdicts and use its SHA-256 fields. The executable cryptographic hashes are a replay aid, not results claimed from this isolated V8 audit.

**Next:** Locate the actual full-rule native byte parser/dispatcher, and use last-value/Unicode duplicate lexical controls during source-binding and cost-sound replayer development.
