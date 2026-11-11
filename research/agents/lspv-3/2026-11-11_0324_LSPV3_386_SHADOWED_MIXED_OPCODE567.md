# LSPV-3/567: original /386 raw-byte shadowed opcode and SOURCE/DEF provenance ambiguity

**2026-11-11 03:24 PST | Hypergraph & Proof Certificates | historical Route B | PROVED/RESTRICTED ORIGINAL-CODE PROPERTY + COMPUTATIONAL HOSTED-V8 REPLAY. P versus NP OPEN.**

## Candidate and four falsifiers declared before search

**Candidate:** The original archived `/386` checker accepts raw JSON objects containing (i) forged *earlier* duplicate source-specification, SOURCE-provenance, DEF-owner, and operation-kind members, and (ii) unrecognized fields advertising AND3, LOCAL-CONVERT, GF(2), zero costs, exported wires and discharged branch contexts, because its actual `JSON.parse` + `checkProof` reads the *last* duplicate member and only the recognized subset of properties. Such an accepted packet is **not** a heterogeneous historical R_mix341 proof.

F1: the original checker rejects the duplicate member packet despite the final valid values. F2: reversing member order fails to change acceptance. F3: the `kind=LOCAL-CONVERT` record is actually dispatched as LOCAL-CONVERT, or unsupported fields change paid work. F4: the complete original CLI with its eleven original negative tests rejects the shadowed packet. All four are defeated by the exact replay below. The controls are explicitly finite; the source-code property is global for its named accessor fields.

## Original implementation, non-composition, and prior art

Original unchanged archived verifier: `experiments/arc/lspv2_386_independent_verify.js`, **Git blob 338305c0ce101704205e57543756b8127074a986**. Original authenticated 69-record guarded odd-K4 packet: `results/raw/arc/2026-11-10_2124_LSPV3_561_ARCHIVED_386_NATIVE_PACKET.json`, **Git blob d0fa96a155672f8f6a6a3428eacafa15e79b9e88**. Its canonical final parsed source has 17 SOURCE clauses, one paid DEF owner with three free facets, 49 paid RES, W=50, and ends with the empty clause. The historical R_mix341 full mixed parser is still unlocated. The distinct original /341 checker (`experiments/arc/lspv2_341_independent_verify.js`, blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`) dispatches only AND3 and XOR.

**Prior art acknowledged:** LSPV-5/417 already established duplicate JSON member erasure for the different original /341 fixture checker. LSPV-2/549 showed that even one packet separately accepted by /341 and /386 proves no cross-rule binding. LSPV-3/559 established the /341 closed-world dispatch. **What changes:** this is an exact ORIGINAL **/386** byte-level composite witness with forged signed-source charge, SOURCE and paid-DEF facet owner IDs, counterfeit missing mixed opcodes and *complete original-CLI acceptance*. It does not establish any new genuine cross-rule operation.

The `/386` checker directly parses JSON with `JSON.parse`; it checks `spec.charge`, record `kind`, `source`, `gate`, `pivot`, clause `c`, `parents`, and the paid summary. It never inspects a record's `rule`, `weight`, `context`, `exported_wire`, or `advertised_gf2` members. The raw witness places `"charge":[0,0,0,0]` before the valid odd-charge vector, `"source":98765` before `"source":0`, `"gate":98765` before `"gate":0`, and `"kind":"LOCAL-CONVERT"` before `"kind":"RES"`. Unread metadata falsely advertises `"rule":"AND3"`, `"weight":0`, a discharged branch context and a GF(2) conclusion. The actual last-value parsed object remains the unchanged valid /386 proof plus inert extra keys.

## Theorem 567.1 (PROVED/RESTRICTED exact original-code parser distinction)

Let `B` be the byte strings parsed by Node/V8 `JSON.parse`, `J:B→Objects` its parsed-value mapping, and `V_386` the archived original `checkProof`. Then the actual mathematical acceptance predicate is `A_386(b)=V_386(J(b))`, not an injection from raw bytes to uniquely named objects. For any base packet accepted by `V_386`, adding any number of duplicate recognized members with arbitrary **earlier** values while leaving the final recognized member unchanged preserves the parsed value at those keys; inserting any number of otherwise accepted unrecognized metadata members also preserves the checker-visible state. In particular, the published **4,345-byte** raw packet is accepted with exactly the same paid work as the original 4,144-byte packet:

$$
W_{386}(P_{\mathrm{shadow}})=W_{386}(P_{\mathrm{base}})=49+1=50.
$$

The source-charge string in raw text is **not uniquely determined** until the parser resolves duplicate members. Thus a raw SHA-256 alone, without a unique-key parse and canonical-source binding policy, cannot prove that a *visibly first* formula or opcode was what the checker validated. This is a byte-to-semantics ambiguity, not an UNSAT soundness failure of the last-value parsed program and not a proof that LOCAL-CONVERT is legal.

**Proof:** The original checker reads the decoded object, not raw member offsets. JavaScript `JSON.parse` retains the last of repeated member names. In the witness each first shadow value is overwritten by the genuine final value. Additional metadata is not addressed by any checker operation. Therefore all original checked source clauses, signed pivots, gate owner identities, parent references, paid counts and contradiction are unchanged. Reversing each duplicate order makes the malformed value authoritative and triggers the exact original error. Real `kind:"LOCAL-CONVERT"` fails the checker's explicit `['SOURCE','DEF','RES']` kind whitelist. QED for the named cases.

## Native exact-byte test matrix

| Control | Actual original core | Expected |
|---|---|---|
| Baseline original 4,144 B | ACCEPT, 725 assertions, W=50 | ACCEPT |
| Composite 4,345 B with four shadowed members + fake mixed metadata | **ACCEPT, 725 assertions, W=50** | ACCEPT |
| Reverse charge, last charge even | REJECT `not odd` | REJECT |
| Reverse SOURCE ID, last `source=98765` | REJECT `wrong source 0` | REJECT |
| Reverse facet owner ID, last `gate=98765` | REJECT `undefined gate` | REJECT |
| Reverse operation kind, last `LOCAL-CONVERT` | REJECT `record kind or clause at 20` | REJECT |
| Genuine `LOCAL-CONVERT` kind without duplicate | REJECT | REJECT |
| Add only ignored `rule=LOCAL-CONVERT, cost=0` metadata | ACCEPT, W=50 | ACCEPT |
| Corrupt actual signed SOURCE clause | REJECT `wrong source 0` | REJECT |

**Complete original CLI replay:** baseline and shadowed packet both ACCEPT, both report **4,492 assertions, eleven bundled negative controls, 17 sources, 69 records, one DEF, 49 RES, paid W=50**. The original mathematical `checkProof` and complete CLI code bodies were executed in hosted V8; only filesystem, crypto digest and `structuredClone` host bindings were adapted. The hosted digest field was deliberately unmeasured, and the independently executable Node.js reproducer is published, **not independently run as an operating-system subprocess in this run**. The original code and all nine test cases passed with no verifier edits. The faithful OS-node script uses genuine Node `crypto` and `vm` and can be executed as `node experiments/arc/lspv3_567_shadowed_386_mixed_opcode.cjs`, with `--write` for a separate OS ledger.

## Exact accepted-byte corpus and conservative repair

- Native accepted packet: `results/raw/arc/2026-11-11_0324_LSPV3_567_SHADOWED_386_ACCEPTED_PACKET.json`.
- Original-checker hosted-V8 raw result: `results/raw/arc/2026-11-11_0324_LSPV3_567_SHADOWED_386_HOSTED_V8_RAW.json`.
- Full standalone code: `experiments/arc/lspv3_567_shadowed_386_mixed_opcode.cjs`.
- Original source and input Git blobs above, plus exact publication blob readback in issue #3.
- Five-role handoff: `research/coordination/2026-11-11_0324_LSPV3_SHADOWED_NATIVE_386_OPCODE567_FIVE_ROLE_HANDOFF.md`.

For any prospective full R_mix341 checker, enforce **unique decoded member names at the raw-token layer before ordinary JSON object construction**, then enforce a typed allowlist for consumed fields or explicitly reject unknown fields. Bind an external original-source digest to the uniquely decoded signed original clauses and graph rather than to an arbitrary first or last occurrence in a raw textual display. Re-run all hostile near-misses on the **same historical single-dispatcher executable**, without substituting our repair as if it were historical law.

The control does **not** justify deleting a genuine shortcut that an authentic checker accepts; the accepted /386 shadow packet's 50 paid nodes remain charged exactly once, with three actual free DEF views. Logical work, raw bytes/evidence, actual checker runtime, proof span, and peak live space are distinct. No time/space measurements were fabricated.

## Literature, source, and current-corpus record

Reviewed the complete root `proof1.txt` (blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`) and `proof2.txt` (blob `20fd65cf8842d32a851a14a1496c7ea6156cb160`), issue #3 including current peer /539, /553, /554 and /569 entries; `AGENTS.md` (blob `4ae902888754d0b06ba4ce1aaeca0657a92b46a9`); `CODEX.md` (blob `754999f50de93cdb693ed37bc8110d31e9e698ef`); `.codex/skills/pnp-research/SKILL.md` (blob `b8df83a7b0b1428f349b0e02ce1387d979e8db7f`); LSPV-3/542 and 559-566, LSPV-2/549 and original /341 rule declaration, LSPV-5/417/483, LSPV-1/569 and LSPV-4/539, current GROKPROOF /0415, and the original Claude world-ledger. No historical unified mixed dispatcher was recovered in this audit.

