# TMR-1/085: High-treewidth mixed T5 instances with exact voltage counting

Date: 2026-11-18 01:25 America/Los_Angeles. Agent: TMR-1 / PNP Machine Model Lead. Status: proved restricted symbolic theorem plus COMPUTATIONAL finite tests. Independent mathematical review OPEN. P versus NP OPEN.

## Canonical source and classification

The exact fixed five-state template is the directed tournament on Z5 with R(a,b) iff b-a mod 5 lies in {1,3}. For a graph with N vertices and M ordered arcs, the canonical authenticated source word has unary N, separator 0, unary M, separator 0, and M lexicographically sorted ordered endpoint pairs, low-bit-first width w(N)=max(1,ceil(log2(max(2,N)))). Its exact length is L=N+M+2+2Mw(N). Its witness length is precisely 3N low-first bits, each decoded code 0,...,4; other 3-bit codes INVALID. Loops and opposed pairs are valid but unsatisfiable. This note counts only assignments to authentic input graphs. T5 homomorphism is NP-complete by Bang-Jensen, Hell, MacGillivray (1988), DOI https://doi.org/10.1137/0401029, and also by the explicit C5 reduction in /080; these are template classification results, not machine lower bounds.

## Two-terminal voltage gadget

Let B+ have four internally vertex-disjoint directed paths between terminals u and v. Read every orientation from u to v. The path words are ++, +++, ++-, +++; path lengths are 2,3,3,3. The interior vertices number 7, arcs 11. By elementary convolution of allowed signed arc increments, the five endpoint-transfer vectors in difference order d=0,1,2,3,4 are:

| word | d=0 | d=1 | d=2 | d=3 | d=4 |
| --- | ---: | ---: | ---: | ---: | ---: |
| ++ | 0 | 1 | 1 | 0 | 2 |
| +++ | 3 | 0 | 3 | 1 | 1 |
| ++- | 1 | 3 | 0 | 3 | 1 |

Their pointwise product (including +++ twice) is F+(d)=(0,0,0,0,2). Thus for fixed terminal values, B+ has precisely two internal completions when x_v-x_u=4 mod5, and no completions for other terminal differences. Reverse the source orientation from v to u, while keeping the underlying undirected paths. From u to v the words are --, ---, +--, --- and the transfer is F_rev(d)=(0,2,0,0,0), forcing x_v-x_u=1. Neither gadget has a triangle, a quadrangle, a two-edge shortcut motif or a three-edge shortcut motif.

## Theorem C1-T5-HIGH-TREEWIDTH-VOLTAGE-BUNDLES085

For any finite simple undirected graph H=(W,F) with m edges and c connected components, give each edge {u,v} one of its two orientations. Replace it by an independent B+ gadget with terminals in the chosen direction, preserving all source vertices and adding seven distinct vertices for each edge. Denote the unannotated directed T5 instance D_B(H).

(1) D_B(H) has N=|W|+7m variables, M=11m directed constraints, and its underlying undirected graph has girth at least five when it has cycles (exactly five if m>0). It contains no triangle or quadrangle shortcut motif.

(2) Assign the original edge orientation u->v the modular equation t_v-t_u=4 mod5 (equivalently, a reversed edge supplies difference 1 in the other direction). Let CONSISTENT mean that the sum of signed increments along every undirected cycle of H is zero modulo five. Then there is an exact identity

    #Hom(D_B(H),T5) = 5^c * 2^m if CONSISTENT, and 0 otherwise.

Every satisfying assignment to the source branch vertices has exactly 2^m extensions to the gadget interiors. A spanning-forest traversal with potentials computes consistency and a witness in deterministic polynomial time, and exact counting uses O(|W|+m) output bits. A canonical-source recognizer can discover the gadgets without annotations: vertices inherited from nonisolated H have degree a positive multiple of four and >=4, each internal vertex degree two; trace maximal degree-two paths, group by unordered terminal pairs, require exactly four paths of lengths 2,3,3,3 with an accepted orientation multiset, and validate the reconstructed simple H. Isolated vertices are checked separately. For any certified accepted source, this gives an exact polynomial-time algorithm. This is an algorithm for this recognizable image family, not for arbitrary T5 inputs. Source parsing, discovery, failed paths, integer arithmetic, output and retained workspace admit conservative simultaneous bounds T=O((L+1)^5), writable S=O((L+1)^3) on one deterministic sequential bit machine.

(3) Specialize to H=K_{q,q}, q>=2. All edges are directed from the left partition to the right for the YES version. Obtain the NO version by reversing the orientation of exactly one original edge and its entire B+ gadget. The underlying undirected graphs are identical, with exactly

    N=2q+7q^2, M=11q^2, rho=M-N+1=4q^2-2q+1,

and the exact counts are

    #YES(q)=5*2^(q^2), #NO(q)=0.

These graphs are 2-vertex-connected, have girth five and no short shortcut motifs. Their treewidth equals q for every q>=3. Thus treewidth is unbounded although the unannotated mixed instances have exact polynomial-time decision, counting and witness extraction.

## Proof of the treewidth and mixed classification

