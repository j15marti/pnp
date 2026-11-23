# Decomposition Obstructions: DOUBLE-TRACTABLE-COMPATIBILITY1

**Date:** 2026-11-23 09:25 PST (America/Los_Angeles).
**Role:** PNP Decomposition Obstructions, independent constructive red-team.
**Target:** Uniform all-input polynomial-time decomposition for ordinary signed 3-CNF-SAT.
**Status:** PROVED/EXACT for elementary reductions and controls below, COMPUTATIONAL for finite tests, independent mathematical review pending. P versus NP remains OPEN.

## 1. Principal counterexample to an insufficient universal decomposition lemma

**Falsified claim (as a proposed sufficient criterion):** For every 3-CNF F, efficiently finding a polynomial number of individually satisfiable and polynomial-time decidable subproblems automatically yields a polynomial-time decider for F.

There is an immediate counterexample with **exactly two components**. For each clause C=(l1 OR l2 OR l3), assign C to H if it has at most one positive literal and to D otherwise. Then:
- H is Horn, satisfied by the all-zero assignment since every length-three H clause has at least two negative literals.
- D is dual-Horn, satisfied by the all-one assignment since every length-three D clause has at least two positive literals.
- F is exactly H AND D; the partition can be constructed in linear symbolic time.
- Nevertheless, deciding satisfiability of H AND D for arbitrary inputs is exactly ordinary NP-complete 3-SAT. The unknown information lies entirely in **global compatibility**, not in the existence, discovery or separate satisfiability of the two decomposed pieces.

This construction is elementary, not claimed novel. It establishes that *a finite polynomial-time tractable cover is not a sufficient P=NP theorem*. The missing theorem must provide a polynomial-time compatibility operator, a common witness, or a bounded exact interface **on every input**.

## 2. Second obstruction: even 2-SAT + Gaussian elimination is NP-complete to combine

Define MIXED-2SAT-AFFINE-SAT: input is a 2-CNF B and a list A of GF(2) linear equations; decide whether B AND A has a common Boolean assignment. The following stronger restricted family is NP-complete, by an explicit uniform decision reduction from 3-SAT, although B and A are *each satisfiable for every constructed input*.

Let F on n Boolean variables consist of m clauses C_i=(l_i1 OR l_i2 OR l_i3). Introduce new pairwise distinct selector bits y_i1,y_i2,y_i3 for every clause. Construct:

B(F) = AND over all i [AND over j<k (NOT y_ij OR NOT y_ik)] AND [AND over j (NOT y_ij OR l_ij)].

A(F) = AND over all i [y_i1 XOR y_i2 XOR y_i3 = 1].

Both modules are trivial individually:
- B(F) is 2-CNF, and the all-zero selector assignment satisfies B(F) for *any* original-variable assignment.
- A(F) is a disjoint system of length-three parity equations, independently satisfied by y_i1=1, y_i2=y_i3=0.
- The GF(2) rank is exactly m, with total nullity n+2m. The two modules share 3m selector variables; each selector occurs in only one affine equation and exactly three binary clauses. There is no difficult Gaussian solve or hidden expensive language recognition.

**Proof of exact decision equivalence.** In any joint model, each parity triple has odd Hamming weight (one or three). The three binary at-most-one clauses prohibit two or three ones. Thus exactly one y_ij equals one per clause. Its binary implication requires the corresponding l_ij to be true, hence the original C_i is true. Conversely, from any satisfying original assignment, select one true literal in every clause, set exactly its y_ij to one, and the binary and parity subsystems are simultaneously satisfied. Therefore:

SAT(F) iff SAT(B(F) AND A(F)).

Membership of the mixed problem in NP is immediate by certificate verification. Hence its restricted promise that both named components are individually satisfiable is NP-complete under a polynomial-time reduction (formally, an NP-complete restricted language with syntactically generated instances). This result is a direct explicit special case of the general boundary described by Schaefer's tractability classification [1].

**Size and cost.** The reduction uses n+3m variables, 6m binary clauses, and m length-three affine rows. The symbolic output size and construction time are O(n+m), or O((n+m) log(n+m)) bits and bit operations under explicit binary identifier encoding. Auxiliary selector rank/nullity and module satisfiability are known syntactically; zero-cost subsystem-oracle assumptions are unnecessary.

