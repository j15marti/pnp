# Erasure interfaces and blockwise computation

**Research date:** 22 November 2026, America/Los_Angeles.  
**Named receiving dependency:** ERASURE-BLOCK-ACQUISITION1.  
**Status:** exact restricted implications and a constructive extension of the current triangle-bundle solver. The all-input acquisition and unrestricted recurrent-work premises remain OPEN. P versus NP is unresolved.

## 1. What this continuation accomplishes

The user asked to continue the proof and consult recent project conversations. Recovery covered the recent reverse-erasure, T_q/CM forbidden-region, instruction-length, WRAPPER, safe-merging, and charged-agent discussions. Actual definitions and primary reports were checked before combining claims.

The substantive result is an application of the project's earlier block-cut methods to the new degree-cover solver. Its exponential parameter becomes local to a biconnected block rather than counting all high-degree vertices across the source. The accompanying erasure theorem identifies exact support information at a fixed interface and proves that its semantic changes can be bounded across an entire removal sequence.

The conclusions are:

1. For a fixed boundary of k variables over a d-element domain, erasing internal pins gives a nested sequence of extension relations. At most d^k boundary tuples can be newly admitted over the whole sequence.
2. For one normalized triangle-bundle articulation, the exact pinned interface is a three-bit support mask. Without pins, the actual color symmetry reduces it to one feasibility bit.
3. For authenticated unpinned triangle-bundle sources, independently deciding articulation blocks changes the current branching bound from 3 to the power of the total global hub count to a sum of 3 to the power of the hub count inside each block.
4. The existence of a one-bit interface does not bound its acquisition cost. Acquiring it on an arbitrary piece already subsumes ordinary graph three-colorability.
5. Source discovery, local computation, retained global storage, and output are charged on one implementation. No FLMV contradiction or superpolynomial lower bound follows from this extension.

The combination is useful in either direction. It supplies a larger rigorously tractable class and a stronger bypass test for compulsory-work claims. It does not settle which direction the unrestricted problem takes.

## 2. Precedence and what is actually new here

The generic techniques are established and have substantial project precedence.

M22-BLOCK-CUT-FACTOR139 already proved a paid polynomial(N) times sum over blocks of 3^{q_B}, local logarithmic defect regimes, exact articulation support messages, pins, and witness gluing for its monotone exact-(2,2) source grammar [1]. ARC233 already provided discovered block-cut composition, charged shared workspace, source-deletion heredity, and examples with unbounded global parameters but easy local blocks in a typed affine/2CNF class [2]. T5-TWO-TERMINAL-ORBIT073 already used translation symmetry for compact boundary tensors and exact series/parallel composition in its distinct ordered Z5 binary relation [3].

Today's application uses the newly authenticated positive Boolean exact-one triangle-bundle source, its degree-cover backend, the particular local hub parameter r_B, and the current N^7 time tariff [4,5]. The prism/K4 controls, complete current ledger, fixed-boundary erasure bookkeeping, and new finite checks make that application concrete.

The old sources do not license an unproved change of language. The older ordered binary relation, strict symmetric ternary T5, proper 3-CNF, and the current exact-one source remain distinct. No historical novelty is claimed for articulation decomposition, support masks, orbit compression, or generic dynamic programming.

## 3. General qualitative erasure theorem

Let P be any fixed finite-domain constraint system. Let B be a fixed boundary of k variables, each with domain D of size d. All other variables are internal. Let

\[
\rho_0\supseteq\rho_1\supseteq\cdots\supseteq\rho_t
\]

be partial assignments obtained by erasing internal supplied values. No constraints are added or changed. Define

\[
R_j=\{\beta\in D^B:
\exists\text{ an internal assignment satisfying }P,\rho_j,\beta\}.
\tag{1}
\]

**Theorem 1.**

\[
R_j\subseteq R_{j+1},
\qquad
\sum_{j=0}^{t-1}|R_{j+1}\setminus R_j|
\le d^k-|R_0|
\le d^k.
\tag{2}
\]

