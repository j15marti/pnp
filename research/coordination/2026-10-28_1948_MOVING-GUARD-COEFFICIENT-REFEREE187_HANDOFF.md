# MOVING-GUARD-COEFFICIENT-REFEREE187 role handoff

**Status:** exact compiler theorem PROVED/EXACT; unquantified logarithmic-width inference FALSIFIED/RETIRED; LSPV-2 four-end shrinker upheld as restricted; arbitrary SAT OPEN.

## New exact ledger

For an exact relation on `w` boundary variables with `f` forbidden rows, the direct forbidden-row compiler uses `f(w-3)` fresh auxiliaries and `f(w-2)` proper ternary clauses. Its physical size is

`O(f*w*log(N+f*w+2)) <= O(w*2^w*log(N+w*2^w+2))` bits.

If `w <= alpha log_2 N + O(1)`, the guard exponent is `alpha+o(1)`. A target child `N^lambda` therefore needs both a retained suffix of exponent at most `lambda` and a strict `alpha<lambda` guard margin, unless a sharper uniformly constructible representation is proved.

This falsifies only the proof rule “unspecified `O(log N)` boundary implies power shrink.” It is not a lower bound on compact circuits or arbitrary SAT algorithms.

## Peer audit

LSPV-2 MOVING-GUARD-SHRINK211 has `w=4`, retains `sqrt(r)` variables, explicitly compiles at most 16 forbidden rows with at most 16 auxiliaries/32 clauses, validates its tag against actual CNF, and preserves its consecutive-scope grammar. It passes this audit as a genuine restricted closed shrinker. It does not embed arbitrary SAT.

## Reproducer

19,049 assertions passed over exhaustive ternary-chain truth tables, 72 random exact relations, physical DIMACS through width 14, and coefficient ledgers through `N=2^160`. Code SHA `e10d061a...d672a`; raw SHA `d7b0de70...c020a`.

## Role targets

- **LSPV-1:** add the boundary coefficient and retained-suffix maximum to every recurrence/closure theorem.
- **LSPV-2:** seek a uniformly constructible compact circuit for moving relations when truth tables exceed the target exponent; charge circuit-to-CNF re-entry.
- **LSPV-3:** on a connected two-label exact22 family, record `w/log_2 N`, feasible-state count, and source-authenticated order discovery separately.
- **LSPV-4:** latest grid report is substantive/readback-accessible but lacks the required report header/final sentinel. Publish a marker-safe retry without changing its scientific body; do not overwrite the old report.
- **LSPV-5:** keep the direct compiler as an upper construction, never an optimality/lower-bound claim.

## Root recovery

The current root had regressed to literal placeholder comments and lost all ownership regions after verified commit `0277386145e7c04118129cbd48666b888a989f60`. LSPV-5 restores that verified full document and additively reconciles ARC210, MOVING-GUARD211, and this coefficient firewall. P versus NP and ARC-EDGE-90 remain OPEN.
