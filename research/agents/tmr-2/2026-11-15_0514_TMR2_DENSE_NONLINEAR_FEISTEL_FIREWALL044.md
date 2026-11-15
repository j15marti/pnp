# TMR-2/044: Dense nonlinear Feistel interface defeats a rank tariff after Gaussian, separator, and block-product controls

**2026-11-15 05:14 PST | FEISTEL096 | TMR-2, PNP Information Necessity**

**Status:** PROVED/RESTRICTED symbolic family, exact projected relation, affine-hull and tariff theorems. Independent mathematical peer review OPEN. Finite checks COMPUTATIONAL. Unrestricted SAT-machine superpolynomial obstruction and same-system transfer OPEN. P versus NP OPEN.

## 1. Predeclared candidate and four falsifiers

Candidate: replace TMR-2/043's disjoint NAE3-block relation with a genuinely coupled nonlinear relation having exponential X/Y matrix rank, full affine hull, growing primal treewidth, non-Schaefer semantics, and no coordinate-block factorization, and test whether this forces expensive SAT-machine work.

Falsifiers: F1 a shared polynomial-size circuit represents the entire relation; F2 one fixed correct total SAT decider has a cheap verified family-specific path; F3 a single authentic terminal cost-one transition discharges a source-static rank component; F4 Gaussian or cheap bounded-separator projection destroys the claimed coupling. F1, F2, and F3 occur; F4 does not hold for the narrowed Gaussian/primal-treewidth claims, yet a compact shared circuit is the decisive cheap quotient.

## 2. Recovered evidence and primary literature

Read FIRST the approved 2026-11-14 fusion directive SHA 54c9177fc211dfca6c94d89d6ebbf3f3908809d6. Then the 2026-11-13 replacement directive, full proof1.txt (28,714 characters, SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343), full authentic proof2.txt Git blob (1,051,196 characters, SHA 930c5eeddafce656717f28055a7a9a755f44737c), full root main.tex Git blob (2,545,859 characters, SHA 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34), issue #3 and current comments, AGENTS.md, CODEX.md, repository skill, all five TMR handoffs, TMR-2/043 code and matrix, original TMR-1/043, TMR-3/043, TMR-4/044, TMR-5/040 reports and LEAD-0029 Lipschitz audit. Ordinary GitHub file reads of the two huge root files gave blank text; authentic complete blobs were instead fetched by SHA. Historical /341 full logical UNSAT authority FAIL; /386 tested guarded fragment RESTRICTED.

Primary context: T. J. Schaefer, STOC 1978, DOI https://doi.org/10.1145/800133.804350 (Horn, bijunctive and affine distinctions); M. Luby and C. Rackoff, SIAM J. Comput. 17(2), 1988, DOI https://doi.org/10.1137/0217022 (invertible permutation construction context); Aho and Ullman, SIAM J. Comput. 1(1), 1972, DOI https://doi.org/10.1137/0201002 (straight-line programs). The new construction is independently proved below and is NOT claimed pseudorandom or cryptographically secure.

## 3. Exact explicit growing proper-3CNF

Fix integer m>=5, with cyclic indices modulo m. Write E0 for the m(m-3)/2 unordered noncycle pairs of the m-cycle. Over GF(2), set

$$
Q_m(z)=\bigoplus_{\{i,j\}\in E_0} z_i z_j,\quad
g_i(z)=Q_m(z)\oplus z_i z_{i+1},
$$

and define the reversible two-shear mapping

$$
U=X\oplus g(Z),\qquad V=Z\oplus g(U).
$$

Construct a shared AND/XOR straight-line network for Q(Z), all g_i(Z), U, then Q(U), all g_i(U), V. Each AND output t=a AND b is encoded by (NOT a OR NOT b OR t), (a OR NOT t), (b OR NOT t), padding each binary clause (c OR d) with the exact pair (c OR d OR p), (c OR d OR NOT p) for its own fresh p. Each XOR output t=a XOR b is encoded by the four ternary forbidden-parity clauses (NOT a OR b OR t), (a OR NOT b OR t), (a OR b OR NOT t), (NOT a OR NOT b OR NOT t). Thus every source clause has exactly three distinct variables.

Finally flip the polarity of each odd one-based original X input variable in ALL its literal occurrences, leaving all other source variables unchanged. This bijectively changes the source encoding and yields a canonical satisfying witness with those X variables 1 and every other variable 0. Both all-zero and all-one COMPLETE assignments fail, but the formula is satisfiable.

The exact counts are

$$
G_m=2m^2-2\text{ genuine shared gate identities},\quad
v_m=4m^2-2\text{ variables},\quad
c_m=9m^2-m-8\text{ proper clauses}.
$$

Standard indexed binary encoding has length N_m=Theta(m^2 log(m+2)). Every variable appears with both polarities; all authentic extension and padding bits are explicitly encoded and checked. This is not a semantic truth-table source.

## 4. Five symbolic properties, with proofs

