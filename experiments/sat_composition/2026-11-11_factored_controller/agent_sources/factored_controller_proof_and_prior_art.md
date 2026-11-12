# Exact small-separator composition: proof, acquisition cost, and limits

## Scope

This note audits a deterministic controller for an explicitly typed 2-CNF plus affine system, or a Horn CNF plus affine system. Its theorem concerns a validated tree decomposition and the ranks of the affine rows assigned to individual bags. It is an implementation and audit of established project results, especially ARC229, ARC233, and ARC235. The generic composition method is classical constraint-network dynamic programming [1], and the local fixed-rank algorithms are established [2,3]. No unrestricted polynomial SAT theorem or algorithm-independent lower bound follows.

The new implementation work combines automatic bounded-separator discovery, the previously validated general-rank local engines, exact messages, reconstruction, and explicit resource-cap behavior. The new obstruction below is scoped to the decomposition certificate class and the specified polynomial representation.

## 1. Validated input structure

Let F consist of named original constraints on an explicit variable roster V. Each constraint is a signed clause in the selected local grammar, or an affine equation over GF(2). Form its primal graph by adding all edges of the clique on every original constraint scope.

A supplied or discovered decomposition is a tree T of bags B_t satisfying:

1. Every source constraint has exactly one owner t, with its entire scope contained in B_t.
2. Every declared variable occurs in a bag.
3. For each variable, the bags containing it form a connected subtree.
4. Every adjacent-bag intersection is checked from the actual bag contents. Its size is at most two for the 2-CNF backend, or at most one for the general Horn backend.

The source checks include empty clauses, zero affine rows, coefficients, right-hand sides, literal signs, and the complete source-to-owner map. Source identity is not inferred merely from an already computed answer.

Root T. For a nonroot bag t let S_t=B_t intersect B_parent(t), with S_root empty. Define R_t on S_t to be the exact set of assignments extendible to all constraints owned in t's subtree. Running intersection ensures that a subtree meets the rest of the formula only on S_t. Sibling interiors are disjoint after the parent bag is fixed.

## 2. Exact message compilation and its threshold

Every relation R on s<=2 Boolean variables has an exact 2-CNF representation with at most 2^s clauses. For each forbidden assignment a, add the clause containing x when a_x=0 and NOT x when a_x=1. This clause excludes exactly a. For s=0 the empty relation is represented by an empty clause and the nonempty relation by TRUE.

Thus messages with at most two variables can be conjoined with the parent's owned 2-CNF without changing its grammar. Parent-separator assignments are added as unit clauses. Neither operation adds affine rows. For a Horn backend, arbitrary unary messages are Horn, so adhesion one works identically. Arbitrary binary messages need not be Horn: x OR y has models 01,10,11, which are not closed under intersection.

At arity three, odd parity is a direct obstruction. Its models 100,010,001 have coordinatewise majority 000, which is not an odd-parity model. Every 2-CNF relation is majority-closed: if the majority violated a binary clause, each literal would be false in at least two of the three input assignments, so one input would violate both literals. Existential projection preserves majority closure. Consequently, a nonbijunctive ternary relation cannot be encoded by existential auxiliary 2-CNF alone either.

This is the threshold for *arbitrary* exact tables. Some larger tables are still bijunctive and can be recognized as such. That more general guarded case was already stated in ARC229. Similarly, recognized Horn messages can exceed one coordinate without breaking the Horn backend.

## 3. Bottom-up decision and top-down witness

Assume all child tables have been computed exactly. Compile them as above. For every assignment sigma to S_t, solve the conjunction of:

- the original clauses and affine rows owned by t;
- the exact clauses representing each child table;
- the unit clauses fixing sigma.

Set R_t(sigma)=true exactly when this local problem is satisfiable. Store a corresponding bag witness when true. Each successful bag assignment extends independently into its child subtrees because its child-separator restriction belongs to the exact child table. Conversely, any model of the subtree restricts to a locally feasible bag assignment. This proves message exactness by induction.

At the root, the unique empty assignment is feasible exactly when F is satisfiable. Recover a model by following cached witnesses: a parent bag determines a true child-table entry, whose stored witness agrees on the entire actual separator. Running intersection then makes all occurrences of every variable agree. Check the reconstructed assignment against the original source constraints.

