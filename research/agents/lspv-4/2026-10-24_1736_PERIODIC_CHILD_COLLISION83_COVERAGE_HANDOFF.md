# LSPV-4 PERIODIC-CHILD-COLLISION83: additive five-role proof-gap and coverage handoff
Timestamp: 2026-10-24 17:36 Asia/Seoul. **P versus NP OPEN.** Independent review pending. All existing task schedules unchanged.

## Exact new result and predecessor correction
For M=2^h proper ordered 3-CNF with n=6, N=(4M+2)ceil(log2(64(M+7))), odd K=Theta(sqrt(N)/log N), p=2^ceil(log2(8K)), g=p/8>K, Q=min(M,floor(N^(3/5))), select K consecutive clause indices starting at jK mod M.
Construct opposite-label periodic parents U_M and V_M: filler clause D=(u OR v OR w) except at positions a*g mod p, a=0,...,7. Put all eight signed core clauses C_a on x1,x2,x3 in U_M, but replace C_7 by C_6 in V_M. Every clause is proper ternary. Source model counts are (0,7).

**PROVED/EXACT restricted:** each selected child contains at most one core record, so exact six-variable child model counts are 56 if filler-only or 49 if containing one core. The complete ordered vector of Q child counts is identical for UNSAT U_M and SAT V_M. Every child is SAT. No status-only or isolated-count-only parent-label reconstruction can succeed on both inputs.

**PROVED/EXACT restricted:** the Q clause index sequences are distinct, yet only 1+8K serialized child bitstrings occur on U_M and 1+7K on V_M, for Q>=p. A flat fixed-address canonical child buffer changes at most six literal fields from one selected child to the next. The original predecessor CYCLIC-VIRTUAL-SELECTOR82 unqualified phrase "Q distinct ordinary children" needs correction to **Q distinct ordered index selections**: an all-identical-clause M=16,K=3 valid source has 16 selections and ONE child encoding. Predecessor's separate Omega((Q-1)K) flat-write theorem had an **explicit all-records-distinct premise**, so that conditional theorem is not refuted.

This counterexample refines the status-only MINIMAL-UNSAT-PROJECTION20 counterexample by showing identical complete isolated **model-count** transcripts, while leaving real source/child-bit inspection and cross-child compatibility available to adaptive algorithms. No unrestricted time LB follows.

## Reproducible tests
- Program: research/agents/lspv-4/2026-10-24_1736_PERIODIC_CHILD_COLLISION83_MINI.py (standard-library, zero random seeds).
- Raw: research/agents/lspv-4/2026-10-24_1736_PERIODIC_CHILD_COLLISION83_RAW_SUMMARY.json.
- Full locally run auditor also checked complete signed fixed-width serialized bitstrings and all source/child 64-assignment truth tables: 7098 child checks, 8 source checks, zero failures. Do not assume the extended transient local file is accessible to peers; the compact GitHub auditor reproduces the essential results.
- M,N,K,p,Q,D_U,D_V,flat-changed-fields:
  256,15390,7,64,256,57,50,1341;
  512,32800,11,128,512,89,78,2109;
  1024,69666,15,128,805,121,106,4524;
  4096,311334,29,256,1976,233,204,10740.
- All selected children SAT on both sources. Even their model-count vectors coincide at each j. Finite computations do not prove general hardness.

## Adaptive-state BIT-RESOURCE1 ledger
Input has read-only source n,M and no label advice. A total uniform policy may parse M,N,K,p,g, attempt both canonical grammars with logarithmic writable counters and flags, scan all expected signed clause records, and then output SAT or UNSAT directly, with arbitrary exact DPLL fallback on unrecognized inputs. On the canonical families this costs O(N polylog N) primitive bit work and O(log N) peak work bits; fallback has no favorable universal bound. All source reads, policy checks, index arithmetic, unchanged writes, failed recognition, potential caches, child buffers, control/head flips and cumulative bit-time are distinct channels. The finite menu is not an all-decider coverage claim.

## Proof spine, statuses and external endpoint
FILLED: exact content orbit, exact model-count collision, narrow correction to predecessor wording.
PARTIAL/RESTRICTED: cyclic virtual bit service, fixed-buffer literal write ceilings, source grammar recognizer.
FALSIFIED/RETIRED: unqualified child-bitstring uniqueness from distinct index sets; unqualified QK rewrite LB without record distinctness; parent SAT inferred from isolated child counts.
OPEN: all-input both-label semantic reconstruction with exact charged simultaneous time-space contraction; cofinal finite-hit ARC to FLMV.
KNOWN: FLMV Corollary 5.8, in its original random-access Turing model, excludes t<241/200, s<11642479/23232400. Prior 2cos(pi/7) universal SAT product endpoint remains retired.

## Coverage manifest and gaps
- Inherited pinned 3532-file GitHub hash/keyword crawl at 55a3fcc10f74419c9c3e1a577ed0f8ce83e2f640. No claim of complete body review.
- Direct full GitHub reads: CYCLIC-VIRTUAL-SELECTOR82 report blob 265eba9c5b2e80be7f9405e39f13da6e49818acd; AGENTS.md blob c5265db06c0febdb07fd99759b14b1ee845654a2; CODEX.md blob 754999f50de93cdb693ed37bc8110d31e9e698ef; repo skill blob b8df83a7b0b1428f349b0e02ce1387d979e8db7f; main13.tex blob 87dbaad5e18932b1db7fca57fc40e0ac020a6f49; root main.tex read at SHA 53bc5ab7e303eb607700995253a636236851f48f before publication; original Drive ARC existential-region document 1QirzuNPCG-CrE3EX6WweqsPdDbtoblCDEE4YI0HGyC0 and continuity document 1TselU5xLzVf7nbD2R0r-XZz_8t-S_WNrkiOZxNpbR5E.
- Selected peer handoffs read: Role 1 VIRTUAL-FENCE124, Role 5 TYPED-LEGAL-POTENTIAL123, Role 2 FALLBACK-PADDING118, Role 3 STREAM-WITNESS-BITTIME86. Repo search queries included periodic deletion children, periodic selector, child model-count transcript, MINIMAL-UNSAT-PROJECTION20, EAGER-LAZY-FRONTIER34, CACHE-MISS-FRONTIER18, PC22_ALLFIELD1. Search matches are not full proof reviews.
- Existing work distinguished: MINIMAL-UNSAT-PROJECTION20 already refuted status-only reconstruction; SELECTOR-CAPACITY81 distinguished all-selector descriptor support; CYCLIC82 supplied arithmetic child access; Role 5 corrected typed bit flips. Nothing here transfers CP22/PC22 proof-system/query lower bounds to arbitrary SAT decider running time.
- Still unread/unavailable: original HEREDITARY-SCOPED10 executable (Drive continuity log has restricted summary only), full Drive LOG/PROVED_EXACT/BOOL/SIL pagination, and many selectively indexed GitHub proof bodies. Do not infer absent result from inaccessible locations.
- Next experiment: independently verify whether a proposed scoped-interface gluing procedure can distinguish these parents without a global source scan, using complete counted source bit reads, compatibility witnesses, boundary caches, headers and same-machine peak space. Inspect HEREDITARY-SCOPED10 original code if located.

Report: research/agents/lspv-4/2026-10-24_1736_LSPV-4_PERIODIC_CHILD_COLLISION83.tex.
No GitHub files of other roles intentionally changed; only LSPV-4-owned root reconciliation is authorized. Independent review/consumption remains unconfirmed.
<!-- END_OF_VERIFIED_HANDOFF::LSPV-4::PERIODIC-CHILD-COLLISION83 -->
