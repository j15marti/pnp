# TMR-2/074 | 2026-11-17 19:12 PST | Authenticated three-separator orbit counting with unbounded treewidth

**Identity:** TMR-2 / PNP Information Necessity. **Primary object:** original-label exact counting for the five-symbol tournament CSP, \(R(a,b)=[(b-a)\bmod5\in\{1,3\}]\). **Status:** PROVED/EXACT for the stated restricted symbolic construction; external independent mathematical review OPEN. Finite execution COMPUTATIONAL. P versus NP OPEN.

## 1. Chosen dependency, candidate and falsifiers (specified before the corpus and primary-source review)

Target the **D2-T5-AUTHENTIC-IRREDUCIBLE-3SEPARATOR-OBSTRUCTION** dependency following TMR-2/073. The candidate is a *countercontrol*: even connected, triangle-free, exactly 3-vertex-connected T5 source graphs of unbounded minimum degree, unbounded treewidth, unbounded vertex cover and feedback rank can have a fully source-recognizable polynomial-time exact count. More strongly, equal-size authentic sources can have mixed YES/NO answers without a directed two-cycle. This refutes any necessary-work arrow relying on those graph parameters together, but cannot refute a theorem that has stronger explicit hypotheses.

Four prospective falsifiers were (F1) loss of original-label multiplicity in eliminating the private source/sink vertices; (F2) a recognizer that tacitly receives terminals, block sizes, vertex names, or a decomposition oracle; (F3) a hidden 1-/2-separator, low-degree source, triangle or bounded-treewidth route in the *base* graphs; and (F4) a mixed NO control obtained merely by inserting a contradictory directed two-cycle. The exact proof and executed audit resolve F1--F4 for the declared source family. A universal decision lower bound remains OPEN.

**Complete same-source chain:** canonical explicit ASCII graph bytes -> parse and authenticate all original vertices and arcs -> discover pure sinks, three shared terminals and complete private bipartite blocks from the actual incidence table -> certify every expected and every extra arc -> build the 25 relative-color cofactor coordinates (at most seven nonzero before optional terminal arcs) -> multiply independent block completion integers -> check actual terminal arcs -> sum root rotations, emit exact count and verify an original five-label witness on YES -> return exact decision. Invalid source is INVALID; valid nonmembers use correct original-label exhaustive enumeration. No supplied structural descriptor, source class promise on arbitrary inputs, graph isomorphism oracle or auxiliary-variable normalization is used.

## 2. The exact family

For every pair of integers \(h\ge4\) and \(b\ge2\), take three shared original vertices \(s,t,u\). For each \(i=1,\ldots,b\), introduce \(h-3\) private source vertices \(P_i\) and \(h\) private sink vertices \(Q_i\), and add all genuine T5 arcs
\[
(v,w)\qquad(v\in\{s,t,u\}\cup P_i,\quad w\in Q_i).
\]
There are no other arcs in the *base* graph \(B_{h,b}\). The blocks are oriented \(K_{h,h}\)'s, intersecting exactly in the three original source-side terminals. Counts:
\[
n=3+b(2h-3),\quad m=bh^2,\quad
\beta=m-n+1=b(h^2-2h+3)-2.
\]
The base graph has minimum undirected degree \(h\), no triangles, and vertex connectivity exactly 3. Indeed, every \(K_{h,h}\) is \(h\)-vertex-connected, all blocks retain at least one shared terminal after any removal of at most two vertices, and removal of all three terminals disconnects the \(b\) private blocks. Its treewidth is exactly \(h\): it contains \(K_{h,h}\), while each block has a tree decomposition with every bag containing all \(h\) source-side vertices and one sink, with width \(h\); these block decompositions join at bags that already contain the three terminals. The minimum vertex-cover size is \(3+b(h-3)\): all source-side vertices form such a cover, and a matching saturates them (assign three terminals to three sinks in block 1, each private source to a distinct remaining block sink). These are actual source parameters before any optional terminal arcs, not claims that they force hard computation.

Define mixed same-size variants with exactly two additional *original* terminal arcs, without opposite pairs. The YES variant adds \(s\to t\) and \(s\to u\). The NO variant adds \(s\to t\) and \(t\to u\). Both source digraphs are acyclic and have exactly \(bh^2+2\) arcs. These extra arcs create undirected triangles; the triangle-free assertion applies ONLY to the base graph. The terminal arcs do not decrease minimum degree or vertex-connectivity and remain inside width-\(h\) bags, so treewidth remains \(h\).

