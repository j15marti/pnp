# M22-AUX-WEIGHTED-COVER150 — Role-5 coverage and gap handoff

**Status:** PROVED/EXACT in the declared standalone uniform-sign block model. ARC-EDGE-90, DIRECT-POST, and P versus NP remain OPEN.

## Theorem

For three source ports, each with one already-used occurrence of the same sign, no standalone private-auxiliary completion using proper pure-sign ternary clauses can have existential port projection exactly `{000,111}` when the number of auxiliaries is `a=3` or `a=6`. The proof does not require clause uniqueness or prior extension of either constant port word. Literal sign-complementation gives the opposite uniform source orientation.

## Exact weighted certificates

Let `P_t,N_t` count selected positive/negative clauses containing `t` ports. Exact signed degrees give total positive port incidence 3, negative port incidence 6, and `2a` auxiliary incidences per sign.

- `a=3`: weight port-Hamming-one assignments with auxiliary weights 1 and 2 by 1 and 2. Rejection of all nonconstant ports demands weighted coverage 27. Clause capacity is bounded by twice the positive port incidence plus the negative auxiliary incidence: `2*3+6=12`.
- `a=6`: weight port-Hamming-one assignments with auxiliary weights 3 and 4 by 1 and 3. Required coverage is 195. Clause capacity is bounded by 12 times positive-port incidence, once positive-auxiliary incidence, and 11 times negative-auxiliary incidence: `12*3+12+11*12=180`.

Both inequalities are impossible. Therefore some weighted assignment satisfies every clause and has a nonconstant port word.

## Status upgrade

This replaces the solver-only conclusions for the uniform `a=3` and `a=6` cases with an elementary exact proof. The earlier exhaustive and MILP computations remain independent controls, not dependencies.

## Scope and rejection ledger

- **FALSIFIED/RETIRED exactly:** standalone uniform-sign three-port equality completion with `a=3` or `a=6` private auxiliaries.
- **OPEN:** `a>=9`; contextual or cross-variable balancing; shared clauses/auxiliaries; nonlocal semantic reductions.
- **Not DIRECT-POST:** the weighted deficit is a static constant-template obstruction. An adaptive SAT decider need not build this gadget, and the quantity is neither independently large with input length nor terminal-zero on complete machine states.
- **Not ARC:** a hypothetical fixed block would have linear output; the actual block fails before the first typed adapter level, so no two recursive ARC levels or simultaneous exponent successor exist.

## Peer reconciliation

- Role 1's fixed NAE local law fails PSD already on easy SAT targets; this is a restricted relaxation obstruction, not decision hardness.
- Role 2 proves fixed-depth Davis–Putnam elimination leaves `N^{1+o(1)}` ordinary children; no power shrink.
- Role 3's one-exposed paired-core erasure is exact, but pair-free eligible sources reduce to identity and children leave the target.
- Role 4's coverage threshold is a restricted dynamic-programming accounting result and does not supply FLMV bit resources or a universal edge.

## Coverage

Full latest reports read: Role 1 M22-NAE-PSD-CLIQUE150, Role 2 M22-DP-LOCALITY151, Role 3 M22-SINGLE-EXPOSURE-ERASURE108; Role 4's newly published DP-COVER106 code/raw output was read while its report path was not yet present. Primary literature checked: Döcker arXiv:1912.08032 and Darmann–Döcker arXiv:1908.04198. Inherited archive census was not rerun; Drive and older-revision pagination remain unexhausted.

## Next artifact

Do not enumerate `a=9` blindly. First solve the 14-orbit symmetric dual for a structural certificate or construct a genuinely contextual two-variable block whose ports and inverse addresses are public and whose output traffic/peak space are fully charged.
