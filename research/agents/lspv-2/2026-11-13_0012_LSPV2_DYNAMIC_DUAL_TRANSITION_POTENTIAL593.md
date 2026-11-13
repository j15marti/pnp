% LSPV-2 REPORT::593::2026-11-13_0012_PST
# LSPV-2/593: A transition-consistent paid-once dual potential, and its zero-cost mixed-shortcut falsifier

**2026-11-13 00:12 PST | SAT-Circuit Reduction Builder | historical Route A retained | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## One construction and four falsifiers

**Candidate for restricted P2-C3:** upgrade the certified terminal Set-Cover envelope of LSPV-2/592 into a **stepwise consistent lower-bound transformer** over shared-DAG histories with each distinct owner charged once. A fixed feasible dual witness yields a nonnegative potential whose decrease on **every** legal owner-purchase transition is at most the new distinct-owner payment. This is a theorem ONLY of an independently declared necessary-obligation cover transition system, not historical R_mix341.

F1: one shared owner satisfying m branch-AND obligations can make the potential drop by more than its single charge. F2: a fractional 3/2 abstract cost is automatically a realizable integer proof. F3: reusing already paid gate owners through arbitrary free facets incurs a second payment. F4: excluding an unauthenticated zero-charge mixed shortcut preserves the potential lower bound. F1-F3 are disproved in restricted tests and original /386 controls; F4 is positively demonstrated as a real model-level soundness failure of the omitted-rule abstraction.

## Complete restricted theorem and proof

Let U be a finite set of **authenticated necessary** obligations, I a finite set of distinct globally paid owner identities, C_i a subset of U covered by owner i, and w_i >= 0 its once-only tariff. The concrete paid history D is a subset of I. Every completed trace must have union of C_i over i in D equal to U. All source, context, port, freshness, branching, and mixed-rule constraints are additional concrete conditions; this independent cover representation is not asserted to characterize them.

A permissible transition may add any A subseteq I while retaining already paid identities. Its marginal logical cost is

$$
\Delta W(D,A)=\sum_{i\in A\setminus D}w_i,\qquad
D'=D\cup A.
$$

Fix any nonnegative dual vector y indexed by U satisfying the certified constraints

$$
\sum_{u\in C_i}y_u\leq w_i\quad\text{for every owner }i.
$$

Define the state potential

$$
h_y(D)=\sum_{u\notin\bigcup_{i\in D}C_i}y_u.
$$

**Theorem 593.1 (stepwise consistency, complete proof).** For every D and A,

$$
0\leq h_y(D)-h_y(D\cup A)\leq\Delta W(D,A).
$$

Indeed, each obligation removed from the uncovered set is newly covered by at least one owner i in A \ D. Assign each such obligation to one such i. The sum of its y-weights is no greater than the sum of the full owner coverage y-weights, which by dual feasibility is at most the sum of the w_i for newly paid owners. No old owner is charged twice; this holds for arbitrarily many obligations and simultaneous branch-AND requirements. On a valid terminal paid history, h_y=0, so telescoping gives h_y(D) <= **every** concrete remaining paid work from D. This is a consistent, admissible lower-bound potential for this restricted model.

If a transition merely reuses an already paid node, D'=D and the potential change is exactly zero. A claimed abstract transition cost greater than concrete paid work would violate the MAY cost condition; our transition costs are equal by definition. A further source/context/wire projection must be shown to simulate **each authentic rule** independently before this potential can serve historical P2-C3.

**Theorem 593.2 (zero-cost shortcut collapse).** If a newly admitted cost-zero owner i covers any u for which y_u>0, the dual constraint for i fails. In particular, if an unauthenticated legal rule could discharge *all* necessary obligations at zero cost, every feasible y has h_y(D)=0 from an empty paid history. Thus a positive projected lower bound is conditional on authenticating all rule shortcuts and certifying the necessity of U. Unknown mixed operations are MAY, not illegal. This is a formal explanation for why a restricted /386 dual cannot be elevated to full R_mix341.

**Constructive feasible dual for tests:** Set y_u to the minimum of w_i/|C_i| over all owners i covering u. For each owner i, summing these fractions over C_i gives at most w_i. This construction is polynomial in the explicit incidence size but need not be the strongest dual and does not construct or decide an optimum SAT proof.

## Falsification-first executable results

Exact reference program: experiments/arc/lspv2_593_dynamic_dual_potential.cjs. Git blob SHA 9e4944af2cb6d53c2f7a3abc0b3d646674902314. Local SHA-256 f38fd6c6b0ce3432f5ff6714a2caf53d67c842272de0fac9488136c9737913ed. Raw JSON: results/raw/arc/2026-11-13_0012_LSPV2_593_CONSISTENT_DUAL_POTENTIAL_RAW.json, Git blob d7bfbf1600597ac806b16eb3d7c9f6a2bc77137a, local SHA-256 2d77c73015947a30096529326dceb1e7110fe21770b9a4cded068ef1d1261221.

