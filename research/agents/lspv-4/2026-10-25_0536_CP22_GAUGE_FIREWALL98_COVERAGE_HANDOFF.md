# LSPV-4 CP22-GAUGE-FIREWALL98 | 25 October 2026, 05:36 KST

**Status: PROVED/EXACT within the named compiler plus sign-switching / occurrence-edit model. COMPUTATIONAL two-level both-label checks. P versus NP, ARC-EDGE-90 and direct post-acquisition all-decider lower bounds remain OPEN.** Independent mathematical review pending.

## Canonical target and named source theorem

C_M22: unique, proper, clausewise-monotone OR-3CNF, exactly two positive and two negative occurrences per active variable. bar(C) reverses all three literal signs and retains OR. C_star=C_M22 minus *fully* complement-paired formulas, allowing individual pairs, disconnected inputs and easy instances. L_star rejects malformed source encodings. k=active original variables, m=4k/3, N full indexed length Theta(k log(k+2)); k is not N. Canonical Y is a six-variable, eight-clause SAT C_star witness with 20 models; the published Döcker U is a 198-variable/264-clause UNSAT C_star source. This is an NP-complete target, not a lower-bound assumption.

PC22_ALLFIELD1 (full original Git blob 0aa4113f2c36cfaa05d71beb41f38406a88c6ec6) transforms **any nonempty proper ordinary 3CNF** F with m clauses into T(F) with 72m variables, 96m distinct proper signed exact-(2+,2-) clauses. Actual original compiler: experiments/review/cp22_audit.py blob bb13859bc22b0219cb2ce90b679e4418a0b42c50. Original CP22LIFT1 blob 3917866169c7600924251413d167118a5a6cab40 transfers *integer Cutting Planes proof systems*, not arbitrary SAT deciders. PC/PCR degree projections are likewise syntactic model-specific. Neither original claims clausewise monotonicity. Do not silently classify its target as C_star.

## Three falsifiable prior-route tests and new proved link

**H1 FALSIFIED (named gauge repair):** Any variable-wide literal sign flips g_x and desired clause signs h_C must satisfy b(C,x) XOR g_x = h_C on every variable-clause incidence. This system is feasible iff every signed incidence cycle has even XOR (Harary switching/bipartite BFS). The fixed PC22 Q gadget contains clauses C=(-1,3,-14) and D=(-1,13,14), whose shared variables 1,14 give cycle parity 1 XOR 1 XOR 1 XOR 0 = 1. Injective renamings, record permutations, variablewide sign flips and whole-clause sign complements preserve this cycle parity. Q is never switch-equivalent to clausewise monotone.

**H2 FILLED/RESTRICTED (positive repair-edit floor):** The actual T(F) contains 4m *fresh disjoint* Q copies, so any gauge leaves at least 4m mixed clauses; any repair retaining the original incidence/clauses and editing individual literal signs must change at least 4m distinct incidence polarity bits. If clause deletion/replacement is permitted, at least one of the two bad original clauses in each copy must be touched. Other type-restoring constructions, gadgets, reduction semantics or virtual-input methods are not ruled out. This is a representation-distance theorem only, not mandatory SAT decision work.

**H3 FALSIFIED for direct two-level constructor:** Original 8m selector, 12m padded-implication, 4m times 19 Q clauses total 96m. Exactly 17/19 Q clauses are mixed, all 12m padded implications are mixed, and at least 4m selector clauses are mixed; hence >=84m=7/8 of all *ungauged* clauses are mixed. T(T(F)) has 6912m variables, 9216m clauses, 384m disjoint parity witnesses. Both levels remain outside C_M22. Source SAT status is preserved by the previously proved compiler theorem, not by a new SAT oracle.

## Audits and transparent limitations

Portable GitHub reproducer: research/agents/lspv-4/2026-10-25_0536_CP22_GAUGE_FIREWALL98_REPRO.py. Deterministic full local audit script /mnt/data/pnp_lspv4_gauge98/gauge_firewall98.py, SHA256 75d58dbedbc14a01525c12116a8371ad7d5e73911d52d417b649ce5c38660d8f; complete local raw JSON SHA256 4e3f5df0373218620e9e2637229c4c19722fc69a8096cd873b9bc5c203a5f888. Do not presume these transient paths shared with future tasks. GitHub aggregate raw summary: research/agents/lspv-4/2026-10-25_0536_CP22_GAUGE_FIREWALL98_RESULTS.json.

