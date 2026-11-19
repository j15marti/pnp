# TMR-5/078: connected bounded-degree T5 source with exponential fixed-order rank and polynomial direct exact count

Date: 2026-11-17 19:46 PST. Owner: TMR-5 / PNP Machine Bottleneck Redteam. Named dependency: **D5-T5-FIXED-ORDER-RANK-TO-MANDATORY-WORK**. Status **FALSIFIED/RETIRED** for any implication asserting that large chosen-order assignment rank or OBDD width forces large *unrestricted T5 decision/counting work*. The explicit source-scoped construction is **PROVED/EXACT RESTRICTED**, independent external mathematical review OPEN, finite execution COMPUTATIONAL. P versus NP OPEN.

## Candidate and attempted falsifiers, fixed before source/corpus search

For each n>=1 construct an authentic connected simple oriented T5-CSP source G_n with at most 9 incident edges per vertex, primal treewidth exactly four, and O(n) vertices/arcs, such that the full original-variable assignment indicator has rank at least 2^n over **every** field across one explicit bad prefix partition, hence any variable-ordered five-way OBDD at that prefix needs at least 2^n nodes. Yet a second OBDD order has O(n) nodes, and strict source recognition plus correct exact original-assignment counting costs polynomial bit time. Quantifiers: for every n there exists this explicitly constructible G_n; for every field K the stated **fixed-cut** rank lower bound holds; for all original assignments the representation semantics agree. No statement of an all-order or all-algorithm lower bound.

Falsifiers: (1) a nonrotation endomorphism of an authentic internal T5-module invalidates the count; (2) overlapping modules create inconsistent rotations or missing/duplicate input arcs; (3) the claimed identity rank submatrix has a cross-term of 1 or diagonal 0 in some field; (4) source recognition, integer output, or a good-order evaluator hides an exponentially costly stage. Earlier general-order sensitivity and compilation-vs-runtime barriers are known in Bryant 1986, Razgon KR2014, and the project's DISJ control. The contribution here is a concrete fixed-T5, simultaneously connected, bounded-degree, treewidth-four end-to-end witness, not a new universal OBDD theorem.

## Authentic source construction

Write Sigma=Z5 and R(x,y) iff (y-x) mod5 in {1,3}. Take n complete directed copies Q_i of the EXACT ten-arc tournament T5, with five positions q_{i,0},...,q_{i,4}. For i<n, identify q_{i,1} with q_{i+1,0}; make no other identifications. For each i add two private vertices a_i,b_i and the two actual directed input arcs q_{i,0}->a_i->b_i. The source is a genuine original-vertex graph, not a preloaded tensor, quotient or expanded Boolean circuit. The original template has no pins; the rotations are global satisfying homomorphisms. An explicit generator uses first five source indices 0..4, next four fresh indices per later module, and finally consecutive a_i,b_i indices, and emits all actual arcs. The strict source format can use the canonical ASCII header "p t5 V E", explicit v-rows for all vertex IDs and e-rows for all sorted unique arcs; any departure is rejected as malformed, while valid nonmembers need a separate exact fallback.

Direct counting of vertices/arcs gives V=5n-(n-1)+2n=6n+1, E=10n+2n=12n. Each core module is an undirected K5, consecutive modules meet in exactly one vertex, and each 2-path attaches at a vertex: a bag decomposition with K5 bags and path bags proves treewidth <=4, and K5 proves equality. Any shared core vertex has at most 8 incident tournament arcs plus one leaf-path arc; maximum degree <=9. The underlying source is connected. In a sorted explicit-digit encoding complete source length L=Theta(n log(n+2)).

## Exact original-assignment count and constructive decision

Any homomorphism of a five-vertex loopless tournament onto T5 is injective (different source vertices share a directed arc, so cannot map to one loopless target vertex), hence bijective. Every automorphism of THIS T5 is a rotation: the image of 0 has five choices; fixing the image of 0 fixes the two out-neighbors separately because the arc between them distinguishes 1 and 3, and fixes the two in-neighbors separately because their mutual arc distinguishes them. A rotation by the chosen initial color realizes each choice, so exactly five automorphisms exist.

