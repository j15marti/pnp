# MULTISAT-LAYER1 | 2026-10-18 12:48 Asia/Seoul

STATUS: PROVED/EXACT elementary monotone composition and restriction-inheritance theorems (independent review pending); COMPUTATIONAL finite controls; OPEN unrestricted lower-bound transport; P vs NP OPEN.

## IDEAS PROPOSED BEFORE LITERATURE

A. Feed independent 3-CNF SAT decision bits into an outer Circuit-SAT witness verifier.
B. Instantiate both layers using clique, which has published monotone circuit lower bounds.
C. Seek an actual composition/direct-product lower bound, not an assumed multiplication of unrelated bounds.
D. Audit monotone versus nonmonotone outer gates and model-matched MCSP transport.

## LITERATURE CHECK AND REVISIONS

Cavalar, Kumar and Rossman, *Monotone Circuit Lower Bounds from Robust Sunflowers* (Algorithmica 2022), prove strong bounds for monotone clique circuits in a stated parameter range. Alon and Boppana (Combinatorica 1987) prove other exponential monotone clique bounds. KRW composition theorems via lifting concern depth and specified inner gadgets, not a free product of arbitrary monotone *size* bounds. Cheraghchi et al. (STACS 2021) prove one-tape MCSP bounds, which cannot be used as generic Circuit-SAT lower bounds.

## CONSTRUCTION AND PROVED THEOREMS

Let b_i = SAT(F_i), where independent 3-CNFs F_i have disjoint witness variables x_i. Let C(z,b) be a polynomial-size outer Boolean verifier and R(b) = exists z C(z,b). Define H(x,z) = C(z,F_1(x_1),...,F_k(x_k)), where F_i(x_i) is Boolean formula evaluation, not an oracle call.

**MONOTONE-SAT-COMPOSE1.** For every family F_i, SAT(H)=R(b) whenever R is monotone increasing. Conversely, if this equality is valid for all 3-CNF families, then R must be monotone. Proof: inner evaluations u obey u<=b. If H accepts then R(u)=1, and monotonicity yields R(b)=1. Conversely, choose a satisfying local assignment for every b_i=1, and any assignment for b_i=0. Necessity: use the eight distinct proper 3-clauses on three variables, which form an UNSAT cube, and the seven-clause cube obtained by deleting one clause, which is SAT but has falsifying assignments. They realize every u<=b. Thus existential composition yields OR_{u<=b} R(u), equal to R(b) for every b precisely when R is monotone.

**CLIQUE-OF-3SAT1.** For every outer graph edge e, an inner 3-CNF F_e(y_e,x_e) verifies the existence of an s-clique in an input graph y_e with m vertices. The outer circuit existentially verifies a t-clique on r vertices in the graph with edge bits SAT(F_e(y_e,*)); because the outer predicate is monotone, one polynomial-size ordinary Circuit-SAT instance H_y has SAT(H_y) iff CLIQUE_{r,t}((CLIQUE_{m,s}(y_e))_e). All y_e are fixed input bits when H_y is built, not existentially guessed graph bits.

**MONO-RESTRICTION-MAX1.** If R and P_i are nonconstant monotone functions on disjoint input blocks and every input of R is essential, then for G=R(P_1,...,P_k),

mSIZE(G) >= max(mSIZE(R), max_i mSIZE(P_i)).

Proof: each nonconstant monotone P_i has a one-variable restriction equal to identity, yielding R after simultaneously restricting the blocks. For each i, choose constants at other positions making the monotone essential outer R equal input i; fix the other P_j to those constants, yielding P_i. Restriction never increases monotone circuit size. Applied to clique-of-cliques, this gives two separate published superpolynomial sources of restricted-model hardness, but NOT their product.

**MULTI-WITNESS-COVER1.** For k disjoint black-box witness-validity arrays of lengths W_i, suppose an L-bit output representation makes at most q adaptive oracle queries per output bit along the all-zero transcript and must distinguish all zeros from a singleton witness at any address. Then L*q >= sum_i W_i, by counting the union of queried addresses. In particular, an outer OR does not by itself overcome the CLOCKSAT1 black-box witness-coverage barrier. Source-syntax shortcuts remain outside this statement.

## FINITE TESTS

Source: experiments/meta/2026-10-18_multisat_circuit_compose1.py.
Raw: results/raw/meta/2026-10-18_MULTISAT_CIRCUIT_COMPOSE1.json.

Exhaustive k=2 outer Boolean functions: 16 tested, exactly 6 compose correctly, precisely the 6 monotone ones. k=3: 256 tested, exactly 20 compose correctly, precisely the 20 monotone ones. Nonmonotone failures: 10 and 236. Verified the UNSAT eight-clause cube and SAT seven-clause cube; four-clause 3-CNF identity gadgets; every graph on four vertices (64 cases) with an outer three-clique verifier; and 140 bit-sensitivity controls for AND of independent parity blocks. No discrepancies. These are finite semantic controls, not general-machine lower bounds.

## PROOF DAG AND RESEARCH DECISION

ESTABLISHED: proper CNF witness gates, exact monotone SAT composition, monotone circuit clique bounds at their published parameters, and restriction-max inheritance.

CONDITIONAL: cofinal MCSP slope g(beta)/beta -> infinity implies separation given same-model lower bounds and one uniform collapse exponent.

OPEN: a product-like SAT composition lower bound strictly stronger than the max restriction bound, a valid transfer to unrestricted solver cost or one-tape MCSP, and any implication P!=NP.

RETIRED: charging for individually recognizable fixed UNSAT Tseitin source instances as if their decision bits were hard; treating existentially selectable zero evaluations as UNSAT certificates; multiplying arbitrary proof-system, monotone, and one-tape lower bounds.

Allocation: keep THRESHOLD-DESCENT1 as highest-priority MCSP route and CLOCK-INDEPENDENT-GATE1 as independent meta-complexity route. Use this nested 3-SAT/Circuit-SAT construction as a parallel model-matched composition test bed.

HIGHEST-VALUE NEXT LEMMA: SYNCHRONIZED-SAT-DIRECTPRODUCT1. Prove a genuinely stronger-than-max lower bound for an explicit outer witness predicate composed with variable YES/NO inner 3CNF families, in one declared computational model, including all input translation and oracle/access costs. Only after that seek a source-matched compiler to the MCSP magnification endpoint.

References: Cavalar-Kumar-Rossman (Algorithmica 2022), Alon-Boppana (Combinatorica 1987), de Rezende et al. (KRW Composition Theorems via Lifting, FOCS 2020), Cheraghchi-Hirahara-Myrisiotis-Yoshida (STACS 2021).

FINAL_VERIFICATION_SENTINEL::MAIN::MULTISAT-LAYER1::2026-10-18_1248::P_VS_NP_OPEN
