# SIGMA3-BDDWITNESS57: Authenticated witnessed affine fibers
Date: 2026-11-18 07:30 Asia/Seoul. Status: PROVED/EXACT restricted MT-OBDD and affine-fiber QBF theorems (independent review pending); COMPUTATIONAL finite tests; all-input P versus NP OPEN.

## PROPOSE / SEARCH
Four prespecified candidates: (1) compute exact nonlinear guard-fiber affine hulls without parent SAT queries from source-authenticated multi-terminal ordered BDDs; (2) retain ACTUAL accepted challenge witnesses during Gaussian elimination; (3) test authentication of arbitrary source circuits against candidate BDDs; (4) test universal ordering blowup and hereditary sublinear SAT children. Reviewed FIBER56, SELECTOR_OBSERVABLE21, TMR-4 OBDD-rank transfer code, and project AGENTS.md. Primary literature: Bryant 1986 DOI 10.1109/TC.1986.1676819; Henshall, Schachte, Søndergaard, Whiting, 2009 CATS Boolean Affine Approximation with Binary Decision Diagrams (PRIOR ART for BDD affine envelopes); Balabanov et al. 2015 AAAI DOI 10.1609/aaai.v29i1.9750; Fortnow et al. 2005 JACM DOI 10.1145/1101821.1101822. No general-novel BDD affine hull claim.

## BDD57-A: witness-preserving affine-hull compiler, PROVED/EXACT
Authoritative layered MT-OBDD g:{0,1}^n->{0,1}^k with s decision nodes, a reachable terminal labels. For each nonempty fiber Y_t, construct p_t and q_{t,1},...,q_{t,r}, ALL actual elements of Y_t, with independent differences q_i XOR p spanning aff(Y_t)-p. Bottom-up each node merges lifted child witness POINTS, then greedy Gaussian rank selection keeps only genuine points. Each node/label needs <=2(n+1) candidates. Time O(a*s*n^3) bit ops; peak workspace O(s*n^2) bits with per-label streaming, ignoring read-only authenticated input. Polynomial in the supplied BDD size, not arbitrary equivalent circuit size.

## IMPORTANT CORRECTION TO FIBER56 NEGATIVE STRATEGY
A row-reduced direction is not necessarily the XOR of the anchor with an accepted fiber member. Y={000,110,101}, p=000, original differences 110 and 101. Gaussian elimination can generate 011; virtual point 011 is NOT in Y. Thus issuing y=p XOR 011 as a Herbrand counterchallenge is INVALID. The decision theorem uses affine span and remains correct. For a genuine negative-response witness, retain actual q_i, or charge a fresh witness search. This compiler retains actual representatives.

## BDD57-B: EXACT three-block QBF with both strategies
Phi = exists x forall y exists z [ A z = B_{g(y)} x + C_{g(y)} y + d_{g(y)} ] over GF(2). L spans the left nullspace of A. TRUE iff ONE common x solves L(B_t x+C_t p_t+d_t)=0 for every nonempty fiber t and LC_t(q_{t,i} XOR p_t)=0 for every frame direction. Equivalently, for EACH fixed x, all-universal correctness equals correctness on the at most a(n+1) ACTUAL representatives. YES: compute x then Gaussian z(y) adaptively after each y. NO: for each supplied x, scan genuine representatives and supply losing y plus dual u with u^TA=0, u^T RHS=1. No free negative witness. Appended fully constrained deterministic gate traces remain unique, but extra nonlinear acceptance gates can invalidate the affine criterion.

## BDD57-C/D: scoped barriers, PROVED/EXACT
Given arbitrary circuit F and candidate BDD D, checking F(y)==D(y) for all y is coNP-complete even D=constant-zero, by reduction from UNSAT(F). Therefore an untrusted BDD guess is not a free certificate. Fixed order EQ_n(x,y), x-block before y-block, requires OBDD width >=2^n at the cut even though equality has linear circuits and an O(n)-size OBDD with interleaved variables. Neither is a general computational lower bound.

## SAME-MACHINE COST AND SAT EXPONENTS
Complete explicitly encoded input length N. Conservative deterministic compiler: O(N^5) bit operations and O(N^3) writable bits by streaming frames and incremental Gaussian elimination, with genuine YES/NO responses charged. For a separate restricted residual-SAT extension with N^beta global tags, N^kappa reachable labels, N^theta residuals per label and SAT children of encoded length N^lambda, fixed hypothetical SAT decider T(M)=M^(K+o(1)), S(M)=M^(L+o(1)):
K' <= max(5,rho,beta+kappa+theta+lambda*K)+o(1);
L' <= max(3,lambda*max(1,L))+o(1);
rho accounts for source rereads. lambda=1/2 yields guest coefficient K/2 but compiler costs 5 and 3 dominate, not a DTISP contradiction. Source authentication, arbitrary circuit translation, hereditary child eligibility, and simultaneous low space OPEN. General P versus NP OPEN. No inferred lower bound from exponential challenge counts, large OBDD size under a fixed order, or gate-trace uniqueness.

## BUILD / ADVERSARIAL
Python standard library auditor seed 20261118072457. 243085 checked assertions, 0 discrepancies; 1050 random DAG-sharing MT-OBDD QBFs plus 10 structured QBFs; 2161 nonempty fiber frames and 8280 fixed-x equivalence comparisons; independent exhaustive z evaluation against compiled Gaussian QBF; 13760 adaptive Skolem responses; 5528 certified true Herbrand counterchallenges; 250 SAT-dependent circuit-vs-zero-BDD guards (158 SAT/92 UNSAT); nonlinear AND and parity guards, compact z=y, eight unique/omitted gate-trace controls, wrong-prefix trap, 280 K_nn parity flows, 96 signed integer flows, 2^n equality residuals for n=1..7. Finite checks do not establish asymptotic statements.

Reproducibility: script SHA256 5c477d820c35bb00f096e3655757ce85b12a9ee9049754cd401039dad72ab660 ; raw JSON SHA256 9d53a582660c19e31d8ec7c7154a323e4473da736d628b422c9ee94d855e22ff ; full local bundle SIGMA3_BDDWITNESS57_20261118_research_bundle.zip contains Markdown formal report, LaTeX, BibTeX, complete auditor, JSON results and checksum manifest.

## NEXT
Try a single explicit width-w authoritative MT-OBDD guard combined with unrestricted Circuit-SAT residual leaf. Apply actual SAT witness self-reduction and recompile the child. Verify the child size/order, full two-sided continuation semantics, access and acquisition cost, live-memory accounting, and hereditary source closure. Falsify by replacing the trusted guard with compact arbitrary circuit whose certified OBDD expands exponentially. No edits to TMR-owned manuscripts. P versus NP remains OPEN.

SIGMA3_BDDWITNESS57_VERIFIED_HANDOFF_20261118_0730KST