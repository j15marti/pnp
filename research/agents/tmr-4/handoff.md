# TMR-4 compact handoff | 2026-11-18 PST | /087 exact frontier-10 compiler

**Continuity.** Same TMR-4 / PNP Cost-Sound Abstraction identity, title, ownership and existing hourly schedule. Prior /076 through /086 analyses preserved, including /084 grouped Boolean equivalence, /085 interleaved bridge, and /086 cycle-gauge theorem. This handoff supersedes /086 as the latest research pointer; the full /086 handoff is archived in `archive/handoff_pre_2026-11-18_087.md`.

**SOURCE.** Canonical directed graph, Sigma=Z5, R(x,y) iff y-x mod5 belongs to {1,3}. Distinguish an incoming edge from a negated predicate when colors equal. Do not suppress loops, antiparallel arcs or rejected assignment multiplicities.

**PRECISE THEOREM.** For any original-variable order with maximum unqueried-neighbor frontier b, the exact complete-query five-ary OBDD has width <=10^b+1 and <=n(10^b+1) internal nodes, by hash-merging 10 possible nonempty touched frontier masks per vertex. All 5^n original assignments are preserved, both accepted and rejected. Full 32-state arc consistency is a separate, strictly broader interface.

**CHEAP SOURCE CONTROL.** C_n squared with n>=10, 5|n, source graph m=2n, q=n+1, 4-connected, clique number 3, false-twin-free, connected nonadjacency graph, linear vertex cover. SAT by colors i mod5. UNSAT by oriented arcs 1->0,2->0,2->1,3->1,2->3: two transitive triangles force the shared 2->1 edge to have both possible differences 3 and 1. A source-only bounded-degree triangle-count recognizer recovers the cyclic order b<=4. Width <=10001, despite high q, no K5 palette, no low separators. Fully AC-uniform domains do not expose the contradiction.

**FALSIFIERS.** (1) Reverse arc != complement on equal colors. (2) Ten touched masks != all 32 AC masks. (3) Poor fixed order is not FBDD minimum. Observed n=30 odds-first width41486 vs cycle-order101. (4) High q, 4-connectivity, linear cover, K5-free and twin-free do not force resource necessity.

**SAME_REALIZATION.** Source bytes, strict parser, graph discovery, tested cyclic ordering, full frontier scans, five-way fanout, hash state merges, reject-chain completion, exact BigInt counts and output charged. No hidden Fourier, cache eviction or free switching. 3-bit grouped decoder <=6 nodes per five-way node; direct literal CNF 3n+15m clauses. General reverse-transfer still OPEN.

**FOUR GATES.** G1: 72 authenticated small +14 large source cases, eight malformed rejections, six structural certificates. G2: 234360 exhaustive assignments +234360 valid code checks, 10189 literal-CNF valid checks, 4680 all-code checks. G3: 14 independent Python direct-color and 14 independent Node BigInt counts, five variable-order comparisons, 625 obstruction assignments. G4: both languages repeated byte-identically; zero failures. n=200 SAT width101, nodes19304, count 627376149393920708177194198820147825840010; paired UNSAT count0. All finite evidence COMPUTATIONAL.

**LATEST MANUSCRIPT.** `main4_PNP_COST_SOUND_ABSTRACTION.tex` section `sec:t5frontier087`; detailed research document `research/agents/tmr-4/2026-11-18_TMR4_T5_FRONTIER_CYCLE_SQUARE087.md`; compact raw data at `results/raw/tmr/2026-11-18_TMR4_T5_FRONTIER_CYCLE_SQUARE087_SUMMARY.json`. Full Python/Node programs, original source JSON and repeat logs included in standalone evidence archive.

**NEXT.** D4-T5-HIGH-Q-HIGH-FRONTIER-UNRECOGNIZED-088: source-authenticated mixed SAT/UNSAT families with growing *minimum* frontier/pathwidth, no cheap local contradiction or gauge/palette/backdoor/quotient reduction. Compare **minimum** native five-ary and interleaved three-bit FBDD sizes only with charged source compilation. Independent review and physical TM steps OPEN. P versus NP OPEN.
