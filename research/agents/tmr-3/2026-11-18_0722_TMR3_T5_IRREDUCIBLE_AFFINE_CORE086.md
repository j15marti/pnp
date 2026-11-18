# TMR-3/086: canonical path core and Z5 affine closure

Owner: TMR-3 / PNP Time-Space Tradeoffs. 2026-11-18, Pacific Time.
Status: PROVED/EXACT restricted algorithm and infinite-family width falsifier. Finite validation is COMPUTATIONAL, not an unrestricted lower bound. P versus NP OPEN. Independent review OPEN.

## End-to-end authentic source pipeline

Input is a completely encoded directed graph G=(V,E), including loops and antiparallel arcs, and the fixed relation R(a,b) iff b-a in {1,3} mod 5. Parse source, discover maximal directed paths with internal indegree=outdegree=1 vertices, isolate components consisting of directed cycles, propagate exact modular difference equations after intersections of short-path supports, then count every original vertex assignment using integer path weights. All components and constraints are derived from the original input. No outside decomposition, oracle, preloaded checkpoint or promise is used.

## Theorem 086A: exact path factorization

Put B={v:(indeg(v),outdeg(v)) != (1,1)}. Every arc lies in a unique maximal directed B-to-B path (allowing equal endpoints) with private interiors, or in an independent directed cycle whose every vertex is (1,1). Define M as the 5x5 adjacency matrix of R and W_l(d)=(M^l)[0,d]. Then

    Z(G) = (product_{cycles C} 5 W_|C|(0))
           * sum_{x in Z5^B} product_{paths P:u->v} W_|P|(x_v-x_u).

Proof: Every (1,1) internal vertex has one predecessor and one successor. Following arcs yields exactly these paths and disjoint cycles. All internal assignments are independent conditional on B. M powers enumerate precisely their fixed-endpoint extensions; trace(M^l)=5 W_l(0) counts a pure directed cycle.

The support sets of W_l are: l=1: {1,3}; l=2: {1,2,4}; l=3: {0,2,3,4}; all l>=4: Z5. Pure directed 1- and 2-cycles are UNSAT; directed cycles of length at least 3 have positive trace. Decision may drop internal private paths of length>=4; exact counting must retain their integer weights.

## Theorem 086B: mod-5 affine closure

For each short path, intersect its support with all other short paths on the same endpoint pair, normalizing orientation and existing affine offsets. An empty intersection proves UNSAT. A singleton {d} forces x_v-x_u=d modulo five and is merged with potential union-find. Recompute intersections after each round until no singleton remains. Each successful merge strictly reduces the number of root variables, so there are at most |B|-1 successful merges and the process is polynomial. Every forced equation is a logical consequence of original constraints, hence preserves all colorings. Remaining short-path constraints are a correct residual CSP over DSU roots.

In particular, a direct arc and a parallel private directed 2-path force difference +1, because {1,3} intersect {1,2,4}={1}; the private vertex is uniquely x_u+3. Supports for three parallel lengths 1,2,3 have empty intersection. A directed triangle of such +1 gadgets is UNSAT even though the bare directed triangle is SAT: adding the three equations would demand 3=0 mod5.

## Theorem 086C: exact fast count after contraction

If every maximal source path has endpoints in the same DSU class after affine closure, and r affine roots survive, its endpoint differences are fixed. Thus

    Z(G)=5^r * (product_{pure C} 5 W_|C|(0))
               * (product_{source P} W_|P|(fixed_difference_P)).

This identity remains true with long paths. Each affine root has five global rotations and all path factors are constant in those rotations. For general instances with interroot paths, exactly enumerate the remaining 5^r root assignments with the original integer path weights, preserving source-vertex counting semantics.

## Theorem 086D: arbitrary directed H gadget and high-width counterexample

For any oriented/source directed H, keep each arc u->v and add a fresh private 2-step u->p_uv->v. Call the resulting original source H+. All edges force x_v-x_u=1, and the unique private color is x_u+3. Consequently Z(H+)=5^{c(H)} if these mod-5 differences are consistent on every underlying connected component, and zero otherwise. This is source-decidable in polynomial time by potential union-find.

For an oriented complete bipartite graph K_{k,k} (all arcs left to right), H+ has n=2k+k^2 vertices, m=3k^2 arcs, undirected source treewidth at least k, and exactly FIVE original source colorings, for every k>=1. At k=100: n=10,200; m=30,000; Z=5. The source contains K_{k,k} as a subgraph. Original branch-graph width therefore can grow without any necessary computational hardness. An affine-inconsistent three-cycle of the same gadgets has Z=0, giving an UNSAT easy-family control.

## SAME_REALIZATION time and space

Let N be encoded original input bit length and r final DSU-root count. A single deterministic blank-start one-tape implementation has conservative simultaneous upper bounds

    T(N)=O((N+1)^12 (1+5^r)),
    S_peak(N)=O((N+1)^4) bits.

The one execution charges input authentication, every source read, adjacency and path searches, failed affine-closure scans, addresses and indices, potential union-find operations, exact O(N)-bit path-table arithmetic, root enumeration when needed, retained live workspace, output and validation. For recognized closed-form sources the factor 5^r is not enumerated: T=O((N+1)^12), with the same S bound. The bound is a symbolic single-tape implementation analysis, NOT executed microcode, NOT a universal time-space lower bound. High representation width or a large cycle space does not imply a necessary runtime.

## Reproduction and evidence

The full local self-contained reference, in the linked reproducibility ZIP, executed 1,296 deterministic checks without failure; SHA256 697ae79a030bf48e2e4fb68fe28ce4792c70638c4efa6f7d96e4cd10214818f7. Controls: exhaustive 512 directed graphs on 3 vertices with loops, 570 seeded random original digraphs (n=1..6) versus independent 5^n brute force, 150 original endpoint-path counts, cycle checks, contradictions, exact counts on K_{k,k}+ through k=100, 15 disconnected gadgets counted directly. The independent compact repository Python implementation executed 704 controls with no failures (seed 86086). A new theorem section compiled standalone into two pages; combined-manuscript compilation, native one-tape microcode, outside peer review are OPEN.

Gates: DISJ PASS restricted as a width-only fallacy control; relativization NOT APPLICABLE to any class separation; simultaneous DTISP PASS restricted constructive upper bound on the same realization; deterministic configuration counting PASS only as upper-bound consistency. Preserve Horn/2SAT, affine/XOR, bounded-width DP, disconnected products, loops/opposed arcs, source padding, path saturation, legal alternate algorithms, Natural Proofs/algebrization caveats, prior /341 full-UNSAT FAIL and /386 RESTRICTED.

Next load-bearing dependency: C3-T5-AFFINE-RESIDUAL-HARD-CORE087. Seek source-recognized residual hard candidates after BOTH private-path and forced-affine compression; test primal/dual width, rank, Fourier and exact branch-and-bound on authentic inputs. A representation lower bound alone is not a same-machine time-space lower bound.

Reference: Bang-Jensen, Hell and MacGillivray, The Complexity of Colouring by Semicomplete Digraphs, SIAM J. Discrete Math. 1(3), 281-298 (1988), DOI 10.1137/0401029. NP-completeness of the unrestricted T5 template follows because T5 is semicomplete with multiple directed cycles. No quantitative SAT-to-T5 reduction exponent is claimed.
