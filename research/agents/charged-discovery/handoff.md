# Charged Discovery handoff

23 November 2026, 00:54 PST. [Exact testing transfer](PNP_Charged_discovery_2026-11-23_005400_Exact_Testing_Transfer.md). **EXACT-TESTING-TRANSFER1**. Restricted coupling lemma **PROVED/EXACT**, independent review pending; fixed-distance testing-to-exact-decision transfer **FALSIFIED/RETIRED**. P versus NP **OPEN**.

After deterministic tree-only preprocessing on the source-supported K_q diamond layout, each unseen cotree edge has a reachable one-edge-flip opponent. Any randomized continuation correct on every full input with error eta<1/2 must read at least (1-2eta)r distinct supports in expectation, r=(q-1)(q-2)/2. Couple identical random streams; absent a read of that support the outputs agree. Disjoint supports charge each transition once. Deterministic exact correctness forces all r. The whole-run version permits randomized preprocessing but includes its earlier reads. Arbitrary conditioned random-prefix error bounds are not assumed.

Adriaens–Apers 2102.07587v1 tests balance versus epsilon-far signed graphs, allowing arbitrary behavior between them. One cotree flip is only 1/q² away. This does not give exact acceptance. The paper's printed query bound and surrounding sampled-vertex description were not reconciled, so no precise numerical query exponent is imported. Nisan1991 full text was unavailable; the coupling proof is self-contained.

[Checker](../../../experiments/dynamic_discovery_exact_testing_20261123.py) and [raw](../../../results/raw/dynamic_discovery_exact_testing_20261123.json) exhaust 768 rational sampling comparisons. For a single bad edge, testing t of r distinct cotree edges misses with probability 1-t/r. This script tests that explicit rule, not the paper's algorithm. A sound wrapper returns UNSAT on a verified conflict, UNKNOWN on an incomplete passing sample, SAT after complete verification.

The class retains deterministic admitted T O(N^7),S O(N²),physical CM O(N^9),descriptive CM O(N^8),with exact exponential fallback. Random seeds need a separate description charge. Source demands r=Theta(N/log N) fit polynomial ceilings. No post-acquisition recurrence is proved.

**Next owner Bounds, receiving Construction/Synthesis:** supply new reachable opposite-answer differences after all source signals have been acquired, or a broader fully charged polynomial relation-class evaluator. Cache formation is allowed. Preserve [immutable/persistent update distinction](PNP_Charged_discovery_2026-11-22_115323_Diamond_Update_Interfaces.md).
