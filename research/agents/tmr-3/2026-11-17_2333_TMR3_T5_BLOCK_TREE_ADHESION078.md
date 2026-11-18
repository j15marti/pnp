# TMR-3/078: source-derived block-cut tree gluing for exact T5 counting

**Date:** 2026-11-17 23:33 PST. **Role:** TMR-3 / PNP Time-Space Tradeoffs. **Named dependency:** C3-T5-TREE-ADHESION078, CLOSED for **adhesion-one** block-cut trees with bounded relative strong-two-covers; higher adhesion remains OPEN. **Status:** PROVED/EXACT RESTRICTED, independent review OPEN. Finite tests are COMPUTATIONAL; P versus NP OPEN.

## Candidate, falsifiers, and scope

**Candidate:** For a directed incidence graph with hubs and private three-parent sinks, discover the primal graph's biconnected blocks from the original input, assemble its block-articulation forest, and compute five-entry separator messages using small **relative** strong-two-covers of each block. The cut variables may recur in many pieces but must be assigned and summed **once**.

**Falsifiers:** (1) a sink triple crosses two blocks and is lost or multiplied twice; (2) an articulation hub is counted twice when adjacent blocks are composed; (3) a local cover leaves two free hubs in one triple, invalidating unary factorization; (4) discovery, head motions, failed searches, counting precision, or message caching is free; (5) the chain family still admits one globally bounded separator after which all local covers are bounded. Each has an explicit structural or computational control.

The target is the loopless tournament on Z5 with R(a,b) iff b-a is 1 or 3 modulo 5. Authenticate the original explicit directed graph on n vertices with m distinct arcs. Loops or opposed arcs force zero; duplicate identical arcs are idempotent. The recognized family consists of hubs of indegree zero (including isolated vertices) and private outdegree-zero sinks of indegree exactly three from distinct hubs. Every source sink remains a distinct counted variable even when its triple coincides with another sink's triple. Unsupported graphs or supported graphs failing the cover budget use the exact original-arc spanning-forest fallback, not a promise oracle.

A sink with hub colors a,b,c has exact marginalized weight
```
w(a,b,c) = sum_{z=0}^4 R(a,z) R(b,z) R(c,z).
```
Therefore Z(G)=sum_{x:H->Z5} product_{sinks e} w(x_e). The weight equals 2 for a singleton predecessor support, 1 for a compatible two-color support {u,u+2}, and zero otherwise. Only actual original sinks supply factors.

## Exact theorem: tree of overlapping adhesion-one interfaces

Form the undirected **primal graph** on hubs, joining any two hubs in the same source triple. Compute its biconnected edge-blocks and articulation vertices by a charged Tarjan DFS. Every three-hub source triple is a triangle in the primal graph and thus lies **entirely in one unique biconnected block**. Assign each original sink weight to that block, retaining multiplicity. The bipartite block-cut incidence graph is a forest. Root each tree at a block.

For a block B with parent articulation p (or no parent at a root), find C_B subset of B\{p}, |C_B|<=t, such that
```
|e intersect (C_B union {p})| >= 2
```
for every source triple e inside B. Here {p} is empty for root blocks. Discover covers by iterative deepening and branching over the deficient triple's remaining one or two slots. A budget-t search has at most O((t+1)3^t poly(N)) cost, including unsuccessful branches.

For each directed block-cut child subtree meeting B at articulation v, compute its **five-entry message** M_child(v,a) for each a in Z5. For a fixed parent color (if present) and local cover coloring gamma in Z5^C_B, each remaining block variable appears in at most one still-free position of every source triple. Thus its local triple weights and messages from all child subtrees are unary. Sum independently over its five colors; multiply these sums, the fully fixed triple weights, and the already-computed child-unary values of fixed cover vertices. Then sum over gamma. The result is M_B(p,a), or a scalar for a root. A child message **excludes** the parent articulation variable, so gluing at p never multiplies the variable count twice. Disjoint roots multiply, and primal-isolated original hubs contribute 5 each.

This recurrence sums each original hub assignment and sink assignment exactly once. If Z(G)>0, the source decision instance is satisfiable. It does not rely on any lower-bound hypothesis.

## SAME_REALIZATION resource envelope

Let N be binary source length and B the number of nontrivial biconnected primal blocks. For any fixed input cover budget t, on recognized sources for which every rooted block has a relative cover of size at most t, a single blank-start deterministic locally headed multitape machine implements the complete pipeline in the conservative simultaneous bounds

```
T(N) = O((N+1)^12 * [1 + B * ((t+1)*3^t + 5^(t+1))])
S_peak(N) = O((N+1)^4) writable bits.
```

N includes the graph source; each block message has five O(N)-bit integers. Parse and authenticate, discover every block and articulation, construct the exact rooted forest, branch for covers, evaluate all assignments, pay for graph/index/address/head accesses, exact integer arithmetic, retained messages/stack and full binary output in the same execution. Message multiplication and storage remain polynomial, since a subtree count is at most 5^n. We make no subpolynomial space claim. The Python reference uses recursion for Tarjan; a standard explicit DFS stack implements the claimed Turing machine bound.

