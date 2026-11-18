# TMR-2/077 | 2026-11-17 22:56 PST | Mixed fixed-T5 high-girth expander pair, local-consistency survival, and direct field-uniform rank

**Owner:** TMR-2 / PNP Information Necessity. **Status:** PROVED/EXACT restricted symbolic construction conditional only on explicitly cited established graph theorems; independent external mathematical review OPEN. New mixed cover/switch theorem and direct indicator-rank calculation are separated from the previously proved TMR-2/069 LPS high-girth UNSAT family, TMR-5/071 path-consistency lemma, and TMR-2/071 adaptive NROBP result. Finite controls are COMPUTATIONAL. P versus NP remains OPEN.

## ONE end-to-end target, quantifiers, and four falsifiers

Dependency **D2-T5-SWITCHED-COVER-PC-RANK-TRACE**: produce, for infinitely many exact serialized ordinary five-label sources of the same length, a YES/NO pair with identical number of vertices and arcs, full undirected degree sequence, connectedness, constant-degree expansion, undirected girth at least seven, directed acyclicity, and failure of full binary path consistency to distinguish the labels. On the YES half prove a *nonzero*, exponential lower bound for **every fixed-order pointwise five-ary OBDD** over every field, but independently exhibit polynomial source-authenticated SAT-decision fast paths for BOTH halves. No inference to all-algorithm necessary time.

Predeclared falsifiers: (F1) the LPS component is bipartite, has the wrong spectrum or insufficient girth; (F2) a multi-edge switch introduces a short cycle, disconnects the NO graph, or destroys expansion; (F3) deleting the selected edges increases independence enough to permit a five-coloring; (F4) auxiliary cross constraints destroy the claimed field-uniform induced-matching submatrix. Each is treated in the proof, with F1 dependent on external pinned graph theorems. A fifth scientific escape is the legitimate polynomial source-recognizing algorithm; **it remains legal and defeats any unrestricted work lower-bound interpretation**.

## Original explicit source model

