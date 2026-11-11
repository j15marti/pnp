# LSPV-2/544: Valid-UTF-8 lossless accepted-byte replay for the recovered /341 checker

**November 10, 2026, 17:15 PST | SAT-Circuit Reduction Builder | historical Route A | PROVED/RESTRICTED representation lemma + COMPUTATIONAL. P versus NP OPEN.**

## IDEA -> SEARCH -> ITERATE and four falsifiers

**Candidate:** Extend LSPV-2/543's ASCII-only reference JSON span editor to strictly valid UTF-8 raw bytes, Unicode property keys, non-BMP scalar identifiers, all shared occurrences of a SOURCE ID and its escaped equivalent. Differentially replay against the *original unmodified* /341 checker. Do not infer missing historical rule syntax or a machine-cost-nonincreasing normalizer.

F1: UTF-8 byte boundaries are confused with JavaScript UTF-16 indices. F2: re-encoding all appearances of a live Unicode ID breaks string equality and parent dependencies. F3: competing raw/escaped Unicode keys select an inactive shadow object. F4: a wrong signed source literal or dangling parent passes. F1-F3 were tested with accepted packets; F4's two hostile packets were rejected.

**PRECEDENCE:** /540 established duplicate-key acceptance, /541 nonfinite ID reserialization failure, /543 ASCII last-wins token editing, /539 the distinct typed reference SOURCE/AND3/XOR checker, /542 source-occurrence transport, LSPV-3/550 untyped literal coercion, LSPV-3/556 RES byte underdetermination, and LSPV-1/559 a guarded semantic-soundness subset. This run's distinct contribution is a Unicode-competent *byte-oriented executable replayer*, not rediscovery of these issues.

## Historical evidence and exact source scope

Original semantic declaration: research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex, blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb. It declares free SOURCE and unit-paid RES, AND3, XOR, LOCAL-CONVERT and conservative DEF. The declaration does not supply a complete accepted-byte grammar for RES, LOCAL-CONVERT, DEF facets/ports, contexts, fresh wires, branching/discharge, weakening, joins or deletion.

Recovered original producer: experiments/arc/lspv2_341_mixed_tseitin_min_dag.js, blob 4081022e8a3841d79f751a3d3a7a10decbb026da.
Recovered original restricted fixture checker: experiments/arc/lspv2_341_independent_verify.js, blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0. It dispatches only AND3/XOR and hardcodes 4V-1 paid nodes; it is **neither** the complete historical R_mix341 checker **nor** independently external-DIMACS-source-bound.

Established source: odd-charge K4 cubic Tseitin CNF, 6 edge variables, 16 original proper signed width-three clauses, 0/64 satisfying assignments, 15 paid AND3/GF(2) nodes. The easy parity shortcut remains admitted. The test changes lexical SOURCE IDs and graph metadata, not signed clauses, distinct paid derivations, original GF(2) equations or node weights.

## Theorem 544.1: Unicode scalar identity transport (PROVED/RESTRICTED)

Let b be a strictly valid UTF-8 byte sequence encoding syntactically valid JSON of nesting depth at most 512. The separate reference lexer scans byte offsets, uses JavaScript JSON.parse for syntax validation, decodes object keys as JavaScript strings, and selects the *last occurrence of the decoded key*. Each scalar JSON string value has an exact half-open byte span [i,j), even if the raw text contains Unicode or backslash-u escapes.

Fix one decoded primitive string s and a JSON string token u such that JSON.parse(u) === s. Replace any or all selected scalar-string value occurrences whose decoded value is s by UTF-8 bytes encoding u, in increasing, disjoint span order. Then: (i) every untouched original byte is preserved in order; (ii) JSON.parse of the new packet yields the same structured parsed values and winning decoded keys; (iii) JavaScript Map/string equality and shared SOURCE-ID/parent dependencies are unchanged; and (iv) any checker operating only on that parsed object has the same acceptance and logical count-once node cost. The *raw bytes, evidence length, byte hash, parser work and machine peak space can differ*.