A shared vertex between consecutive copies uniquely determines the next rotation. Thus the entire T5-core chain has exactly five labelings, given by q_{i,j}=t+i+j mod5, with t in Z5. For each fixed q_{i,0}, a_i has two possible labels and each determines two possible b_i labels. The pairs are private. Hence the exact ORIGINAL source assignment count is

    Z(G_n) = 5 * 4^n,

and each G_n is YES. The integer has exactly 2n+3 bits. A polynomial-time labelled-source recognizer reconstructs/compares every module and arc, with no supplied hidden decomposition; on recognized sources it outputs YES and the exact integer by a bit shift and multiplication by five, optionally producing a full witness. A conservative same-machine bit budget, including full parsing, invalid-input handling, graph generation, attempted checks, address arithmetic, source seek, multiplication/output and final validation, is T=O((L+1)^4), peak writable S=O((L+1)^2). This is a **recognized-family upper bound**; a correct generic fallback on valid nonmembers may use 5^V exhaustive search. The finite Python test below generates the adjacency records and exercises symbolic count/rank controls but does NOT implement the full ASCII parser or native Turing-machine compiler.

## Rank and fixed-order OBDD lower bound, on the assignment indicator ONLY

Fix the bad prefix X to contain every module/core vertex and a_1,...,a_n, with suffix Y=(b_1,...,b_n). Fix all core colors to t=0. At each i restrict row a_i to {c_i+1,c_i+3}, where c_i=q_{i,0}, and restrict column b_i to {c_i+2,c_i+1}. The local 2x2 acceptance matrix is literally

        b=c+2   b=c+1
 a=c+1     1       0
 a=c+3     0       1

because +1,+3 are exactly the permitted differences. Therefore the 2^n-by-2^n submatrix of the ACTUAL original-label assignment indicator is I_(2^n), over every field K. Its full fixed-cut matrix rank is >=2^n. A fixed-order 5-way OBDD querying all X before any Y must have at least 2^n distinct nodes at that layer, since each node determines one residual suffix function. The same obstruction survives any blockwise Boolean encoding of legitimate T5 labels when all X code bits precede all Y code bits, by restricting to legal codewords. This is a lower bound only for that declared order/representation, not for arbitrary decision of the encoded graph source.

There is an explicit good fixed order, processing the first module and its a_i,b_i pair, then each next module's four fresh vertices and its pair. All arcs whose endpoints have been read are checked, and at most the shared anchor color plus six within-block T5 colors need remain in state. A reject state is absorbing. Thus there is a complete original-variable five-way OBDD with at most O(5^7 n) internal nodes (a coarse constant), accepting exactly the same original assignments; an adaptive FBDD can use the same program. In parallel, exact tensor contraction / dynamic programming on the size-five bags costs polynomial time with bounded intermediate tensors. The direct formula is faster still. A source-aware algorithm never has to build the bad OBDD.

## Independent executed finite evidence and prior-work comparison

Executed CPython standard-library script: experiments/tmr/tmr5_t5_clique_chain078.py, revision tmr5-t5-clique-chain078.py.v1, no randomness/seed. Local executed source SHA256 b241aff18f27a0e1d236f7a19ca6ce07db76f359f3f6a1a94e629ba6ebd5c1a9. Full local raw JSON SHA256 1c087465492cf8b103850e90346243a3e07577e0c696cb41f24de501045064a4 (published summary JSON reserialized for compact readability). Python bytecode compilation passed. The script enumerated all 5^5=3125 target assignments to authenticate the five module automorphisms, enumerated all 5^7=78,125 complete original-source assignments for n=1 with count 20, built every actual source graph n=1..5, verified all arcs/degree/identification/count formulas, and computed independent 2^n binary suffix rows for each core rotation. Exact GF(2) Gaussian elimination returned ranks 2,4,8,16,32 with all assertions passing. The all-n/all-field theorem is the identity-submatrix proof, NOT inferred from finite tests.

