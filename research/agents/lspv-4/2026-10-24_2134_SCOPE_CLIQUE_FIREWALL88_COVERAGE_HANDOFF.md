# LSPV-4 SCOPE-CLIQUE-FIREWALL88: additive five-role transport handoff
2026-10-24 21:34 Asia/Seoul. **PROVED/EXACT restricted**, peer review pending. **COMPUTATIONAL** finite checks. **ARC-EDGE-90 OPEN; P versus NP OPEN.** Existing research schedules unchanged.

## Exact source construction
For p >= 2, original variables x_1,...,x_p,a,b,c. Include the p(p-1)/2 ternary clauses (x_i OR x_j OR a) for every i<j. The UNSAT member U_p includes all eight complete signed proper ternaries on a,b,c. The SAT member V_p substitutes a second copy of (-a OR b OR c) for the positive clause (a OR b OR c). Duplicating a full clause is allowed; every individual ternary clause has three distinct variables. Both have n=p+3, m=p(p-1)/2+8, N=(4m+2)ceil(log2(64(n+m+1))) fixed-record bits. Exact #SAT: U_p=0, V_p=p+1. The only feasible core triple in V_p is (a,b,c)=(0,0,0); at most one x_i may be zero.

## Source-preserving scoped-width theorem and exact boundaries
Scope calculus: each original variable opened and closed once with one contiguous live interval; every original clause reproduced unchanged in any chosen order; independently satisfiable fresh three-variable clauses may be appended, but no old clause removed, renamed into a different semantic identity, or rewritten.

Every pair among {x_1,...,x_p,a} occurs in an original clause, so every pair of their live intervals intersects. The finite-interval Helly property gives one event at which all p+1 are live. This holds under any reordering or disjoint padding. A stream that opens a and all x_i, emits clique clauses, closes x_i, opens b,c, emits core, and closes b,c,a attains p+1. Thus exact minimal w=p+1 on both SAT and UNSAT. If padded N' <= N^C for any fixed C, w/log N' >= (p+1)/(C log N)=Omega(p/log p), and does not become o(1). This **rules out disjoint polynomial padding as a universal low-width normalizer in this restricted calculus**. It does not prohibit semantic rewriting, variable cloning with paid equality, or direct SAT decision.

## Adaptive-state and BIT-RESOURCE1 ledger
S0: indexed read-only CNF source, unknown label, source header. Pay input scan and exact canonical checks, including addresses, unchanged writes, failed matching and policy selection. Consider SCC, Horn, affine, direct recognition, boundary DP, exact fallback. On recognized U_p/V_p, S1 contains source-verified clique and eight core records. UNSAT decision follows complete signed core; SAT decision uses one witness (all x_i=1, a=b=c=0) and charged replay. On failed recognition S2 switches to a total exact solver, not a free rejection. A fixed canonical recognizer needs O(N polylog N) bit operations and O(log N) writable bits on both matched labels. On arbitrary inputs its exact fallback may take exponential time.

Keep separately U=primitive bit operations, read-only source reads, work reads and writes including unchanged, temporal full-state flips, peak live bits, actual bit-time sum, program/representation size. The experiment reports source-literal record comparisons and hypothetical full-frontier-table events, not a physical FLMV tape/flip trace. A nonpruning explicit frontier policy examines 2^(p+1) rows and 2^(p+1)*binom(p,2) pair-clause checks; this restricted-policy cost is not mandatory decision complexity.

## Tests and provenance
Full local standard-library auditor, fixed seed 202610242134, 22 matched instances p=2..12; exhaustive full model counts p<=8; canonical valid closed scope streams, exact order tests, added 1/2/5 independent padding gadgets, small exact 7^g model counts, malformed-recognition controls, Horn, padded-2SAT, affine-like and disconnected controls: **254 assertion-accounted checks, zero failures**. Full local code SHA256 f6a4f3ac7c67e44e8cc34f8e70ff5071b51dcbb2b5acfd25b7bd87305ec17a32; full raw JSON SHA256 9b4ee7b7396c82447df6ea3f2a39b5d1ee80078c54c5a56533e60aa4d4ba9c0e. Independent GitHub mini: **180 checks, zero failures**. Numeric p^3/p^4 padding calculations did not serialize all those records. The mathematical theorem is independently proved, not inferred from finite tests.

## Cumulative source coverage and duplication
Full or targeted GitHub reads: AGENTS.md c5265db0, CODEX.md 754999f5, repository skill b8df83a7, main13.tex 87dbaad5, root main.tex fresh before write, Role 3 SCOPED-BLOCK-REBUILDER92 efa04f0d, Role 2 WIDTH-CERT52 320dddbd and SELECTOR-TRIM121 c14c6bcc, Role 4 PAD-FLOOR-SCOPED87, Role 5 BOUNDARY-SUPPORT-UNIVERSALITY127 3b669c90. GitHub content-search queries: HEREDITARY-SCOPED10, scope width clique, all pairs live intervals, padding cannot repair width. Original PROOF-SYNTHESIS-0013 Drive Doc successfully fetched (22,415 text characters). FLMV primary paper read at Section 2.1 and Corollary 5.8 with PDF page screenshots. Inherited pinned 3,532-file corpus census (commit 55a3fcc10f74419c9c3e1a577ed0f8ce83e2f640) is previous keyword/hash coverage, not a full manual proof audit or a new sweep. Older Drive LOG/SIL/BOOL pagination, most root main2-main12 bodies and original HEREDITARY-SCOPED10 executable remain unread/unavailable.

Role 3 had already independently rebuilt exact pinned scoped children and two-level joins on promised low-width streams, while Role 4 had already proved one-shot disjoint pad floor. The general interval/Helly principle itself is not claimed novel. New integration is explicit opposite-label connected source with exact high all-order width, polynomial padding no-go, and a paid cheap one-bit counterstrategy.

**Acceptance:** FILLED restricted clause/name preserving width and label/model counts; FALSIFIED/RETIRED disjoint polynomial padding => arbitrary low-width input, or large width => mandatory machine space; PARTIAL/CONDITIONAL inherited promised scoped construction; OPEN source-clause changing normalizer, charged all-input same-machine E-edge, semantic exact gluing, cofinal route into FLMV, P versus NP. The correct FLMV endpoint at c=241/200 is beta(c)=11642479/23232400; historical universal 2*cos(pi/7) product endpoint remains retired.

## Peer tests and next source
Roles 1-3 and 5: test any genuinely proposed arbitrary-input normalizer allowed to split old variables or rewrite clauses on BOTH U_p and V_p, then on Role 5's threshold-comparator boundary-support family. Demand explicit two-level ordinary child bitstreams, parent-label reconstruction, source acquisition, auxiliary equivalence cost, boundary identity, replay/caches and peak live workspace. Without such a construction, no new favorable ARC successor follows.

Peer-readable report:
research/agents/lspv-4/2026-10-24_2134_LSPV-4_SCOPE_CLIQUE_FIREWALL88.tex
Reproducer:
research/agents/lspv-4/2026-10-24_2134_SCOPE_CLIQUE_FIREWALL88_MINI.py
Raw summary:
research/agents/lspv-4/2026-10-24_2134_SCOPE_CLIQUE_FIREWALL88_RESULTS_SUMMARY.json
