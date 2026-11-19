# TMR-5/084: connected bounded-degree high-treewidth T5 UNSAT instances invisible to every singleton-anchored AC-3 pass

**Owner:** TMR-5 / PNP Machine Bottleneck Redteam. **Research date:** 2026-11-18 00:46 PST. **Status:** constructive theorem conditional on a finite explicitly reproducible 71-vertex AC-3 certificate, with a symbolic one-vertex gluing proof; independent external mathematical review and proof kernel OPEN. **P versus NP OPEN.**

## Counterexample and exact construction

Fix R(a,b) iff (b-a) mod 5 belongs to {1,3}, with labels in Z5. Let H- be the 11-vertex Grötzsch graph M(C5): its original rim 0..4 forms a 5-cycle; clones 5..9 are connected to each rim neighbor of the corresponding original vertex; apex 10 joins all five clones. H- has 20 edges and chromatic number four. Indeed, a 3-coloring of the Mycielski graph would recolor base vertices using the apex color with their clone colors, yielding an impossible 2-coloring of C5. Since the undirected target C5 has chromatic number three, #Hom(H-,C5)=0.

Define a positive control H+ with 11 vertices and the same 20 edges: left vertices i=0..4 and right vertices 5+j, j=0..5, with edge i--(5+(i+d) mod 6) for d=0,1,2,3. H+ is connected bipartite. Direct independent C5 source backtracking yielded 0 homomorphisms for H- and 660 for H+.

Expand every source edge {u,v}, u<v, with fresh a,b,c and the five genuine T5 arcs
```
u->a, a->b, b->c, u->c, c->v
```
The first four force a=u+1, b=u+2, c=u+3 mod5 uniquely, and the last allows exactly v-u in {1,4}. Every C5-coloring has a unique T5 original-variable lift. The expanded D(H-) therefore has 71 original T5 vertices, 100 genuine arcs, is a DAG and has a bipartite underlying graph, yet is UNSAT.

**NEW FINITE CERTIFICATE:** For each of the 71 possible pinned T5 vertices, ordinary binary AC-3, started with that one vertex fixed to label 0 and all other domains full, terminates in **nonempty** arc-consistent domains. The executable separately checks every retained label has constraint support after convergence. Rotation symmetry implies all 355 anchor/label combinations survive. The second, independently written synchronous/Jacobi AC-3 implementation confirms every anchor, while a separate C5 source backtracker confirms UNSAT. Thus universal singleton-anchored AC-3 decision completeness is **FALSIFIED**, even with raw T5 DAG and bipartite-underlying source restrictions.

## Unbounded connected construction and gluing lemma

**One-vertex gluing lemma.** If two CSP graphs have nonempty arc-consistent boxes for every single-vertex/single-label pin, identifying one vertex from each preserves this property. For a pin in the first block let D be its supported box. For each color c in D(s) of the common vertex, take a nonempty arc-consistent box for the second block with s=c and union these boxes over c. Unions of boxes over the same binary constraints are arc-consistent, and the shared domain is exactly D(s). The two boxes glue to a supported global box. AC-3 from the initial domains contains this box and cannot wipe out. Symmetry handles a pin in either block. Iterate over a tree of one-vertex overlaps. Any satisfiable component in which each vertex can realize each label by a witness also has the required property.

Identify apex 10 of each H- block with original vertex 0 of the next, making an h-block chain. Optionally identify its last apex with a corner of an LxL grid, L>=2. Expand all edges using the five-arc gadget. The expanded grid is satisfiable for every pin by rotating a two-coloring of the bipartite grid, with forced unique gadget extensions. Hence the gluing lemma and base certificate give, for **every** h>=1 and L>=2, a connected UNSAT T5 source on which **no single-vertex anchored AC-3 call detects inconsistency**. This infinite-family assertion uses the finite 71-vertex computational certificate; it is not a standalone symbolic classification of all base AC-3 domains.

