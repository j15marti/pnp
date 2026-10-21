# ROUND-ADAPTIVE-BATCHING60 HANDOFF

Timestamp: 2026-10-22 08:48 KST

**P versus NP OPEN; P versus RP OPEN.**

New restricted theorem: an explicit keyed parent source can answer queries exposed in `R` adaptive rounds, with `Q_r` queries fixed at the start of round `r`, using

`sum_r ceil(Q_r/B) <= Q/B+R`

parent passes. Charged time is

`G+O(N(Q/B+R) polylog N+Q polylog N)+T_output`,

and peak space is the current `B`-query block plus parser, generator state and current output.

Phase law: for `Q=N^alpha`, `B=N^beta`, `R=N^rho`, source time exponent is `1+max(alpha-beta,rho)`. At `alpha=.6`, `beta=.5`, child length exponent `.5`, the ARC candidate `(1.1,.5)` survives exactly for `rho<=.1`, conditional on all omitted costs fitting. Thus full nonadaptivity is not necessary; at most `N^.1` exposure rounds suffice. `rho=.11` already costs `N^1.11`; singleton rounds restore `N^1.6` in this architecture.

Still OPEN: a source-key compiler, `R<=N^(0.1+o(1))` exposure for genuine arbitrary-SAT ARC children, hereditary preservation, real child construction, query-generation cost/state and exact target-machine simulation. This is not the all-input contractor.

Finite audit: 544,787 assertions; 542,964 adaptive membership queries; 33,740,739 charged source-record visits; zero failures.

Next tests:

- :00 — build the best indexed KT evaluator for the batched target and compare with `p_k`.
- :12 — log all generalized-WRAPPER source/gate/timer channels and seek a direct deterministic bypass.
- :24 — instrument a genuine ARC recurrence for round count, keys, generator costs, child size and both SAT/UNSAT behavior.
- :36 — certify disjoint original-coin dependency cones or exhibit an overlap.
- :48 — prove the source-key compiler and bounded-round theorem, or falsify them with a concrete adaptive family.

Artifacts: `research/main/2026-10-22_0848_MAIN_ROUND_ADAPTIVE_BATCHING60.md`, `experiments/review/2026-10-22_round_adaptive_batching60_audit.py`, and `research/raw/ROUND_ADAPTIVE_BATCHING60_raw.json`.
