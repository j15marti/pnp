# LSPV-4/527: Cost-optimal native-fixture string-ID relabeling

**2026-11-10 15:40 PST | LSPV-4 Time-Space Resource Auditor | historical Route A label retained | PROVED/EXACT restricted + COMPUTATIONAL | P versus NP OPEN.**

**Path:** [P2-D1] -> [P2-C3] -> [P2-B1], separate [P2-B2]/B3. **Proposed new evidence:** [P2-L4-527]. Precedence: [P2-L4-525] proves ID-length/fanout inflation for separately typed shared XOR proofs; [P2-L4-526] proves accepted-byte GF(2) evidence-read sensitivity; [P2-L2-540]/[P2-L2-541] prove JSON numeric-normalization hazards; [P2-L3-554] prohibits equating recovered-checker ACCEPT with semantic UNSAT.

## IDEA and falsifiers (before search)

**Candidate:** Every nonempty ASCII alphanumeric *string* source/proof ID in the recovered original /341 SOURCE/AND3/XOR fixture is tested only for equality and Map lookup. Uniform bijective renaming should preserve original-checker acceptance, paid nodes, shared dependencies and span. The shortest explicit JSON name-value encoding for a *fixed* proof DAG has an exactly solvable assignment optimum based on ID reference frequencies. This is a representation upper-bound control, not a shortest-proof or SAT-solving theorem.

F1: A consistent bijective rename is rejected by unchanged original checker. **FALSIFIED for all seven existing fixtures.**

F2: Non-greedy assignment of allowed codeword lengths beats matching highest frequencies to shortest names. **FALSIFIED by exchange proof; 24 exhaustive assignments and 75 independent random exhaustive controls.**

F3: Invalid inference IDs, corrupted source clauses, false AND3 rows or bad deletion witnesses pass after renaming. **FALSIFIED by five original-checker negative tests.**

F4: Non-string or nonfinite JSON numeric tokens can be freely normalized. **Not claimed.** The new optimizer refuses a numeric ID, preserving the known counterexamples [P2-L2-540]/[P2-L2-541].

## SEARCH, precedence, exact sources

Read the complete root proof1.txt (initial blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b) and proof2.txt (initial blob 7ed8b99f9925b97680b3c0d8aa9951706ceb603a), issue #3 and current November 10 comments, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, role handoffs, the LSPV-1/539-549 file index and full LSPV-1/544-545 analyses, issue #3 evidence for LSPV-1/556-557; full LSPV-2/539 and issue records for /540-/542; LSPV-3/544-549 and issue reports for /550-/554; relevant LSPV-4/522-526, actual GROKPROOF/2026-11-09_2015_PROGRESS.md and research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex. Earlier LSPV-3/549 already treats canonical arbitrary-size IDs in a **different, explicitly specified** contextual CASE/LEAF/WEAKEN test calculus; this report does not claim first discovery of large IDs or of abstract normalization.

Original fixed rule declaration: research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex, Git blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb. Declared weights: free SOURCE and one per fresh derived RES/AND3/GF(2)/LOCAL-CONVERT/paid DEF, references to previously paid nodes do not themselves create new deductions. Actual complete accepted-byte semantics for most of these operations **remain unrecovered**.

Pinned actual original fixtures: experiments/arc/lspv2_341_mixed_tseitin_min_dag.js (blob 4081022e8a3841d79f751a3d3a7a10decbb026da); independent verifier experiments/arc/lspv2_341_independent_verify.js (blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0). These prove only the recovered partial fixture language, which is **not independently external-source-bound** and has known accepted SAT-source errors.

External source files actually reread: konard/p-vs-np scripts/proof_status.json (93b77ed3d8fe456f81c690035f45f07910a247f2); blkph0x/p-vs-np-proof-research METHOD_INDEX.md (18d693ea71dfa433370eb7afbebc3106e32f03e5); meelgroup/frat-xor format.md (986a21aa92b62f844ef1fce852193142c41b2b1f); tanyongkiam/cake_lpr README.md (e94f45e9aa000cd9ada12f4c771ac9daf28fe53c, 1 Nov 2026 final planned release); MassimoLauria/cnfgen cnfgen/families/tseitin.py (4bb5fd198fc4a698a5a207f67b36a9591b2a3bab); openai/math README.md (cc5b0a03bca6c742f045d683b6647a6f44ef2cae). None defines historical /341 accepted bytes.