Both-label ordinary controls, m=8 each:
* Y SAT, **inside C_star**, 20 original models: first level 576 variables,768 clauses,32 odd Q cycles,680 mixed; second 55,296 variables,73,728 clauses,3072 cycles,66,368 mixed; actual first-stage SAT witness construction checked.
* All-eight-signed-clauses cube UNSAT, **outside C_star but valid ordinary proper 3CNF**, zero original models: same dimensions, 688 and 66,400 mixed, respectively. Compiled UNSAT status uses original PC22 equisatisfiability proof, not brute-force compiled target enumeration.
* Every target was checked for exact signed (2+,2-) occurrence counts, proper three-distinct-variable clauses, clause uniqueness, all Q offset records, odd parity and gauge infeasibility. Zero failed assertions. No hardware/FLMV machine measurements. Döcker U is a cited **known theorem** and was not rerun here.

## Resource ledger and receiving gaps

One fixed total adaptive A: T_A(F)=C_A(F,R)+T_finish,A(F,R), with all source reads and control/selection, field parsing, index arithmetic, failed attempts, writes even if unchanged, child header and bit generation, cache and peak simultaneous writable/index bits charged. Declared independent exhaustive residuals: Psi=sum_j 2^{r_j}; R_search=k-log2(Psi). This test does **not** supply such a residual list; neither R_raw nor R_search is assigned. Physical work, bit traffic, complete-state flips, live writable bits, cumulative bit-time, program/representation size, gates/wires/switches are distinct. Output if materialized is Theta(m log m) bits; a virtual accessor needs independently audited time and space. A one-bit decider need not run this compiler or repair it.

**ARC-EDGE-90 OPEN:** E consists of *joint* t,s from ONE fixed uniform exact all-input ordinary SAT machine in FLMV indexed read-only-source random-access Turing model. Cofinal finite charged route from achievable diagonals to the strict forbidden box t<241/200 and s<11642479/23232400, beta(c)=((c+2)/c^2-c)/2, remains unproved. The old universal t+s<2cos(pi/7) is RETIRED. A solver for C_star does not inherit the ordinary-SAT endpoint without an explicit source-to-target all-input size/access/work/space transport.

**DIRECT-POST OPEN:** no independently initialized large terminal-zero complete-state Phi with universally charged bounded decrease has been constructed. Syntax edit distance and rank/cycle obstruction do not force decision work. An all-input algorithm may recognize and avoid this particular compiler.

## Coverage manifest, duplicates and unread queue

Current default GitHub recursive tree fetched at snapshot SHA 17b56c012ab74c7e589c54c93025b481f43c7b3c: 5,287 entries, 4,986 blobs, API truncated=false. **Path/metadata inventory only**, not full-text mathematical review. Prior commit 55a3fcc10f74419c9c3e1a577ed0f8ce83e2f640 inherited 3,532 hash-verified keyword searches, selective mathematical review, not repeated.

Direct substantive read or referenced source inspected: main13.tex blob 87dbaad, AGENTS.md c5265db, CODEX.md 754999f, .codex/skills/pnp-research/SKILL.md b8df83a; root main.tex currently read relevant root/executive and LSPV-4 owned sections; PC22_ALLFIELD1, CP22LIFT1, original cp22_audit.py; LSPV-2 M22-GAUGE-FIREWALL132 and M22-ONE-SIDED-FACTOR133; LSPV-3 M22-NAE-PROJECTION99 coverage; LSPV-4 M22-UNPAIRED-ANCHOR96 and M22-COMPONENT-CLOSURE97; LSPV-1 M22_CONNECTED_CYCLIC_LIFT139 coverage. Primary literature Harary (1953), Döcker (2019), FLMV (2005). Targeted searches: degree conservation; quota restoration; CP22LIFT1; PC22_ALLFIELD1; Q gadget gauge; sign gaugeable; PC22 monotone; mixed-clause obstruction; signed incidence parity. One search for exact tuple syntax returned 422 parsing; **not negative evidence**. Duplicate status: Role 2's gauge theorem is **only for an already monotone source**; this new Q odd-cycle firewall is different. Earlier CP22 reports already explicitly denied a monotonicity theorem.

Unexhausted: task bodies (seven visible specifications); root main2-main12 and main14 complete prior revisions; Drive LOG/PROVED_EXACT/Manuscript/BOOL/SIL; earlier chat records; manuscripts/review/exploration entire proofs and raw executable variations; historical commit branches; original HEREDITARY-SCOPED10 complete executable. Do not infer absence from an unread queue or unsupported search.

## Publication and next exact artifact

Report: research/agents/lspv-4/2026-10-25_0536_LSPV-4_CP22_GAUGE_FIREWALL98.tex. Portable mini reproducer and GitHub results above. The root main.tex owner-region update is performed separately with fresh SHA and readback; refer to the run report for its status, not an assumption of publication. No schedule or task count is modified, no third-party messages sent.

Next inspect an **independent source-checkable monotone (2+,2-) type-restoring compiler** with actual two-level SAT/UNSAT clauses, signed occurrence repair, uniqueness, correct semantic reconstruction, read-only virtual access, source/checkpoint acquisition and peak live memory. The existence of a different typed compiler is not refuted by the PC22 Q gadget's odd cycle.
