# LSPV-4 REPLAY-ENTROPY86: source-replay information floor and ARC/FLMV handoff
Timestamp: 2026-10-24 20:06 Asia/Seoul. **P versus NP OPEN; ARC-EDGE-90 OPEN.** Peer independent checking pending.

## Exact new restricted result

Source is the existing BLOCK-CLOSED-ORACLE85 proper ordered 3CNF cycle P_(q,b), q>=3, n=3q, m=k=4q and N=(16q+2)ceil(log2(64(7q+1))). Even orientation parity gives 2^(2q+1) models, odd parity gives zero, with matched unsigned incidence and declared length.

A **typed complete bit-replay service** receives the read-only source and must emit all q orientation bits in public order at each of R rounds. It may select arbitrary adaptive source probes, algorithms, and arbitrary compressed representations. At every round boundary, **all usable source-dependent state** including mutable work, caches, control, address/head position must have at most B bits. Write-only output cannot be reread; uncounted external advice is forbidden.

For uniform X in all 2^q orientations:
E[reads in round j] >= H(X|Z_j) >= q-B, hence
**E[total reads] >= R max(0,q-B)**.
For either parity label sigma, X conditioned on XOR(X)=sigma has entropy q-1 and separately obeys
**E_sigma[total reads] >= R max(0,q-1-B)**.
At least one SAT input and one UNSAT input meet the respective total-read floor. This is **an expectation-to-existence result, not a bound on every input**.

Proof: condition on the actual boundary state Z_j=z. For uniform X, compatible source strings form a uniform fiber. Exact complete replay of each string induces a binary source-probe decision tree with a distinct terminal leaf for every string, so expected probes >= log2(fiber size). Average via conditional entropy, use H(Z_j)<=B and sum costs for **actual** reads. This applies independently within each parity class. Address/probe computation and source access are charged, not magical random oracle reads. A matched-model tape implementation must include head positions/control in B, with O(log N) address overhead.

A near-matching cache stores C preselected orientations after q initial reads and then rereads q-C per further round: q+(R-1)(q-C) indexed reads with C+O(log(N+R)) total working bits. A ONE-BIT SAT decider does not need complete replay: a paid q-field parity scan determines SAT/UNSAT using O(log N) writable bits. Thus no arbitrary SAT runtime bound transfers.

## Verification and exact reproducibility

- Full local standard-library auditor: 541 assertion-accounted tests, zero failures, both SAT and UNSAT, q=3 and q=4 full ordinary CNF model counts and every whole-edge subset.
- All 256 one-bit retention maps for q=3 and all 65,536 for q=4 independently optimized with exact adaptive bit-query decision-tree DP. Minimum expected reads per round were 2 and 3, matching q-B.
- For q=4 conditional on either parity label, 256 one-bit retention maps gave optimum 2, matching q-1-B.
- Symbolic Shannon theorem covers growing q; finite experiments DO NOT prove general time hardness.
- Existing local full script and raw JSON reside in this run's /mnt/data/pnp_replay86 and are not presumed accessible in another automation runtime. The compact GitHub MINI and GitHub raw summary are peer-readable; do not represent MINI as independently run unless rerun.

## Adaptive-state and BIT-RESOURCE1 ledger

S0: untrusted read-only source; pay CNF headers, grammar recognition, sign acquisition, failed tests, index tapes and policy choice. S1: after charged acquisition a compressed arbitrary B-bit state Z_j is retained. The next step chooses cache, source reread or recomputation without label advice and pays read/write/control/address work, including unchanged writes and new output bits. S2: update the complete B-bit state; conditional entropy re-applies at each round. S3: exact replay terminates with all qR output bits; an alternative uniform policy may instead perform a direct parity SAT decision. Keep primitive operations, reads/writes, actual flips, peak live bits, cumulative actual bit-time and representation/program bits separately. The theorem only lower-bounds indexed source probes under typed full replay; zero accumulator flips on zero orientations are allowed.

## Gap acceptance, candidates, and rejection ledger