The standalone Node.js execution tested 5 exhaustive shared-owner star families m=2..6, one triangle fractional integrality control, 120 seeded finite positive-weight incidence instances, and a deliberate unauthorized zero-cost escape: **127 cases, 94,261 assertions, 6,092 paid-prefix comparisons, 80,856 paid-transition checks, all PASS**. The triangle has dual potential 1.5 versus cheapest integer cover 2. A two-obligation toy has falsely retained y=(1,1), and an omitted zero-cost owner covering both produces an **illegal potential decrease of 2 at zero cost**. Re-adding it to the owner model forces the dual to zero. The 120 cases are deterministic pseudo-random, seed hexadecimal 593c0de; all finite enumeration and exact-cost minima were checked for the small instances.

Separately, the **unchanged original archived /386 sibling checker**, SHA-256 22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113, was run as a fresh Node OS process on each existing externally tested packet: ACCEPT W29 (one owner, 0 free facets, 2,867 bytes); ACCEPT W32 (one owner, 2 free facets, 3,153 bytes); ACCEPT W32 (one owner, 130 free facets, 9,970 bytes); REJECT all three bad terminal-pivot mutations. Each positive has 17 SOURCE clauses. The original native checker and packet hashes are pinned in the reproducibility archive. These are reused positive shortcut controls from /592, not newly authenticated grammar. The native checker is a different source- and Resolution-only program from /341 and is **not the missing full historical R_mix341 checker**.

This run distinctly tracks paid logical work (29/32/32), file bytes, source access, checking processes, abstract transition probes and semantic proof construction; it makes no claimed native verifier-time, worst-case span or peak-space lower bound.

## Source/novelty audit and barrier discipline

Read original proof1.txt Git blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343 and full proof2.txt immutable Git blob f678f707880da4dfc97dabf778430c6dc816cb1f, issue #3 and latest peer entries, AGENTS.md, CODEX.md, the pnp-research skill, relevant actual LSPV-2/539–549 and /582–592, LSPV-3/607, LSPV-1/612, LSPV-5/520 and the latest shared handoffs. The surviving original /341 and /386 rule dispatchers, the /341 accepted SAT-source String bug, source occurrence requirements, existing shared paid-history controls, and the /592 Set-Cover endpoint LP are **previous work**, not original discoveries claimed here.

Primary sources: Cook and Reckhow (1979), https://doi.org/10.2307/2273702 (fixed sound proof-system checking); Cousot and Cousot (1977), https://doi.org/10.1145/512950.512973 (sound abstract simulation); Clarke et al. (2000), https://doi.org/10.1007/10722167_15 (CEGAR); Cruz-Filipe et al. (2017), https://arxiv.org/abs/1612.02353 (certified LRAT checker); de Colnet and Mengel (2021), https://arxiv.org/abs/2103.09609 (bounded-degree Tseitin regular Resolution, different proof model). Consulted repository references konard/p-vs-np, blkph0x/p-vs-np-proof-research, meelgroup/frat-xor and tanyongkiam/cake_lpr; none supplies the absent private single mixed dispatcher. The mathematical argument is the standard feasible-dual amortized inequality, here used as a **new restricted P2-C3 step-transformer regression**, not a claim of a new optimization theorem. Any transfer from external proof grammar, LRAT or regular Resolution to R_mix341 remains OPEN.

The unknown-rule toy is a **FAILED TRANSFER** control: an obligation family not certified across all legal transitions cannot support a positive all-rule dual lower bound. Relativization, algebrization, natural-proofs and SAT-uniformity obstructions are not circumvented. Tractable Horn/2SAT/XOR instances, learned clauses, extensions, reconvergent proofs, and inexpensive mixed-rule shortcuts remain required positive controls. The computational search is finite and does not prove a growing historical lower bound.

## Exact remaining status and handoff

P2-D1 **OPEN** (complete original accepted-byte grammar and externally authenticated mixed checker missing). P2-C3 **OPEN** (no all-rule concrete/abstract simulation; the restricted dual transformer is conditional on necessary certified obligations and authenticated owners). P2-B1 **OPEN**. P2-B2 and B3 **separately OPEN** and noncircular. P1-01/03/04 **OPEN**. **P versus NP OPEN.**

**Next target:** obtain a genuine historical single-checker accepted, externally SOURCE-bound RES-to-AND3 or DEF-to-LOCAL-CONVERT packet with rejected corrupt signed-port control; derive every valid positive obligation incidence from that actual checker before attempting an all-rule potential lower bound.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Neither proof tracker needs a status/node change from this explicitly restricted result. Root main.tex was reconciled only inside the LSPV-2 owned region: old Git blob c8ea33f799a149c54adb1ee76bf5dbcbbca471fc, new blob d461c99badfe7c7dad3060ece16f8ee549f4a1ae. Exactly one 1,680-character insertion; removing it restores the entire old blob. All five BEGIN/END ownership pairs remain balanced, and every non-LSPV-2 byte is unchanged. All five existing roles were privately verified enabled with their unchanged Pacific schedules, titles and two Route A / three Route B allocation. No automation was created, renamed, disabled, duplicated, or rescheduled. Historical weights and ownership boundaries unchanged.

% END_OF_VERIFIED_REPORT::LSPV-2::593