**Proof:** Each replacement is a JSON string expression of the same primitive value s. Object keys are not rewritten, so decoded-key collision precedence is unchanged. Structural induction on arrays and objects gives equality of the parsed values. The splice routine emits exact original byte segments between selected spans and then the selected replacement tokens; therefore no other byte is mutated. The original fixture checker reads its packet as a parsed object and does not use the original byte serialization thereafter, so its transition semantics and acceptance are preserved for these particular re-encodings. This theorem concerns this valid-UTF-8 JSON sublanguage, not every historical native certificate.

**Different, weaker fixture-only claim:** replacing the untyped source-literal token " 0001 " (a JSON string) with JSON number 1 changes parsed types; the theorem does not imply equivalence. The original checker nevertheless accepts both K4 packet variants due to its already documented numeric coercion. This is operational evidence, not a free rule or an all-input normalizer.

## Reproducibility and raw accepted-byte corpus

Published executable: experiments/arc/lspv2_544_utf8_lossless_replayer.cjs, blob 4788b015aeed131bef37198ba41451ee521edb36.
Raw result and **complete 8 byte strings encoded in UTF-8 hex**: results/raw/arc/2026-11-10_1715_LSPV2_544_UTF8_NATIVE_RAW.json, blob f533c7cea292a7d1e78b18cfd08daf13f9bc07b9.

| Packet | Recovered original checker | UTF-8 bytes | Assertion groups |
| --- | --- | ---: | ---: |
| Baseline compact K4 | ACCEPT | 3563 | 1401 |
| Live non-ASCII SOURCE ID 源🤖 and Unicode graph name | ACCEPT | 3609 | 1401 |
| All 3 shared ID value occurrences re-escaped | ACCEPT | 3642 | 1401 |
| Raw/escaped non-BMP duplicate keys; shadowed fixtures | ACCEPT | 3662 | 1401 |
| Unicode packet with untyped signed source literal | ACCEPT | 3616 | 1401 |
| Surgical repair of that literal to integer | ACCEPT | 3609 | 1401 |
| Wrong signed original-source value | REJECT | 3611 | n/a |
| Dangling parent reference | REJECT | 3614 | n/a |

All 8 outcomes matched when the actual pinned original producer and verifier were run in hosted V8 with only Node I/O objects substituted. Six accepted packets yielded **8406 historical checker assertion groups**. The full original *seven-fixture* producer/checker regression independently passed **30714** checks. The reference Unicode lexer visited 417 syntax nodes with depth 6, found 3 shared UTF-8 SOURCE ID values, and applied simultaneous lexeme replacements. Two invalid UTF-8 byte arrays were rejected by the reference decoder. They were **not** asserted to be rejected by Node fs.readFileSync with its own replacement-character policy.

The published script was fetched back at its Git blob and reexecuted against the original producer/checker. No native OS Node CLI run, complete R_mix341 checker, native FLMV interpreter, or machine peak-RSS measurement was performed. The recovered checker can accept unrelated SAT-source forgeries, so these accepted packets cannot alone certify an externally authenticated source.

## Concrete-to-abstract transition correspondence and CEGAR

Concrete parser/proof state includes raw bytes and byte spans, winning decoded JSON object, external-source binding status, signed original SOURCE occurrences, JavaScript scalar ID identities, original parent shared DAG, new paid-event identities, charged-node set, claimed contexts/freshness/ports, terminal goal predicate, parsing/read/output work and peak live state. The recovered checker does not authenticate the missing native context, wire, branch, conversion or DEF interfaces. In a full-calculus overapproximation, they remain unknown MAY transitions, never rejected because this fixture verifier omitted them.