Primary methods: Pommerening et al., ICAPS 2021, DOI 10.1609/icaps.v31i1.15971 on cost partitioning, and Nordström, LMCS 2013, DOI 10.2168/LMCS-9(3:15)2013 on proof DAG pebbling. Their theorems do not authenticate this project calculus. Urquhart, JACM 1987, concerns ordinary Resolution hardness only. No branded Google interface, OS checkout or repository-wide local preflight was available.

## ITERATE: exact named-proof normal-form theorem

Fix a finite proof packet P from the **string-ID sublanguage** of the recovered /341 fixture: all IDs in clauses[].id, proof[].id, proof[].parents[] and deleted[].sourceId are distinct-at-definition, nonempty alphanumeric ASCII JSON **string values**. IDs appear nowhere else in source literals, graph data, source commitments or semantic fields. There are D different IDs with positive total occurrence counts f(i), including each defining occurrence. No raw lexical interpretation of the names beyond exact Map-key equality is permitted. Choose an injective rename into A^+ with the 62-character alphabet of ASCII digits and English letters. JSON quotation marks delimit strings, so codewords do not need to be prefix-free.

Let f_1 >= ... >= f_D be the sorted occurrence counts. Let ell_1 <= ... <= ell_D be lengths of the globally D shortest nonempty words from this alphabet; exactly 62^j allowed words have length j.

**Theorem 527.1 (PROVED/EXACT in the specified grammar):**

$$
B_{\rm ID,min}=\sum_{i=1}^{D} f_i\ell_i.
$$

If original compact-JSON packet size is B_0 and original name-value bytes are B_ID,old, the optimally renamed packet has **exactly**

$$
B_{\rm opt}=B_0-B_{\rm ID,old}+B_{\rm ID,min}.
$$

Every original fixture accepted by the native recovered verifier is accepted after such a globally injective relabeling, with the **same** signed CNF, proof rule instances, original-source deletion witnesses, charged distinct-node work W, shared DAG and weighted critical path. No native full-calculus rule is added.

**Proof:** Original restricted checker uses the ID strings only in Map membership/lookup, freshness, parent and deletion-source equality, so a global injection preserves and reflects each such test. Every truth-table, graph, source-literal, affine and contradiction check is unaffected. For optimization, any used longer codeword while a shorter unused codeword exists can be replaced with a strictly smaller charge. Among the D shortest codewords, if a higher-frequency ID has a longer assigned word than a lower-frequency ID, swapping the two changes cost by the negative quantity -(f_i-f_j)(ell_long-ell_short). Repeated exchanges produce the stated minimum. Unescaped ASCII JSON field separators/quotes retain the same lengths. This proves name-value **byte** optimality for the fixed DAG, not shortest proofs or other evidence channels. QED.

## Original checker replay and independent controls

The *unchanged* original producer and verifier JavaScript bodies were executed with only CLI input/output adapters in hosted V8. Before and after relabeling, the original seven-fixture checker ran **30,714 assertion groups and accepted every fixture**. Original and optimal single-fixture compact JSON sizes:

| Original proper 3-CNF fixture | Paid W | Distinct IDs | Name occurrences | Bytes before | Bytes after | Saved |
|---|---:|---:|---:|---:|---:|---:|
| K4 | 15 | 31 | 77 | 3,364 | 3,260 | 104 |
| K3,3 | 23 | 47 | 117 | 5,081 | 4,897 | 184 |
| Cube | 31 | 63 | 157 | 6,880 | 6,617 | 263 |
| Petersen | 39 | 79 | 197 | 8,757 | 8,446 | 311 |
| Prism6 | 47 | 95 | 237 | 10,682 | 10,323 | 359 |
| Prism16 | 127 | 255 | 637 | 33,003 | 32,093 | 910 |
| Bridged K4x2 | 39 | 79 | 197 | 8,701 | 8,390 | 311 |

The entire seven-fixture packet shrank from **77,713 to 75,271 bytes**, saving **2,442 bytes** with W and all original checker assertion counts unchanged. Prism16 name field alone fell from 1,998 to its restricted-language optimum 1,088 bytes. Its 255 IDs use 62 one-character and 193 two-character words.

