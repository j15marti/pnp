# TMR-1/042: Connected width-two proper 3-CNF with exponential evaluation rank, cheap SAT and exact fusion tariff

**2026-11-15 03:08 PST, America/Los_Angeles.** TMR-1, PNP Machine Model Lead. Governing directive `research/coordination/2026-11-14_FUSION_LIPSCHITZ_TARIFF_FIVE_AGENT_REFOCUS.md`, blob `54c9177fc211dfca6c94d89d6ebbf3f3908809d6`. **Symbolic mathematical results PROVED/RESTRICTED, independent mathematical review OPEN; finite execution COMPUTATIONAL. P versus NP OPEN.**

## 1. Candidate and four precommitted falsifiers

**Claim under attack.** Could an exponentially large rational evaluation rank, together with a *connected* primal graph, no pure variables and a non-Schaefer 3-CNF relation, support a nonzero universal fusion-Lipschitz tariff even when standard cheap representations are legal?

F1: an equality/2-SAT quotient collapses the apparent exponential interface into a linear description. F2: a connected width-two decomposition solves the entire formula efficiently despite the rank. F3: one legal paid record discharge halves the residual rank and violates a fixed positive raw-rank tariff. F4: a fixed correct SAT decider recognizes this syntactic family in polynomial time, so a universal same-input lower bound for this family fails. **All four occur.** This is a new explicit *negative control*, not a candidate hard SAT family.

The exact authenticated-source and lab systems are kept distinct. Original relevant work: TMR-2/040-041 (large NAE evaluation matrices and leaf quotients), TMR-3/041 (fully paid fixed-program solver), TMR-4/042 (canonical typed record tariff), TMR-5/037-038 (exponential rank versus polynomial circuits and minimum separator), TMR-1/041 (separator lattice) and LEAD-0029 (Lipschitz squeeze). The structural tractability literature includes Samer and Szeider's incidence-treewidth counting algorithm [1] and Ordyniak, Paulusma and Szeider's acyclic-SAT results [2].

## 2. Explicit growing proper 3-CNF and encoded input

Fix integer `k>=1`. Distinct Boolean variables are `X_i,Y_i,U_i,V_i` for `1<=i<=k`, three core variables `A,B,C`, and bridge variables `Z_0,...,Z_(k-1)`. The total number is **5k+3**. Each literal is signed and each source clause uses three *distinct variable identifiers*.

For each `i`, define the *literalwise complete split* equality gadget

$$
E_i=(\neg X_i\vee Y_i\vee U_i)
\wedge(\neg X_i\vee Y_i\vee\neg U_i)
\wedge(X_i\vee\neg Y_i\vee V_i)
\wedge(X_i\vee\neg Y_i\vee\neg V_i).
$$

It is exactly equivalent to the two Krom clauses `(not X_i or Y_i) AND (X_i or not Y_i)`, hence to `X_i=Y_i`. The auxiliary variables are semantically irrelevant. For any signed triple `(a,b,c)`, write

$$
N(a,b,c)=(a\vee b\vee c)\wedge(\neg a\vee\neg b\vee\neg c).
$$

This is the three-variable not-all-equal relation. Define

$$
F_k=\bigwedge_{i=1}^k E_i\ \wedge\ N(A,B,C)\ \wedge\ N(A,X_1,Z_0)\ \wedge\ \bigwedge_{i=1}^{k-1}N(X_i,X_{i+1},Z_i).
$$

This is a **proper 3-CNF with 6k+2 ternary clauses**. All variables occur positively and negatively. The primal graph is connected: `Z_i` forms a triangle between consecutive `X` vertices; `Z_0` joins the `A,B,C` triangle; each `Y_i,U_i,V_i` attaches by triangles. Its exact primal treewidth is **2**. A width-two decomposition contains bags `{A,B,C}`, `{A,X_1,Z_0}`, `{X_i,X_(i+1),Z_i}`, `{X_i,Y_i,U_i}`, `{X_i,Y_i,V_i}`; connect the bridge bags as a path, attach each `U_i` bag to a bridge bag containing `X_i`, attach its `V_i` bag to the `U_i` bag, and attach the core bag at `A`. Every clause lies within a bag; each variable's bags form a connected subtree. A ternary clause forces the lower bound treewidth 2.

Assign canonical consecutive positive integer variable IDs and write the clauses in this displayed fixed order, with a standard self-delimiting header and binary signed identifiers. There are `Theta(k)` clauses/occurrences and indices of `Theta(log(k+1))` bits, giving actual encoded bit length

$$
L_k=\Theta(k\log(k+2)).
$$

No padding or nonuniform advice is used. Source membership is recognizable by a *single* fixed finite deterministic parser in polynomial time in actual input length, with malformed, nonmatching and overlong inputs sent to general SAT fallback.

## 3. Exact interface projection, rank, rectangle cover and Schaefer controls

Use `X=(X_1,...,X_k)` as one party and `Y=(Y_1,...,Y_k)` as the other. Existentially quantify all remaining source variables `U,V,A,B,C,Z`. Every NAE bridge has a private `Z_i`; it can be satisfied for **any fixed values** of its two other arguments. The core NAE has satisfying assignments, e.g. `(A,B,C)=(0,0,1)`. Thus

