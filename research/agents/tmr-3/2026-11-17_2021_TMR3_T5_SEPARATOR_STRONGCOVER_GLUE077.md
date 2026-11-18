# TMR-3/077: source-derived separator gluing of local strong-two-covers

**Date:** November 17, 2026, 20:21 PST. **Role:** TMR-3 / PNP Time-Space Tradeoffs. **Named dependency:** C3-T5-STRONG-COVER-GLUING077, CLOSED on the exact declared incidence family. **Status:** PROVED/EXACT RESTRICTED, independent mathematical review OPEN. Computational checks are finite. **P versus NP OPEN.**

## Candidate and three falsifiers, fixed before construction

Candidate: source-discovered hub separator S of size at most b, whose deletion leaves primal-hypergraph components, each admitting a relative strong 2-cover of size at most t, supports exact count in polynomial bit-work times the charged separator/cover enumeration, with polynomial simultaneous workspace.

Falsifiers: (1) an actual original sink has parents in two distinct post-separator components; (2) a chosen relative cover leaves two free parents in a triple, destroying unary factorization; (3) the algorithm implicitly assumes preloaded separator, component identification, or large tables, or fails to count distinct sinks with identical parent triples. All were addressed constructively, not by deleting legal source graphs.

## Model and complete source-to-output chain

The target T5 is the fixed 5-vertex tournament on Z/5Z, with (x,y) an arc iff y-x is 1 or 3 mod 5. The input is the full explicit original directed graph with n labeled vertices and m directed arcs, encoded in N bits. The parser validates every vertex index and arc. Duplicate identical arcs are semantically idempotent. An actual loop or two opposed arcs force zero; these are exact original-graph semantics.

The recognized family has hubs (all vertices with indegree zero, including isolated vertices) and private sinks (positive indegree exactly three, outdegree zero, three distinct hub parents). Every original sink remains an independent counted variable, even when multiple sinks have the same three parents. Inputs outside this family are passed to the exact original-arc forest-difference counter rather than to an assumed promise oracle.

For an actual private sink with parent colors a,b,c, write
```
w(a,b,c) = sum_{z in Z5} R(a,z) R(b,z) R(c,z).
```
Its values are exactly 2 when all parents are equal, 1 when the parent support is a pair {u,u+2} mod 5, and 0 otherwise. Thus the full original graph's exact count equals the sum over all hub colorings of the product of one w factor **per original sink**. This reduction is an exact summation over actual original variables, not a replacement of the original decision problem.

For the triple-hypergraph on hub set H, let S be any subset. Construct the connected components B_1,...,B_r of the primal graph on H\S, where vertices sharing a triple are adjacent. Hence each actual triple is either contained in S or has all its non-S parents in exactly one B_i. For each i, choose a **relative strong 2-cover** C_i subset B_i, satisfying
```
|e intersect (S union C_i)| >= 2     for every triple e meeting B_i.
```
A complete source-derived search tries all S of sizes 0,...,b; for each, it extracts components and finds each C_i by iterative-depth branching on an offending triple. If deficit 1, branch on either remaining vertex; if deficit 2, branch on one of at most three pairs. The exhaustive search is paid, and does not use a provided decomposition witness.

For a fixed boundary assignment sigma in Z5^S and fixed local cover assignment gamma in Z5^C_i, every remaining triple contains **at most one** unassigned interior hub. The local sum factors exactly:
```
M_i(sigma) =
    sum_{gamma in Z5^C_i}
      [product_{e contained in S union C_i} w_e(sigma,gamma)]
      * product_{v in B_i \ C_i}
           [sum_{a in Z5} product_{e: e\(S union C_i)={v}}
                                      w_e(sigma,gamma,v=a)].
```
Empty products equal one, so isolated original hubs contribute 5. The complete answer is
```
Z(G)= sum_{sigma in Z5^S}
            [product_{e contained in S} w_e(sigma)]
            * product_{i=1}^r M_i(sigma).
```
Every global hub assignment appears in exactly one tuple (sigma, gamma_1, free_1,...,gamma_r, free_r). Multiplication over components is legitimate after sigma is fixed, and summing independent private-sink colors yields exactly the original graph's count. All additions and products are exact integers. Hence Z(G)>0 iff the original source is satisfiable.

## Simultaneous actual-machine resource ledger

Put h=|H| and B(h,b)=sum_{j=0}^{min(b,h)} binom(h,j). For given nonnegative integer budgets b,t, on every recognized graph that admits such a decomposition, one fixed, blank-start locally headed deterministic multitape implementation achieves the conservative bounds
```
T(N) = O((N+1)^12 [1 + B(h,b) (t+1) 3^t + r 5^(b+t)]),
S_peak(N) = O((N+1)^4) writable bits.
```
Here the same actual execution performs parsing, source authentication, repeated separator trials, all failed cover branches, component discovery, table-free online enumeration, five-color edge-weight evaluation, graph/index/head/address operations, exact O(N)-bit integer arithmetic, retained color/cover stacks, and full binary count output. The machine streams one separator assignment at a time and one cover assignment at a time; it never stores a 5^b table. No physical checkpoint, oracle or preloaded certificate is hidden in the polynomial workspace. The exponent 12 is a deliberately loose physical bit-machine upper envelope, not an optimized runtime.

