# LSPV-3 RECURSIVE-FRONTIER-REPLAY260: five-role handoff

Date: 2026-10-30 16:24 America/Los_Angeles. One integrated user-directed adaptive residual-SAT / arbitrary-A ARC / actual FLMV program; P versus NP OPEN. Do not alter any of the five existing task identities, enabled/paused states, hourly offsets, or role boundaries.

## Mathematical result and exact scope

An authenticated clause-order frontier DP already supplies exact per-source-clause local pattern support H_i(u). Given global prefix L_a and suffix R_b, split the interval in half, recompute the two midpoint messages by scanning source clauses, recursively solve halves, and at each leaf join original clause C_i with global L_(i-1) and R_i. This is a source-charged Hirschberg-style recomputation specialization, not an unrestricted new SAT algorithm. For w=max_i |B_(i-1) union Vars(C_i)|, retaining O(log m) messages gives O(2^w(w+log N)log m+S_B+log^2N) writable bits. Total per-interval rereads, boundary acquisition d_i, all output bits and proof replay are charged: O(N+log(m+1) SUM_i [d_(i-1)+d_i+2^|U_i|poly(|U_i|+k+log N)]+mk2^k) indexed-word operations.

The numeric source-band grammar |variable ID - clause index|<=b can be verified by a complete source scan. Boundary discovery costs O(b^2 k) clause-occurrence reads per cut and O(bk log N) scratch. A source renaming destroys the cheap-b grammar even though SAT is invariant; recognizing the best order/representation is not free.

**UNSAT and SAT protection:** H_i(u)=0 forbids precisely a local partial assignment cube, not the whole formula. A complete source UNSAT verdict is obtained from empty forward support and must be checked by authenticated message replay. SAT uses a checked complete source witness. Neither arbitrary original-clause S/U target nor a failed bounded repair proves UNSAT. Explicit support-stream output is not a free FLMV work tape.

## Independent finite controls and negative total-work result

Independent full-table DP uses global-variable masks, independently checks 23 original source cases and 9,958 records, exhausts model truth tables for small sources, and rejects two deliberate corruptions. W1 connected strict signed exact-(2+,2-) source has zero models, SWAP6 has 54 models and 70/160 unsupported clause patterns. Source-indexed original S/U targets, both inversions, all SS/SU/US/UU modes, coherent endpoints and flip trails were checked as adverse controls.

Selected host-language operation counts: Band128 SAT full DP 839166/replay 1917887/UP-DPLL 61057; UNSAT 837844/1915434/17566; W1 UNSAT 876048/1604689/19962; SWAP6 SAT 875345/1602849/9548. On Band128 SAT, 2115 full-table stored entries versus replay live envelope 111. On W1 replay's loose live envelope of 111416 is worse than full-table's 90772. Thus memory improvement is a conditional work/space tradeoff, NOT a speedup or model-independent space bound. Band512 replay streams 35308 output bytes and uses 9952436 selected events; all source/output bytes counted. No actual CDCL binary or native FLMV tape-transition benchmark performed.

Four falsifiers: (1) replay both-label correctness: succeeds in restricted model; (2) smaller live tables imply less computation: false; (3) low numeric-band order/recognition is free and invariant: false; (4) a streamed table is a power-smaller ordinary SAT child: false. This run does not supply any hereditary all-input A->Phi(A) successor or prove P!=NP.

## Role ownership and one next theorem arrow

LSPV-1: audit the logical output-object distinction; forbid replacing source-support bits by a free small ordinary SAT child or an answer-labeled oracle.
LSPV-2: test whether a *verified* low-space source representation can emit a genuine ordinary short child, with exact total symbol accessor and both-label semantics.
LSPV-3: seek a policy that chooses bounded-frontier replay vs simple UP-DPLL vs affine/Horn/Krom while keeping simultaneous native writable space below N^(1/2+o(1)), all discovery/restarts/failed trials charged; next ask whether one resulting child is physically N^(1/2+o(1)).
LSPV-4: model-match the input head and all original-source repeated reads/output writes against FLMV Theorem 5.7, not Python selected-operation events.
LSPV-5: independently referee the recursive global-boundary proof, table-space bound, easy renamed-band controls, root section and existing report259 sentinel; retain strict status labels.

## Verifiable publication and artifact custody

Complete four-page LaTeX PDF, BibTeX, source producer, independent verifier, policy controller, original-source raw JSONs, exhaustive local pattern JSONLs and checksums were validated (ZIP testzip and SHA256 manifest) and uploaded successfully to persistent Research Library:
`/P-vs-NP/2026-10-30_1624_LSPV-3_RECURSIVE_FRONTIER_REPLAY260_COMPLETE.zip`,
Library `libfile_89af6f962ec48191b7de0ad21a1a083f`,
ZIP SHA-256 `9abaccba34a153282115568949c2cf0a6bb94ba6b9d4631871cac408b07fb2bc`.

GitHub compact formal TeX record: `research/agents/lspv-3/2026-10-30_1624_LSPV-3_RECURSIVE_FRONTIER_REPLAY260_PUBLIC.tex`.
Detailed public explanatory record: `research/agents/lspv-3/2026-10-30_1624_LSPV-3_RECURSIVE_FRONTIER_REPLAY260_PUBLIC.md`.
Compact machine-readable measurements: `results/summaries/arc/2026-10-30_1624_LSPV3_RECURSIVE_FRONTIER_REPLAY260_COMPACT.json`.
The full producer and unaggregated raw tables are in the persistent Library archive, not claimed to be fully GitHub synchronized. Root `main.tex` should be reconciled only in LSPV-3 marked region after report readback.

Prior method citations: Hirschberg 1975, DPMC/project-join (Dudek-Phan-Vardi 2020), FLMV JACM 2005, Dreier-Ordyniak-Szeider JCSS 2024. Root-contract and governance remain authoritative. P vs NP OPEN.

END_OF_VERIFIED_HANDOFF::RECURSIVE-FRONTIER-REPLAY260
