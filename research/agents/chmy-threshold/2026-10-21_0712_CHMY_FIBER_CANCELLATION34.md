# CHMY Threshold Bridge 34 — Fiber cancellation and seed/locality feasibility

Research date: 2026-10-21 07:12 Asia/Seoul. Retried publication 2026-10-21. Status: PROVED restricted counterexamples, FAIL direct lifting, OPEN general transfer. P versus NP remains OPEN.

## Proposals registered before literature review

(A) Strengthen the source GapMCSP YES promise to create margin for circuit-complexity-preserving truth-table expansion.
(B) Lift the genuine uniformly seeded Forbes–Kelley/CHMY generator through the Bridge33 encoder, assessing pseudorandomness against uniform *target-length* strings.
(C) Keep one shared global circuit witness across two MMW Stream-Merge updates while replacing search by short ordinary PH queries.
(D) Test whether the published CHMY branching-program lower bounds can be transported to OPS's required nonuniform circuit class.

This run resolved (A) and (B) negatively in precise restricted models. (C) and (D) remain open.

## Primary-source contracts

CHMY, STACS 2021, Theorem 16: for 1/2 < mu' < mu < 1, randomized one-way-read-only-input, ONE read/write work-tape oracle Turing machines, two-sided error at most 1/3 and N^o(1) oracle queries do not decide MCSP[N^mu] in time N^(2(mu'-o(1))). Corollary 23 gives a uniformly seeded local generator with sigma = ~O((sqrt(T)+log(1/epsilon))*log(q*2^ell*T)). Its security is against uniform N-bit truth tables, not arbitrary larger target distributions. The genuine CHMY generator was not numerically instantiated; results below apply to every possible generator output.

OPS, Theory of Computing 2021, Theorem 1.4: a nonuniform circuit lower bound for logarithmic-gap GapMCSP at every sufficiently small positive beta is required. CHMY does not establish this premise.

MMW, STOC 2019, Theorem 4.2: ordinary MKTP[p], p >= log N, has an O(Np)-time, O(p)-space oracle-streaming algorithm with ordinary Sigma_3 SAT queries of O(p) bits. It does not provide the desired SAT-to-MKTP reduction.

## Theorem 34A: public-fiber parity cancellation (PROVED within its interface)

For M>N, let E(f)_i = f_{pi(i)} XOR h(i), where pi:[M]->[N] and h:[M]->{0,1} are public source-independent functions. Pigeonhole guarantees distinct a,b among the first N+1 output positions with pi(a)=pi(b). Therefore E(f)_a XOR E(f)_b = h(a) XOR h(b) for every source truth table f.

A one-way finite-state tester stores the bit at a, reads to b and checks that relation. It has zero work-tape cells, zero randomness and zero oracle calls. It accepts E(f) with probability 1 and an independent uniform M-bit truth table with probability 1/2. For length-specific public pi,h, O(N) finite-control states suffice. Thus lifting the genuine CHMY G_N through E cannot yield a PRG against uniform M-bit targets for epsilon<1/2. The correct original CHMY comparison is G_N(U_sigma) versus U_N; pushforward only yields E(G_N(U_sigma)) versus E(U_N) with a charged simulator.

For the particular Bridge33 encoder E(f)(x,y) = f(x) XOR [y_0 AND (x_0 XOR y_1)], x-major and y-minor serialization, n>=3, the first eight output bits form four equal adjacent pairs. A constant-state, zero-work-tape one-way tester checks these four equalities in eight reads: acceptance is 1 on every E(f), 1/16 on U_M, advantage 15/16. Restriction y=0 recovers f and CC(f) <= CC(E(f)) <= CC(f)+9, but circuit-size preservation does not imply E(U_N)=U_M; indeed TV(E(U_N),U_M)=1-2^(N-M) when E is injective.

Public masks or public permutations cannot remove all repeated-source-bit relations; they may only move the first witness, which still occurs among the first N+1 positions.

## Theorem 34B: full-stream exponent wedge (PROVED restricted)

Write source CHMY time T=N^(2nu+o(1)), where 1/2<nu<theta<1, and source LOW GapMCSP cutoff N^theta/(c log N). A circuit-complexity-preserving expansion M=N^r with target threshold exponent beta' can preserve all promised source LOW functions only when asymptotically r*beta' >= theta (boundary logarithmic constants require source-promise strengthening). To force beta'<1/2 requires r>2theta. Generating or online reading all M target bits within source CHMY time N^(2nu) requires r<2nu. Since nu<theta, these inequalities are incompatible.

More generally, if the published CHMY generator is certified with source time exponent h, seed upper-bound exponent h/2+delta, target time exponent h'>=1, and a fully charged simulation requires r*h'<h while the PRG's output circuit is certified below M^beta' via h/2+delta<r*beta', then h'<2beta'-2delta/r<=2beta'. Thus the *published seed-bound certificate* alone cannot certify superlinear target hardness at beta'<=1/2 within these assumptions. This is NOT an impossibility for unrelated reductions or a stronger generator.

For simple length padding, lambda=1/r, h=1+g, and rho=(h-r)/(r(h-1)) yields rho-lambda=(1-r)/(r(h-1))<0, failing rho>lambda.

## Finite audit and machine accounting

Independent deterministic standard-library audit exhaustively checked all 256 N=8 input truth tables and all 16,384 bits in the corresponding M=64 targets; 8,192 adjacent-pair equalities; four public mask functions; four source-index maps with repeated-coordinate witnesses; 6,840 rational-grid parameter triples with no valid r satisfying both full-stream conditions; and a concrete circuit for nonconstant source x_0 XOR x_1 with nine added Boolean gates. All asserted checks passed in the original recorded run.

Standalone E(f) uses exactly N source-bit reads, M=N^2 output writes, Theta(M) generation time and O(log M) auxiliary counter bits. The PRG distinguisher uses zero work cells. A fully fused generator+one-work-tape target decider has NOT been verified with this same time bound; naive parked-counter simulation incurs work-head travel. No seed-dependent advice, cryptographic hardness, or surrogate generator is assumed.

## Next falsifier

Study a source-accessible mixing code E(f)_i = XOR_{j in S_i} f_j XOR h(i) with provably high dual distance. First try to produce an early low-weight parity relation; otherwise audit source buffering, repeated reads, full target output, work-tape fusion, CHMY original hidden-seed distribution, and both GapMCSP classifications. No cofinal threshold/hardness-margin improvement has been established.

## Sources

1. Cheraghchi, Hirahara, Myrisiotis, Yoshida. One-Tape Turing Machine and Branching Program Lower Bounds for MCSP. STACS 2021. https://doi.org/10.4230/LIPIcs.STACS.2021.23
2. Oliveira, Pich, Santhanam. Hardness Magnification Near State-of-the-Art Lower Bounds. Theory of Computing 2021. https://theoryofcomputing.org/articles/v017a011/
3. McKay, Murray, Williams. Weak Lower Bounds on Resource-Bounded Compression Imply Strong Separations of Complexity Classes. STOC 2019. https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf

END VERIFIED SCIENTIFIC REPORT BODY.