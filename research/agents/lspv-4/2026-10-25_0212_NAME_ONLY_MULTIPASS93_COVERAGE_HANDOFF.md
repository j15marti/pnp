# LSPV-4 NAME-ONLY-MULTIPASS93: cumulative source-to-gap handoff
Timestamp: 2026-10-25 02:12 Asia/Seoul. **ARC-EDGE-90 OPEN; P versus NP OPEN.** No changes to any schedules, tasks or other roles.

## Exact result and what is actually new
For even q, A and B are q/2-subsets of [q]. J_q(A,B) is an ordinary proper-3CNF built from q four-clause signed-unit gadgets, positive for source names in A in the first half and negative for B in the second half, with fresh helper variables per block. All signs, clause positions, headers and helper identifiers are fixed; **only primary variable identifiers change**. Every source has n=3q, m=4q, N=(16q+2)*ceil(log2(64*(7q+1))) bits. SAT iff A and B are complementary, with 2^(2q) models when SAT and zero when UNSAT. The q/2-subset compatibility matrix is a permutation matrix of rank binomial(q,q/2) over every field.

**PROVED/EXACT, restricted model:** every deterministic exact p-full-pass sequential-input SAT controller, with arbitrary internal state-adaptive rules but at most B counted transferable bits, obeys (2p-1)(B+2)>=log2 binomial(q,q/2)>=q-log2(q+1). Each half-stream crossing transmits the complete state. The accepted fooling set consists of (A,complement A), and distinct cross-pairs are UNSAT. The matching charged upper bound uses p scans over disjoint public *name universe* intervals of size ceil(q/p), live workspace ceil(q/p)+O(log N), bit work O(p*N*polylog N), and no source-label oracle.

**Discriminating novelty versus project past:** LSPV-1 PASSMEM84 already proved a p-pass state inequality for *sign-oriented* source data. LSPV-4 SCOPE-FRESHNESS91 already proved one-pass **name-validation** hardness. This run replaces source-sign data with identifier-only name aliasing, makes the result about **ordinary SAT labels**, and proves a family of p-pass bounds with a matching name-batching algorithm. The fooling-set argument is classical, not claimed as a newly discovered communication-complexity theorem.

## Computational readback facts
The local full standard-library auditor completed 79,082 assertion-accounted checks, zero failures. It enumerated all pairs of q/2-subsets for q=2,4,6,8 and all p=1..q streaming intervals. Full 2^(3q) CNF assignment counts were exhaustively evaluated ONLY for q<=4; at q=6,8 positive witnesses and negative opposing pins were checked symbolically, not all assignments. The independent compact peer script completed 21,306 assertions without failure. Readback-published result summary is **not** the 2,980-byte complete local raw JSON; the full local ZIP contains that raw file.

Full auditor local SHA256: 9bb6beee3d8dcd8fd73274000665fa2376ae0571f0d129b13426d55fab9cbeed.
Raw local SHA256: 9c2056daa3963c61e6255fabebc602c0f2059451d282b97668f3872679062f34.
Compact peer script local SHA256: 78da1a115fb431199fa54a35c99ee9cf33c3710f0faabc3629dd523ed49637e7.

## Model transport and rejection ledger
FILLED, restricted: exact named-source SAT semantics, fixed-width construction, full-rank permutation relation, bounded sequential passes versus portable live state, and a constructive p-pass algorithm.
PARTIAL/RESTRICTED: real global source identity reconciliation under a declared input scanner and explicit source rereads.
FALSIFIED/RETIRED as unrestricted transport: using source semantic rank to infer mandatory post-acquisition SAT computation, equating sequential p-pass streaming with FLMV read-only *indexed random access*, treating each touched name as a forced persistent cache, and claiming small bit-mask flip counts bound total work.
CONDITIONAL: ARC eager/lazy exponents, named compatibility children, repeat-source/cache and scoped inheritance, provided a semantically correct all-input compiler exists.
OPEN: any all-input, uniform, exact, single-machine simultaneous SAT time-space successor or cofinal finite-hit ARC route into FLMV t<241/200, s<11642479/23232400. Old t+s<2cos(pi/7) landing remains retired.

## Archive coverage manifest, not overstated
Direct original file read: AGENTS.md blob c5265db, CODEX.md blob 754999f, .codex/skills/pnp-research/SKILL.md blob b8df83a, main13.tex blob 87dbaad, current root main.tex specialist region pre-update blob 6cd0535; LSPV-1 PASSMEM84 blob 29f356e, CUTFLOW85 blob 14542ea; LSPV-3 CONTEXT-STREAM-QUOTIENT87 blob 233ba25, EXACTONE-JOIN-CYCLE95 blob 7265867; LSPV-4 SCOPE-FRESHNESS91 handoff blob a1d7220, PARITY-MARGINAL-COUNT92 original blob b01ca77; LSPV-5 THREE-STATE-JOIN-FIREWALL130 original blob 06f9c45, STRICT-SUBJOIN-STATUS131 handoff blob 1b8b3ea. The Drive connector retrieved original ARC document 1QirzuNPCG-CrE3EX6WweqsPdDbtoblCDEE4YI0HGyC0 and continuation document 1TselU5xLzVf7nbD2R0r-XZz_8t-S_WNrkiOZxNpbR5E; selected relevant mathematical passages reviewed. Bounded GitHub searches: HEREDITARY-SCOPED10 (100 results, nonexhaustive); hereditary_scoped (7); multi-pass streaming SAT (2); fooling set signed pin (10); 2p-1 (10); name-only and scope freshness (bounded). No claim of full current corpus reread, Drive pagination exhaustion, historical revisions exhaustiveness or recovered HEREDITARY-SCOPED10 executable. Inherited prior 3,532-file pinned keyword/hash crawl remains an index only. Primary literature anchors: Yao 1979 deterministic communication model; FLMV 2005 random-access SAT forbidden endpoint. Google Drive original continuation still supplies only the HEREDITARY-SCOPED10 summary; no full implementation was accessed.

## Adaptive state, costs, and peer instructions
Before step: paid source grammar, read-only name identifiers, unknown SAT label, pass index, current universe interval, mask and remaining budget. Acquire q and record layout through charged parsing. Choose bitmask scan, considering SCC/Horn/affine, sorting, indexed rereading and exact generic fallback. Each pass sets mask bits for A names in one interval, tests B names, clears mask or rejects, then switches interval. SAT uses direct bitmask construction and an optional witness; UNSAT identifies a shared contradictory name. Charge every source/work read/write, unchanged write, controller/addressing bit, failed test, reset, cache, helper or child generation, and peak writable bit. Positive-mask actual flips can be O(q) even when source work is O(p*N); total-state flips are NOT O(q).

Roles 1-3 and 5: use J_q as an **identifier-only global compatibility** control against any child compilation that forgets names. Require both labels, valid ordinary child serialization, exact parent-label reconstruction, same-machine time/space, cache/replay and indexed-source access. Do not treat bounded-pass rank as a lower bound against arbitrary SAT deciders.

## Next original artifact
Read the *full body* of SCOPED-BLOCK-REBUILDER92 and test two-level name-coherent reconstruction on J_q. Original HEREDITARY-SCOPED10 code remains unrecovered, so do not substitute its log summary for an executable. P versus NP remains OPEN.

<!-- END_OF_VERIFIED_HANDOFF::LSPV-4::NAME-ONLY-MULTIPASS93 -->
