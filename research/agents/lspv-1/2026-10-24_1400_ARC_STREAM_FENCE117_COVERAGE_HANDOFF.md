# ARC-STREAM-FENCE117 | LSPV-1 shared proof-gap handoff

Timestamp: 2026-10-24 14:00 Asia/Seoul. P versus NP remains **OPEN**. This is an additive audit, not a replacement for the previous ARCARCHIVECURVE90 coverage manifest. Schedules and task counts were not changed. No external messages were sent.

## Exact new receiving lemma and status

**ARC-STREAM-117: PROVED/EXACT conditional FLMV firewall, not ARC-EDGE-90.** Suppose one fixed total uniform FLMV-model transducer converts every ordinary SAT source of encoded size N into an equisatisfiable valid active-slot 3CNF event stream of bit length M <= N^(mu+o(1)), live width w <= kappa log2 N + o(log N), producer time N^(r+o(1)), and peak work/index space N^(sigma+o(1)). An online exact existential frontier DP on its one-way output yields a **single** all-input SAT decider with joint exponents (max(r,mu+kappa), max(sigma,kappa)). If there is c>max(1,r,mu+kappa) with max(sigma,kappa)<beta(c), beta(c)=((c+2)/c^2-c)/2, FLMV forbids the transducer. Output is intercepted online, never stored as an uncharged ordinary child. Global input IDs are not supplied: stream uses canonical active slot indices.

Examples: mu=1, kappa=0, r=11/10, sigma=1/2 cannot all hold. Nor can mu=23/20,kappa=1/40,r=11/10,sigma=1/2. At mu=11/10,kappa=3/20,r=11/10,sigma=3/20, curved witness c=13/10 also forbids the producer even though time exponent 5/4 is outside the old fixed 1.205 box. The impossibility is derived from FLMV Corollary 5.8 and Theorem 3.1, confirmed directly from the author PDF with visual inspection of pages 6 and 18 (1-based). This does **not** show arbitrary polynomial-time low-frontier normalization impossible if its time/space lie outside the box.

**ARC-PURE-117: PROVED/EXACT family-relative generic escape.** Role 2 FLMV-CURVE-FRONTIER115's K_h edge clauses (x_i OR x_j OR z_ij) have private pure positive z_ij. A paid pure-literal scan deletes all binomial(h,2) edge clauses and the positive d bridge/filler, leaving 7 SAT or 8 UNSAT core clauses. At h=32 the unchanged-clause maximum frontier observed is 33, but reduced width is 3 and the residual DP uses at most 8 rows. This does not undermine Role 2's unchanged-clause width theorem; it refutes any unjustified translation to mandatory work against adaptive source-aware deciders.

**ARC-EDGE-90: OPEN.** No all-input reachable exponent-pair successor has been constructed. A normalizer for certified streams is not a normalizer for arbitrary ordinary SAT. A proof of the abstract existential closure is itself equivalent to P!=NP given FLMV, as independently established by Roles 3 and 5; it is not a cheaper missing lemma in logical strength.

## Reproducible audit and adaptive-state ledger

Expanded local full-body audit in this run: seed 202610240600; 254 instances; 186 SAT and 68 UNSAT; 18,519 assertions and 0 failures. Source-level choices: pure (98 cases), all-false witness (40), complementary-pair contraction + SCC (17), exact residual frontier DP (99). Both labels included on padded 2SAT, affine XOR3, complete signed 3CNF core, random proper3CNF and K_h families. Above h=5 the K_h label follows the proven constant core, not exhaustive search over all input variables. GitHub contains a separate complete compact minirepro and a machine-readable results summary. Do not conflate the compact minirepro's assertions with the expanded 18,519-assertion audit. The expanded audit and full raw row ledger were also created in the current execution's local container but are not inherently cross-runtime shared.

State 0: acquired full signed source clauses by charged parsing; no label oracle.
State 1: sign-occurrence counts; source-aware pure-literal deletion, with failed recognition/scan charged; raw source still retained.
State 2: remaining formula and observable parameters (clause count, signs, pair structure). Try all-false witness, then valid complementary-clause contraction + 2SAT SCC, otherwise streaming DP.
State 3: SAT/UNSAT decision confirmed by independent brute evaluator on small controls; peak logical workspace includes retained source and table, not a claimed FLMV <= N^1/2 space implementation.
The algorithm menu is an experimental restriction; it does not cover all computable uniform policies.

## Source and coverage delta, no false exhaustion claims

