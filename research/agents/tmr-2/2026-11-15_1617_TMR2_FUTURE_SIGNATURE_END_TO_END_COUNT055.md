# TMR-2/055: Source-authenticated exact #CNF and a future-signature quotient of neighborhood rank

**November 15, 2026, 16:17 PST.** Owned Track A. Revision \`TMR2_FUTURESIGNATURE_E2E055_v3\`, deterministic seed 20261115. Restricted symbolic lemmas: **PROVED/EXACT, independent mathematical review OPEN**. Finite executable tests: **COMPUTATIONAL**. No general SAT-time lower bound, no unrestricted circuit transfer. **P versus NP remains OPEN.**

## Chosen chain and precommitted falsifiers

**D2-COUNT-PIPELINE:** authentic DIMACS CNF bytes -> parse/authenticate a canonical proper width-three gadget -> recover cross-only bipartite graph and its actual edge list -> detect a disjoint matching (or use fully charged general neighborhood-state counting DP) -> compute the **exact number** of satisfying assignments -> print the integer. For other valid width-at-most-three CNFs, perform an explicitly exponential exhaustive count; reject malformed syntax. Thus the implementation is an all-valid-source exact counting algorithm, NOT a claimed polynomial-time general #SAT solver.

**Named dependency closed:** D2-SOURCE-QUOTIENT. The previously computed fixed-formula cut rank \`r\` is connected to a real source recognizer, complete exact-count evaluator and a strictly coarser *future-count-continuation* quotient with an explicit transition interface for TMR-4. The previously open step from high rank to mandatory counting work is **falsified for the matching subfamily**, not transferred to unrestricted algorithms.

Falsifiers, specified before the literature/corpus verification: (F1) two unions with equal future cardinality signatures might produce different exact counts under the same continuation; (F2) the seven pin clauses may multiply the count or admit a second extension; (F3) finding the compact quotient may itself require exponentially many future evaluations; (F4) rank \`2^k\` might misleadingly be interpreted as necessary exact-count work despite a source-recognized polynomial evaluator. F1 and F2 are ruled out by proof, F3 is an **authentic caveat**, and F4 is a **legal cheap counteralgorithm**.

## Encoding and semantics, including both labels and counts

Let \`A={1,...,a}\`, \`B={a+1,...,a+b}\`. The source is a genuine DIMACS CNF with header \`p cnf a+b+3 m+7\` and a comment \`c split a b\`. An ordered block of seven ternary clauses on fresh variables \`p,q,r\` excludes every value of the triple except \`000\`: for nonzero mask \`z=1,...,7\`, clause \`(ell_p OR ell_q OR ell_r)\` has \`ell_i=-i\` when mask bit i=1, and \`ell_i=i\` otherwise. Each graph edge \`(u,v)\`, with \`u in A,v in B\`, contributes \`(-u OR -v OR p)\`. All clauses have three distinct variables, no duplicates, and the seven pins force \`p=q=r=0\`.

There is **exactly one** extension to pins for each independent-set assignment of original vertices; forbidden edge assignments have no extension. Therefore
\[
\#F_G=\sum_{S\subseteq A}2^{b-|U(S)|},
\qquad U(S)=\bigcup_{u\in S}N(u)\subseteq B.
\]
SAT(F_G)=YES via the all-zero original assignment and unique zero pins. Neither this source formula's assignment matrix nor its #SAT value is the arbitrary SAT decision function on encoded formulas.

The recognizer checks the real source (including header counts, ordered pin clauses, split domains, edge signs and duplicate edges) before choosing the graph-specific procedure. On all other valid parsed width-at-most-three CNFs it takes the ordinary exhaustive exact-count fallback. Invalid source syntax is reported INVALID. No generic source is silently interpreted as a matching.

## End-to-end constructive counting theorem

**Theorem D2-1 (PROVED/EXACT, scoped).** For all nonnegative integers \`a,b\` and every cross-only simple bipartite edge set \`E\`, the authenticated source above is counted exactly by the uniform algorithm:
\[
W_0(\varnothing)=1,\quad
W_{t+1}(U)=W_t(U)+W_t(U\text{ via the 1-branch}),
\]
where the unambiguous operational form is to send weight \`W_t(V)\` to **both** keys \`V\` and \`V\cup N(a_{t+1})\`, accumulating repeated keys. At stage \`a\`, return
\[
Z=\sum_U W_a(U)\,2^{b-|U|}.
\]
All counts are nonnegative exact integers of at most \`a+b+1\` bits, and every source-to-output edge is actual parser/graph/DP/output work.

*Proof.* For each prefix \`S\subseteq A_{\le t}\`, its union \`U(S)\` is the state key. At \`t=0\` there is one empty prefix. Every prefix at \`t+1\` uniquely either excludes or includes the new left vertex, giving exactly the two updates. Hence \`W_t(U)\` counts prefixes that yield that union. For each completed prefix, the allowed B assignments are precisely the subsets of \`B\setminus U\`; their number is \`2^{b-|U|}\`. The pin lemma makes this the *full* CNF #SAT count. For invalid/other valid sources the generic fallback directly enumerates every Boolean valuation. QED.

Define \`F_t={U(S):S subset A_{\le t}}\`, \`r_t=|F_t|\`, and \`r=max_t r_t=r_a\`. The earlier TMR-2/053 Boolean-lattice zeta theorem says the assignment cut matrix has rank \`r\` over EVERY field. \`r_t\` is nondecreasing, because excluding the new vertex preserves every old union.

For a standard deterministic multitape realization using balanced search trees, explicit masks of \`b\` bits and exact \`a+b\`-bit weights, conservative worst-case **bit** budgets are
\[
T_{\rm DP}=O(N^3+a\,r\,(N+a+b)^3),\qquad
S_{\rm DP}=O(N^2+r(N+a+b)^2),
\]
where \`N\` is the complete encoded source bit length. These deliberately loose bounds cover source parsing and authentication, label/address storage, set-union, balanced lookup, duplicate aggregation, output and buffers; they do not identify a built-in JavaScript hash operation with a unit-time physical TM step. The source branch selection and any rejected recognition are charged. Rank or graph parameters are not supplied as oracles.

## New count-continuation congruence

For a prefix union \`U\` at stage \`t\`, let \`R_t=A_{>t}\`. Define the full future cardinality signature
\[
\sigma_t(U)=\bigl(|U\cup N(S)|:S\subseteq R_t\bigr)
\]
in a fixed order of future subsets. Define \`U\equiv_t V\` iff their signatures are identical. This is a **counting-continuation equivalence**, not Boolean residual-function equality and not equality of neighborhoods.

**Theorem D2-2 (PROVED/EXACT, scoped).** The equivalence is right-congruent with BOTH choices on the next left vertex \`u\`. That is, for \`U\equiv_t V\`,
\[
U\equiv_{t+1}V,\qquad
U\cup N(u)\equiv_{t+1}V\cup N(u).
\]
At stage \`a\`, members of the same class have equal exact B-completion count. Consequently, the weighted union DP can merge \`U\equiv_t V\` at every stage without changing \`#F_G\`.

*Proof.* For every \`S subset R_{t+1}\`, equality of the old signatures gives equality of \`|U union N(S)|\` and \`|V union N(S)|\`. It also gives equality after adjoining the next vertex \`u\`, since \`S union {u}\` is a subset of \`R_t\`. These are exactly the zero and one branches' next signatures. At the terminal stage the only future subset is empty, so equivalence means \`|U|=|V|\`, and each continuation contributes exactly \`2^{b-|U|}\`. Grouping integer weights is therefore exact, with no double-counting. QED.

**Not free:** constructing the literal signatures by enumeration costs at least their lengths \`2^{a-t}\` per examined state (and further union/popcount work), so the naive quotient-discovery routine can remain exponential even when its quotient is tiny. The published program actually executes this naive quotient only in finite audits, not in the claimed production matching fast path.

## Exponential rank versus polynomial exact counting, on the SAME source

For the canonical perfect matching \`a=b=k\`, every left vertex has a private distinct right neighbor. After the first \`t\` left vertices, \`r_t=2^t\` and
\[
\operatorname{rank}_K D_{G_k}=2^k
\quad\text{for every field }K.
\]
But each union's future signature depends **only on its cardinality** \`j\`: all future matching edges are disjoint. Therefore the exact future-quotient class count is
\[
q_t=|\mathcal F_t/{\equiv_t}|=t+1,
\]
and one can compute the whole exact count by the usual binomial recurrence \`w_{t+1,j}=w_{t,j}+w_{t,j-1}\` followed by \`sum_j w_{k,j}2^{k-j}=3^k\`. More directly, the authenticated source recognizer checks that all A and B degrees are at most one, then computes
\[
\#F_G=3^m2^{a+b-2m}
\]
by paid repeated small-integer multiplication and output, where \`m=|E|\`. One **fixed** uniform solver handles all such inputs; no advice, answer oracle, assignment guessing, or uncharged parameter selection is used.

On that recognized path, conservative deterministic multitape bit bounds are \`T=O(N^3)\`, \`S=O(N^2)\` for parser, sorted/deduplicated edge pairs, degree checks, exact \`O(a+b)\`-bit arithmetic and decimal output. No lower bound is inferred from the old exponential rank or from the enumerated \`2^k\` raw DP entries. For unrestricted #SAT the fallback may take exponential time, and this example establishes NO algorithm for an arbitrary encoded 3-CNF in polynomial time.

The **named physical invariant/interface for TMR-4** is \`D2-FUTURE-QUOTIENT(t)\`: the equivalence partition \`equiv_t\` for a declared left-to-right, read-once, integer-weighted neighborhood-DP evaluator. Permitted transitions are (i) authenticated source parse; (ii) edge-neighborhood construction; (iii) zero/one update of each *actually materialized* state with exact weight addition; (iv) any explicitly computed equivalence merge, paying for signature discovery or a proved specialized rule; (v) switch to a legal alternative algorithm, with its actual discovery and runtime charged; (vi) output or all-input fallback. \`q_t\` is NOT automatically a lower bound for an unrestricted program, and does not imply all \`q_t\` classes must be materialized by a solver that uses another representation. The registered transition tariff must attach to **actual materialized objects**, not latent semantic classes.

## Actual verification and limits

The **published hosted-V8 source** \`experiments/tmr/tmr2_future_signature_e2e055.js\` was directly evaluated (revision v3). Its raw JSON is \`results/raw/tmr/2026-11-15_1617_TMR2_FUTURESIGNATURE_E2E055_V8_RAW.json\`. The 130 source instances include perfect matchings through k=8, complete bipartite and star controls, 112 seeded random bipartite sources with a,b<=4, and all-zero/isolated structures. It independently checks original DIMACS exhaustive counts, genuine graph-DP counts, expensive future-signature quotient counts, exact GF(2) rank on small source matrices, and actual fast-path choice: **915 assertions, 5,626 charged signature-subset visits, zero failures**. Three generic non-gadget CNFs exercise exhaustive fallback; two malformed inputs are rejected. No assertion count establishes asymptotic hardness.

A separate local native Node prototype v2 independently returned 130 cases, 1,047 assertions, zero failures, but is NOT the published source revision. No complete checkout, repository preflight, kernel check, LaTeX build or instruction-level TM replay was executed; GitHub connector reads and hosted V8 were used instead. Reported asymptotic multitape budgets are conservative mathematical implementations of the declared data structures, not measured instruction counts. Seed is 20261115, no randomized isolation.

## Four mandatory gates, hostile controls and provenance

| Gate | Verdict | Scope |
|---|---|---|
| DISJ | **PASS restricted; FAIL any rank-to-general-runtime inference** | Perfect matching is precisely the DISJ hostile control: rank 2^k, exact #SAT 3^k, polynomial authenticated counting. |
| Relativization | **PASS local combinatorial proof; OPEN unrestricted bridge** | No P-vs-NP separation attempted. No nonrelativizing P-vs-NP ingredient is identified; algebrization/Natural Proofs remain relevant to any later unrestricted transfer. |
| Simultaneous DTISP | **PASS same-run restricted counting bounds; OPEN lower-bound transfer** | The source recognizer, selected route, arithmetic, buffers and output belong to one execution. No FLMV forbidden-box premise is claimed. |
| Configuration counting | **PASS upper-bound guard only** | The deterministic finite-machine configuration count gives \`T<=2^{O(s+log N)}\` for the total machines under the stated model, never a work lower bound. |

Horn/2-SAT: the projected edge relation is both Horn and Krom; the gadget is intentionally a cheap subclass. Affine/Gaussian: linear systems have a separate polynomial algebraic route, so no obligatory materialization of neighborhood classes. Treewidth: matchings have bounded treewidth and polynomial DP. Equality, autarkies and product factors may all enable further compression. Padding and duplicated clauses do not manufacture work. The seven pins give exactly one extension per satisfying assignment; adding auxiliary Tseitin variables requires an audited extension multiplicity. The TMR-2/052 unique-selector projection collapse, unique-solution rank-one control, compact shared circuits, variable-order adaptation, caching/recomputation, coefficient bits and exact output count are not excluded. Walsh-Hadamard in characteristic two is singular; no basis-transfer claim is made. /341 is FAIL as full UNSAT authority; /386 remains RESTRICTED. No quantum/majority theorem is invoked.

**Original corpus/source:** TMR-2/053 exact neighborhood-zeta theorem and source code/raw; TMR-2/054 dynamic DISJ frontier; TMR-4/055 fully charged shared-register compiler and manuscript; TMR-5/050 one-switch limitation; current issue #3; 2026-11-15 end-to-end directive; Bryant (1986), *Graph-Based Algorithms for Boolean Function Manipulation*, IEEE Transactions on Computers, DOI 10.1109/TC.1986.1676819; Jenssen, Perkins and Potukuchi (2023), *Approximately counting independent sets in bipartite graphs via graph containers*, DOI 10.1002/rsa.21145 (approximate, not used as an exact algorithm). The future-signature congruence is proved here without claiming original discovery of automata minimization.

**ONE next dependency:** D2-QUOTIENT-CONSTRUCTION: identify a nontrivial, efficiently recognizable family beyond disconnected matching/product controls for which future count-equivalence classes admit a polynomial-time computable canonical signature, and build a same-realization algorithm whose *discovery plus evaluation* is polynomial in the input and the certified number of classes. Any further lower-bound implication must survive alternative compact methods and TMR-4's physical transition audit.
