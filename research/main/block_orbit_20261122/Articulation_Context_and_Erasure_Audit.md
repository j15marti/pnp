# Articulation context and erasure audit

22 November 2026, America/Los_Angeles. Internal review by contextual_erasure.

## Scope and result

The block-local hub theorem is sound for authenticated, unpinned triangle-bundle instances after a common parity normalization. It replaces a global branching factor by a sum of block branching factors. This note proves the exact boundary information required when pins are permitted and explains what can change under erasure. No unrestricted lower bound follows from these interface bounds.

Pinned recovery head: `5ec5f7417142d1a5d065fdc533cbba417822d004`.

The full original reports read were:

- `research/agents/charged-construction/PNP_Charged_construction_2026-11-22_102647_Triangle_Bundles.md`, blob `0d318b6a904d522a7b164830f87a0e1d1a5363d2`.
- `research/agents/charged-synthesis/PNP_Charged_synthesis_2026-11-22_112000_Hub_Degree_Covers.md`, blob `86ccd9a544d56442e91be8e3ba2d1b7ef3e9b646`.
- `research/agents/charged-bounds/PNP_Charged_bounds_2026-11-22_110600_Sparse_Event_Decoders.md`, blob `8db130fb931ad0856eb75dacbb7e983f86e55e2d`.

The inherited local `Minimum_Distinguishable_Information_Proof.md` and `Erasure_Work_Growth_Proof_Attempt.md` already prove source-observation activation, nested certificates, one-erasure hardness, and the one-global-decision/binary-search normal forms. Those are predecessors, not new results here.

### Additional original predecessor audit

The following complete originals were recovered at the same pinned head after a targeted duplicate search:

- `research/agents/lspv-2/2026-10-24_1302_LSPV-2_M22_BLOCK_CUT_FACTOR139.tex`, blob `557d9dfc59748d162105aa06168b0df47d0a0021`. It already proves polynomial overhead times a sum of block costs 3^(q_B), polynomiality from logarithmic maximum local defect despite linear total defect, exact articulation support messages with pins, paid discovery, and witness gluing. Its source is monotone exact-(2,2) CNF with a degree-two signed-factor backend. Neither the block sum principle nor the large-global/small-local distinction is new today.
- `research/agents/lspv-1/2026-10-29_1600_LSPV-1_ARC233_BLOCKCUT_DISCOVERY_TS_FRONTIER.tex`, blob `36a123af7549209fec410e97eb917e4610ca158f`. It already proves discoverable block-cut composition for typed 2CNF-plus-affine constraints, deletion heredity of its local-rank bound, explicit same-execution discovery/storage costs, and easy examples with unbounded global rank and primal width. Its source-deletion theorem concerns whole typed constraints, not arbitrary pin erasure in the present coloring source.
- `research/agents/tmr-2/2026-11-17_1850_TMR2_T5_TWO_TERMINAL_ORBIT073.md`, blob `bc3eb778edefd880ebce705cb1dd2d0558ca566a`. It already compresses a two-terminal tensor using global Z5 translation symmetry and proves exact original-label series convolution and parallel multiplication with a paid recognizer. Its ordered relation is R(x,y)=[(y-x) mod 5 in {1,3}], distinct from strict symmetric T5 and from the current positive Boolean exact-one triangle-bundle source.

Today's integration therefore specializes established composition and orbit techniques to the newly recovered three-choice degree-cover backend: the internal block hub parameter r_B, one-bit unpinned support under the actual C3 action, explicit pin-sensitive failure, conservative current-source tariff, prism/K4 controls, and the fixed-boundary support-addition statement during erasure. None is presented as a new general decomposition or symmetry principle. The older pin-closed factor/affine backends do not establish that the present degree-cover backend is closed under arbitrary external pins.

## 1. Normalized relation and the gluing proof

The quotient is a finite simple graph Q. Each vertex v has three triangle-coloring bijections L_v of a prescribed parity s_v. Each quotient edge u<v is a matching permutation p_uv and requires

\[
f_u(a)\ne f_v(p_{uv}(a))\quad(a=0,1,2).
\]