**044.1: Exact permutation projection.** Existentially eliminating all gate and padding wires gives precisely the graph of the displayed mapping, up to the fixed X sign flip. The gate clauses are truth-function equivalences, and each padded two-clause pair is equivalent to the unpadded two-clause constraint. The inverse is explicitly

$$
Z=V\oplus g(U),\qquad X=U\oplus g(Z).
$$

Thus the external input/output relation is a bijection of 2m-bit strings.

**044.2: Exact communication rank and rectangle cover.** The 2^(2m) by 2^(2m) projected evaluation matrix is a permutation matrix. Its rational and real rank, exact fooling-set maximum and minimum all-one-rectangle cover all equal 2^(2m). No compulsory machine work follows from this fact alone.

**044.3: Full affine hull (no surviving affine equations).** For any a in GF(2)^m, the quadratic ANF of a dot g(z) has coefficient sum_i(a_i) on every noncycle monomial and coefficient a_i on the distinct cycle monomial z_i z_(i+1). Since E0 is nonempty, being affine forces every a_i=0. Therefore the functions g_i are independent modulo affine functions.

For an affine expression a dot X+b dot Z+c dot U+d dot V constant on the projected graph, substitute X=U+g(Z) and V=Z+g(U). The expression is

$$
(a+c)\cdot U+(b+d)\cdot Z+a\cdot g(Z)+d\cdot g(U).
$$

Here U and Z range independently. Independence modulo affine forces a=d=0 and then b=c=0. Its only constant affine form is trivial. The graph's affine hull is all GF(2)^(4m), despite having just 2^(2m) tuples. Source input complementation is an affine isomorphism, so it preserves this result.

**044.4: High treewidth and nonproduct dependency.** Every unordered pair of Z inputs occurs in the same genuine AND-gate ternary clause, through either Q or a cycle term. Likewise each pair of intermediate U wires appears in a genuine stage-two AND clause. Hence the CNF primal graph contains K_m and has treewidth at least m-1. For every i, output U_i depends essentially on X_i and on EVERY Z_j: the Boolean derivative of Q with respect to Z_j is a nonzero sum of its m-3 nonneighbors, never canceled by the distinct cycle monomial. Thus all input coordinates and U outputs lie in one connected bipartite essential-dependency component. Each V_i depends on at least one X_j, since g_i(U) is nonconstant and U ranges freely with X at fixed Z. Therefore the mapping does not factor as nontrivial disjoint-coordinate input/output products. This narrowly defined nonfactorization is NOT a circuit lower bound, because the shared Q circuit is polynomial.

**044.5: Non-Horn, non-dual-Horn, non-bijunctive and nonaffine projection.** Pin all Z inputs except Z_1 and Z_3 to 0 and existentially project away other external coordinates. U_4 (whose original X_4 is not sign-flipped) obeys exactly

$$
u=x\oplus(a\land b)
$$

on (x,a,b,u)=(X_4,Z_1,Z_3,U_4). This relation fails closure under coordinatewise meet, join, majority and ternary XOR, with explicit witness tuples in raw results. These closures are preserved by pinning and existential projection. Therefore both the full projected graph and full proper-3CNF source are outside the four tractable Schaefer relation classes. This does not preclude easy recognition of this specific family.

## 5. Genuine polynomial SAT shortcut

One fixed uniform deterministic total decider on arbitrary binary inputs parses proper 3-CNF, enumerates m=5,...,N and generates each canonical source template whose encoded size fits, compares the whole input exactly, constructs and verifies the stated satisfying assignment on a match, and otherwise calls exhaustive SAT search. For the specified canonical growing family, total paid multitape work is polynomial in N_m, including source reads, generation, matching, verification and output. The algorithm is still correct and total outside that family because of its exhaustive fallback; NO all-input polynomial runtime is claimed. The finite tester additionally confirms satisfiability survives global renaming, complementary source sign changes, clause reordering and duplication; these transformations are NOT claimed to lie in the canonical recognizer's polynomial-time accepted language.

Both uniform endpoint assignments fail after the source X sign changes, and the external relation has no nontrivial affine equations, yet the shared network and a legal verified witness are cheap. Therefore the inference from exponential rank, nonlinear coupling, large source treewidth and no affine quotient to compulsory SAT-decision time is **FALSIFIED/RETIRED for this explicit candidate**. Theorem 044.1 itself is a circuit construction, not a lower bound.

## 6. Qualified zero closure and exact rational tariff

Separately define the preauthenticated GATE-CHECK record calculus R_FEIS(m). A state contains the exact authenticated signed source, a correctly supplied complete gate assignment, the set P of verified original gate identities, a reversible view flag and live h. Authentic zero-cost VIEW/NOP only change view metadata and preserve P,h; the genuine zero SCC quotient therefore preserves all components below. Paid CHECK_ID at cost 1 verifies one unchecked gate assignment and adds its identity to P, counting shared identities only once. Paid HALT costs 1 and is legal only when all G_m CHECK events have occurred. Completed goals are absorbing and p=0. This is a deliberately restricted certification task with *all* gate AND-obligations; it is neither a physical machine simulation nor a SAT decision lower-bound model.

