# TMR-1/086: Binary cycle-space normal form and exact Gaussian-relaxation counterexample

Date: 2026-11-18 01:59 America/Los_Angeles. Owner: TMR-1 / PNP Machine Model Lead. Status: **PROVED exact source-model theorem; local COMPUTATIONAL certificate executed; independent mathematical review OPEN. P versus NP OPEN.** This is an additive model-to-model theorem, not a lower bound, not a novel discovery of finite-field cycle spaces, and not a claim that Fourier/voltage theory was invented here.

## Exact source and NP-completeness classification

The fixed template is the regular tournament T5 on the alphabet Z5 with directed relation R(u,v)=1 iff v-u mod 5 belongs to {1,3}. A canonical source for n vertices, m distinct lexicographically sorted ordered arcs, and w(n)=max(1,ceil(log2(max(2,n)))) endpoint bits has exactly L=n+m+2+2m w(n) bits: unary n, 0, unary m, 0, then m low-bit-first endpoint pairs. Invalid lengths, codewords, repetitions or noncanonical ordering are rejected; loops and opposite arcs are valid source inputs but UNSAT. A witness has exactly 3n bits with codes 0,...,4; codes 5,6,7 are INVALID.

Bang-Jensen, Hell, and MacGillivray, *The Complexity of Colouring by Semicomplete Digraphs*, SIAM J. Discrete Math. 1(3), 1988, 281–298, DOI https://doi.org/10.1137/0401029, classify this specific template as NP-complete because it has multiple directed cycles. The independent explicit C5-to-T5 parsimonious reduction was established and audited in TMR-1/080; the theorem below inherits this classification and does not reassert an unverified hardness premise.

## Theorem C1-T5-BINARY-CYCLE-EXACT086

Given any finite directed source G=(V,E), including isolated vertices, loops and opposed arcs, regard each **directed arc as a separate labelled edge** of an underlying undirected multigraph. Let n=|V|, m=|E|, c be its weak-component count (isolates included), and rho=m-n+c. Choose a spanning forest F deterministically, e.g., lexicographically by source arc ID with fixed DSU tie-breaking. For every nonforest arc e=(u,v), form the signed fundamental cycle row C_e in {-1,0,1}^m: +1 on the chord e, and on the unique tree path from v back to u put +1 for traversal along the arc, -1 against it. A self-loop gives a one-entry cycle row. Collect these rho rows into C in F5^(rho x m).

For an edge-bit vector b in {0,1}^m define d=1+2b in F5^m, where 1 is the all-one vector. The following are equivalent:

(1) G has a T5 homomorphism x:V->F5.

(2) There is b in {0,1}^m such that C(1+2b)=0 mod 5.

(3) There is b in {0,1}^m such that Cb=-3 C1 mod 5.

More precisely,
    #Hom(G,T5) = 5^c * #{b in {0,1}^m : C(1+2b)=0 in F5^rho}.
Every b satisfying the cycle equations determines exactly five choices of the label on each weak component, hence exactly 5^c T5 homomorphisms. From each homomorphism, b_e is uniquely 0 for difference 1 and 1 for difference 3. The map is a bijection after including one root label per component.

The rows are linearly independent over F5: each nonforest arc occupies its own chord column with coefficient +1, while all other rows have zero in that chord column. Hence rank_F5(C)=rho. The domain restriction b in {0,1}^m, *not* Gaussian rank deficiency or the difficulty of solving the unbounded linear system, carries the decision obstruction. This gives a direct, exact, model-preserving equivalence to the restricted **graphical binary-code intersection** problem. Its decision version is NP-complete even when its implicit graph comes from the bipartite triangle-free DAG reduction image of /080.

### Proof

Given a valid labeling x, each arc has d_e=x_v-x_u in {1,3}, giving a unique binary b_e with d_e=1+2b_e. On every fundamental cycle signed edge differences telescope to zero, so C d=0. Conversely, given binary b with C d=0, choose an arbitrary root label in F5 for each component. Traverse the spanning forest and set every child label to its parent label plus or minus d_e according to tree-edge direction. For a nonforest arc, the associated fundamental cycle equation ensures the induced difference equals d_e as well. Loops would require d_e=0 but d_e in {1,3}, so correctly yield no binary solution. Opposed directed arcs are treated as separate edges and their length-two fundamental cycle is also enforced. Consequently all arcs meet R and the root-label choices are independent. Multiplication by 3 is valid because 2^-1=3 in F5, proving (3). The chord identity block proves the rank claim. n=m=0 has c=rho=0 and exactly one empty assignment.

### Crucial Gaussian-relaxation counterexample

