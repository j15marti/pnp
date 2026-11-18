# TMR-5/077: all-arity cyclic-polymorphism firewall for the exact five-symbol beat CSP
Date: 2026-11-17, 18:40 PST. Identity: TMR-5 / PNP Machine Bottleneck Redteam. Named dependency: D5-T5-ALL-ARITY-CYCLIC-FIREWALL. Status: PROVED/EXACT for this fixed five-element relational template, external independent mathematics review OPEN. Finite tests COMPUTATIONAL. P versus NP OPEN.

## Candidate, exact quantifiers, and falsifiers before primary-source search

For every integer k>=2, there is NO cyclic k-ary polymorphism f:T5^k->T5, meaning a total operation satisfying both (i) all coordinatewise original R-arcs map to original R-arcs and (ii) f(x0,...,x(k-1))=f(x1,...,x(k-1),x0) for every tuple. The template is exactly Z5 with R(a,b) iff (b-a) mod 5 is 1 or 3. This is an operation-algebra claim, not a worst-case computational-work claim. Falsifiers: an arity with no directed closed walk in the target; an alleged coordinatewise product edge containing a forbidden tournament arc; cyclicity failing to identify the two tested input tuples; and a commutative binary operation missed by the prior independent all-binary classification.

The full chain is authentic fixed ten-arc template -> O(k)-length source-derived directed-walk certificate -> genuine edge of product digraph T5^k -> cyclic evaluation of both endpoints -> forbidden irreflexive target loop -> absence of that polymorphism -> correctly scoped finite-core algebraic tractability obstruction. No assertion of a general SAT-machine lower bound, NP hierarchy, or P-versus-NP consequence.

## Theorem 1: no cyclic polymorphism of any arity k>=3

Set j to the least nonnegative residue of 2k modulo 5. For k=3, j=1; for every k>=4, j<=4<=k. Choose any sequence of k increments with j entries equal to 3 and k-j entries equal to 1. Their sum is k+2j, congruent to k+4k=0 (mod 5). Starting at a0=0 and adding these increments modulo 5 produces a closed directed walk a0->a1->...->a(k-1)->a0 in the exact R-template. Repeated vertices are allowed, as they are in a directed walk and in an operation tuple.

Let x=(a0,...,a(k-1)) and y=(a1,...,a(k-1),a0). Every coordinate satisfies R(x_i,y_i), so (x,y) is an authentic directed edge of T5^k. If f is a polymorphism, R(f(x),f(y)); if f is cyclic, f(x)=f(y). But R(t,t) is false for every t. Contradiction. The proof is uniform for each k, covers nonlinear operations, and assumes neither idempotence nor affine form.

Small exact certificates: k=3 uses increments (3,1,1) and tuple (0,3,4); k=4 uses (3,3,3,1) and tuple (0,3,1,4); k=5 uses five 1-increments and tuple (0,1,2,3,4). The same modular recipe works at every larger arity. This direct obstruction is mathematically elementary and should not be misrepresented as a new general CSP dichotomy theorem.

## Theorem 2: binary cyclic operations are also absent

A cyclic binary operation is commutative. TMR-5/075 independently proved that *every* binary polymorphism of this T5 template, not just every affine one, is a rotated projection f(a,b)=a+t or f(a,b)=b+t, t in Z5. None is commutative. The proof uses the authentic shifted-diagonal subcopies and the closed five-step offset walk, not an unverified large-arity extrapolation. The present independent executable also enumerates all 5^5 shifted-diagonal profiles against all 100 genuine product arcs and recovers precisely the ten profiles, no commutative one. The arity-two case cannot be obtained by the directed-closed-walk argument: this tournament has no directed two-cycle, as expected.

Combining theorems 1 and 2 gives: **for every k>=2, there is no cyclic k-ary polymorphism of the exact T5 template**. Unary rotations exist; they do not conflict with this statement.

## Consequence, primary sources, and strict limits

The template is a core: mapping two distinct tournament vertices to the same image would send their connecting directed arc to a forbidden loop. In the idempotent singleton-expanded finite-core algebra, any Taylor term would imply a cyclic term of every prime arity p>5 (Barto and Kozik, 2012, cyclic terms theorem). The explicit all-arity obstruction rules this out. Via the standard algebraic NP-hard direction, this independently corroborates the known NP-completeness classification; it is NOT a new reduction or a resource lower bound.

Primary classification: Bang-Jensen, Hell, MacGillivray, *The Complexity of Colouring by Semicomplete Digraphs*, SIAM J. Discrete Math. 1(3), 1988, 281-298, DOI 10.1137/0401029. Original theorem: a fixed semicomplete digraph containing more than one directed cycle has NP-complete homomorphism CSP. Primary algebraic result: Barto and Kozik, *Absorbing Subalgebras, Cyclic Terms, and the Constraint Satisfaction Problem*, Logical Methods in Computer Science 8(1:7), 2012, DOI 10.2168/LMCS-8(1:7)2012 (Taylor finite algebra has p-ary cyclic term for each prime p exceeding domain size). These original results were checked through accessible original journal/article pages. No formal proof assistant kernel was executed.

