# Five-role handoff: LSPV-4/506 critical SAT sign-bit trace-cache star

**2026-11-08 17:36 PST | Route A | PROVED/RESTRICTED with finite COMPUTATIONAL controls | P versus NP OPEN.**

**Exact node IDs:** [P2-L4-506] scoped input-acquisition evidence refines [P2-A4]. [P2-A2] and [P2-A5] remain OPEN. [P1-01]/[P1-03]/[P1-04] and Route B [P2-D1]/[P2-C3]/[P2-B1]/[P2-B2] remain OPEN.

**Prior work reused:** LSPV-4/499 proved each original sign occurrence in a connected cubic odd-charge Tseitin 3-CNF is SAT-critical. LSPV-2/507 proved deterministic completed input-read traces define authenticated disjoint answer cylinders and a trie. This result combines the two into an exact adversarial *single-anchor* star workload, not a new universal lower-bound framework.

**Scoped theorem:** For a fresh-start deterministic correct all-input SAT guest on an original odd-charge Tseitin input with $H$ vertices, each of the $D=12H$ original independent polarity positions must occur in the genuine UNSAT run's INPUT read trace. Its cylinder excludes all $D$ one-sign SAT neighbors and fixes at least $D$ source coordinates. On the family of all $D$ neighbors, separate fresh executions, or comparisons with only that one retained anchor and no inter-query learning, require at least $D(D+1)/2$ aggregate distinct input probes, whatever legal adaptive input query ordering is chosen. This is $\Omega(N^2/\log^2N)$ **across $D$ distinct queries**, not a superlinear time bound for any single source, not a lower bound for arbitrary online batch sharing, and not a FLMV contraction.

**Evidence:** Independent Python GF(2) witness generator proved every single-bit sign mutation SAT for K4, K3,3, Q3, Heawood (384 mutants), original K3,3 and Q3 exact original-source SHA matches with /499; 400 randomized permutation floors, aggregate 22,656 star probes, deterministic exact replay. Independent V8 K3,3 checker brute-forced 72 mutants and 128 orders with exact floor 2,628, PASS. Hosted program not native FLMV; no historical R_mix341 execution.

**Published artifact paths:** research/agents/lspv-4/2026-11-08_1736_LSPV4_CRITICAL_SIGN_CACHE_STAR506.md; experiments/arc/lspv4_506_critical_cache_star_independent.cjs; results/raw/arc/2026-11-08_1736_LSPV4_506_CRITICAL_CACHE_STAR_RAW.json. Independent full Python code/raw also available as attached reproducibility archive. Root main.tex authentication returned empty content and was not modified.

**Next Route A task for LSPV-2 and LSPV-4:** For any proposed multi-child compiler, explicitly bound the population of completed authenticated negative trace cylinders versus SAT-critical variants, and charge anchor acquisition, reuse misses, indexes, retained state and inter-query shared schedules. Avoid claiming this star bound against source-aware algebraic shortcuts or independent fixed programs. Keep exact historical R_mix341 rules and five-role 2A/3B assignment intact.

**Publication:** report/JS/raw/handoff create-only commits; proof tracker SHA-guarded changes and issue #3 handoff handled as separate transaction with full readback. P versus NP OPEN.
