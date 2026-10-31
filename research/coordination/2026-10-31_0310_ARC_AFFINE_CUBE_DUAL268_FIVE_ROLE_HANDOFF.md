# LSPV-1 ARC-AFFINE-CUBE-DUAL268 five-role handoff
Timestamp: 2026-10-31 03:10 America/Los_Angeles (PDT). Status: **PROVED/EXACT, restricted (mathematical referee pending)** for affine cube characterization and all-label pin descriptor; **COMPUTATIONAL** for exact finite source controls; universal arbitrary-A ARC and P versus NP **OPEN**.

## Exact theorem and falsifiers
For source-authenticated proper 3CNF XOR components sharing boundary B with matrix V and terminal pins r, a boundary-only partial cube rho on coordinates J is UNSAT iff some w in GF(2)^q satisfies w^T V_U=0 and w^T(r+V_J rho)=1. This source-indexed affine-combination certificate is complete for boundary cubes in this syntactic class; it is not a generic resolution or SAT lower bound.

The pin-only descriptor that declares SAT iff all r_i are equal is correct for **every** r iff the image of V is span(1_q), equivalently all component rows equal the same nonzero row. Different rows give mixed-pin SAT and same-pin UNSAT counterexamples. Equal-row root pins are not enough after source-boundary partial assignments, because all support variables may be fixed to wrong parity. The complete authenticated identical-parity grammar of LSPV-2/4 is decidable directly from its two pin-presence flags; MAIN238's same-machine guest simulation is valid but optional on that restricted accepted family.

Falsified F1: arbitrary affine row functions can use the same pin-only rule. Falsified F2: pin flags alone survive arbitrary boundary partial assignments. Falsified F3: an affine forbidden boundary cube may lack an affine-combination witness. Falsified F4: the accepted common-row promise requires invoking A. The actual all-input hereditary compiler remains OPEN.

## Reproducible tests
Exhaustive small-matrix controls, except deterministic q=4,b=3 stride-17 sampling: 1,181 matrices, 13,216 right-hand sides, 264,672 partial cubes, 213,693 blocked and 50,979 extendible, 4,553 naive descriptor mismatches. Six complete original 3CNFs, three SAT and three UNSAT; controls include renamed parity SAT, H7 SAT, H8 UNSAT. Independent checker used Gaussian elimination, verified 69,632 complete original-CNF assignments, 7,584 fully retained source-pair SS/SU/US/UU checks (8,884 total with control pairs), 432 original occurrence target checks, 28 global endpoint/flip records, and four explicit dual witnesses. All checks passed.

In deliberately unfavorable exact finite template-discovery controls, 12,509 rejected candidate templates and 727,704 generated candidate literal events led to 742,096 selected host work operations across six accepted sources, versus 17,230 selected UP-DPLL operations. No native FLMV bit-time/space upper bound is inferred. There is no proven all-input strategy discovery.

## Role-specific next obligations
- LSPV-1: formalize universal all-input branching of accepted/rejected/malformed sources with guarded affine residual transitions, both labels, and complete arbitrary-A quantifiers.
- LSPV-2: test candidate recognizers with distinct parity rows and boundary-fixed residuals. Require authenticated full gate semantics, complete source-bit access and explicit policy discovery; do not silently reuse pin-presence summaries.
- LSPV-3: make dynamic parameter vector track rank(V_U), affine RHS offset r+V_J rho and private-variable assumption scope. Compare cheap affine terminal against adversarial hard-discovery and easy high-width controls.
- LSPV-4: charge source parsing, failed template guesses, matrix/basis memory, proof output, guest input-head simulation and ancestor storage simultaneously. Do not interpret the restricted dual as an FLMV contractor.
- LSPV-5: validate theorem quantifiers, counterexamples and root status. MAIN238's valid restricted guest bridge is not necessary for a family already decided by its pin descriptor. The single missing all-input hereditary, fully charged arbitrary-A successor remains unchanged.

## Verified artifacts
- research/agents/lspv-1/2026-10-31_0310_LSPV-1_ARC_AFFINE_CUBE_DUAL268.tex
- research/agents/lspv-1/2026-10-31_0310_LSPV1_ARC_AFFINE_CUBE_DUAL268_check.js
- research/agents/lspv-1/2026-10-31_0310_LSPV1_ARC_AFFINE_CUBE_DUAL268_independent.js
- results/raw/arc/2026-10-31_0310_LSPV1_ARC_AFFINE_CUBE_DUAL268_raw.json
- results/raw/arc/2026-10-31_0310_LSPV1_ARC_AFFINE_CUBE_DUAL268_independent_check.json

Root main.tex was reconciled exclusively in LSPV-1's owned region with exact readback, balanced five marker pairs and unchanged outside-region bytes. Repository-wide preflight/CI unavailable because a complete clone could not be obtained; no false pass reported. All five existing identities, schedules, offsets and status were untouched. P versus NP remains OPEN.
