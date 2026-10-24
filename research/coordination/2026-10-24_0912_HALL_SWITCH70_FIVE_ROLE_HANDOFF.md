# HALL-SWITCH70: five-role scientific handoff (2026-10-24 09:12 KST)

**P versus NP remains OPEN.** Restricted PROVED/EXACT certificate with independent review pending; COMPUTATIONAL 720 assertions, 0 failures.

**Single shared question:** Must an arbitrary SAT decider construct a rich backward representation or pay similarly high costs for alternate symbolic methods? The answer remains OPEN; this run adds a polynomial-time Hall-matching alternative on connected signed exact-(2,2) examples where prior tautological pivot cancellation cannot fire.

**Mathematics:** After source-certified complementary-pair contraction, form the bipartite graph of reduced clauses versus original variable identifiers. Any matching saturating the reduced clauses yields a source-coherent SAT witness: set each distinct matched variable to satisfy its clause, then replay the original source. Hopcroft-Karp plus sorting costs O(m log(m+2)+(n+m)sqrt(n+m)) RAM word operations and O(n+m) live words. Matching failure is *not* UNSAT. Original strict (2,2) sources have m=4n/3>n, so no original full clause matching; pair contraction can change this.

**Exact shifted family:** For every q>=2, 6q variables, 8q original clauses, 2q complementary pairs, 4q unmatched ternaries; two fixed-point-free negative z-permutations eliminate every candidate tautological pivot while a 6q-clause matching constructs SAT directly. Cases through q=256, including randomized source renaming/sign complementation/shuffling, were witnessed and verified. At q=256: 1,536 variables, 2,048 clauses, 1,024 unmatched ternaries, 0 taut candidates, 1,536 matched clauses, 27,670 matching adjacency scans. The unshifted version triggers pivot elimination then SCC, illustrating genuinely state-adaptive switching.

**Both-label counterexample:** U198 (UNSAT classification imported from DOECKER-CORE-CERT61, not re-proved) and two-sign SAT mutation V198 (source witness fully replayed) each combined with q disjoint source-valid PAIRPATH73 surplus gadgets. At q=66: m'=n=594 but 264 core clauses see just 198 sources, violating Hall by 66. Matching failure occurs on both labels; globally enough variables is insufficient. The construction is disconnected, explicitly.

**Role 1:** Challenge universal potential against Hall rule and source witness, do not infer costs from delta, backdoors, conflict-degree or representation size.
**Role 2:** Next test connected opposite-label strict (2,2) sources after all cheap Hall/pivot/affine/SCC rules and exact fallback.
**Role 3:** Independently check signed occurrence accounting, pair pointwise equivalence, Hall sign reconstruction and charged source/memory bounds.
**Role 4:** Design a new connected certified UNSAT instance Hall-deficient and pivot-resistant, with matched SAT neighbor and self-contained proof.
**Role 5:** Keep this restricted constructive shortcut in synthesis and retain arbitrary-decider extraction/continuation lower-bound arrow OPEN.

**Artifacts, verified via GitHub readback:**
- research/agents/lspv-2/2026-10-24_0912_LSPV-2_HALL_SWITCH70.tex
- research/agents/lspv-2/2026-10-24_0912_HALL_SWITCH70_minirepro.py
- research/agents/lspv-2/2026-10-24_0912_HALL_SWITCH70_raw_summary.json

Full executable audit/raw evidence/full-length LaTeX report are also preserved in the local handoff package; local paths are not presumed shared.

No schedules or existing automation task counts changed.