If a local solver returns UNRESOLVED, that result is not a false message entry. A controller must propagate uncertainty or invoke another complete route. A resource cap does not prove UNSAT. There may be sound early UNSAT exits from independent already refuted constraints, but no missing table entry can be assumed false.

## 4. Time and storage

Let n_t=|B_t|, and let d_t be the coefficient rank of the affine rows originally assigned to t. The local formula includes all incoming message clauses, so its complete encoded length N_t must be charged. Pins are unit clauses, so the affine rank is at most d_t even if conditioning or simplification lowers it.

Define D(n,d)=sum_{i=0}^{min(n,d)} binomial(n,i). The established exact local algorithms give the upper bound

    T <= T_discovery + T_validation + T_ownership
         + sum_t 2^{|S_t|} poly(N_t) D(n_t,d_t)
         + T_reconstruction.

The polynomial factors include failed local calls, table conversion, source copies, indexing, parity reduction, and bit-operation overhead. No full union of all child separators is enumerated at the parent. The parent absorbs each small exact table into its local clause system. Thus a central bag can have an arbitrarily large accumulated interface while making at most four parent-state calls.

For fixed max_t d_t, polynomially many explicitly represented bags, and polynomial discovery/validation, the complete procedure is polynomial. The global affine rank may grow with the number of bags. Conversely, merely bounding separator size does not bound local affine rank.

An exact counting identity sharpens witness storage. For any valid decomposition tree with k bags and n distinct variables,

    sum_t |B_t| = n + sum_{edges tu} |B_t intersect B_u|.

Each variable's connected occurrence subtree contributes one fewer edge than vertices. Hence adhesion two gives total bag occurrences at most n+2(k-1). Storing at most four Boolean witnesses per bag uses at most 4(n+2(k-1)) witness bits in an ideal packed representation. This excludes Python object overhead, source data, graph copies, and active local workspace. Choosing the streaming seed backend gives polynomial local workspace even when local rank grows; it does not make its running time polynomial.

## 5. Sound finite discovery by small cuts

For a current graph G, use connected components when disconnected. Otherwise search singleton separators and then all pairs. A selected cut S is removed, yielding at least two nonempty components C_1,...,C_r. Create a separator bag S, and recursively decompose each induced graph on C_i union S after adding clique edges on S. The fill edges are graph bookkeeping and impose no Boolean constraints.

Inductive validity follows as follows. Each child decomposition covers its filled graph. Since S is a clique there, some child bag contains all of S. For s<=2 this follows directly from vertex or edge coverage; the general clique-in-a-bag property also follows from the Helly property of connected subtrees. Reroot the child tree at such a bag and attach it to the new separator bag. Variables outside S occur in one child only. Occurrences of variables in S connect through the new root. Thus running intersection is maintained, and all original edges remain covered.

An original factor scope is a primal clique. It cannot meet two different components outside S, because then it would contain an edge between those components. Therefore every original factor remains entirely within one child C_i union S, or entirely inside S. Assign it once to a containing bag after construction or use an equivalent exact ownership rule during recursion. The clique-fill invariant also preserves earlier boundary interfaces: a previous interface clique remains contained in a bag of every relevant recursive decomposition.

Every child graph is strictly smaller than the current graph, since at least one other nonempty component is excluded. The proposed implementation additionally charges *all* split operations, including empty-separator disconnected splits, to a global split budget L. Each split has at most n children. It therefore creates at most 1+nL recursive calls and bags. With L<=max(1,n), this is O(n^2), including fallback leaves.

At any call, there are O(n^2) candidate singleton/pair cuts, each checked by graph traversal in O(n^2) with a dense upper bound. Thus exhaustive discovery costs O(n^6) conservatively under the default split budget, plus polynomial parsing, graph construction, rerooting, copying, and certificate validation. A linear articulation-point routine improves the singleton stage without changing this safe bound. Pair probes that fail or precede a budget exit must be charged. Budget exhaustion retains the entire residual graph as a leaf bag, which preserves correctness but can leave its rank large. No optimality or guaranteed recognition of every useful decomposition is claimed.

The actual Hopcroft–Tarjan triconnected-decomposition theorem gives linear time and space in its RAM model [4]. An implementation using exhaustive pair probes must not claim that bound merely because the theorem exists.