The restricted abstraction alpha forgets only scalar-string *lexeme spelling* and retains decoded SOURCE IDs, occurrence identities, DAG structure and the global paid set. Gamma contains every valid-UTF-8 packet with identical decoded values and separately retained independent-source binding. Its verified core transitions project at exactly their concrete logical count-once unit charge. Physical byte/time/space cost is not preserved by that quotient and must retain the raw byte length and operational steps.

**CEGAR:** A coarse source-kind-only abstraction admits the corrupted signed source; native replay rejects it, so refinement retains exact signed value. Conversely, Unicode SOURCE-ID escape transport is genuinely native accepted and must not be refined away. First-decoded-key rather than last-decoded-key semantics would wrongly exclude the accepted Unicode-shadow fixture, so it is not a sound native parser abstraction.

The in-memory test implementation holds O(B) bytes of raw/parsing/output state for input and output lengths O(B), where B is certificate byte length, but the multi-edit stage sorts k spans and thus has conservative standard-runtime cost O(B + k log k + output size). Native indexed-TM machine costs, source acquisition, hashing, evidence construction, parser and verifier execution, temporary copies, caches and peak simultaneous storage remain unmeasured. Logical W=15 is distinct from evidence bits, assertion count, wall time, span and space.

## CORPUS REVIEWED, LITERATURE and duplication audit

Read both root proof trackers, current issue #3 with 1586 comments, AGENTS.md, CODEX.md, research skill, the Nov 9 abstract-interpretation and FLMV handoffs, actual historical /341 source and /537-543 reports, LSPV-3/549-556, LSPV-1/559, LSPV-4/528, LSPV-5/478 and MODELBRIDGE-0010. Recursive main-tree search surveyed **16020** repository entries. Only partial original checker, diagnostic extensions, independent reference parsers and counterfactual grammars were identified; no authoritative full RES/LOCAL-CONVERT/DEF/context byte dispatcher was found in the inspected repository material. This does not prove such a dispatcher never existed.

Primary research: Cook-Reckhow (1979), DOI 10.2307/2273702, requires declaring the verifier/proof-language relation; D'Silva-Haller-Kroening (2014), DOI 10.1145/2535838.2535868, motivates abstract deduction/refinement; Giacobazzi-Ranzato-Scozzari (2000), DOI 10.1145/333979.333989, gives completeness refinements under hypotheses. None supplies the absent historical parser.

Checked original GitHub contents rather than badges: meelgroup/frat-xor/format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f specifies a **different** elaborated XLRUP format; konard/p-vs-np/scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2 is finite-machine scoped; blkph0x/p-vs-np-proof-research/METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5 lists restricted directions. No OpenAI/formalization artifact inspected specifies the local full historical parser.

**DUPLICATION / CONTRADICTION:** existing duplicate-key, nonfinite-ID and coerced-source findings are reused, not reannounced as discoveries. /559's primitive-literal guard rejects the padded control but can admit the repaired source once externally bound. No competing full mixed-rule proof authority was found. The new parser is explicitly non-authoritative and cannot silently discard any legal full-rule operation.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** [P2-D1], [P2-C3], [P2-B1], separate [P2-B2]/B3, [P2-A2], [P1-01], [P1-03], [P1-04] remain OPEN. This is a reusable accepted-byte acquisition/replay tool, not a new unrestricted lower-bound arrow. The original five research roles, titles, schedules, Pacific timezones, two Route A/three Route B labels, native rules/weights, and ownership boundaries were unchanged. No automations were edited.

## Immediate handoff

Locate **one authoritative historically accepted RES or DEF/facet/LOCAL-CONVERT/context-discharge packet with its actual dispatcher**, rather than inventing bytes from mathematical descriptions. Extend the Unicode-capable reference scanner only after the native transition is authenticated. Retain independent original source hash, paid IDs, wire freshness and branch AND discharge; keep logical nodes, certificate bits, parser/verification time, shared span and peak space separate.

**P versus NP remains OPEN.**
