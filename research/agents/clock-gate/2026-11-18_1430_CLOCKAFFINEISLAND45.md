# CLOCKAFFINEISLAND45 | 2026-11-18 14:30 PST

**PROVED/EXACT restricted affine-source-island theorem; independent mathematical review OPEN; COMPUTATIONAL finite controls; P versus NP remains OPEN.**

## Pipeline and four falsifiable mechanisms

The authentic source is an N=2^n-bit truth table read once in address order. The target is a stage-uniform short-output quotient H with joint fixed-PH supplied-circuit equality and a charged one-way-input, one-work-tape implementation. The missing end-to-end arrow is exact H(YES_s) versus H(NO_t) separation for YES_s={f:CC(f)<=s} and NO_t={f:CC(f)>t}. This run FALSIFIES universal NO-image exclusion for an unusually strong candidate.

Pre-literature mechanisms: M1 restrict all output coordinates to a large original-source affine island, not the whole source cube, looking for low ANF degree; M2 add n authentic online-indexed provenance bits; M3 add globally degree-N, order-sensitive nonlinear output bits and establish fixed-PH verification; M4 leak ALL even source bits as a hostile control to force the restriction degree to rise. Each falsifier is checked explicitly.

## Theorem 45A: AFFINE-ISLAND RESTRICTED-DEGREE/MASS SECTION

For n>=2 let N=2^n, B=N/2, and injectively embed E:{0,1}^B into authentic N-bit truth tables by E(z)_(2j)=z_j and E(z)_(2j+1)=1-z_j. Let H:{0,1}^N->{0,1}^m be ANY total map. For every actual output bit, including every seed/provenance/decoder bit, define P_i(z)=H_i(E(z)) and total restricted degree D=sum_i deg_GF2(P_i).

For every label v attained on the island: (1) an original authentic source E(z) gives H(E(z))=v and has CC(E(z))<=C(n+1)(D+1); (2) the fiber contains at least 2^max(0,B-D) distinct authentic original sources. Consequently, if s>=C(n+1)(D+1), s<=t and 2^(B-D)>U(n,t), EVERY attained island output lies in BOTH H(YES_s) and H(NO_t). An explicit generous bound for the number of standard n-input, fan-in<=2 Boolean circuits with <=t gates is U(n,t)<=(t+1)(n+t+2)[16(n+t+2)^2]^t. Thus for D=o(N), s above the sparse-circuit section cost, and t=N^beta (fixed beta<1), all island labels are mixed eventually.

**Proof:** The fiber indicator Q_v(z)=product_i(1+P_i(z)+v_i) over GF(2) is nonzero and degree<=D. Choose a satisfying z with inclusion-minimal 1-support S. Setting all other variables to zero turns Q_v into the exact AND of the |S| support bits; therefore |S|<=D. The source E(z)(i)=(i mod 2) XOR 1[(i>>1) in S] has an ordinary circuit consisting of at most D equality tests, proving (1). The binary Reed-Muller minimum-weight inequality gives at least 2^(B-D) ones for any nonzero B-variable polynomial of degree<=D (induction on the last variable proves it). E is injective, so these are distinct original sources. If the fiber is larger than all functions of circuit complexity<=t, some member has CC>t, proving (2) and the consequence. QED. No efficient hard-source generator is claimed.

This strengthens the applicability of the existing project's classical THRES-POLYFIBER10, CLOCKRMFIBER25 and CLOCKADAPTIVEPOLY31 ideas to a **large easy-lift affine island even when global H degree is maximal N**. It does NOT prove saturation for outputs outside this island. No mathematical originality for Reed-Muller or Chevalley-Warning is asserted.

## Theorem 45B: high-degree, source-coupled, fixed-PH one-tape counterexample

Let J_n={0,1,2,4,...,2^(n-2)}, exactly n distinct pair indices among B=N/2. Define H_n(f)=(p(f),A(f),V(f)) with p(f)=(f_(2j):j in J_n increasing), A(f)=AND_(i<N)f_i, and V(f)=OR_(j<B)(f_(2j) AND f_(2j+1)).

On E(z), A=V=0, p=(z_j:j in J_n). Hence **every one of the 2^n island outputs (p,0,0)** has **exactly 2^(B-n)** distinct genuine original-source preimages. Every label has a sparse y with <=n nonzero z bits and a genuine original-source circuit of size <=n^2+10: share n-1 negated address literals, use at most n(n-2) AND gates for n equality tests, n-1 OR gates, and six gates for the final XOR. Thus D=n, but the COMPLETE output coordinates A and V have global source-variable ANF degree N. For V use the identity V=1+product_j(1+f_(2j)f_(2j+1)), whose top monomial has degree N. V(1100...)=1 but V(1010...)=0: same source Hamming weight, different index order. A has a pivotal assignment for every source bit.

