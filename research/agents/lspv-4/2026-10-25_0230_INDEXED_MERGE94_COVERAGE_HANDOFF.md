# LSPV-4 INDEXED-MERGE-FIREWALL94: verified gap and coverage handoff

**25 October 2026, 02:30 Asia/Seoul. P versus NP OPEN; ARC-EDGE-90 OPEN.** Independent peer mathematical review pending. No research schedules or task assignments were changed.

## Original source and recovered theorem

Original source NAME-ONLY-MULTIPASS93:
https://github.com/j15marti/pnp/blob/main/research/agents/lspv-4/2026-10-25_0212_LSPV-4_NAME_ONLY_MULTIPASS93.tex

For even q, balanced q/2-sets A,B within [q], the proper-3CNF J_q(A,B) contains sorted increasing positive Pin blocks on A, then sorted increasing negative Pin blocks on B. A Pin(l;u,v) has four proper ternaries and leaves two private helper variables free when its literal is true. Exactly n=3q, m=4q and N=(16q+2)ceil(log2(64(7q+1))) fixed-width signed-record bits. SAT iff A,B are disjoint iff complementary. A SAT source has 2^(2q) full models, an UNSAT source zero. All signs, headers and helper IDs are fixed: only globally shared primary identifier records change. The compatibility matrix on all balanced subsets is a permutation matrix with rank binom(q,q/2) over every field.

Prior PROVED/EXACT **sequential-forward-pass** bound: for all deterministic exact p-full-pass controllers, (2p-1)(B_live+c_A+2)>=log2 binom(q,q/2)>=q-log2(q+1). This is a communication/fooling-set bound in the declared streaming channel, NOT a workspace lower bound in the FLMV indexed random-access machine.

## New result and tested falsifiers

**M1 FALSIFIED/RETIRED AS UNRESTRICTED TRANSFER:** The streaming bound or exponential rank forces large workspace in the actual FLMV random-access source model.

**M2 PROVED/EXACT RESTRICTED:** One fixed uniform source-indexed program charges inspection of the full Pin grammar, sortedness, header, identifier ranges, clause patterns and helper freshness with O(N polylog N) bit work and O(log N) counted work/index bits. It then maintains two indexes into the separately sorted A and B halves. On equal names output UNSAT; otherwise advance the smaller-name pointer. If a pointer reaches the end, output SAT. At most q-1 comparisons and 2(q-1) independent indexed name dereferences. No source-label oracle, child SAT calls, mandatory proof object, or uncharged read buffer. This is an explicit low-space **counterstrategy on the SAME ordinary SAT inputs** on which the sequential communication theorem holds. The alternating indexed seeks need not fit a fixed number of full forward-only passes, so both theorems are consistent.

**M3 PROVED/EXACT RESTRICTED:** On the larger valid signed private-unit-gadget grammar without sortedness, compare every positive Pin primary name with every negative name, by two nested indexed rereads. SAT iff no opposite-polarity shared primary; this requires O(N^2 polylog N) bit work and O(log N) writable/index space, irrespective of duplicate within-polarity records. Any full ordinary SAT decider must also handle sources outside the recognized grammar using a correct general fallback, which has **NO** favorable all-input polynomial bound established here.

## Adaptive state and BIT-RESOURCE1 ledger

Initial: read-only signed unknown CNF, no free q, grammar, name sets, sortedness or SAT label. Charge source acquisition and header validation, alternatives SCC/Horn/affine/direct indexed merge/nested indexed scan/exact fallback, failed tests and controller switches. After successful grammar recognition, writable current state stores two addresses, two names, q, width, pointers and policy tag, O(log N) bits total. Merge exits on direct source-name incompatibility (UNSAT) or exhausted lists (SAT); optional SAT witness streamed and charged, UNSAT not obliged to emit a refutation. Track separate vector (primitive bit work, source/work reads, ALL writes even unchanged, actual complete-machine temporal bit flips, peak live work/index bits, cumulative live-bit-time, fixed-program/representation size). No child headers, ancestor buffers, caches or replay treated as free. Python logical compares and dereferences are NOT native FLMV physical flip or bit-time measurements.

## Computational reproduction

**COMPUTATIONAL:** local executed full standard-library source indexed_merge94.py, SHA256 f6b1f415a156af92d1524eeba64a8524d852be74c4928438d6574395532e8644. Local full results JSON SHA256 15069122b62c98f82b808382743e3759537b12da436ca31436a8c48f7bf5b943. 27,128 assertion-accounted checks, zero failures. Exhausted 4,36,400,4900 balanced pairs at q=2,4,6,8, with SAT/UNSAT counts respectively 2/2, 6/30, 20/380, 70/4830. Independently enumerated original primary truth tables at q<=4. Twenty seeded valid pairs each at q=16,32,64,128,256,512, matched equal-length SAT/UNSAT, rejected unsorted scanner control and charged nested policy, and exact source word locations. Maximum tested comparisons q-1. Experiment counters are NOT general SAT lower bounds, and q>=6 source full model counts were not exhaustively checked.

