# TMR-5/075: Binary and all-arity affine polymorphisms of the exact five-symbol tournament
2026-11-17 16:42 PST. Status: **PROVED/EXACT finite-template algebraic theorem**, external independent mathematical review OPEN. Executed finite control COMPUTATIONAL. **P versus NP OPEN.**

## Candidate, model, and falsifiers (fixed before source search)

Template \(\Sigma=\mathbb Z_5\), \(R(a,b)\) iff \(b-a\pmod5\in\{1,3\}\). This exactly authenticates A>B,D; B>C,E; C>A,D; D>B,E; E>A,C. A k-ary polymorphism is a homomorphism \(f:T_5^k\to T_5\), meaning \(R(x_i,y_i)\) for *each* coordinate implies \(R(f(x),f(y))\). **Candidate D5-T5-BINARY-AFFINE-POLYMORPHISM:** every binary polymorphism, not assumed linear, is a rotated projection; every affine \(\mathbb Z_5\)-operation of arbitrary arity preserving R is a rotated projection. Possible falsifiers: nonrotation tournament endomorphism; binary operation failing shifted-diagonal representation; a mixed five-step increment cycle closing correctly; a coefficient vector combining at least two genuine inputs and preserving all product arcs.

## Theorem A: automorphism and endomorphism group

Every endomorphism of the loopless tournament is injective: identifying distinct adjacent vertices maps their unique arc to a nonexistent loop. It is therefore bijective. The five translations \(a\mapsto a+t\) are automorphisms. An automorphism fixing 0 must fix its two outneighbors 1 and 3 individually, because \(3\to1\), and its two inneighbors 2 and 4 individually, because \(4\to2\). The stabilizer of 0 is trivial. Thus the **only five endomorphisms** are the five translations.

## Theorem B: **all ten binary polymorphisms**

Let \(f:T_5^2\to T_5\) be arbitrary. For each \(d\), the shifted diagonal \(D_d=\{(a,a+d):a\in\mathbb Z_5\}\) is an induced copy of \(T_5\) in the direct product. By A, its restriction must be a translation, so \(f(a,a+d)=a+c_d\) for five constants \(c_d\).

On a genuine product arc, the two coordinate increments \(r,s\in\{1,3\}\) produce an output difference
\[
r+c_{d+s-r}-c_d\pmod5.
\]
The equal increments require nothing new. The cross increments \((r,s)=(1,3),(3,1)\) are equivalent to
\[
c_{d+2}-c_d\in\{0,2\}\quad\text{for every }d\in\mathbb Z_5.
\]
Following \(d=0,2,4,1,3,0\) gives five increments each 0 or 2. If h are 2, closure requires \(2h=0\pmod5\) and \(0\le h\le5\), hence h is 0 or 5. If all are 0, \(f(a,b)=a+c_0\); if all are 2, \(f(a,b)=b+c_0\). Conversely all ten maps preserve the tournament. **Exactly ten binary polymorphisms exist, precisely two idempotent**. This symbolic argument is independent of the finite enumeration and does not presume an affine form.

## Theorem C: no nontrivial affine mixing, **at every arity**

Let \(k\ge1\) and \(f(x)=c+\sum_{i=1}^k a_i x_i\pmod5\). Preservation is equivalent to
\(\sum_i a_i d_i\in\{1,3\}\) for *every* legal coordinatewise increment vector \(d\in\{1,3\}^k\). Put \(A=\sum a_i\pmod5\). The all-1 and all-3 vectors require \(A,3A\in\{1,3\}\), forcing \(A=1\). Changing just coordinate i from 1 to 3 requires \(1+2a_i\in\{1,3\}\), so each \(a_i\in\{0,1\}\). Changing any two with coefficient 1 would give \(1+2+2=0\), forbidden. Thus exactly one coefficient equals 1 and the rest 0; adding any constant c gives precisely a rotated projection. The converse holds. **No nontrivial Gaussian-linear, affine averaging, or coordinate mixing operation over \(\mathbb Z_5\) is a polymorphism of the original T5 relation, for any arity.** This does NOT exclude nonlinear high-arity polymorphisms or algorithms based on other reductions.

## Original-source-to-output verifier and matched resources

