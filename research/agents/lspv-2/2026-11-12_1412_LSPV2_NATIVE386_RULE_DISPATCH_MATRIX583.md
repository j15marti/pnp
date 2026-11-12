# LSPV-2/583: Exact original-/386 rule-dispatch corpus, three live native positions

**2026-11-12, approximately 14:25 PST | SAT-Circuit Reduction Builder | historical Route A | PROVED/RESTRICTED source-code property and COMPUTATIONAL original-OS differential. P versus NP OPEN.**

## Candidate and four falsifiers

**Candidate [P2-D1/P2-C3]:** Differentially replay twenty potential native rule tags at each of three actual SOURCE, defining-facet DEF and terminal signed-Resolution positions in accepted original-/386 source-pinned proofs. Produce exact accepted/rejected packets and independent source hashes. This tests the recovered checker, **not** the unknown complete historical `R_mix341` dispatcher.

F1: AND3, XOR or LOCAL-CONVERT becomes a live accepted opcode in /386. F2: relabelling an authenticated SOURCE/DEF/RES position creates another accepted derivation without satisfying its native parent and owner obligations. F3: corrupt original SOURCE, gate facet, signed pivot, paid count, dependency order or wire freshness still passes. F4: the checker executes a purported GF(2) or LOCAL-CONVERT step merely because its metadata is present on an actual RES record. F1-F3 failed in original CLI execution, and F4 failed by original code inspection; an annotated RES packet was accepted only as RES.

## Exactly authenticated authority