**Proof.** Every extending assignment that satisfied the earlier pins also satisfies the smaller pin set. Thus the relations are nested. A boundary tuple can be added at most once. The differences in (2) are disjoint subsets of the complement of R_0, proving the sum bound. QED.

This theorem describes every stage simultaneously. It does not require examining all removal orders. For k=1 and d=3, at most three boundary values can newly become extendible, however many internal variables are erased. For a strict T5 piece the same domain-only statement gives an upper bound of five additions at a fixed one-variable boundary. No special T5 template property or exact necessity of five bits is inferred.

This is a semantic statement, not a time upper bound. Discovering the first newly supported value may involve a difficult decision problem. Nor does (2) bound the total number of semantic changes if the boundary is enlarged, replaced, or adaptively chosen. Such a representation change has its own acquisition and storage costs.

If the entire original formula is globally UNSAT, every restriction obtained by pinning variables is UNSAT. Removing pins cannot create a model absent from the original formula. This makes the answer profile constant, but does not make discovering that constant inexpensive. An all-UNSAT promise would trivialize decision and cannot be used to establish a lower bound for a solver required to handle both labels.

## 4. Exact interface information: composition, pins, and context

Suppose two pieces P and Q share exactly the boundary B, have disjoint internal variables, and have no hidden cross-piece constraints. Let R_P,R_Q be their extendible boundary relations. Then

\[
P\land Q\text{ is feasible}
\quad\Longleftrightarrow\quad
R_P\cap R_Q\ne\varnothing.
\tag{3}
\]

The forward direction restricts a global witness. For the reverse direction, choose a shared tuple and combine its two extending assignments. Their only common variables agree.

For a one-variable boundary a with three normalized values, write S_P(a) for this relation. A three-bit mask represents it exactly.

**Theorem 2, context equivalence.** In the identity-matching three-color subclass with arbitrary normalized unary pins, two pieces are interchangeable in every compatible one-articulation context if and only if their supports are equal.

**Proof.** Equal supports give identical intersections with every external support. If S differs from T, choose c in their symmetric difference. An external context forcing a=c distinguishes them. This context is realizable with two leaves adjacent to a, pinned to the other two colors. QED.

Every subset of the three colors is realizable: attach one leaf pinned to each excluded color. There are eight distinct supports, requiring three fixed bits for an exact source-free reusable interface. This is an interface lower bound, not a lower bound on all offline SAT algorithms or a claim that the source itself must be discarded.

A small pin counterexample is useful. Take two identity-matching triangles,

\[
(v,a,b),\qquad(v,c,d),
\]

and pin

\[
a=1,\ b=2,\qquad c=0,\ d=2.
\]

The first piece is feasible only with v=0. The second is feasible only with v=1. Each piece has a true SAT bit, but their union is UNSAT. Their support masks, {0} and {1}, detect the conflict.

These pins are on normalized three-state quotient variables. Arbitrary pins on Boolean names in the compiled exact-one source require a separately proved translation into this normal form. The scalar block algorithm below does not claim such arbitrary-pin closure.

## 5. Actual triangle-bundle source and complete input length

Fix the existing source encoding and one deterministic total Boolean decider before choosing inputs. The source language is positive Boolean exact-one triples. It is not strict symmetric T5.

An admitted source encodes a finite simple quotient graph Q with q vertices and k edges. Every quotient vertex expands to a triangle of three places. Every quotient edge u<v carries a perfect matching p_uv in S3. A triangle coloring is a bijection f_v from its places to three colors, and the edge requires

\[
f_u(a)\ne f_v(p_{uv}(a))
\qquad(a=0,1,2).
\tag{4}
\]

The existing graph-star compiler has graph size h=3q and e=3q+3k. Its two root rows for each i=0,...,2h-1 are

\[
(3i,3i+1,3i+2),\qquad
(3i+2,3((i+1)\bmod2h),6h+i).
\]

For graph edge x<y in sorted slot j it adds

\[
(6x+c,6y+c,8h+3j+c),\qquad c=0,1,2.
\]