**Counting nuance.** If t_i(x) is the number of true literal occurrences of source clause i under assignment x, then the exact number of mixed models is sum over original x of product_i t_i(x). Consequently the reduction is decision-preserving, not parsimonious; no direct #P-hardness conclusion is taken from equality of counts.

**Alternative without XOR.** Replace each parity-and-at-most-one selector triple by choosing exactly one edge in a one-pigeon/three-private-holes matching subproblem. Matchings for distinct clauses use disjoint holes and are trivially feasible in isolation. Binary implication constraints connect the selected hole to a true original literal. This is the same exact 3-SAT reduction. Efficient matching plus efficient binary compatibility checks do **not** automatically make their conjunction efficiently decidable.

## 3. Minimal UNSAT and SAT-neighbor audit

Let F_8 consist of all eight possible signed length-three clauses on variables x1,x2,x3. Each Boolean assignment falsifies precisely one clause, so F_8 is UNSAT. Deleting any single clause creates a SAT instance with exactly one original satisfying assignment. The mixed encoding has:
- F_8: n=3,m=8, 27 total variables, 48 binary clauses, 8 disjoint parity equations, GF(2) rank 8, 24 shared selector bits. The two components are separately SAT; their conjunction is UNSAT.
- Each single-clause deletion: n=3,m=7, 24 variables, 42 binary clauses, 7 parity equations, GF(2) rank 7, 21 shared selector bits. Each neighbor is SAT with exactly 24 selector extensions for its one original assignment.

The extension count 24 follows because, after deleting its sole falsified clause, the remaining seven clauses have respectively three, three, and one clauses with one, two, and three true literals: 1^3 * 2^3 * 3 = 24.

The independently constructed generic unit-propagating DPLL program, using the standard four-3CNF-clause translation of each odd-parity triple, recorded 7 visited states on the UNSAT source and 8 to 12 states on the eight SAT neighbors. This is a *small easy adversarial semantic example*, not a certified hard benchmark. Separate parity and binary module deciders accept all nine inputs.

## 4. Independent finite checks, adversarial controls, and parameter ledger

Executed with standard Python in the current research run:
- Exact source-vs-mixed agreement on all 256 subsets of the eight signed three-variable clauses.
- Independent enumeration of *all mixed variables*, rather than only the source witness, for 93 subformulas with at most three clauses.
- Eight SAT neighbors of the minimally UNSAT eight-clause core; all have 24 mixed witnesses.
- 48 seeded random and planted three-literal instances (n=3 to 8); agreement and separate subsystem SAT.
- 16 seeded near-threshold random signed 3-CNF inputs (n=8,10,12,14, m≈4.3n): 13 SAT and 3 UNSAT, exact agreement, both modules separately SAT. No asymptotic hardness certified.
- Exponentially many distinct syntactic residuals on the easy 2-CNF family AND_i(x_i OR z_i): after fixing all x variables, each subset of remaining unit z_i is a different residual, giving exactly 2^n residuals (4096 at n=12), despite polynomial-time 2-SAT recognition.
- A high-treewidth easy family: all pairwise equalities x_i=x_j encoded by binary implications on n variables. Its primal graph is K_n, treewidth n−1, but a single SCC pass solves it. At n=20 this gives 380 binary clauses and treewidth 19.

**Parameter warning.** The representation has interface k=3m and nullity n+2m even though each module is trivially SAT. Gaussian elimination can find the rank in polynomial time, but cannot by itself certify compatible binary models. Neither the 2^k enumeration cost nor high treewidth nor the 2^n residual diversity constitutes an unrestricted lower bound. A universal polynomial algorithm might use a different semantic representation; proving it cannot do so would itself require new mathematics.

## 5. Resource and model audit

**Uniform reduction R:** deterministic streaming transducer; fixed code, no oracle or advice, handles arbitrary signed three-literal clauses. Let N be the encoded 3-CNF length. Explicit names and selectors, 6m binary records and m parity records are constructible in poly(N) time with poly(N) workspace. Clause and row recognition is direct, not a difficult classifier. There are no shared probabilistic coins.

