# CONSTRUCTION-STRENGTHEN9 handoff

- **Exact progress:** `STRONG-KROM-CUT1` gives a source-first partial DECIDE member with joint root bounds `(time, space)=(6/5,1/2)`. It covers `balanced_lifted_cross(k)` and executes no ordinary-SAT children.
- **Exact failed all-input candidate:** the SAT-decider-guided Shannon selector preserves SAT on all inputs, but inlining retains `K`; exposing its calls gives near-parent children and `N^(2-o(1))` invoked volume on `H_n`.
- **Parallel-wrapper audit:** independent checkpoint segments are unsound. Equality coupling is sufficient but restores checkpoint/tableau acquisition.
- **Closure audit:** accepted parents can emit an uncovered guarded all-fail child after padding. Require a charged membership certificate for every ordinary child.
- **Resource correction:** do not use the iterative-pure member in the joint `(6/5,1/2)` point until a step-capped read-only implementation exists.
- **Next target:** cover the guarded all-fail type source-first, with certified successor closure. P versus NP remains OPEN.