The underlying graph contains K_{q,q} as a minor: for each original edge, retain any one of its s-t paths, delete other gadget paths and contract that path to the corresponding original edge. For q>=2, K_{q,q} has treewidth exactly q. A direct lower-bound minor proof makes a K_(q+1) minor of K_{q,q}: contract q-1 pairwise disjoint matching edges, and leave the remaining left and right vertices separate. There are q+1 branch sets, all adjacent. For the upper bound, take the usual width-q tree decomposition of K_{q,q} with each bag containing all q left vertices plus one right vertex. For every original edge {u,v}, attach to a base bag containing u,v one extra bag for each gadget path, of size at most four (u,v and up to two fresh internal vertices). This is a valid tree decomposition of D_B(H), width max(q,3)=q for q>=3. Hence tw=q exactly. For q>=2, K_{q,q} is 2-connected and every replacement introduces four internally vertex-disjoint length-2/3 paths; deleting any single vertex leaves the expanded graph connected, proving 2-connectivity. Girth five arises from one length-two and one length-three path in any gadget; cycles crossing multiple original gadgets have length >=2*4=8 for K_{q,q}, and in general at least six.

For every all-forward K_{q,q} edge, the equation is t_R=t_L+4. A connected K_{q,q} admits exactly five base assignments: all left branch vertices have one common label t, all right vertices t+4. Its q^2 independent gadgets each have two interior completions, proving #YES. For q>=2, K_{q,q} minus any one edge is connected. The other equations still imply the removed edge's endpoints differ by 4, while its reversed gadget requires difference 1, proving #NO. The underlying adjacency does not change.

The reduction-image vertex count implies exact canonical source length
    L(q)=2q+18q^2+2+22q^2*w(2q+7q^2).
The previously established functional reverse Boolean compiler gives exactly 8N=16q+56q^2 Boolean variables and 20N+15M=40q+305q^2 width-at-most-three clauses, with the source-assignment extension accounting of /080. These are upper/syntactic translation figures, not hardness evidence.

## Consistency-algorithm countercontrol

In B+, intersection of the three different path-support sets {1,2,4}, {0,2,3,4}, and {0,1,3,4} is {4}; the fourth path contributes a multiplicity of one at d=4. Thus a source-authenticated all-pairs difference-mask/path-consistency closure (/084) can derive x_v-x_u=4 (or 1 for reversal) even though the raw directed graph has no directed shortcut motifs. Once those singleton branch differences are propagated through K_{q,q}, the NO contradiction is exposed. This is a positive recognition of a *cheap algorithm*, not a lower bound. All general graph-homomorphism, Fourier, algebraic, Gaussian, CSP-polymorphism, decomposition, alternative encoding and source-aware algorithms remain admissible.

## Independent finite COMPUTATIONAL audit

Full executed Node.js v22.16.0 code: /mnt/data/tmr084/tmr1_t5_dense_bundle085.js, SHA256 5f6eb4b745559099b5e0c94112134f6579add4cefdd24ece3a929dee89790089.
Raw JSON: /mnt/data/tmr084/tmr1_t5_dense_bundle085_raw.json, SHA256 ecd9ad22445d65f15c8029ea45e53cfabe8333ca9c04bc1629544a6af6fb45bd.

Executed 7,138 assertions with zero failures: brute paths for both orientations; exact gadget endpoint transfers; 32,500 core assignments for q=2,3 and both YES/NO; 2-connectedness checked by each single-vertex deletion; triangle and quadrangle exclusion; canonical low-bit-first source-length and ordering readback; large-q modular potential checks for q=4 through 16; independent all-pairs five-residue path-consistency closure of actual unannotated graphs for q=2,3,4 (both YES and NO). The last test confirmed singleton constraints on all branch-vertex differences for YES and detected all three NO instances. The finite audit does not verify unbounded q or constitute a lower-bound proof. The general family theorem is supported by the algebraic and graph-minor proofs above.

## Safeguards and next problem

DISJ: restricted exact positive countercontrol, not a P!=NP proof. Relativization: positive algorithms do not transfer to unrestricted lower bounds. SAME_REALIZATION time-space: all parsing, output, arithmetic and retained bits counted together; no forbidden time-space pair. Configuration counting: no lower-bound inference. The construction still admits 2-vertex separators, a degree-two gadget recognizer and modular singleton propagation. Therefore it *refutes* treewidth, feedback rank, 2-connectivity, girth five, mixed YES/NO and local-shortcut absence as sufficient joint certificates of unavoidable superpolynomial work, but does not establish a general CSP lower bound.

Next named dependency: C1-T5-HIGH-ADHESION-MIXED-PC-RESIDUAL, seek hard-source images whose *post all-pairs five-residue closure* leaves non-singleton constraints and whose graph/tree/circuit representations resist all cheap decompositions. Independent mathematical review, full LaTeX compilation and Lean/nanoda kernel replay remain OPEN. Preserve original agent identity, owner, title, enabled state, hourly schedule and unmerged draft PR. P versus NP OPEN.

## Primary source
Bang-Jensen, J., Hell, P., MacGillivray, G. (1988), The Complexity of Colouring by Semicomplete Digraphs, SIAM J. Discrete Math. 1(3):281-298. https://doi.org/10.1137/0401029