**Concrete finite theorem, not an asymptotic experiment:** n=20, N=1,048,576, B=524,288, choose s=500 and t=4096. The section cost n^2+10=410 <=s. Each of 2^20 island outputs has 2^524268 original preimages, whereas log2 U(20,4096)<114776. Every such output therefore has BOTH an easy YES_500 original source and a (nonconstructively) hard NO_4096 original source. This proves a finite quantitative two-sided collision for every island label. For arbitrary fixed 0<beta<1 the same holds eventually at t=N^beta and any s between n^2+10 and t.

**Uniform fixed-PH supplied-circuit equality:** Given an n-input Boolean source circuit C and a target vector, evaluate the n source addresses 2j from J_n. To compute A ask one NP query whether some i has C(i)=0 (negate reply). To compute V ask one NP query whether some j satisfies C(2j)=C(2j+1)=1. Thus the complete source-circuit equality relation is uniformly in P^NP[2], a fixed PH level. This does not give a polynomial-time source-hardness decision or execute an oracle on the source tape.

**Charged physical transducer:** A one-way read-only input streams all N authentic source bits. ONE ordinary two-way work tape stores a pair counter, pending bit, A/V accumulators, and n selected provenance bits. At pair j, select its genuine even-indexed source bit when j=0 or j is a positive power of two; this is detectable online without an input-length header, and collects exactly n bits for N=2^n. At EOF, validate N and serialize p followed by A,V. Conservative bound O(N log^2 N) single-work-tape time, O(log N) work space, n+2 output bits. Input, counter moves, sampling buffer, EOF and output are all charged. Python tests logical scans, not microstep tape simulation. Every source bit is read exactly once.

The required **universal NO-image exclusion FAILS**, despite maximal global ANF degree, source order dependence, logarithmically many genuine provenance samples, joint fixed-PH equality and near-linear headerless single-work-tape implementation.

## Verified computation and hostile controls

The complete executed local CPython 3.13.5 audit, seed 20261118143045, passed **538,446 assertions with zero failures**. Authentically enumerated all 16, 256 and 65,536 source words for N=4,8,16 with independent streaming evaluation; sampled 1,200 each for N=32,64 and 500 for N=128. Exhaustive complementary-pair islands through B=16: n=5 produced 65,536 distinct island sources, 32 attained labels, exactly 2,048 sources per label, with explicit sparse representatives. Exact Möbius ANF degrees for A,V are N at N=4,8,16. Ordered-pair changes at fixed Hamming weight and full coordinate-provenance leakage were also controlled. Counting margins at n=10,12,14,16,20 were positive; n=20 is >409,492 log2 bits.

A **separately executed compact Python reproducer** passed **65,821 checks with zero failures** and verifies the exact n=20 counting arithmetic. GitHub Python is this compact reproducer, NOT the full local audit. GitHub JSON is only the executed summary, NOT the entire local raw dataset.

**Four gates:** DISJ N/A (no rank implication); relativization unrestricted OPEN; simultaneous DTISP FAIL for this source-NO-pure candidate and general transfer OPEN; deterministic configuration PASS as an upper-bound model sanity check only. Natural Proofs and algebrization not bypassed, /341 FAIL as full UNSAT authority, /386 RESTRICTED. Prior partial-MCSP, majority-closure, Chevalley-Warning, affine, adaptive-hash/seed, exceptional KL, two-probe, histograms, 2CNF and monotone-certificate guards remain active. No TMR-owned living manuscript or agent schedule was modified; this separate Clock Gate role owns none. No checkout preflight was run; connected GitHub source reads were used. Independent mathematical review pending.

**ONE NEXT: AFFINE-ISLAND-HIT46.** Test whether an actual source-NO-pure quotient can evade the restricted-degree/mass trap simultaneously on all large, efficiently liftable affine source islands while preserving legitimate alternative circuits, fixed-PH joint verification and charged same-realization one-tape execution. P versus NP OPEN.

References: [1] Saptharishi, Shpilka, Volk, *Efficiently Decoding Reed-Muller Codes from Random Errors* (2015), https://arxiv.org/abs/1503.09092 . [2] Cheraghchi, Hirahara, Myrisiotis, Yoshida, STACS 2021, https://doi.org/10.4230/LIPIcs.STACS.2021.23 . [3] Repository THRES-POLYFIBER10, CLOCKADAPTIVEPOLY31 and CLOCKRMFIBER25.