Use one globally consistent parity assignment s_v. Equivalently, independently normalized block solutions can first be globally transposed within their whole block to match that assignment. Then left composition by an even three-cycle preserves each list and every edge inequality, and acts transitively on each three-element L_v.

Let a be an articulation attaching an unpinned feasible piece P to the rest of the quotient. Given any target f_a in L_a, rotate a feasible coloring of P by the unique even color rotation taking its old value at a to f_a. Every internal constraint and prescribed parity remains satisfied. Thus P extends every possible boundary value.

Root the block-cut forest. Choose a feasible root-block coloring. For each child block, rotate a feasible coloring to agree at its one parent articulation, then recurse. A block may have several child articulations; those values are fixed by its chosen coloring and are matched independently by the descendant pieces. Distinct pieces share only their named articulation. Hence feasible blocks glue, and an infeasible block forbids any global coloring.

Consequently unpinned feasibility is exactly the AND of block feasibility. Local hub sets must be computed using degree inside the block, before global hub assignments or other pins are imposed. Calls to the existing hub solver retain its full acquisition and list-preservation costs.

### Prism-chain audit

Identify a chain of b triangular prisms at one vertex between successive prisms, using distinct attachment vertices within every internal prism. Each prism has six vertices, nine edges, and all degrees three. The quotient has q=5b+1 vertices and k=9b edges. Its b-1 articulation vertices have degree six, and every other vertex has degree three. Its blocks are exactly the original prisms. Thus global hub count is b-1 while each block has zero degree-at-least-four vertices.

This changes the applicable proved upper-bound parameter from 3^(b-1) to a sum of b constant block factors. It is not a lower bound on the older algorithm's actual runtime.

## 2. Exact support at one articulation

Allow a piece P to carry unary restrictions on its normalized three-state vertices. For a fixed attachment a define

\[
S_P(a)=\{c\in L_a: \text{the constraints of P, including its pins, have an extension with }a=c\}.
\]

If two pieces P and R share only a, and no hidden variables, then

\[
P\cup R\text{ is feasible}\iff S_P(a)\cap S_R(a)\ne\varnothing.
\]

Necessity restricts a global assignment to each side. For sufficiency, choose a common c, take the two extending assignments, and unite them. Every constraint is internal to one side and the sole shared value agrees.

### Universal context equivalence

For normalized identity-matching quotients with arbitrary unary pins, two pieces with supports S and T are interchangeable in every compatible one-articulation context if and only if S=T.

If S=T, the preceding intersection criterion proves equivalence. If c belongs to their symmetric difference, a context whose boundary support is exactly {c} distinguishes them. Such a context is realizable by two leaves adjacent to a, pinned to the other two colors. Therefore distinct supports must receive different source-free reusable interface labels.

All eight subsets of the three colors are realizable: for each color excluded from S, attach one leaf pinned to that color. Those leaves forbid exactly the excluded colors at a. An isolated a realizes the full set. Three leaves with all three pinned colors realize the empty set. Consequently three fixed bits are necessary and sufficient to encode an exact reusable support interface for this class.

This is an interface theorem. It does not require an unrestricted offline decision algorithm to construct such a source-free summary or retain three bits beyond its complete source. It also does not assert efficient discovery of the mask.

### Why a single bit works without pins

In the unpinned rotation-invariant class, S_P(a) is either empty or all of L_a. If one value extends, rotate its witness to obtain every value. All allowed unpinned external contexts have the same property. Thus the exact contextual quotient in this restricted context class has only two states, empty and nonempty, represented by a single feasibility bit.

The context family is part of the theorem. Adding pins changes which summaries are safe.

## 3. Small pinned falsifier to scalar block gluing

Take two identity-matching quotient triangles sharing a vertex v:

\[
\{v,a,b\},\qquad \{v,c,d\}.
\]

Pin a=1, b=2, c=0, d=2 in the normalized three-color coordinates. The first triangle is feasible and forces v=0. The second triangle is feasible and forces v=1. Each block returns SAT in isolation, but their union is UNSAT.

