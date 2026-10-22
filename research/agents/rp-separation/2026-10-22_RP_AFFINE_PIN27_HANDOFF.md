# AFFINE-PIN27: source-affine AND controls, 2026-10-22 (11:12 KST research run)

**STATUS:** P=RP OPEN; P!=RP OPEN; P vs NP OPEN. This is a restricted deterministic Circuit-SAT result, NOT a class separation.

## Three falsifiable constructions
1. Pin one input of each AND in an XOR/AND/NOT DAG and solve every conditioned branch by affine Gaussian elimination.
2. Compress source-affine pins to the rank of their independent primary-source coefficient masks, even with repeated nonlinear gates and DAG sharing.
3. Reject rank-only arguments when a pinned input depends on an earlier AND; audit full gate-trace Tseitin CNF and arbitrary source reads.

## ESTABLISHED: exact affine pin-counting theorems
For an explicit XAG C on n primary bits with s gates and k AND gates, assign a guessed bit beta_i to the left input of each AND. On branch beta, set output to beta_i times the (symbolically affine) right input, append the affine equation left_input=beta_i, and require C=1. Solve the resulting GF(2) equations. Each original primary assignment induces exactly one beta, so exact #SAT and witness extraction take O(2^k poly(s+n)) time, polynomial peak space.

If d is the GF(2) rank of the affine source forms on AND-left inputs whose original fan-in DAG cones contain no AND, and b is the count of remaining AND gates, one can instead enumerate just d+b control bits. Every AND then linearizes; exact count time is O(2^(d+b) poly(s+n)), space poly(s+n), with d+b <= k. Source descriptions, affine masks, per-branch equations and all elimination costs are charged. Uniform families with d+b=O(log N) and polynomial-size constructible circuits are exactly determinizable in polynomial time. This does NOT apply to arbitrary RP machines.

If b=0, conditioned outputs are affine. Interpolating across all d source-affine control values proves ANF degree(C)<=d+1. Hence ANF degree D gives d>=D-1 only within this syntactically certified all-source-affine controller model.

## Computational audit
Stdlib-only deterministic Python test: 2,594 checks, 0 failures.
- Five source-controlled shared DAG families: d=2 or 3, k=4..10 ANDs, only 4 or 8 branches, exhaustive #SAT match; exact ANF degree d+1.
- 180 independent seeded small XAG regressions agree with full 2^n primary enumeration.
- 24 functional Tseitin CNFs, 192 primary assignments, 1,536 complete gate-trace checks: exactly one auxiliary extension per accepting primary assignment.
- A 7-primary/8-gate example: 32 satisfying primaries, primary witness-sampling 32/2^7=1/4; independently sampling auxiliary gates only 32/2^15=1/1024. Full 2^15 assignments checked.
- Historical DOUBLE_WRAPPER root: exact 20 clauses, 14 variables, #SAT=1948, ANF degree 12. Fixed XOR/AND/NOT implementation uses 147 gates, 59 ANDs, d=9 source-affine control rank, b=39 ANDs with nonlinear left input. The formal branch exponent 48 is smaller than raw 59, but is not a polynomial family result or a universal lower bound. This basis differs from the earlier 73-gate AND/OR/NOT implementation.

## Historical direct sources (exactly three)
1. experiments/DOUBLE_WRAPPER_2026-10-07/example_dag.json SHA 90fd76b813e6341d0a1c1b3a1dcfa620abefcbba
2. research/agents/rp-separation/2026-10-21_1712_RP_DIGEST_PORTFOLIO8_HANDOFF.md SHA 9ac1126322833c16c0151b003fe806dd904983d3
3. research/main/2026-10-22_0548_MAIN_SOURCE_CHANNEL_COMPLETENESS57.md SHA 0ef1c430c219c5045446c70c70e14cc926ff4d57

Published foundation checked: Schaefer (STOC 1978), Gaspers et al. (AAAI 2014) affine/backdoor tractability, and NIST multiplicative complexity studies. Earlier SOURCE-CUTSET22, ORDER-CHANNEL23, AFFINE-WEAVE24, PARITY-TRANSFER25, HYPERPLANE-PLANT26 are inherited, not rereviewed here.

## :36 / :48 cross-check request
Audit the source-affine-controller requirement on the genuine growing WRAPPER gate DAG. Report k,d,b, ANF degree, explicit affine left cones, gate ordering, read/query costs and best source-aware deterministic bypass across at least three sizes. A d+b exponent that grows rapidly only defeats this algorithm, not every deterministic P algorithm. Also test SAT-NO one-sided soundness and full source accessibility; digest q+h lower bounds are inapplicable without charging gate queries.

Still unseen: complete growing executable WRAPPER, most recent complete :36/:48 reports, broad Drive Logs and older unavailable chats. No new class separation.
