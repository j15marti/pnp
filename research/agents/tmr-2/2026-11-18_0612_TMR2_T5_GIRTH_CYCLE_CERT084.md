# TMR-2/084: Certified fixed-T5 high-girth NO and a polynomial-time first sensitive cycle moment

Date: 2026-11-18 06:12 PST (America/Los_Angeles). Research owner: TMR-2 / PNP Information Necessity. Status: **PROVED/EXACT restricted symbolic results**, **COMPUTATIONAL finite certificates and histograms**, **independent external mathematical review OPEN**. P versus NP **OPEN**.

## Target, model, and falsifiers

Let \(T_5\) have vertices \(\mathbb Z_5\) and \(R(a,b)\) iff \(b-a\pmod 5\in\{1,3\}\). A source is a finite original directed graph \(D=(V,A)\), asking for an assignment \(x\in\mathbb Z_5^V\) with \(\prod_{(u,v)\in A}R(x_u,x_v)=1\). Isolates and all original variables are counted in \(Z(D)\); neither a promise oracle nor a free auxiliary is used.

Dependency: **D2-T5-REGULAR-GIRTH-EXPLICIT-CERTIFIED-NO-AND-DYNAMIC-CYCLE-BARRIER**, from /083. Candidate: use exactly the W(3,4) 170-vertex, five-regular, girth-eight incidence skeleton and independently certify an explicit, source-generated NO orientation against a same-skeleton YES. Measure whether the exact *first* orientation-sensitive forest-to-cycle moment requires expensive work.

Falsifiers established before testing: (i) the sampled NO could have a T5 witness; (ii) any omitted propagation branch could invalidate an apparent UNSAT proof; (iii) first differing moment could remain equal on the pair; (iv) counting shortest cycles could be intrinsically superpolynomial despite degree five and large girth. A further hostile control is any legal short source-aware NO certificate, which would defeat the intended information-necessity inference.

## Theorem 1: degree-five shortest-cycle moments have polynomial-time source computation

For any simple undirected graph \(H=(V,E)\) with \(n\) vertices, \(m\) edges and girth \(g\), and any orientation \(D\), define
\[
 \mathcal Z_D(t)=\sum_{x\in\mathbb Z_5^V}\prod_{e\in E}(1+tR_e(x)).
\]
For \(k<g\), every \(k\)-edge selection is a forest, hence
\[
 [t^k]\mathcal Z_D(t)=\binom mk5^{n-k}2^k.
\]
At exactly \(k=g\), a selected edge set is either a forest or a single \(g\)-cycle plus isolated original vertices. Let \(\mathcal C_g(H)\) be the set of **undirected** \(g\)-cycles, counted once. Then
\[
\boxed{
[t^g]\mathcal Z_D(t)=\binom mg5^{n-g}2^g+
5^{n-g}\sum_{C\in\mathcal C_g(H)}\bigl(Z(D[C])-2^g\bigr).
}
\]
If an \(\ell\)-cycle has \(p\) edges oriented along a selected traversal and \(q=\ell-p\) against it, the exact original-label cycle count is
\[
Z(C;p,q)=5\sum_{b=0}^\ell\binom\ell b
 \mathbf1\{p+2q+2b\equiv0\pmod5\}.
\]
This follows by assigning each oriented edge its allowed modular step (forward \(1,3\), backward \(2,4\)), enforcing a total step of zero, and multiplying by five choices of the starting label. The formula was separately checked against a 5-by-5 transfer matrix in the executable audit.

**Polynomial upper bound, explicitly scoped to fixed \(\Delta\)-regular graphs with \(\Delta\ge3\).** The Moore breadth-first-tree bound implies \((\Delta-1)^g=O(n^2)\) with constants depending on \(\Delta\). Rooted simple-path enumeration up to depth \(g\) therefore visits at most \(O(n\Delta(\Delta-1)^{g-1})=O(n^3)\) path states. Canonical minimum-vertex and traversal-reversal tests enumerate every undirected shortest cycle once. Finding \(g\), reading and authenticating the source, calculating its orientations, counting signed cycle steps, computing integer binomials and the final \(O(n)\)-bit factors, and writing the output all require polynomial deterministic bit-work and peak space on the **same run**. There is no assertion that this moment decides all T5 sources or distinguishes every pair.

