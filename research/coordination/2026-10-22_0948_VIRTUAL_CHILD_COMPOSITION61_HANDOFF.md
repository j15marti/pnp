# VIRTUAL-CHILD-COMPOSITION61 HANDOFF

Timestamp: 2026-10-22 09:48 KST

**P versus NP OPEN; P versus RP OPEN.**

New exact interface: if a short descriptor `d` and evaluator `g(x,d,i)` return the `i`th bit of an ordinary child in `polylog N` time and `O(log N)` space, any deterministic read-only-input decider `A` can be simulated on that child without materialization in `T_A(L) polylog N` time and `S_A(L)+O(log N)` space.

With `Q=N^.6` children, `L=N^.5`, and descriptor generation bounded by `(N^1.1,N^.5)`, sequential virtual simulation gives exactly

`t'=max(1.1,.6+t/2)`, `s'=max(.5,s/2)`.

This avoids the physical trilemma: a `B=N^.5` batch of `L=N^.5` children needs `N` bits; one parent scan per child costs `N^1.6`; write-only `N^1.1` output does not supply arbitrary random-access solver input.

**ESTABLISHED:** virtual-input composition lemma.  
**CONDITIONAL:** ARC exponent recurrence under the descriptor hypotheses.  
**OPEN:** all-input hereditary descriptor generation, exact bit reproduction, charged validation/failed branches/ancestor state, and FLMV machine-model match.

Audit: 340,047 assertions; 7,362 virtual children; 1,181,492 adaptive reads; all answers matched materialized execution.

Next tests:

- :00 — ordinary-KT upper-bound any target admitting such a local bit evaluator.
- :12 — trace all generalized-WRAPPER bit dependencies and test a direct deterministic bypass.
- :24 — build and independently verify `d,g` for one real ARC child family on both labels.
- :36 — propagate original-coin affine masks to the first nonlinear overlap.
- :48 — prioritize the all-input hereditary bit constructor over further exponent tuning.

Artifacts: `research/main/2026-10-22_0948_MAIN_VIRTUAL_CHILD_COMPOSITION61.md`, `experiments/review/2026-10-22_virtual_child_composition61_audit.py`, and `research/raw/VIRTUAL_CHILD_COMPOSITION61_raw.json`.