The source feasibility correspondence and named-image recognition are the inherited Construction results, not a newly claimed parsimonious counting reduction [4]. The direct source has

\[
n=33q+9k,\qquad m=21q+9k.
\]

Its unary-name-count and fixed-width identifier encoding has

\[
w=\lceil\log_2(n+1)\rceil,\qquad
N=n+2+2\lfloor\log_2(m+1)\rfloor+3mw.
\tag{5}
\]

Source parsing, failed recognition attempts, row and field comparisons, missing-edge verification, quotient recovery, and any relocation are paid. A valid source outside the recognized image receives the existing exhaustive fallback. Correctness is therefore not confined to a promise that every input has the desired structure.

The symbolic native implementation tariff is inherited from its explicit source-recognition specification. The new Python audit operates on recovered quotient objects; it is not a native bit-parser or physical-tape validation.

## 6. The symmetry that makes one bit sufficient

A derangement of three colors is an even permutation. Equation (4) therefore forces

\[
s_v=s_u\oplus\operatorname{sign}(p_{uv}),
\tag{6}
\]

where s_v is the parity of f_v. Inconsistent parity equations imply UNSAT. Otherwise fix one consistent parity assignment, giving each vertex the three-element list

\[
L_v=\{f\in S_3:\operatorname{sign}(f)=s_v\}.
\]

For fixed f_u, precisely one f_v in L_v is forbidden, namely f_u p_uv^{-1}. Each edge is consequently a correspondence matching between three choices.

Let R=(0\,1\,2) act on color names. The simultaneous transformation

\[
f_v\longmapsto R^j f_v
\tag{7}
\]

preserves (4) and all chosen parities. It acts transitively on L_v because any two permutations of the same parity differ by one of I,R,R^2.

**Lemma 3.** An unpinned feasible piece attached at one vertex a extends every prescribed value in L_a. An infeasible piece extends none.

**Proof.** Take a feasible coloring. Apply the unique even rotation sending its value at a to the prescribed value. Equation (7) preserves the entire piece. QED.

Its exact one-articulation support is therefore either the full domain or empty. One feasibility bit is an exact reusable interface on this unpinned source class. This bit is still not free to compute.

Arbitrary correspondence covers need not have the symmetry (7). For example, a K4 cover with five identity conflict matchings and a transposition on the sixth can have a proper two-value support at an attachment. The theorem uses the actual triangle relation, not just the number of states.

For k boundary variables under a retained common rotation symmetry, simultaneous rotation has orbits of size three. A full orbit table has 3^{k-1} positions when k>=1. Arbitrary internal pins generally destroy this symmetry; a generic erasure sequence only receives the d^k bound of Theorem 1.

## 7. The block-local hub algorithm

Compute the block-cut forest of the original quotient before pinning any hubs. Bridges count as blocks and isolated vertices are handled directly. For each nontrivial block B define

\[
r_B=|\{v\in V(B):\deg_B(v)\ge4\}|,
\qquad
A(Q)=1+\sum_B3^{r_B}.
\tag{8}
\]

Degrees are measured inside B.

**Theorem 4.** For the admitted unpinned sources,

\[
\operatorname{SAT}(Q)
=
\bigwedge_B\operatorname{SAT}(B).
\tag{9}
\]

Apply the existing hub routine to each block independently, using its local degrees.

**Proof of gluing.** A whole coloring restricts to each block. Conversely, root a block-cut tree and choose a feasible root-block coloring. A child block meets the already processed part at one articulation. Lemma 3 rotates a feasible child coloring to agree there. Its remaining vertices and edges are new to the processed part, so no further conflict is introduced. Continue through the tree. Several children at one articulation can be matched independently. Isolated vertices have available choices. QED.

Keep a common global parity assignment. If an implementation independently normalizes each block, a whole-block color transposition first aligns its parity convention; an even rotation then matches the attachment. The finite witness audit explicitly uses the appropriate whole-block color permutation.

### Local decision backend

