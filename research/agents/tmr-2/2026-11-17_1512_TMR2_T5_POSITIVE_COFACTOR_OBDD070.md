# TMR-2/070 | November 17, 2026, 15:12 PST | Nonzero T5 cofactors with all-order exponential OBDD width but trivial source SAT

Owner: TMR-2 / PNP Information Necessity. Living manuscript: \`main2_PNP_INFORMATION_NECESSITY.tex\`. Scientific status: **PROVED/EXACT restricted symbolic result relying on the established LPS expander theorem; external independent mathematical review OPEN**. Finite audits **COMPUTATIONAL**. P versus NP **OPEN**.

## Precise selected dependency and falsifiers

**D2-T5-NONZERO-COFACTOR-OBDD-EXPANDER** advances /069's D2-T5-NONZERO-COFACTOR-PC-OBSTRUCTION. For a uniformly source-generated, genuine satisfiable T5 family, prove that **for every original-variable order** one semantic assignment-indicator cut has rank exponentially large over Q and every corresponding five-ary OBDD has exponential width, while preserving a polynomial-time source-authenticated SAT witness. A ranking by width alone cannot yield a necessary-time lower bound for arbitrary graph-source deciders.

Falsifiers declared before original-source review: (F1) the four-arc path transfer has a zero or singular pinned-endpoint matrix; (F2) the rank comparison fails when private variables are split arbitrarily by an OBDD cut; (F3) the expander's many cut edges cannot supply a linear induced matching with all other core labels fixed; (F4) the alleged cheap YES algorithm uses an uncharged LPS identity oracle, an invalid graph encoding, or a nonuniform witness. The audit below resolves F1-F4 for the restricted construction. It does not establish arbitrary FBDD or Turing-machine lower bounds.

## Actual encoded family, rather than an assignment-table oracle

Let \(T_5=(\mathbb Z_5,R)\), \(R(a,b)=[b-a\bmod5\in\{1,3\}]\). Start with an **explicit** undirected simple graph \(H=(V,E)\), \(n=|V|\), \(m=|E|\). For each edge \(e=\{u,v\}\) with \(u<v\), introduce three fresh original CSP vertices \(a_e,b_e,c_e\), and exactly the four source arcs

\[
u\longrightarrow a_e,\quad a_e\longrightarrow b_e,\quad
v\longrightarrow c_e,\quad c_e\longrightarrow b_e.
\]

Thus \(G(H)\) has \(n'=n+3m\) genuine five-label variables and \(m'=4m\) actual R constraints. No auxiliary labels are silently existentially forgotten in the original Boolean assignment indicator. Serialize all vertices and sorted distinct arcs in the corrected /068 canonical ASCII grammar, one declaration per vertex. For the LPS choice below, \(m=3n\), so \(n'=10n,\;m'=12n\), and complete source length \(L=\Theta(n\log(n+2))\).

Choose the nonbipartite LPS Cayley family \(H_q=X^{5,q}\) on \(\mathrm{PSL}_2(\mathbb F_q)\), with every prime \(q>125\), \(q\equiv1\pmod{20}\). These conditions ensure the required quadratic-residue branch, 6-regularity, and infinitely many parameters by Dirichlet. Use the already specified quaternion/group BFS constructor with parameter \(p=5\), then explicitly serialize every induced four-path. Its size is \(n=q(q^2-1)/2\), \(m=3n\). Generation including candidate screening, modular root search, generator construction, complete group BFS, sorted arcs, caches and output is polynomial **in the generated explicit source size L**, not asserted polynomial in \(\log q\) or in the binary index of the q-th eligible prime. The LPS bound is \(\lambda_2\le2\sqrt5<6\); its girth is at least seven for these large q. The subdivided G has girth at least 28 and treewidth \(\Omega(n)\) since H is a graph minor. Independently, the conclusion below only needs the expander eigenvalue bound, not the girth theorem.

## Exact private-variable count, all-YES decision and actual label counts

Let \(A_{ab}=R(a,b)\). Each four-arc path with endpoints fixed to \(s,t\) contributes exactly

\[
 W_{st}=\sum_{\alpha,\beta,\gamma\in\mathbb Z_5}
 R(s,\alpha)R(\alpha,\beta)R(t,\gamma)R(\gamma,\beta)
 =(A^2(A^\mathsf T)^2)_{st}.
\]

Direct integer multiplication yields
\[
 W=\begin{pmatrix}
6&1&4&4&1\\1&6&1&4&4\\4&1&6&1&4\\
4&4&1&6&1\\1&4&4&1&6
\end{pmatrix},\quad
\det A=2,\quad\det W=16.
\]
Every W entry is strictly positive, and \(\operatorname{rank}_{\mathbb Q}W=5\). Over characteristic 2, \(\det W=0\); all large-rank claims here are explicitly over Q, R or C. Z5 Fourier diagonalization exists and does not imply a work lower bound. The exact **original-variable** count, not the number of core assignments alone, is
\[
 Z(G(H))=\sum_{\sigma:V(H)\to\mathbb Z_5}
          \prod_{\{u,v\}\in E(H)}W_{\sigma(u),\sigma(v)},\qquad
 5^n\le Z(G(H))\le 5^n6^m.
\]
This identity sums over all original private-variable extensions, with multiplicities \(W_{st}\) from 1 to 6, and is not pointwise equality after deleting those variables.

Stronger: every \(G(H)\) is a syntactically three-level DAG. The assignment **all core vertices 0, all near-edge vertices 1, all central vertices 2** satisfies every arc, because \(R(0,1)=R(1,2)=1\). A blank-start original-source parser can check this three-level pattern, validate and output an explicit original-label witness in polynomial time, without recognizing the indexed LPS family or computing any graph chromatic number. On any unmatched valid input it may use correct general exhaustive search. Hence the promised SAT decision is trivially YES, including when the cofactor bound below is exponential. Full binary path consistency cannot refute these instances because the assignments actually exist; this is not an UNSAT path-consistency obstruction.

## Main theorem: expander cofactor rank and OBDD width for *every* order

**Theorem D2-T5-POSITIVE-MARGINAL-ALLORDER-RANK.** Let \(H\) be a simple d-regular graph of n vertices with second adjacency eigenvalue at most \(\lambda<d\), with max degree \(\Delta=d\), and let \(G(H)\) be the exact four-path source. For every ordering \(\pi\) of **all** \(n+3m\) original CSP variables, the pointwise Boolean indicator \(C_{G(H)}\), viewed as a rational matrix across a prefix/suffix cut of \(\pi\), has rank at least
\[
 5^k,\qquad
 k\ge\frac{(d-\lambda)n}{16d(d+1)}
\]
(up to harmless rounding). Consequently any exact five-way fixed-order OBDD for this **assignment-indicator function** has width at least \(5^k\) at some layer of **every** order. For LPS \(d=6,\lambda=2\sqrt5\), one may take \(c=(6-2\sqrt5)/672>0\), giving width at least \(5^{cn}\), or \(2^{\Omega(L/\log L)}\) in explicit source length. This is a representation lower bound, *not* a SAT-on-source decision or exact-count time lower bound.

**Proof.** Fix any variable order and stop immediately after exactly \(\lfloor n/2\rfloor\) **skeleton/core** vertices have appeared, regardless of how many private path vertices were processed earlier. Let \(U\) be that set and \(V\setminus U\) the remaining core vertices. Spectral expansion gives
\(e_H(U,V\setminus U)\ge(d-\lambda)|U|/2\ge(d-\lambda)n/8\)
for n sufficiently large. Greedily retain a crossing edge \(uv\), deleting all crossing edges incident to any vertex of \(N_H[u]\cup N_H[v]\). Each choice deletes at most \(2d(d+1)\) edges. The selected k edges form an *induced matching* in all of H, and \(k\ge(d-\lambda)n/[16d(d+1)]\).

Now sum each private variable over its full five-label domain **on the same side of the cut on which it actually occurs**. Row-side summation and column-side summation are separate linear maps \(L_\pi,R_\pi\) over Q. They transform the original Boolean cofactor matrix \(M_\pi\) into the exact weighted skeleton marginal
\[
 F_H(x_U,x_{V\setminus U})
 =L_\pi M_\pi R_\pi^\mathsf T
 =\prod_{\{u,v\}\in E(H)}W_{x_u,x_v}.
\]
Consequently \(\mathrm{rank}_{\mathbb Q} M_\pi\ge\mathrm{rank}_{\mathbb Q} F_H\), no matter where private vertices were placed in \(\pi\). Fix every core vertex outside the induced matching to 0, restricting F to a \(5^k\times5^k\) submatrix. Because no different matching endpoints are joined by an edge, that submatrix, after permuting rows/columns, is
\[
 c_0\,D_U\,(W^{\otimes k})\,D_V,
\]
where \(c_0>0\) and \(D_U,D_V\) are diagonal matrices with **strictly positive** entries produced by edges to fixed vertices. The diagonal factors are invertible over Q, and W is nonsingular, so this submatrix has rank exactly \(5^k\). This proves the original Boolean cofactor rank lower bound. A width-w deterministic five-ary OBDD has at most w distinct suffix Boolean cofactors after the cut, so its matrix has rank at most w. Hence w≥5^k on every order. No assertion is made about adaptive FBDDs, unrestricted branching programs, circuits computing the **source-level** answer, or all SAT machines. QED.

**Important semantic separation.** The 4-path lift does not make \(C_G\) rank-one: its satisfying-assignment indicator is highly nontrivial. It makes the **existential source decision** cheap because a fixed 3-layer witness works. The exponential rank remains even after allowing *any static order* of original variables, but a source-aware decider need not construct this indicator at all. Exact counting on the **general** lifted class is #P-complete by TMR-4/072's independently scoped nonnegative partition-function dichotomy application; this does **not** imply #P-hardness of the single indexed LPS sequence nor a SAT-decision lower bound.

## Same-execution resource ledger and TMR-4 interface

For an explicit input of length L, a deterministic conventional locally headed multitape machine authenticates the canonical header, all n' vertex lines, all m' unique ordered arc records and indices, builds the complete incidence table, tests the three-level source certificate, writes all n' original witness labels, then returns YES. A conservative **single-run** bound for recognized lift sources is \(T_{\rm SAT}(L)=O((L+1)^6)\), \(S_{\rm peak}(L)=O((L+1)^3)\) writable bits, including construction of the recognizable type partition, all attempted lookups, source head travel, caches, counters, complete witness output and validation. This upper bound does not rely on computing a decomposition of H or its eigenvalues.

For exact count, the *same* parser can reconstruct H and evaluate the fixed positive W table by enumerating 5^n core labelings, multiplying m original private-variable extension counts with at most O(n')-bit integers, and accumulating the exact result. A deliberately conservative same-run upper ledger is \(T_{\rm count}(L)=O(5^n(L+1)^6)\), \(S_{\rm peak}(L)=O((L+1)^3)\). General valid nonmembers retain the O(5^{n'} poly(L)) original-variable fallback; an unrecognized graph is never declared UNSAT or counted zero for free. No claim of polynomial-time exact count for LPS indexed sources.

The **D2-T5-POSITIVE-COFACTOR-TRACE** sent to TMR-4 carries (SOURCE_CURSOR, CANONICAL_ARCS, LEVEL_CERT, CORE_ORDER, PRIVATE_SUM_MAPS, CUT_EDGES, INDUCED_MATCHING, W_FIELD, COFACTOR_MATRIX, EXACT_WEIGHT_ACCUMULATORS, CACHE_STATE). Complete paid interface: READ/PARSE/GUARD, LABEL-LEVEL/DISCOVER, ARC-VERIFY, RECOGNIZE/SWITCH/FALLBACK, BRANCH_LABEL, SUM_PRIVATE, FACTOR_W, CUT/REBASE, CACHE/DROP/RECOMPUTE, EXACT_BIGINT_ADD, WITNESS/COUNT/OUTPUT/VERIFY. An adaptive solver can bypass this tensor and directly use the level certificate; arbitrary FBDD and all-machine model transfer are OPEN.

## Hostile controls, four gates and limitations

DISJ **PASS as a sanity falsifier**: DISJ's full assignment matrix can have exponential rank despite a linear-size circuit; the present theorem makes NO rank-to-general-work transfer. Horn, 2-SAT, affine/Gaussian, equality, autarky, products, bounded treewidth and tree-decomposition methods, padding, auxiliary multiplicity, source recognizers, local basis/field changes, unique-selector projection and unique-solution rank one remain legal. Our connected expander skeleton defeats a trivial *disjoint product* interpretation but is still cheap for source SAT. Fourier and characteristic-2 differences are explicit. No isolation oracle, majority/quantum claim or unrestricted field-independent inference is used.

Relativization **PASS for this restricted algebraic/graph-theoretic upper and representation theorem, OPEN for any unrestricted P!=NP bridge**; BGS, algebrization and Natural Proofs remain active. Simultaneous DTISP **PASS for one restricted constructive upper machine, NOT APPLICABLE as an FLMV contradiction**, since no superpolynomial source-decision lower bound or forbidden (T,S) pair is supplied. Deterministic configuration counting **PASS as upper-only consistency check** \(T\le2^{O(S+\log L)}\) for total halting deterministic machines, not a necessary-work lower bound or randomized/quantum argument. /341 FAIL as full logical UNSAT authority; /386 RESTRICTED.

**Executed V8**: \`experiments/tmr/tmr2_t5_fourpath_rank070.js\`, revision \`tmr2-fourpath-expanded-cofactor070.js.v1\`, no random seed; 729 exact tests, zero failures. All 25 endpoint three-variable extension counts, modular-prime-101 nonsingularity, five independently enumerated small skeleton counts, canonical source roundtrips, deterministic 3-level witnesses, malformed-source rejection, exact 25×25 conditional marginal rank, and a 25×125 raw Boolean cut reduced back to W were checked. Raw JSON: \`results/raw/tmr/2026-11-17_1512_TMR2_T5_FOURPATH_RANK070_V8_RAW.json\`. A separate locally executed CPython/SymPy verifier \`tmr2_t5_fourpath_rank070.py\`, revision v2, made 708 exact checks with zero failures, including rational rank; the Python file remains a local run artifact, not yet claimed GitHub-published. Neither program builds an eligible large-q LPS graph or executes full path consistency. Independent external mathematical review, LaTeX build, preflight on repository checkout and physical TM replay remain unperformed.

**Pinned originals and scope**: Lubotzky, Phillips, Sarnak, *Ramanujan Graphs*, Combinatorica 8 (1988), 261-277, DOI 10.1007/BF02126799; TMR-2/069 original LPS construction/report and raw; TMR-4/072 **open draft PR #231** original four-path marginal and finite audit (not represented as merged main); Bulatov-Grohe, TCS 348 (2005) DOI 10.1016/j.tcs.2005.09.011, and Govorov-Cai-Dyer, JCSS 132 (2023), DOI 10.1016/j.jcss.2022.09.002, for the general exact-count classification. These are not all independently rederived here.

## ONE next load-bearing lemma

**D2-T5-MIXED-DECISION-FBDD-OBSTRUCTION (OPEN):** Find a uniformly authentic, nontrivially mixed-YES/NO source family for which actual dynamic original-label cofactors remain quantitatively large after allowing legal source recognition, adaptive/free variable orders and all cheap algorithms. A meaningful theorem must name a restricted evaluator model and charge every transition; the all-order static OBDD rank bound above alone cannot imply unavoidable SAT decision work. P versus NP remains OPEN.