## 6. A three-anchor obstruction with an explicit satisfying assignment

For m>=2, create m disjoint selector triples T_i={p_i,q_i,r_i} and three anchors z1,z2,z3. Let H contain all three pairwise at-most-one clauses within each triple, and every implication s -> z_a for selector s and anchor z_a. There are n=3m+3 variables and 12m binary clauses. Add one parity equation per selector triple.

The primal graph has each T_i as a triangle and every selector adjacent to every anchor. It is 3-vertex-connected: after deleting at most two vertices, an anchor remains, every remaining selector connects to it, and every other remaining anchor connects through a remaining selector. Deleting all three anchors leaves exactly the m separate triangles. Hence its vertex connectivity is exactly three.

This obstruction applies to every source-exact adhesion-two decomposition of this primal graph, not only the greedy finder. Any such decomposition must contain a bag holding all vertices. To see this, repeatedly consider a leaf bag. Unless it contains every vertex, a nonempty leaf-private part and a nonempty outside part would be separated by its intersection of size at most two, contradicting 3-connectivity. Thus a leaf not containing all vertices is contained in its neighbor and can be removed. Eventually a full bag remains. Once a full bag exists, running intersection implies that every other bag has size at most two: all its variables must cross the first edge on its path to the full bag. Every original ternary parity equation must consequently be owned by the full bag. Their disjoint supports give local rank m there.

For the specific flat 2-CNF closure-polynomial backend, choose targets as follows. Compute its deterministic ordinary 2-SAT base a on H with no equations, and set

    b_i = 1 XOR parity(a restricted to T_i).

This is a uniform polynomial-time construction using an ordinary 2-SAT call. Each translated parity indicator has zero constant term and is the sum of its three selector coordinates. If the base selected p in a triple, the three singleton closures are {y_p}, {y_p,y_q}, and {y_p,y_r}. If the base selected nothing, they are three distinct singleton choices, possibly enlarged by the common anchors that were zero in the base. If any base selector is one, every anchor is already one, so selector-generated closures introduce no anchor flips. Cross-triple products are all consistent and distinct. Therefore the actual polynomial dictionary has exactly 3^j terms after j rows and 3^m final terms, with 3(3^m-1)/2 candidate products.

The input is nevertheless transparently satisfiable: set all anchors to one, set every even-target triple to zero, and choose one selector in every odd-target triple. This is not a lower bound on SAT or all portfolios. For the present natural ordering the base chooses one selector per triple, making every opposed target even, and even the original all-zero assignment satisfies the formula. A Horn least-model check solves that case immediately; the seed backend can also exploit a translated anchor flip. The demonstrated exponential trace is specific to the chosen flat polynomial representation. The decomposition obstruction is stronger and basis-independent, but remains a statement about this certificate class, not intrinsic computational difficulty.

Independent executable verification is in `verify_three_anchor_obstruction.py`. It checks m=2,...,9, all 1,796 removals of zero, one, or two vertices across those graphs, the three-anchor cut, exact live-term counts, explicit source witnesses, and capped UNRESOLVED behavior. It additionally checks every valid base for m=2 (23 bases) and m=3 (71 bases), covering empty, mixed, and selected triples. Results are in `three_anchor_validation.json`. At m=9, the flat backend has 19,683 final terms and 29,523 candidate products.

### 6.1 Balanced targets obstruct all four specified local routines

Keep exactly the same Horn clauses and graph. Let p_i be the parity of the deterministic ordinary 2-SAT base in triple i. Set q=floor(m/2), and choose a target vector b of Hamming weight q maximizing its distance h from p. Explicitly, assign the q ones first to positions where p_i=0, then to remaining positions in deterministic order. If p has weight w, then h=w+q when q<=m-w, and h=2m-w-q otherwise. Therefore h>=q>=1.

For the original Horn least-model polynomial, an odd-target row contributes three distinct singleton-closure terms. An even-target row contributes the constant and those three terms. Across triples, every choice of a constant or a selector term produces a different support, and all selected supports are consistent. The common anchors do not identify distinct selector choices. Hence the final dictionary has exactly

    3^q * 4^(m-q)

terms. For the translated 2-CNF polynomial, a row differing from the base parity contributes three closed terms, while a matching row contributes the constant and three terms. The same support argument gives exactly

    3^h * 4^(m-h)

