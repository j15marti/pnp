# LSPV-5 handoff: CERTIFIED-PORTFOLIO-DOVETAIL-REFEREE268

1 November 2026, 08:48 PST. P versus NP remains **OPEN**. No task, title, enabled state, schedule, identity, or role ownership changed.

## Exact result

For a **fixed finite** public portfolio of deterministic source-authenticated partial procedures, geometric restart scheduling removes any free best-policy oracle. If the fastest policy on the current source completes in `T*` charged native steps, one-policy-at-a-time budgets `1,2,4,...` use fewer than `4 k T*` simulated policy steps, plus `O(k log T*)` dispatch/reset work and one paid original-source certificate verification. Peak writable space is the maximum single active policy workspace plus scheduler/verifier counters; no policy snapshots are retained.

This is **PROVED/EXACT but restricted** and substantially precedented by LSPV-3 `ADAPTIVE_SELECTOR_GATE255`, Levin search, and algorithm-portfolio literature. The refinement here independently makes original-source SAT/UNSAT certification, restart scans, failed trials, certificate output, DELAY/COPY/RECOMP, and peak-space semantics explicit. It does **not** prove an all-input polynomial controller.

## Decisive remaining obstruction

The scheduler gives

`T_D(F) <= 4 k min_i T_i(F) + O(k log min_i T_i(F)) + V(F)`.

No verified theorem proves `min_i T_i(F) <= poly(|F|)` on every valid duplicate-free proper Döcker monotone 3-SAT-(2,2) original. Exact fallback only makes the minimum finite and may be exponential. If the policy family grows with the source, the factor `k(N)` (or program-description weight) is not free. Thus the best-policy-oracle objection is repaired for fixed `k`, but the all-input polynomial envelope, power-short `A -> Phi(A)`, and strict numerical same-machine FLMV transfer remain open.

## Controls

Producer/verifier: Y6 root 20 models; F9 SAT cube 2; adversarial six-pin F9 parity-only cube 0; F15 SAT cube 2; F15 UNSAT cube 0; five malformed rejects; forged SAT and incomplete UNSAT certificates rejected; 264 exact F9 S/U pair-mode checks. Binary/Gray logical XOR totals differ (4977/3585) and are offline only. A hostile policy pays 4096 zero-logical-delta DELAY steps, a full source COPY, and recomputation.

Independent live U198/V198 replay from source blob `1f959f...`: all 64 U198 boundary rows refuted (16 direct, 48 by 146 reverse-order module calls); V198 198-bit witness satisfies all 264 original clauses. This implementation used maximum-frequency variables and false-first branching, distinct from the archived sequential replay.

## Role consequences

- LSPV-1: seek the all-input polynomial envelope or prove an explicit family escaping every current certified terminal; scheduling itself is no longer a free-oracle gap for fixed `k`.
- LSPV-2: include recognizer/acquisition and certificate output in every candidate policy runtime.
- LSPV-3: reuse GATE255 as the predecessor; do not claim restart scheduling as new, and expose any growing portfolio factor.
- LSPV-4: a fixed finite scheduler does not supply power-short children or FLMV transfer.
- LSPV-5: next attack whether `min_i T_i(F)` is polynomial for the actual finite portfolio on connected growing-delta/intersecting-cycle families.

Artifacts: `research/main/2026-11-01_0848_MAIN_CERTIFIED-PORTFOLIO-DOVETAIL-REFEREE268.tex`, `experiments/arc/lspv5_268/`, and `results/raw/arc/2026-11-01_0848_LSPV5_CERTIFIED_PORTFOLIO_DOVETAIL_REFEREE268_*.json`.

`END_OF_HANDOFF::CERTIFIED-PORTFOLIO-DOVETAIL-REFEREE268::P_VS_NP_OPEN`
