# TMR-2/091: sharp girth-five cycle-rank obstruction and paid endpoint-cofactor witness

**Owner:** TMR-2, PNP Information Necessity. **Date:** November 18, 2026, America/Los_Angeles. **Primary object:** fixed-template five-label digraph CSP \(R(a,b)=[b-a\pmod5\in\{1,3\}]\). **Status:** analytic scoped theorem; finite enumerations independently checked by direct assignments and feedback-edge tree DP. This is not a lower bound on unrestricted computation.

## 1. Source-aware, five-state path-cofactor algebra

Let \(S\) denote cyclic shift on the five terminal differences, so that the directed-edge transfer is \(A=S+S^3\). An edge followed against its orientation contributes \(A^\top=S^2+S^4=AS\). Since these circulant matrices commute, a source path of length \(\ell\) with \(r\) reversed arcs has exact original-label endpoint cofactor
\[
 K_{\ell,r}=A^\ell S^r=S^{\ell+r}(I+S^2)^\ell.
\]
Its five row counts are cyclic translates and sum to \(2^\ell\). The exact positive-support cardinalities are **2, 3, 4 and 5** for \(\ell=1,2,3,\ell\geq4\), independent of arc orientation. For \(\ell\leq4\), the \(\ell+1\) exponents \(\ell+r+2j\pmod5\) are distinct; for longer paths, multiplication by \(A\) or \(A^\top\) preserves strictly positive rows. These are genuine source-to-source transition cofactors, not a static matrix rank argument.

For internally vertex-disjoint paths \(P_i\) sharing terminals \(u,v\), independence of internal variables and global cyclic color symmetry give
\[
Z=5\sum_{d\in\mathbb Z_5}\prod_i K_i(0,d).
\]
The recognition and traversal of paths, source parsing, cyclic gauge, integer multiplication, and all intermediary storage must be paid separately. Computing a row with the intentionally simple evaluator uses ten integer accumulator updates per original edge; no general upper/lower bound is inferred from that specific implementation.

## 2. Analytic theorem: girth at least five plus cycle rank at most two forces SAT

**Theorem 091-A (sharp in feedback-edge number).** Let \(G\) be any **simple oriented** graph, with no loops or antiparallel arc pairs, whose underlying undirected girth is at least five and whose total cyclomatic number
\(\beta(G)=|E|-|V|+c(G)\) is at most two. Then \(G\to T_5\).

**Proof.** Trees are satisfiable by extending each assigned parent over an outgoing or incoming arc (two choices). Any oriented cycle is satisfiable: a three-cycle orientation maps to a directed or transitive triple in \(T_5\); a cycle of length four can be cut into a three-edge path (terminal support four) and a one-edge path (support two), whose supports intersect; for length at least five, a four-edge subpath has full endpoint support, and the remaining edges can be satisfied. Vertex transitivity makes the cycle-extension compatible with any preassigned articulation label.

A connected core with at most two independent undirected cycles is a cycle, two cycles connected by bridges or articulation points, or a **theta** comprising three internally disjoint paths between two branch vertices. Tree attachments never prevent a solution, and two separate cycle blocks can be glued through articulation vertices or bridges. For the theta, write path lengths \(a\leq b\leq c\); girth at least five gives \(a+b\geq5\). If \(a=1\), then \(b,c\geq4\) and their endpoint supports are full. If \(a=2\), then \(b,c\geq3\): the three supports have sizes at least \(3,4,4\), hence their intersection contains at least \(3+4+4-2\cdot5=1\) difference. If \(a\geq3\), all three support sizes are at least four and intersection size at least two. Thus every theta core is satisfiable. Components multiply. QED.

**Sharpness:** cyclomatic number three suffices for UNSAT at girth five. Thus any UNSAT simple oriented source of girth at least five must have \(\beta\geq3\); this is a **source structural necessity**, not a computational lower bound. The girth assumption matters: \(K_4\) minus one edge, oriented as \(0\to1\to2\to3\), \(0\to3\) and \(1\to3\), is UNSAT with four vertices, five edges, \(\beta=2\), girth three. A three-path \(K_{2,3}\) with words \(++,+-,--\) is UNSAT at girth four, with five vertices and six edges.

## 3. Explicit smallest-cycle-rank girth-five counterexample

Take four internally vertex-disjoint paths between terminals \(u=0\) and \(v=1\), in terminal traversal order, with orientation words
\[
 P_1=++,\qquad P_2=+++,\qquad P_3=++-,\qquad P_4=---.
\]
The resulting source has \(n=9\), \(m=11\), undirected girth five, \(\beta=3\) and no direct terminal edge. Its exact five-dimensional endpoint rows, indexed by \(d=v-u\pmod5\), are
\[
\begin{array}{c|rrrrr|l}
 &0&1&2&3&4&\text{forbidden }d\\\hline
 ++&0&1&1&0&2&\{0,3\}\\
 +++&3&0&3&1&1&\{1\}\\
 ++-&1&3&0&3&1&\{2\}\\
 ---&3&1&1&3&0&\{4\}
\end{array}
\]
The union of the four forbidden-difference sets equals all five residues. Hence the supports have empty four-way intersection and the instance is **exactly UNSAT**. No assignment to the two terminals extends through all four source paths. This is a direct zero-cofactor certificate with **four legal source factors**, not an appeal to increasing static rank.