terms. The earlier closure analysis covers all possible valid bases. When some base selector is one, all base anchors are one and selector-generated closures contain no anchor flips. When every base selector is zero, the only shared closure bits are anchors originally zero. Distinct products still have distinct selector restrictions. Both exact polynomial dictionaries are exponentially large in m.

The streaming seed routines also have exponential prefix work on these balanced targets. For the original Horn formula, the positive rules never derive a selector from another coordinate. A satisfying assignment needs at least one selector in each of the q odd-target triples. Any seed whose closure is a satisfying assignment consequently contains at least q selectors.

For the translated 2-CNF formula, every satisfying original assignment has all anchors one because q>0. If the base has some selector one, its anchors are already one; a seed containing an anchor-flip coordinate is therefore incompatible with every satisfying assignment. Those anchor-flip coordinates are the only positive-implication mechanism that can transmit a selector change between different triples. Without them, each triple whose target differs from its base parity needs its own selector seed. If the base contains no selected triple, positive implications go from selectors to anchors and cannot create selectors in another block. Thus every satisfying translated seed has size at least h.

The specified streaming implementation enumerates all seeds in increasing cardinality. It must therefore attempt every seed of size below q in Horn coordinates, or below h in translated coordinates, before it can return SAT. These lower prefixes are

    sum_{i=0}^{q-1} binomial(3m+3,i),
    sum_{i=0}^{h-1} binomial(3m+3,i),

respectively. Both are 2^{Omega(m)} because q grows linearly with m. The source has size polynomial in m even with explicit integer-mask encoding, so these are superpolynomial growth rates in its encoded size. This claim concerns the actual cardinality-ordered enumeration routines; it is not a lower bound on every way to search for seeds.

The family still has a direct easy witness: set one selector in each odd-target triple, no selectors in the even-target triples, and all anchors to one. A Gaussian particular solution with all nonpivot variables zero, followed by Horn forward closure, also produces such a witness for these disjoint parity supports. Consequently the balanced construction demonstrates a limit of the four implemented local procedures and the adhesion-two certificate class. It supplies no algorithm-independent SAT lower bound.

`verify_balanced_three_anchor_obstruction.py` preserves the earlier simple controls and checks the balanced construction separately. Polynomial runs were checked through m=9; uncapped seed runs and exactly exhausted lower-prefix caps were checked through m=8. All 94 valid bases for m=2,3 were also tested, including 2,686 independent tests of forbidden smaller seeds using intersections of truth-table models rather than a forward-closure routine.

At m=8 (27 variables), both polynomial modes have exactly 20,736 final terms. The Horn seed routine tries 3,926 seeds; the translated 2-CNF routine tries 19,655. Both must first exhaust all 3,304 seeds of sizes below four. At m=9, the polynomial final sizes are 82,944 for Horn and 62,208 for translated 2-CNF. The m=20 arithmetic bound gives 61,917,364,224 final polynomial terms and a required smaller-seed prefix of 28,169,466,944 for both modes on the current base. Those m=20 exponential runs were not executed; the report labels these as derived bounds. Raw results are in `balanced_three_anchor_validation.json`.

## 7. Why adhesion three is an actual expressive boundary

A verified adhesion-three tree with maximum local affine rank one can already encode arbitrary 3-SAT. For each original clause (l1 OR l2 OR l3), make a leaf with private p,q,r, the parity row p XOR q XOR r=1, and implications p -> l1, q -> l2, r -> l3. Its projection onto the three original variables is exactly the clause: at least one selector must be true, and whenever an original literal is true one may choose its selector alone. A root bag contains all original variables and no owned constraints. Every leaf meets it on the three clause variables and has affine rank one; the root rank is zero. This is a uniform SAT-preserving reduction, with straightforward NP membership.

Thus unrestricted adhesion three plus fixed local affine rank alone describes an NP-complete class. This was already proved in project ARC230 and is restated with the full gadget in ARC236. It does not say that every ternary message is hard. ARC236 already gives a restricted extension by pinning a small hitting set of the nonbijunctive ternary child scopes, with charged O(3^h) cover search and at most 2^{s+h} local calls.

## 8. Recovered project precedence and differences

Actual GitHub source reads were made from `j15marti/pnp`. The original report copies are saved alongside this note.