References: [1] IETF RFC 8259 §4, https://www.rfc-editor.org/rfc/rfc8259 (object members SHOULD be unique; duplicates are not interoperable); [2] ECMAScript `JSON.parse` duplicate-member semantics, https://learn.microsoft.com/en-us/openspecs/ie_standards/ms-es3ex/020e9e54-2a02-41c7-88b6-5ce93e9b48dc; [3] Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979), 36–50, DOI 10.2307/2273702; [4] `meelgroup/frat-xor/format.md`, a separate verified-CNF/XOR ecosystem, not R_mix341.

**Current gap:** P2-D1 still lacks a complete original accepted-byte R_mix341 single-checker grammar. Hence full P2-C3 alpha/gamma and CEGAR, P2-B1 superpolynomial all-rule lower bound, and separately P2-B2/B3 transfer all remain OPEN. No new P/NP proof, no hard-family claim.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** No proof1.txt or proof2.txt edit: previously known duplicate-member boundary is extended to a distinct authentic archived checker but closes no load-bearing proof claim. The GitHub fetch of full root `main.tex` returned `sha=9e81c188172949641d880640adf1dffa21e17121` with **empty content** for the oversized manuscript, so safe LSPV-3-region-only reconciliation and full outside-byte readback were impossible; `main.tex` was left untouched rather than risking destructive overwrite. Local preflight/report-check scripts could not run in this connector-only environment. All five scheduled agents, identities, Pacific timestamps, historical weights, ownership boundaries and TWO Route A / THREE Route B labels were preserved. P versus NP remains OPEN.
