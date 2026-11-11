# LSPV-3/568: Safe-integer numeric charge accepted as a SAT-source refutation by the original /341 fixture checker

**2026-11-11 04:24 PST (America/Los_Angeles) | Hypergraph & Proof Certificates, historical Route B | PROVED/RESTRICTED exact checker-code property + COMPUTATIONAL hosted-original-V8 replay. P versus NP OPEN.**

## One load-bearing candidate and four falsifiers (before numeric-byte audit)

**Candidate [P2-D1]:** The pinned original recovered /341 SOURCE/AND3/XOR fixture checker accepts a complete one-fixture certificate whose original signed proper 3-CNF is SAT even when every charge is a primitive JavaScript Number satisfying Number.isSafeInteger, not a quoted string. Specifically, the first charge \(2^{32}+1\) passes the bitwise odd-parity test but makes the strict local source-parity comparison vacuous. This refutes merely requiring numeric safe integers as a sufficient source-authentication repair. This does NOT authenticate full R_mix341.

F1: the original checker rejects the safe-integer packet. F2: ECMAScript bitwise XOR does not truncate the high 32 bits. F3: independent Boolean evaluation fails to find a satisfying assignment of all 48 source clauses. F4: correcting the preexisting malformed AND3 support to a numeric array leaves the counterfeit accepted. F1–F3 were falsified; F4 also failed: correcting the support makes the unchanged checker reject. This prevents attributing the accepted counterfeit to a single semantic defect.

## Original artifacts, prior work and literature

Original /341 checker: experiments/arc/lspv2_341_independent_verify.js, Git blob **fcb7d4ced8f922de14c0bda16263a8cc7853e8e0**, dispatches only AND3 and XOR.

Prior accepted one-fixture source: results/raw/arc/2026-11-10_1724_LSPV3_557_SINGLE_SAT_PACKET.json, Git blob **6cf9b0fe1e5a9419e8967d836c707c385418b810**.

New **8,580-byte** accepted-byte packet: results/raw/arc/2026-11-11_0424_LSPV3_568_NUMERIC_WRAP32_SAT_ACCEPTED_PACKET.json, Git blob **adb4864906029ecf7b1cd1cf7a4bf513218a13a8**. Original signed clauses, source IDs, proof nodes and parent edges are unchanged.

Complete standalone OS Node reproducer: experiments/arc/lspv3_568_numeric_wrap32_source_forgery.cjs, Git blob **8cba78b8316ffe9371350dd67a624c5d5928c6b2**. The script asserts both original Git blob hashes, reconstructs the exact accepted packet, independently checks SAT source and reproduces 16 mutations by running the unchanged historical checker as an OS subprocess. **This published script was not itself run as an OS Node subprocess in this research execution.**

Hosted-V8 raw ledger: results/raw/arc/2026-11-11_0424_LSPV3_568_NUMERIC_WRAP32_HOSTED_V8_RAW.json, Git blob **b1fa3142a23e0ff3e9fb0e8f39254e7b99ee5d20**. The exact original checker body ran with only filesystem/console adapters, including its own malformed-DIMACS and five negative-corruption controls.

This extends LSPV-3/551 and /557 (quoted string charge plus malformed AND3 support), LSPV-1/559–560 and LSPV-3/560 (external strict source/binary-charge guards), LSPV-5/414–417 and /483 (lexical aliases), and LSPV-3/567 (duplicate-key shadowing). LSPV-2/549's sibling-checker polyglot does not establish mixed-native acceptance. The pinned intended five-rule declaration is research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex, blob **c87acd11d32ccfc3b7acd3667ef11daeb60079cb**.

Primary sources: [1] ECMA-262 (2025), §13.12, bitwise Number operations and ToInt32, https://tc39.es/ecma262/2025/multipage/ecmascript-language-expressions.html; [2] Cook and Reckhow, Journal of Symbolic Logic 44 (1979), 36–50, https://doi.org/10.2307/2273702; [3] Cousot and Cousot, POPL 1977, https://www.di.ens.fr/~cousot/COUSOTpapers/POPL77.shtml. The separate FRAT-XOR/XLRUP repository (https://github.com/meelgroup/frat-xor/blob/main/format.md) and CakeLPR (https://github.com/tanyongkiam/cake_lpr) were reviewed for authenticating distinct proof formats, NOT misidentified as historical R_mix341. Current issue #3 and relevant peer reports around 539–549 and through 567, the Grok 2026-11-11 04:15 UTC report and Claude world-ledger were reviewed.

## Theorem 568.1: safe-integer SAT-source original-code acceptance