- ARC229, summarized in the recovered `main.tex`, already proves exact binary-message absorption, avoids full accumulated-interface enumeration, allows any fixed local affine rank using the published theorem, and treats larger separators under a verified bijunctivity promise.
- ARC233 already gives polynomial discovery through a block-cut forest with unary messages and fixed local affine rank.
- ARC235 is an almost exact antecedent of the present pair-separator controller. Its report is `research/agents/lspv-1/2026-10-29_1715_LSPV-1_ARC235_TWO_ADHESION_FRONTIER.tex`, blob `8c2f657e2b36edeb9e2a0210dcf7449d8524b689`. It specifies exhaustive singleton/pair separators, virtual clique fill, exact ownership, running intersection, binary-message compilation, witnesses, cost accounting, and the arity-three obstruction. Its executable accepts rank at most one and returns UNKNOWN above one. It splits into two sides and proves a linear node bound by a potential argument. The new multiway bounded-budget construction instead uses a conservative quadratic node bound, a stack traversal, and the already validated arbitrary-rank local engines.
- ARC235 first compiles affine rows of arity at most two into exact 2-CNF, preserving source ownership. Without this normalization its greedy recognizer had a nine-variable deletion defect. It explicitly does not prove that recomputing a greedy decomposition preserves recognition after deleting constraints. Keeping a fixed validated decomposition does preserve a local rank cap under source deletion. The current work should retain this distinction.
- ARC236 is `research/agents/lspv-1/2026-10-29_1800_LSPV-1_ARC236_TERNARY_MESSAGE_COVER_FRONTIER.tex`, fetched at commit `56eeba7c81589bc31bc1c7f5325625cb061c40ab`, blob `721e2e993145c4ed7f784f23ce8e67129b291bb1`. It already states the hitting-cover extension and width-three rank-one star reduction. Its accompanying implementation specializes to rank-one stars, rather than arbitrary trees.

No classical priority is claimed for the current theorem. The concrete contribution is the current executable integration, independently audited source/decomposition semantics and caps, reuse of the general-rank backends, and the explicit three-anchor representation obstruction.

## References

[1] Rina Dechter and Judea Pearl. *Tree-Clustering Schemes for Constraint-Processing*. AAAI 1988, pages 150–154. The paper forms clusters, a join tree, and exact local compatibility constraints. Its generic procedure explicitly enumerates cluster solutions; the present typed local solver changes that local cost.

https://cdn.aaai.org/AAAI/1988/AAAI88-027.pdf

Retrieved web ref: turn36view0.

[2] V. Arvind and Venkatesan Guruswami. *CNF Satisfiability in a Subspace and Related Problems*. IPEC 2021, LIPIcs 214, Article 5. Theorem 2 gives deterministic O*(sum_{i<=d} binomial(n,i)) time for 2-SAT restricted to an affine subspace of codimension d. Theorem 17 supplies the deterministic algorithm. This is XP, so constant d is polynomial; d=O(log N) alone does not yield a polynomial bound.

https://drops.dagstuhl.de/storage/00lipics/lipics-vol214-ipec2021/LIPIcs.IPEC.2021.5/LIPIcs.IPEC.2021.5.pdf

https://arxiv.org/pdf/2108.05914

[3] Joshua Brakensiek, Sivakanth Gopi, Venkatesan Guruswami. *CSPs with Global Modular Constraints: Algorithms and Hardness via Polynomial Representations*. Section 3.2 gives n^{k(M-1)+O(1)} time for Horn formulas with k modulo-M equations for prime-power M, yielding n^{k+O(1)} at M=2. Its least-model `FindMinimal` routine is the relevant seed-enumeration precedent.

https://arxiv.org/pdf/1902.04740

[4] John E. Hopcroft and Robert E. Tarjan. *Dividing a Graph into Triconnected Components*. SIAM Journal on Computing 2(3), 1973, pages 135–158. The stated graph algorithm runs in O(V+E) time and space on a random-access computer. This is prior art for graph decomposition, not the measured bound of an exhaustive pair-search implementation.

https://doi.org/10.1137/0202012

https://ecommons.cornell.edu/entities/publication/523e4718-725e-4dc0-801e-d3fccd888d27

Retrieved web refs: turn34search4, turn34search5.
