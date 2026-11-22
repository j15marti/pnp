# Articulation blocks replace global hub enumeration

Research date: 22 November 2026, America/Los_Angeles. Subagent mathematical note for the coordinator. No repository edits or new experiments were performed by this subagent.

Status: exact restricted mathematical implication, subject to independent review. Source acquisition and sole-tape costs inherit the explicitly pinned source-recognition specification. This is not a strict-T5 theorem, a polynomial algorithm for arbitrary SAT, or a new general coloring technique.

## Recovered source and predecessor

Read at repository head `5ec5f7417142d1a5d065fdc533cbba417822d004`:

1. `research/agents/charged-construction/PNP_Charged_construction_2026-11-22_102647_Triangle_Bundles.md`, blob `0d318b6a904d522a7b164830f87a0e1d1a5363d2`.
2. `research/agents/charged-synthesis/PNP_Charged_synthesis_2026-11-22_112000_Hub_Degree_Covers.md`, blob `86ccd9a544d56442e91be8e3ba2d1b7ef3e9b646`.
3. `experiments/dynamic_synthesis_hub_cover_20261122.py`, blob `1fd99d6715d15bb8883bc9b839680512620b9a74`.
4. `research/agents/charged-discovery/PNP_Charged_discovery_2026-11-22_084818_Two_Variable_Separators.md`, blob `790b0e7dee1a1b2f965fe702e248e2416b7a001c`.

The last source is an important limitation: a supplied star of pieces with two-variable interfaces can retain NP-complete root composition even when every leaf relation is the same binary NAND. It is not an articulation-block theorem. Older T5 two-terminal orbit reports also use symmetry compression, so historical novelty is not claimed here.

The source is a positive Boolean exact-one formula produced from a named triangle-bundle graph, with a complete polynomially checked recognition guard and exact fallback on nonimages. For a simple quotient Q with q vertices and k edges, each vertex becomes a triangle, and each quotient edge carries a perfect matching p_uv in S3. The direct source has n=33q+9k names and m=21q+9k triples. Its exact encoding is

\[
N=n+2+2\lfloor\log_2(m+1)\rfloor+3m\lceil\log_2(n+1)\rceil.
\]

The previous hub solver pins all quotient vertices of global degree at least four. With r such vertices it has symbolic sole-tape bounds T=O(3^r N^7), span O(N^2), physical CM O(3^r N^9), and descriptive CM O(3^r N^8). It is correct on every admitted quotient, but its bound is polynomial only on restricted parameter classes.

## Exact relation and the symmetry being used

A coloring of triangle v is a bijection f_v from its three places to three colors. The directed edge u<v with matching p_uv requires

\[
f_u(a)\ne f_v(p_{uv}(a))\qquad(a=0,1,2).
\]

The edge-sign equations are s_v=s_u XOR sign(p_uv). Inconsistency implies UNSAT. If they are consistent, fix one root sign per connected component and let L_v be the three bijections of sign s_v.

Let R=(0 1 2) act on color names. Simultaneous left composition f_v -> R^j f_v preserves every displayed inequality and preserves parity. For each v this C3 action is transitive on L_v: if f,g have the same parity, then g f^{-1} is one of I,R,R^2. This is a symmetry of the actual triangle relations, not a premise about arbitrary three-choice correspondence covers.

## Lemma 1: full support at an articulation

Let B be any quotient block with these full unpinned parity lists. If B is feasible, then for every vertex a of B and every g in L_a there is a feasible coloring of B with f_a=g.

Proof. Take any feasible f. There is a unique R^j with R^j f_a=g. Left-compose all choices in the block by this R^j. It preserves the constraints and produces the desired value at a. Conversely an infeasible block has empty support. Thus its projection at a is exactly L_a or the empty set. QED.

## Theorem 2: block-local hub algorithm

Compute the ordinary block-cut forest of Q, including bridges as blocks and treating isolated vertices separately. For each nontrivial block B let

\[
r_B=|\{v\in V(B):\deg_B(v)\ge4\}|.
\]

Then feasibility of the full unpinned normalized cover is the conjunction of feasibility of its blocks. Apply the existing hub algorithm separately to each block, using degrees inside that block, and stop if one block is infeasible.

