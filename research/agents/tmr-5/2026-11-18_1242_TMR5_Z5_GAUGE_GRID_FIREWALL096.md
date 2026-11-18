# TMR-5/096: Z5 gauge equivalence, high-treewidth directed-cycle/DAG twins

**Date:** 2026-11-18, Pacific. **Owner:** TMR-5 / PNP Machine Bottleneck Redteam. **Status:** exact mathematical construction, local-edge truth-table and independent numerical reproductions; external proof review pending. P versus NP remains OPEN.

## Gauge equivalence theorem

Let T5 have universe Z5, with arc relation R(a,b) iff b-a in S={1,3} modulo five. Then -S={2,4}=S+1. Fix a reference direction u_e->v_e on every edge of an undirected graph H. For an orientation O let its twist t_O(e) be 0 on reference-directed edges and 1 on reversed edges. Thus the edge restriction is x(v_e)-x(u_e) in S+t_O(e).

If orientations O,O' admit a potential phi:V(H)->Z5 with

    phi(v_e)-phi(u_e) = t_O'(e)-t_O(e)  (mod 5),

then x -> x+phi maps the solutions of O bijectively onto the solutions of O'. In particular their satisfiability and **exact solution counts agree**. Conversely, a vertex-translation equivalence of this kind requires this condition because S has no nontrivial translational stabilizer. The potential exists iff the signed twist difference sums to 0 modulo five around every undirected cycle. Find it on a spanning forest and check each chord in O(n+m) time. This tests gauge equivalence; it is not a general T5 SAT algorithm.

If A is the T5 adjacency matrix and P the shift matrix P[i,j]=1 iff j-i=1 mod 5, then

    A^T = A P,   A A^T=A^T A,   M(path of length L with b backwards arcs) = A^L P^b.

The arrangement of the backward arcs is irrelevant to the transfer. Since row 0 of A^4 is (4,4,1,6,1), every oriented private path of length at least four has strictly positive transfer for every pair of endpoint symbols. Such a path is decision-inert, but its exact counting weight is generally nonconstant.

## The unbounded-treewidth native T5 counterexample

For each integer h>=2, replace every vertex (r,c) of an h x h grid by an undirected 16-cycle with labeled ports v[r,c,i], i=0,...,15. Connect neighboring cells horizontally from left-cell port 0 to right-cell port 5, and vertically from upper-cell port 10 to lower-cell port 15. Every connector arc points right/down.

In D_h, orient every cell's 16-cycle consistently, v_i->v_(i+1 mod16). In D'_h, reverse the internal edges v_i->v_(i+1) for i=0,...,14 and **keep** closing edge v_15->v_0 and all connectors.

The shared underlying graph has:

    vertices N=16 h^2;
    arcs M=16 h^2+2h(h-1)=18h^2-2h;
    cycle rank r=M-N+1=2h(h-1)+1;
    maximum undirected degree 3, bipartite, and 2-vertex-connected.

Bipartiteness follows from local port parity (0/10 even, 5/15 odd). Every grid connector belongs to a lifted grid cycle, and each cell remains connected when one vertex is deleted, proving 2-connectivity. Contracting each 16-cycle yields the h x h grid minor; treewidth is therefore at least h.

D_h has precisely h^2 strongly connected components of size 16, each an oriented cycle. D'_h is a DAG, because each cell is now acyclic and inter-cell connectors go only right/down.

**Theorem:** #Hom(D_h,T5)=#Hom(D'_h,T5) exactly, for every h>=2.

**Proof:** Set phi(v[r,c,i])=i mod 5. Each reversed internal arc has phi(v_(i+1))-phi(v_i)=1. The unchanged closing arc has difference zero because phi(v_15)=phi(v_0)=0; connector endpoints are ports 0,5,10,15, all with phi=0. Apply the gauge theorem. This is an explicit bijection of *all* satisfying assignments.

