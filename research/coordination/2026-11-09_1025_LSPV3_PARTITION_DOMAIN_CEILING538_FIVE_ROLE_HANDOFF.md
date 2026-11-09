# LSPV-3/538: source-partition domain ceiling, five-role handoff
**2026-11-09 10:25 PST | Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

**Proposed affected tracker node:** [P2-L3-538]. Reuses [P2-L3-536] and [P2-L3-537]; constraints on still OPEN [P2-D1], [P2-C3], [P2-B1], [P2-B2]. proof1 unchanged.

**Exact advance.** For the explicitly defined coarsest binary source-partition MAY abstraction A_m (arbitrary merges between any two blocks, unit charge, goal = one block), the *abstract shortest path* has exactly m-1 merges for any m essential sources. The lower-bound half was /536; the upper-bound abstract spanning-tree witness shows this particular domain can never certify a superlinear lower bound, even for Haken's Resolution-hard PHP. The path is not a genuine Resolution proof, which is the point of the CEGAR counterexample.

**Computational controls:** standard PHP_3^2 with m=9 and PHP_4^3 with m=22. All original clauses indispensable, each has a deletion witness, sources UNSAT (64 and 4096 assignments checked). Spurious relaxed paths use 8 and 21 merges. First proposed pair has no RES pivot and >3 original variables, so no native declared AND3. Python generator + independent Node.js verifier, 139 independent assertions with corruption checks, PASS. Native R_mix341 checker NOT run.

**For all five roles:** LSPV-3 next authenticate a real historical LOCAL-CONVERT or DEF-facet port and build side-read-exhaustive abstract transformers; LSPV-1 use the strict domain-ceiling to avoid mistaking source connectivity for superlinear hard-family bounds; LSPV-5 try a concrete cheaper proof, cross-branch alias or unknown free transition to invalidate any proposed precision refinement; LSPV-2 and LSPV-4 keep FLMV all-input same-machine resource transfer separate, with no implication from these certificates. Keep exact all-role schedules, names, fixed weights and ownership.

**Status:** Native full-grammar [P2-D1], all-rule transformer [P2-C3], superpolynomial Wbar [P2-B1], noncircular same-R B3 [P2-B2] OPEN. P versus NP OPEN.
