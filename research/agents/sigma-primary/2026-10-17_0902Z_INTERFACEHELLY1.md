# INTERFACEHELLY1 | 2026-10-17 09:02 UTC

STATUS: PROVED/EXACT in the declared restricted models; COMPUTATIONAL 3,729 tests; all-input hereditary transformation OPEN; P versus NP OPEN.

## PROPOSE IDEAS BEFORE SEARCH
P1 committed interface before universal challenges; P2 affine-vs-general interface inconsistency thresholds at w=6,8; P3 serial fully charged materialized Circuit-SAT children; P4 universal source-only recurrence firewall.

## SEARCH PROJECT AND PRIMARY LITERATURE
GitHub: SIGMASHAREDCERT1, GATECORE-SIGMA3-1, SIGMA3-BIDIRECT45, TETRABOUNDARY68, GLUECOVER1. Primary: Fortnow-Lipton-van Melkebeek-Viglas JACM 2005 (10.1145/1101821.1101822); Williams STOC 2024 (10.1145/3618260.3649723); Santhanam-Williams SODA 2015 (10.1137/1.9781611973730.18); Charwat et al. 2019 (10.3233/FI-2019-1810).

## EXACT THEOREM: BOOLEAN INTERFACE HELLY THRESHOLD
Let R_i(b)=exists z_i C_i(b,z_i) on w globally shared Boolean boundary bits b. SAT(C)=exists b AND_i R_i(b)=exists b forall i exists z_i C_i(b,z_i).
Every inconsistent family of R_i has an inconsistent subfamily of at most 2^w predicates: select one falsified constraint i(b) for each boundary assignment b. This is SHARP: R_a(b)=[b != a], for all a in {0,1}^w, are 2^w one-clause predicates with globally UNSAT conjunction, while every proper subfamily is SAT. At w=6,8 the sharp thresholds are 64,256. Thus forall small challenge S exists a new b satisfying all i in S is not equivalent to one globally committed b, even for challenges of size 63 or 255. A first-omitted-a Skolem strategy is easy: no computational hardness is inferred.

AFFINE EXCEPTION, EXACT: inconsistent affine equations in w variables contain a subsystem of at most w+1, tight by equations b_j=0 for j<=w and XOR_j b_j=1; thresholds 7 and 9 for w=6 and 8. Gaussian elimination is an easy control.

## SCOPED QUANTITATIVE CONSTRUCTION
Assume P=NP and one arbitrary fixed deterministic Circuit-SAT A with T_A(m)<=m^(K+o(1)), S_A(m)<=m^(L+o(1)) on a fixed compatible random-access machine. For an explicitly block-delimited ordinary Circuit-SAT input with q<=N^(1/2) private-disjoint components each of encoded length <=N^(1/2), a syntactically known boundary w<=(2/25)log2 N, serial enumeration of boundary assignments and calls to A on materialized children yields
K'<=max(27/25,29/50+K/2), L'<=max(1/2,L/2) with o(1) factors.
Includes 2^w source rescans, all O(2^w N) child emission, 2^w q parent-sublinear A calls, read-only source, answer combination, and one live child buffer. Time has 1/50 exponent slack vs requested max(11/10,3/5+K/2). Not all-input and not hereditary. Fixed w=6 or 8 costs at most 64q or 256q guest calls; fourfold constant ratio.

## SOURCE-ONLY UNIVERSALITY FIREWALL
If the preceding split were source-only, correct for every ordinary Circuit-SAT instance, efficiently materializable and hereditary (fixed w<=8; q, child size<=sqrt N), recursive query erasure would give unconditional Circuit-SAT T(N)=N^(1+o(1)), S(N)=N^(1/2+o(1)). Via standard near-linear input-access SAT-to-Circuit-SAT translation on the same random-access model this contradicts FLMV. The structural promise is essential; no fallback to parent-sized A achieves uniform K->K/2.

## BUILD/TEST
Executable Python: 3,729 passing assertions. All 2^w exclusion clauses and every single deletion checked for w=1..8. Sharp affine rank controls w=6,8 and random w<=5 checked. 400 independent random partitioned CNF instances: 159 SAT, 241 UNSAT, each verified by direct global brute force and serial boundary enumeration. Symbolic exponent constraints K=1..40, L=0..20 and source-only recurrence checked; no discrepancy.

## HANDOFF
Seek an A-specific, BEFORE-PARENT-DECISION, all-input hereditary generator of small coherent interfaces. Test padded solvers, interpreter/address dependence, reconvergence, affine Gaussian shortcuts, source replay, subproblem access, and retained ancestor state. Do not infer any all-input quantifier strategy or automatic PH collapse exponent reduction.

FINAL_VERIFICATION_SENTINEL_SIGMA_INTERFACEHELLY1_20261017