Removing any entire path leaves positive exact counts, respectively \(90,15,15,10\). Removing any single one of the eleven original directed edges yields SAT. Reversing only the first arc \(0\to2\) produces a matched-skeleton YES source with exactly **135** original-label solutions and witness \((0,0,2,1,2,3,1,2,1)\). The exact canonical NO source is 112 ASCII bytes, SHA256 `f7afe7fd50158319162328eaf16d73ca71d2ed54936959c5d41ec24268eac42d`.

For the length pattern \((2,3,3,3)\), exhaustive evaluation of its \(2^{11}=2048\) arc orientations gives **36 NO and 2012 YES**. All 4096 orientations of the four-path \((3,3,3,3)\) bundle are YES (also follows from four sets each of size four in a universe of five). All 4096 orientations of \(K_4\) with each original edge subdivided into two directed arcs are YES, with a minimum of five allowed assignments to the four original branch vertices. These last two results are **finite computational controls**, not an unrestricted classification of \(\beta=3\).

## 4. Actual source costs and comparable algorithms

The four endpoint paths have lengths totaling eleven. A fixed order of simple five-state cofactor propagation performs **110 accumulator updates**, then **15 multiplications over the five residues** to form the four-factor products, followed by five-residue aggregation and the global gauge factor of five. Paid costs additionally include source authentication, locating the degree-two paths, checking endpoints and multiplicities, allocations and integer bit arithmetic. The existence decision may use just five-element support masks; zero sets \(\{0,3\},\{1\},\{2\},\{4\}\) cover all terminal differences. Both the original source and its reversed-edge YES control are recognized without search.

An independent original-label depth-first verifier visits **196 recursion nodes** on the NO instance. A separately coded spanning-forest exact-counting DP, with three feedback edges and four distinct chord endpoints, examines **625 pinned endpoint states**; 585 fail their chord tests, 40 invoke tree evaluation. Both return exact integer zero. The one-flip YES source has count 135 by direct DFS, the feedback-edge DP, and explicit witness checking.

On the earlier four-variable /087 NO source, ex post **reduced OBDD width is 1** for all orders because the full original-label truth function is constant zero. Its one-edge-flipped YES counterpart has minimum and maximum peak cofactor width six over all 24 orders; for the five-variable \(K_{2,3}\) counterpart these are likewise six across 120 orders. An ex post OBDD width of one does **not** entail a constant-time algorithm for discovering UNSAT. Source-aware construction/search cost must be charged.

For any \(k=\beta(G)\), a straightforward exact algorithm chooses a spanning forest, enumerates color assignments to endpoints of the \(k\) nonforest edges (at most \(2k\) distinct pinned vertices), rejects incompatible chords, and counts residual forest assignments with five-state tree messages. This has a transparent \(O(5^{2k}\operatorname{poly}(N))\) arithmetic-operation upper bound, plus integer bit costs, and remains valid for disconnected graphs. The local full auditor checked this algorithm against independent direct DFS on 120 seeded small forests, unicyclic and bicyclic orientations, with exact agreement.

## 5. TMR-4 handoff, novelty and safeguards

**D2-T5-GIRTH5-BETA3-FOUR-PATH-COVER091:** store the source-certified theta decomposition; each five-entry path cofactor and zero-support mask; the five-way terminal-difference coverage certificate; \(n,m,c,\beta,g\); all 11 edge-critical deletion checks; the matched YES witness and exact counts; and **paid** parsing, path recognition, transfer arithmetic, pinned-tree DP, source compression and cache costs. This supplies an explicit smallest-\(\beta\) counterexample to extrapolating girth-five \(\beta\leq2\) satisfiability, while demonstrating that even a critical NO with girth five has a tiny recognizable certificate.

Next target: construct mixed YES/NO sources with **growing** feedback-edge number, high girth and high irreducible residual structure after deleting degree-one vertices, suppressing degree-two paths, recognizing multi-path bundles and running exact tree and separator DP. Do not mistake source-size complexity of a certificate, a cofactor representation, or an extensional branching program for necessary unrestricted runtime. NP-completeness of fixed T5 is established independently [1], but **P versus NP remains OPEN**. Full LaTeX compilation, external proof review, native repository preflight and physical Turing-machine replay remain open.

**Artifacts:** `experiments/tmr/tmr2_t5_bicyclic091_compact.py`, `results/raw/tmr/2026-11-18_1212_TMR2_T5_BICYCLIC091_SCOPED.json`, `main2_PNP_INFORMATION_NECESSITY.tex`.

**References.** [1] Bang-Jensen, Hell, MacGillivray, *The Complexity of Colouring by Semicomplete Digraphs*, SIAM J. Discrete Math. 1(3) (1988), 281–298, https://doi.org/10.1137/0401029. [2] Zhuk, *A Proof of the CSP Dichotomy Conjecture*, JACM 67(5) (2020), https://doi.org/10.1145/3402029. These sources classify the general target; the present bounded-cycle-rank theorem is an independently proved restricted statement.
