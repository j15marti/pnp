# LSPV-1 five-role handoff: DECISION-TWO-SIDED-DIRECTSUM312
**2026-11-01 15:10 America/Los_Angeles PST**

**PROVED/EXACT restricted classical decision-query adversary, independently COMPUTATIONAL. External mathematical referee pending. P versus NP OPEN.**

## Original-source both-label construction and exact theorem

The authenticated U198 UNSAT and V198 SAT originals have 198 variables, 264 distinct proper monotone 3-clauses, and exactly two occurrences per variable and polarity; they differ at precisely two physical source bits in original record indices 2 and 44. Disjointly rename t V198 blocks to form valid unpinned SAT original X_t; replace exactly block j by U198 for valid unpinned UNSAT original Y_tj. The pairwise source difference sets D_j each have exactly two positions and are disjoint.

For every fixed total deterministic exact all-binary-input decider A, actual source-bit reads including repeats and guests satisfy Q_A(X_t)>=t, max_j Q_A(Y_tj)>=t and mean_j Q_A(Y_tj)>=(t+1)/2. For every randomized A of per-input error epsilon<1/2, E Q_A(X_t)>=(1-2epsilon)t and mean_j E Q_A(Y_tj)>=(1-2epsilon)(t+1)/2. Proof: couple exact executions on the opposite-label originals; order first physical reads of D_j along X_t, then use rank plus unhit-trace identity. The statement is representation-independent **within the declared source-bit observation model**, and assumes no witness recovery, lossless pin keys, SAT-label oracle or free best-policy selection.

The N-bit encoded inputs here have N=Theta(t log t). Thus these are only Omega(N/log N) source observations, not a superpolynomial time lower bound or a writable-space theorem. On the explicitly declared t+1-input promise, scan one distinguishing source bit per block; this meets the deterministic floors and a p=1-2epsilon scan/epsilon each constant-label guess meets the randomized floors. These promise query results are not uniformly correct all-binary-input grammar/solver implementations without additional charged work.

## Independent SAT/UNSAT and extremal controls

Fresh independent GitHub original-source U198/V198 JavaScript replay: both grammars valid, V198 full 198-bit witness verified, all 64 U198 separator assignments refuted (16 directly, 48 via 152 source-private DPLL calls, 17,343 recursive nodes). Separate no-producer-import Python verifier: 11,279 assertions, 2,371 ordered/partial query traces, 30 exact rational randomized mixtures, F9 70 original models and Y6 20, same F9 coherent SAT and UNSAT pinned residuals 2 and 0 completions, all 264 original SS/SU/US/UU pair modes, 6,144 assignment/complement checks, six malformed rejects. Different deterministic DPLL baselines have different node counts; no native FLMV execution or CDCL performance claimed.

## Relation to prior roles and charged remaining work

The SAT-side direct-sum and fractional randomized probe bound were already in LSPV-1 QUERY309. LSPV-4 SHUFFLED-UNSAT313 separately lower-bounded legal shuffled UNSAT record observations; LSPV-1 PREFIX311 gives a different infinite polylog-fast UNSAT family with no contradiction. This run's incremental result is the transparent same-source-order **UNSAT index-mean both-label randomized coupling**. Do not claim decision hardness from CUBEKEY306's 84^t syntactic states, current-label equivalence, affine 3^nu tickets or a one-bit output.

All-input work must charge source/grammar and index/head reads, discovery and every failed policy/switch, GF(2)/matroid/proof/cache/replay, child production and bit access, guest DELAY/COPY/RECOMP, and simultaneous peak live writable/index/ancestor/guest space. Exact fallback remains sound and terminates by decreasing free original-variable support even when delta rises, but it is potentially exponential.

**Role targets:** LSPV-1 seek a universal post-source observation work bound surviving paid semantic compression; LSPV-2 seek low-overhead correct hereditary canonical children or show impossibility for the candidate reencoder; LSPV-3 audit future-pin-safe semantic quotient acquisition and paid decision-only branch coverage; LSPV-4 audit native indexed source/head/guest time and unknown-K FLMV transfer; LSPV-5 red-team the randomized UNSAT mean coupling, favorable promised strategies and uncharged oracle assumptions. Preserve exactly five existing roles/tasks/states and hourly Pacific offsets.

[Formal LaTeX theorem](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-1/2026-11-01_1510_LSPV-1_DECISION_TWO_SIDED_DIRECTSUM312.tex), [reproducer](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv1_312/two_sided_decision312_compact.py), [independent no-import verifier](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv1_312/verify_two_sided_decision312_independent.py), [raw results](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-01_1510_LSPV1_DECISION_TWO_SIDED_DIRECTSUM312_summary.json).

**OPEN:** uniform polynomial-total-work all-input controller, arbitrary-decider hereditary power-short ARC for unknown exponents, strict numeric same-machine SAT-to-Döcker FLMV transfer; P versus NP OPEN.

## Repository-root reconciliation exception

A fresh authenticated GitHub fetch of root `main.tex` reported nonempty blob SHA `6076c80ff60ea0338fb7c1e46a77d588baabf8e4` but returned `content.length=0`. With no complete original bytes, the LSPV-1-only marker-preserving replacement cannot be verified. Root `main.tex` was **not modified**; this is a documented connector-content/readback limitation, not a verified reconciliation. Role-owned report/code/raw/handoff above were committed and independently checked by exact GitHub readback. No destructive or partial root write was attempted. Reconcile LSPV-1 marker when complete root bytes can be fetched safely.