Define the actual seven-component zero-closed vector

$$
p(C)=(0,0,(2^{2m}-1)h,0,G_m-|P|,0,h).
$$

| Rule | Cost | CNF | AFFINE | SEP | FUSION | GAMMA | INTERFACE | MACHINE |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| VIEW/NOP | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CHECK_ID | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| HALT | 1 | 0 | 0 | 2^(2m)-1 | 0 | 0 | 0 | 1 |

The displayed entries are exact signed discharges, not absolute changes. The complete feasible nonnegative cone is

$$
\lambda_\Gamma\le1,\qquad
(2^{2m}-1)\lambda_{\rm SEP}+\lambda_{\rm machine}\le1.
$$

The exact rational initial LP optimum is G_m+1=2m^2-1: take lambda_GAMMA=lambda_machine=1 and all other weights zero; the matching dual pays G_m distinct authentic CHECK rows plus one HALT row. Positive rank weight can be scaled for fixed m, but any single constant positive rank weight across unbounded m FAILS at the paid final HALT. For a real cost-one physical machine, that last-step failure also applies to any independently proposed terminal-masked source-static rank, without transferring the record calculus's mandatory CHECK work to that machine.

## 7. Native finite checks and hostile-control inventory

The **exact V8 audit() function executed** and then serialized as the standalone source under experiments/tmr/tmr2_dense_feistel096.js. It performed **16,088 checks with zero failures**, no randomness, over m=5,...,9. It verified proper 3-CNF arity/count/polarities, source and intermediate K_m clique edges, both endpoint failures, signed/permuted/reordered/duplicate witness controls, intermediate gate semantics, reversal, and exact genuine source satisfaction. For m=5 and 6, it exhaustively checked all 1,024 and 4,096 input/output assignments and found full affine-hull binary matrix ranks 21 and 25. For m>=7, only structure and sampled assignments were checked; the all-m conclusions rely on the proofs, NOT those samples. Four local polymorphism witness counterexamples were generated.

| m | CNF variables | clauses | gates | matrix rank |
|---:|---:|---:|---:|---:|
| 5 | 98 | 212 | 48 | 1,024 |
| 6 | 142 | 310 | 70 | 4,096 |
| 7 | 194 | 426 | 96 | 16,384 |
| 8 | 254 | 560 | 126 | 65,536 |
| 9 | 322 | 712 | 160 | 262,144 |

Controls: Gaussian and equality/union-find cannot explain the projected graph as affine, but compact AND/XOR, Tseitin and circuit quotients make it easy; Horn, dual-Horn and Krom failure does not exclude family-specific easy SAT; bounded-treewidth source DP cannot be presumed because source has K_m, but a shared quadratic network exists; pure-variable elimination cannot start, but certified autarky and the complete legal witness are allowed; source padding bits are explicit and correctly checked, not counted as entropy; learning, preprocessing, sharing, input rereads, caching and recomputation are legal; no selected DAG, padded bytes or source entropy is used as compulsory runtime; no actual CEGAR path was deleted. The fixed recognizer, not an uncharged advice string, supplies the cheap family path. The physical microstep representation, clock, and program-transfer proof are still OPEN.

Files: experiments/tmr/tmr2_dense_feistel096.js ; results/raw/tmr/2026-11-15_0514_TMR2_FEISTEL096_V8_RAW.json ; results/raw/tmr/2026-11-15_0514_TMR2_FEISTEL096_TARIFF.json. No native OS Node executable or compiled finite-alphabet SAT machine was run.

## 8. Dependencies and peer work

PASS/RESTRICTED: exact proper3CNF, invertible nonlinear projection, rank and 1-rectangle cover, full affine hull, primal clique, connected dependency and restricted CHECK/HALT tariff. FALSIFIED/RETIRED as a proposed universal implication: raw exponential rank plus nonaffine nonlinear coupling plus high treewidth plus no coordinate-block product implies high SAT time. OPEN: an actually dynamic program-sensitive SAT obstruction, fusion-safe superpolynomial initial gap, unrestricted all-transition physical simulation, and same-system all-decider transfer.

TMR-3: quantify a real fixed finite-tape recognizer and witness verifier. TMR-4: independently check the two tariff inequalities, permit every real shortcut as MAY and test the nonterminal activation collision. TMR-5: audit all-m affine hull and source counts. TMR-1: preserve independent same-system transfer. Weakest next TMR-2 lemma is a *dynamic* fusion/information component that survives sharing, compact nonlinear circuits and family recognition, with all real machine steps charged.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Both root proof trackers and root main.tex remain unchanged; TMR-5 retains synthesis ownership. Existing five agent identities, hourly Pacific schedules and enabled states unchanged. P versus NP remains OPEN.

END_OF_TMR2_REPORT::044::FEISTEL096::2026-11-15_0514_PST
