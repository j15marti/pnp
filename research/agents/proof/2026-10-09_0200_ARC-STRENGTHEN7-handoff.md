# ARC-STRENGTHEN7 handoff

- PROVED/EXACT and independently red-teamed: `EXTREME-1` tests the two extreme assignments and at most three one-bit repairs from one falsified clause on each side. A source-pointer implementation is `N^(1+o(1))` time, `N^(o(1))` writable space, zero children, and never returns FALSE.
- PROVED/EXACT: prepending it strictly enlarges the corrected recursively covered promise while preserving the joint `(6/5,1/2)` promise point. The witness family `Psi_m` is in the report.
- CANDIDATE ONLY: singleton strong-Horn/dual-Horn component solving. The semantic scanner is sound, but the tested component map uses linear state. Empty residual clauses, duplicate clauses, shared component/Horn buffers, and width-four successor typing were added to the obligation list.
- COMPUTATIONAL: 41,448 exact-width-three formulas plus 17,902 mixed-width formulas, zero semantic mismatches; runtime 3.57s under a 25s alarm. Python memory is not a machine-space certificate.
- IMPORTANT REPAIR: do not reuse ARC6's old `A(U)=A(SAT)` fallback equality after adding `EXTREME-1` unless its hard embedding is re-shielded so every model is Hamming distance at least two from both extremes.
- OPEN: an all-input favorable controller or an implication from `SAT in P` that acquires one without paying the unknown exponent `K`. P versus NP remains OPEN.

Next target: build and charge a read-only component enumerator that completes within `N^(6/5+o(1))` time and `N^(1/2+o(1))` live state on a provably new strong-Horn/dual-Horn family, or build the near-extreme-resistant fallback shield.