The obstruction excludes cyclic and totally symmetric all-arity polymorphisms, not every conceivable nonlinear higher-arity operation, direct CSP decomposition algorithm, Boolean-circuit algorithm, Fourier algorithm, or source-aware shortcut. It does not establish that any T5 instance needs superpolynomial work. TMR-1's authenticated 3SAT-to-T5 chain remains a valid *upper reduction* only; no representation-to-arbitrary-machine lower bound exists.

## Complete physical ledger for the verified diagnostic, not an alleged SAT solver

Given a canonical unary k declaration, a fixed sequential blank-start deterministic bit-machine first authenticates the k field and template constants, computes j=(2k) mod5, generates k increments and a k-entry label tuple, checks every arc and the final closed edge, and writes the explicit witness; source traversal, counters, addresses, modulo-five arithmetic, retained tuple and output are charged. With full input length N>=k and output length O(k), the conservative paired upper is T=O((N+1)^3), S_peak=O((N+1)^2) in a conventional locally headed bit-machine. A streaming variant uses less. This certifies the product-graph obstruction, not generic CSP satisfiability.

Exact CPython 3.13.5 program `tmr5-t5-cyclic-obstruction077.v1` has no randomness: checked all 10 template arcs and all 5^5 binary shifted-diagonal profiles against 100 product arcs, identified 10 valid binary maps and zero commutative ones, and checked all 998 constructed cyclic-product edges for k=3,...,1000 (500,497 individual original coordinate arcs), with zero failures. The symbolic proof establishes all larger k; finite evidence is COMPUTATIONAL. Executed script SHA256 3878bfe4a2eb276339b22d1c98df26798e11cf6e6c304f33520150529674a340; raw JSON SHA256 85d42c84c396d99b9e44629192914e5d07e57f51490866393944d8b7e8b8f845. Python compile and second execution performed locally. Repository preflight was NOT RUN: no local checkout and git DNS inaccessible. Full manuscript LaTeX compilation, Lean/nanoda, native TM step-trace and external mathematical peer review NOT RUN.

## Four mandatory gates and controls

| Gate | Exact verdict |
| --- | --- |
| DISJ sanity | PASS restricted: no rank/representation-size to unrestricted work inference; DISJ small-circuit counterexample remains intact. |
| Relativization | PASS for local finite-template algebra as an intermediate statement; any all-oracle P vs NP separation OPEN and not asserted. Algebrization/Natural Proofs remain nontrivial if attempted. |
| Simultaneous DTISP | NOT APPLICABLE WITH REASON to a lower-bound contradiction: only paired upper diagnostic time/peak space are claimed. |
| Deterministic configuration counting | PASS as upper-bound consistency safeguard only, never a necessary-work lower bound or quantum/randomized transfer. |

Source-aware polynomial easy families remain legal: Horn/2SAT/affine restricted sources, explicit independent products, directed cycles, K_{s,t}, bounded treewidth, lower-degree peeling, twin/cofactor quotient, virtual checkpoint alternatives, adaptive OBDD/FBDD, exact counting, unique-solution indicators, caching, switching, padding, selectors and group/Fourier transforms. No gauge or rank descriptor becomes a compulsory arbitrary-machine step. Historical /341 full-UNSAT FAIL and /386 RESTRICTED unchanged.

## Ranked end-to-end synthesis and single next target

| Rank | Named chain | Status and barrier |
| --- | --- | --- |
| 1 | TMR-1 authentic signed 3SAT -> 3COLOR -> C5 -> T5 and its verified labelled-image quotient | PROVED/EXACT restricted, original T5 NP-complete KNOWN THEOREM; representation-independent T5 decision lower bound OPEN |
| 2 | TMR-2 dynamic cofactor and mixed YES/NO NROBP source controls | Restricted exact upper/representation results; source-aware easy mixed families falsify necessary-work promotion |
| 3 | TMR-4 full original-assignment OBDD/FBDD and twin quotient | Restricted exact upper compilation; bounded representation->unrestricted machine cost OPEN |
| 4 | TMR-3 prime-incidence/missing-triple exact counting | Restricted exact upper families; general checkpoint evaluator and necessary-time result OPEN |
| 5 | This all-arity cyclic-polymorphism firewall | PROVED/EXACT fixed-template algebra; excludes a class of tractability operations, not direct solver ingenuity |

**ONE highest-value next dependency:** an explicit quantified representation-independent *necessary-work* lemma for genuinely mixed YES/NO source-authenticated T5 instances, surviving paid 3SAT-image inverse, rigid-triad quotient, directed-twin quotient, local consistency, adaptive/Boolean branching programs, and all legal direct source-aware and algebraic algorithms. P versus NP remains OPEN.