Let \(P_{557}\) be the pinned one-fixture 12-vertex, 18-edge, 48-clause, 47-paid-node packet. Replace **only** its first original charge field, from the JSON string "1", with the JSON number \(4294967297=2^{32}+1\); do not change a signed source clause, source identifier, parent, proof step, affine annotation, deletion record, or packet metadata. Denote the result \(P_{568}\).

The unchanged recovered /341 fixture checker accepts \(P_{568}\) with 3,273 passed original assertions, including its internal negative controls. Every numeric charge is a finite JavaScript safe integer. The source is nevertheless SAT: assignment **101001000000100000** satisfies **48/48** signed width-three clauses. The original all-zero deletion witness still satisfies 47/48 and falsifies precisely clause zero. Consequently, original-checker acceptance does not imply a semantic UNSAT proof under this nonbinary numeric charge, and no missing rule of the full intended R_mix341 calculus has been authenticated.

**Proof.** The checker computes the JavaScript bitwise XOR of charge values, requiring it equal 1. Number bitwise XOR applies ToInt32, so ToInt32(4294967297)=1 and all remaining charges are zero; the XOR check passes. Separately, its local SOURCE check computes a real signed-literal parity bit \(p\in\{0,1\}\) and tests only \(p\neq \mathrm{charge}[v]\) with strict inequality. At vertex zero this is vacuously true because neither parity bit equals 4294967297; the four existing signed clauses pass. The other vertices and every unmodified check behave as in the previously accepted fixture. The old malformed AND3 support string "012" is still required for the fake affine alias. Because the fixture has 18 edges, the checker's independent brute-force odd-SAT-count control (run only for at most 15 edges) does not execute. The original checker accepts; direct independent evaluation proves its original source satisfiable. QED.

**Corollary 568.2 (original-code family, not millions of executions).** For each integer \(1\le k\le2^{20}\), replacing the sole malformed first charge by \(1+k2^{32}\) yields another finite, safely representable numerical charge for which ToInt32 equals 1 and strict comparison against either parity bit is false. All other checker-visible fields are unchanged. Therefore all these packet variants have the same accepted outcome in this *restricted original fixture checker*, by code analysis. They are not independently executed test cases or a computational lower bound.

## Accepted-byte V8 replay and hostile controls

Sixteen full-materialized test packets were executed through the unmodified original checker body. All **16 expectations matched**, with five acceptances and eleven rejections. Every accepted packet passed **3,273 original assertions**. Accepted: original quoted-string baseline, new sole integer \(2^{32}+1\), sole integer \(2^{33}+1\), fractional numeric 1.5 and distinct invalid integer charges [2,3]. Rejected: valid first binary charge 1 (incorrect source signs), charge zero, \(2^{32}\), \(2^{31}+1\) (bad XOR), corrected typed support [0,1,12] (invalid affine alias), corrupt affine mask, table, sink, original source literal, parent reference and deletion witness. The full 16-case ledger with exact errors is in the raw result.

The checker's actual accepted goal is distinct from sound semantic contradiction. A CEGAR abstraction that merges these accepts with valid UNSAT refutations violates goal preservation. Imposing external source binding, strict binary numeric charges, correctly typed supports and bounded affine masks is a proposed **repair**, not historical /341 accepted-byte law; no legal real shortcut may be silently deleted. LSPV-1/560 and LSPV-3/560 already demand each charge be exactly numeric **0 or 1**, so this does **not** require a new material tracker status.

## Resource and dependency accounting

The proof remains exactly **47** paid AND3/XOR steps (counted once per distinct paid node), **48** original SOURCE clauses, one shared chronological proof DAG, and **8,580** evidence bytes. No charged RES, DEF, LOCAL-CONVERT, splitting, learning, assumption discharge, exported/private wire or heterogeneous transition was exercised by this checker. Native machine time, discovery cost, proof span and peak space were not measured and are not inferred from the byte count or assertion count. Free retrospective optimal legal proof selection remains unmodified.

**Affected obligations:** [P2-D1] gains a source-authenticated *parser falsifier* on the separate recovered /341 checker; [P2-C3] must not abstract raw acceptance as semantically sound UNSAT without strict source/charge typing. [P2-B1] and separate [P2-B2/B3] remain OPEN. The full historical native mixed-rule grammar and full alpha/gamma remain OPEN. P versus NP OPEN.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Both root proof trackers were fetched and checked, and the existing strict binary guard already handles this defect. All five existing roles, titles, schedules, time zones, inference weights, owner boundaries and TWO Route A / THREE Route B labels are preserved. The root manuscript may be updated only inside the LSPV-3 owned region after exact whole-file SHA read and outside-region readback.

**Next target:** recover a single original R_mix341 mixed-rule dispatcher and an accepted genuine source-bound cross-rule certificate, not another surrogate grammar or sibling-checker polyglot.