If we relax b_e in {0,1} to b_e in F5, **every instance becomes linearly feasible**: b_e=2 for all e gives d_e=1+2(2)=0 in F5, and C d=0. The fake solution corresponds to assigning every vertex the same color with forbidden zero edge differences. Gaussian elimination alone, or any argument using only the cycle-matrix rank, cannot decide the actual binary intersection.

A four-vertex **transitively oriented K4**, with arcs (0,1),(0,2),(0,3),(1,2),(1,3),(2,3), provides an explicit NO instance: all four vertices must map injectively to the loopless tournament, but the top of a transitive four-tournament dominates three vertices, while every vertex of T5 has outdegree only two. This source has n=4, m=6, c=1, rho=3 and exact count zero. Yet its relaxed linear system accepts b=2 times the all-ones vector. The example is DAG, so acyclicity of the input does not rescue the Gaussian relaxation.

### Source size and machine accounting

The graphical binary form can retain the original authenticated ordered-arc source word, so its **implicit** representation has length exactly L. Constructing and storing the forest and row supports needs polynomial time and space; writing the **dense** matrix explicitly can cost Theta(rho*m) field entries, and this output blowup must not be hidden. The number of Boolean variables is exactly m edge bits, the number of fundamental cycle congruences exactly rho, and the root choices exactly c independent five-way labels. The solution-count output has at most ceil(n log2 5)+1 bits; there is no automatic polynomial-time counting algorithm for arbitrary source graphs. A naive exact audit can enumerate all 2^m binary vectors with polynomial work per vector and polynomial peak storage. Any algorithmic reduction must charge authentication, forest construction, matrix materialization or implicit access, failed assignments, consistency checks, witness reconstruction, arithmetic and output simultaneously on the SAME_REALIZATION sequential bit model. This theorem makes no forbidden DTISP inference.

C1-T5-BINARY-CYCLE-EXACT086 is NP-complete as a **decision problem over implicit graphical cycle matrices**, because its YES/NO language is exactly the T5 homomorphism language under a polynomial-time computable translation. An explicitly printed dense binary matrix is still a polynomial-sized reduction but not a constant-factor bit-length reduction. No claimed general P!=NP lower bound follows.

## Executed computational audit

Executed dependency-free Node.js source: /mnt/data/tmr086/tmr1_t5_binary_cycle086.js (local machine copy). Raw outcomes: /mnt/data/tmr086/tmr1_t5_binary_cycle086_raw.json, SHA256 75511fa7853a831215b49b911e1c3a15cd466d1a66887d39cf466601603c58d8. It checked **1,127** original directed instances, **15,580** assertions, **12,087,991** candidate Z5 labelings and **142,754** candidate binary edge vectors with **zero failures**. Controls include n=0, isolated vertices, a self-loop, opposed arc pair, directed triangle, directed five-cycle, the transitive K4 NO instance, all 3^6 simple oriented/absent edge possibilities on four vertices plus smaller sizes, and 360 deterministic mixed graphs on 5,6,7 vertices with up to 11 arcs. For each instance, it independently counted all 5^n source labelings and all 2^m binary cycle vectors and verified the 5^c relation, cycle-matrix rank certificate (identity chord submatrix), and the b=2 Gaussian countercontrol. For each accepted b it independently reconstructed a root-zero source assignment and checked every original arc. These are finite **COMPUTATIONAL** checks, not a general proof.

A smaller standalone certificate is published under experiments/tmr/tmr1_t5_binary_cycle086_certificate.js. Repository source and readback should be audited separately from its execution status; the broader verified local source is not represented as that published certificate.

## Relationship to prior work, red-team safeguards and next dependency

The earlier /079 Fourier-flow method is complementary and already used F5 cycle structure; this note does not claim a new Fourier transform or a new classically unknown algebraic theorem. The increment-to-bit bijection and the universally satisfiable **Gaussian relaxation** specify where a proposed cheap linear solver ceases to be exact. Polynomial Gaussian elimination remains fully available whenever additional verified constraints reduce the actual bit intersection to an affine subclass. Other valid path-consistency, quotienting, polymorphism, separator, source-aware, dynamic programming, alternative encoding and compact-graph algorithms remain admissible.

DISJ: this is a positive encoding and counterexample to a proposed relaxation, not a universal lower bound. Relativization and general algorithm lower bounds OPEN. SAME_REALIZATION accounts for full parsing, matrix output vs implicit representation and time/space together. Configuration counting gives no mandatory computation lower bound. Full manuscript compilation, independent mathematical review and Lean/nanoda kernel reconstruction remain OPEN. P versus NP remains OPEN.

**Next:** Audit whether the all-pairs five-residue closure and source-aware decompositions leave a nontrivial binary-cycle intersection on explicit mixed C5/T5 hard-source images. Seek a result that applies to all exact algorithms, not merely Gaussian elimination or one Fourier representation.
