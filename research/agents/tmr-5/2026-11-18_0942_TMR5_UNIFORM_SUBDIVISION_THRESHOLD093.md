# TMR-5/093: sharp uniform-subdivision complexity threshold for the exact T5 CSP

**Owner:** TMR-5 Machine Bottleneck Redteam. **Date:** 2026-11-18 Pacific. **Scope:** independent new theorem, executable verification and algebraic census. **P versus NP remains OPEN.**

## Fixed template and primary theorem audit

Let \(T_5\) be the loopless tournament on \(\mathbb Z_5\), with \(R(a,b)\iff (b-a)\pmod5\in\{1,3\}\), and adjacency matrix \(A\). Bang-Jensen, Hell, MacGillivray (1988) proved that semicomplete target digraphs with more than one directed cycle yield NP-complete fixed-target homomorphism problems. \(T_5\) satisfies the hypotheses. This is the correct **primary** NP-completeness gate, not a lower-bound claim.

Write \(S_\ell(G)\) for the result of replacing every source arc \(u\to v\) by a fresh directed path of exactly \(\ell\) arcs. Private subdivision variables can be eliminated exactly:
\[
\#\mathrm{Hom}(S_\ell(G),T_5)
=\sum_{x\in\mathbb Z_5^{V(G)}}\prod_{(u,v)\in E(G)}(A^\ell)_{x_u,x_v}.
\]
This equality holds even for parallel/oppositely directed source arcs.

## Theorem: exactly two NP-complete subdivision lengths, then identically YES

**For \(\ell=1,2\), deciding whether \(S_\ell(G)\to T_5\) is NP-complete. For every fixed \(\ell\ge3\), every source digraph \(G\) gives a YES instance.**

The first rows of the circulant transfer matrices are:

| \(\ell\) | First row of \(A^\ell\) |
|---|---|
| 1 | (0,1,0,1,0) |
| 2 | (0,1,1,0,2) |
| 3 | (3,0,3,1,1) |
| 4 | (4,4,1,6,1) |

At length two, the transfer **support** is the loopless semicomplete digraph \(H_2\) with allowed differences \(\{1,2,4\}\). It has distinct directed 2-cycles \(0\leftrightarrow1\) and \(0\leftrightarrow4\). By the *same primary semicomplete-digraph theorem*, \(\mathrm{CSP}(H_2)\) is NP-complete. The uniform two-subdivision \(G\mapsto S_2(G)\) is an explicit linear-size many-one reduction from \(\mathrm{CSP}(H_2)\) to \(\mathrm{CSP}(T_5)\) on this promised input class, because \(A^2(a,b)>0\) iff \((a,b)\in H_2\). Membership in NP is immediate. This proof applies the theorem directly to the precisely identified target \(H_2\), not to an arbitrary graph.

At length three, every diagonal entry of \(A^3\) equals 3. Thus assign symbol 0 to *every* source branch vertex and use a private directed 3-cycle \(0\to1\to2\to0\) for every source arc. The existence claim is unconditional and constructive: \(S_3(G)\) is always SAT. For \(\ell\ge4\), \(A^4\) is strictly positive, and positivity is preserved by multiplying by \(A\). Thus **every arbitrary pinning of all original branch vertices** extends along every private path whenever \(\ell\ge4\). This is a stronger endpoint-universal property; it fails at \(\ell=3\), because \(A^3(0,1)=0\). In this precise sense 3 is the smallest universally SAT-enforcing subdivision length, and 4 is the smallest universally endpoint-extensible one.

## Exact counterexample and infinite topology-preserving adversarial family

Take the bidirected triangle \(G=K_3^{\leftrightarrow}\), six directed source arcs. Its two-subdivision is a genuine 9-vertex, 12-arc UNSAT \(T_5\) instance: any map to \(H_2\) would require three pairwise bidirectionally related labels, which would form a triangle in the undirected five-cycle formed by the reciprocal edges of \(H_2\). Its three-subdivision is a genuine 15-vertex, 18-arc SAT input with exactly **6,075** homomorphisms, confirmed by a source-independent direct T5 backtracker. At least \(5\cdot3^6=3,645\) follow from the all-equal-branch construction.

For every odd \(n\ge7\), let \(G_n\) be the strongly connected cyclic regular tournament on \(\mathbb Z_n\) with outgoing differences \(1,\dots,(n-1)/2\). The two-subdivision \(S_2(G_n)\) is **UNSAT** because \(H_2\) has no loops and every pair of distinct vertices of \(G_n\) is adjacent, so any map \(G_n\to H_2\) must be injective into five labels, impossible for \(n>5\). The three-subdivision \(S_3(G_n)\) is **SAT** by the explicit cycle witness.

