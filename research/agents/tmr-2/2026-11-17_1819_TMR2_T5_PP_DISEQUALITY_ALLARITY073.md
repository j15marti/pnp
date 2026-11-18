# TMR-2/073 | 2026-11-17 18:19 PST | Six-arc pp-disequality, full polymorphism classification, and constructive T5 NP-hardness

**Authority/identity:** TMR-2 / PNP Information Necessity, Track A, on the 2026-11-17 FIVE-SYMBOL BEAT-RELATION CSP directive and 2026-11-15 END_TO_END_AGENT_MANUSCRIPTS ownership. The exact template is Sigma=Z5, R(a,b) iff b-a mod5 is in S={1,3}. **P versus NP OPEN.** Algebraic and reduction results below are PROVED/EXACT with external mathematical review OPEN; executable finite evidence is COMPUTATIONAL. No general SAT time lower bound.

## Candidate and falsifiers (before source search)

**Dependency D2-T5-PP-NEQ-ALLARITY-CLOSURE:** Find an authentic constant-size R-only primitive-positive definition of full two-color disequality and use it to classify ALL finite-arity T5 polymorphisms, not merely binary/affine cases. Seek a complete source-to-CSP NP-hardness transfer; do not mistake it for a lower bound on arbitrary SAT algorithms.

Falsifiers: F1 a forbidden diagonal endpoint pair or missing unequal pair in the proposed gadget; F2 a high-arity nonprojection K5 polymorphism defeating the spectral equality case; F3 nonrotation automorphisms; F4 hidden unary pins, lost auxiliary witnesses, or an incorrect counting reduction; F5 assuming that recognizing the reduction image solves the original hard source. F1/F3 checked exhaustively and proved, F2/F4 proved, F5 explicitly blocked.

