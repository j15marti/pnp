# TMR-4/087 | Exact frontier-10 OBDD and 4-connected high-q cheap-source falsifier

**2026-11-18 PST | additive to /086.** The source is the five-valued CSP with R(a,b) iff (b-a) mod 5 in {1,3}. See living manuscript Section `sec:t5frontier087` for theorem statements and self-contained proofs. This is a restricted upper bound and a counterexample to erroneous representation-hardness transfers, not an unrestricted machine lower bound.

## Precise candidate

For a fixed variable order, at level t store a nonempty five-bit domain mask only for each *unqueried vertex adjacent to a queried vertex*. Each such mask is one of five translate-pairs or five singletons; the full mask belongs only to an untouched variable, and the empty mask sends the computation to a complete-query rejecting chain. With maximum future-boundary size b, exact five-way OBDD width is at most 10^b+1 and internal nodes at most n(10^b+1). Every original 5^n assignment retains its exact terminal decision, including accepting and rejecting multiplicities. The general 32-mask interface with AC propagation between unassigned variables is broader and not contradicted.

A particularly relevant family is the undirected square C_n^2, n>=10 divisible by 5. Its two-orientation SAT/UNSAT sources have m=2n, q=n+1, 4-vertex connectivity, clique number three (no T5 palette), linear minimum vertex cover n-floor(n/3), no false twins, connected complement, and no separators of size <=3. The SAT orientation is x_i=i mod 5. The UNSAT orientation includes the five arcs 1->0, 2->0, 2->1, 3->1, 2->3. The two transitive triangles force the common edge 2->1 to have simultaneously color differences 3 and 1. Source-only recognition counts common neighbors of each underlying edge (two for distance-one cycle edges, one for distance-two edges), checks the extracted cycle and its exact square, and obtains a cyclic order with b<=4. Thus both are efficiently compilable, with the conservative width bound 10001.

## Four falsifiers

1. Reverse orientation is not Boolean negation of R on equal colors. Loops and antiparallel arcs must remain inconsistent.
2. The unrestricted 32-state arc-consistency interface does not force 32 states for forward-only frontier propagation. The UNSAT example itself remains fully unary arc-consistent from full domains.
3. Odds-first *fixed* orders on the SAT family have observed widths 21,311,1731,7871,41486 for n=10,15,20,25,30; recovered cycle orders have 46,96,101,101,101. This is finite order dependence, not minimum-FBDD hardness or an asymptotic lower bound.
4. High cycle rank, 4-connectivity, linear cover, lack of twins and K5 palette do not imply expensive source computation.

## SAME_REALIZATION and four verification gates

The reference program parses actual canonical input bytes, validates zero-based vertices and unique directed arcs, handles loops and reverse arcs, scans graph endpoints to build every frontier (charged <=2m(n+1) comparisons), allocates each reachable state, five-way fan-out, merges exact mask vectors, maintains a depth-specific reject chain, computes both counts with arbitrary-precision integers, and explicitly prices result storage and writing. The cycle-square recognition and chosen variable order are source-computed rather than supplied by a target oracle. Cost upper bound O(nm + 5(10^b+1)(m+nb)) finite RAM operations, plus hash allocation, precision, and output. No Fourier transform, cache eviction, or adaptive switching was used. A validity-checked grouped three-bit decoder has at most six binary nodes per five-way node; direct literal CNF uses 3n+15m clauses and 9n+90m literals.

**G1:** 72 authenticated small source cases, 14 SAT/UNSAT cycle-square cases, eight malformed sources rejected and six small structural certificate checks. **G2:** 234,360 exhaustive five-way pointwise comparisons and valid-code checks, plus 10,189 executed literal CNF checks on valid codes and 4,680 executed complete three-bit code checks. **G3:** 14 independent color-state DP counts in Python and 14 independent full-color BigInt DP counts in Node, five alternate-order count equalities, and 625 assignments excluding the four-vertex obstruction. **G4:** byte-identical Python and Node reruns, zero unexpected failures.

At n=200, SAT: m=400, q=201, width 101, 19,304 actual diagram nodes, count **627376149393920708177194198820147825840010**. UNSAT: count 0. At n=30, bad-order width 41486 versus good-order width 101.

Audited Python SHA-256: `efeb9172adc01c7b7fb8b204f77e6fbd7dc0d9cc1c1b3a95abcf90c29de1b330`. Independent Node SHA-256: `aba26d359bbf3f79d9003885f9efe02df4472a8f5390255a9f71e1642c764363`. Raw JSON SHA-256: `acf3bc8bfa4ac64d2bdafa426bce1907ee79b9a1e75851bd081a7fd6a2f2f7b3`.

## Follow-up dependency

**D4-T5-HIGH-Q-HIGH-FRONTIER-UNRECOGNIZED-088.** Challenge mixed SAT/UNSAT source graphs with *growing minimum frontier*, no local triangle certificate, and no cheap gauge, palette, separator, backdoor, 32-mask, twin, quotient or pathwidth recognition. Seek genuine minimum native five-way FBDD vs unrestricted interleaved-bit Boolean FBDD separation only on the same authenticated source; continue charging parsing, finding the representation, sharing and output. Keep unrestricted reverse transfer OPEN. Independent mathematical review and physical-machine microsteps OPEN. P versus NP OPEN.

Reference: Barto, Kozik, Niven, SIAM J. Comput. 38(5), 2009, DOI 10.1137/070708093 establishes NP-completeness of this fixed-template smooth tournament CSP, not a deterministic lower bound.
