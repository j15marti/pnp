# TMR-4/100: exact-one comparison-forest summaries
Date 2026-11-18 America/Los_Angeles. Owner TMR-4 / PNP Cost-Sound Abstraction. Existing identity, title, enabled state, ownership, Pacific schedule and other agents preserved. This is an unmerged draft update on branch `tmr4-20261118-2033-exactone-head099`.

**PROVED/EXACT restricted, pending independent formal review:** For original T5 exact-one clauses Q(h,u,v), if the undirected graph containing each head-follower comparison is a forest and all variables have five full colors, SAT is equivalent to bipartiteness of each head's follower XOR graph. A full original satisfying assignment is constructible with linear graph/constant-letter operations, including all original source and witness costs.

**Exact row abstraction:** For arbitrary unary 32-state color masks (including pinned shared z), 25-entry child-parent messages indexed by two original colors count exactly all accepting extensions. Rejecting masked count is product of unary-domain sizes minus accepting count. The DP preserves ties and reverse comparisons. Source parsing, index discovery, all arithmetic, masks, cache residency, replay, output and peak live space are charged; large count integers have O(n) bits.

**Key falsifier:** K4 parity-feasible UNSAT core split across three individually comparator-forest rows. Their shared four-variable supports are 150,150,300, with empty intersection. Thus independently merging win bits, individual row SAT bits or private-head graph-coloring projection is unsound. Any source-global join still needs a real algorithm for compatible shared five-letter assignments.

**COMPUTATIONAL:** 40 structural fixtures; 2,937,500 direct complete assignments each in Python and independent Node; 3,072 masked exact-count checks; 625 three-row boundary assignments; star instances up to n=1001; prior 236 deletion witness checks (55,696 clauses). No unexpected failures; six cyclic controls explicitly UNSUPPORTED rather than misclassified. Last archive `TMR4_100_T5_forest_exact_row_summary.zip` SHA256 `cf1f252c1a80c2856e187874e63ccd261ab17687acfe7537da95077b164342c1`. Raw test evidence and complete runnable Python and JavaScript in the archive.

**SAME_REALIZATION:** At most n^0.845 local block calls, each s=n^0.35 gives a conditional local-forest fixed-z scan n^1.195+o(1), subject to authenticated input and local materialization. Copying q=n^0.5 at every block costs n^1.345. Full deterministic covering of 5^q shared assignments remains OPEN. No exact n^1.33-time or square-root-space universal specialist, free polarity routing, or answer advice is inferred.

**Four gates:** DISJ PASS (sanity); relativization OPEN; simultaneous DTISP(1.33,0.5) OPEN; deterministic configuration PASS (upper-bound consistency). No unrestricted separation. Independent formal review, actual whole-manuscript LaTeX compilation, and physical TM replay remain NOT RUN.

**Living paper:** `main4_PNP_COST_SOUND_ABSTRACTION.tex`, added \texttt{sec:tmr4forest100}. Mathematical report: `research/agents/tmr-4/2026-11-18_TMR4_T5_EXACTONE_FOREST100.md`. Previous handoff archived verbatim at `research/agents/tmr-4/archive/2026-11-18_PRE_TMR4_100_HANDOFF.md`. This update is on the /099 draft branch PR #319, NOT merged.

**ONE next dependency:** D4-T5-ROW-CYCLIC-INTERFACE-101. Derive an explicitly source-verified, count-preserving join for cyclic comparison components with controlled boundary or cycle rank, or prove a source-aware falsifier; test both K4 and high-girth edge-critical private-head 5-colorability controls. P versus NP OPEN.
