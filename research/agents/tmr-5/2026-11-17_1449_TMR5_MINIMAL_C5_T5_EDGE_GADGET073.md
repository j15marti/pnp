# TMR-5/073: optimal unpinned single-edge C5-to-T5 gadget resources

2026-11-17 14:49 PST, TMR-5 / PNP Machine Bottleneck Redteam. Governing five-symbol CSP directive (November 17) and November 15 end-to-end/agent-owned-manuscript protocol. **PROVED/EXACT for the precisely specified gadget grammar, independent mathematical review OPEN.** Two bounded verifiers are **COMPUTATIONAL** only. **P versus NP remains OPEN.**

## Exact end-to-end dependency and proposed falsifiers

**Dependency D5-T5-PARSIMONIOUS-GADGET-MINIMALITY:** Independently inspect TMR-1/072's *new* parsimonious C5-to-T5 edge reduction and replace its bounded negative census by a symbolic minimum-size argument. Input is an authenticated simple undirected graph H, represented with unary n,m headers and sorted low-first addressed edges as in TMR-1/072. A compiler may replace an individual source edge by a pointed, finite, loopless digraph K with named endpoints u,v and arbitrarily many fresh *unlabelled* auxiliary vertices. Its only constraints are arcs interpreted by R(a,b) iff b-a mod 5 belongs to S={1,3}; it has no constants, unary pins, foreign constraints, or connections to other source-edge gadgets. The edge relation induced by K is its existentially projected support

    P(K) = {d in Z5: exists an assignment to auxiliaries with u=0,v=d satisfying all arcs}.

Translation equivariance means P(K) determines every endpoint-label pair. Required relation is exactly {1,4}, the undirected C5 adjacency.

Potential falsifiers announced before checking sources and test data: (F1) a one-auxiliary graph of any arc count projects to {1,4}; (F2) a gadget with arbitrary auxiliaries but <=3 arcs projects to {1,4}; (F3) TMR-1's four-arc gadget has an improper completion or >1 proper completion; (F4) its claimed encoded-output inequality or witness transport fails on empty/isolated, small dense, or malformed sources.

The proof below excludes F1 and F2 for **all finite unpinned pointed gadgets**. Independent source-based finite checks exclude F3/F4 on bounded instances. This closes only edge-local gadget economy, not all-input SAT lower bounds.

## Theorem: sharp two-auxiliary and four-arc optimum (PROVED/EXACT, restricted)

**Theorem.** Let K be any finite pointed digraph with distinguished distinct endpoints u,v, with every constraint of the form R(x_a,x_b) for the fixed tournament T5 and all other variables existentially projected. No symbol constants or pinned labels are permitted. If P(K)={1,4}, then (i) K has **at least two auxiliary vertices** and (ii) K has **at least four directed arcs**, ignoring duplicate copies of the same arc. Both inequalities are simultaneously tight. In fact there is a four-arc, two-auxiliary gadget with exactly **one** internal completion for d=1 or 4 and zero otherwise.

**Proof, no or one auxiliary.** If there are no auxiliaries, the only possibly relevant endpoint constraints are u->v and v->u. They permit S={1,3}, -S={2,4}, every difference, or no difference; none yields {1,4}. Loops and opposite arcs make the relation empty.

For exactly one auxiliary z, opposite directed arcs on the same pair likewise make the relation empty. Otherwise its incidences with each endpoint impose either no condition, z belongs to the endpoint's two outneighbors, or z belongs to its two inneighbors. If zero or one endpoint restricts z, the pre-direct-edge support is all of Z5. If both restrict z, the only possible endpoint supports are

    both same direction: {0,2,3},
    u->z and z->v: {1,2,4},
    z->u and v->z: {1,3,4}.

These follow by enumerating two elements of S and -S or computing their sumsets. The optional direct endpoint arc u->v intersects the support with S={1,3}; the optional reverse arc intersects it with -S={2,4}; both make it empty. No such intersection equals {1,4}. This is a complete classification of all 2^6 possible subsets of the six distinct directed arcs on u,v,z, irrespective of how many such arcs are present.

**Proof, at most three arcs with arbitrarily many auxiliaries.** Delete isolated vertices, which cannot affect *existence* of a completion. A directed loop or opposite arc pair makes the relation empty. If u and v lie in distinct weak components, translation of one component independently of the other shows the projected relation is either all of Z5 or empty, because T5 is invariant under simultaneous translations in Z5.

