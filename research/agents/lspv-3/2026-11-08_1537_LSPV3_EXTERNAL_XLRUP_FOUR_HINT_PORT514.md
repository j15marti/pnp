# LSPV-3/514: Four-hint XLRUP certificate interface versus historical R_mix341

2026-11-08 15:37 PST | Route B | PROVED/RESTRICTED formal construction; COMPUTATIONAL independent exact-format-subset checks; P versus NP OPEN.

Proof-chain evidence: new [P2-L3-514], refining [P2-D1], [P2-D3], [P2-C3], [P2-L3-499], [P2-L3-509], [P2-L3-513] and historical checker scope [P2-L5-413]. [P2-B1], [P2-B2], [P2-C3] and [P2-D1] remain OPEN.

## IDEA: one precise hypothesis and four falsifiers

Hypothesis: the four signed *original* 3-clauses of each cubic odd-Tseitin vertex, taken with their original IDs, are an exact set of XLRUP clause hints for the published four-premise XOR-from-clause macro (the XLRUP i x record). Their balanced XOR sums produce the contradictory empty parity equation. This yields an explicitly charged external-format upper-bound control, while exposing a type/arity mismatch with the historical two-antecedent R_mix341 calculus.

Falsifiers registered before source review: (F1) at least one signed original clause quartet fails the strict XLRUP covering test; (F2) XOR sign orientation or shared sums fail to produce 0=1; (F3) altered original clauses, missing/foreign hints or corrupted XOR records pass independent verification; (F4) exact historical native accepted-byte grammar already makes the same four-source macro a legal *single unit-cost* R_mix341 inference. F1-F3 were tested and did not fire. F4 remains unestablished, not counted as a negative test.

## SEARCH: governing files and actual source scope

Full main proof1.txt blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b, 18,553 UTF-8 characters, and proof2.txt blob 4ae2add2ae19febfc780e22ad0d45dbaf5123d88, 534,420 characters, were read before this run's writes. Read current issue #3 including recent LSPV-1/517 and LSPV-2/505 comments; historical five-agent refocus 2026-11-02_1204 at stated pinned commit; AGENTS.md blob 19656af..., CODEX.md 754999f..., pnp-research skill b8df83a...; original R_mix341 declaration research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex blob c87acd11..., original recovered checker experiments/arc/lspv2_341_independent_verify.js blob fcb7d4ce...; LSPV-1/349 source-excess Euler identity 407c00e..., LSPV-3/512 bridge-star 9dddd8c..., LSPV-3/513 6f1e40f..., LSPV-5/413 historical-parser audit a80ba040..., LSPV-1/517 ca05459.... Actual Grok report GROKPROOF/2026-11-08_1130_PROGRESS.md blob 6942a99..., Claude world-ledger research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex blob 79e4d4e... were read.

Required external change-aware reads: konard/p-vs-np scripts/proof_status.json blob 93b77ed3 and proofs/complexity/README.md 7ee9a11e; blkph0x/p-vs-np-proof-research METHOD_INDEX.md 18d693ea and REVIEW_ADDENDUM.md 6a7cc2f8. Both are scoped exploratory claims, not authority for native R_mix341. Read meelgroup/frat-xor format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f, including strict XLRUP i x / i cx rules, cake_xlrup/example.xnf blob 80a25baf and example.xlrup blob cd550705, and cake_xlrup/README.md c71de809; tanyongkiam/cake_lpr README.md e94f45e9; peitl/short-proof README.md 93d2090d; openai/math README.md cc5b0a03. None authenticates historical R_mix341 mixed RES/DEF/LOCAL input types. Web queries checked Urquhart 1987 expander-Tseitin Resolution, XLRUP strict XOR hints, and clausal proof case-split lifting. No separate Google-branded interface was used.

Known primary result (model qualified): Urquhart, JACM 34 (1987), 209-219, DOI 10.1145/7531.8928, and Ben-Sasson/Wigderson, JACM 48 (2001), 149-169, DOI 10.1145/375827.375835, give exponential ordinary shared-DAG Resolution lower bounds on appropriate odd-charge bounded-degree expander Tseitin families. These finite K4/K3,3/cube/prism controls are NOT claimed to themselves form a certified expander hardness family. Cook/Reckhow JSL 44 (1979) is the standard fixed-proof-system qualification.

## ITERATE: source-authenticated typed construction

Take any connected simple cubic graph G=(V,E), h=|V|, n=3h/2, odd vertex charge chi. At every vertex v, include the four original signed strict 3-CNF clauses forbidding the incident-edge assignments of parity different from chi(v). Therefore m=4h source clauses. The original serialized source has O(h log(h+2)) bits.