Proof of composition. Necessity follows by restriction of a whole coloring. For sufficiency, root each block-cut tree. Choose a feasible coloring of its root block. A child block meets the previously colored part at exactly one articulation a. By Lemma 1, rotate a feasible child coloring to agree with the already chosen f_a. This introduces no other conflict because its other vertices and edges are disjoint from the already processed part. Continue through the finite tree. The same argument handles multiple children at one articulation. Isolated vertices have three available choices. QED.

This also works if each local hub routine chooses its own root sign: a global color transposition switches its root-sign convention, and a subsequent even color rotation matches the attachment choice. For implementation simplicity one can instead retain the globally fixed signs.

The hub theorem applies within each B: after pinning its vertices of degree at least four, every remaining vertex satisfies |L'_v| >= 3-t_v >= deg_B(v)-t_v. Residual connected covers with a block other than a clique or cycle are feasible by the degree-cover theorem. The actual exceptional covers are decided by the existing width-three Boolean elimination, including empty isolated lists and infeasible cycles. The argument never treats an exceptional graph type as automatically UNSAT.

### Exact imported result

Bernshteyn, Kostochka and Pron, *On DP-coloring of graphs and multigraphs*, arXiv:1609.00763v1, Definitions 2-4 and Theorem 9. For a connected simple graph, failure of degree correspondence colorability is equivalent to all blocks being cliques or cycles. Here the import is only the guaranteed colorability of a specific cover with lists at least the degrees when its graph has a different block. The primary PDF was opened directly at https://arxiv.org/pdf/1609.00763; Lemma 12 was also checked.

## Paid implementation and resource bounds

Authentication of the original exact-one source is performed once. Retain its original rows, the recovered quotient and matching data. Build the block-cut forest by standard explicit DFS, or by slower polynomial connectivity tests; every address and scan is charged. There are at most k nontrivial blocks. Their total edge count is k and their total vertex-occurrence count is O(q+k), so no exponential copies or duplicated source are needed.

Set

\[
A(Q)=1+\sum_B3^{r_B}.
\]

For each block reuse one workspace and the existing three-choice hub solver. Bound each branch by the previous full N-sized budget, which is conservative. The resulting same-implementation symbolic bounds are

\[
T=O(A(Q)N^7),\quad S=O(N^2),\quad
CM_{phys}=O(A(Q)N^9),\quad CM_{min}=O(A(Q)N^8).
\]

The descriptive bound uses a replay description from the complete input and the step counter. Since every r_B<=q<=N and the number of blocks is at most N, log T=O(N). No efficiently computed compressor is assumed.

If r_* = max_B r_B <= c log_3(N+2) for fixed c, then A(Q)=O(N^{c+1}) and this is a polynomial class. It is strictly broader as a structural parameter bound than requiring the total number of global degree-four vertices to be logarithmic. No universal bound on r_* is supplied.

The full algorithm remains a total correct source decider by retaining the earlier exhaustive fallback whenever source authentication fails. The quoted polynomial class concerns the admitted images. Native sole-tape timing is not claimed.

## Witness reconstruction without assuming a constructive theorem

For an accepted block, retain one successful hub assignment. Its residual cover has maximum degree three and |L_v|>=deg(v). To find a witness, choose any remaining vertex v, try a choice c in L_v, delete v, and delete the at-most-one conflicting choice c forbids at each neighbor. For every other vertex u,

\[
|L'_u|\ge |L_u|-1_{uv\in E}\ge \deg(u)-1_{uv\in E}=\deg_{H-v}(u).
\]

Thus the same polynomial residual decision routine applies to every trial. A feasible current cover has at least one trial that preserves feasibility. At most 3q trial calls recover a full assignment. One extra factor N in the conservative tariff suffices: witness time O(A(Q)N^8), physical CM O(A(Q)N^{10}), descriptive CM O(A(Q)N^9), with O(N^2) span. These bounds are intentionally loose.

Rotate each recovered child-block witness to match its parent articulation. The known graph-star extension then fills the exact-one private names, with every fill and final witness check charged polynomially. No model-counting algorithm is obtained from decision.

## Strict parameter improvement