The fixed template has exactly ten directed arcs. A complete candidate binary operation table contains 25 entries, and preservation checks all 100 genuine product arcs; reading its full canonical source and producing its YES/NO outcome requires constant work for this fixed domain. For affine candidate operations encoded by unary arity k and k three-bit coefficient entries plus a validated constant, accept iff exactly one coefficient is 1 and all others are zero. Reject malformed codes 5--7, wrong lengths, and trailing data. A uniform conventional locally headed deterministic blank-work-tape machine can parse the entire N-bit source, count nonzero coefficients, and emit its output with **T=O((N+1)^2), peak S=O(N+1)** on one execution including source access, indices, buffers, verification, and final output. This verifies operations, *not* arbitrary CSP instances, and the result yields no solver time lower bound.

## Actual computational evidence

Executed twice on CPython3.13 with no random seed; byte-identical results. Published exact script SHA256 \`3f7938d484d4d5a2bbc02b5fa1f27577b652981b83a4dc15f09638f4d837a79b\`; executed JSON SHA256 \`bde12b3159f6a767cce51d6e11c78723d8aab23a3ac0f7821f2fcd4f60157ebc\`. Checked all ten template arcs, 5! permutations and 5^5 unary tables, all 625 normalized binary profiles against the 100 product arcs, all ten rotated projections, and 19,530 affine coefficient vectors for arities 1 to 6 with 1,111,110 increment-pattern evaluations. **20,330 assertions, zero failures.** All infinite/arbitrary-arity results above follow from symbolic proofs, not extrapolation. External independent mathematical review OPEN. No local repository checkout/preflight, full LaTeX compilation, native physical microtrace or Lean/nanoda executed.

Paths: \`experiments/tmr/tmr5_t5_polymorphism075.py\`; \`results/raw/tmr/2026-11-17_1642_TMR5_T5_POLYMORPHISM075_RAW.json\`.

## Four gates and controls

| Gate | Verdict |
|---|---|
| DISJ | **PASS restricted**: no static rank or representation-size inference to necessary arbitrary-machine work. |
| Relativization | **PASS for fixed-template finite combinatorics**; unrestricted P versus NP or oracle transfer OPEN, BGS/algebrization/Natural Proofs not bypassed. |
| Simultaneous DTISP | **NOT APPLICABLE WITH REASON** to a SAT lower bound: only a matched upper operation-checker ledger was proved. |
| Deterministic configuration counting | **PASS upper consistency safeguard only**, never a work lower bound or randomized/quantum result. |

All Horn/2-SAT/affine *instance subclasses*, treewidth, cycles, selectors, source-aware decompositions, direct counting, caching, products, unique-solution, changing fields/bases, and higher-arity nonlinear algorithms remain legal. Lack of affine template polymorphisms does not force any particular CSP decision algorithm or rule out efficient easy families. /341 remains FAIL as full UNSAT authority; /386 remains RESTRICTED.

## Ranked end-to-end dependency table

1. TMR-1 exact authenticated 3SAT -> 3COLOR -> undirected C5 -> T5 construction PROVED/EXACT restricted (independent /074 audit), and T5 NP-complete KNOWN THEOREM. Arbitrary-machine SAT lower-bound arrow **OPEN**.
2. TMR-2 adaptive NROBP and fixed-order OBDD representation lower bounds PROVED restricted on source-YES-trivial families; representation -> mandatory decision work **OPEN**.
3. TMR-4 source-derived FBDD compiler and positive four-path exact-count effects PROVED restricted; full all-algorithm necessity **OPEN**.
4. TMR-3 source-aware forest/module/Fourier/prime-incidence exact-count upper algorithms PROVED restricted; universal obstruction **OPEN**.
5. Fixed-template binary and all-arity affine polymorphism classification PROVED/EXACT here, but arbitrary nonlinear high-arity operations and machine-transfer claims **OPEN**.

**ONE highest-value next target:** an authenticated, genuinely mixed YES/NO T5 family with a representation-independent quantitative necessary-time/space invariant surviving all source-aware, adaptive, and algebraic algorithms. A lower-priority algebraic check would classify nonlinear higher-arity Taylor/WNU operations. No NP separation is inferred.

## Primary theorem sources

[1] Bang-Jensen, Hell, MacGillivray, *The Complexity of Colouring by Semicomplete Digraphs*, SIAM J. Discrete Math. 1(3) (1988), 281-298. https://doi.org/10.1137/0401029. The original abstract classifies semicomplete targets with more than one directed cycle as NP-complete, and this fixed T5 has five directed triangles.

[2] Barto, Kozik, Niven, *The CSP Dichotomy Holds for Digraphs with No Sources and No Sinks*, SIAM J. Comput. 38(5) (2009), 1782-1802. https://doi.org/10.1137/070708093. Original smooth-core dichotomy confirms the fixed template's known complexity. Neither source is claimed to contain the new direct small-template classification proved here.
