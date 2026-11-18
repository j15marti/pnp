# CLOCKMONOCHAIN26 | Unate-chain and Reed-Muller mixed-fiber obstruction

**Date:** 2026-11-17 America/Los_Angeles. **Owner:** CLOCK-INDEPENDENT-GATE1, separate from the five TMR manuscript owners. **Status:** PROVED/EXACT for the declared semantic class, independent mathematical review OPEN. Finite evidence COMPUTATIONAL. **P versus NP OPEN.**

## Dependency and falsifiers

Target chain: authentic N=2^n MCSP truth table -> source-authentic lossy quotient H -> short YES-image circuit witnesses and universal NO exclusion -> uniformly fixed-PH equality verifier -> near-linear headerless one-way-input/one-work-tape compilation -> model-matched CHMY lower-bound consequence. This run attacks the exact **universal NO-exclusion premise**, not the full transfer.

Four falsifiable candidates: (A) unate high-total-ANF-degree output (OR, AND, majority) might evade CLOCKRMFIBER25; (B) antitone/signed output provenance might force hard fibers; (C) parity or low-degree polynomial guards might eliminate a monotone fiber; (D) removing unateness should break the proposed chain argument. (A)-(C) fail under the theorem below; (D) is an essential model boundary. No mathematical novelty/priority is claimed for classical monotone-chain, counting, or Reed-Muller ingredients.

## Theorem: UNATE-CHAIN-RM-MASS26

Let f in {0,1}^N be an actual N=2^n-bit source truth table. Let H(f)=(A_1(f),...,A_k(f),P_1(f),...,P_r(f)) be a deterministic vector-valued quotient. Each A_i is either **globally coordinatewise nondecreasing** or **globally coordinatewise nonincreasing** on the raw source Boolean lattice, with a fixed sign per whole output. This is narrower than general input-wise unateness with mixed signs. Each P_j is an arbitrary global multilinear polynomial in the full original N source-bit variables over GF(2), degree d_j. The source dependence of selectors, provenance, and seeds must be included in these *complete* output functions, not treated as external free inputs.

Write D=sum_j d_j and L0=ceil((N+1)/(k+1))-1. For every such H, some prefix truth table p_a[i]=1 iff i<a, with n-input circuit size O(n), satisfies

    |H^{-1}(H(p_a))| >= 2^{max(0,L0-D)}.

There is moreover an interval [p_a,p_b] in the source Boolean lattice of free dimension L=b-a>=L0 on which all k unate coordinates are simultaneously constant; within that interval at least 2^{max(0,L-D)} sources match the complete H output of p_a.

**Proof.** The standard increasing prefix chain p_0<=p_1<=...<=p_N has N+1 vertices. Each globally increasing A_i flips at most once (0 to 1), and each globally decreasing A_i flips at most once (1 to 0); therefore the entire k-bit A-vector changes at most k times on the chain. It has at most k+1 constant runs, one of length at least ceil((N+1)/(k+1)) vertices. Choose endpoints p_a,p_b of the longest run, with L=b-a>=L0. For any source z between the endpoints, the monotone value of each A_i is squeezed between its *equal* endpoint values, and so is constant on the **entire** L-dimensional subcube, not only on the chain.

Restrict P_j to the L free raw source-bit coordinates of that cube. Restriction cannot increase ANF degree. Set v_j=P_j(p_a), and let Q(z)=product_j(1+P_j|cube(z)+v_j), with multiplication over GF(2). Then Q is the indicator of all sources in the cube matching the polynomial outputs. Q is nonzero, because p_a is such a source, and has degree at most min(L,D). By the binary Reed-Muller minimum-weight theorem, every nonzero multilinear degree-e function on L Boolean variables is nonzero on at least 2^{L-e} assignments. Hence Q has support at least 2^{max(0,L-D)}, proving the claim. The Reed-Muller fact also follows by induction from Q=x_i R+S, where R is nonzero degree e-1, using the pairs of evaluations where R=1.

## Exact MCSP NO-image collision

Let Y_s={f:CC(f)<=s}, where CC is ordinary nonuniform n-input fan-in-two Boolean circuit size for a fixed complete basis with b gate types. The standard circuit encoding bound is

    |Y_s| <= U(n,s)=(s+1)(n+s+2)[b(n+s+2)^2]^s.

Each prefix p_a has a comparison-to-a-hardwired-threshold circuit of size <=c0(n+1), for one basis-dependent absolute constant c0. Thus for s>=c0(n+1), if

    L0-D > log2(U(n,s)),

the fiber of the YES source p_a has strictly more members than all size-s source functions combined. Some original source f_NO with CC(f_NO)>s must satisfy H(f_NO)=H(p_a). EXACT source MCSP YES/NO promise purity is impossible; in particular CLOCKASYMTRANSFER24's universal NO exclusion fails if its short witness budget w includes p_a.

Equivalently, exact purity requires

    D >= ceil((N+1)/(k+1))-1-log2(U(n,s)).