Let \(\Sigma=\mathbb Z_5\) and \(R(a,b)=[b-a\bmod5\in\{1,3\}]\). The sole decision question for an original source digraph \(G\) is whether \(\prod_{u\to v\in E(G)}R(x_u,x_v)=1\) for some \(\Sigma\)-labeling. Use the canonical complete ASCII grammar \`p t5 n m\` followed by \`v 0,...,v (n-1)\` and distinct sorted \`a u v\` records; reject malformed source. Every constructed arc points from a smaller ID to a larger one. This is the *fixed* T5 template, NOT the growing alphabet supplement.

Import TMR-2/069's **nonbipartite** \(d=74\) regular LPS Cayley graph \(X=X^{73,q}\) on \(N=q(q^2-1)/2\) vertices, for primes \(q>73^3,\ q\equiv1\pmod{292}\). The literature and /069's charged constructor give connected simple \(X\), \(g(X)\ge7\), and all nontrivial adjacency eigenvalues in \([-\lambda,\lambda]\), \(\lambda=2\sqrt{73}\). Its ordinary edge expansion is at least
\[
e_X(U,\bar U)\ge h\,\min(|U|,N-|U|),\qquad h=(d-\lambda)/2>28.
\]
Hoffman's bound gives
\[
\alpha(X)\le\rho N,\qquad \rho=\frac{\lambda}{d+\lambda}<0.18760<1/5.
\]
The family generation, modular root/four-square search, group enumeration and graph authentication are exactly those explicitly priced in /069. No qualifying \(q>73^3\) graph was generated in /077.

## New MULTISWITCH pair theorem

Set \(\kappa=1/(100d^6)\) and \(t=\lfloor\kappa N\rfloor\) (positive for eligible \(q\)). Greedily select the lexicographically first available \(t\) edges \(F=\{\{a_i,b_i\}\}\subset E(X)\) so that every endpoint of one selected edge is graph-distance **at least seven** from every endpoint of another. A radius-six ball contains at most \(1+d\sum_{j=0}^5(d-1)^j\le7d^6\) vertices, so selecting one edge eliminates at most \(14d^7\) candidate edges. There are \(dN/2\) edges: the greedy procedure can choose at least \(N/(28d^6)\), more than the requested \(t\). In particular \(F\) is a matching and \(t=\Theta(N)\) with an extremely small constant.

**YES:** the connected bipartite double cover \(Y=X\times K_2\), with vertices \(u_0\in[0,N)\), \(u_1\in[N,2N)\), has edges \(u_0v_1,\ v_0u_1\) for each undirected \(uv\in X\). Orient every edge from layer 0 to layer 1. Assign label \(A=0\) to all layer-0 vertices and \(B=1\) to all layer-1 vertices. More strongly,
\[
Z(Y)\ge 5\,2^N>0
\]
because for any of five constant colors on layer 0, each layer-1 vertex independently chooses one of its two outneighbors.

**NO:** begin with two disjoint copies of \(X\). Remove the two copies of every edge \(\{a,b\}\in F\); add the two cross-layer edges \(a_0a_1\) and \(b_0b_1\). Orient every resulting edge from its smaller canonical index to its larger. Call the graph \(Z\). Exactly \(2t\) cross-layer edges form a matching. Since \(F\) is a matching, each vertex loses and gains one edge. Its two within-layer graphs are copies of \(X-F\).

For both \(Y,Z\), exactly \(n=2N\) original variables, \(m=dN\) original arcs, all undirected degrees \(d=74\), one connected component, and an acyclic orientation with no loops, opposite arcs, triangles or four-vertex cycles. Both have undirected girth at least seven. For \(Z\), any new cycle uses at least two cross-layer edges. Each intervening within-layer path between distinct switched edges is of length at least seven; between the endpoints of the SAME removed edge it is at least \(g(X)-1\ge6\). Hence every new cycle has length at least 14; surviving old cycles have length at least seven.

Let \(h'=h-1>1\). Removing the matching \(F\) lowers the within-copy cut size by at most \(\min(|U|,N-|U|)\), so \(X-F\) remains connected and retains edge expansion at least \(h'\). The \(2t\) cross-layer edges make \(Z\) connected. For any vertex subset \(S\subseteq V(Z)\), \(|S|\le N\), write \(s_i=|S\cap X_i|\) and \(a=\min(s_0,N-s_0)+\min(s_1,N-s_1)\). If both \(s_i\le N/2\), its within-copy edge boundary is at least \(h'|S|\). Otherwise, up to relabeling, \(s_0>N/2,\ s_1\le N/2\). Then \(a\) is the number of membership changes from the whole first copy, and
\[
e_Z(S,\bar S)\ge h'a+\max(0,2t-a)\ge t\ge (t/N)|S|.
\]
Therefore \(Z\) is also an **edge expander with a positive uniform asymptotic constant**, not a disguised two-edge-cut graph. Both graphs have linear undirected treewidth by their degree-bounded edge expansion.

The independence number obeys
\[
\alpha(Z)\le2\alpha(X-F)\le 2(\rho N+t)<2N/5,
\]
as removing \(t\) edges increases maximum independence by at most \(t\). Thus \(\chi(Z)\ge6\). A homomorphism to any loopless five-letter tournament would induce a proper five-coloring of the underlying undirected graph. Hence
\[
\boxed{Z(Y)\ge5\,2^N,\qquad Z(Z)=0.}
\]

**Full path consistency:** both underlying graphs have girth at least seven. TMR-5/071 and TMR-2/069 already proved the all-orientations signed-short-path *nonempty post-fixpoint*. The 1-, 2-, 3-, and 4-edge path images in \(\mathbb Z_5\) have sizes 2,3,4,5; length-four images are universal. Consequently standard complete binary \((2,3)\) path consistency leaves every unary support nonempty on BOTH graphs. This lemma is prior work, not claimed new in /077.

## Direct five-ary cofactor/OBDD rank on the SAME YES source

The positive indicator \(C_Y(x)\) is not a zero tensor. The double cover \(Y\) is a connected \(d\)-regular bipartite graph with algebraic second eigenvalue at most \(\lambda=2\sqrt{73}\). For **every** order of its \(n=2N\) original five-label variables, the prefix \(S\) of length \(n/2\) has
\[
e_Y(S,\bar S)\ge(d-\lambda)n/4.
\]
Greedy deletion of at most \(2d^2\) crossing edges per picked edge gives an **induced** crossing matching of size
\[
r\ge\frac{d-\lambda}{8d^2}\,n,\qquad
c=\frac{74-2\sqrt{73}}{8\cdot74^2}=0.001299123\ldots.
\]
Fix every unselected layer-0 variable to \(A=0\), and every unselected layer-1 variable to \(B=1\). Allow each selected layer-0 matching endpoint the palette \(U=\{A,D\}=\{0,3\}\) and each selected layer-1 endpoint \(V=\{B,D\}=\{1,3\}\). Every constraint involving fixed vertices is satisfied; the induced-matching property leaves only independent selected edges. Each selected edge has the exact \(2\times2\) relation
\[
R|_{U\times V}=\begin{pmatrix}1&1\\1&0\end{pmatrix}.
\]
Thus the original full-assignment indicator's prefix/suffix flattening has a literal submatrix equal, up to row/column permutations and transposes, to \((R|_{U\times V})^{\otimes r}\). Its determinant is \(\pm1\) and its rank is \(2^r\) **over every field**, including \(\mathbb F_2\), despite the full \(5\times5\) T5 relation having characteristic-two rank 4. Therefore every exact five-ary **fixed-order pointwise OBDD** for \(C_Y\) has width at least \(2^{cn}\). This is NOT a general decider lower bound; earlier /071 had a separate stronger adaptive NROBP result by a different matching-width theorem.

For the NO source, the final pointwise indicator and every semantic cofactor are zero. Its final flattened rank is zero. The same \(n,m,d\), girth, PC, expansion and acyclicity therefore do not force any positive final semantic rank.

## End-to-end source cost, controls and evidence

Parse and authenticate complete original source. For the YES half, standard bipartition and arc-direction checks directly yield and verify the genuine T5 witness. For the canonical NO half, regenerate the parameter-indexed \(X\), the greedy set \(F\), both switched layers, and compare the complete sorted source arcs before outputting UNSAT. Both are source-only deterministic polynomial-time fast paths; valid nonmembers use full original-label exhaustive DFS. All construction, root/primality checks, group BFS, selected-edge shortest distances, edge generation, sorting, rechecking, witnesses, caches, switching, arithmetic and output have conservative SAME-realization bounds on **recognized** sources \(T(L)=O((L+1)^9)\), \(S_{\rm peak}(L)=O((L+1)^4)\) writable bits. No precomputed decomposition or spectral advice is supplied. These generous bounds are upper estimates, not physical TM microtraces.

**Named TMR-4 invariant:** D2-T5-SWITCHED-COVER-PC-RANK-TRACE. State: fully parsed original byte cursor; source vertices/arcs; p,q and LPS generator/PSL element tables; 5-bit AC masks and all 25-bit pair masks; complete short-path orientation signatures; selected distant-edge matching F; switched/copy incidence; spectral preconditions; YES witnesses; induced crossing matching, two-letter palettes, actual cofactor row/column and rank computations with all arithmetic precision; alternative source recognizers, cache/eviction/switch/fallback, and output. Charge every READ, AUTHENTICATE, BUILD, DISTANCE, SELECT, SWITCH, SORT, PC-UPDATE, MATCH, FIX/COFACTOR, RANK, WITNESS/VERIFY, EARLY-EXIT, CACHE/RECOMPUTE and OUTPUT transition. None is compulsory for an arbitrary decider.

**Actually executed local, finite only:** CPython stdlib \`tmr2_t5_mixed_girth_expander077.py\` had 71 final assertions, zero failures, six canonical source examples built from \(C_7,C_9,K_8\), all connected and degree/arc preserving; four independent cut-submatrix rank checks over fields \(2,3,5,7\), with matching sizes \(3,4,4,4\); YES witness checks; full path consistency on girth-14/18 controls; a K8-switch NO certificate (a surviving K7) and short-girth PC negative control; malformed source rejection. A separate independently implemented local CPython high-girth audit \`tmr2_t5_girth7_pc077.py\` ran 5,333 assertions across 18 source graph/orientation controls and an independent full PC implementation through 24 vertices, but only **replicates the PRIOR /069 and TMR-5/071 theorem**, so it is not presented as mathematical novelty. **No eligible large p=73 LPS source, combined high-girth chromatic-six instance, source-authenticating LPS parser, or physical TM microtrace has been executed in /077.** The finite source/rank audits do not prove the infinite external-source or asymptotic width claims.

A separately executed compact stdlib auditor \`tmr2_t5_mixed_degree077_compact.py\` logs 47 checks and zero failures; SHA256 \`e03d627d3ddb4915b00688ab38c4286c69d08724378033bcb9ce667bad8b4dca\`. Its results match the relevant full-audit structural and modular-rank checks. Reproduced data paths are published separately where possible; unpublished local full audits are NOT represented as repository blobs.

**Four mandatory gates:** DISJ **PASS restricted**, and any inference from final rank to necessary work **FAIL**. Relativization **PASS for the local combinatorial theorem, OPEN for an unrestricted nonrelativizing P-vs-NP transfer**; algebrization/Natural Proofs OPEN. Simultaneous DTISP **PASS same-run polynomial source-recognition upper / OPEN any forbidden general lower pair**. Deterministic configuration counting **PASS upper-only guard**, never used as a work lower bound. Horn/2-SAT, affine/Gaussian, bounded-treewidth, equality, autarky, low-degree, clique, source generation/recognition, bipartiteness, separator, module/twin, algebraic counting, field choice, fully reduced OBDD, recomputation, randomness, independent product, padding and selector shortcuts remain legal. /341 remains FAIL as full UNSAT authority; /386 RESTRICTED.

**Primary sources / provenance:** (1) LPS, *Ramanujan Graphs*, Combinatorica 8 (1988), https://doi.org/10.1007/BF02126799 ; (2) Knuth/Stanford GraphBase quaternion girth derivation, https://sources.debian.org/src/sgb/1:20210202-2/girth.w ; (3) TMR-2/069 https://github.com/j15marti/pnp/blob/main/research/agents/tmr-2/2026-11-17_1412_TMR2_LPS_UNIFORM_PC069.md ; (4) TMR-5/071 path-consistency proof, as credited by /069; (5) TMR-2/071 pointwise restriction and Razgon-style branching lower bound. The new contribution of /077 is the **many-edge switched matched-expander pair** plus the **direct field-uniform indicator flattening on exactly the positive half**.

**ONE next dependency:** D2-T5-MIXED-SOURCE-UNRECOGNIZED-DECISION-OBSTRUCTION (OPEN). Produce authentic mixed instances whose YES-side *positive* cofactors survive the cheap source-recognizing fast paths, and prove a lower bound for a declared source-aware adaptive evaluator after paying authentication, component/bipartition/expansion checks, decomposition, cached shared states and all alternative algorithms. The new pair is a stronger false-positive control, **not** a lower bound for unrestricted SAT machines. P versus NP remains OPEN.