Within a block, enumerate the at most 3^{r_B} choices for vertices of degree at least four. Reject an assignment that violates an edge between pinned hubs. Delete the hubs and remove forbidden choices from their neighbors.

For an unpinned vertex v with t_v pinned neighbors,

\[
|L'_v|\ge 3-t_v
\ge\deg_B(v)-t_v
=\deg_H(v).
\tag{10}
\]

The residual graph H has maximum degree at most three.

Bernshteyn, Kostochka, and Pron characterize connected graphs that fail degree correspondence colorability: in the simple-graph case, every block must be a clique or a cycle [6]. Thus a residual component with a different block is feasible for its actual cover under (10). This is a sufficient acceptance test; exceptional graph types are not automatically rejected.

For a component whose blocks are all cliques or cycles, use exact Boolean variable elimination. The cliques have at most four vertices. A leaf cycle has a nonattachment vertex with at most two remaining neighbors, and a leaf clique has a nonattachment simplicial vertex with at most three. Eliminating such a vertex creates a factor on at most three neighbors. Since domains have size at most three, each local factor update inspects at most 3^4 assignments, with polynomial bookkeeping. Empty lists and constant factors are retained. This decides the actual exceptional cover.

A successful hub assignment combines with the residual component witnesses; every global witness induces one enumerated hub assignment. This proves correctness of both labels. The backend is the existing HUB-DEGREE-COVER1 result applied locally [5].

## 8. Same-execution charged ledger

Authentication and decomposition happen once. Retain the original source, recovered quotient, matchings, block incidence data, and output state. Nontrivial blocks partition the k quotient edges, and their total vertex incidence is O(q+k). Process blocks sequentially and reuse the same workspace. There is no simultaneous storage of all hub assignments.

Use the conservative previous N-sized tariff for each local branch. Then

\[
T=O(A(Q)N^7),\qquad S=O(N^2),
\tag{11}
\]

\[
CM_{\mathrm{phys}}=O(A(Q)N^9),\qquad
CM_{\min}=O(A(Q)N^8).
\tag{12}
\]

The first cumulative bound sums the actual uniform physical span bound over the same execution. The second uses input-and-time replay: each configuration has a description of O(N+\log(T+2)) bits given the fixed algorithm. Since r_B<=q<=N and there are at most N blocks, log T=O(N). The description bound is not an efficiently computed compression routine.

On admitted-source runs, the bounds include failed internal recognition attempts, block discovery, exact comparisons, branch rejection, list rebuilding, child representation, state retention, head travel, and terminated output, according to the inherited symbolic source tariff. Valid nonimages retain the separately stated exhaustive fallback. The Python runtime is not used as evidence for these exponents.

Let r_*=max_B r_B. If r_*<=c log_3(N+2) for fixed c, then A(Q)=O(N^{c+1}), so time O(N^{8+c}) and the corresponding cumulative costs are polynomial. No universal bound on r_* is established.

### Parent residence cannot be dropped

If calls have private local costs C_i and take times T_i, while M_0 bits of source, decomposition, and other parent data remain resident, a partitioned workspace ledger gives

\[
C_{\mathrm{total}}
\le C_{\mathrm{outside}}
+\sum_i C_i
+M_0\sum_iT_i.
\tag{13}
\]

This is an upper bound under an actual storage partition, not a product of unrelated worst cases. For a physical span measure, the occupied interval and any gaps must additionally be charged; the direct O(N^2) bound in (11) handles this conservatively. For minimum-description CM, use replay directly rather than treating K as additive over storage components.

The recent CM-contraction discussion contains precisely the same parent-residence issue. Our conservative full-input ledger does not meet its low-auxiliary-memory contract, and no transfer to an FLMV-forbidden pair is claimed.

### Witnesses

After a successful hub assignment, pin a residual vertex to each of its at most three choices in turn, delete that vertex, and remove the conflicting choice at each neighbor. The invariant remains

\[
|L''_u|\ge |L'_u|-1_{uv\in E}
\ge\deg_H(u)-1_{uv\in E}
=\deg_{H-v}(u).
\]

