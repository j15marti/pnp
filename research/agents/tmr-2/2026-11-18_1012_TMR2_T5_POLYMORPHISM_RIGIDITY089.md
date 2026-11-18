# TMR-2/089: exact binary-polymorphism rigidity of the five-symbol beat CSP

**Date:** 2026-11-18, America/Los_Angeles. **Owner:** TMR-2 / PNP Information Necessity. **Target:** the exact directed tournament (T_5) with (R(a,b)iff(b-a)\bmod5\in\{1,3\}\). **Status:** finite exact proof certificate and algebraic deductions; not an algorithmic time lower bound. Independent external mathematical review OPEN; P versus NP OPEN.

## New theorem: all binary polymorphisms are shifted projections

**Theorem.** For every binary operation (f:\mathbb Z_5^2\to\mathbb Z_5) satisfying
[
R(a,c)\land R(b,d)\implies R(f(a,b),f(c,d)),
]
there is a (c\in\mathbb Z_5) such that either (f(a,b)=a+c) for all (a,b), or (f(a,b)=b+c) for all (a,b). There are **exactly ten** such operations.

**Finite-checkable proof.** The diagonal (g(x)=f(x,x)) is an endomorphism of (T_5). Since the template is a loopless tournament, (g) is injective and therefore an automorphism. The automorphisms are precisely the five rotations (x\mapsto x+c): the image of one vertex and the directed edge between its two outneighbors determine all images. Post-compose by (g^{-1}) to normalize (f(x,x)=x).

The product digraph (T_5^2) has 25 vertices and 100 arcs. Its polymorphism condition is exactly a graph homomorphism (T_5^2\to T_5). Starting from the five diagonal singleton constraints, exact arc consistency forces each off-diagonal domain to ({a,b}) at ((a,b)), after three propagation passes (60 candidate-label deletions). The *single* remaining choice (f(0,1)\in\{0,1}) has two branches. In each, two further AC passes force all 25 domains to singletons, yielding respectively the first and second projections. Checking all 100 arcs verifies both. Each branch removes 19 more candidate labels. No other normalized operation survives because AC deletions preserve every genuine homomorphism. Restoring the five target rotations proves the theorem. The full 25-variable computation uses **three AC passes and one binary branch**, not an enumeration of (5^{25}) operations. A separate C++ forward-propagation implementation independently counted exactly two idempotent completions (three DFS nodes).

This is a computationally checkable finite proof of a universal identity about the **fixed** (T_5) template, not a finite-sample estimate about large input graphs.

## Three additional checks of polymorphism structure

**No ternary majority polymorphism.** A majority term would force (f(4,3,3)=3), (f(4,3,4)=4), and (f(4,4,3)=4). In the 125-vertex, 1000-arc product graph (T_5^3), these three singleton conditions alone make binary arc consistency inconsistent. Every two of the three survive AC, although that does *not* certify pairwise satisfiability. This is a compact, fully reproducible local obstruction, not a claim to classify every ternary operation.

**No Maltsev polymorphism.** The componentwise arc
[
(0,0,2)\longrightarrow(1,3,3)
]
belongs to (T_5^3), but the Maltsev identities force the outputs (m(0,0,2)=2) and (m(1,3,3)=1), and (R(2,1)=0). This is a direct two-tuple contradiction.

**Dichotomy qualification.** Only projections as *binary idempotent* operations does not rule out Taylor/Siggers or higher-arity weak-near-unanimity polymorphisms. Thus this result is **not** an independent full algebraic-dichotomy certificate. The 1988 Bang-Jensen–Hell–MacGillivray semicomplete-target theorem already classifies this fixed target as NP-complete, because it contains more than one directed cycle. The general finite-domain dichotomy was subsequently proved by Bulatov and Zhuk. This research thread preserves that prior art and does not infer (P\ne NP).

## Exact 32-domain propagation maps

Define the outgoing mask (P_+(S)=\{b:\exists a\in S,R(a,b)\}) and incoming mask (P_-(S)=\{a:\exists b\in S,R(a,b)\}). Every one of the 32 subsets is accounted for; modulo cyclic translation there are exactly eight orbits. Representative sets are shown in the **0–4** encoding.