**Independent subsystem solvers:** 2-SAT SCC and GF(2) elimination are polynomial. Here even predetermined witnesses prove their separate satisfiability, so their solution time can be omitted when evaluating the compatibility obstruction. The jointly correct verdict cannot be computed from the pair of Boolean subsystem verdict bits; both bits are always 1 for every constructed F.

**Same-execution cost example:** The exact source-enumeration control inspects up to 2^n assignments and O(m) clauses per assignment, T=O(2^n m polylog N) under a standard bit-cost implementation, S=O(N polylog N) bits including formula/input buffers, and physical cumulative bit-time CM no more than O(T S). The total minimum-description cumulative CM likewise has a trivial O(T S polylog T) machine-encoding ceiling; it is not established equal to physical CM. This is one deliberately exhaustive exact algorithm, not a compulsory cost for arbitrary solvers. Python tracemalloc peak numbers and wall time are implementation measurements, not native sole-tape T/S/CM.

**For any hypothetical polynomial-time compatibility algorithm:** all reduction, transformation, normalization, discovery, dynamic program, memoization, cache, representation, output, and source access costs must be charged in its one execution. Since R is polynomial, a uniform polynomial-time compatibility solver for this fixed class would immediately give an unrestricted polynomial-time 3-SAT solver; no such method is supplied by this report.

## 6. Exact failure conditions and next dependency

The elementary tests falsify any universal lemma with the consequent "individually tractable pieces + poly-time discovered cover => polynomial whole" unless the lemma additionally bounds the cost of satisfying *interpiece compatibility*. A sufficient corrected lemma could require all three simultaneously:

1. A polynomial-time uniform finder constructs the decomposition and authenticates every transformation.
2. Each bag/subproblem is solved soundly in polynomial time, including the cost of producing compatibility summaries.
3. The total computation of **compatible** summaries, including any adaptively selected interfaces, is polynomial in the encoded input size, for every source F.

A special case is a *computed* interface k<=C log N with 2^{O(k)}poly(N) compatibility. The present family has an explicit k=3m interface under its natural split, so it does not satisfy that hypothesis automatically. The existence of some other favorable representation is OPEN.

**Proposed next experiment:** take bounded-occurrence proper 3-CNF families and signed high-girth formula families, apply the same selector reduction, then measure computed incidence treewidth, residual canonicalization, SCC-and-Gaussian closure, clause-learning cost, and selector-vs-original variable backdoors. Search for *semantically nontrivial* fast summary languages and for sound instances where those summaries fail to compose. Cross-review issue #324's restricted frontier and checkpoint claims without transferring their model restrictions to unrestricted SAT.

## 7. Sources and prior work

[1] Thomas J. Schaefer, *The Complexity of Satisfiability Problems*, STOC 1978, pp. 216-226, DOI https://doi.org/10.1145/800133.804350. Tractability classification by constraint language; our explicit selector reduction is not claimed as a novel NP-completeness phenomenon.

[2] Naomi Nishimura, Prabhakar Ragde and Stefan Szeider, *Detecting Backdoor Sets with Respect to Horn and Binary Clauses*, SAT 2004, https://ac.tuwien.ac.at/files/pub/nishimura-ragde-szeider-2004.pdf. Their published distinction between parameterized tractable strong-backdoor detection and W[2]-hard weak-backdoor detection constrains claims about cheaply finding useful structure.

[3] Marko Samer and Stefan Szeider, *A Fixed-Parameter Algorithm for #SAT with Parameter Incidence Treewidth*, arXiv:cs/0610174, https://arxiv.org/abs/cs/0610174. Bounded width is a legitimate sufficient condition when width and its representation costs are included, not a universal guarantee.

[4] Internal baseline: https://github.com/j15marti/pnp/blob/main/research/main/T5_Resource_Lower_Bounds_Exhaustive_Handoff_2026-11-21.md and https://github.com/j15marti/pnp/issues/324. The project already distinguishes restricted representation lower bounds, actual physical CM, minimum-description CM and the scalar-decision obstacle. This work addresses a **constructive decomposition sufficiency** claim; it does not assert the T5 lower-bound bridges were closed.

**Independent review:** Pending. No native tape runtime, complete project-wide preflight, arbitrary 3-SAT polynomial decider, or lower bound for unrestricted machines was executed/proved.