The same residual decider applies. At most 3q calls recover a block witness. Align child-block witnesses at articulations, then use the inherited source extension. Conservative witness bounds gain one factor N over (11)-(12). No exact-counting consequence is inferred.

## 9. A family that separates the old and new parameters

Take b triangular-prism blocks in a chain, identifying successive blocks at distinct attachment vertices within each internal prism. Each prism has six vertices, nine edges, and degree three. Then

\[
q=5b+1,\quad k=9b,\quad
r_{\mathrm{global}}=b-1,\quad r_B=0\text{ for every block}.
\tag{14}
\]

All quotient degrees are three or six, so degree-at-most-two peeling cannot remove anything. The source dimensions are

\[
n=246b+33,\qquad m=186b+21,\qquad N=\Theta(b\log b).
\]

Global hub enumeration carries the factor 3^{b-1}. The new bound has A(Q)=b+1, hence polynomial time on this family.

For an equal-dimension balanced SAT/UNSAT pair, attach a terminal K4 block. Now

\[
q=5b+4,\ k=9b+6,\ r_{\mathrm{global}}=b,
\quad n=246b+186,\ m=186b+138.
\tag{15}
\]

Keep identity matchings on the prisms. Identity matchings on K4 make it UNSAT. Using the nontrivial three-cycle R on every oriented K4 edge makes that block feasible with f_v=identity throughout. Both edge-sign systems are balanced; all blocks still have r_B=0.

For the specific published global product-enumeration code, the UNSAT member visits its entire 3^b assignment loop. This is a code-specific observation, not a lower bound for all solvers. The new block routine may reject the terminal block immediately after source acquisition and decomposition.

At b=16, the equal-dimension pair has q=84, k=150, n=4122, m=3114, and N=125592 bits under (5). The global enumeration parameter is 3^16=43,046,721. There are 17 local blocks, each with no internal hub, and A(Q)=18. The audit checks the new decision and witnesses; it does not claim to have executed all 43 million old assignments.

### A new large-block control recovered during this run

The latest Accounting report gives a ring of d diamonds with d degree-four hubs, n=144d source names, and m=108d rows [12]. Its quotient is biconnected: deleting a terminal leaves a connected chain, and deleting a private diamond vertex leaves its other private vertex joining the two terminals. Thus its single block can have arbitrarily large r_B. Nevertheless, each diamond transmits a constant-size permutation, and feasibility is just whether the ordered product is the identity. Paid product accumulation is polynomial. A public normalized checkpoint containing only the d unknown symbols forces d first reads, but a different paid preprocessor can retain the product verdict and remove that suffix obligation.

This is an inherited source-backed control, not a new audit performed here. It shows that large local hub count alone is not a hardness certificate. The next difficult-block proposal must also survive algebraic product recognition and other compact representations.

## 10. What this says about minimum information and WRAPPER merging

The support relation is exactly the information relevant to composition through a declared boundary. However, its size and acquisition cost are different questions.

Given any connected graph G with identity matchings, attach a fresh boundary vertex a to one vertex of G by a bridge. If G is three-colorable, the bridge extends and global rotations realize every value at a. If G is not three-colorable, no extension exists. Therefore

\[
S(a)=
\begin{cases}
L_a,&G\text{ is three-colorable},\\
\varnothing,&G\text{ is not three-colorable}.
\end{cases}
\tag{16}
\]

Even the one-bit unpinned interface can encode an arbitrary three-colorability decision. Its existence is not a general fast algorithm.

This connects to the previous safe-label theorem [7]. That theorem requires both decision-safe merging and polynomial acquisition/UNSAT frontier bounds. The present algorithm supplies a concrete cheap summary on a larger structural class. It does not construct a universally cheap label for an arbitrary biconnected block.

WRAPPER-style sharing remains legitimate: once a support or verdict is computed, later compatible uses can reuse it. If the interface changes, existing summaries may require refinement. The pinned two-triangle example identifies a real loss of compatibility information; it does not establish that every unrestricted solver must discover that information by the displayed method.

