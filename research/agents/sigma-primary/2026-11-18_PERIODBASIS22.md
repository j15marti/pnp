# SIGMA2 Circuit-SAT: PERIODBASIS22 (2026-11-18)
Status: PROVED project-specific restricted/promise reduction, finite tested; independent mathematical review pending. NO all-input SAT lower bound or exponent contraction; P versus NP OPEN.

## PROPOSE BEFORE SEARCH
The local PROPOSALS.txt was recorded before literature and repository search: recover unknown low-rank Boolean observation H using SAT-certified translation periods; prove a randomized low-rank promise sampler; integrate with affine observable quotient; check hidden period and syntactic support adversaries; fully charge hypothetical P=NP resources.

## SEARCH
Primary Carlet, Boolean Functions for Cryptography and Coding Theory, pp. 120-121 (translation-derivative linear kernel prior art), https://www.math.univ-paris13.fr/~carlet/book-fcts-Bool-vect-crypt-codes.pdf ; Soos, Gocht, Meel, CAV 2020, https://meelgroup.github.io/publication/cav20sgm/ ; Dudek, Phan, Vardi CP 2020, https://arxiv.org/abs/2008.08748 ; Williams STOC 2024, https://doi.org/10.1145/3618260.3649723.
Project files read: research/agents/sigma-primary/2026-11-18_SELECTOR_OBSERVABLE21.md, 2026-11-18_RANKQUOTIENT20.md, and sigma3-strategy/2026-11-18_0531KST_SIGMA3_AFFINEBASIS55.md.

## EXACT RESTRICTED THEOREM
For readable Boolean circuit E(X,B) with n shared outer bits X, b universal boundary bits B, source length N, define global zero-derivative periods
T={v in GF(2)^b: for all x,B E(x,B)=E(x,B xor v)}.
T is a linear subspace. Promise r*=b-dim(T)<=r0. A randomized search samples v uniformly and checks membership via one complete SAT difference miter D_v(X,B)=E(X,B) xor E(X,B xor v) per candidate (UNSAT iff v belongs to T). It finds b-r0 linearly independent certified periods with probability at least 1-epsilon after at most
q=(b-r0) ceil(2^(r0+1) ln((b-r0)/epsilon))
trials/calls, for b>r0; identity H for b=r0.
After j<b-r0 independent periods, the probability that a random v belongs to T but not their span is (2^dim(T)-2^j)/2^b >=2^(-r0-1); union-bound geometric tail gives guarantee.
Take rank-r0 H with ker(H)=span(periods). For EVERY fixed original x and every B, E(x,B)=E(x,B_h) whenever HB=h=HB_h. Therefore
forall B not E(x,B) iff AND_{h in GF(2)^r0} not E(x,B_h).
All positive certificates are sound, irrespective of probability. If random search fails, report failure or use exact identity projection H=I_b; never claim unsound compression.

The difference miter's two *functional* Tseitin copies share X,B (second B shifted by constant v), with a disagreement output clause. Each 3CNF has O(N) clauses and O(N log N) indexed serialization bits. Each SAT/UNSAT decision is charged.

## SELECTOR / AFFINE INTEGRATION
For source-certified G_i=R_i(X) AND [A_B,i B xor A_V,i V=f_i(X)] AND E_i(X,B), discover H_i by the above sampler for E_i. With L_i a left-nullspace basis of A_V,i, M_i=L_i A_B,i and K_i a kernel basis of M_i, prior selector-observable theorem applies with delta_i=rank(H_i K_i)<=r0_i, yielding sum_i 2^delta_i projected observations plus sum_i q_i fully charged SAT queries. The SAME X is used in every branch. Real universal challenge is |I|+|B|+|V|, not the O(log N) selector index alone. Original Y-dependent traces remain after forall Y; only the new X-only circuit's trace is existential.

## COUNTEREXAMPLES
Syntactic boundary support b may hide observable rank 1 (full parity) or rank 2 (nonlinear AND of two dense parities). With unknown v* nonzero, f(B)=1 iff B in {0,v*} has period space {0,v*}; detecting its period requires Omega(2^b) queries in a restricted period-membership-only oracle model, NOT a lower bound for arbitrary source-reading SAT algorithms. SAT(F(X)) remains when E(X,B)=not F(X), even with rank zero.

## EXECUTED TESTS, EXACT SIZES
Primary standard-library verifier: 35 arbitrary small source circuits, 115 hidden-affine-observation nonlinear circuits, 396 small difference-miter CNFs independently solved by DPLL, 354 candidate fibers, 896 period membership checks against exhaustive truth tables, 19,136 semantic identities, 30 safe-fallback controls. Independent truth-table verifier: all 65,808 pairs of Boolean functions at b=1,2,3; 131,616 candidate-fiber checks, 1,037,352 quotient-coset checks. Zero discrepancies.
Dense b=20, n=1 source: E(x,B)=(not x) AND parity_1(B) AND parity_2(B), 40 gates. 1,048,576 universal challenges; rank 2, four projected observations; 59 random draws, 57 exact GF(2) period checks, 18 independent periods. Dense membership uses symbolic algebraic identity, NOT real SAT calls; a genuine miter was generated. Source JSON 1586 bytes; miter 121 variables, 354 clauses, 4330 DIMACS bytes. Materialized X-only winning 3CNF 166 variables, 636 clauses, 7657 DIMACS bytes; pinned-input DPLL verifies x=1 wins, x=0 loses.

## CONDITIONAL P=NP COST
If deterministic SAT T_A(L)=O(L^d), d>=1, and b<=N, full conservative time is
O(q[(N log N)^d+b^2]+[N*2^r0*log(N*2^r0)]^d).
No general f(d)<d. On rank-unpromised sources the fallback may be exponential. No new lower bound for arbitrary SAT decision machines.

## HANDOFF
Authenticate the nonlinear/affine source decomposition; establish a hereditary low-rank bound including index-based addressing and reconvergent gates; compare adaptive SAT period queries with membership-only oracle; preserve common-X and original gate trace quantifiers; charge every source scan, memory, UNSAT decision and final SAT call.

PERIODBASIS22_SENTINEL_20261118