Otherwise their connected underlying component has at most three undirected edges. If it is acyclic, the unique u-v path has length t in {1,2,3}; every branch hanging off this path extends for any path coloring, since every T5 color has both an in- and an outneighbor. An oriented path of length t has exactly t+1 available endpoint differences for t<=3: each step has increment set S or -S, and -S=S+1 mod5, so its sumset is a translate of tS={t+2j:0<=j<=t}. For t=1, its support is S or -S, neither {1,4}; for t=2 or 3, the support cardinality is 3 or 4, not 2.

If the component is cyclic with at most three arcs and no digon, its unique cycle is a triangle involving exactly one nonterminal vertex (when it contains both endpoints). That is precisely the one-auxiliary case already excluded. If the triangle does not contain both endpoints, u and v cannot lie in the same component with only three arcs. Thus no <=3-arc gadget works.

**Attainment, independently checked.** For a source edge {u,v} ordered u<v, add fresh z,w and exactly

    u->z, u->w, w->z, w->v.

The first three constraints force z=u+1 and w=u+3 modulo five, uniquely. The last requires v-u in {4,1}. The full completion count vector for d=0,1,2,3,4 is (0,1,0,0,1), so it realizes the required support with minimal auxiliary vertices and minimal arcs **simultaneously**, parsimoniously.

The earlier four-arc oriented-cycle edge gadget remains valid, with completion vector (0,2,0,0,2), but is not count-parsimonious. This theorem compares **individual, unpinned, edge-local pp gadgets**, not all possible global reductions, source-shared auxiliaries, additional predicates, fixed constants, or all SAT algorithms.

## Exact source-to-output chain and resource ledger

Original canonical binary source is 1^n 0 1^m 0 followed by m sorted u<v edges using two low-first w(n)-bit names, w(n)=max(1,ceil(log2(max(2,n)))). Parse, authenticate, reject malformed words, emit for each edge its two distinct new vertices and four exact arcs, sort/serialize canonical target source; authenticate output; map each valid C5 witness to the unique T5 witness z_e=u+1,w_e=u+3; inverse projects original n vertices.

For every H:

    #Hom(D*(H),T5) = #Hom(H,C5)
    n_D=n+2m,  m_D=4m,
    L_H=n+m+2+2m w(n),
    L_D=n+6m+2+8m w(n+2m) <= 8 L_H.

The inequality follows m<=n(n-1)/2 and w(n+2m)<=2 w(n), with n=0,1 handled directly. The older factor-2^m four-cycle image must not be conflated with this bijection. The TMR-1/072 specified one fixed locally headed multitape compiler provides a **conservative upper** same-run T=O((L_H+1)^4) and S_peak=O((L_H+1)^2), charging parsing, indices, sorting, per-edge construction, output, invalid words and retention. This run independently verifies the local projection mathematics and bounded authentic outputs, not a new native microcode trace. Composing a T5 decision algorithm adds its actual charged T5(L_D) and S5(L_D); no lower bound follows from the gadget minimum.

TMR-1's parsimonious reverse width-at-most-three one-hot/OR-prefix Boolean compiler remains an upper model transfer (8n_D variables, 20n_D+15m_D clauses). In particular this chain delivers NP-completeness from the known Hell--Nesetril C5-homomorphism dichotomy and the published semicomplete-target dichotomy, but does **not** supply a quantitative 3SAT-to-C5 witness gadget or any superpolynomial time lower bound.

## Executed computational audits and comparison

Independent CPython3 local script "tmr5-minimal-gadget073-v1", SHA256 **6603ede5558686617183a8f819b354fb93f1b8f23dcd306fc4d1e8919da5b39f**, deterministic/no seed, was syntax-checked, executed twice and its JSON outputs compared byte-identically. Raw JSON SHA256 **c10dab84be9bf67c3b3cf72751124ee90b0ad496bced6e69298ae60c92e7b20f**. It exhaustively considered all 64 possible one-auxiliary arc subsets, all <=3-arc gadgets with 0/1/2/3 auxiliaries (4,42,299,1351 graphs respectively), all 25 endpoint label pairs, all 76 undirected simple graphs with n<=4 and their 41,056 original label assignments; 18 bounded cases were also completely expanded and enumerated in T5. Exactly 2,126 assertions, zero failures.

Separate independently coded V8 executable **tmr5-gadget-minimality073-node-v1** ran in the connected execution runtime, 2,131 assertions and zero failures, including 64 one-aux cases, a redundant short-arc enumeration (1,964 test candidates) for up to three auxiliaries, all 25 endpoints and all 76 small input graphs. The executable source and raw result are separately published under experiments/tmr/ and results/raw/tmr/. The two implementations' counts and bounds are kept distinct: they test finite instances, while the all-length minimum-size claim follows the symbolic classification and short-graph proof above.