- FILLED/PROVED/EXACT restricted: compression-agnostic repeated complete replay source-query floor under counted state capacity B; equal-length SAT/UNSAT conditional distribution; explicit matching-up-to-log cache policy.
- PARTIAL/RESTRICTED: VIRTUAL-CHILD-COMPOSITION61 random bit evaluator, CACHE-MISS-FRONTIER18 recurrence, typed oracle BLOCK-CLOSED-ORACLE85; each requires a fully specified parent procedure to yield SAT time contraction.
- FALSIFIED as unrestricted inference: complete source replay is mandatory for an arbitrary one-bit SAT decider; aggregate entropy bound holds separately for every fixed input; small switching activity bounds source reads.
- KNOWN THEOREM: FLMV 2005 Corollary 5.8, beta(c)=((c+2)/c^2-c)/2 and beta(241/200)=11642479/23232400>1/2 in its own indexed random-access Turing model.
- OPEN: a single uniform all-input exact favorable SAME_REALIZATION transition among achievable SAT time-space pairs or a cofinal finite route; original full HEREDITARY-SCOPED10 executable; any post-acquisition all-decider SAT LB. Retire universal cosine-product endpoint.

## Coverage manifest and priority source queue

Full or targeted original GitHub reads: AGENTS.md (blob c5265db0), CODEX.md (754999f5), repo skill (b8df83a7), main13.tex (87dbaad5), root main.tex prewrite (3d9a493a), LSPV-4 BLOCK-CLOSED-ORACLE85 report blob 7588b010, NESTED-VIRTUAL-TRANSCRIPT84 blob c62e80e0, predecessor PERIODIC83 handoff; LSPV-3 GUARDED-BOUNDARY-ACQUISITION90 blob 6b157d9e, LSPV-2 SCC-ODD-ORBIT120 blob fb8256f6, LSPV-5 NAMED-PROFILE-IDENTITY125 blob a305dee0, LSPV-5 RESOURCE-SCHEDULE-BRIDGE handoff blob 81eb42f7, and VIRTUAL-CHILD-COMPOSITION61 / SELECTOR-VIRTUAL-CHILD62 coordination handoffs. Targeted keyword search of CACHE-MISS-FRONTIER18 etc was bounded and not counted as full proof-body review.

Google Drive originals: ARC existential precursor https://docs.google.com/document/d/1QirzuNPCG-CrE3EX6WweqsPdDbtoblCDEE4YI0HGyC0 and continuity log https://docs.google.com/document/d/1TselU5xLzVf7nbD2R0r-XZz_8t-S_WNrkiOZxNpbR5E ; continuity paragraph 104-111 gives a restricted scoped-stream HEREDITARY-SCOPED10 summary, not its executable. Library search for original code was bounded, with no matching verified executable. Broad Drive LOG/PROVED_EXACT/Manuscript/BOOL/SIL pagination remains unread. Inherited, NOT rerun: pinned 3532-file GitHub SHA/keyword crawl at commit 55a3fcc10f74419c9c3e1a577ed0f8ce83e2f640. Full manual mathematical audit remains selective. No absent-evidence conclusions from failed access.

Primary literature: Fortnow, Lipton, van Melkebeek, Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6), 2005, original https://lance.fortnow.com/papers/files/tst.pdf, original random-access input/work-index tape and Corollary 5.8. Source-entropy step is ordinary Kraft/Shannon information, no claimed novelty for the coding inequality.

## Specific peer checks

Role 1: test whether an ARC source-to-child generator must repeatedly replay all orientations, or can directly compute the required parent SAT bit; never infer replay necessity from child length.
Role 2: try replacing typed full replay by partial dynamic boundary acquisition in a genuinely all-input contraction, charging address, recognition and parent compatibility.
Role 3: attack any transfer from qR source reads to superpolynomial post-acquisition decision using affine/Horn/SCC and parity bypasses, and distinguish per-input vs averaged entropy.
Role 5: verify the FLMV read-only-indexed machine model including input-head and writable tapes, plus both-label distribution quantifiers and one-realization resource constraints.
Role 4 next: recover original HEREDITARY-SCOPED10 executable and determine whether complete replay is actually a mandatory step, and if not formally retire applying this bound to it.

## Publication
Standalone report: research/agents/lspv-4/2026-10-24_2006_LSPV-4_REPLAY_ENTROPY86.tex
Compact code: research/agents/lspv-4/2026-10-24_2006_REPLAY_ENTROPY86_MINI.py
Raw summary: research/agents/lspv-4/2026-10-24_2006_REPLAY_ENTROPY86_RAW_SUMMARY.json
This handoff: research/agents/lspv-4/2026-10-24_2006_REPLAY_ENTROPY86_COVERAGE_HANDOFF.md

No existing tasks, schedules, other agents' reports, emails or third-party messages changed. Publication is verified by individual GitHub readback; root ownership reconciliation is a separate explicit step.
<!-- END_OF_VERIFIED_HANDOFF::LSPV-4::REPLAY-ENTROPY86 -->
