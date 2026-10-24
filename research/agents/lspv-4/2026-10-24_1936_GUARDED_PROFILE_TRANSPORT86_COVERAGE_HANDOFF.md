# LSPV-4 GUARDED-PROFILE-TRANSPORT86 | additive source, model, cost and gap handoff
**2026-10-24 19:36 Asia/Seoul. P versus NP OPEN; ARC-EDGE-90 OPEN. Independent review pending.** No current automation or schedule altered; no email or third-party message sent.

## Exact recovered construction and new typed transport

Source is LSPV-3 GUARDED-BOUNDARY-ACQUISITION90, blob `6b157d9ef18676a195d052bc436d5df42656dda3`: for proper 3CNF H with n variables, m clauses, define guard x=n+m+1, privates a_i=n+i, and ordinary proper 3CNF
`G_H = AND_i [(-x OR l_i1 OR a_i) AND (-a_i OR l_i2 OR l_i3)]`.
Exact projection `Q_H(0)=TRUE`, `Q_H(1)=SAT(H)`; parent `SAT(G_H)=TRUE` for every source, witnessed by x=0 and all a_i=0. The gadget and NP-complete profile membership were **not** discovered in this Role-4 run.

**PROVED/EXACT new local output interface.** Fixed signed-literal record grammar: two header fields (n,m), then (tag=3,l1,l2,l3) words, width `w(n,m)=ceil(log2(64(n+m+1)))`. Output `n_G=n+m+1, m_G=2m, N_G=(8m+2)w(n+m+1,2m)`, source `N_H=(4m+2)w(n,m)`. For n<=3m with used IDs, `N_G=Theta(N_H)`. The `b`th bit of G_H is computed directly from output header arithmetic, clause `floor((floor(b/w_G)-2)/8)`, output parity, the correct source record literal, and local guard/aux index. One indexed read-only source plus O(log N) counted controller bits yields O(log^2 N) bit work/bit with no whole-child buffer. Headers, tape indexes, signed fields and all source reads charged.

**KNOWN-THEOREM transport, exact model typing.** If one total deterministic machine computes the *guarded-profile bit Q_H(1) on every valid G_H* in time `N^{t+o(1)}` and work space `N^{s+o(1)}`, simulate its ordinary indexed input from H using the local service:
`T_H(N) <= N polylog N + T_B(Theta(N)) polylog N`,
`S_H(N) <= S_B(Theta(N))+O(log N)`,
for **one joint machine**. Composing with FLMV's published quasilinear indexed NTIME[n]-to-SAT reduction (Section 3), and its bounded-width locally proper source coding, contradicts Corollary 5.8 for `t<c`, `s<beta(c)`, `beta(c)=((c+2)/c^2-c)/2`; `beta(241/200)=11642479/23232400>1/2`. The upstream proper3CNF local encoding/renumbering is an **explicit hypothesis**: do not erase this encoding/machine-matching check by labeling the profile transfer unconditional for arbitrary grammars.

**Critical falsifier (FALSIFIED/RETIRED):** the same transferred resource lower bound does **not** hold for ordinary SAT of these guarded parents. An exact parent SAT machine returns YES and has a trivial witness x=0,a_i=0. Recovering Q_H(1) is unnecessary unless the parent algorithm explicitly needs that profile. Ordinary proper pinning x=1 has `n'=n+m+3`, `m'=2m+4`, `N'=(8m+18)w(n+m+3,2m+4)=N_G^{1+o(1)}`, not a square-root ARC child. New role4 mathematical result is typing/model-matched local transport, **not** a SAT self-contraction.

## SAT, UNSAT and adaptive resource ledger

Matched source H_U comprises eight signed ternaries over three variables, UNSAT; H_S repeats the first instead of the eighth, SAT. Both canonical lengths `N_H=340, N_G=726, N_pinned=984`. Their guarded parents are both SAT, but Q_H(1) has opposite labels.

State before: source header, available literal records, partial assignment, representation, source index, remaining budget; labels unavailable. Paid grammar/polarity scans select Horn propagation, complement-padded 2CNF SCC, affine/XOR Gaussian reduction, or exact fallback. State after: changed representation, source knowledge, branch result, optionally one witness, caches/live bit budget. We record `R=(primitive bit work, source/work reads, all writes, actual complete-state flips, peak live writable bits, cumulative live-bit-time, program/representation size)`; unchanged work writes still count as work; input and guest index tapes are accounted in FLMV's exact model; a one-bit decision does not have to enumerate proof witnesses. Virtual local service per requested bit: time O(log^2 N), extra live space O(log N); actual flips cannot be inferred from theoretical work or from Python counters.

