# CROSS-TRACK SYNTHESIS 70 | 2026-11-18 13:35 PST
**New restricted theorem:** Degree-five, directed-path-depth-three T5-DAG compiler with parsimonious solution bijection and exact canonical one-hot CNF retraction. All unrestricted algorithmic lower-bound arrows and P versus NP remain **OPEN**. Independent external referee/physical TM replay outstanding.

## Proposed before search (frozen and SHA-audited locally)
1. Reverse Resolution transport for fixed gadgets and its potential counterexamples.
2. Fully charged source-aware resource contraction and easy structured controls.
3. Same-original-input UWI admitting adaptive derived-query deciders and a common clock.
4. Necessary nonrelativizing WRAPPER hinge, not ordinary relativizing self-reduction.

## Latest substantive specialist outputs actually read
Resource Contraction TMR-1/096: https://github.com/j15marti/pnp/blob/tmr1-20261115-independent-lean060/research/agents/tmr-1/2026-11-18_1200_TMR1_PARSIMONIOUS_DAG_FLATTEN096.md .
Resource Contraction TMR-3/091: https://github.com/j15marti/pnp/pull/299 ; previous /090 https://github.com/j15marti/pnp/blob/research/tmr3-t5-block-cut090-20261118/research/agents/tmr-3/2026-11-18_1121_TMR3_T5_BLOCK_CUT_FACTOR090.md .
Nonrelativizing Simulation LSPV-5 SKETCHCRT1 (12:06 PST): https://github.com/j15marti/pnp/blob/main/research/main/2026-11-18_1206_MAIN_LSPV5_SKETCHCRT1_CONDENSED.tex .
Universal Obstruction TMR-2/091 (12:12 PST): https://github.com/j15marti/pnp/blob/main/research/agents/tmr-2/2026-11-18_1212_TMR2_T5_BICYCLIC_TRANSFER091.md .
Proof Transport TMR-4/093: https://github.com/j15marti/pnp/pull/300 ; cross-track predecessor /069 https://github.com/j15marti/pnp/blob/main/research/agents/cross-track/2026-11-18_1231_T5_DAG_RESOLUTION_BIDIRECTIONAL69_STATUS.md .
Also searched newest GitHub commits, issue #3 handoffs, project conversations, Library circuit audit, older Google Drive WORKSAT transport, and original research (Bang-Jensen/Hell/MacGillivray, Atserias/Dalmau, Ben-Sasson/Wigderson, Baker/Gill/Solovay).

## Theorem 70-A: explicit linear-size parsimonious bounded-degree four-layer compiler
Fix R(a,b) iff (b-a) mod 5 is 1 or 3. For every source arc e=(u,v), create separate occurrence-clones P_e (layer 0), Q_e (layer 1), and one cross arc P_e -> Q_e. For each original vertex v, list all occurrence-clones at v (loop tails and heads distinct). Between every consecutive pair s,t, put a fresh equality gadget with internal a (layer 2) and b (layer 3):
s->a, s->b, t->a, t->b, a->b.
Keep isolated source vertices as isolated target vertices.

The exact two-terminal cofactor is E(x,y)=1 iff x=y, 0 otherwise, with unique auxiliaries (a,b)=(x+3,x+1) mod 5 for x=y. Every original satisfying assignment therefore extends uniquely and every expanded satisfying assignment projects to an original one: #Hom(C5(G),T5)=#Hom(G,T5).

For n source vertices, m arcs, k nonisolated vertices and i=n-k, there are 2m-k equality links and
N=6m-2k+i <= n+6m; M=11m-5k <=11m.
Every arc strictly increases its 0/1/2/3 layer, hence the graph is a loop-free directed DAG of maximum directed path length 3. Any occurrence-clone participates in at most two equality gadgets (4 incidences) and one cross arc (1 incidence): underlying undirected TOTAL degree <=5; each internal gadget vertex has degree 3. The transformation handles loops, opposed arcs, isolates, and the empty input. A malformed encoding maps to the fixed four-node six-edge contradictory equality-plus-cross-arc DAG. Source scanning, incidence construction, output, sorting, bit serialization, workspace and memory are fully charged to a uniform polynomial algorithm, with O(n+m) graph-record size. This is an exact restricted NP-completeness-preserving construction, not an unrestricted time lower bound.

## Theorem 70-B: exact Boolean retraction
Use five one-hot atoms per vertex: one at-least-one clause, ten at-most-one clauses, and 15 forbidden color-pair clauses per arc. Map each clone atom to the original vertex's corresponding color atom; internal a-c maps to original color c-3, internal b-c to c-1. Identity on isolates. Duplicate literals/clauses collapsed. Each internal gadget arc's forbidden pair becomes an original at-most-one clause, each cross arc becomes an original constraint clause, and vertex clauses map onto all original one-hot axioms. Thus **sigma(F_C)=F_G as exact clause sets**, including loops, opposed arcs and empty sources. Independent ordinary Resolution+weakening normalization/tautology handling for arbitrary proof files on this multi-clone compiler is not yet kernel-certified. The /069 reverse-transport proof offers a restricted path; no arbitrary-decider lower-bound transport follows.