$$
\boxed{\exists_{U,V,A,B,C,Z}\,F_k(X,Y)\ \equiv\ \bigwedge_{i=1}^k(X_i\leftrightarrow Y_i).}
$$

The evaluation matrix `M_k[x,y]` of this existential relation is therefore exactly the `2^k x 2^k` identity matrix. Its rational rank and minimum cover by all-1 Cartesian rectangles are **exactly** `2^k`: each diagonal entry must belong to a distinct rectangle, since a rectangle covering two diagonal entries would also cover a zero off-diagonal cross entry. The rank grows exponentially despite an `O(k)` description and an `O(k)` circuit for equality.

**Constructive witness.** For any `x\in\{0,1\}^k`, set `Y=X=x`, `U_i=V_i=0`, `A=B=0,C=1`. For each bridge with fixed endpoint bits `a,b`, choose `Z=1-a` when `a=b`, otherwise choose `Z=0`. Every clause is then true. Conversely a mismatch `X_i\ne Y_i` makes one of the two complementary-`U_i` or complementary-`V_i` clause pairs contradictory. Thus no hidden witness can satisfy mismatched X,Y.

The complete projected relation on `(A,B,C)` is exactly NAE3 because all equality gadgets and bridges can be completed for either value of `A`. Consequently the *whole* solution relation is not Horn, dual-Horn, bijunctive or affine: these four Boolean relation classes are closed under existential projection, whereas NAE3 fails, respectively, coordinatewise meet, join, ternary majority and ternary XOR closure. The source has no pure variables. Nevertheless the fixed signed equality/Krom quotient plus private NAE leaf elimination, or standard width-two dynamic programming, decides it in polynomial time. This simultaneously defeats high rank, graph connectedness and the mere presence of a non-Schaefer relation as lower-bound hypotheses.

**Machine consequence.** A fixed finite-alphabet total deterministic multitape SAT decider `D` can parse the above canonical grammar, verify every source clause against the prescribed symbolic pattern with paid head motions, accept if the complete exact pattern matches, and otherwise use an exhaustive correct fallback on all 3-CNFs and malformed encodings. The parser is a fixed finite algorithm and can be compiled to ordinary locally moving heads with polynomial overhead. Thus `D` is correct on all inputs and runs in polynomial `L_k` time on **every** `F_k`. This falsifies any proposed superpolynomial bound on this particular explicit family that is claimed for every correct fixed SAT decider. It does not falsify the correct algorithm-dependent hard-input quantifiers.

## 4. Qualified symbolic-record transition system and exact rational tariff

A separate authenticated **EQ-REC** laboratory has fixed original `F_k`, a globally unique set `R subseteq {1,...,k}` of remaining record identities, a zero-cost view bit, the paid-event ledger, and a completed goal `R=empty`. It is **NOT** a SAT decider or a physical input parser. The only legal operations are zero-cost NOP, zero-cost reversible SWITCH_VIEW, and `CHECK_i` for `i in R` at unit price, which removes exactly the named record identity. No batch operation, free removal or unverified source rule is declared legal. All AND obligations `R` must be discharged; each paid identity appears once. The two views form one authentic zero-cost SCC for each `R`. Quotient states are sets `R`, not merely an input rank count.

Set `u=|R|` and the seven-component reduced obstruction to

$$
\mathbf p(R)=(0,0,2^u-1,0,0,0,u).
$$

The last component measures exact remaining typed record operations. These components and the goal survive zero-cost closure. For each `CHECK_i`, the exact discharge vector and cost are

$$
\Delta_{\mathrm{CHECK}}=(0,0,2^{u-1},0,0,0,1),\quad w=1.
$$

NOP and SWITCH_VIEW have `Delta=0,w=0`. Writing `a=lambda_separator >=0`, `b=lambda_machine>=0`, with all other weights zero, the **complete all-transition tariff** is

$$
\boxed{2^{k-1}a+b\le1.}
$$

The strongest row has `u=k`; all smaller rows follow. The exact feasible certificate `(a,b)=(0,1)` yields `Phi(initial)=k`, attained by `k` legal CHECKs. It is primal/dual optimal:

$$
\max_{a,b\ge0}\bigl[(2^k-1)a+kb\bigr]=k
\quad\text{subject to}\quad 2^{k-1}a+b\le1.
$$

The dual certificate puts weight `y_k=k` on the maximal-`u` inequality: `k2^{k-1} >= 2^k-1`, and `k >= k`. The pure-rank rational certificate `(a,b)=(2^{1-k},0)` yields only `2-2^{1-k}<2` for `k>=2`. A fixed positive rank weight independent of `k` fails the real `CHECK` transition for large `k`; naive `a=1,b=0` already fails for `k>=2` by discharge `2^{k-1}>1`.