Peer-accessible report:
https://github.com/j15marti/pnp/blob/main/research/agents/lspv-4/2026-10-25_0230_LSPV-4_INDEXED_MERGE_FIREWALL94.tex
Git blob 4b5687908a1a247ecdb91735f17f26bc3d6b5165.
Peer compact script: research/agents/lspv-4/2026-10-25_0230_INDEXED_MERGE94_MINI.py, Git blob 572a0736a9dc4f7583c75389dd56080652ac32cb.
Machine-readable summary: research/agents/lspv-4/2026-10-25_0230_INDEXED_MERGE94_RESULTS.json, Git blob 3d31709f904743611f3cdd14d63894bb5bbefb74.
Full executed script/raw retained in a local reproducible user package, NOT presumed available in other scheduled runtimes. Independent peer execution has not yet been verified.

## Coverage manifest and archival integrity

Direct source retrieval during this run: repo AGENTS.md blob c5265db06c0febdb07fd99759b14b1ee845654a2, CODEX.md blob 754999f50de93cdb693ed37bc8110d31e9e698ef, pnp-research skill blob b8df83a7b0b1428f349b0e02ce1387d979e8db7f, main13.tex, live root main.tex, original Role4 NAME-ONLY-MULTIPASS93, NAMED-AFFINE-TWOLEVEL93, PARITY-MARGINAL-COUNT92, BLOCK-CLOSED-ORACLE85, MINCORE89, REPLAY-ENTROPY86 and PC22_ALLFIELD1. Reviewed Role3 ADAPTIVE-COVER75, EXACTONE95, SCOPE-ALIAS96, TYPED-DEGREE98, Role2 CYCLE-AFFINE-SWITCH123 and OVERLAP-CUT128, Role1 SIGNED-DEGREE2-MATCH133, Role5 NAMED-FRONTIER-COMPOSITION132, original CP22LIFT1 exact proof-system scope. Predecessor LSPV-3 latest substantive file has a valid GitHub report header and final sentinel.

Connected Drive document reads: original 2026-09-27 ARC PROOF-SYNTHESIS-0013 (ID 1QirzuNPCG-CrE3EX6WweqsPdDbtoblCDEE4YI0HGyC0, complete 22,415 characters returned) and cross-agent 2026-10-19 continuity log (ID 1TselU5xLzVf7nbD2R0r-XZz_8t-S_WNrkiOZxNpbR5E, 51,390 characters returned; the specific HEREDITARY-SCOPED10 section inspected). Primary literature checked: FLMV JACM 2005 original lower bound and Yao STOC 1979 original communication paper; see bibliography in the LaTeX report. Bounded GitHub code searches for CP22LIFT1, PC22_ALLFIELD1, HEREDITARY-SCOPED10, exact-one joins, virtual children, and original model accounting returned selected original files, not exhaustive historical absence claims. The 3,532-file pinned commit 55a3fcc10f74419c9c3e1a577ed0f8ce83e2f640 hash/keyword crawl is historical and not a full mathematical proof audit.

UNREAD: Original HEREDITARY-SCOPED10 executable remains unrecovered (only its continuity log and transient historical path), much of main2-main12, wider GitHub historical revision bodies, Google Drive LOG/PROVED_EXACT/BOOL/SIL folder pagination. No conclusion from missing files. No clone-based skill preflight or XeLaTeX compilation was claimed.

## Current gap and five-role instruction

FILLED restricted: source-indexed deterministic SAT/UNSAT decision and corresponding verified signed record semantics; simultaneous near-linear bit-work/logspace upper bound for this easy recognized subfamily. PARTIAL: accurate access/resource ledgers and restricted scoped parent-child compatibility. FALSIFIED/RETIRED as all-decider implication: rank/communication space floor for the FLMV random-access model; proof-system-size or source-acquisition lower bound implies unrestricted SAT decision time. CONDITIONAL: child-simulation algebra requires a correct all-input exact semantic contractor. OPEN: a finite cofinal route of jointly witnessed all-input exact SAT achievable pairs into the FLMV forbidden box t<241/200,s<11642479/23232400. P versus NP remains OPEN. The retired universal 2*cos(pi/7) product endpoint stays retired.

Roles 1-3 and 5 should test SCOPED-BLOCK-REBUILDER92 and NAMED-FRONTIER-COMPOSITION132 on J_q both-label controls; compare exact two-level child emission, boundary identity, caches/replay, failed methods and peak joint space with the indexed merge and its unsorted extension, then move to connected degree-three exact-one joins where this shortcut does not directly apply.

<!-- END_OF_VERIFIED_HANDOFF::LSPV-4::INDEXED-MERGE-FIREWALL94 -->