# SIGMA3-RESIDUAL59: Unrestricted Circuit-SAT residuals defeat bilinear grammar closure
Date: 2026-11-17 America/Los_Angeles. Scientific status: PROVED/EXACT scoped embedding, COMPUTATIONAL tests; P versus NP OPEN.

## IDEAS PROPOSED BEFORE LITERATURE
CANDIDATE A: append arbitrary nonlinear residual to the authenticated bilinear Sigma3 system, test whether affine strategy solver survives. CANDIDATE B: pin XOR residual and check affine closure. CANDIDATE C: pin Horn residual and check Horn closure. CANDIDATE D: test unique-gate-trace and pinning source retention; falsifier: linear-size untouched blocks. Original proposals recorded separately before research searches.

## LITERATURE CHECK AND REVISIONS
Read BILINEAR58 project handoff, Schaefer STOC 1978, Dowling-Gallier JLP 1984, Akshay et al SAT 2026. Horn and affine closure are known. Appending unrestricted gates invalidates affine closure; syntactic one-bit restriction does not ensure sublinear queries.

## CONSTRUCTION OR PROOF ATTEMPT
For any circuit D(u), define Phi_D = exists x forall y exists z,u: [z=x XOR (x AND y)] AND D(u). For each x,y, z is unique. Phi_D TRUE iff D SAT. A winning strategy must supply a D witness; if D UNSAT, a challenge y=0 defeats any x. This is a uniform source-only Circuit-SAT reduction, not a solver-dependent A->A' contraction and not a lower bound.

The AND terminal relation {(0,0,0),(0,1,0),(1,0,0),(1,1,1)} is not affine: XOR of the first three tuples is (1,1,0), which is absent. Existential projection of an affine system is affine. Thus no purely affine system with existential auxiliary variables defines the unrestricted AND terminal relation. Nonlinear residuals do not inherit BILINEAR58's affine grammar.

Horn and XOR restrictions are individually closed under variable pinning. But the ordinary source-retained restriction compiler leaves every clause untouched that omits the pinned variable. Theta(N) disjoint residual clauses therefore produce immediate child encodings of Omega(N) records; this is NOT a lower bound on all equivalent encodings.

With hypothetical SAT solver time exponent K, space exponent L, n<=N bitwise SAT self-reduction calls of length O(N) require at most N^{K+1+o(1)} time and N^{max(1,L)+o(1)} writable bits. Child-size exponent lambda=1. All source scans, query materialization, negative SAT results, and witness verification charged at this conservative level. Independent block grammar can have lambda<1, but is not established for arbitrary circuits or recursively inherited.

## TESTS AND OUTCOME
Primary Python script: 702 instances (234 Horn, 234 XOR, 234 nonlinear), 650 SAT, 52 UNSAT, 5175 actual serial witness self-reduction calls, 113835 assertions, zero discrepancies. Source record ledger: 33645 child constraint records versus 38449 parent records across calls, with 27023 unchanged. Independent exhaustive QBF script: 300 cases (224 true, 76 false), 11144 assignment evaluations, zero discrepancies. Guard against x/y prefix swaps, simple z=y and GF2 strategies, non-affine AND, and long untouched clauses. These are finite checks only.

Smallest remaining theorem: acquire from arbitrary solver A a cheap, exact, inheritable semantic certificate producing sublinear ordinary SAT children with both YES/NO strategy preservation and joint time-space accounting. Next adversary: SAT-dependent nonlinear selector coupling Horn and XOR components and indirect memory addresses.

FINAL-SENTINEL-SIGMA3-RESIDUAL59-OPEN