Nor does a large full boundary table force materialization. Symbolic factors, circuits, symmetry, and cached answers remain allowed. A lower bound would have to constrain acquisition/evaluation under all relevant alternative representations.

## 11. What the other recent chats contribute

### Entropy and erased analytical history

The current ACCUMULATED-DECODER-HISTORY1 report already proves the history correction [8]. Let V_j=(B_0,Pi_1,...,Pi_(j-1)), let B_j=f_j(V_j), and assume an actual decoder U_j=d_j(B_j,Pi_j), with source-dependent event identities and metadata accounted as in that report. Earlier obligations are therefore recoverable from the accumulated records. Then

\[
\sum_j H(U_j\mid B_j)
=
\sum_j H(U_j\mid V_j)
+\sum_j I(U_j;V_j\mid B_j)
\le H(X\mid B_0)+\sum_j\delta_j.
\tag{17}
\]

For repeated copies of one decision D, H(X|B_0) can be replaced by H(D|B_0)<=1. The added delta terms measure information omitted from the analytical decoder. They do not prove physical erasure or compulsory recomputation. This is recovered prior work, not a new theorem here.

The newer sparse-event example also shows that two identical payloads can carry different information through their selected addresses or times [9]. Metadata and a replayable event-selection rule must be charged before using a decoder bound.

### CM forbidden regions and contraction

The recent T_q/CM chats provide fixed low-resource exclusions and a conditional solver-transformation route. The contraction note's actual recurrence includes retained parent memory:

\[
t'=\max\{1.1,\ 0.825+t/4\},
\]

\[
\gamma'=\max\{1.35,\ 0.825+\gamma/4,\ 1.075+t/4\}.
\tag{18}
\]

Its favorable fixed point is not an implemented universal transformation. The source-dependent decomposition, generation costs, and hereditary applicability to every resulting solver remain open.

The newer additional-regions note raises its standalone auxiliary-CM exclusion to gamma<1.24 using the corrected Williams table pair (1.24,0.666), with strict slack and its model-preserving reduction assumptions [10,11]. This transfer requires small initial auxiliary workspace, at most polylogarithmic growth in usable workspace per charged step, and at least one charged bit per elapsed step. These premises give T<=C_aux and S_max<=soft-O(1+sqrt(C_aux)). This is auxiliary writable memory, not the physical input-inclusive CM convention in (12). The old claimed universal product exponent near 1.801 is withdrawn in the corrected manuscript; it is not used here.

Our block improvement neither proves that every input has a cheap decomposition nor reaches a forbidden simultaneous resource pair. Its scalar gluing has no assignment enumeration across articulations, but it still pays local solving and retained global storage.

### Instruction length

For a fixed total algorithm A, a self-delimited N-bit input plus a constant simulator describes the complete halting trace:

\[
K(\operatorname{trace}_A(F)\mid A)
\le N+2\log_2N+O(1).
\tag{19}
\]

The decompressor may run as long as A. Static program length is constant in N, and dynamic instruction count is a time measure. Thus small trace descriptions and long execution can coexist. Summed per-configuration cost is distinct from the description length of the whole trace.

These guards prevent information from being artificially renewed as values are erased. They leave acquisition, transport, and computation as the actual unresolved costs.

## 12. New executed evidence

A standalone Python 3 audit adapts the pinned hub routine and adds independent compound-instance comparisons, block witness gluing, exact support tests, and erasure checks. Seed: 2026112201. It ran once under a 30-second cap and completed successfully in approximately 0.43 seconds.

Observed results:

| Check | Count |
|---|---:|
| Compound quotient comparisons with an independent six-permutation oracle | 288 |
| Labels among those cases | 215 SAT, 73 UNSAT |
| Additional small prism-chain oracle comparisons | 6 |
| All permutation-edge/even-rotation identities | 648 |
| Uniform one-boundary projection checks | 450 |
| Exact normalized block-count factorization checks | 225 |
| Realized three-bit support masks | 8 |
| Ordered distinct-mask separating contexts | 56 |
| Erasure orders / steps | 24 / 96 |
| Witness residual-decision calls in the audit | 2,147 |