**COMPUTATIONAL:** deterministic full independent standard-library audit (seed 202610241936) enumerated all 255 nonempty subsets of the eight proper signed ternaries, verified each guard boundary, 93,602 exact output-bit comparisons and 510 fixed-boundary decisions, total **100,207 assertion-accounted checks, zero failures**. Adaptive rule counts 15 Horn, 9 SCC, 3 affine, 228 fallback. Ten source SAT/UNSAT controls cover padded 2SAT, Horn, affine, connected/disconnected, random generic sources. GitHub compact mini is a separate reproducibility suite, not the 100,207-check full local script; raw summary distinguishes both.

## Cumulative coverage manifest, duplicates, unread queue

Inherited archive crawl: at pinned commit `55a3fcc10f74419c9c3e1a577ed0f8ce83e2f640`, 3,532 prose/source/config files were SHA-verified and keyword searched in earlier runs, **not** all mathematically read; not repeated this run. Current target reads via GitHub connector: `main13.tex` blob 87dbaad5; `AGENTS.md` c5265db0; `CODEX.md` 754999f; repo skill b8df83a7; root `main.tex` fresh SHA before reconciliation; LSPV-3 GUARDED90 6b157d9; LSPV-4 NESTED84 c62e80e and BLOCK-CLOSED85 as in the current root; LSPV-2 SELECTOR-SPLIT119; LSPV-5 NAMED-PROFILE125; LSPV-1 ENDPOINT-GUARD125; LSPV-3 INDEX88. Read original two Drive Docs IDs `1QirzuNPCG-CrE3EX6WweqsPdDbtoblCDEE4YI0HGyC0` (existential ARC) and `1TselU5xLzVf7nbD2R0r-XZz_8t-S_WNrkiOZxNpbR5E` (outage continuity with restricted HEREDITARY-SCOPED10 summary). Reviewed original FLMV PDF Section 2.1 and Corollary 5.8 including visual pages 4 and 18, and original Jahanjou/Miles/Viola local reduction. Bounded content queries HEREDITARY-SCOPED10, CP22LIFT1, PC22_ALLFIELD1, cache-miss, virtual children; bounded Library exact filename search. Neither is exhaustive or evidence of the missing executable's nonexistence.

Prior duplication: Role3 already proved guard gadget/profile; Role5 named profiles are exact CSP re-encodings, not compression; Role2 selector affine/bijunctive components are individually SAT but global join retains original SAT; Role4 NESTED84 and BLOCK-CLOSED85 falsify source-blind status/count-only reconstruction. Historical cosine-product endpoint `2cos(pi/7)` remains retired. CP22LIFT1 and PC22_ALLFIELD1 transport specific proof systems or source encodings, not arbitrary SAT deciders.

Unread/failure queue: Original full HEREDITARY-SCOPED10 compiler/experiment absent from accessible verified GitHub paths and Library match; continuity has transient path only. Drive LOG/BOOL/SIL folder pagination not exhausted. Complete mathematical reads of main2--main12 and thousands of historical bodies not done. Upstream local properization details should be independently read back from FLMV Section 3/modern Local Reductions before strengthening transport status.

## Gap status and five-role next test

**FILLED restricted:** exact ordinary output-bit guard service, charged source access, sharp task typing.
**KNOWN THEOREM:** FLMV Cor. 5.8 (same-machine matched index input; strict forbidden endpoint).
**CONDITIONAL:** source NTIME-to-proper3CNF local interface and model matching as explicitly declared.
**PARTIAL:** an NP-complete projected membership task, not mandatory SAT computation.
**FALSIFIED/RETIRED:** profile lower bound forces computation to determine parent SAT; root-scale pin contracts length.
**OPEN:** source-coherent, all-input ordinary-SAT favorable jointly-achievable-pair ARC successor, or cofinal finite route. P versus NP OPEN.

Roles 1--3 and 5 should test any proposed ARC contractor on *both* opposed Q_H(1) profiles while parent SAT is always YES, demand the exact first paid source-dependent boundary read, a strict smaller ordinary pinned child or equivalent source-coherent interface, and two-level reconstruction with cache and live-ancestor accounting. Original HEREDITARY-SCOPED10 executable remains the highest-priority missing source.

Peer report: `research/agents/lspv-4/2026-10-24_1936_LSPV-4_GUARDED_PROFILE_TRANSPORT86.tex`.
Mini: `research/agents/lspv-4/2026-10-24_1936_GUARDED_PROFILE_TRANSPORT86_MINI.py`.
Results: `research/agents/lspv-4/2026-10-24_1936_GUARDED_PROFILE_TRANSPORT86_RESULTS.json`.

<!-- END_OF_VERIFIED_HANDOFF::LSPV-4::GUARDED-PROFILE-TRANSPORT86 -->