**Prior-art reconciliation.** Bang-Jensen, Hell and MacGillivray (1988) already proved this T5 homomorphism problem NP-complete via their semicomplete-target theorem. TMR-5/075 (draft PR #209, not presumed merged) already proved all *binary* polymorphisms and all *affine Z5* polymorphisms are rotated projections. This result classifies *all arities and all operations* and supplies an explicit R-only reduction, without asserting research priority.

## Lemma 1: pp-disequality in six true tournament arcs

For x,y in Z5 introduce four private variables s,t,u,v and the conjunction

\[
\mathcal N(x,y)=\exists s,t,u,v\ 
 R(x,s)R(t,s)R(t,u)R(u,y)R(y,v)R(v,t).
\tag{1}
\]

Every factor denotes a real directed input arc. No disjunction or supplied color palette is used. Split it into A(x,t)=exists s R(x,s)R(t,s), and B(t,y)=exists u,v R(t,u)R(u,y)R(y,v)R(v,t). Endpoint difference masks are

\[
D_A=S-S=\{0,2,3\},\qquad
D_B=(S+S)\cap[-(S+S)]=\{1,4\}.
\]
\[
D_{\mathcal N}=D_A+D_B=\{1,2,3,4\}.
\]

Consequently \(\mathcal N(x,y)\) iff \(x\ne y\), for every endpoint pair. This is a primitive-positive definition of the complete irreflexive K5 adjacency inside T5.

Exact private-witness multiplicities must not be erased for counting. For A, the middle witness count is two for difference 0 and one for differences 2/3. For B, the ordered pair count is two at differences 1/4 and zero otherwise. Their convolution gives the exact four-private-variable matrix
\[
W=\begin{pmatrix}
0&6&2&2&6\\
6&0&6&2&2\\
2&6&0&6&2\\
2&2&6&0&6\\
6&2&2&6&0
\end{pmatrix}.
\tag{2}
\]
It has Boolean support \(W(x,y)>0\) iff \(x\ne y\), but is not a uniform count-preserving relation.

## Theorem 2: every polymorphism is a rotated projection

For every integer \(k\ge1\), the entire k-ary polymorphism set of T5 is
\[
\operatorname{Pol}_k(T5)
=\{(x_1,\ldots,x_k)\mapsto x_i+c\bmod5:\ 1\le i\le k,\ c\in Z5\}.
\tag{3}
\]
There are exactly 5k such operations. Its idempotent reduct has only coordinate projections. In particular there is no nontrivial Taylor/Siggers/majority operation; no tractable Taylor polymorphism was overlooked.

**Complete proof.** Primitive-positive definitions are preserved by polymorphisms: given k satisfying input tuples and the k separate choices of witnesses in (1), apply f coordinatewise to each witness group; every resulting arc remains an R arc. Thus f preserves disequality. Define H_k as the categorical graph product K5^k, adjacent when all k coordinates differ. Then f:H_k -> K5 is a proper five-coloring.

The adjacency matrix of H_k is \((J_5-I_5)^{\otimes k}\), with N=5^k vertices, degree d=4^k and eigenvalues \((-1)^j4^{k-j}\) for 0<=j<=k. Its minimum is tau=-4^{k-1}. Hoffman's independent-set ratio bound is
\[
\alpha(H_k)\le N(-\tau)/(d-\tau)=5^{k-1}.
\]
The five color fibers partition all N vertices and are independent, so each has size exactly 5^{k-1} and attains equality. Equality in the spectral proof puts each centered fiber indicator in the tau-eigenspace, which is precisely the sum of the k coordinate-first-order eigenspaces. Therefore each fiber indicator is of the form \(1/5+\sum_i g_i(x_i)\), where each \(g_i\) has zero mean. A Boolean additive function cannot depend on two distinct coordinates: choose one strictly increasing pair in each, observing that each increase of a Boolean value must be 1; together the two increments force 2, impossible. Thus each color fiber is a cylinder \(x_i=a\) for one i, and its cardinality forces precisely one a. Cylinders from different coordinates intersect, so the five disjoint fibers use one common coordinate i. Hence f(x)=pi(x_i) for a permutation pi of Z5.

The previously proved unique-successor gadget \(R(a,b)\land \exists w R(a,w)R(w,b)\) has support exactly \(b=a+1\bmod5\). Every T5 automorphism pi preserves this pp relation, hence pi(a+1)=pi(a)+1, forcing pi(a)=a+c. All rotations preserve R. QED. The k=1 argument also proves all endomorphisms are automorphisms, so the template is a core. No 0-ary constant polymorphism exists because R is irreflexive.

The finite-domain algebraic dichotomy is consistent with this no-Taylor core. The following fully explicit reduction establishes NP-hardness without requiring that dichotomy.

## Theorem 3: explicit 3-COLOR -> T5-HOM reduction with source costs

For a finite simple undirected H on n explicitly declared vertices and m edges, add two adjacent universal vertices p,q. The resulting H' has n+2 vertices and m+2n+1 edges, and H is three-colorable exactly when H' is five-colorable. For each edge {x,y} of H' in canonical endpoint order, insert an independent fresh copy of the **six R arcs/four private vertices** in (1). Let D(H) be the fully encoded resulting directed graph. It contains exactly
\[
|V(D)|=9n+4m+6,\qquad |E(D)|=12n+6m+6.
\tag{4}
\]

Every H' five-coloring extends to a T5 assignment by Lemma 1 independently for every edge. Every T5 assignment restricts to a proper H' five-coloring and thus a three-coloring of H. Therefore the directed reduction is a polynomial many-one reduction in the correct direction \(3\text{-COLOR}\le_m^P T5\text{-HOM}\). T5-HOM is in NP because all declared vertices receive five-symbol labels and all arcs can be checked, so T5-HOM is NP-complete by an explicit proof (not a new complexity result).

**Full source pipeline:** read complete explicit undirected graph, reject malformed records, add the two universal vertices/edges, sort their endpoint pairs, create exactly four named new vertices for each edge, output exactly six canonical sorted arcs, then verify the emitted target's explicit vertex declarations and arc identities. On an ordinary fixed multitape bit machine with binary identifiers and one actual source, the construction can be conservatively implemented in O((L+1)^6) time and O((L+1)^3) peak writable bits, with all original reads, sorting, address indices, temporary buffers, failed syntax checks, output and verification charged. Encoded output is O((n+m) log(n+m)) bits. No auxiliary oracle, undischarged preprocessing or free witness supplied. An image recognizer may reverse this particular canonical construction but obtains an instance of general 3-COLOR, not a polynomial solver.

**Pointwise/count firewall.** For a graph H without the two universal vertices, the lifted T5 source has
\[
\#T5(\mathrm{Lift}(H))=
\sum_{\chi:V(H)\to Z5}\prod_{\{x,y\}\in E(H)}W(\chi(x),\chi(y)).
\tag{5}
\]
Boolean existential projection is the five-colorability predicate, but (5) has pair-dependent weights (2/6). For one undirected edge, five-colorings=20 but exact original T5 accepting assignments=80. This reduction is **NOT parsimonious** and makes no unsupported exact #P-completeness transfer.

## New TMR-4 invariant and legal alternative executions

**D2-T5-PP-NEQ-WITNESS-TRACE** records after actual source-derived gadget elimination a weighted boundary function
\[
I_t(b)=\sum_{\chi\text{ on processed variables},\ \chi|_{\partial F_t}=b}
\prod_{e\in F_t}W(\chi(e_1),\chi(e_2)),
\]
with the Boolean support quotient separated. Exact transition interface: SOURCE-READ; CANONICAL-PARSE/VALIDATE; IDENTIFY/GENERATE ALL SIX ARCS; AUTHENTICATE FOUR PRIVATE VERTICES; BOUNDARY-LABEL-ASSIGN; SUM THE PRIVATE WITNESSES; RETAIN/FORGET ORIGINAL VERTICES; INTEGER-WEIGHT-CONTRACT; CACHE/RECOMPUTE/SWITCH; COUNT OR DECIDE; VERIFY OUTPUT. Source recognition, graph-coloring, component splitting, Gaussian/affine, bounded-treewidth DP, adaptive variable orders, FBDD/OBDD, memoization and all legal inexpensive alternatives remain available. No representation width is converted into unavoidable decision time.

A concrete falsifier for unsound count projection: replacing W by its Boolean support makes the one-edge exact count 20 instead of 80. A second falsifier for compulsory work: obvious source-reconstructible graph families may have large prescribed tensor width but cheap recognition and direct witness generation. The new invariant is a correctly costed transfer object, not a work lower bound.

## Executed evidence, gates, controls and pinned references

**Published executable:** experiments/tmr/tmr2_t5_ppneq073.js, Node 22, revision tmr2-t5-ppneq073-js.v1, seed 2026111718. **Published immutable raw:** results/raw/tmr/2026-11-17_1819_TMR2_T5_PPNEQ073_NODE_RAW.json. Actual local execution: **194 checks, zero failures**, including 25 gadget endpoint pair counts, all 32 mask propagation maps, all 3,125 endomorphism candidates, all 75 simple undirected graphs up to n=4 with canonical T5 source generation/parsing and weighted support comparison, an original 5^6-label brute-force lifted edge (exact count 80), the K6 unsatisfiable control, malformed-input rejection and sharp-Hoffman arithmetic for k<=8. Separate local independent CPython implementation, seed 202611171819, completed **511 checks, zero failures** with 60 seeded random graphs; its exact source is not claimed GitHub-published. Finite audit remains COMPUTATIONAL, not a proof of the k-universal assertion.

Original R circulant has eigenvalues \(\zeta^j+\zeta^{3j}\), determinant 2, and rank 5 over Q/C/odd characteristics versus 4 over F2. This must not be mistaken for H_k's real symmetric tensor-product matrix or for an algorithmic lower bound.

**Four gates.** DISJ sanity **PASS scoped**: no static-rank work inference; all easy Horn, 2-SAT, affine, product, selector, unique-solution and compact-circuit controls stay legal. Relativization **PASS for local algebra/reduction only**; any NP separation is OPEN and no nonrelativizing or algebrization/Natural Proofs workaround is asserted. Simultaneous DTISP **PASS for one restricted reduction upper-time/upper-space realization only**, no forbidden-region or all-algorithm lower bound. Deterministic configuration counting **PASS upper-bound consistency only**; \(T\le2^{O(S+\log L)}\) for a total deterministic machine, never a necessary-work lower bound and not automatically randomized/quantum. Unexecuted family controls remain OPEN, not silently passed. /341 FAIL as full UNSAT authority; /386 RESTRICTED.

**Primary sources:** Bang-Jensen, Hell and MacGillivray, *The Complexity of Colouring by Semicomplete Digraphs*, SIAM J. Discrete Math. 1 (1988), 281-298, https://doi.org/10.1137/0401029. W. H. Haemers, *Hoffman's Ratio Bound*, Linear Algebra Appl. 617 (2021), 215-219, https://doi.org/10.1016/j.laa.2021.02.010. Graph k-coloring k>=3 classical NP-hardness, e.g. Karp (1972) and Garey, Johnson, Stockmeyer (1976). Related project reports: TMR-2/072 and TMR-5/075 (draft). External mathematical review OPEN; this run did NOT execute full manuscript LaTeX, checkout preflight, native TM microtrace or unrelated model formalizations.

**ONE next lemma: D2-T5-IMAGE-MIXED-DYNAMIC-COUNT-BOUNDARY (OPEN).** For authentic YES/NO 3-COLOR-to-T5 images, construct and compare the actual source-recognized 3-coloring solver path with weighted W contraction, exact boundary/cofactor states and adaptive FBDD/OBDD costs on the same graphs. Seek an explicit restricted-model representation lower bound with correct input transitions and multiplicities, or exhibit the first cheap legal falsifier. P versus NP remains OPEN.
