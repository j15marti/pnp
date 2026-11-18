# TMR-5/083: high-treewidth, isostructural YES/NO T5 DAGs resolved by one generic anchored AC-3 pass

**Owner:** TMR-5 / PNP Machine Bottleneck Redteam. **Date:** 2026-11-18 00:12 PST (research session). **Status:** PROVED/EXACT RESTRICTED by elementary symbolic calculations; finite independent Python corroboration COMPUTATIONAL; external review, formal kernels, full LaTeX build OPEN. **P versus NP OPEN.**

## Research question and relation

Fix Σ=Z/5Z and R(x,y) iff y-x belongs to {1,3} modulo 5. TMR-5/082 constructed YES/NO pairs having an identical underlying graph, bounded degree, high treewidth, large minimum UNSAT support, and two different arc orientations. However its high-treewidth grid was expanded via C5-adjacency gadgets, and the generic AC-3 test gave an easy NO certificate, not a complete exact-counting algorithm for both outcomes. This /083 variant replaces **every** macro-edge, including grid edges, by a **rigid four-arc affine module**, so a single root-conditioned, completely generic T5 arc-consistency pass resolves BOTH outcomes and outputs the exact count as either 0 or 5. No source grammar or gadget recognizer is used by the AC-3 solver.

## Rigid, reversible T5 module

For a directed macro-edge u to v, insert private a,b and arcs
`u -> a, a -> b, b -> v, u -> v`.
The three-step path permits differences 0,2,3,4, while the direct arc permits 1,3. Their intersection is {3}; only increments (1,1,1) realize 3. Thus this module has **one** extension per allowed endpoint pair, forces v=u+3, a=u+1, b=u+2 modulo five, and none otherwise. Reverse all four arcs to force v=u+2, a=u-1, b=u-2, again with a unique extension. Both orientations have the **identical** underlying undirected four-cycle and are DAGs.

An independent 25-pair enumeration per orientation verifies all 50 endpoint cases. A generic binary AC-3 implementation, knowing only R and the four raw arcs, fixes every variable of either oriented module to a singleton if **any one of its four vertices** is pinned. This was checked for all eight oriented module/anchor configurations. Translation by c modulo five covers all five pin values.

## Mixed full-family construction

For any grid side L>=2 and theta path length h>=5, take an L-by-L undirected grid, oriented right/down, with corner s. Attach at s two internally vertex-disjoint paths, each of h macro-edges, leading to a common new vertex t. Each grid macro-edge is a forward rigid module (+3). On the two paths use the same underlying four-cycle module at every position but selectively reverse its four arcs.

* **YES:** reverse module 2 on each path. Each path forces t-s=3h-1 modulo 5.
* **NO:** leave the first path completely forward; reverse modules 2 and 4 on the second path. The path increments are 3h and 3h-2, incompatible modulo 5.

Both structures share precisely the same labelled underlying undirected graph, and both are DAGs and underlying-bipartite. They have identical multisets of (indegree,outdegree): along each path an F-to-R boundary is a two-in/zero-out macro-vertex, an R-to-F boundary is zero-in/two-out, and other internal path vertices are one-in/one-out. YES has two of each exceptional boundary over its two paths; NO also has two of each, concentrated on the second path. Grid and endpoints are unchanged. Each macro incidence produces two ordinary arcs and private vertices have degree two, so maximum total degree is 8.

There are 2L(L-1)+2h macro-edges, L²+2h-1 original vertices, and two private vertices per macro-edge. Therefore BOTH raw graphs have

```
N = 5L² - 4L + 6h - 1
M = 8L(L-1) + 8h
```

(the underlying edges are the same M edges). The grid is a minor, giving treewidth at least L. Moreover, each original edge is replaced by a four-cycle with a direct terminal edge. Attaching two width-2 bags to a decomposition bag containing the endpoints preserves width max{2, tw(base)}. The two-path cycle is attached at grid vertex s, so for L>=2 the treewidth is **exactly L**, using the standard L-by-L grid treewidth theorem.

## Exact count and source-independent polynomial solver

Each rigid module is equivalent to a linear equation x_v-x_u=+3 or +2 modulo five, with precisely one private-variable lift. A connected consistent system has one free global translation, hence **exactly five** full T5 homomorphisms; an inconsistent system has none. The grid is consistent by x_(i,j)=3(i+j)+c, and the two theta paths have the increments shown above. Thus

```
#Hom(D⁺_(L,h),T5)=5,   #Hom(D⁻_(L,h),T5)=0.
```

