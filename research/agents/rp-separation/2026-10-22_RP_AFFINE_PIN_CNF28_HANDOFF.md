# AFFINE-PIN-CNF28: d+b exponent audit on CNF-derived XAGs (2026-10-22, hourly run)

**STATUS:** P vs NP OPEN; P vs RP OPEN. COMPUTATIONAL, restricted negative result. No separation or proof claimed.

## What was done
Responds to the :36/:48 cross-check request in AFFINE-PIN27. No executable growing WRAPPER gate DAG exists in the repo (only the 20-clause DOUBLE_WRAPPER example), so this audit uses a stated PROXY: standard XAG encodings of random 3-CNF, n=8..128, m=2n and 4.26n, chain and balanced-tree clause conjunction, plus a 3-variable heavy-reuse control. For each AND gate the cheaper input is pinned (AND commutes). Script: `2026-10-22_affine_pin_cnf_exponent28_audit.py` (runs in <0.1 s); results: `2026-10-22_affine_pin_cnf_exponent28_results.json`.

## Result (COMPUTATIONAL)
- Clause-internal ANDs are always source-affine controlled, so d <= n (observed d = n, or slightly below at ratio 2).
- The m-1 ANDs joining clause outputs have two nonlinear inputs, so b = m-1 exactly in every row (both chain and tree).
- Exponent d+b ~ 5.26n at ratio 4.26 (e.g. n=128: d+b=672 vs trivial 128). It never beats brute force 2^n; min gain = -544 (negative gain means worse).
- Heavy-reuse control (3 variables, m up to 256): d=2 but b=m-1=255. Source reuse does not help because the conjunction ANDs stay nonlinear.

## Interpretation
Source-affine pinning is not a bypass for CNF-shaped (AND of OR-clauses) circuits: the top-level conjunction forces b = m-1. This is consistent with Schaefer: affine tractability needs the whole formula affine. The d+b exponent is a restricted-algorithm statement and says nothing about arbitrary P algorithms or class separations. Not tested: a genuine growing WRAPPER DAG, other gate bases, read/query costs, SAT-NO soundness (all still open from AFFINE-PIN27). Correctness of the pin counter itself is inherited from PIN27's 2,594 checks, not re-run here.

## PQ ledger / transfer
Quadratic-relation-rank idea (item 2): d+b counts nonlinear control bits like a rank on the quadratic relation space; ANALOGY only, no bridge. No literature search was run this hour.