Published external XLRUP strictness (meelgroup/frat-xor/format.md): an XOR-from-clause step i x requires every CNF-encoding clause of its claimed XOR to contain at least one listed hint clause; it does NOT perform free Resolution among hints. Here each vertex's four original clauses are EXACTLY its parity equation's four CNF-encoding clauses. So one source-hinted i x step per vertex passes that strict *external* four-source check, with independent original clause IDs.

Aggregate h rows in a balanced tree of h-1 binary XLRUP x steps. Each edge occurs in exactly two vertex rows, and the charge XOR is one, so the root is 0=1. Export the empty clause with one strict i cx step. Thus an external format trace has exactly

$$
q_{\mathrm{XLRUP\ records}}=h+(h-1)+1=2h
$$

records. This is NOT the historical R_mix341 weighted minimum. Each XLRUP i x record consumes four source hints, whereas the historical R_mix341 paid native clauses/AND3 and every derived node are limited to at most two named antecedents. The original source/AND3/XOR certified historical derivation uses 4h-1 paid nodes. One cannot substitute an external multi-hint record as a single historical unit-cost inference without proving a legal charged simulation. Historical RES, DEF, LOCAL-CONVERT, exported/private wires and assumption discharge still lack a complete accepted-byte checker.

At each balanced-tree level, disjoint vertex subsets imply that an edge variable appears in at most two partial rows. Total displayed row-literal appearances at that level are <=2|E|=3h. With O(log h) levels and O(log h)-bit numbered variable/source/node IDs, the original source and explicit textual external trace use O(h log²(h+2)) bits. Ideal external step-depth <=2+ceil(log2 h) in a unit-record, unlimited-processor model. Dense BigInt row tables can separately require O(h²) bits and bit operations; source parsing, hint checking, constructor, verifier, output, caching, failures, and machine peak storage have not been treated as unit-cost free operations.

## Independent reproduction and hostile controls

Published JavaScript experiments/arc/lspv3_514_xlrup_bridge.js blob 6dc6b857a22c99c20ba8c57103025dacd2b3a68b was executed in V8, fetched from GitHub after commit, and the FULL READBACK BYTES were independently executed again with identical results. Independently written Python checked the same format subset, source hashes, all 3-CNF signed literals, XOR equations, strict covering hints, final contradiction, and generated actual text CNF and XLRUP candidate files. This is an independent implementation of the published *format specification*, NOT execution of formal CakeML cake_xlrup. The full independently written Python, six source/proof pairs, and detailed raw are supplied as a conversation fallback archive with SHA-256 45a0f29852a4eea14f0d681d8ca88dbba1885df57701853b39694ad926de23f1.

| Graph | h | CNF bytes | XLRUP bytes | External records |
|---|---:|---:|---:|---:|
| K4 | 4 | 163 | 174 | 8 |
| K3,3 | 6 | 239 | 289 | 12 |
| Cube | 8 | 340 | 395 | 16 |
| Prism8 | 16 | 740 | 938 | 32 |
| Prism16 | 32 | 1541 | 2085 | 64 |
| Prism64 | 128 | 7086 | 10993 | 256 |

Both implementations rejected 8 corrupted/negative controls per graph, 48 independently per implementation: signed source tamper, omitted source hint, alien hint ID, incorrect XOR RHS, nonexistent XOR parent, incorrect XOR sum, false clause export, and even-charge SAT noncontradiction. Python exhaustive deletion SAT controls also passed for K4, K3,3 and cube. Largest case Python control+verification wall time 0.139 seconds and tracemalloc peak 261,594 bytes; host interpreter RSS, source head/network reads and GitHub writes are additional. No native Turing-machine time/space exponent is claimed.

The external verified checker cake_xlrup and historical full /341 mixed checker were NOT executed on these external traces. They remain candidates for actual checker replay, not verified native checker-accepted certificates.

## Scientific outcome, model barrier, and publication status

The material new artifact is an original-source-authenticated **external-format four-source interface control** with an exact 2h-record external construction and concrete strict-hint parser replays, plus a typed obstruction to treating those external records as native unit-cost R_mix341 inferences. This is not an academic novelty claim, not a complete transfer and not an all-rule lower bound. It does not establish B3 or all-input SAT hardness.

[P2-D1] historical full grammar, [P2-C3] complete mixed normalization, [P2-B1] superpolynomial all-rule minimum, and [P2-B2] noncircular same-calculus B3 remain OPEN. No alteration of historical weights/rules, the five agent roles, schedules, enabled states, 2 Route A / 3 Route B allocation, or root main.tex. **P versus NP OPEN.**
