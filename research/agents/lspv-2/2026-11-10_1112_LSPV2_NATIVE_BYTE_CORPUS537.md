# LSPV-2/537: Minimal source-checked native-341 accepted-byte corpus and typed replay

**2026-11-10 11:12 PST | Route A label retained | COMPUTATIONAL + restricted structural lemma. P versus NP OPEN.**

## IDEA and 4 falsifiers

Candidate: use exact recovered historical /341 SOURCE/AND3/XOR verifier bytes to extract a compact accepted-byte K4 corpus, a separate cost-preserving typed replayer, and discriminating unrecognized-opcode probes. Falsify by (F1) the original seven-fixture replay/check count drifts, (F2) a required field is removed and minimal K4 rejected, (F3) malformed actual source, parent or table is accepted, (F4) omitted external source/context/weight metadata changes checker behavior.

## Source and provenance

Original producer blob `4081022e8a3841d79f751a3d3a7a10decbb026da`; original verifier blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`. The executable pins both blobs and runs the **unmodified JavaScript bodies in V8 with only Node file and console I/O shimmed**. This is exact recovered checker logic, not native external subprocess or any new full-calculus parser. Historical /341 declared RES, LOCAL-CONVERT and DEF in prose but source-inspected verifier dispatch handles only AND3 and XOR; this was already found by LSPV-5/413. LSPV-1/553 separately established ignored external-source fields and rejected paid padding. This run provides a smaller positive byte artifact and integrated byte corpus plus typed transition replay, not novelty for those observations.

Established family is odd-charge K4 cubic Tseitin: four vertices, six original edge variables, sixteen original signed proper ternary clauses. Each local vertex contributes four forbidden-parity clauses; source DIMACS is reconstructed explicitly in the raw ledger. For this family the published LSPV-2/341 declared at-most-binary unit-paid mixed calculus has a 15-paid AND3/XOR refutation and a source-essentiality lower bound, **not** full historical byte-grammar closure. Gaussian elimination is an easy parity shortcut and is retained.

## COMPUTATIONAL accepted-byte evidence

- Full seven-fixture published producer packet: **30714** historical checker assertion groups across 7 fixtures.
- Minimal accepted standalone K4 JSON packet: **3090 UTF-8 bytes**, only `fixtures:[one]` and `summary:[null]`, without top-level version or definition. Exact recovered checker: **1401** assertions.
- Corpus: **28** separate byte packets, **6** accepted and **22** rejected. Full bytes, expectations and observed diagnostic are serialized in `results/raw/arc/2026-11-10_1112_LSPV2_537_NATIVE_BYTE_CORPUS_RAW.json`.
- Independently written typed reference projection: 16 distinct authenticated original-source labels, 15 distinct paid AND3/XOR nodes, 31 reachable ancestors. All contexts in this fragment are empty, no definitions are imported. The logical count is not evidence bits, execution time, span or peak memory.
- Twelve declared-but-unsupported or alternative opcodes, including RES, LOCAL-CONVERT, DEF, SOURCE, SPLIT, ASSUME, DISCHARGE, JOIN, DELETE, WEAKEN, GF(2), RAT, are rejected by this **limited original checker**. These are NOT negative certificates for a fuller historical calculus; unresolved opcodes remain overapproximated, not erased.
- Genuine semantic mutations of the signed source, AND3 truth table, XOR row, parent reference, paid ID, sink and deletion witness are rejected. Forged `externalOriginalInput`, `context`, `weight`, `version`, and summary content do not bind; ignore these fields in any cost-sound projection and check source binding separately. Fresh legal paid padding fails **only** the hardcoded `4V-1` length guard; cannot use this checker to lower-bound every valid length in the prose calculus.

## Restriction-scoped transition lemma and abstract satisfaction

For the executable original-checker fragment with its accepted K4 witness, a concrete verified prefix consists of original-source-labelled Boolean factors, a topological shared DAG of AND3 and XOR derived nodes with unique JS IDs, and empty (unimplemented) contexts. Map each verified transition to its typed support/truth-table or affine row and count each fresh paid node once. Exact-check preservation follows inductively from the original verifier guards and the independently replayed truth tables/XOR equations. The projected paid count equals the checked derived-node count, hence does not exceed it. This is **not** a simulation of a missing RES, DEF, LOCAL or branch transition. For the full declared R_mix341, the conservative abstract transformer must still admit unknown possible operations at no greater unknown charged cost until authoritative parsing/weights are recovered.

CEGAR control: a coarse kind-only abstract XOR transition admits the candidate with a corrupted XOR mask at the original 15-node count; exact native checker replay rejects the bad mask; refinement with an exact affine-mask relation excludes it while retaining the genuine 15-node proof. This is a finite spurious-path test, not a superpolynomial lower bound. The goal is complete UNSAT plus checked original signed CNF; an arbitrary unrelated external `externalOriginalInput` field is not such a binding.

## Cross-check and limitations

Original source and peer reads: both full root trackers (proof1 Git blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`; proof2 `c920eaea9e74fefa314e0ca0291cc9b537052a02`), issue #3 through LSPV-1/553, AGENTS/CODEX/skill, handoffs Nov 9 assumed-time and abstract-negative, LSPV-2/341,/536, LSPV-1/553, LSPV-3/549, LSPV-5/413,/435 and MODELBRIDGE-0010. Primary literature Cook-Reckhow 1979, D'Silva-Haller-Kroening 2013/2014, Giacobazzi-Ranzato-Scozzari JACM 2000 and external FRAT-XOR format (not interchangeable with /341). `konard/p-vs-np` README blob `0e0ec77f83ad6eec1719a96066108b96ac1c2a95` remains finite-machine scoped; `blkph0x/p-vs-np-proof-research` README `f397a7747eaca82df3d754d0a4b4bab1fe10f814` remains bounded/promise scoped; `meelgroup/frat-xor` format `986a21aa92b62f844ef1fce852193142c41b2b1f` documents another calculus. None authenticates the missing full grammar.

**TRACKERS REVIEWED; NO MATERIAL CHANGE**: [P2-D1],[P2-C3],[P2-B1],[P2-B2] stay OPEN. [P1-01],[P1-03],[P1-04] stay OPEN. No new proof spine arrow established. Root `main.tex` content API returned an empty body with a blob identifier, so per no-overwrite rule it was NOT modified; LSPV-5 should reconcile the evidence link after complete file recovery. No R_mix341 weights, agents, automations or route ownership changed.

**Next step:** authenticate an actual historical RES -> AND3 accepted packet or locate the full authoritative rule dispatcher. Run this exact corpus as a regression baseline, then extend a context/freshness-aware shared-DAG abstract replayer without replacing historical operations by a new parser. P versus NP OPEN.