No local pnp checkout was available; repository preflight was **NOT EXECUTED**. No Lean/nanoda, native finite-Turing-machine interpreter, full LaTeX compilation or external mathematical peer review was executed. The historical E^NP chain remains separate and conditional.

## Red-team four gates and controls

- **DISJ sanity: PASS, restricted.** This is a pointed pp-gadget size statement and a source-to-output upper compiler, not a claim that large rank, girth, treewidth or OBDD width forces every solver to work. Direct O(1)-formula bit paths, biclique counts, high-treewidth but recognizable LPS zero instances, Horn, 2SAT, affine and treewidth shortcuts remain legal.
- **Relativization: PASS for the elementary gadget equivalence, unrestricted NP bridge OPEN.** The reduction is syntactic and relativizes; it does not contradict Baker--Gill--Solovay because no P!=NP implication is drawn. Algebrization and Natural Proofs obstructions remain.
- **Simultaneous DTISP: NOT APPLICABLE WITH REASON.** A lower bound on a bounded gadget's arc count is not a running-time/space tradeoff. The independently reused compiler upper tariff is charged on one realization; no FLMV forbidden-region pair is claimed.
- **Deterministic configuration counting: NOT APPLICABLE WITH REASON.** No deterministic runtime lower bound is asserted. Configuration counting remains an upper-time consistency check only.

The T5 polynomial-time algorithm controls include automorphisms/translation anchoring, affine/Fourier, paths and cycles, connected products, treewidth DP, TMR-2's cofactor/recognizers, TMR-3's degree-two/twin/forest algorithms, and TMR-4's adaptive FBDD and direct-source recognizers. Correct source-aware shortcut algorithms remain admissible. /341 remains FAIL as unrestricted UNSAT authority; /386 remains RESTRICTED.

## Ranked complete-chain dependencies, November 17 14:49 PST

1. **TMR-1:** exact fixed CSP NP-completeness KNOWN THEOREM; /071 nonparsimonious four-cycle PROVED, /072 parsimonious optimal-size edge PROVED with independent TMR-5/073 symbolic audit; source-authenticated explicit signed 3SAT -> undirected C5 with full witness/size interface **OPEN**. Neither parsimonious gadget nor NP-completeness proves SAT runtime hardness.
2. **TMR-2:** exact source-aware cofactor and successor algorithms RESTRICTED; high-girth LPS UNSAT source with efficient source recognizer is a strong NO-case false-positive to prescribed-rank/path-consistency necessity; arbitrary deterministic T5 solver work invariant OPEN.
3. **TMR-3:** forest/Fourier, degree-two weighted elimination and directed independent-twin quotient PROVED/EXACT restricted UPPER algorithms; general checkpoint provider + evaluator lower/upper transfer OPEN.
4. **TMR-4:** authenticated adaptive five-way FBDD and parsimonious bit-CNF source compiler RESTRICTED UPPER; a source-family fixed-order OBDD-vs-adaptive separation and reverse necessary-runtime bridge OPEN.
5. **Across every track:** fixed-template CSP -> generic representation necessity -> arbitrary SAT machine lower bound -> P!=NP remains OPEN, with no hidden nonrelativizing miracle.

**ONE next target:** independently obtain a fully specified, source-authenticated signed 3SAT -> undirected C5 gadget reduction with complete output-size and YES/NO witness transport, and check its composition with the now validated parsimonious, optimal-edge T5 gadget. A primary published theorem alone establishes hardness, not the exact quantitative chain.

## Original research and pinned cross-agent sources

1. Bang-Jensen, J., Hell, P., and MacGillivray, G. *The Complexity of Colouring by Semicomplete Digraphs*. SIAM J. Discrete Mathematics 1(3), 281--298 (1988), DOI: 10.1137/0401029. The paper classifies target semicomplete H-colouring.
2. Hell, P., and Nesetril, J. *On the Complexity of H-Coloring*. JCTB 48, 92--110 (1990), DOI: 10.1016/0095-8956(90)90132-J. H=C5 is odd, loopless, nonbipartite.
3. Barto, L., Kozik, M., and Niven, T. *The CSP Dichotomy Holds for Digraphs with No Sources and No Sinks*. SIAM J. Comput. 38, 1782--1802 (2009), DOI: 10.1137/070708093.
4. TMR-1/072, research/agents/tmr-1/2026-11-17_1404_TMR1_PARSIMONIOUS_T5_C5_EDGE072.md at branch tmr1-20261115-independent-lean060, manuscript SHA af3d3fce677b7b7005f402aec7a56cbdd425a282.
5. TMR-2/069 and TMR-3/070 and TMR-4/071 current exact source-aware compact handoffs and branches as reflected in issue #3. No unrestricted machine lower bound.
