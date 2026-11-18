# SIGMA2 Circuit-SAT: ADAPTIVEQUOTIENT23
Date: 2026-11-17 America/Los_Angeles
STATUS: Proven restricted candidate-preserving reduction with finite tests. Independent mathematics review pending. No all-input SAT lower bound or exponent contraction. P vs NP OPEN.

## PROPOSE > SEARCH > BUILD
Five original hypotheses were saved to PROPOSALS_PRESEARCH.md before external search: X-adaptive observation H(X), affine-in-universal-seed coefficient extraction, shared-X selector slicing, global-period barrier, and fully charged P=NP accounting.
Repository read: PERIODBASIS22, SELECTOR_OBSERVABLE21, RANKQUOTIENT20, FIBERHOIST16, PHABSORB1.
Primary literature: Carlet, Boolean Functions for Cryptography and Coding Theory (2021), doi:10.1017/9781108606806; Wimmer et al. HQSpre (2019), doi:10.3233/SAT190115; Heule-Seidl-Biere QBF preprocessing validation (2017), doi:10.1007/s10817-016-9390-4; Williams STOC 2024, doi:10.1145/3618260.3649723. Related techniques are PRIOR ART; novelty claim limited to project-specific combined formulation.

## Exact certified candidate-dependent quotient
For E(X,B) and supplied polynomial-size GF(2) matrix circuit H(X) of r rows, certify with one ordinary SAT query that the miter
 [H(X)B=H(X)B'] AND [E(X,B) XOR E(X,B')]
is UNSAT; X is shared, B,B' independent. If certified, for EVERY candidate x,
 EXISTS B E(x,B) iff OR over z in GF(2)^r of
   [Reach(H(x)B=z) AND E(x,Rep(x,z))],
where a deterministic conditional Gaussian-elimination circuit computes Reach and canonical Rep with zero free variables. All original X inputs remain identical across observations and across selector branches. Explicit source size N, matrix-circuit size M: certification miter O(N+M+rb) gates; X-only quotient O(M+2^r(N+(r+b)^4)) gates conservatively; standard serialized CNF O(S log S) bits, fully charged. Counting identity: #B E(x,B) = 2^(b-rank(H(x))) * SUM_{z in image H(x)} E(x,Rep(x,z)). This does not assume constant rank as x varies.

## Affine-in-seed extraction
For arbitrary readable E, c(X)=E(X,0), a_j(X)=E(X,e_j) XOR c(X). One SAT miter checks E(X,B)=c(X) XOR sum_j a_j(X)B_j for ALL X,B. If UNSAT, exactly
 FORALL B NOT E(x,B) iff NOT c(x) AND AND_j NOT a_j(x).
Candidate-specific counterexample: B=0 if c(x)=1, else B=e_j for a_j(x)=1. Identity miter O(bN) gates and one charged SAT/UNSAT decision. New existential Tseitin traces are only for the X-only output; original B-dependent gate traces must stay after FORALL B.

## Explicit global-period obstruction and falsifiers
E_b(X,B)=X dot B with n=b: each fixed x has period codimension <=1, but the common global period space is {0}, with codimension b. This makes PERIODBASIS22's candidate-independent global kernel maximally pessimistic; H(X)=X is an adaptive one-row quotient. For b=20, 1,048,576 universal seeds per x reduce to <=2 observation states; only winning x=0. Materialized general DAG 120 nodes; functional CNF miter 120 variables,236 clauses,2619 bytes; winning DAG CNF 120 variables,236 clauses,2621 bytes. Optimized winning CNF 20 variables,20 unit clauses,123 bytes. Big miter UNSAT shown by exact algebra, NOT solved by DPLL.
Bad supplied H: E(B)=B1, H(B)=B0, invalid representative shortcut; miter SAT and must reject. NP-hard embedding E(X,B)=NOT F(X) AND B0 for arbitrary 3-CNF F has adaptive rank <=1 and QBF true iff SAT(F). No SAT-time lower bound follows. For k-bit selector and b-bit seed, complete challenge length is k+b, not k, and the same X is used for every branch.

## Executed tests
Primary standard-library verifier: all 65,536 Boolean truth tables for n=1,b=3 checked (exactly 256 affine); 4,096 arbitrary E,H pairs (196 certified, 3,900 rejected); 800 random adaptive families; 3,682 exact candidate/count checks; 479,018 equal-projection equality checks; adaptive correct SAT miter 66 clauses/691 bytes actually solved UNSAT with DPLL and fault-injected miter 81 clauses/864 bytes actually solved SAT. Independent verifier: 65,536 tables by second derivatives; 378,624 derivative checks; 2,046 bilinear candidate fibers; 2,036 nonzero-period exclusions; 2,008 complete trace/CNF checks. Zero failed assertions.

## Charged counterfactual and handoff
Hypothetical SAT time O(L^d) gives affine certificate plus final SAT calls conservatively O((bN log(bN))^d), not f(d)<d; general supplied-H quotient pays certification plus final solver on O(S log S) bits. Hidden arbitrary F(X) remains. Next: combine X-dependent H with affine reservoir kernels; derive rank(H(x)K) exact counts; test source-authenticated extraction on index-addressed and reconvergent nonlinear gates; seek hereditary low-rank guarantees and red-team all quantified trace placements. No general SAT lower bound. P vs NP OPEN.

## Additional exact certification complexity boundary (audited after initial commit)
AFFINE-SEED recognition (E(X,B) affine in B for every X) is coNP-complete for readable circuits. Reduction from UNSAT(F): E(X,b0,b1)=F(X) AND b0 AND b1 is affine in the universal bits for every X iff F is UNSAT. Candidate-dependent one-row FIBER-FACTOR recognition is also coNP-complete: supply H(B)=b0 and E(X,b0,b1)=F(X) AND b1. Fiber constancy holds iff F is UNSAT. Complementary witnesses are polynomially checkable; one ordinary SAT miter performs each check conditionally on a correct solver. The primary verifier exhaustively tested both reductions on all 256 Boolean functions on 3 X bits, with precisely one accepting function each. Certification cost is not free.

ADAPTIVEQUOTIENT23_SENTINEL_20261117