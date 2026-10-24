# LSPV-1 SIGNED-DEGREE2-MATCH133: additive gap, coverage, and rejection handoff

Date: 2026-10-25 00:26 Asia/Seoul. P versus NP OPEN. ARC-EDGE-90 OPEN. No changes to existing schedules.

## Exactly proved restricted link

For signed EXACT-ONE constraints of arbitrary signs with at most two source occurrences per variable, build a weighted graph with one mandatory vertex per source clause. Degree-one variables are optional clause-leaf edges. Degree-two same-polarity variables are optional clause-clause edges. Degree-two opposite-polarity variables each receive one mandatory choice node and two alternative edges to their clause endpoints. Weight every graph edge by the number (one or two) of mandatory endpoints. SAT iff the maximum-weight matching saturates all mandatory nodes. A matching returns a coherent assignment to every named source variable; no independent local witness joins are assumed. Polynomial time and polynomial space follow from known general weighted matching. This extends DEGREE-MATCH-LADDER132's positive-only source result. The different BLOSSOM-FACTOR60 covers paired ordinary OR-clauses, not this signed exact-one language. Independent mathematical review pending.

Parameter k counts original source variables with at least three occurrences. Branch on their assignments, then replace residual literals in already satisfied clauses by unary exact-one constraints on their complements; the remaining source occurrence degree is at most two. This gives 2^k poly(N) time and polynomial writable space. Moore--Robson planar cubic monotone 1-in-3-SAT proves NP-completeness at exactly three positive source occurrences. This is a sharp class distinction, not a lower bound on unrestricted deterministic time.

Matched controls: K4 source with six variables, four distinct ternaries and occurrence two. All-positive member SAT; opposite-polarity-per-variable member UNSAT by total-true-literal count six versus four. Same unsigned incidence and connectedness.

## Computational and bit ledger

Public repro SIGNED_DEGREE2_MATCH133_repro.py and results JSON (same role directory), seed 202610240826, NetworkX 3.6.1. Exhaustive K4 signed masks 4096, 1200 random source occurrence<=2, 240 random source occurrence<=3, all cross-checked against independent complete truth tables. 5536 independent formulas, 2992 SAT, 2544 UNSAT, 11078 assertion-accounted checks, zero failures. 5500 weighted-matching calls, 1394 explicit high-variable branches. Expanded local SHA256 script b3f78e6dc263c9966253312950b7f23c95b3c01d59bb5ff69a108c83614e0250, JSON 981733053d6aa906c0d28aa19d07f82dbd265d60d29b280568f70a85ef35925b. The Python proxies do not measure FLMV Turing-machine operations, physical bit flips or space.

Adaptive resource vector: (primitive bit work, source reads, work reads, all writes, complete-state flips, peak mutable bits, cumulative live bit-time, fixed program size, representation size). Charge parsing, recognition, sign grouping, missing-orientation controls, matching-node generation, edge list construction, branch failures, optional witnesses and reconstruction, caches, switching, source rereads and exact fallback. SAT and UNSAT are handled without knowing the label. Matching graph need not be emitted by an unrestricted SAT decider.

## Coverage and gap ledger

Current GitHub full tree metadata 5143 entries, truncated=false. Targeted primary body reads on GitHub: AGENTS.md, CODEX.md, pnp-research skill, root main.tex relevant sections, main13.tex, Role1 DEGREE-MATCH-LADDER132, Role2 BLOSSOM-FACTOR60 and LINEAR-SPACE-CUT-REPLAY127, Role3 EXACTONE-JOIN-CYCLE95, Role4 SCOPE-FRESHNESS-VALIDATION91, Role5 THREE-STATE-JOIN-FIREWALL130. Peer predecessor Role5 has a verified substantive report and final sentinel. Six term-group GitHub searches, with results reviewed selectively. Native Drive ARC Sept27 221-paragraph document fetched and inspected in part. Inherited pinned snapshot 3532-file hash/keyword review is historical only; not an exhaustive manual review. Most older root MAIN snapshots, Drive LOG/PROVED_EXACT, original HEREDITARY-SCOPED10 body, and source history revisions not exhausted. Do not infer missing item from an empty bounded search.

Primary literature: Edmonds 1965 and Gabow 2016 polynomial general matching, Moore--Robson 2001 positive cubic 1-in-3 NP-completeness, Schaefer 1978 exact-one NP-completeness, FLMV JACM 2005 endpoint. PQ Schur-square, collision entropy and VLSI locality analogies provide no direct necessary resource transfer to an arbitrary SAT decider.

## Ranked dependency map and receiving obligation

1. ARC/FLMV: known model-matched forbidden time-space endpoint and exact conditional cofinal finite-hit arithmetic, but ARC-EDGE-90 (all-input achievable-pair contraction) OPEN. Existential closure need not compile a specific base program. Each pair still requires one fixed uniform exact all-input realization simultaneously meeting time and space.
2. UWI-1/universal selectors: correct restricted witness characterizations, but no all-decider cost transfer to an unconditional lower bound.
3. CP/PCR/DNNF/semantic rectangle: restricted representation/proof size bounds, but no necessary output/proof obligation for every one-bit decider.
4. WRAPPER, clocks, hashes and causal provenance: conditional causal/replay arguments, not a complete unconditional all-input decision cost; retired cosine product remains retired.

Peer link audit: Role2 LINEAR-SPACE-CUT-REPLAY127 optimizes a restricted source scope cost proxy; Role3 EXACTONE-JOIN-CYCLE95 preserves source names across three-state global joins; Role4 SCOPE-FRESHNESS-VALIDATION91 proves named-scope validity and reopening are not free; Role5 THREE-STATE-JOIN-FIREWALL130 gives the opposite-label pair where pairwise consistency does not settle global SAT. Our signed occurrence-two matching theorem adds a distinct adaptive positive shortcut, and does not conflate NP-hard global joins with mandatory runtime.

ARC-EDGE-90 remains OPEN: show a fully charged all-input, uniform, exact SAT replacement, or a finite cofinal route of simultaneously achievable time-space exponent pairs into a verified FLMV forbidden region. A source recognizer plus full-parent fallback cannot yield worst-case contraction, NP-completeness alone cannot supply an unconditional time lower bound, and an ideal algorithm is free to use a different method. Keep the old cosine product boundary retired.

NEXT: If original HEREDITARY-SCOPED10 appears, test its named variable opening/closing and output child semantics on the matched signed K4 pair and Moore--Robson cubic source, with actual ordinary child bits and no independent-child SAT assumption.