If no recognized decomposition satisfies the supplied budgets, the search is still fully charged and a correct all-input forest-difference counter computes the exact original answer in additional O(poly(N) 2^(n-c)) time, polynomial space, with c weak components. For b=1,t=2, both the exhaustive discovery cost and the successful evaluation cost are polynomial in N.

**Not an FPT claim in b:** enumerating B(h,b) separators costs approximately h^b for variable b. The construction is polynomial for fixed b,t; describing it as f(b)poly(N) would be false without a new separator-finding algorithm.

## Infinite family with unbounded global cover

For every r>=1, introduce a central hub a and, for each i=1,...,r, distinct hubs b_i,c_i,v_i and three distinct private sinks with parent triples
```
(a,b_i,v_i), (a,c_i,v_i), (b_i,c_i,v_i).
```
The full original directed graph has n=1+6r vertices and m=9r arcs, and is connected. Its triple-primal graph becomes r components after deleting just S={a}. Each local C_i={b_i,c_i} is a relative strong 2-cover. Nevertheless its **global** strong 2-cover number is exactly 1+2r: when a is chosen, the third triple forces at least two among b_i,c_i,v_i in each block; when a is not chosen, the first two triples force all three of b_i,c_i,v_i. Therefore the previous global 5^tau2 enumeration requires exponential r-dependence in its stated bound, while separator-gluing is polynomial.

For any fixed a-color the three sinks of block i contribute
```
M(a)=sum_{b,c,v in Z5} w(a,b,v)w(a,c,v)w(b,c,v)=28.
```
A direct five-state enumeration gives one product-8 assignment, six product-2 assignments, eight product-1 assignments, and 110 zero assignments, independent of a by cyclic symmetry; the sum is 8+12+8=28. It follows exactly that
```
Z(G_r)=5*28^r.
```
For r=40, n=241,m=360, and Z=38484979364170447062492137914782951187182927182409110650880 (59 decimal digits). This example is a positive easy-family control, not a lower bound for arbitrary T5 CSP.

## Finite evidence and reproducibility scope

The full local CPython 3 standard-library reference source is `tmr3_t5_separator_glue077.py`, revision `tmr3-t5-separator-glue077-v1`, seed 202611172021, SHA256 `50aad4cd6f4036dc0a3282791b86fadedc5ab62435064dd3976d0cd9bfa7da40`. Its raw JSON is SHA256 `80c87a47e72303287b83296cfc70d086df96d497535181d1b0c6f5435c4bcd9e`. A fresh second local execution was byte-identical. **341 actual assertions, zero failures**: 98 independent original five-color brute comparisons on small arbitrary digraphs; six additional structural cases; 27 family formula and decomposition assertions; 80 independently evaluated random triple-incidence graphs; 125 exact W checks; four malformed-input rejections; one 40-block high-parameter exact check. The published research conclusion is a separate symbolic proof, not induction from these tests. Neither native multitape microcode nor full LaTeX build nor independent mathematical peer review was executed. This connector-only environment has no local repository checkout, so the preflight script was not run.

## Four mandatory gates, literature and restrictions

DISJ sanity: **PASS restricted**: this is a positive source-derived exact counter; no static rank or representation lower bound is interpreted as necessary work. Relativization: **NOT APPLICABLE WITH REASON** to a separation, because none is claimed; BGS, algebrization and Natural Proofs remain guards for any future lower-bound transfer. Simultaneous DTISP: **PASS restricted** for one complete sequential deterministic run including all source and output costs; arbitrary-machine forbidden-region or SAT transfer **OPEN**. Deterministic configuration counting: **PASS only as upper-bound consistency**, never as lower bound or randomized/quantum claim.

All competing easy-family algorithms (bounded treewidth, affine/linear algebra, degree-two suppression, twin and module quotients, all product and padding tricks, selector/unique-solution, actual caching/recomputation) remain allowed. This decomposition is related to standard separator/treewidth dynamic programming; it is not represented as a new general complexity-class result. The historical checker /341 remains FAIL as a full UNSAT authority and /386 remains RESTRICTED.

General T5 decision is NP-complete by Bang-Jensen, Hell and MacGillivray, *The Complexity of Colouring by Semicomplete Digraphs*, SIAM J. Discrete Math. 1(3), 281-298 (1988), DOI 10.1137/0401029. T5 is a tournament with more than one directed 3-cycle, so the original dichotomy applies. Its classification does not itself give a known sparse 3-SAT reduction blowup suitable for a numerical time-space exponent transfer.

**ONE next load-bearing lemma:** C3-T5-TREE-ADHESION078: construct and charge a source-derived tree of overlapping separator pieces with bounded complete interfaces and local relative covers, without assuming an expensive decomposition or silently counting a shared hub multiple times. Seek a family beyond fixed global separators; either supply a complete weighted-message proof and uniform discovery cost or a counterexample to the interface. **P versus NP remains OPEN.**
