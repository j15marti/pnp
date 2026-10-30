# LSPV-3: MONOTONE-PROBE-RESUME254

30 October 2026, 09:31 America/Los_Angeles. Active issue #3. No schedule, identity, enabled-state or role changes. P versus NP remains OPEN.

## Concrete result

PROVED/EXACT, independent mathematical review pending: for fixed CNF F and monotone base extension alpha subset beta, if tau=UP(F,alpha+probe) is nonconflicting, then UP(F,beta+probe)=UP(F,tau+beta). Queue only newly assigned variables and inspect their source occurrences. Do not carry this cache across backtracking, source rewrites or additional clauses without a new validation argument. Conditional cached values must never become unconditional assignments.

Storing a nonconflict answer is FALSIFIED even when its cached assignments remain consistent with the new base. On strict22 SWAP6, probe -5 under base -2,-8 only forces -14. Adding -10 remains consistent with those cached values but causes source C3:-13, C20:-1, C8:7, C9:conflict. The same 54 source models are independently re-enumerated. The forced x2 consequence is prior; the current result concerns safe resumption and its cost.

## Fully charged restricted bound

With n occurring variables, literal count ell, maximum clause width w and source bit length N, at most 2n local probe sessions yield one complete failed-literal closure in O(N+n*w*ell+n^2 log(n+2)) indexed-word operations and O(N+(ell+n^2)log(N+2)) bits. Every session assigns each variable once; summed clause scans cost at most w*ell per session. At most n successes are freshly regenerated from source clauses and independently verified. Failed probes, base-log updates, candidate scans and sorts are charged. For strict22 ell=4n,w=3. This is NOT a bound on the complete search tree.

## Tested consequences, including losses

Same-engine whole-source selected events, UP / fresh filtered probes / resumed probes:
W1 UNSAT 24656 / 9151 / 10294.
SWAP6 SAT 12442 / 7547 / 7700.
Renamed SWAP6 SAT 1804 / 7575 / 8136.
Tseitin UNSAT 2057 / 4153 / 4677.
Dense SAT 2119 / 5568 / 5264.
Fresh and cached proof objects and DPLL nodes are identical. Cache does not add deductive power. Full original-clause diagnostics add 10616 events on each canonical 15-variable source. The simpler filter remains the better tested default on strict22.

Connected 2CNF repeated-probe workload F_k has 3k+1 variables, 4k clauses, immediate all-zero witness. The specified fresh closure procedure has Theta(k^3) selected events; resumed closure has Theta(k^2), with a counting-scan variant realizing quadratic word-RAM time. Generic comparison sorts retain the logarithmic upper factor. At k=64: 3741895 vs 279978 events, 147192 vs 608584 Python peak bytes. This is an explicit procedure time-space tradeoff, NOT a hard SAT family or a general solver improvement.

## Reproducibility and publication

Fresh audits: 15548 pair modes, 616 triple modes, 2636912 clause/complement identities. Exact fresh/cached closure proof matches on 200 random formulas; 400 truth-table solver outcomes. Independent repeated-scan oracle: 3510 resumption steps on 1200 formulas. Eighty connected strict22 roots under partial assignments: 77 SAT cofactors and 3 UNSAT cofactors; do not call pinned cofactors strict22 roots. Five corrupt proofs rejected. Eleven benchmark sources x three methods x five timing repetitions preserved logical outputs/counts. Each invocation stayed below 30 seconds.

Published artifacts in research/agents/lspv-3/ with fresh full-file blob matches:
- 2026-10-30_0931_MONOTONE_PROBE_RESUME254_PUBLIC.tex, b36d28ef13b8d071cba15243020625de84ed3b3b, commit 0ea1b63d8de0aa6aff3780244c5230231f912876.
- 2026-10-30_0931_MONOTONE_PROBE_RESUME254_check.py, 371ec0c9314d501b100d34e912eb9c3827354366, commit ce13e18e33bc455797cb3fc4a3d5fe02c9532d1c.
- 2026-10-30_0931_MONOTONE_PROBE_RESUME254_check.json, 397a76dce3c8af99d1692600473797b824bc1324, commit bd71493ce68967f1921e4e18139b352519cffbb9.

The compact standalone checker performs its own 600-formula, 1816-step resumption test and SWAP6 enumeration; it is NOT the entire performance experiment. Full source, complete raw data, six-page PDF and hashes are provided in the conversation archive. No full GitHub/Library synchronization is claimed. Main integration remains PENDING; root was left unchanged rather than reconstructed. Last root source read: 25968b221476bcaee108eb0b73dde0ef8ca6def4. No checkout preflight script was executed.

## Literature and role handoff

Known methods: Gwynne-Kullmann JAR 52(1),31-65 (2014), DOI 10.1007/s10817-013-9275-8; Biere-Jarvisalo-Kiesl SAT Handbook chapter 9 (2021). Official Z3 src/sat/sat_probing.cpp blob 1e4421a1446df06152ed1dd9e296a33563f5a5d2 explicitly caches implied literals and resets cache entries. This is precedent, not a proof of this implementation. No novelty claim. PySAT installation failed; no industrial CDCL run.

LSPV-1/5: referee monotone fixed-point identity and per-closure amortization; do not promote it to polynomial complete search.
LSPV-2: test dependency-guarded implications across source rewrites; the current theorem does not authorize that reuse.
LSPV-4: preserve cache allocation, proof regeneration, source indexing and complete diagnostic costs; native tape ledgers require separate simulation.
LSPV-3 next lemma: a checkable second-visit/activation condition that limits cache allocation and replay when reuse is sparse, without a free answer-class bit or uncharged score discovery. Universal all-input coverage remains OPEN.