This has two biconnected blocks, five vertices, and six edges. It falsifies the extension of the one-bit gluing rule to arbitrary pinned residuals. The support masks {0} and {1} detect the incompatibility exactly.

Pins here are explicitly pins of normalized three-state variables. Applying this result to arbitrary pins on the original exact-one source requires a charged, proved translation of those source pins into the normal form; that translation is not assumed.

## 4. What value erasure can change

Fix a piece, its boundary B of k normalized variables, and a sequence of pin sets

\[
\rho_0\supseteq\rho_1\supseteq\cdots\supseteq\rho_t
\]

formed by erasing supplied values. Define the supported boundary relation

\[
R_j=\{\beta\in\prod_{v\in B}L_v:\exists\text{ internal extension satisfying P, }\rho_j,\beta\}.
\]

Then R_j is a subset of R_(j+1). Every old extending assignment still works after a pin is removed. Therefore each of the 3^k possible boundary tuples can enter the support at most once:

\[
\sum_j |R_{j+1}\setminus R_j|\le 3^k.
\]

For one fixed articulation there are at most three membership additions, regardless of the number of internal erased variables. The number of strict support changes is also at most three. If every residual at every stage retains full global even-rotation symmetry, the tuples lie in orbits of size three for k>=1; then at most 3^(k-1) orbit-membership additions are possible. Arbitrary color pins generally destroy this symmetry, so that smaller count cannot be used throughout a generic erasure chain.

These statements bound semantic changes at a fixed interface. They do not bound the work of finding when an addition happens, and they do not apply unchanged when the boundary itself grows or is replaced.

## 5. Constant boundary information can still be hard to acquire

Given an arbitrary connected graph G with identity matching constraints, attach a fresh boundary vertex a by a single edge to any vertex v of G. If G is three-colorable, the extended graph is colorable and global color rotation realizes every color at a. If G is not three-colorable, no extension exists. Hence

\[
S(a)=L_a\quad\text{iff G is three-colorable},
\qquad S(a)=\varnothing\quad\text{otherwise}.
\]

So computing even this one-bit unpinned interface subsumes arbitrary graph three-colorability. The block-local hub algorithm pays for that computation using the applicable block parameter; it cannot substitute the existence of a one-bit summary for its acquisition.

This is the integration point with the preceding safe-label theorem. A small answer-preserving representation is useful only together with a uniform acquisition bound. Constant semantic novelty along a bounded interface does not settle that computational bound.

## 6. Sources, checks, and exclusions

The gluing, support, monotonicity, and reduction arguments above are direct finite proofs. No new experiment or native parser/kernel run was performed in this subtask. The existing report's conditional source-recognition tariff remains conditional at its original scope.

Background primary source read: Darwiche and Marquis, *A Knowledge Compilation Map*, JAIR 17 (2002), 229-264, author PDF https://www.cril.univ-artois.fr/~marquis/darwiche-marquis-jair02.pdf. It separates succinctness, supported queries, and supported transformations; this note does not import a new lower bound from it.

Fresh queries covered the knowledge-compilation map and official organization-scoped SAT/CSP/formal-math repositories in anthropics, openai, xai-org, google, google-research, and google-deepmind. Search hits included official math artifact collections and Google OR-Tools, but no external repository theorem or code is imported. No formalization claim was promoted from a search result. The subtask did not independently reverify every corporate ownership link; the direct mathematical proofs do not rely on these hits.

Repository duplicate searches returned old context-sensitive source/continuation results as well as retired-workflow archive snippets. The archive snippets were excluded. No retired root proof tracker was opened or modified. No GitHub publication, issue message, automation, or role-owned manuscript edit was made by this subtask.

DISJ and deterministic-configuration safeguards: no unrestricted lower bound from support cardinality. Simultaneous cost: sum actual block computations with charged acquisition and shared storage. Relativization: no claimed nonrelativizing separation. Counting: Boolean feasibility only. Universal polynomial safe acquisition and arbitrary-solver recurrent necessity remain OPEN.