The 15 prism-family cases use b=1,2,4,8,16, each with no terminal, a SAT terminal, or an UNSAT terminal. Larger cases are checked by the new algorithm and directly verified witnesses; the independent raw oracle is confined to the stated small cases.

The optional count identity tested is only for normalized quotient colorings:

\[
Z_Q=3^{1-b}\prod_B Z_B
\]

for a connected quotient with b nontrivial blocks. Each articulation value has Z_B/3 local extensions by the free rotation action. This does not make the local counts cheap and does not imply a count identity for the compiled exact-one formula.

Audit source SHA256:
cddc11fabf7322283f08dc9a7006260b0bd580b312cd71508fcefa030d669cc0.

The new raw evidence does not validate the native source parser, a physical single-tape implementation, an unrestricted complexity claim, or a formal proof kernel. Previous 3,052-case hub tests were recovered as prior evidence and were not rerun.

## 13. Review, gates, recovery, and remaining task

One collaborator developed the block application. A second read the complete note and independently audited gluing, parity alignment, pin failures, witnesses, the families, and count scope. A third checked cross-chat CM/entropy connections and retained-parent accounting. The coordinator reviewed the original backend and ran the new audit. This is same-conversation internal review, not external peer review or formal verification.

The active repo instructions, ownership directive, six current handoffs, relevant originals, and the preceding safe-merging result were recovered. Initial main head was 5ec5f7417142d1a5d065fdc533cbba417822d004. There was no complete checkout; the repository preflight and native tape checks were not run. Retired proof trackers were not opened or edited.

The first 100 branch names were inventoried, without claiming complete pending-branch coverage. File handoffs and original pinned reports, not an assumption about all branches, supply the source state. The active coordination issue is 324.

Fresh primary queries concerned degree correspondence colorability and articulation/color symmetry. Bernshteyn-Kostochka-Pron Definitions 2-4 and Theorem 9 were read. Williams's corrected manuscript was opened for the inherited forbidden-region discussion. Repository duplicate search recovered [1-3], which are explicitly credited.

Fresh organization-scoped searches for biconnected coloring covered anthropics, openai, xai-org, google, google-research, and google-deepmind. The DeepMind query returned a rate-limit error and then no hits on one retry. OpenAI returned an unrelated percolation manuscript at 4eaee87548250b2682affda7d05d947c05554bae; it was not imported. Corporate GitHub profiles and Google's official organization policy were checked. No external code or formalization result is used.

| Gate | Status |
|---|---|
| Sharing / equality sanity | PASS in scope: block verdicts and supports are reused; no repeated source charge |
| Simultaneous time, space, CM | PASS symbolically under the inherited source tariff; one execution and retained source accounted |
| Deterministic configurations | PASS: replay used only for upper descriptive cost |
| Relativization / other barriers | No claimed separation or new barrier-crossing mechanism |
| Native encoded implementation validation | Not executed in this continuation |
| General polynomial acquisition | OPEN |
| Arbitrary-solver recurrent lower work | OPEN |

**Receiving task:** investigate one biconnected block with large local hub parameter, or a pin-aware support acquisition method whose cost remains controlled. Articulation interfaces have now been handled for the declared unpinned source class. A proposed lower bound must survive this bypass and the older affine/block-cut controls. A proposed positive extension must preserve exact support under every allowed context and charge its discovery. Neither branch may assume the desired hardness or an uncharged decision oracle.

## References and source pins