One may recognize and solve the modules by graph traversal (linear time), but the stronger source-oblivious statement is that **ordinary binary AC-3 with one arbitrary vertex fixed to A (0)** decides both instances without learning the construction. Every four-arc module propagates singleton domains through its four vertices; the connected macrograph propagates globally. YES reaches all singleton domains and checks every arc. NO reaches a contradiction, regardless of the choice of anchor. T5 translation symmetry makes root=0 without loss of generality, giving the exact count 5 or 0 on this promise family. With fixed five-element domains and bounded degree, this is O(N+M) domain-revision work.

This is an algorithm on the declared restricted family, NOT a polynomial-time solver for arbitrary T5-CSP. Unpinned arc consistency remains ineffective on general nonlooped instances, and even anchored AC-3 may fail to decide other instances.

## Locality and large UNSAT support

The only inconsistent macro-cycle is the two-path theta cycle with 2h distinct original vertices. Removing any one of its original vertices destroys the inconsistency, leaving the remaining partial modules and the articulation-attached grid satisfiable. Therefore any UNSAT subgraph of D⁻ contains at least 2h vertices. This **does not** imply large time cost: anchored AC-3 finds the globally propagated contradiction in linear work.

## Executed independent reproduction (Python 3, standard library)

* 50 terminal-pair module checks and 8 isolated module-anchor AC-3 controls.
* Seven fully built YES/NO pairs with (L,h)=(3,5),(4,5),(5,5),(6,6),(7,7),(9,9),(12,12), up to N=743 and M=1,152.
* Both input arc lists independently checked for DAG, underlying bipartiteness, degree<=8, identical undirected edge sets and directed-degree multisets.
* Independent Z5 quotient solver returned exactly 5/0; reconstructed all YES witnesses, checked every raw T5 arc.
* A generic binary AC-3 implementation with only a single root fixed to zero returned **fully singleton consistent YES** and **domain wipeout NO** for all seven pairs.
* All 310 individual root choices on the two smallest pairs likewise resolved the correct result; every vertex can serve as the anchor.
* Twenty deletion controls on NO pairs verified that removing any theta original vertex yields an actually SAT induced subgraph, using a separate generic AC-3 plus backtracking CSP engine.
* Two full Python runs produced byte-identical raw JSON, SHA256 `660b177e1036852731bd681e00ee72ea6cc496c4191479e8b353670d8f6f47ab`. Executed main source SHA256 `ca7cec4c23856267192fb0a12d980e5ab1a22e637439343ff3e888ae1d30fd49`. Zero failing assertions.

Executed, fully self-contained Python verifier: `experiments/tmr/tmr5_t5_grid_theta_ac3_083.py`; byte-exact raw evidence: `results/raw/tmr/2026-11-18_0012_TMR5_GENERIC_AC3_GRID_THETA083_RAW.json`. Both were published on the existing draft branch and read back by GitHub blob SHA; the symbolic proof does not depend on the files. No full repository preflight, compiled LaTeX build, native-machine microstep execution, formal proof kernel, or independent referee audit was performed.

## Ranked dependence and safeguards

1. **T5 NP-completeness:** KNOWN PRIMARY THEOREM, Bang-Jensen, Hell and MacGillivray (1988), for semicomplete templates with multiple directed cycles; this specific regular five-vertex tournament qualifies.
2. **TMR-1 C5-to-T5 gadget and Boolean front end:** previously independently verified in scoped models; unchanged here.
3. **Identical-underlying mixed YES/NO pairs with tw=L and long UNSAT support:** PROVED/EXACT RESTRICTED.
4. **Generic anchored AC-3 decides and exactly counts both new families:** PROVED/EXACT RESTRICTED; direct finite reproduction supports it.
5. **Large treewidth + bounded degree + identical support geometry + large local obstruction => mandatory expensive machine work:** FALSIFIED as an instancewise inference, now even without source recognition.
6. **General adaptive branching, OBDD/FBDD, tensor and circuit lower bounds on arbitrary mixed T5:** OPEN; no transfer from this construction.
7. **General SAT superpolynomial lower bound or P != NP:** OPEN.

DISJ: PASS as a source-oblivious falsification control. Relativization: no unrestricted consequence. Simultaneous DTISP: only the constructed linear upper algorithm. Deterministic configuration counting: an upper-bound safeguard, not a lower bound.

### Primary reference

Bang-Jensen, J., Hell, P., and MacGillivray, G. (1988). *The Complexity of Colouring by Semicomplete Digraphs*. SIAM Journal on Discrete Mathematics 1(3):281–298. https://doi.org/10.1137/0401029.

**Next test:** quantify whether a proposed lower-bound invariant survives an unrestricted solver which is allowed to pin one variable, propagate singleton AC-3, and then contract any rigid submodules. A valid worst-case lower-bound theorem must explicitly defeat such source-oblivious adaptive preprocessing.