This is a concrete falsifier of extrapolating /083's *query scope* obstruction to a superpolynomial running-time obligation: the first sensitive coefficient is source-computable in polynomial time throughout the fixed-degree regular family, even when \(g=\Omega(\log n)\).

## Theorem 2: exact 170-vertex certified NO with a seven-node source refutation

Reconstruct \(W(3,4)\) from GF(4) projective points and totally isotropic lines, normalize nonzero four-vectors by their first nonzero coordinate, and join each point to each of its five isotropic lines. The construction yields exactly 85 points, 85 lines, 425 incidences, connected graph, degree five, undirected girth eight and 13,600 undirected eight-cycles.

Canonical YES orients every point-to-line incidence, with assignment \(x_{\rm point}=0\), \(x_{\rm line}=1\). In fact \(Z(\mathrm{YES})\ge5\cdot2^{85}\), by a common arbitrary point label and an independent choice of its two outneighbors at every line.

Canonical NO follows the same sorted incidence list, orienting each edge with deterministic xorshift32 seed **202611180612** (32-bit shifts 13, 17 and 5, least-significant-bit orientation). This is a **seeded pseudorandom construction**, not a fair independent random-sampling proof. Canonical original-source ASCII is the header \`p t5 170 425\`, followed by \`v i\` declarations for all 170 vertices and sorted \`a u v\` arcs. The NO source is 4,623 bytes with SHA256:
\`cc9e6c343ca2bccfe8839a8dd077d4d543e75e2bd669100f5e87861637a10632\`.

Global translation \(x_v\mapsto x_v+c\bmod5\) is an automorphism of the fixed template, so it suffices to reject all assignments with \(x_0=0\). Repeated sound arc-revision on the **complete authentic source** yields this exhaustive split:

\[
x_0=0\quad\Longrightarrow\quad x_{85}\in\{1,3\}.
\]
\[
\begin{array}{rcl}
x_{85}=1&\Longrightarrow&x_1\in\{2,4\},\\
x_{85}=3&\Longrightarrow&x_1\in\{1,4\}.
\end{array}
\]
Fixing \(x_1\) to any one of the four stated leaves makes an original source variable's support empty under arc consistency. There are **three internal branching nodes and four contradictory leaves**, seven nodes total, depth two after the gauge. The result is \(Z(\mathrm{NO})=0\), not a claim that every 170-vertex NO is easy.

A separate **whole-source AC implementation** reconstructs all support sets directly from the elementary R(a,b) predicate, not from the discovery routine's precomputed 32-mask maps. It independently replays all seven tree nodes, twelve full arc-sweeps and 79,243 primitive label-pair tests. No omitted branch or unverified conflict leaf is accepted.

## Exact first distinguishing moment on the same skeleton

The enumerator visits exactly **13,600** distinct undirected eight-cycles in each orientation. Its histogram groups a traversal with its reverse, using \(h=\min(q,8-q)\).

| \(h\) reversed arcs | YES eight-cycles | NO eight-cycles |
|---:|---:|---:|
| 0 | 0 | 116 |
| 1 | 0 | 896 |
| 2 | 0 | 3,097 |
| 3 | 0 | 5,962 |
| 4 | 13,600 | 3,529 |
| **Total** | **13,600** | **13,600** |

The exact respective sums of the 13,600 eight-cycle homomorphism counts are 4,760,000 for YES and 3,467,195 for NO. All coefficients of degree \(<8\) agree by Theorem 1, while
\[
\boxed{
[t^8]\mathcal Z_{\rm NO}(t)-[t^8]\mathcal Z_{\rm YES}(t)
=-1\,292\,805\cdot5^{162}\neq0.
}
\]
Thus **a polynomially computed, source-aware shortest-cycle statistic already distinguishes this pair**. The edge-subset oracle limitation remains correct for its precisely declared model, but it cannot imply large work for arbitrary source readers. The statistic is not a general SAT test: a different NO may share its eighth-cycle statistic with a YES.

## Finite evidence, scope, and same-realization ledger

The full local CPython standard-library script \`tmr2_t5_girth_cycle084.py\` was executed after an early independent transfer-matrix fixture correction. Final revision \`tmr2-t5-girth-cycle-certified084.v1\`, 15,661 assertions, **zero final failures**, full decoded source SHA256 \`1072e1fa7c0a00cb13e10ddb7966d01fdb9e5a0faeb8253f14557badb280f9e2\`. Its final JSON has SHA256 \`a2e9dd66e05dd2eb1c2a368a72d3e85a073966c45a6e54c0e16503b16a6d575f\`. A smaller separately executed verifier \`experiments/tmr/tmr2_t5_girth_cycle_cert084.py\` reconstructs the source, verifies the seven-node proof and recomputes the cycle statistic. Repository raw extract: \`results/raw/tmr/2026-11-18_0612_TMR2_T5_GIRTH_CYCLE084_EXTRACT.json\`.

Additional stress control: 100 **deterministically seeded pseudorandom** orientations, seeds 202611180700 through 202611180799, were individually checked by complete gauge-and-AC branch certificates and the independent AC replay. All 100 were certified UNSAT; 87 certificates used seven nodes and 13 used nine. These observations are **COMPUTATIONAL**, not a theorem about all random orientations and not independent uniformly random samples. The separately sourced fair-random orientation bound from /083 remains a mathematical statement about its *different* probability experiment.

Same-run discovery/read cost includes GF(4) arithmetic, normalization, all incidences, complete canonical ASCII source and SHA256, one 32-bit PRNG traversal, unary gauge check, certificate search with recorded 5,253 source-arc revisions and 884 domain updates, independent full-graph support revisions, BFS girth, 13,600 cycle enumeration, all exact integer arithmetic and serialization. The certificate search itself is a valid polynomially checkable **witness of UNSAT on this source**, not an all-input polynomial T5 algorithm. The small verifier was executed locally; a full repository checkout/preflight, full LaTeX compilation, external mathematical review and physical Turing-machine microstep trace were not run.

## Four gates, cheap controls, and handoff to TMR-4

**DISJ:** PASS for the scoped exact moment/proof tree; FAIL any inference from static assignment rank or a large enumeration table to general necessary work. **Relativization:** PASS for the explicit upper construction / OPEN for any unrestricted P-versus-NP claim; BGS, algebrization and Natural Proofs safeguards remain. **Simultaneous DTISP:** PASS for a valid matched certificate-verifier and moment-evaluator polynomial upper; OPEN any forbidden pair or SAT lower bound. **Deterministic configuration counting:** PASS as an upper-bound consistency check only; no necessary-work inference or quantum/randomized transfer.

All source-aware subgraph-pattern recognizers, Fourier/cycle-space calculations, exact weighted contraction, variable elimination, treewidth/OBDD/FBDD methods, direct witnesses, caching, recomputation, separator/twin/module reductions, affine/Gaussian, Horn/2-SAT, DISJ, selector/padding, original-auxiliary multiplicities and other legal shortcuts remain admissible. /341 remains FAIL as an unrestricted UNSAT authority, /386 remains RESTRICTED.

Named trace to TMR-4: **D2-T5-GIRTH8-CYCLE-MOMENT-VERSUS-GAUGE-AC-CERT-TRACE**. Source-authenticated events are READ/PARSE/HASH, GF4_GEOMETRY, ORIENT, ROOT_GAUGE, AC_REVISE, BRANCH_ALL_SUPPORTED, EMPTY_DOMAIN_CERT, SOURCE_RECHECK, GIRTH_BFS, CANONICAL_CYCLE_ENUM, SIGNED_STEP_HISTOGRAM, BIGINT_COEFFICIENT, CACHE/RECOMPUTE and OUTPUT. The cycle moment and AC proof are two **optional** paid decision-information routes; neither may be declared compulsory for unrestricted machines.

**ONE next load-bearing dependency:** **D2-T5-GROWING-GIRTH-RESIDUAL-NONLOCAL-DECISION** (OPEN). Construct a growing explicit mixed YES/NO family, not a constant-core extension, with individually checkable NO certificates and no constant-depth gauge-AC refutation, and compare the *minimum* known source-aware decision costs to exact cofactor, cycle-flow, OBDD/FBDD and weighted contraction costs. An unbounded width or high-girth moment filtration by itself is insufficient. P versus NP remains OPEN.

Primary literature: N. Linial and M. Simkin, *A randomized construction of high girth regular graphs*, Random Structures & Algorithms 58(2), 345–369 (2021), DOI https://doi.org/10.1002/rsa.20976. Earlier local sources: TMR-2 /078, /079, /080, /081, /082 and /083. This report does not claim that Linial–Simkin's sampler was executed.