A consistently renamed **16,384-character K4 source-ID** appears in three places. The original checker accepts the enlarged 52,510-byte K4 fixture. The same optimal name relabeling recovers a 3,260-byte fixture with exactly 15 paid nodes and original acceptance. Five corrupt native-checker packets are rejected: missing parent, duplicate paid ID, forged signed source literal, false AND3 truth table, and corrupt deletion witness. Optimizer itself refuses unsupported numeric ID input. A 24-permutation exhaustive length assignment check and **75 independent Python randomized exhaustive small tests** confirm the exchange formula.

The exact published audit is experiments/arc/lspv4_527_native_identifier_relabel_optimal.cjs, blob c89e85e24b51106486a7b42a362af6b26683e7eb. Actual raw output: results/raw/arc/2026-11-10_1536_LSPV4_527_NATIVE_IDENTIFIER_OPT_RAW.json. **Execution scope:** original producer/checker and identical published audit function ran in hosted V8, with Node CLI I/O adapted and an ASCII-only byteLength shim; the published standalone Node process was **not** executed as an operating-system CLI. No stubbed SHA value is claimed as a computed digest; repository Git blob SHA pins came from authenticated connector reads.

## Exact resource qualification and all-rule firewalls

- **SOURCE:** declared zero logical inference charge; original signed literal, source-ID field, deletion witnesses, external authentication, and original byte processing have physical costs. A proof packet carrying its own source is not an independently source-bound native checker.
- **AND3:** declared unit cost per *fresh* inference; two references, local truth table, up to eight checked assignments, support and optional affine alias all incur evidence and validation work.
- **GF(2) XOR:** declared unit per *fresh* inference; two parent references, BigInt parsing, mask XOR, RHS checks, value retrieval and serialization incur physical cost. Reusing the same existing paid node does not create a second logical charge.
- **RES / paid DEF / defining facets / LOCAL-CONVERT:** declared unit for new derived nodes, but historical accepted-byte syntax, permitted views, wire ownership and reference/application tariff remain unauthenticated.
- **CASE / assumption weakening / discharge / joins / deletion:** not authenticated as general historical proof rules. The fixture's deleted[] assignments are source-minimality *test evidence*, not a zero-cost general proof-rule declaration.

A cost-sound name-invariant abstraction maps the original and optimally renamed proof DAGs to the same globally paid occurrence set. The abstract logical work equals concrete W, never double charging references or cross-branch reuse. Its abstract goal must be **source-bound genuine UNSAT**, not the known unsound raw fixture ACCEPT tag [P2-L3-554]. Any may-rule absent from the authenticated grammar must receive a conservative permitted transition, potentially zero abstract cost, until actual native semantics is recovered.

**Physical construction:** source/evidence length B and D IDs must be read, field types verified, frequencies counted, names sorted, D mappings stored, each reference rewritten, whole output serialized, and checker executed with parsing/caching/retention/recomputation costs. An explicit compiler has polynomial serial bit time and polynomial all-phase writable space in B. The original Node implementation holds source/objects/copies simultaneously and was not instrumented for RSS or indexed native WORK high-water; no uncharged compression or FLMV exponent claim follows. Raw long names impose actual input/read/rewrite costs even though the *output* can be short. Sparse/dense affine representations, extension proofs, context-compatible learned lemmas and retention-versus-recomputation remain admissible alternatives.

**Known legal shortcut:** these original odd-Tseitin sources have cheap GF(2) mixed proofs, so expander-Tseitin ordinary Resolution hardness cannot transfer through this native mixed fragment. Name compression cannot establish [P2-B1]. No existing per-reference historical rule charge is revised or invented.

## Publication and precisely outstanding proof gaps

Material evidence [P2-L4-527] qualifies physical certificate resource accounting and string-ID normal forms. Review proof1.txt unchanged; update proof2.txt only with complete current SHA and verified readback, otherwise disclose blocker. Root main.tex returned **zero characters despite a SHA** on full read, so it cannot be modified without potentially overwriting other agent regions. This role-owned report and handoff are the durable fallback.

**Still OPEN:** full accepted-byte and semantic rule authentication [P2-D1], all-rule cost-sound goal-preserving abstraction [P2-C3], superpolynomial worst-case minimum for fixed full mixed calculus [P2-B1], and the separate noncircular B3 implication [P2-B2]. No five-agent identities, schedules, time zones, two Route A/three Route B labels, fixed historical weights or ownership boundaries were changed. **P versus NP OPEN.**