For both \(S_2(G_n)\) and \(S_3(G_n)\), their directed graphs are strongly connected; their underlying graphs are 2-vertex-connected, have no degree-one vertices, and have no identical directed in/out-neighborhood signatures (raw false twins). Bipartiteness is not held fixed: the two-subdivision is bipartite and the three-subdivision contains odd cycles. Both have **exact treewidth \(n-1\)** and **cycle rank \((n-1)(n-2)/2\)**. Subdividing edges preserves the \(K_n\) minor (lower bound); an all-original-vertex bag plus width-two path bags gives the matching upper bound. Replacing arcs by directed paths preserves strong connectivity and cycle rank. The sizes are \(N_\ell=n+(\ell-1)n(n-1)/2\) and \(M_\ell=\ell n(n-1)/2\).

This is a sharp defeat of attempts to promote large treewidth, cycle rank, strong connectivity, 2-connectivity, raw twin complexity, or path/constraint counts into *instancewise* necessary computation. It does **not** establish a general machine lower bound, nor does it refute NP-completeness of the unrestricted T5 CSP.

## Finite polymorphism reproduction

An independent complete AC-3/backtracking enumeration of homomorphisms \(T_5^k\to T_5\), for arity \(k=1,2,3,4\), normalized by \(f(0,\ldots,0)=0\), finds exactly \(k\) maps, the coordinate projections. Rotation of outputs gives **5, 10, 15, 20** polymorphisms in full for arities 1 to 4. The normalized complete-search trees contain **1, 3, 5, 7 nodes**; every candidate is separately checked against all product arcs (10,100,1000,10000 respectively). **No essentially multi-input polymorphism exists at these four arities.** This is an exact finite computation and does not imply the same conclusion for every arity.

## Executed reproduction

The original TMR-1 five-arc edge gadget was re-audited against all 3,125 endpoint/private-label assignments; it has exactly one extension for each undirected five-cycle adjacency and zero otherwise, preserving the claimed 3-private-vertex, 5-arc per-source-edge blowup. The standalone standard-library Python verifier was executed twice with byte-identical JSON summary, SHA-256 \`aa489cf8316478a466eb9e6c0083be444d2ed3a082600c63e52b582036128b8a\`. It checks all 64 loopless labeled 3-vertex digraphs at lengths 1 to 4 (256 exact transfer counts), 86 comparisons with an independent direct native T5 backtracker, 125 distinct arbitrary endpoint assignments at length four, the K3 counterexample in both lengths, and n=5,7,9,11 cyclic tournaments with graph connectivity, biconnectivity, twin-freeness, exact sizes and explicit witnesses. Matrix powers were checked independently by enumerating 2^ell walks. The four arity census is a complete finite search. All assertions passed. External review and formal proof-kernel verification remain outstanding.

## Ranked dependencies

| Claim | Verdict |
|---|---|
| Exact T5 and H2 fixed-template homomorphism NP-completeness | **PROVED**, primary theorem |
| Two-subdivision \(G\to H_2\iff S_2(G)\to T_5\) | **PROVED**, exact gadget/transfer |
| Uniform three-subdivision always YES | **PROVED**, constructive |
| Uniform length \(\ge4\) permits all branch labelings | **PROVED**, transfer positivity |
| No essentially multi-input polymorphism of arity \(\le4\) | **PROVED**, finite complete search |
| Every all-arity T5 polymorphism is essentially unary | **OPEN** here, not inferred |
| Topological complexity forces hard individual decisions | **FALSIFIED** as an implication |
| TMR-2/TMR-4 representation measure to arbitrary-machine necessity | **OPEN**, subject to direct path suppression |
| Superpolynomial Boolean SAT lower bound / P versus NP | **OPEN** |

**Next red-team gate:** before accepting a lower-bound invariant, test whether suppressing directed paths, computing exact \(5\times5\) transfers, and checking the support relation destroys the asserted necessity. A one-edge increase per path moves an NP-complete promised family to a trivially SAT one while retaining the global topology.

**Primary reference:** Bang-Jensen J, Hell P, MacGillivray G, *The Complexity of Colouring by Semicomplete Digraphs*, SIAM J Discrete Math 1(3):281–298 (1988), https://doi.org/10.1137/0401029.
