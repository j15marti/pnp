# TMR-2/083: 5-regular high-girth T5 YES/NO pairs with exact low-order moment camouflage

**Date:** 2026-11-18 05:07 PST (America/Los_Angeles). **Role:** TMR-2, PNP Information Necessity. **Primary source:** the fixed five-symbol beat-relation CSP / T5-homomorphism, not a growing-domain substitute. **Status:** PROVED/EXACT restricted symbolic consequences of a cited randomized graph-construction theorem; finite checks COMPUTATIONAL; independent mathematical review OPEN. **P versus NP OPEN.**

## One exact end-to-end target and falsifiers

Target D2-T5-REGULAR-GIRTH-CYCLE-MOMENT-FILTRATION: authentic canonical \`p t5 n m\` T5 source -> verify five-regular connected bipartite skeleton and true arc directions -> induced low-order subinstance count/multivariate moment -> forest transfer -> first cycle-sensitive operation -> legal restricted oracle consequence, plus a cited source-generator path producing same-skeleton YES/NO samples with high probability.

Falsifiers predeclared before the research/source search: (F1) five-regular large-girth bipartite skeletons fail to exist with randomized polynomial-in-output construction; (F2) a connected five-regular skeleton has non-negligible probability of a T5-satisfiable uniformly oriented source; (F3) some oriented forest count depends on its arc orientations; (F4) the cycle transfer and its first possible orientation dependence disagree with a direct original-label counter. The scoped mathematical lemmas survive these tests. We do **not** claim source-verifiable NO certificates or any compulsory general solver runtime.

## Theorem A: fixed degree 5, growing girth, and exponentially rare SAT orientations

For every fixed real 0<c<1 and all sufficiently large even N, Linial and Simkin [1] give a randomized polynomial-time-in-N graph construction that, with probability tending to one, generates a connected simple **5-regular** undirected graph K_N of girth at least \(\lfloor c\log_4 N\rfloor\). The original procedure starts from a Hamilton cycle and adds valid remote edges; its guarantees are in [1], not established by our finite audit.

Take the canonical bipartite double cover of K_N and choose any connected component H_N. The cover has degree 5, girth at least that of K_N, and is bipartite. If K_N is nonbipartite it is connected with 2N vertices; otherwise it has two isomorphic components with N vertices each. Therefore H_N is a **connected simple 5-regular bipartite graph** with n in {N,2N} vertices and m=5n/2 edges, with \(g(H_N)=\Omega(\log n)\). Its construction and authentication are polynomial in the actual output size.

Directing all edges left-to-right gives an explicit **YES** T5 source with the complete original-label witness x(left)=0, x(right)=1. Independently orient the same undirected edges by fair bits to produce D. For each proposed vertex labeling f in \(\{0,\ldots,4\}^{V(H_N)}\), if adjacent labels coincide then f realizes no orientation; otherwise f realizes **exactly one** orientation, because T5 is a loopless tournament. Consequently
\[
\mathbb E_{\rm orientation}[Z(D)]
=\frac{P_{H_N}(5)}{2^{m}},
\]
where P_H(5) is the number of proper five-colorings of H. Since H is connected, any spanning tree gives
\[
P_{H}(5)\le5\cdot4^{n-1}.
\]
By Markov on the nonnegative integer Z,
\[
\boxed{
\Pr_{\rm orientation}\bigl[D\to T_5\bigr]
\le \frac{5\cdot4^{n-1}}{2^{5n/2}}
=\frac54\,2^{-n/2}.
}
\]
This is a rigorous probability bound **conditional on each successful H_N**. Thus the randomized poly-output source procedure yields mixed same-skeleton YES/NO T5 sources with probability tending to one, with both sides connected, bipartite as undirected graphs, 5-regular and of logarithmically increasing undirected girth. The NO orientation is overwhelmingly likely, **not individually verified or supplied with a short UNSAT certificate**; a random seed alone is not proof of unsatisfiability. The theorem supplies existence and a successful-sampling probability, not a worst-case all-input solver.

This is a strictly stronger *structural* form of the previously recorded existential large-girth same-skeleton construction /078: fixed degree five, randomized polynomial-in-output skeleton construction and an exponential quantitative NO-probability. It does not claim efficiently certified hard NO instances.

## Theorem B: all exact edge-subinstance moments below girth are orientation-blind

Let D be **any** loopless orientation of a simple undirected graph H with n vertices and girth g, and let F be any subset of k<g undirected edges, retaining the entire original vertex set including isolates. Then (V,F) is a forest with n-k weak components. For each tree choose one root color (5 choices) and propagate along each tree edge (2 target choices for every fixed parent label, regardless of the source direction). Hence
\[
\boxed{Z(D[F])=5^{n-k}2^k\quad\text{for every }|F|=k<g.}
\]
Define the exact multivariate edge-subinstance polynomial
\[
\mathcal Z_D(\{z_e\})
=\sum_{x\in\mathbb Z_5^V}
 \prod_{e=(u,v)\in E(H)}(1+z_e R_e(x_u,x_v)).
\]
For every edge set F, the coefficient of \(\prod_{e\in F}z_e\) equals Z(D[F]). Thus **all multivariate coefficients through total degree g-1** are the same for all orientations of H. With common weight t on every edge, the exact first g coefficients are
\[
[t^k]\mathcal Z_D(t)
=\binom{m}{k}5^{n-k}2^k,\qquad 0\le k<g.
\]

**Restricted adaptive oracle consequence (PROVED/EXACT):** Give a machine the undirected skeleton H, but hide all arc directions; allow arbitrary adaptive queries returning exact original-label counts Z(D[F]) for edge subsets of size at most g-1, and no other orientation-dependent information. For the matching YES/NO pair, every query returns exactly the same count. Therefore *no number* of such queries can distinguish the pair; some query involving at least g edges, or access to another orientation-sensitive interface, is necessary in THIS MODEL. This is a lower bound on **oracle query scope**, not a runtime, communication, memory, FBDD, circuit, or unrestricted T5 decision lower bound. In particular an ordinary solver can read the original arc directions directly.

If a graph orientation is UNSAT, every UNSAT subgraph contains an undirected cycle and therefore at least g original edges and g nonisolated original vertices; this does not imply a large proof DAG or expensive search.

## Theorem C: exact cycle phase shows the degree threshold can be sharp

For an oriented cycle C_l, traverse the undirected cycle in one fixed direction. Suppose p source arcs agree with traversal and q oppose it, p+q=l. A forward step has color increment in {1,3}=1+{0,2} mod 5, and a reverse step has increment in {2,4}=2+{0,2}. Each of the l steps independently selects the 0 or 2 summand. Exact closed-walk counting gives
\[
\boxed{Z(C_l;p,q)=5\sum_{b=0}^l\binom lb\,\mathbf1[p+2q+2b\equiv0\pmod5].}
\]
All arc-sign words with the same p,q have the same count, but some different p,q do not. In particular the undirected eight-cycle has 180 homomorphisms when all eight edges form a directed cycle and 350 when all four bipartition-left vertices direct every edge toward the right. Both have identical exact edge-subinstance counts for every subset of at most seven edges. This proves that the first possible orientation-sensitive degree g can actually be attained.

**Named dynamic invariant for TMR-4: D2-T5-CYCLE-ENTRY-MOMENT-FILTRATION.** An authentic source-trace maintains original vertex/edge identities, current forest components (DSU), n, k, the cycle-first threshold, and exact root-rotation-invariant counts. The transition BRIDGE_JOIN has exact factor 2/5 in the count over all original variables because connected-component color rotations are uniform and independent. The transition CYCLE_CLOSE is the first that can introduce a nontrivial signed-cycle correlation; it must retain/compute/charge an authentic source-derived boundary or cycle syndrome. READ/PARSE/GUARD, CHOOSE_QUERY, DSU_FIND/JOIN, CHECK_GIRTH, BRIDGE_JOIN, CYCLE_CLOSE, EXACT_BIGINT, CACHE/DROP/RECOMPUTE, SOURCE_RECHECK and OUTPUT are paid. No operation is declared compulsory for general machines, which may exploit source-aware, Fourier, Gaussian, separator, low-width, symmetry, or direct witness/certificate methods. A moment-length count alone is not a work lower bound.

## Reproducible finite controls actually executed

Executed pure hosted JavaScript/V8 audit \`tmr2-t5-regular-girth-moment083.v1\`, deterministic xorshift seed **202611180507**, provided as a standalone Node.js source under \`experiments/tmr/tmr2_t5_regular_girth_moment083.js\` and immutable output under \`results/raw/tmr/2026-11-18_0507_TMR2_T5_REGULAR_GIRTH083_RAW.json\`.

The completed execution contained **3,324 assertions, 0 failures**, with 210 independent original-five-label brute-force forest counts cross-checked against a distinct exact BigInt tree-DP routine; all 336 orientations of cycles of lengths 4, 6, 8 checked against the exact binomial phase formula; direct 8-variable enumeration confirmed 180 versus 350; independent GF(4) finite-field construction recreated the W(3,4) incidence skeleton with n=170, m=425, degree five, girth eight and connectivity; 280 randomly sampled edge subsets (sizes 0 to 7) per orientation, **560** exact independent subtree-DP comparisons, matched the forest formula. The skeleton edge-sequence FNV32 is \`4c709636\`; the audited sampled orientation FNV32 is \`2f535090\`. The measured numerical upper probability bound for random orientation of this finite graph is \(3.2311742677852644\cdot 10^{-26}\). The sampled orientation's actual SAT/UNSAT status was **NOT certified** and is not claimed.

The symbolic infinite-family theorem relies on the externally published high-girth construction and the double-cover/counting proofs, NOT on extrapolation from W(3,4). The W(3,4) base orientation from the /082 report remains an independent finite NO certificate with a short refutation, explicitly allowed here. No individual high-girth growing-family NO certificate, native Node execution, actual Linial-Simkin generator run, repository checkout/preflight, LaTeX build, physical Turing-machine trace or external referee was performed. The report/experiment is not claimed to replace those validations.

## Source costs and verification gates

Skeleton discovery/authentication parses each complete canonical source (n,m, all original directed arcs), rejects malformed syntax and repeat/antiparallel/loop edges where the theorem requires a simple orientation, computes degree and connectivity, verifies bipartiteness and girth by paid BFS, stores the original per-edge direction, and checks the supplied edge subset. Tree-DP costs O(25(n+k)) arithmetic operations plus exact integer bit costs on O(n)-bit values, with polynomial peak storage; monomial coefficient enumeration for all subsets is combinatorial and NOT free. A straightforward Linial-Simkin sampling implementation has polynomial-in-N source generation/edge checks when it succeeds; the theorem is high-probability, not a guaranteed uniformly certified construction. Exact probability bound uses O(n)-bit powers. The entire same-run finite verifier has polynomial time/peak storage in authenticated input length; no actual TM microstep replay was executed.

Mandatory controls: **DISJ PASS for restricted oracle lemma, FAIL for any static-coefficient to unrestricted-machine time inference.** **Relativization PASS local / OPEN unrestricted**, with Baker-Gill-Solovay, algebrization and Natural Proofs unchanged. **Simultaneous DTISP PASS on the same finite verification algorithm, OPEN any forbidden lower pair.** **Deterministic configuration count PASS upper-bound consistency only**, with no necessary-work conclusion. Horn/2SAT, affine/Gaussian, rank, full-cycle Fourier, bounded treewidth, exact separators, independent products, selectors, source-aware fast certificates, equivalent circuits, and caching/sharing/recomputation remain legitimate alternatives. /341 FAIL full UNSAT and /386 RESTRICTED.

## ONE next load-bearing lemma

**D2-T5-REGULAR-GIRTH-EXPLICIT-CERTIFIED-NO-AND-DYNAMIC-CYCLE-BARRIER (OPEN):** choose a connected 5-regular high-girth bipartite skeleton from an actual reproducible near-logarithmic-girth generator, provide one **independently checkable UNSAT certificate for its specific NO orientation** and the identical-skeleton YES witness, then quantify source-authenticated adaptive cycle-closure (not merely initial girth, width, or low-degree) costs against Fourier/flow, tree-DP, separators, source-recognizable patterns and unrestricted bypasses. An all-solver superpolynomial lower bound remains entirely OPEN.

## Original and project sources

[1] N. Linial and M. Simkin, *A randomized construction of high girth regular graphs*, Random Structures & Algorithms 58(2):345-369, 2021, DOI 10.1002/rsa.20976; arXiv:1911.09640v3 (2020-06-29): https://arxiv.org/abs/1911.09640.

[2] H. Sachs, *Regular graphs with given girth and restricted circuits*, Journal of the London Mathematical Society s1-38:423-429, 1963, DOI 10.1112/jlms/s1-38.1.423. Background fixed-degree large-girth existence, not the claimed randomized efficient generator.

[3] Prior TMR-2/078 same-skeleton undirected-girth YES/NO existence and PC/SAC theorem: \`research/agents/tmr-2/2026-11-18_0007_TMR2_T5_UNDIRECTED_GIRTH_SINGLETON078.md\`.

[4] Prior TMR-2/082 W(3,4) and high-conditioned-width countercontrol: \`research/agents/tmr-2/2026-11-18_0415_TMR2_T5_SYMPLECTIC_SUBFIELD_WIDTH082.md\`.

[5] TMR-4/086 signed-cycle syndrome algorithm and TMR-5/088 Fourier-flow audit recorded on issue #3; the current result is a different local-information **query-scope** characterization and does not rediscover their exact cycle-space counter algorithms.

END_OF_REPORT::TMR2::2026-11-18_0507_PST_REGULAR_GIRTH_MOMENTS083
