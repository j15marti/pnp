# Factored SAT controller: independent interface review

Status: standard tree-decomposition composition, with exact backend costs retained. This is not an unrestricted polynomial SAT result.

## Required decomposition contract

The bag graph must be a forest, every assigned original constraint must have all of its variables in one bag, and the bags containing each variable must form a connected subtree. Running intersection is essential: otherwise two pieces can give contradictory values to a variable without any separator noticing. An affine row crossing pieces cannot be split into separate parity claims without introducing and correctly charging an interface.

If each original constraint is assigned to one containing bag, then a child subtree communicates its exact projected support on the intersection with its parent. Running intersection ensures that this intersection contains every variable shared between that subtree and the remainder. Conjoining child supports with the bag's assigned constraints is exact.

For a separator of at most two Boolean variables, every support is representable by a 2-CNF: add the unary or binary clause excluding each forbidden boundary assignment. For an arbitrary Horn backend the corresponding universal guarantee holds on at most one boundary variable, because all unary relations are Horn.

The dynamic program performs at most four boundary queries per non-root bag at adhesion two, or two at adhesion one, plus the required root queries. This bounds the composition overhead; it does not bound the cost of the exact local backend. A single arbitrarily large bag already contains the unrestricted mixed Horn/affine problem.

## Two-coordinate messages are necessary

One child may project to u=v and another to u!=v. Every unary projection of each child is full, but their conjunction is empty. Thus independent unary summaries are not sufficient at a two-variable separator.

An explicit two-bag instance has bags {u,v,x} and {u,v,y}. The first child's constraints are u XOR x=0 and v XOR x=0. The second child's constraints are u XOR y=0 and v XOR y=1. Exact two-bit messages detect the inconsistency.

## Positive binary messages are legitimate in 2-CNF mode

Take private p,q, the equation p XOR q=1, and Horn implications p=>u and q=>v. Eliminating p,q gives precisely the relation u OR v. A 2-CNF message encoder must support this positive binary clause.

This example also shows why an arbitrary Horn backend cannot simply accept every two-bit child message as a Horn clause. The boundary relation has full affine hull and fails intersection closure, so it cannot be expressed as a boundary-only conjunction of Horn clauses and affine equations. A different representation or auxiliary variables would require an additional composition argument.

## A meaningful adhesion-three boundary

Use private selectors p,q,r, their odd-parity equation, their three pairwise at-most-one clauses, and the implications p=>u, q=>v, r=>w. Eliminating the selectors gives u OR v OR w.

This relation has seven models and full affine hull. It is not bijunctive: the majority of 100,010,001 is 000, which is excluded. Therefore it cannot be represented exactly as a boundary-only conjunction of 2-CNF and affine equations. The affine equations would all have to be trivial, leaving the impossible 2-CNF representation.

This does not rule out useful larger-separator methods. Some larger supports are affine or otherwise tractable; the example limits the generic binary-message theorem.

## Caps and unknown child states

Each child boundary state must distinguish SAT, UNSAT, and UNRESOLVED. An unresolved state is possible, not forbidden.

For a sound UNSAT conclusion, evaluate the parent against the upper support containing SAT and UNRESOLVED child states. If even that relaxation is UNSAT, the original parent is UNSAT.

For a sound SAT conclusion, every chosen child boundary state must have an actual satisfying witness. One way to guarantee this is to solve against the lower support containing only child states already certified SAT. Otherwise the answer remains UNRESOLVED unless missing child witnesses are obtained.

A concrete cap control gives a child private p,q with the genuine nonunit Horn clause NOT p OR NOT q and the equation p XOR q=0, independently of its separator bit. Under the tested 2-CNF translation, both boundary states remain UNRESOLVED with zero seed or expansion budget. Discarding them would incorrectly derive an empty support; treating them as certified SAT would fabricate a witness. The root's empty local query is solved by the Gaussian terminal, but the controller correctly downgrades its candidate to UNRESOLVED because the selected child has no certificate. Pure-affine or unit-only controls are now legitimately resolved by the new polynomial Gaussian terminal and should not be expected to remain unknown.

## Separator controls

The one-anchor expansion family consists of m selector triples, their odd equations, within-triple pairwise exclusions, and each selector implying the common anchor. Bags {a,p_i,q_i,r_i} have adhesion one and avoid the 3^m flat polynomial expansion.

For a graph with no articulation vertex, use two common anchors a,b and make every selector imply both anchors. With at least two triples, removing either single anchor leaves the graph connected, while removing both separates the triples. Bags {a,b,p_i,q_i,r_i} have adhesion two. Choosing every first selector and both anchors true is a complete explicit witness.

The 33-variable Mycielski selector instance from the preceding audit remains a hostile exact terminal. A decomposition cannot discard its compatibility simply because its local unary/binary abstract fixed points are consistent.

## Automatic discovery invariant

Deleting a separator S partitions a scope graph into components C_i. Each child graph retains C_i union S and makes S a clique. A parent bag S is attached to a child bag containing all of S. Such a bag exists because every clique is contained in a bag of a valid tree decomposition: the connected occurrence subtrees of clique vertices pairwise intersect and satisfy the tree Helly property.

Every original factor remains covered because its scope is a clique. Running intersection is preserved by attaching each occurrence of a separator through a bag containing that separator. Fill edges constrain only the structural search and are never added to the logical formula. Budget fallback preserves the entire remaining residual in one bag, so it affects decomposition quality without changing SAT semantics.

The independent discovery audit checks every labeled graph through five vertices, using tautological clauses to retain isolated vertices. It also supplies every clique of size at least three as an affine factor and verifies that each entire scope has a containing bag. Articulations are separately compared with brute-force vertex deletion. These checks do not depend on the solver's own decomposition validator.

## Three-connected scope graphs force a full bag

For any tree decomposition of a three-vertex-connected graph whose adjacent bag intersections have size at most two, some bag contains every graph vertex.

For each tree edge, consider the unions of vertices on its two sides. Their overlap is exactly the adhesion by running intersection. If both sides had an exclusive vertex, deleting the adhesion would separate the graph, contradicting three-connectivity. Thus at least one side has no exclusive vertex. Orient every edge toward a side containing all graph vertices; ties can be oriented arbitrarily. A finite directed tree has a sink. Each side pointing into this sink contains the whole graph, and running intersection forces every vertex into the sink bag itself.

Once a full bag exists, no other bag can contain three distinct original vertices: the path from that bag to the full bag would have an adhesion containing all three. Therefore every original ternary affine factor must be owned by the full bag. For the source agent's three-anchor family, all m independent ternary parity rows are forced into that bag, so the original local affine rank remains m in this scope-preserving certificate class.

This is a limitation of the specified graph decomposition and local-rank certificate. It does not rule out semantic simplification, branching on the anchors, a different representation, larger interfaces, or a faster unrestricted SAT algorithm.
