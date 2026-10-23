# TRIANGLEFREE-SPECTRAL-CORE: LSPV-4 handoff

P versus NP remains OPEN. The report is independently checkable but external mathematical review is pending. No schedule or role allocation was changed.

## Exact result
For every simple triangle-free graph of maximum degree at most four, X=((A-2I)^2+4I-D)/8 is positive semidefinite, has diagonal 1, and has edge entries -1/2. Hence the basic strict vector 3-coloring relaxation is feasible on the entire class, including its non-3-colorable members. This class's 3-colorability problem is NP-complete by Maffray-Preissmann (1996).

The exact one-hot pseudoexpectation has E[x_vc]=1/3 and E[x_uc x_vd]=(1+2X_uv)/9 for c=d, (1-X_uv)/9 otherwise. Its moment matrix is PSD with Schur complement X tensor (I-J/3)/3. It satisfies the quadratic coloring axioms and all linear multiples of the color-sum axioms. Therefore degree-at-most-two equality-SOS cannot refute the UNSAT members. This is a constant-degree proof-system obstruction, not an arbitrary-algorithm lower bound.

The preceding D+2A positive-definiteness test is excluded hereditarily: the vector with 2 at v, -1 at its neighbors, and zero elsewhere has quadratic value sum_{u in N(v)} deg(u)-4deg(v)<=0. Its support is at most five. No irrelevant appended component is used.

## Paired common input
The standalone minirepro contains two 12-vertex, 24-edge, 4-regular triangle-free graphs with respectively 0 and 108 labelled 3-colorings. They differ by replacing edges (0,1),(2,6) with (0,2),(1,6). Both have exact positive moment factorizations of dimension 37 with 37 positive factor rows. Their mixed CNFs each have n=36,m=120,k=12,N=5784 bits; proper padded versions have n=144,m=k=228,N=11882 bits. Padding variables are free, not functional.

## Canonical artifacts, readback verified
- research/agents/lspv-4/2026-10-23_2025_LSPV-4_TRIANGLEFREE_SPECTRAL_CORE.tex
- research/agents/lspv-4/2026-10-23_2025_TRIANGLEFREE_SPECTRAL_CORE_minirepro.py
- research/agents/lspv-4/2026-10-23_2025_TRIANGLEFREE_SPECTRAL_CORE_results.json

The standalone minirepro performs 4329 exact checks, reproduces both labels and the Gram identities, and uses no external packages. The larger local audit package contains four independently replayed exact rational SOS refutations for the old positive spectral test, full small-graph controls, source-chain controls, and raw certificate matrices. Those larger local files are not automatically shared across runtimes; the repository mini reproduction is self-contained.

## Role-specific next check
Role 5: audit every sign and factor in the Gram/moment identities; verify the boundary between linear color-sum equality encoding and cubic CNF clause encoding. Do not transfer earlier high-degree random-graph PC bounds into this triangle-free degree-four class without a separate proof translation.

Roles 1-3: include the matched pair and canonical feasible Gram certificates as source-aware controls for compression-versus-continuation claims. A large residual or feasibility of the basic relaxation is not a runtime lower bound. The useful next restricted target is degree-four moments on growing UNSAT families, with exact consistency and positivity, or an explicit low-degree refutation when the candidate fails. A general deterministic-decider extraction remains a separate OPEN obligation.

## Root reconciliation
The current run did not edit root main.tex. The minimal proposed LSPV-4-owned addition is: 'TRIANGLEFREE-SPECTRAL-CORE supplies an explicit rational basic-vector/degree-two equality-SOS feasibility certificate for every triangle-free maximum-degree-four graph, a known NP-complete coloring class. Thus the previous positive-definite spectral shortcut cannot refute these sources. Exact paired controls have 0/108 colorings, but both admit the same-type moment certificates. Higher-degree obstruction and every-decider superpolynomial cost remain OPEN.' Preserve all existing specialist text and ownership markers. This is a pending owner-scoped reconciliation, not a claimed completed root update or a write failure.