Take b disjoint triangular-prism graphs, each with six vertices and nine edges. In each internal copy choose distinct attachment vertices and identify successive attachments to form a chain. Each prism is a biconnected cubic block and is three-colorable. The resulting quotient has

\[
q=5b+1,\quad k=9b,\quad r_{global}=b-1,\quad r_B=0\text{ for every block}.
\]

Every vertex has degree three or six, so degree-at-most-two peeling does nothing. With identity matchings the source is feasible. More generally every parity-consistent matching instance on these blocks is feasible by the degree-cover theorem. The direct source has n=246b+33, m=186b+21 and N=Theta(b log b). Global hub enumeration carries an exponential 3^{b-1} bound while the block algorithm has polynomial work.

For an equal-size balanced SAT/UNSAT pair, attach one terminal K4 block at another articulation. Then

\[
q=5b+4,\ k=9b+6,\ r_{global}=b,\
n=246b+186,\ m=186b+138,
\]

and still r_B=0 everywhere. Keep identity matchings on all prism edges. Identity matchings on the K4 give UNSAT. On the same K4, choose the nontrivial 3-cycle R as every oriented edge matching. The constant choice f_v=identity is compatible there, so that block and the whole source are SAT. Both versions have all-even edge signs and identical encoding dimensions.

For the current published global product enumerator, the UNSAT member reaches the end of all 3^b hub assignments. The block algorithm rejects its K4 independently. This is a comparison between explicit algorithms and parameters, not an unrestricted lower bound.

## Why pins and multiple boundary vertices change the statement

The scalar block summary is valid only because the actual unpinned relation has transitive color symmetry. Arbitrary unary pins can destroy it. A correct one-articulation summary is then a subset of three choices, represented by a three-bit mask. Two articulation choices require their joint relation, not separate unary masks.

Concrete pinned counterexample: three identity-matching triangle blocks share one articulation a. In block i pin one other vertex to choice i, for i=0,1,2. Each block is feasible and permits every choice at a except i. Their three supports have empty intersection. Keeping only each block's SAT bit would incorrectly accept.

Even unpinned arbitrary correspondence covers need not have the symmetry above. In a K4 cover, put identity conflict matchings on five edges and on the sixth edge uv put a transposition fixing color i. The other five edges force u and v to have the same choice; the special edge allows precisely the two choices different from i. Three such K4 blocks sharing u, for i=0,1,2, are individually feasible and jointly infeasible. These covers are not the normalized triangle-bundle covers admitted by the theorem.

If a fixed piece has a fixed one-vertex boundary and internal pins are erased monotonically, its true support mask only expands. It has at most three membership additions over the entire erasure sequence. This limits semantic novelty; it is not a bound on the cost of discovering each update. An adaptive change of boundary or decomposition requires new acquisition accounting.

## Optional count identity, narrowly scoped

Let Z_B count normalized three-choice assignments on each block, not assignments of the compiled exact-one formula. Transitive free C3 action gives exactly Z_B/3 assignments for each specified articulation choice. For a connected quotient with b nontrivial blocks,

\[
Z_Q=3^{1-b}\prod_B Z_B.
\]

This is an exact factorization if the block counts are available. It does not make those block counts polynomial-time computable. The earlier star compiler supplies a feasibility correspondence, not a proved parsimonious counting correspondence, so no exact-one count identity is inferred.

## Remaining dependency and falsifiers

The contribution is a sound block parameter and a paid constructive extension of the current hub algorithm. It gives no new post-cache compulsory work. A valid next candidate must address a biconnected block with a large local hard parameter, or compute its context-relevant relation cheaply. Identity matchings on arbitrary quotients still contain ordinary three-colorability.

Falsifiers: loss of actual color symmetry; unary pins treated as full lists; overlaps of more than one vertex treated as articulation gluing; polynomial block work summed as though all hub assignments were simultaneous; source-image or exact-counting scope silently widened. No such widening is used here.

The argument passes equality/sharing sanity and uses one same-execution ledger. It is an upper-bound construction, not a nonrelativizing separation. Configuration replay is used only for an upper descriptive-cost bound. Independent review and any new finite tests remain the coordinator's next actions.