Independent contextual primary sources: Bang-Jensen, Hell, MacGillivray, "The Complexity of Colouring by Semicomplete Digraphs", SIAM J. Discrete Math. 1(3), 1988, DOI 10.1137/0401029, confirms NP-completeness of THIS target by the >1-cycle semicomplete classification. Bryant, "Graph-Based Algorithms for Boolean Function Manipulation", IEEE Trans. Computers C-35(8), 1986, DOI 10.1109/TC.1986.1676819, for OBDD order dependence. Razgon, "On OBDDs for CNFs of Bounded Treewidth", KR 2014, arXiv:1308.3829, for distinction between structural width and restricted compilation. These are background/classification, not attribution of this explicit constructed family to those sources.

## Four gates and controls

| Gate | Verdict |
| --- | --- |
| DISJ sanity | **PASS** as a direct false-positive control: large fixed-cut rank and bad-order width coexist with an actual easy one-run algorithm; **FAIL** any inference rank/OBDD width => compulsory arbitrary-machine work. |
| Relativization | **PASS** for elementary graph/count/OBDD facts, **OPEN** for a nonrelativizing unrestricted P-vs-NP bridge, not asserted; BGS/algebrization/Natural Proofs remain applicable to any future claim. |
| Simultaneous DTISP | **PASS** only as a matched restricted upper T,S bit-machine ledger. **NOT APPLICABLE WITH REASON** to any forbidden-region time-space lower-bound contradiction because none is claimed. |
| Deterministic configuration counting | **PASS upper-only** for the restricted total recognizer; it supplies no work lower bound, randomized/quantum extension or P-vs-NP consequence. |

Controls: graph is connected, has maximum degree nine and primal treewidth exactly four despite bad-order rank 2^n. Legal easy path is a direct source recognizer, constant-bag tensor DP, and a good-order OBDD/FBDD. No field-basis trick can erase the stated fixed-cut rank because it contains an identity; yet changing the cut/order legitimately avoids the cost. DISJ/Horn/2-SAT/affine/unique-solution/equality/autarky/products/padding/selectors, source inversion, TMR-1's gadgets, TMR-2 cofactor, TMR-3 Fourier and TMR-4 quotient methods remain legal. This all-YES family does NOT falsify a separately stated necessary-work conjecture conditioned on globally mixed YES/NO hard distributions. /341 FAIL full UNSAT authority, /386 RESTRICTED, unchanged.

Repository-wide preflight NOT EXECUTED (no local Git checkout), native physical microcode NOT EXECUTED, full LaTeX build and independent formal proof kernel NOT EXECUTED, external referee OPEN.

## Ranked cross-track consequence and one next dependency

1. TMR-1: explicit 3SAT->T5 NP-hardness is PROVED/EXACT scoped with classical NP-completeness KNOWN THEOREM. It is a reduction, **not** a runtime lower bound. Polynomial inverse on labelled image remains a legal solver preprocessor.
2. TMR-2: fixed-cut residual/cofactor width can be exponential even on this bounded-degree, treewidth-four, directly countable authentic source. Any necessity invariant must quantify over legal orders, algebra and direct algorithms and discriminate original-source decisions from assignment indicators.
3. TMR-4: bad OBDD requires 2^n states, good OBDD has O(n) states on the SAME original function. Thus a chosen compilation's width does not transfer to arbitrary-machine work. Compiler constructions on restricted domains remain valid upper bounds.
4. TMR-3: constant-treewidth tensor contraction and exact original-count formula are valid cheap paths; checkpoint-provider/necessary evaluator bounds remain OPEN.

The **ONE next load-bearing dependency** is a quantified decision-work obstruction on a single genuinely mixed YES/NO T5 family **after** the paid TMR-1 image inversion, canonicalization, forced-triad/low-degree and twin/semicomplete/3-separator quotients, *and* minimization over legal adaptive, algebraic and direct source-aware algorithms. A lower bound must target the encoded decision language, not one prescribed prefix of a fixed formula's solution tensor. P versus NP remains OPEN.
