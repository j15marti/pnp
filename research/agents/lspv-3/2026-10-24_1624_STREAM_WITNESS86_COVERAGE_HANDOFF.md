# LSPV-3 STREAM-WITNESS-BITTIME86: Cumulative evidence and peer handoff
Timestamp: 2026-10-24 16:24 Asia/Seoul. P versus NP OPEN. Existing research schedules unchanged.

## Verified publication
Standalone LaTeX: research/agents/lspv-3/2026-10-24_1624_LSPV-3_STREAM_WITNESS_BITTIME86.tex. Initial commit 100f3971558062767656b8af27cbb09fa7ac4836, finite-test description corrected at b10e83f5bc741769861df4177873d4c7faea51df. Full report and end sentinel were read back.
Python source: research/agents/lspv-3/2026-10-24_1624_STREAM_WITNESS86_audit.py. Portable source revision commit 7493c489d3f61c5f8dac8ae35ed9db28eb29ebb2, with full same-directory raw regeneration.
JSON summary: results/raw/2026-10-24_LSPV3_STREAM_WITNESS86_raw.json, commit 34d61f59c3b9002ad012f216cffd60be1801ea97.
Original full local raw JSON SHA256: bed6e5193f63bc477aa28094bb550c88a77dd4bf5b03479e90c43f2496f15a37.

## Exact new project-specific test
The source E_n has Boolean variables x_i,y_i,z_i,w_i and 4n proper ternary clauses encoding x_i iff y_i, with arbitrary auxiliary values. An optional forced-true guard plus true semantically vacuous ternary connectors makes the incidence graph connected without changing its feasible x/y relation. Two unit pins x_1=0 and y_1=b, correctly padded into proper 3CNF, produce a matched SAT member b=0 and UNSAT member b=1 with 4n+7 variables, 5n+12 clauses, and identical unsigned supports.

Under the specified deterministic ONE-WAY COMPLETE witness-verification contract, candidate assignment bits arrive x_1...x_n,y_1...y_n, then auxiliaries, without rereading or free advice. The verifier must accept every satisfying assignment and reject every invalid assignment. The 2^n possible x prefixes are distinguishable by appending y=x: every such exact verifier has peak writable space at least n bits on some candidate. For each j after reading j y bits, condition on the common y prefix p of length j. The 2^(n-j) different x suffixes must occupy distinct canonical complete writable state codes. Counting short binary codes gives average live bit length at least n-j-2 when positive. Thus averaged over uniform accepting diagonal witnesses, sum of n checkpoint live-bit counts is at least (n-1)(n-2)/2, so some accepted candidate has cumulative bit-time Omega(n^2). This is a space/activity theorem in a restricted streaming verifier, NOT a lower bound on exact SAT decision.

A deterministic exact online transducer translating grouped x...y output into interleaved x_1y_1x_2y_2... requires n-1 writable bits at the cut before y_1, even if it is allowed unbounded time. With native interleaved witness generation, the equality verifier instead has O(log n) memory; with indexed candidate-bit recomputation it also has small memory at separately charged time. Direct source-aware SCC/equality reasoning decides the entire source family cheaply. The UNSAT pin control can be recognized without any candidate. A sound PARTIAL witness verifier is allowed to accept only a special cheaply checkable witness, so the complete-verifier premise cannot be silently transferred to MOVINGCOVER1 or arbitrary SAT deciders.

## BIT-RESOURCE1 vector and ARC transport
Record primitive bit work, source reads, workspace reads, unchanged and changed writes, actual complete-state flips, peak complete writable bits, cumulative live-bit-time, code/representation size. N=Theta(n log n) encoded source bits. The special one-way complete-validator model yields peak at least Omega(N/log N) and cumulative bit-time at least Omega(N^2/log^2 N) on some accepted transcript. Bit-time is not an FLMV time or peak-space coordinate, and these bounds need not hold on the same transcript. Input/work head metadata is charged. Accumulator bit flips are not all controller/address flips. A full root decision can bypass complete witness validation. No forbidden same-machine SAT pair has been constructed.

## Tests
One 30-second-bounded standard-library chunk. n=1..7. Formula checks 262128 for all (x,y) pairs but ONLY two uniform auxiliary settings per pair, not an exhaustive auxiliary sweep. State-separation pairs 21590; bit-time bound controls 7; interleaved-order checks 21844; connected-incidence checks 21; total 305590 zero failures. No random seed. These finite checks are COMPUTATIONAL; the general propositions have elementary symbolic proofs in the report.

## Coverage and duplication delta
Full connector reads: AGENTS.md blob c5265db0, CODEX.md 754999f5, research skill b8df83a7, main13.tex 87dbaad5, LSPV-3 ADAPTIVE-COVER75 ac4b3feb and SELECTOR-ARC-MARGIN85 8ebb1313, LSPV-5 BIT-LEDGER-CEILING120 04fed3ea, LSPV-4 MOVINGCOVER1 8c0f1b11, LSPV-4 SELECTOR-CAPACITY81 handoff 787084d5. Targeted executive and specialist region of root main.tex at initial blob 9afd01b452578f4e5f1c49a8b1a6e2f612fca551. Full 22,415-char original Google Drive ARC ancestor by exact canonical URL. Original FLMV PDF original model/endpoint with visual page-18 check.
Bounded GitHub searches: one-pass witness verifier, witness stream equality, witness-verification memory, equality stream, source-readable witnesses, HEREDITARY-SCOPED10, BIT-LEDGER-CEILING120, MOVINGCOVER1, LQP, SOURCE-CHANNEL. These do not exhaust the corpus. The inherited pinned 3532-file search at commit 55a3fcc10f74419c9c3e1a577ed0f8ce83e2f640 was not rerun. Full HEREDITARY-SCOPED10 original and Drive LOG/PROVED_EXACT/BOOL/SIL remaining pagination are unread/unavailable. The equality communication argument is classical, not newly invented.

## Gap acceptance
KNOWN THEOREM: FLMV matched random-access forbidden endpoint.
PROVED/EXACT restricted: grouped one-way complete-witness peak and bit-time barrier; online reordering buffer floor.
COMPUTATIONAL: finite CNF both-label, connectivity and stream consistency checks.
FALSIFIED/RETIRED as universal: compulsory complete-witness output or grouped order for arbitrary deciders; bit-time treated as temporal bit work; expensive verify equated to expensive SAT decision.
PARTIAL/RESTRICTED: source-recognized witness generation and local boundary joins; MOVINGCOVER1 conditional selector; BIT-LEDGER-CEILING120 source and operation auditing.
OPEN: any all-ordinary-input fully charged resource-improving ARC successor or cofinal finite route.

## Adaptive-state/resource handoff
Before: fixed source, representation, accumulated witness prefix and remaining budget, label unknown. Acquire source grammar and interface under charged scans. Rule: compare grouped x/y with retained x, or try source-aware SCC/affine, indexed replay, interleaved generator, selective sound witness acceptance, explicit fallback, with switching and failure charged. After: accept only on exact full witness or verified partial witness, or decide directly with an independently correct source algorithm. Charge source/workspace reads, changed/unchanged writes, control/head transitions, caches, child index services, output headers, and peak live bits. This is NOT every adaptive SAT policy.

First missing arrow: a fully charged all-input exact SAT same-machine successor. Next artifact: full original ARC-HEREDITARY-SCOPED10 executable, particularly witness/boundary output ordering and source-address/replay costs. No schedule changes.
<!-- END_OF_VERIFIED_HANDOFF::LSPV-3::STREAM-WITNESS-BITTIME86 -->