The worst-case all-input algorithm also includes the always-correct fallback cost O(poly(N) 2^(n-c)), where c is the number of weak components, whenever family/cover recognition fails. The displayed faster bound is conditional on successful **source-discovered** recognition. For any fixed t it is polynomial on this subclass, independently of the number and depth of blocks. No claim is made of polynomial unrestricted T5 counting or general bounded-adhesion decomposition recognition.

## Infinite chain family escaping one-separator gluing

Introduce chain hubs a_0,...,a_r, two private hubs b_i,c_i per link i=0,...,r-1, and **three distinct sinks** for each link, with incoming hub triples
```
(a_i,b_i,a_(i+1)), (a_i,c_i,a_(i+1)), (b_i,c_i,a_(i+1)).
```
Each link's primal graph is K4; consecutive links intersect only at a_(i+1). Therefore there are r biconnected blocks arranged in a path. The full original graph has n=1+6r and m=9r. A root block needs a relative cover of at most three, while each nonroot block needs at most two beyond its parent articulation, so t=3 is uniform.

The triples (b_i,c_i,a_(i+1)) have pairwise disjoint hub sets, forcing every global strong-two-cover to have at least 2r hubs. A single separator hub can split the chain into at most two components and can contribute to at most one of these disjoint triples, so no fixed local cover budget t works in the preceding /077 one-separator theorem as r tends to infinity.

Writing M(u,v)=sum_{b,c in Z5}w(u,b,v)w(u,c,v)w(b,c,v), its 5x5 transfer matrix is circulant and has row sum 28 (verified directly). Hence

```
Z(G_r) = 1^T M^r 1 = 5 * 28^r.
```

At r=50, the original graph has n=301 and m=450, and its count is the 74-digit integer
```
11399126454007400982033240128771226250829462728238570616626484419357573120
```
produced directly by the block-tree solver. At r=120, n=721,m=1080, the solver again verifies the formula and returns a 175-digit count. These are easy-family countercontrols, not hardness evidence.

## Finite implementation audit

A self-contained CPython 3 standard-library implementation, `tmr3_t5_blocktree078.py`, revision `TMR3-T5-TREE-ADHESION078-v1`, seed 202611172327, was executed locally. Its main deterministic self-audit: **240 assertions, zero failures**, comprising 112 arbitrary small-digraph comparisons against the direct 5^n enumerator, 100 random triple-incidence comparisons with independent hub-color weighted enumeration, 16 chain-mode/formula checks, seven structural controls and five malformed-source rejections. Modes: 166 block-tree, 55 forest-fallback, six structural-zero. Sixteen additional exhaustive K4 triple-subset checks independently passed. An independent NetworkX biconnectivity computation on the ten-link chain agreed with the implemented Tarjan blocks. Larger chain tests r=1,2,3,10,50,120 all matched 5*28^r. The reported family and finite comparisons are COMPUTATIONAL; the restricted correctness assertion rests on the factorization and block-cut proof.

Local Python source SHA256: `22ff0ed09c679b5396ce720b9a832f17b4e166477d0e2d3abfd2fbdf8dbc6241`. Deterministic raw audit SHA256: `e577a60214ed9ddeea19aa0bb61c04c0c541c58e2948531c83cfb6f5981a58b9`.

## Four gates, easy controls and literature

DISJ: **PASS restricted**, a positive constructive algorithm only, no static-rank-to-work inference. Relativization: **NOT APPLICABLE WITH REASON**, no separation claimed and BGS/algebrization remain safeguards. Simultaneous DTISP: **PASS restricted** for the complete upper-bound execution; transfer to unrestricted SAT time-space lower bounds remains OPEN, lacking an authenticated explicit blowup. Configuration counting: **PASS as upper-bound consistency only**, not a machine lower bound. Retain bounded-treewidth, Horn/affine, degree-two, twin/module, Fourier, strong-cover, padding, selector, uniqueness, caching and recomputation controls. Old /341 remains FAIL as general UNSAT authority, /386 RESTRICTED.

Background graph decomposition: R. Tarjan, *Depth-First Search and Linear Graph Algorithms*, SIAM J. Comput. 1(2):146-160 (1972), DOI 10.1137/0201010. T5 decision is NP-complete by the fixed-template semicomplete digraph dichotomy: Bang-Jensen, Hell and MacGillivray, *The Complexity of Colouring by Semicomplete Digraphs*, SIAM J. Discrete Math. 1(3):281-298 (1988), DOI 10.1137/0401029. That classification alone provides no charged linear-blowup reduction or numeric SAT time-space exponent transfer. Full LaTeX compilation, native TM microcode, preflight and independent external proof review remain OPEN.

**Next load-bearing dependency:** C3-T5-ADHESION-TWO079: exact, source-discovered tree decomposition with **two shared hubs per interface**, supporting weighted 25-entry messages and local cover enumeration; obtain a complete discovery bound or an explicit interface counterexample. P versus NP remains OPEN.
