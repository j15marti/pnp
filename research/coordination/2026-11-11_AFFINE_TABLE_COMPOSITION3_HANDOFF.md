# AFFINE-TABLE-COMPOSITION3: factored compatibility and its exact scope

11 November 2026, 20:25 America/Los_Angeles. Existing roles, priorities and schedules are preserved. This additive continuation follows ATC2 commit `56eeba7c81589bc31bc1c7f5325625cb061c40ab`.

## Implemented and audited

Automatic graph discovery now finds separators of size at most two, fills only the graph attachment clique, and retains complete residual bags when a discovery budget expires. It validates forest structure, running intersection, full source scopes, and ownership. Exact boundary messages remain 2-CNF; general Horn mode restricts boundaries to one variable. Unknown child states are kept possible and cannot manufacture an UNSAT result. A SAT parent candidate selecting an unresolved child is downgraded to UNRESOLVED.

The local engines retain the prior general-rank closure-polynomial and polynomial-workspace seed strategies. A polynomial Gaussian terminal handles unit-clause/affine queries regardless of rank. The wrapper preserves this terminal before low-arity row normalization; independent testing caught and corrected the opposite order, which hid a pure affine input from the terminal. All returned witnesses are checked against the original mixed input and, for selectors, the original CNF.

The time bound is charged discovery/validation/ownership/reconstruction plus a sum over bags of at most four local exact queries. Each non-affine query costs polynomial(local input) times the binomial seed bound at its local affine rank. A fixed maximum local rank yields polynomial time even with growing global rank. Seed-mode workspace stays polynomial without a growing-rank time claim.

## Concrete evidence

The automatic one-anchor and two-anchor 200-triple inputs are SAT at cap 20 under both backends. Global affine rank is 200, maximum local rank 1, largest bags 4/5, and query counts 401/801. The prior 33-variable Mycielski UNSAT input remains refuted.

Independent audits: 1100 small graphs, 2200 decompositions, 1100 articulation comparisons, 28 cap/fallback controls; 580 small/capped solver cases, 4060 subtree-message checks, 11 invalid decompositions; 8 rank-1024 Gaussian cases; 696 wrapper cases and 9 CLI cases. Scripts, raw outcomes and exact hashes accompany the package. Counts are finite verification, not a universal complexity theorem.

## Stronger scoped obstruction

With three shared anchors, the original scope graph is three-connected. Every adhesion-at-most-two decomposition has a full bag; every other bag has at most two original vertices. All original disjoint ternary parity rows therefore belong to the full bag, forcing local rank m in every source-scope-preserving certificate of this class.

Choose parity targets with q=floor(m/2) ones maximizing Hamming distance h from the frozen 2-SAT base parity vector. Then h>=q>=1. The original Horn polynomial has 3^q 4^(m-q) keys; the translated 2-CNF polynomial has 3^h 4^(m-h). Successful seeds need at least q or h generators respectively. The cardinality-ordered routines exhaust all smaller seeds. These are rigorous limits of the specified backends. The family has an explicit easy SAT assignment, and other polynomial procedures can solve it.

## Corpus reconciliation and next target

Original ARC235 (blob 8c2f657e2b36edeb9e2a0210dcf7449d8524b689) already contains the pair-separator compiler, clique fill, binary-message theorem, source accounting, and a rank-one implementation. Original ARC236 (blob 721e2e993145c4ed7f784f23ce8e67129b291bb1) already supplies ternary exceptional-message hitting covers and restates ARC230's rank-one adhesion-three encoding of arbitrary 3-SAT. Both originals were retrieved; no novelty claim is made for those results.

The next target is semantic message recognition and fully charged handling of exceptional interfaces, using the already recorded ARC236 cover theorem where applicable. Increasing separator size alone is insufficient. Uniform coverage remains open. Preserve P1-01, P1-03, P1-04 and unrestricted P2 bridges as OPEN. Root main.tex remains with its authorized owners.

Report: `research/explorations/sat-composition/2026-11-11_AFFINE_TABLE_COMPOSITION3/factored_compatibility.tex`.

Code: `experiments/sat_composition/2026-11-11_factored_controller/`.
