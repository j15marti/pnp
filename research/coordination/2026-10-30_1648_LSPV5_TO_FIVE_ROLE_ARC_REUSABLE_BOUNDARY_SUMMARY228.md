# LSPV-5 -> five-role handoff: reusable boundary-summary firewall 228

**Timestamp:** 2026-10-30 16:48 America/Los_Angeles  
**Status:** restricted theorem PROVED/EXACT; universal reusable power-short frontier summary FALSIFIED/RETIRED in the declared model; ARC and P versus NP OPEN.

## Exact result

For every Boolean boundary function `f:{0,1}^b->{0,1}`, there is a uniform proper 3-CNF `A_f(X,Y)` with

`exists Y A_f(x,Y) = f(x)`

and explicit fixed-width size `N_b = Theta(b^2 2^b)`. Proper 3-CNF continuations `B_a` pin `X=a`, so `SAT(A_f AND B_a)=f(a)`.

If a deterministic preprocessor sees `A_f` before `B_a`, stores summary `S_f`, and the query phase must answer every `B_a` without rereading `A_f`, then the map `f -> S_f` is injective. Therefore some summary has at least

`2^b = Omega(N_b/(log N_b)^2) = N_b^(1-o(1))`

bits. No fixed `N^lambda`, `lambda<1`, works for this universal reusable interface.

## Scope firewall

This is deterministic one-way INDEX / knowledge-compilation storage, not a SAT runtime lower bound. It does not constrain a solver that sees `A` and `B` jointly, retains or rereads the source, recomputes messages, chooses continuation-specific children, or avoids frontier summaries. Do not import it into FLMV without a theorem forcing the same interface on every successful execution.

## Computational audit

- All 256 boundary functions for `b=3` and all 65,536 for `b=4`.
- 1,050,624 exact point-query checks.
- 87,360 existential long-clause-chain checks through `b=8`.
- 32 proper-3CNF pin-gadget checks.
- Same 32-clause skeleton: unique-boundary-model SAT source versus zero-function UNSAT source.
- DPLL: SAT 6 nodes/5 branches; UNSAT 15 nodes/7 branches.
- Raw output retains every original-clause S/U target/inversion, 992 pair compatibility records, endpoints, complements, flip trails and solver work.

## Cross-role reconciliation

- LSPV-1 JUMP-RESET-BISIM256: adopt corrected total-access head semantics; no child contraction.
- LSPV-2 AFFINE-INTERFACE258: adopt exact recognized-source rank quotient; it emits no `N^(1/2)` physical child and measured hybrid work increased.
- LSPV-3 RECURSIVE-FRONTIER-REPLAY260: adopt paid replay upper bound; this handoff blocks promotion to a universally power-short reusable message on all CNFs.
- LSPV-4 ARC-RESPONSE-WIDTH258: adopt prescribed-order residual-state theorem; reordering/replay/source access remain explicit escapes.

## Artifacts

- Report: `research/main/2026-10-30_1648_MAIN_ARC-REUSABLE-BOUNDARY-SUMMARY-FIREWALL228.tex`
- Reproducer: `experiments/arc/2026-10-30_1648_reusable_boundary_summary_audit.py`
- Raw: `results/raw/arc/2026-10-30_1648_reusable_boundary_summary_audit.json`
- Code SHA-256: `43b3936ca29601532166ec8bf6a6707a34b886b09681804da6ec5678d13e530f`
- Raw SHA-256: `61430d659f71b7083ecf169930c9a374bc6647d26bc074bfabda737a1fcdd4c9`

## Next lemma

For an actual proposed `Phi(A)` stage, prove a dichotomy: either it commits to a reusable pre-continuation summary and pays the near-linear floor, or its continuation-specific joint/source access has fully bounded probes, generated child bits, replay, cache and simultaneous ancestor space inside the ARC recurrence. This universal execution-level dichotomy remains OPEN.

P versus NP remains OPEN.

<!-- END_OF_VERIFIED_HANDOFF::ARC-REUSABLE-BOUNDARY-SUMMARY-FIREWALL228 -->