Full exact source bodies read this turn:
- root main13.tex (blob 87dbaad5e18932b1db7fca57fc40e0ac020a6f49)
- root main.tex (read blob 97764e03cbbd455b9c0387fba10d2bfea6e673d7, selected sections actually audited)
- original FINAL-LINK-ARC at pinned commit 55a3fcc10f74419c9c3e1a577ed0f8ce83e2f640
- LSPV-1 ARCARCHIVECURVE90 report plus cumulative handoff
- LSPV-2 FLMV-CURVE-FRONTIER115, latest constructive obstruction
- LSPV-3 ARCHIVE-ARC-SEMANTIC82 and BOUNDARY-TREEWIDTH81
- LSPV-4 BALANCE-HEADER-ORACLE79 plus handoff
- LSPV-5 COFINAL-QUANTIFIER-ENDPOINT116
- MAIN108 weighted transcript source-acquisition firewall
- Drive 1QirzuNPCG-CrE3EX6WweqsPdDbtoblCDEE4YI0HGyC0, Sep 27 ARC ancestor (22,010 extracted chars)
- Drive 1VwhU6bMDlsy9rTI4EOTN4gNipVL8e-jJPO9Wg3oWByU, Oct 21 ARC-FRONTIER21 (5,540 extracted chars)
- Drive 1TselU5xLzVf7nbD2R0r-XZz_8t-S_WNrkiOZxNpbR5E, continuity log (51,034 extracted chars)
- FLMV original author PDF https://lance.fortnow.com/papers/files/tst.pdf sections 2,3,5 plus successful screenshots on pages 6 and 18.

Search exact name ARC-HEREDITARY-SCOPED10 with Drive metadata-only paging: 1 returned continuity log, no next-page token, not the full original. ARC-FRONTIER21 exact-name metadata returned two Docs, one with title ARC-UNANNOTATED-JOIN22. The latter was fetched but its text extractor returned zero paragraphs. Treat this as missing content, not a mathematical no-go. GitHub role directories were listed and latest sources fetched; metadata folder listings are not exhaustive manuscript analysis. The user-supplied pinned 3,532-file full-byte / keyword check was *inherited*, not repeated. Historical main2-main12, older fallback revisions, Drive LOG/PROVED_EXACT/BOOL/SIL and named full HEREDITARY-SCOPED10 executable remain on unread queue. No automatic inference of archive absence.

## Canonical gap IDs, status, and receiving obligations

- ARC-EP-90: FILLED as a KNOWN THEOREM, matched FLMV curved endpoint and strict margin.
- ARC-FH-90: FILLED mathematical meta-implication, separation-equivalent, not an algorithm.
- ARC-STREAM-117: FILLED conditional impossibility in a source-typed streaming-normalizer model. Does not imply the same for arbitrary ordinary-CNF or symbolic outputs.
- ARC-PURE-117: FILLED generic pure-literal shortcut against raw-width lower-bound transport.
- ARC-FRONTIER-90: PARTIAL/RESTRICTED, exact source-scoped DP/child semantics, no all-input normalizer.
- ARC-UWI-90: PARTIAL/RESTRICTED witness-cost equivalence, no joint resource successor.
- ARC-DNNF-90: FALSIFIED/RETIRED as generic mandatory representation transfer.
- ARC-OLDEND-90: FALSIFIED/RETIRED universal cosine product criterion.
- **ARC-EDGE-90: OPEN**: all-input source-valid joint time-space successor (or finitely justified cofinal route) for ordinary exact SAT, allowing all adaptive symbolic approaches.

## Peer handoffs and next exact test

Role 2: its all-order unchanged-clause bound remains exact but the generic pure-literal deletion bypass must be listed as an escape. Explore whether a source-independent finite stream normalization can survive the ARC-STREAM-117 time-space firewall.

Role 3: audit the one-way online producer-plus-DP FLMV machine simulation, particularly output event parsing, canonical active slot indices, and peak index tape space. Keep ordinary-3CNF to full FLMV SAT reduction as a separate proof obligation.

Role 4: apply the guarded endpoint to PC22_ALLFIELD1 header-bit streams; retain source acquisition, output length and source-ID index costs. Check normalizer tradeoff rather than transferring field-query cost to arbitrary SAT decision.

Role 5: integrate the new firewall and source-aware bypass without promoting ARC-EDGE-90. Keep cofinal conditional route equivalence credited to Role 3/5, and the previous pinned corpus coverage manifest.

**Single next artifact:** recover complete original HEREDITARY-SCOPED10 body (not just the continuity paragraph), and explicitly test one arbitrary high-width non-affine ordinary SAT source under any proposed source-accessible normalizer, charging both correctness and same-machine time/space. No all-input favorable route is currently established.

Publication paths: research/agents/lspv-1/2026-10-24_1400_LSPV-1_ARC_STREAM_FENCE117.tex, same prefix _minirepro.py, _results_summary.json and this _COVERAGE_HANDOFF.md. GitHub report, compact executable, raw summary and this handoff were each verified by readback. Root main.tex was reconciled solely in the LSPV-1-owned region, then read back at commit `3df21b0844131dec0849e7f138b9f886aa055876`, content blob `93b3943a1a679730e4b8435677b2ae6ad856d0ca`. All five ownership marker pairs were balanced; global OPEN status was preserved.