## 3. Complete integer three-terminal cofactor theorem

For fixed original terminal colors \(a,b,c\in\mathbb Z_5\), one private block has the exact extension count
\[
F_h(a,b,c)=\sum_{y\in\mathbb Z_5^{h-3}}
\bigl|\operatorname{Out}(a)\cap\operatorname{Out}(b)\cap\operatorname{Out}(c)
       \cap\bigcap_{z\in y}\operatorname{Out}(z)\bigr|^{h},
\quad
\operatorname{Out}(z)=\{z+1,z+3\}.
\]
Each independent private sink has precisely the number of allowed labels inside the intersection; the power \(h\) counts all \(h\) *original* sink assignments separately. Each of the \(h-3\) private source variables is also summed independently. No existential projection is substituted for an exact count.

Let
\[
A_h=2^h+2(2^{h-3}-1),\qquad B_h=2^{h-3}.
\]
There are exactly three cases. If \(a=b=c\), both possible sink labels are common; the all-equal private-source assignment contributes \(2^h\), and the two disjoint nonconstant private-source subcubes contribute \(2(2^{h-3}-1)\), so \(F_h=A_h\). If the terminals use exactly two colors separated by \(\pm2\bmod5\), they have exactly one common outneighbor and every private source has two allowable labels, giving \(F_h=B_h\). In all other cases there is no common outneighbor and \(F_h=0\). There are 5 all-equal terminal assignments and 30 mixed two-color assignments, i.e. 5 times six nonzero relative-color coordinates. Simultaneous label rotation leaves \(F_h\) invariant, reducing 125 absolute terminal tuples to the 25 pairs \((b-a,c-a)\), of which seven survive. This is an exact dynamic tensor under authentic source transitions, not a rank-to-work assertion.

Private blocks are vertex-disjoint conditional on \((s,t,u)\). Their exact multiplicities therefore multiply, and the final root-terminal sum gives
\[
\boxed{Z(B_{h,b})=5\bigl(A_h^b+6B_h^b\bigr).}
\]
With one terminal arc \(s\to t\), precisely two of the six two-color relative coordinates survive, giving \(Z=10B_h^b\). With the two out-star arcs \(s\to t,s\to u\), precisely one survives, giving
\[
\boxed{Z(B_{h,b}^{\rm YES})=5B_h^b.}
\]
With the directed path \(s\to t\to u\), no terminal tuple belongs to the transfer support, hence
\[
\boxed{Z(B_{h,b}^{\rm NO})=0.}
\]
The NO variant contains no opposite directed arc: the zero follows from the actual five-label cofactor, not a syntactic two-cycle. The graph is still a DAG and cannot be solved merely by directed-cycle detection. However a source-aware fast recognizer can distinguish both versions; **mixed answers plus high treewidth do not imply hard SAT decisions**.

## 4. Uniform source authentication, realization and resource partition