* Recovered original-/386 checker: `experiments/arc/lspv2_386_independent_verify.js`, Git blob `338305c0ce101704205e57543756b8127074a986`, SHA256 `22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113`.
* Independently signed K4 guarded source, 17 signed clauses and seven variables: `results/raw/arc/2026-11-12_1412_LSPV2_583_SIGNED_K4_SOURCE.cnf`, SHA256 `3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c`, 215 bytes.
* Source-identical accepted W29 seed: `results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json`, SHA256 `0d8b1894f91d00c554727a92fed35b2bb58f2b1602f2a3cfcb949effda43ceb0`. Accepted W31 live-DEF seed: `results/raw/arc/580_DEF_THEN_RES_W31.json`, executed serialized SHA256 `2aebdff68fa72cecd0889118298f6ebd743d32ea313f124bc14fb3c170ddd835`.
* Separate original-/341 checker `experiments/arc/lspv2_341_independent_verify.js` blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0` authenticates SOURCE/AND3/XOR fixture records only. Neither executable is the complete historical `R_mix341`.

**Original-source restricted lemma.** Every record that survives the archived /386 checker has active parsed `kind` in the exact set `{SOURCE,DEF,RES}`, because the unchanged validator executes `['SOURCE','DEF','RES'].includes(r.kind)` before its separate typed-rule tests. This is a direct property of this **sibling checker**, not a rule definition for historical `R_mix341`; prior /386 archaeology already knew this code boundary.

## Executable 71-packet original-OS matrix

The published, byte-exact locally executed OS driver is `experiments/arc/lspv2_583_native_rule_matrix.cjs`, Git blob `358abea84f96b1823929806f4d611324669909b0`, SHA256 `49919da0809e098e6fe62b3ccc4fe855ac712ba012c19b754ee7b4e5d19b2f39`. It invokes the unmodified pinned Node v22.16.0 checker once per exact candidate, records the SHA256 and byte length of every real packet, stderr rejection text, paid work and assertion count, and independently checks the exact external signed SOURCE clauses. There are no random inputs.

| Actual modified live record | Tested active `kind` strings | Original CLI ACCEPT | Original CLI REJECT |
|---|---:|---:|---:|
| First genuine SOURCE | 20 | 1, `SOURCE` | 19 |
| Genuine free paid-owner DEF facet | 20 | 1, `DEF` | 19 |
| Terminal strict signed Resolution | 20 | 1, `RES` | 19 |

The twenty tags are `SOURCE`, `DEF`, `RES`, `AND3`, `XOR`, `GF(2)`, `GF2`, `LOCAL-CONVERT`, `LOCAL_CONVERT`, `PAID-DEF`, `BRANCH`, `SPLIT`, `ASSUME`, `WEAKEN`, `DISCHARGE`, `JOIN`, `DELETE`, `COPY`, `RESOLUTION`, and `AND2`.

Additionally, two unchanged baseline refutations (W29 and W31) accepted, eight independently forged source/pivot/facet/owner/payment/parent/charge/fresh-wire packets rejected, and one intentionally annotated but **still active RES** packet accepted. **All 71/71 expected outcomes matched: 6 ACCEPT, 65 REJECT, 20,900 accepted-case native assertion groups and 66 intrinsic native negative checks.** The annotations included bogus `GF(2)`, `LOCAL-CONVERT`, `context` and `discharge` fields but did not instantiate any corresponding rule.

Full machine-readable raw manifest (71 per-packet SHA256/bytes/verdict/error records) is `results/raw/arc/2026-11-12_1412_LSPV2_583_NATIVE_RULE_MATRIX_RAW.json.gz.b64`: a newline-terminated BASE64 encoding of gzip-compressed UTF-8 JSON. To recover: `base64 -d < ...json.gz.b64 | gunzip > ...json` (on macOS, `base64 -D`). Exact decoded JSON file SHA256 is `db963fc37dc99854201fd0f45408e1647fb151386489d8282fa8545e56aae61a` (24,805 bytes), and the repository's compressed file Git blob is `ce232eb69390ae2d4e8edfdb41981135d9699f87`. Eight selected positive/negative original accepted-byte packet files and their SHA manifest also accompany the research evidence ZIP.

## Implications and scope

For P2-C3, an unknown complete-historical-rule transition must remain **MAY/overapproximated** until its authoritative byte semantics are acquired. The fact that a genuine AND3 active tag is rejected here does **not** prove any AND3 transition illegal in historical `R_mix341`; conversely annotations or a dual-checker JSON polyglot cannot certify a genuine cross-rule dependency. The earlier /582 SOURCE/DEF/RES cost-sound prefix simulation retains its *restricted* scope. A full mixed-rule `alpha/gamma`, spurious-path CEGAR proof, all-rule lower bound or B3 bridge is not established.

**CORPUS REVIEWED / DUPLICATION AUDIT.** Both root trackers, issue #3 through LSPV-1/602, AGENTS.md, CODEX.md, research SKILL, recent five-role handoffs, original /341 and /386 checker code, actual LSPV-2/539-549 and /573-582 reports, and relevant peer /601-/602 work. Prior REFEREE413 already established /341's incomplete dispatcher; /549 established noncomposition of sibling acceptances; /582 established restricted forward abstraction. No novelty is claimed for those facts. Required external repository direct reads: `konard/p-vs-np` `scripts/proof_status.json` blob `93b77ed3...`; `blkph0x/p-vs-np-proof-research` `METHOD_INDEX.md` blob `18d693ea...`; and `meelgroup/frat-xor` `format.md` blob `986a21aa...`. They do not authenticate missing original transitions.

**Primary methodological sources:** Cook-Reckhow (1979), DOI 10.2307/2273702; Cousot-Cousot (1977), DOI 10.1145/512950.512973; Clarke et al. (CAV 2000), DOI 10.1007/10722167_15; [FRAT-XOR format](https://github.com/meelgroup/frat-xor/blob/main/format.md), a distinct proof grammar.

**WHAT CHANGED RELATIVE TO ROOT MAIN:** the first 20-by-3 original-/386 live-rule differential **corpus** with independent signed SOURCE binding and original-OS replayer, not an expanded historical rule set or a theorem-status change. **ADOPT:** externally authenticated SOURCE, signed ports and owners, original checker verdicts. **REJECT:** inferred full-calculus illegality from this restricted checker or ignored fields as mixed inference. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Neither proof tracker changed. Root `main.tex` could not safely be edited because the repository interface returned only its SHA and zero readable content; a role-owned, outside-region-preserving merge was impossible. No agent or schedule mutations occurred.

**Affected nodes unchanged:** [P2-D1], full [P2-C3], [P2-B1], separate [P2-B2/B3], and [P1-01/03/04] all **OPEN**. P versus NP **OPEN**. Preserve five existing role identities, original 2 Route A / 3 Route B allocations, titles, Pacific Time schedules, weights and manuscript ownership.

**Decisive next target:** locate the single *historical* dispatcher and an independently source-bound genuinely accepted RES→AND3 or paid DEF→LOCAL-CONVERT byte packet, with the same checker rejecting a corrupted signed dependency.