## Theorem 70-C: conditional same-input witness extraction
If an algorithm decided ALL T5 CSP instances in the degree<=5, depth<=3, four-layer DAG class in polynomial time, C5 would decide unrestricted T5 in polynomial time. Use constant-size relative-color pin gadgets from synthesis /062, recompile every adaptive query with C5, and normalize one root per weak source component. For n original vertices and c weak components, witness recovery on the **identical original source G** makes at most 1+4(n-c) restricted-decider calls, including polynomial-generation, arithmetic, workspace, witness translation and verification. The candidate decider can query *derived* graphs, while the final witness belongs to the same original input. This is a conditional, relativizing reduction; it is not a discovered fast decider or a necessary nonrelativizing WRAPPER hinge.

## Hostile audit
Dependency-free Python: 25 exact equality cofactors; ALL 531 labeled source graphs on 0..3 vertices including loops/opposed arcs, with source brute-force counts versus independently implemented general compiled-target MAC counts; 100 further random 4..7 vertex inputs; exact graph layer/degree/depth/N/M/unique-arc checks; exact canonical Boolean CNF retraction checked on each; 48 adaptive compiled-query witness-extractor cases, 73 restricted decider calls. Also independently compiled TMR-3/091 high-degree-but-easy two-terminal bouquet (20 copies of K_{8,8}) to **7116 vertices and 12670 arcs** with max degree 5 and depth 3; exact source count 21889571624213873501580872626770891539924037418352640. The large compiled graph's exact count was *not* directly enumerated.
**534,623 assertions, 0 failures.** Finite experiments do not imply an unrestricted time lower bound.
Executed local audit SHA256 bb8c11711b10f3b3d4756bdfb4dd3e4963646e86916c76af108e655cd17c34c8 .
Raw results SHA256 962cad7f083cf76d8b423bd614ddd0d4d71d5a821debd8c2cbd2a7d536bece34 .
Extended full local report SHA256 742a65f5ff30b286ad2a1100da296c2a707093ae7caa6c4bf76486843802efca .
Presearch proposals SHA256 8093a14432ea1963cc4be8a398f1586639702e5af9ccde3dcd58794557c806d6 .

## Explicit proof DAG
- ESTABLISHED: general T5-HOM NP-complete (Bang-Jensen/Hell/MacGillivray 1988).
- PROVED 70-A: bounded-total-degree-five, four-layer, path-depth-three DAG parsimony; hence its fixed-template decision remains NP-complete.
- PROVED 70-B: exact canonical five-onehot Boolean clause-set substitution.
- PROVED CONDITIONAL 70-C: polynomial-time promise decision -> unrestricted original-input T5 witness-search in FP.
- CONDITIONAL/UNCHECKED: ordinary Resolution+weakening proof-file translation for multi-clone compiler; all-proof checker pending.
- OPEN: universal arbitrary-decider-to-Resolution/OBDD transport; charged unrestricted hereditary resource contraction; nonrelativizing WRAPPER hinge; common-clock same-input UWI; superpolynomial T5 time lower bound; P vs NP.

## Four specialist assignments
1. Resource Contraction (TMR-1/3): fully charge inverse recognition of *unlabeled* outputs and adversarial source-aware 2-connected bouquet, cofactor and block-cut shortcuts, accounting for parsing, memory, arithmetic and recursion.
2. Nonrelativizing Simulation (LSPV-5): identify one necessary WRAPPER operation surviving C5 and relativizing adaptive query self-reduction; otherwise leave hinge OPEN.
3. Universal Obstruction (TMR-2): quantify all eligible algorithms on one final source graph/common clock, including C5-derived queries, and investigate mixed higher-cycle-rank/high-girth sources; C5 itself does **not** preserve high girth.
4. Proof Transport (TMR-4): kernel-check sigma(F_C)=F_G and construct a complete ordinary Resolution+weakening translator for multi-clone proofs, handling collapsed pivots/tautologies; do not infer unrestricted time hardness.

References: Bang-Jensen/Hell/MacGillivray 1988 https://doi.org/10.1137/0401029 ; Atserias/Dalmau 2008 https://doi.org/10.1016/j.jcss.2007.06.025 ; Ben-Sasson/Wigderson 2001 https://doi.org/10.1145/375827.375835 ; Baker/Gill/Solovay 1975 https://doi.org/10.1137/0204037 .
**P versus NP remains OPEN. No specialist agents, schedules, manuscripts, or root trackers were changed.**