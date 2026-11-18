# TMR-1/074: source-authenticated T5 cotree-boundary exact counter

2026-11-17 15:57 PST. TMR-1 / PNP Machine Model Lead. Named dependency C1-T5-COTREE-BOUNDARY-FPT. PROVED/EXACT restricted symbolic theorem, independent external mathematical review OPEN; finite verification COMPUTATIONAL. P versus NP OPEN. TMR-5 independently completed the signed 3SAT-to-T5 compiler on separate open draft PR #209; this report does not duplicate it.

## Candidate, quantifiers and falsifiers

For EVERY valid encoded five-symbol directed CSP G=(V,E), construct a fixed deterministic spanning forest of the underlying undirected graph, pin one root per weak component to zero, enumerate only the labels of nonroot endpoints of nonforest arcs, check all those arcs and exactly count remaining tree completions. Falsifiers: incorrect reverse-arc orientation; lost or duplicated Z5 translation orbit; chord endpoint not pinned; hidden exponential memory or coefficient precision. All are treated explicitly.

The canonical low-first graph encoding is 1^n 0 1^m 0 followed by distinct sorted ordered endpoint pairs, width w(n)=max(1,ceil(log2(max(2,n)))). Its exact bit length is L=n+m+2+2mw(n). Authenticate unary terminators, exact length, ranges, sorted order and absence of trailing bits. Malformed words return INVALID, not a count. Loops and opposed arcs are valid sources but give exact answer 0 because R(a,a)=0 and R(a,b)R(b,a)=0. The empty graph has count 1. Certificates have three low-first bits per vertex, limited to 0..4.

## Theorem and complete proof

Let c be the number of weak connected components, including isolates. After the two zero-detection guards, build a spanning forest F with n-c edges, treating each directed arc as an undirected connectivity test while retaining its direction. There are r=m-n+c cotree arcs. Let B be the union of their endpoints. Choose one root in each component, from B if B meets that component. Let c_* be the number of components containing a cotree arc, and put b=|B|-c_* = |B\setminus roots|. Then b<=min(n-c,2r-c_*), with b=0 when r=0.

THEOREM: One uniform ordinary deterministic, source-authenticating and blank-start bit machine returns the EXACT count Z(G) in
T=O((L+1)^6(1+5^b)) bit operations and S_peak=O((L+1)^3) writable bits ON THE SAME EXECUTION.

PROOF: For each of the 5^b assignments h:B\setminus roots -> Z5, pin all roots to 0 and other vertices in B to h. Discard h if any nonforest oriented arc violates R. Root every forest tree. For each vertex v, candidate label a and its child u, compute, bottom-up,
D_v(a) = pin_ok(v,a) * PRODUCT_child(u) SUM_(d=0..4) [R(a,d) for v->u; R(d,a) for u->v] D_u(d).
This uses actual source arc orientation, not a symmetrized relation. Multiply D_root(0) over components, sum over all surviving h. Each rooted solution has one unique boundary assignment h, and every complete forest assignment counted by this DP satisfies all tree edges. Conversely every solution with all roots pinned 0 is counted once because every cotree endpoint is either a root or enumerated. Translation of ALL labels in one weak component by t mod5 preserves every arc and acts freely, so each satisfying orbit has exactly five elements and exactly one root-zero representative. Therefore
Z(G)=5^c SUM_h [all cotree constraints valid under h] PRODUCT_components D_root^h(0).
This remains valid for disconnected graphs and the empty graph. The exact output and all intermediate nonnegative integers are at most 5^n, thus O(n) bits. The input, forest, root set, rejected trials, counters, addresses, buffers, arithmetic, full output and per-assignment reused 5n-entry DP table are all charged. No exponential table is retained. Naive integer arithmetic easily fits the displayed conservative O(L^6) factor per boundary assignment and O(L^3) peak workspace. QED.

FOREST COROLLARY: If r=0, every component root has five choices and each forest child independently has exactly two choices conditional on its parent, even for reversed arcs. Hence Z(G)=5^c 2^(n-c), and every such input is satisfiable.

## Genuine source-to-output composition and reduction parameter

The existing TMR-5/074 exact signed 3SAT -> 3-COLOR -> anchored C5 -> directed T5 construction has, for nonempty normalized clause set of m' distinct ordered triples and k used Boolean variables, N_D=57+36k+168m' and A_D=80+52k+244m'. The three-color source is attached to one common palette; the anchored C5 stage connects every original graph vertex to one five-cycle; every T5 gadget remains connected to its endpoints. Thus the final directed graph is weakly connected, c=1, and EVERY spanning forest has the exact number of nonforest arcs
r=A_D-N_D+1=24+16k+76m'.
This audit shows that the established NP-hardness construction does not secretly land in the O(log L) feedback-rank promise simply by the gadget chain. There is no inference that faster non-FPT methods cannot exist.

CONDITIONAL NECESSITY: If a uniform polynomial-time SAT-to-T5 reduction produced equivalent canonically encoded graphs of polynomial length and r=O(log(L+2)) for EVERY SAT source length L, composing it with the counter above would put SAT in P and hence imply P=NP. The same holds for a polynomial-time all-source equivalent T5 preprocessing algorithm that always reduces r to logarithmic size. Neither such compiler nor P=NP is asserted. This is a conditional compression barrier, not a complexity separation or a solver lower bound.

## Gates, primary provenance and evidence

DISJ PASS restricted: no rank-to-work claim. Relativization PASS for this explicit algorithm; NP nonrelativizing promotion OPEN. Simultaneous DTISP PASS for the same-realization deterministic UPPER ledger only. Deterministic configuration counting NOT APPLICABLE WITH REASON as a lower-bound device, which the result does not invoke. Fourier/Gaussian, affine, treewidth, polymorphisms, local consistency, product, selector, sharing, caching, Horn/2SAT and source-recognition shortcuts remain legal. /341 FAIL for full UNSAT, /386 RESTRICTED. Algebrization/Natural Proofs do not supply an unrestricted bridge. P versus NP remains OPEN.

Executed CPython 3 finite audit, seed 20261117, script SHA256 72da0c2bec3aa72cac9af982d8ca9ca7962fcf6da3b33b3e3bfa9fcea3cbf665: 760 canonical cases, 2558 assertions, seven malformed rejections, 0 failures, maximum r=10,b=5. Independently executed V8 source tmr1-t5-feedback074-js1 and published EXACT source under experiments/tmr/tmr1_t5_feedback074.js: 438 cases, 1314 assertions, seven malformed rejects, 0 failures, max r=10,b=5. Both compare the exact algorithm against 5^n brute-force enumeration for n<=6; they remain COMPUTATIONAL. Raw metadata in results/raw/tmr/2026-11-17_1557_TMR1_T5_COTREE_BOUNDARY074_RAW.json. No local repository checkout/preflight, whole living-manuscript LaTeX build, independent Lean/nanoda rebuild, or external mathematical peer review performed.

Primary source for NP-complete 3-colorability: Garey, Johnson, Stockmeyer, Some Simplified NP-Complete Graph Problems, Theoretical Computer Science 1 (1976), 237-267, DOI 10.1016/0304-3975(76)90059-1. Original graph compiler TMR-1/073 and independent full signed SAT compiler TMR-5/074 remain separately scoped on their respective open draft branches.

ONE next load-bearing lemma: C1-T5-COTREE-COMPRESSION-AUDIT. Seek or falsify a source-authenticated exact graph reduction that materially decreases feedback rank on a mixed YES/NO family without concealing enumeration in its discovery, and provide SAME-execution time and space.