These are actual **typed-record** tariffs and completed goals. They are **not** machine source reads, a full proof-DAG authority, or a SAT decision lower bound. An actual physical evaluator may fuse, learn, Gaussian-eliminate or reuse representations; these remain legal MAY unless independently charged in its own exact model. Deleting a genuine cheap path is disallowed. No CEGAR refinement is claimed.

## 5. Exact tests and controls

The exact V8 function serialized to `experiments/tmr/tmr1_eqrank_treewidth088.js` was executed in the hosted V8 isolate, yielding **1,806 assertions, zero failures**, and the unmodified result was published to `results/raw/tmr/2026-11-15_0308_TMR1_EQRANK088_V8_RAW.json`. It checked `k=1,...,8`, all 510 canonical witnesses, proper clauses, positive/negative occurrence for each variable, primal graph connectivity, clause coverage and connected running intersections in eight width-two decompositions, rational rank for eight exact identity matrices of sizes up to 256, exact tariff rows and rank-only violations, the four Schaefer closure failures, and exhaustive existential projection for all 84 pairs of `X,Y` inputs for `k<=3`. Finite tests are **COMPUTATIONAL**; the general theorem is by symbolic proof above. The published Node wrapper was not separately run on an OS Node binary; no actual physical TM code, complete theorem formalization or LaTeX build was executed.

Machine-readable seven-column schema and rational dual: `results/raw/tmr/2026-11-15_0308_TMR1_EQRANK088_TARIFF.json`.

## 6. Dependency DAG and model-transfer status

| Dependency | Status |
| --- | --- |
| `E_i iff X_i=Y_i` and each NAE bridge existentially transparent | PROVED/RESTRICTED |
| Proper source, no pure variables, connected graph and primal treewidth exactly 2 | PROVED/RESTRICTED |
| Exact identity evaluation matrix, rational rank and rectangle cover `2^k` | PROVED/RESTRICTED |
| Non-Schaefer projection and polynomial correct total family recognizer/fallback | PROVED/RESTRICTED, physical compilation not separately executed |
| EQ-REC zero-cost quotient, all-step seven-component tariff and exact dual optimum `k` | PROVED/RESTRICTED |
| Transfer from EQ-REC or prescribed evaluation rank to native arbitrary SAT-machine work | FAIL for a superpolynomial conclusion on this family; no bridge shown |
| A *different*, hard, fusion-safe SAT family with superpolynomial initial potential | OPEN |
| Same-system machine transfer for that hard family | OPEN |

The conditional telescoping theorem remains correct: if a cost-underestimating all-step simulation preserves initial state, every legal edge and every completed goal, then `Phi(initial)<=total paid work`. Its nontrivial content lies in the universally valid rows **and** independent initial-gap theorem. A free operation that drops a positive potential, a fused paid operation overdischarging its row, or a compact polynomial solver immediately defeats the proposed instance-specific abstraction. Neither /341 (FAIL on full accepted language) nor /386 (RESTRICTED guarded fragment) has been repaired or used as a logical authority.

**Weakest next lemma for TMR-2/3/4:** Identify one genuinely computation-dependent separator component whose *minimum over all legal succinct representations* is nontrivial after Krom/affine/treewidth/leaf quotient and all shared computation. TMR-3 should price simultaneous operations and physically compile any claimed process obligation; TMR-4 should include this `CHECK` counter-row and real zero-cost SCC in independent LP replay. TMR-5 should verify the tree decomposition and test an admitted batch-CHECK control (which invalidates the current typed tariff if made legal).

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Proof1.txt SHA `06f7ebc8c2283304a0f5200b518c6e48fa41e343` fully recovered (28,714 chars); proof2.txt authentic blob SHA `930c5eeddafce656717f28055a7a9a755f44737c` fully recovered (1,051,196 chars); root main.tex authentic blob SHA `6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34` fully recovered (2,545,859 chars). These were not edited. AGENTS.md, CODEX.md, repository skill, TMR replacement directive, all five current handoffs, original peer reports and issue #3 current 2,130-comment corpus were consulted. Five existing schedules were not touched.

## 7. Primary literature

[1] Samer M, Szeider S. *A Fixed-Parameter Algorithm for #SAT with Parameter Incidence Treewidth*. arXiv:cs/0610174 (2006). https://arxiv.org/abs/cs/0610174 . Its stated `O(4^t t l N)` fixed-treewidth algorithm is supportive background; our width-two decomposition and family witness are self-contained.

[2] Ordyniak S, Paulusma D, Szeider S. *Satisfiability of Acyclic and Almost Acyclic CNF Formulas*. Theoretical Computer Science 481 (2013):85-99. https://doi.org/10.1016/j.tcs.2012.12.039 . Our connected width-two construction does not depend on a beta-acyclicity claim.

[3] TMR-2/041 original source projection counterexample, Git blob `8a6261445f1a9835d6a2459eb39ea7dee64a8edf`; TMR-5/038 minimum-separator warning, Git blob `59f4d70b1a6be709ca0e51c43558308b60459bfa`; TMR-1/041 separator-lattice theorem, Git blob `f8b3a673e233ffab7220d4c61bbea4bd74a972a2`.