| Representative S | Orbit size | P_+(S) | P_-(S) |
|---|---:|---|---|
| {} | 1 | {} | {} |
| {0} | 5 | {1,3} | {2,4} |
| {0,1} | 5 | {1,2,3,4} | {0,2,3,4} |
| {0,2} | 5 | {0,1,3} | {1,2,4} |
| {0,1,2} | 5 | {0,1,2,3,4} | {0,1,2,3,4} |
| {0,1,3} | 5 | {1,2,3,4} | {0,2,3,4} |
| {0,1,2,3} | 5 | {0,1,2,3,4} | {0,1,2,3,4} |
| {0,1,2,3,4} | 1 | {0,1,2,3,4} | {0,1,2,3,4} |

The exact binary AC revisions on an original constraint (u\to v) are (S_u\leftarrow S_u\cap P_-(S_v)) and (S_v\leftarrow S_v\cap P_+(S_u)), with both repeated until stable. All 1024 ordered pairs of domain masks were tested against explicit existential enumeration in the full local auditor.

## Matrix structure and safeguard

For the five-cycle shift matrix (S), the template adjacency matrix is (A=S+S^3) with (det A=2). Its complex Fourier eigenvalues are
[
\lambda_j=\omega^j+\omega^{3j},\qquad \omega=e^{2\pi i/5},\qquad j=0,\ldots,4.
]
The matrix has rank five over (\mathbb C) and over every field of characteristic other than two, including (\mathbb F_5); over (\mathbb F_2) its rank is four. The ordinary fifth-root discrete Fourier matrix cannot diagonalize over (\mathbb F_5), since characteristic five collapses the fifth roots. **Matrix rank does not imply decision hardness, branching-program lower bounds, or necessary tensor-contraction work.**

## Reproducibility, charges and TMR-4 handoff

Published self-contained Python proof checker: `experiments/tmr/tmr2_t5_poly089_compact.py`; full executed local auditor: `/mnt/data/tmr2_t5_polymorphism089.py` (SHA256 `2663595af8dd32a2adce94537d86edf17edc24e98bd7424cee15d19fbb12dbf9`); exact raw local JSON: `/mnt/data/tmr2_t5_polymorphism089_raw.json` (SHA256 `8b895d4f523e0bae2121cc185846ac9e71fb3aab7e939eb6b9a4ee34d63c9a99`). No network, nonstandard libraries, unverified oracle, or source conversion were used by the scripts. The proof checker is source-checkable and directly charges power-graph arc construction, mask updates, AC sweeps, the only two residual branches, and verification. This is **not** a physical Turing-machine replay, and timings/peak memory are not used as lower bounds.

**Named invariant for TMR-4:** `D2-T5-DIAGONAL-POWER-AC-RIGIDITY089`. It records the exact 32-mask propagation semigroup, fixed-template automorphism normalization, the 25-vertex/100-arc product CSP, all permissible AC domain removals, the two surviving branches, exact counts of binary operations, and independent ternary identity obstructions. This is an algebraic *structural filter*, not an unbounded resource obstruction. All original cheap decision methods and source-aware replacements remain permitted. The next useful algebraic question is a fully independently checkable no-Siggers/weak-near-unanimity witness or a concise clone-theoretic proof, although the fixed-target NP-completeness is already sourced. The principal lower-bound objective remains a growing, noncompiled, mixed YES/NO family surviving source-aware contraction and short certificates.

**External references:** Bang-Jensen, Hell and MacGillivray, *SIAM J. Discrete Math.* 1(3), 1988, DOI 10.1137/0401029. Zhuk, *A Proof of the CSP Dichotomy Conjecture* (2017), arXiv:1704.01914. All results here concern **fixed-template** finite-domain CSP polymorphisms. External mathematical review, full manuscript LaTeX compilation, repository-native preflight and physical TM replay remain OPEN. **P versus NP remains OPEN.**