Every expanded instance is a DAG, underlying bipartite, with raw max total degree at most 18; its treewidth is at least L by a grid minor. The YES companion replaces the H- blocks with H+ blocks, is satisfiable, and is built with the same vertex and arc counts and structural restrictions. With no grid: N=70h+1, M=100h; with grid:
```
N=70h+7L^2-6L,
M=100h+10L(L-1).
```
The YES/NO families need not have identical underlying graphs or individual degree sequences. The NO subgraphs contain constant-size UNSAT cores, so this does not claim growing minimum unsatisfiable support.

## Independent execution

Standard-library Python event-queue AC-3 and a separate synchronous/Jacobi implementation were run on the actual, uncontracted five-symbol beat arcs. The first verified every root and an independent support certificate on twelve full instances (h,L)=(1,0),(2,0),(3,0),(1,3),(2,4),(2,6), each YES and NO: **2,244 anchored computations, zero contradictions, zero assertion failures**. The largest was 356 original T5 vertices and 500 arcs. The second AC-3 implementation checked every pin on 71- and 228-vertex UNSAT instances; a separate exact C5 backtracker returned 0/660 on the base sources. General proof is the gluing lemma plus the fixed finite certificate, not extrapolation from h<=3.

Event-queue verifier SHA256: `25d0f74afa573d5696d65dcf558e47a7eb71c271735dce07327ac93cf1cb82ec`.
Independent crosschecker SHA256: `438a14ab6625250fa9bb67ffc07289200a9395cd52c33f315ba21f6241a1cdfd`.
Raw JSON SHA256: `e0ccba8b1e972430fd75d6a1f7b1fd2e647b463885da66126acabbe167f80f2b`.
The full executed sources and full mathematical report are bundled in **TMR5_084_AC3_false_positive_evidence.zip** in the run's delivered artifacts. An independently executed byte-exact compact Python verifier is GitHub-published at `experiments/tmr/tmr5_t5_grotzsch_anchored_ac3_084.py` (blob SHA `cfca23a0051ea9bb0ad9126b9e60bec762d7e012`), and the exact event-queue raw JSON is GitHub-published at `results/raw/tmr/2026-11-18_0046_TMR5_GROTZSCH_AC3_084_RAW.json` (blob SHA `3d12ceaf139e82c6e3a24ca8802528369cffedcf`). The larger local cross-check and full event-queue files are additionally supplied in the ZIP but not separately GitHub-published. External review, Lean/nanoda, native TM replay and full repo/LaTeX preflight were not run.

## Ranked proof-chain audit

1. Exact specific T5 CSP NP-completeness: **KNOWN PRIMARY THEOREM**, Bang-Jensen, Hell and MacGillivray (1988); further Barto-Kozik-Niven (2009) smooth-digraph classification.
2. Five-arc private gadget from C5 to T5: **PROVED/EXACT, scoped**, no implication about machine time.
3. Universal singleton-anchored AC-3 completeness for authentic connected DAG/bipartite T5: **FALSIFIED** by the 71-vertex instance and gluing amplification.
4. Structural treewidth, same N/M and mixed YES/NO -> necessary machine work: **FALSIFIED as an instancewise inference**; these source-recognizable families remain easy to decide.
5. TMR-2 dynamic cofactor rank or TMR-4 tensor/OBDD representation cost -> arbitrary-machine lower bound: **OPEN**.
6. SAT superpolynomial decision lower bound: **OPEN**.

DISJ: PASS as another false-positive control. Relativization: no separation claim. Simultaneous DTISP: only restricted upper methods; no lower-bound transfer. Deterministic configuration counting: upper-bound safeguard only. Source-aware algorithms, nonlinear/global consistency, adaptive FBDD, and Fourier/finite-field shortcuts remain legal.

**Next priority:** require candidate invariants to distinguish actual UNSAT from nonempty anchored-AC-3 fixpoints, while preserving every original source variable and charging all preprocessing. P versus NP OPEN.

### Primary sources
[1] Bang-Jensen, Hell, MacGillivray, *The Complexity of Colouring by Semicomplete Digraphs*, SIAM J. Discrete Math. 1(3):281-298, 1988, https://doi.org/10.1137/0401029.
[2] Barto, Kozik, Niven, *The CSP Dichotomy Holds for Digraphs with No Sources and No Sinks*, SIAM J. Comput. 38(5):1782-1802, 2009, https://doi.org/10.1137/070708093.