1. M22-BLOCK-CUT-FACTOR139. 24 October 2026. https://github.com/j15marti/pnp/blob/5ec5f7417142d1a5d065fdc533cbba417822d004/research/agents/lspv-2/2026-10-24_1302_LSPV-2_M22_BLOCK_CUT_FACTOR139.tex . Blob 557d9dfc59748d162105aa06168b0df47d0a0021.
2. ARC233-BLOCKCUT-DISCOVERY-TS-FRONTIER. 29 October 2026. https://github.com/j15marti/pnp/blob/5ec5f7417142d1a5d065fdc533cbba417822d004/research/agents/lspv-1/2026-10-29_1600_LSPV-1_ARC233_BLOCKCUT_DISCOVERY_TS_FRONTIER.tex . Blob 36a123af7549209fec410e97eb917e4610ca158f.
3. T5-TWO-TERMINAL-ORBIT073. 17 November 2026. https://github.com/j15marti/pnp/blob/5ec5f7417142d1a5d065fdc533cbba417822d004/research/agents/tmr-2/2026-11-17_1850_TMR2_T5_TWO_TERMINAL_ORBIT073.md . Blob bc3eb778edefd880ebce705cb1dd2d0558ca566a.
4. Triangle matchings and 2-degenerate quotients. 22 November 2026. https://github.com/j15marti/pnp/blob/5ec5f7417142d1a5d065fdc533cbba417822d004/research/agents/charged-construction/PNP_Charged_construction_2026-11-22_102647_Triangle_Bundles.md . Blob 0d318b6a904d522a7b164830f87a0e1d1a5363d2.
5. HUB-DEGREE-COVER1. 22 November 2026. https://github.com/j15marti/pnp/blob/5ec5f7417142d1a5d065fdc533cbba417822d004/research/agents/charged-synthesis/PNP_Charged_synthesis_2026-11-22_112000_Hub_Degree_Covers.md . Blob 86ccd9a544d56442e91be8e3ba2d1b7ef3e9b646. Core audit code blob 1fd99d6715d15bb8883bc9b839680512620b9a74.
6. A. Bernshteyn, A. Kostochka, S. Pron. On DP-coloring of graphs and multigraphs. arXiv:1609.00763v1, 2016. https://arxiv.org/pdf/1609.00763 .
7. What survives preprocessing: local obligations and safe merging. https://github.com/j15marti/pnp/blob/d33ab73654a83ecdcffc54380ec661220af3fca5/research/main/Postprocessing_Local_Obligations_and_Safe_Merging_2026-11-21.md .
8. ACCUMULATED-DECODER-HISTORY1. https://github.com/j15marti/pnp/blob/5ec5f7417142d1a5d065fdc533cbba417822d004/research/agents/charged-bounds/PNP_Charged_bounds_2026-11-22_090500_Accumulated_Decoder_History.md . Blob 03ec010cfab3935f1526ee6696a10a2151970e77.
9. Sparse event decoders. https://github.com/j15marti/pnp/blob/5ec5f7417142d1a5d065fdc533cbba417822d004/research/agents/charged-bounds/PNP_Charged_bounds_2026-11-22_110600_Sparse_Event_Decoders.md . Blob 8db130fb931ad0856eb75dacbb7e983f86e55e2d.
10. R. Williams. Alternation-Trading Proofs, Linear Programming, and Lower Bounds. Corrected author manuscript. https://people.csail.mit.edu/rrw/automated-lbs.pdf .
11. Cross-chat files inspected: PNP_CM_Contraction_Proof_Attempt_2026-11-22.md, SHA256 a6218cba2785fc82d6c79e5731b5d926e436babd4f19868b0ef0d77596017d58; Additional_T5_Tq_Forbidden_Regions_2026-11-22.md, SHA256 a713d9cdd827f41e3be99fbbaac160a2b1af8a31acfe18835a524cb15c3f9b43. Their universal transformation/reduction premises are not independently established here.
12. Which reads are compulsory on a diamond ring? 22 November 2026. https://github.com/j15marti/pnp/blob/9015e1a854941a2ee3e687ac56ae566ad50a6877/research/agents/charged-accounting/PNP_Charged_accounting_2026-11-22_113622_Diamond_Product_Reads.md . Blob 19a58b5b159bbe96ce86eae331eaa68b3b2c5e9c. Symbolic product proof and inherited finite results; not rerun in this continuation.