For source threshold s=N^beta (0<beta<1) and a cofinal family with k_j<=N^{a lambda^j+o(1)}, D_j<=N^{delta+o(1)}, delta<1, any **fixed clock-independent stage** j satisfying a lambda^j<1-max(beta,delta) violates purity at large N. This does not assume that one can efficiently *find* the hard f_NO. It is a semantic collision theorem.

## Hostile controls and scope

OR_N and AND_N both have full-source ANF degree N, making CLOCKRMFIBER25's low-total-degree test vacuous, yet each is globally monotone and is excluded by this theorem. Strict majority, thresholds and a fixed antitone feature are covered regardless of their global degree. Global parity is not monotone, but enters as a degree-one P_j. A quadratic check contributes degree two. Changing the sign or provenance selector *based on the source* requires rechecking actual full-source unateness; signed gates are not automatically covered. Unrestricted non-unate high-degree output functions are OPEN. A hypothetical decision-oracle quotient encoding source MCSP directly is exactly pure but not demonstrated to have a cheap uniform compiler or fixed-PH equality verifier.

The theorem does not show all high-degree maps have easy fibers. It only says the specified mixed unate/polynomial families necessarily have at least one YES/NO mixed fiber under the displayed quantitative condition. It does not by itself implement a source-authentic compiler, a uniform inverse, a PH verifier, or a CHMY one-tape transfer.

## Reproducibility and resource ledger

Full executed local Python: 2026-11-17_clock_monotonehybrid26_audit.py, Python 3.13.5, deterministic seed 202611171927, local SHA256 213b1b1901e513b320793b2af6d057daec13bdfddda79cc608ee7d3b9c9d80d7. Full local raw JSON SHA256 f4ed9b93e5e1662c7a725b40a393be95ba19af82fc850265f9159373ec2106a8. 452,711 assertions, **zero failures**. Enumerated all 168 monotone functions of four raw source bits, all 28,224 ordered pairs with two different polynomial-output regimes, 1,200 seeded N=8 mixed systems and 24 full-source OR/AND/threshold/majority cases. Inspected 221,376 cube points and counted 171,076 polynomial-consistent points across 57,672 systems; exact lower bound attained in 26,371. Four finite low-circuit mixed-fiber controls and a parity-chain failure control. Finite two-gate library is a proxy only, not a lower bound for unrestricted MCSP.

The project checkout was unavailable; startup state was recovered from connected GitHub reads of current AGENTS, CODEX, 2026-11-15 end-to-end directive and pnp-research skill; relevant original CLOCKASYMTRANSFER24 / CLOCKRMFIBER25 / source-query and public-seed reports, issue #3 and literature. The complete 452,711-check executable/raw and expanded proof remain in the local research bundle; the reported counts refer to that **actually executed local program**, not to unexecuted remote source.

**SAME_REALIZATION:** The no-go statement requires no source acquisition or computation and does not provide an implementation. Any successful positive quotient still needs authentic full-N input, source-dependent seed/provenance accounting, output serialization, unary witness padding, ALL alternative circuits, one joint fixed-PH verifier, and same-one-tape physical fusion. OR/AND examples stream in O(N) time and O(1) state but are provably not promise pure. No hidden external source tape, oracle, or free proof step is permitted.

**Gates:** DISJ NOT APPLICABLE (no rank-to-circuit inference); relativization OPEN for unrestricted separation; simultaneous DTISP FAIL for the covered class because promise purity fails, OPEN for other constructions; deterministic configuration counting NOT APPLICABLE as a time lower bound (the nonuniform circuit count is a separate combinatorial bound). Natural Proofs/algebrization not bypassed. Prior short-hash, Chevalley-Warning, 2SAT/Horn, partial-MCSP, source-as-seed, k-gram, automatic-section, witness-PH and machine-model controls remain active. P versus NP OPEN.

**ONE NEXT:** NONUNATE-HIGHDEGREE-PURITY27, an authentic order-sensitive, non-unate, high-degree quotient that defeats both this mixed-fiber criterion and CLOCKRMFIBER25, with proven asymmetric YES witnesses, universal NO exclusion, one jointly fixed-PH succinct equality predicate and charged headerless near-linear one-tape compilation. Do not infer P=PSPACE from P=NP or select c>K(c) circularly.

**Sources:** [1] C. Shannon, *The Synthesis of Two-Terminal Switching Circuits*, BSTJ 1949 (circuit counting); [2] I. Reed and D. Muller (1954), binary Reed-Muller minimum distance (proof included above); [3] D. Duffus, B. Sands, P. Winkler, *Maximal Chains and Antichains in Boolean Lattices*, SIAM J. Discrete Math. 1990, DOI 10.1137/0403017 (background only); [4] Cheraghchi, Hirahara, Myrisiotis, Yoshida, *One-Tape Turing Machine and Branching Program Lower Bounds for MCSP*, STACS 2021, DOI 10.4230/LIPIcs.STACS.2021.23 (model-specific lower bound, NOT used to prove this fiber theorem).

END_CLOCKMONOCHAIN26::P_VS_NP_OPEN
