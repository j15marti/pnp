# XYZ-RULES4: Generalized typed points and COMBINE escape

STATUS: COMPUTATIONAL + CANDIDATE. P versus NP remains OPEN.

## Generalized point coordinates

XYZ are retained but no longer assumed complete.

- X: immutable source identity/support token.
- Y: current semantic possibility set or value state.
- Z: live relation/constraint state.
- R: representation type.
- C: certificate/gate state.
- Q: explicit source-read/reacquisition footprint.
- D: causal dependency support.
- G: combiner/aggregation descriptor.
- E: escape-enabling predicate, to be added in the next refinement.

## Core finding

The proposed PRESERVE/CERTIFY/REACQUIRE trichotomy is not exhaustive.

An exact machine can compute a decision-sufficient summary while detailed relations are still available, discard those details, keep only the summary, and never later reread the source or retain a certificate. This is a fourth legal transition class:

COMBINE.

Finite trace audit produced one clean witness for each class:

- PRESERVE: full semantic state retained under representation change.
- CERTIFY: detail discarded but a model/proof certificate retained.
- REACQUIRE: detail discarded and source reread before final decision.
- COMBINE: detail aggregated into an exact decision summary, no retained proof and no later source reread.

This aligns with the existing SHRINKER/COMBINE interface in the research program: any shrinker must state an exact combiner and its soundness, scale, interface, construction, and charging.

## Count-potential hostile test

For m live Boolean obligations aggregated by fan-in-2 conjunction/disjunction:

- exact gate count is m-1;
- balanced depth is ceil(log2 m);
- final semantic summary is one bit;
- raw live-count potential falls by exactly one per binary gate.

Thus a potential based only on the number of live relations yields at most a linear aggregation lower bound in this model. It does not approach an unrestricted SAT lower bound.

Moreover, once any exact decision function has been computed, its extensional output is always one bit. Therefore semantic output length cannot itself force decision cost.

## Updated transition rule

A proposed generalized discharge rule must now allow at least:

PRESERVE, CERTIFY, REACQUIRE, or COMBINE.

The candidate accounting form becomes:

O_before <= O_after + C_certify + C_reacquire + C_combine.

This is only accounting syntax. No lower bound follows until C_combine is independently bounded for every legal same-model transition.

## Main obstruction

TC4[A_SAT] can currently be classified simply as COMBINE: the hypothetical SAT algorithm aggregates the source into one decision bit. Therefore adding COMBINE makes the transition taxonomy more complete but does not close the arbitrary-machine bridge.

The load-bearing problem becomes sharper:

Prove a model-matched theorem that every exact COMBINE operation capable of erasing a chosen source-grounded obligation either preserves a nontrivial residual obligation or pays a bounded local construction/acquisition cost that accumulates beyond polynomial.

Without such a theorem, COMBINE is the universal escape.

## Next target

Define a typed COMBINE interface with input support, output semantic type, continuation equivalence, fan-in, representation description, enabling certificate, source-read footprint, and exact cost. Test whether the same interface can express SCC, Horn closure, Gaussian elimination, separator DP, DPLL, INTERP, RECOMP, and arbitrary SAT A without smuggling the final answer in as a free combiner.

END_OF_VERIFIED_REPORT::XYZ-RULES4