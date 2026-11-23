# Meta Solver Theorem: exact rational nullity, certified compatibility and an all-moduli blind spot

**2026-11-23 10:37 PST**, agent namespace: \`research/agents/meta-solver-theorem\`. Coordination: [issue #324](https://github.com/j15marti/pnp/issues/324). Status: **PROVED** for the explicitly defined parameterized upper bound, **PROVED** for the finite algebraic counterexample, **COMPUTATIONAL** for the tests; **OPEN** for any universal polynomial-time coverage claim. Independent peer review **PENDING**.

This advances the 09:35 COMPATIBILITY-BARRIER-1 / MODULAR-EXACT-ONE-CERT-1 report. Unlike the original GF(3) Fano control, the new 6-variable, 5-edge UNSAT control passes **every** finite-field consistency test of its extracted exact-one equations. Nevertheless, an automatically discoverable exact rational-linear plus Boolean-nullity algorithm decides it with two free-coordinate trials.

## Scope, machine, and quantifiers

Input: an explicitly listed 3-CNF \`F\` with n Boolean variables and m clauses, with a fixed standard binary encoding of total length \`N = Theta(n + m log(n+1))\` (allow shorter clauses, repeated clauses, and a unary or otherwise polynomially bounded variable declaration). We make **no SAT promise**. Ordinary signed literals and all residual clauses are preserved.

Fix **one uniform algorithm** A, independent of the instance. It may extract only **certified syntactic exact-one gadgets**, simplify explicit binary implications, and use exact rational row reduction. Each such step must read its source clauses, not claim a semantic constraint from a heuristic guess. Algorithm A is complete by an explicit enumeration of residual free Boolean coordinates.

For a 3-set \`{x,y,z}\`, we recognize either of the following clause patterns:

1. \`(x OR y OR z)\` AND all three \`(NOT x OR NOT y)\`, \`(NOT x OR NOT z)\`, \`(NOT y OR NOT z)\`.
2. All four clauses encoding \`x XOR y XOR z = 1\` AND the same three at-most-one binary clauses.

Either pattern **entails** \`x+y+z=1\` **over the integers**, where each x is a Boolean 0/1 variable. Recognizers scan/sort/hash *fully present clauses*, not assumed hidden equivalent relations. For duplicate or signed-equivalent variables, substitute only identities proved by mutual reachability in the binary implication graph; x=1-y is permitted and induces a signed coefficient.

After sound binary SCC quotient, let q be the number of remaining independent Boolean variable-pair classes, let Mz=b be the recognized integer equations, and let r be their rank **over Q**. Define the **computable rational-nullity parameter**

\`k(F) = q-r\`.

It is computed in polynomial bit complexity from the input. This is *not* the number of original CNF variables, XOR GF(2) nullity, or a claim that the quotient captures all structural reductions.

## Theorem META-RATIONAL-NULLITY-1 (proved)

For every explicitly listed 3-CNF F, the above *fixed uniform algorithm* decides SAT(F) correctly in

\`T(F) <= 2^{k(F)} poly(N)\`

bit operations, with \`poly(N)\` peak workspace. The polynomial includes recognition, binary implication graph construction and SCC, signed quotient construction, rational elimination with bounded-length integer arithmetic, construction of full candidate assignments, and testing **every original CNF clause**.

If \`k(F) <= c log_2 N\` for an absolute fixed c on a class of inputs, this gives a polynomial-time decider on that class. It does **not** show that arbitrary 3-CNF has such k, nor that a different set of constraints increasing rational rank can be found within polynomial time.

**Proof and exact Boolean-completion induction.** Each accepted exact-one pattern is verified on all its explicit clauses; all satisfying assignments satisfy its integer equality. The implication graph ensures that any two literals in the same SCC are logically equivalent whenever the binary subsystem is satisfiable; if a variable and its negation share an SCC, that subsystem already supplies an UNSAT certificate. Choose one Boolean representative per remaining signed pair and substitute into each certified integer equation. Thus every SAT assignment maps to a binary solution of Mz=b.

Compute exact reduced row-echelon form R over Q. If an inconsistent row \`[0 ... 0 | a]\`, a != 0, appears, no Boolean assignment exists. Otherwise let the free coordinates be \`f_1,...,f_k\`. By induction on j, branching over choices of the first j free bits covers every Boolean solution whose first j free coordinates equal that prefix. The invariant holds at j=0; either value 0 or 1 of f_(j+1) is explored, preserving exhaustive coverage. At j=k the pivots are uniquely determined rational expressions in the selected free bits. A fractional, negative or >1 pivot rejects that branch; if all coordinates are binary, map them back through signed SCC representatives and verify the **entire** original F. If one candidate satisfies F, return SAT with its assignment. If all 2^k choices reject, the induction proves UNSAT. Every operation is explicit.

The rational coefficients have polynomially bounded bit length for 0/1 signed-incidence matrices, by determinant/Hadamard bounds or fraction-free elimination. This establishes the stated bit complexity. A negative certificate can log the exact RREF and one checked rejection reason per Boolean free-bit vector. Its size and verification time are \`O(2^k poly(N))\`; this is **not** a claimed polynomial-sized UNSAT certificate when k is large. A separate local checker confirms each rejection for the two root instances.

**Charged ledger:** fixed-code and input access, clause normalization, exact-one discovery, SCC and its implication edges, signed substitution, rational arithmetic with numerator and denominator lengths, all 2^k candidate constructions, residual clause scans, witness/output, proof log generation and verification are all paid. In a bit-RAM model both running time and cumulative memory are \`2^k poly(N)\`; peak workspace is polynomial *excluding an optional saved exponential certificate*, which may instead be streamed. On a fixed sole-tape machine, standard simulations incur further polynomial factors; physical CM is bounded by time times faithful visited span. No native tape step counts, physical CM traces, or fixed minimal-description CM experiments were performed. This bound is an **upper** bound, not a compulsory-work lower bound for unrestricted solvers.

## Lemma ALL-FIELDS-BLIND-1: five deletion-minimal clauses (proved)

Six Boolean variables x0,...,x5. Require exactly one true variable on each of:

\`(0,1,2), (0,1,3), (0,2,3), (0,4,5), (1,2,4).\`

**UNSAT proof:** The first three equations force x1=x2=x3=t and x0+2t=1. For Boolean t, the only legal choice is t=0 and x0=1. The fourth then forces x4=x5=0. The fifth requires x1+x2+x4=1, contradicting 0=1.

**Every finite-field consistency test fails to refute it:** The *integer* vector \`(-1,1,1,1,-1,3)\` satisfies all five linear equations Mz=1. It therefore maps to a solution modulo **every prime**, indeed every modulus, although it is not Boolean. Consequently, adding any finite collection, or even all, direct field-consistency checks on these equations does not decide this instance. This is a falsifier of a proposed **modular-consistency-only** completeness theorem, **not** of modular propagation interleaved with sound Boolean bounds or general clause learning.

The instance is clause-deletion-minimal: deleting each of the five rows leaves, respectively, **1, 2, 2, 2, 1** Boolean satisfying assignments. The positive ONE-IN-THREE clauses admit ordinary 3-CNF encodings by one positive ternary clause plus three binary at-most-one clauses; alternatively odd XOR plus those binary clauses gives a mixed affine/2SAT representation. Each subsystem is individually SAT. The overall conjunction is UNSAT.

Its Q-incidence rank is 5 on six variables: **k=1** and two Boolean free-coordinate checks suffice. Thus all-fields consistency misses it, while *integrality/bounds-aware rational elimination* detects it cheaply.

## Explicit interface discovery and the SCC quotient

For the above 5-edge problem, replace each occurrence of an original variable by an occurrence copy and add 2-CNF equality implications connecting copies. The copied system has **15** Boolean variables, **5 disjoint XOR rows**, **33 binary clauses**, and **53 CNF clauses** when XOR is expanded. XOR alone is SAT; the binary subsystem alone is SAT.

If equality copies are ignored, Q-rank is 5 and k=15-5=10, so full Boolean-free-coordinate enumeration has **1,024** trials. A polynomial-time binary implication SCC quotient identifies six representative variables, keeps Q-rank 5, and reduces k to **1** and the trials to **2**.

On the 7-line Fano UNSAT control, the corresponding values are **21 copies**, **7 XOR rows**, **49 binary clauses**, **77 CNF clauses**. Without the equality quotient, k=14 and the exact enumeration has 16,384 trials. With SCC, q=7, rank over Q =7, k=0, and one rational candidate has nonbinary pivots. GF(3) also already refutes this particular Fano system by summing its 7 equations. Every Fano line deletion is SAT with exactly one Boolean model.

This is a constructive, explicitly charged **representation-discovery and parameter-reduction theorem for a restricted family**, not an uncharged semantic oracle.

## Counterexample CANONICAL-CORE-COLLISION-1 (proved)

Consider the same recognized exact-one equation x1+x2+x3=1, but retain non-exact-one residual clauses. The formula \`ExactOne(x1,x2,x3) AND x1\` is SAT; the formula \`ExactOne(x1,x2,x3) AND x1 AND x2\` is UNSAT. Their extracted exact-one matrices and rational RREFs are **identical**. Deduplicating residuals using *only* the Gaussian-normalized equation matrix is UNSOUND.

A shared proof-DAG cache must include the residual CNF and current assumptions or a separately certified equivalence. Isomorphism, symmetry, semantic selectors, proof translation and global compatibility all have nonzero acquisition costs.

## Finite experiments and reproducibility

The [standalone GitHub Python checker](2026-11-23_1037_modular_blind_reproducer.py) validates the two root hypergraphs, every single-line-deleted SAT neighbor, an integer witness valid over all fields, rational RREF, and 100 seeded random small exact-one hypergraphs (n=4..8). All checks pass: 100 random cases, **47 UNSAT**, zero contradictory finite-field conclusions on SAT cases, and both root systems UNSAT. It is a deliberately compact independently runnable mathematical test rather than a full general SAT solver.

A more extensive local Python implementation also performs certified gadget recognition from arbitrary input CNF, 2SAT SCC signed quotient, rational RREF, 2^k enumeration with complete original-clause checking, and a small explicit rejection-table certificate and checker. In its **54** deterministic tests (36 ordinary random 3-CNF, 18 structured roots/neighbors/encodings), all labels agree with exhaustive Boolean enumeration for n<=13 or the exact occurrence-copy equivalence for larger encodings. Outcomes: **36 SAT and 18 UNSAT**. The 36 random 3-CNF cases revealed **zero** syntactically extractable exact-one rows, and the algorithm fell back to full Boolean search. The two UNSAT root rejection certificates checked; one-coordinate deliberate corruption was rejected by the checker. These are finite computational audits, not formal verification of the software and not asymptotic evidence.

Observed local Python ablations (noncomparable as machine lower bounds): copied 5-edge root with SCC k=1, 2 trials vs without SCC k=10, 1024 trials; copied Fano with SCC k=0, 1 trial vs without SCC k=14, 16384 trials. This exactly separates **productive representation discovery** from **moving branching into an opaque compatibility interface**.

## Peer comparison and review request

- **Decomposition Obstructions, 09:25:** Its two individually tractable languages can encode NP-complete compatibility. Our result does not evade that barrier. It formalizes a *computable parameter* under which compatibility is FPT, plus a smallest-found-by-this-test modular-only blind control.
- **Constructive Meta-Algorithm, 09:26-09:31:** Its sound same-residual crossfeeding and 31-instance ablation support paid interactions. Our exact-one extraction + signed SCC + Q-rank adds a second, independently sound information-sharing route, including Boolean-domain integrality that ordinary GF(2)/GF(3) checks cannot replace.
- **T5 resource handoff (21 Nov):** Retain C/R relation distinction and decision vs exact counting; a restricted upper bound on Boolean CNF neither proves a strict-T5 lower bound nor collapses P versus NP. Explicitly charging a shortcut remains essential.
- **GF(3) Fano report, 09:35:** Fano is an impressive *positive* algebraic crossfeed, but an inadequate universal test; the new 5-edge counterexample proves that consistency over every modulus can still be powerless.

**Next dependency for peer review:** audit the binary SCC signed-quotient orientation; verify rational rank and all five deletion-neighbor counts; then ask whether additional, polynomially discoverable **integer-domain** deductions decrease k on hard, connected, globally coupled 1-in-3 SAT families. A universal P=NP theorem would still need to bound the resulting k by O(log N), or give another polynomial-cost shortcut, on **every arbitrary 3-CNF**. No such theorem has been proved.

## Sources

1. Schaefer, T. J. (1978). The complexity of satisfiability problems. STOC, pp. 216-226. https://doi.org/10.1145/800133.804350.
2. The 2026-11-21 T5 exhaustive handoff: \`research/main/T5_Resource_Lower_Bounds_Exhaustive_Handoff_2026-11-21.md\`.
3. Constructive Meta Algorithm 09:31 and Meta Solver Theorem 09:35 reports in this repository.
4. Decomposition Obstructions 09:25, see issue #324 comment and review PR #325.
