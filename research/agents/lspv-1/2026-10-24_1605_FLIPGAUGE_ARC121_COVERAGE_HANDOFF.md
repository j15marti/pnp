# FLIPGAUGE-ARC121 | LSPV-1 proof spine and archive handoff

Timestamp: 2026-10-24 16:05 Asia/Seoul. **P versus NP remains OPEN.** Additive continuation of ARC-CHANNEL-CURVE119, BIT-LEDGER-CEILING120, and ARC-EDGE-90. No agent schedule changed.

## New exact scoped mathematical link

For fixed input x and one deterministic autonomous halting machine, let C_0,...,C_T be its genuine **complete** configurations, each containing every finite control, tape/head/index/address state needed for the deterministic successor. Under an injective, coordinate-stable binary encoding iota, define complete-state flip count
Delta=sum_{j=0}^{T-1} Hamming(iota(C_j),iota(C_{j+1})).
A repeated complete configuration on consecutive genuine steps would be a permanent loop. Thus T<=Delta. If every primitive machine step flips at most b(N,T) represented bits, then T<=Delta<=bT, with constants depending on the machine model. If b=O(1), complete-state flipping is Theta(time), not a new independent source of unrestricted SAT hardness.

**FLMV model caveat:** its indexed read macro erases index-tape data in one machine step, so don't replace that macro by one-bit activity without a charged simulation. The lower nonstuttering statement uses genuine complete configurations, not an accumulator or user-selected partial state. This is not a favorable ARC transition.

## Proposed mechanisms and verdict

1. Count complete-state Hamming flips as independent superpolynomial resource: **PROVED/EXACT negative audit**, since bit-local flips and time are equivalent along a halting run.
2. Infer compulsory accumulator value flips from compulsory source reads: **FALSIFIED/RETIRED** by the all-zero parity scan, which has n reads and n unchanged accumulator writes but zero accumulator flips; address/control state still progresses.
3. Infer parent SAT labels from only proper-source-clause child labels: **FALSIFIED/RETIRED**, already proved in MINIMAL-UNSAT-PROJECTION20. Independent q=1..5 replication is COMPUTATIONAL only.

For U charged elementary events, B_i live writable bits, peak S=max B_i and cumulative BT=sum B_i, the identity S<=BT<=(U+1)S holds. A fixed D-bit descriptor retained H steps contributes DH to BT, but another exact solver need not retain it. Hardware energy/gate activity does not transfer into complete-state flips or SAT decision time without a model-preserving compiler.

## Verified artifacts

- Report: `research/agents/lspv-1/2026-10-24_1605_LSPV-1_FLIPGAUGE_ARC121.tex`, complete source-backed mathematical scope and proofs.
- Compact deterministic Python: `research/agents/lspv-1/2026-10-24_1605_FLIPGAUGE_ARC121_minirepro.py`.
- Machine-readable summary: `research/agents/lspv-1/2026-10-24_1605_FLIPGAUGE_ARC121_results_summary.json`.
- Expanded private run bundle includes `bitflip_arc121.py`, `mincore_blind120.py`, and full raw JSON; these expanded artifacts are **not** claimed separately GitHub published.
- Report full source is published and verified by readback. The compact standalone GitHub report differs from the longer expanded local manuscript; no file-identity claim is made.
- Reproduction results: all 2,046 source strings of lengths 1..10 and five 2SAT/Horn/padded controls: no discrepancies. On 10 all-zero bits: 10 reads, 10 unchanged accumulator writes, 0 accumulator value flips, 18 binary address flips, 19 complete-state flips, 77 charged abstract bit events, 5 peak writable bits, 60 bit-time. Independent mincore reproduction: 174,592 complete assignments, q=1..5, all both-label and deletion checks passed. These are finite, abstract-model facts, not FLMV execution measurements.

## Peer links and acceptance

- **Role 2:** HALL-SWITCH70 gives a paid polynomial matching witness on a restricted exact-(2,2) class, an algorithmic escape from mandatory enumeration.
- **Role 3:** ADAPTIVE-COVER75 has query hitting-number tau<=N, no post-acquisition lower bound. ARCHIVE-ARC-SEMANTIC82 shows that the existential cofinal finite-hit sentence is logically separation-strength although it relaxes implementation demands.
- **Role 4:** SELECTOR-CAPACITY-BIT-LEDGER81 demands log binomial(M,K) bits only for **full** child-reconstruction service; a SAT-label-only consumer can be exponentially simpler.
- **Role 5:** WRITE-SHADOW-ENDPOINT118 is model-matched log-word-RAM low-write FLMV pullback; BIT-LEDGER-CEILING120 globally Lipschitz potential range at most LB. They complement rather than prove ARC-EDGE-90.
- **Known endpoint:** FLMV Corollary 5.8 in deterministic indexed random-access model. At c=241/200, beta(c)=11642479/23232400>1/2, with t<c and s<beta(c).
- **Retired endpoint:** t+s<2*cos(pi/7) is NOT a universal deterministic SAT endpoint. Historical scripts labeling it a landing must be corrected before reuse.

## Archive manifest delta and provenance

Directly read/inspected originals: main13.tex (blob 87dbaad5...), root governance AGENTS/CODEX/skill, Role1 ARC-CHANNEL-CURVE119, Role2 HALL-SWITCH70, Role3 ADAPTIVE-COVER75 and ARCHIVE-ARC-SEMANTIC82, Role4 SELECTOR-CAPACITY-BIT-LEDGER81, Role5 WRITE-SHADOW-ENDPOINT118 and BIT-LEDGER-CEILING120, original MINIMAL-UNSAT-PROJECTION20, FULL-COVER-CHILD-FIREWALL74, ROOT-LABEL-QUOTIENT85, September 27 Google Drive ARC source, and primary FLMV paper. Search was targeted, not exhaustive. Pinned 3,532-file hash and keyword audit is an inherited baseline; no claim that all mathematical bodies were rechecked. Google Drive `HEREDITARY-SCOPED10` name search located only continuity log; original full executable construction remains **not retrieved**, not proven nonexistent. Broad LOG/BOOL/SIL pagination, main2-main12, and older revision proof bodies remain unread in this tranche. Do not infer absence from search failure.

## Canonical current gap

**ARC-EDGE-90 OPEN:** exhibit a fixed uniform exact SAT machine transition or finite cofinal route into a published FLMV forbidden region, correct on every ordinary input, with simultaneous time and space on one realization. Every adaptive branch, source/work read, unchanged write, changed flip, address/control event, child bit/header, cache, failed policy, solver call, input/output, compatibility and live ancestor memory must be charged. A method-specific no-go or counterexample is not a contradiction under P=NP.

**NEXT:** recover and inspect the original full HEREDITARY-SCOPED10 generator, then instrument its actual same-machine time/space and both SAT/UNSAT shared-witness semantics; separately test symbolic/affine/Horn/SCC and decide-first bypasses. The current continuation summary does not close the gap.

<!-- END_OF_VERIFIED_HANDOFF::LSPV-1::FLIPGAUGE_ARC121 -->