Use the repaired /068 canonical ASCII grammar: header \`p t5 n m\`, explicit lines \`v 0\` through \`v (n-1)\`, and lexicographically sorted distinct \`a u v\` arcs, with canonical decimal indices and final newline. Every vertex and arc is explicitly present, hence \(n,m\le L\), the full encoded length. A loop is a syntactically valid unsatisfiable constraint; a duplicate arc is INVALID under this grammar.

The recognizer constructs the real inbound/outbound incidence sets. It finds all vertices of zero outdegree as private-sink candidates, discovers \(h\) as their common indegree, checks \(h\ge4\) and a total of \(bh\) sinks for \(b\ge2\), then identifies **exactly three terminals** by outbound adjacency to *every* sink. Each other source must have exactly \(h\) sink neighbors. Group these source vertices by their *actual* sink-neighbor set; demand precisely \(b\) disjoint \(h\)-element sink sets, exactly \(h-3\) private source vertices for each, and full coverage of every input vertex. The recognizer regenerates all \(bh^2\) required arcs from this discovered partition, checks their presence and rejects any surplus except genuine arcs with both ends among the three terminals. It does not rely on the numerical values of vertex names, a supplied \(h,b\) index, or a separation oracle. Arbitrary source-vertex relabelings preserve acceptance.

For every recognized source, construct \(F_h\) from the proved closed form, evaluate the 125 terminal-label choices (or 25 rotation coordinates), apply all actual terminal arcs, use exact integer exponentiation/multiplication and return the exact original-variable count. For a positive cofactor, choose the first terminal tuple with a common outneighbor, assign every private source its root terminal color and every block's sinks one such common outneighbor; verify every original arc. For an unrecognized but valid source use an iterative depth-first original five-label search with early arc checks, making the overall algorithm total and correct, but potentially exponential. Unrecognized cases are **not** in the polynomial-time promise.

One standard locally headed blank-start deterministic multitape bit-machine implements the recognized branch with deliberately conservative **simultaneous** bounds
\[
T_{\rm fast}(L)=O((L+1)^9),\qquad
S_{\rm peak,fast}(L)=O((L+1)^4).
\]
This is not a machine lower bound. Its time partition charges initial byte inspection and parser validation, full source re-reads, adjacency construction, sink and terminal discovery, failed candidates and grouping, full arc-set authentication, constant-size 25/125-cofactor enumeration, integer exponentiation with output precision \(O(n)\) bits, witness construction, original-arc verification, switching and final output. The same execution retains at most polynomial-size source/incidence arrays, group tables, cofactor entries, big-integer work buffers, head positions, indices, caches and witness. Shared vertices are represented once, not duplicated into each block. Alternative DP, bounded-width decomposition, source-orbit symmetry, direct witness checks, caching and recomputation remain legal, including cheaper source-aware solvers.

Even as \(h\to\infty\) and \(b\to\infty\), the input length is \(\Theta(bh^2\log(bh))\), while the output requires \(O(n)\) bits. Thus the recognized polynomial bound does not rely on suppressing large integer coefficients or an implicit exponentially concise source. The generic fallback has \(5^n\operatorname{poly}(L)\) time and polynomial peak workspace, not a polynomial all-input consequence.

## 5. Dynamic invariant for TMR-4

**D2-T5-THREESEPARATOR-ORBIT-TRACE** state fields: SOURCE_BYTES, CANONICAL_VERTICES_AND_ARCS, IN/OUT_INCIDENCE, SINK_SET, DISCOVERED_H_B, THREE_TERMINALS, PRIVATE_SOURCE_CLASSES, SINK_BLOCKS, EXPECTED_AND_EXTRA_ARCS, LIVE_25_RELATIVE_COFATORS, ROOT_ROTATIONS, ORIGINAL_SOURCE_AND_SINK_MULTIPLICITY, INTEGER_PRECISION, OPTIONAL_TERMINAL_TESTS, CERTIFIED_WITNESS, CACHE, SWITCH_FALLBACK, OUTPUT.

Its complete paid interface is READ/PARSE/REJECT, BUILD_INCIDENCE, FIND_SINKS/H, FIND_TERMINALS, GROUP_PRIVATE_SOURCES, CERTIFY_ALL_ARCS, BUILD_25_ORBIT_TENSOR, MULTIPLY_INDEPENDENT_BLOCKS, APPLY_REAL_TERMINAL_ARCS, SUM_ROTATIONS, BIGINT_ARITHMETIC, WITNESS/VERIFY, SWITCH_TO_EXHAUSTIVE, CACHE/DROP/RECOMPUTE and OUTPUT. A TMR-4 transfer must cover *each* actually executed transition, including work and aggregate live space in the same run, and must not posit that arbitrary source deciders execute this pipeline.

## 6. Hostile controls and four gates

DISJ sanity **PASS restricted:** no inference from matrix/cofactor rank or graph width to general circuit or decision cost; the shortcut itself is a control against such inference. Relativization **PASS for elementary local counting / OPEN for unrestricted P-versus-NP transfer**: no nonrelativizing step is supplied, retaining Baker--Gill--Solovay, algebrization and Natural Proofs barriers. Simultaneous DTISP **PASS for a single recognized-instance upper-bound machine / NOT APPLICABLE to any forbidden time-space lower conclusion**. Deterministic configuration counting **PASS as an upper-bound consistency check only**, \(T\le2^{O(S+\log L)}\) for the fixed total deterministic model; it is never construed as a necessary-work lower bound or automatic randomized/quantum statement.

The construction explicitly preserves legitimate DISJ, Horn, 2-SAT, affine/Gaussian, equality, autarky, products, padding/auxiliaries, unique selectors, unique-solution rank-one, low treewidth, source-directed twins/false twins, semicomplete modules, vector/characteristic changes, compact circuits, exact-degree elimination, branch ordering and recomputation controls. The base graph has abundant structural regularity and is source-recognizable; it **must not** be called an irreducible SAT-hard family. The existing /341 authority remains FAIL for full UNSAT, /386 remains RESTRICTED. The targeted irreducibility condition survives degree-at-most-two peeling and one/two-vertex separators but fails at the three-terminal separator and source recognizer, which is precisely this countercontrol's content.

## 7. Evidence, provenance and independent-review status

Exact executed CPython stdlib source:
\`experiments/tmr/tmr2_t5_three_separator074.py\`, revision \`tmr2-t5-3sep074-py.v1\`, seed 202611171912, source SHA256 \`370aea7c8cc6c6683e5906cbb91d0f1102ab10eb7a8669c5b01f32aeb7e2abfc\`, Git blob \`838aff1a687a7b8968e05b81dafeb00bfa5d2be6\`.
Immutable executed raw:
\`results/raw/tmr/2026-11-17_1912_TMR2_T5_3SEP074_PY_RAW.json\`, SHA256 \`7dc58bff23ef56c54e7c630d8570f1a623edfdfa5f6b42e95c103ed6a49c0387\`, Git blob \`fa2b7b6cb402c2cf8e244f06e71dc9b01f930c3b\`.

Final local execution performed **348 exact assertions, 35 family cases, zero failures**, including the 25 relative coordinates for \(h=4,\ldots,9\), independent explicit block enumeration for \(h\le7\), independent direct source-side exact enumeration for small instances, complete original five-color backtracking for three 13-vertex cases, randomized full-graph vertex renamings, actual source/malformed rejection and mixed YES/NO controls. The initial negative-test development failed because an allegedly surplus edge was already a valid block edge; that test was corrected to a genuine reversed sink-to-source edge before the final zero-failure audit. Do not count the failed development run as a successful result. A wall-clock 1.95-second final local audit executed, not a physical multitape Turing-machine replay.

Manuscript \`main2_PNP_INFORMATION_NECESSITY.tex\` updated in place only on proof-verified publication. No independent mathematical referee, physical TM microtrace, Lean kernel rebuild or repository checkout/preflight was performed. Full LaTeX compilation is separately disclosed if executed. This report does not assert novelty of standard separator dynamic programming, graph treewidth facts or the fixed-template CSP NP-hardness theorem.

**ONE next load-bearing lemma (OPEN):** **D2-T5-QUOTIENT-PRIME-ADAPTIVE-DECISION-BARRIER.** Seek authentic mixed YES/NO sources that survive *charged* 1-/2-/3-separator discovery, complete bipartite block recognition, low-degree peeling, forced-triad quotient, directed-twin/module reduction, easy exact transfer and source-derived witnesses. Then specify a restricted adaptive evaluator in which an actual lower bound can be proved, without suppressing alternative source-aware algorithms. P versus NP remains OPEN.

## Original sources and project evidence

[1] Bang-Jensen, Hell and MacGillivray, *The Complexity of Colouring by Semicomplete Digraphs*, SIAM J. Discrete Math. 1 (1988), 281--298. https://doi.org/10.1137/0401029 . Imported NP-completeness is background only.

[2] Focke, Marx and Rzążewski, *Counting List Homomorphisms from Graphs of Bounded Treewidth: Tight Complexity Bounds*, ACM Trans. Algorithms 20 (2024). https://doi.org/10.1145/3640814 . Standard bounded-treewidth counting context; no specific lower bound imported.

[3] TMR-2/073 original source, report and raw: \`experiments/tmr/tmr2_t5_two_separator073.js\`, \`research/agents/tmr-2/2026-11-17_1850_TMR2_T5_TWO_TERMINAL_ORBIT073.md\`, \`results/raw/tmr/2026-11-17_1850_TMR2_T5_TWO_SEPARATOR073_JS_RAW.json\`.

[4] Current issue #3 peer developments: TMR-4/075--076 directed twins and semicomplete-module shortcuts (unmerged draft PR #240/#242), TMR-1/077--078 signed-SAT high-treewidth/directed-acyclic hardness (draft PR #197), TMR-5/077 cyclic-polymorphism barrier (draft PR #209), LSPV-5 COREPEEL1 and VCCORE1 main reports. Their source-aware shortcuts remain live alternatives; this construction is not claimed to subsume them.