**Linear-time SAT witness:** Put g_i=i mod5 for i=0,...,14, g_15=2, and x(v[r,c,i])=r+c+g_i mod5. The 16-cycle increments are fourteen +1 and two +3, horizontal connectors +1, and vertical connectors +3. The assignment x satisfies D_h; x+phi satisfies D'_h. This does not give a counting algorithm for arbitrary h nor an unrestricted CSP decision algorithm.

## Executed independent audits

A separate full Python verifier and independent NumPy/opt_einsum tensor-contraction program are included in the downloadable evidence package. They checked all 25 endpoint label pairs on each native edge against the transformation, all orientations of cycles C3 through C6 by exhaustive 5-symbol assignments against transfer products (8+16+32+64 patterns), SCC/connectivity/degree/bipartiteness and explicit witnesses through h=12 (2,304 vertices), and sparse exact-integer factor elimination versus separate object-integer tensor contractions for h=1,2,3. No assertion failures.

| h | Vertices | Arcs | Rank | Common exact homomorphism count |
|---:|---:|---:|---:|---:|
| 1 | 16 | 16 | 1 | 66,900 |
| 2 | 64 | 68 | 5 | 526,611,256,029,450,000 |
| 3 | 144 | 156 | 13 | 505,333,526,684,804,063,880,617,388,175,996,093,750 |
| 12 | 2,304 | 2,568 | 265 | Equality and witnesses verified without enumerating all solutions |


## Independent TMR-2/091 cross-track reproduction

TMR-2/091 reported a nine-vertex, 11-arc obstruction consisting of four private terminal paths of lengths (2,3,3,3). This run independently enumerated all **2,048** possible edge orientation words. The exact product of directed adjacency matrices agreed with the gauge-compressed formula for every word. There were only **192** different vectors counting backward edges per path (3 x 4 x 4 x 4), and the exact T5 homomorphism count was constant inside each class. Exactly **36** of the 2,048 orientation words were unsatisfiable, contained in **12** compressed classes, reproducing the TMR-2/091 empirical result. This is a genuine source-aware cofactor quotient and an explicit counter to charging distinct orientation words as irreducible machine work. It does not establish an algorithm for arbitrary source graphs or any universal lower bound.

**Attribution:** TMR-2/091 already states the matrix identity A^T=AS for its shift matrix S. The independent TMR-5 contribution here is the vertex-potential gauge theorem, high-treewidth orientation-pair family and independent reproduction/compression of the TMR-2 source obstruction. TMR-4's most recent available handoff remains focused on source-authenticated live-core circuit compilation; applying this gauge quotient to that compiler is a future cross-track test, not an accomplished theorem.

## Ranked dependency firewall

| Statement | Verdict |
|---|---|
| Exact fixed-template T5-CSP NP-complete | **PROVED**, Bang-Jensen/Hell/MacGillivray 1988 primary theorem |
| Z5 gauge theorem and O(n+m) equivalence test | **PROVED**, scoped to vertex translations |
| Identical solution counts with cyclic vs DAG orientations, high treewidth and cubic bipartite 2-connected underlying graphs | **PROVED** |
| Raw SCC/cycle/treewidth/rank measures force hard individual SAT instances | **FALSIFIED as instancewise inference** by explicit YES witnesses |
| Global polynomial counting on this entire grid-blowup family | **NOT ESTABLISHED**; width may grow with h |
| A representation lower bound implies unrestricted machine time lower bound | **OPEN** |
| Superpolynomial SAT lower bounds and P != NP | **OPEN** |

Primary references: [1] J. Bang-Jensen, P. Hell, G. MacGillivray, *The Complexity of Colouring by Semicomplete Digraphs*, SIAM J Discrete Math 1(3), 281–298 (1988), https://doi.org/10.1137/0401029 . [2] L. Barto, M. Kozik, T. Niven, *The CSP Dichotomy Holds for Digraphs with No Sources and No Sinks*, SIAM J Comput 38(5), 1782–1802 (2009), https://doi.org/10.1137/070708093 .

**Next falsification target:** use this exact Z5 potential condition to normalize cyclic/SCC claims before comparing variable-order OBDDs, adaptive FBDDs, tensors and direct source-aware CSP algorithms.
