# THRES-DUALTRACKS16 | 2026-10-19 01:47 KST

**Status:** Two scoped combinatorial results proved, one CHMY-backed same-one-tape range-language transport conditional on the specialized overlay proof; independent review pending. No ordinary MCSP parameter descent, no P versus NP proof.

## Sources and proposals

Read ASYMPTOTIC_CONE5, LOSSY_PROMISE_CASCADE6, PARTIAL_SAMPLE_WEDGE7, PROMISE_CASCADE_FIXEDPOINT8, SOURCEQUERY_SYNTHESIS10, STREAMSATURATION12, AUTOMATICSECTION15, and newer main commits. Checked CHMY ECCC revision: Lemma 14, Theorem 15, Corollary 22. Targeted Forbes-Kelley FOCS 2018 explicit PRG and Boolean finite differences.

Proposals: (1) continuously stateful source-sweep affine-cube tester; (2) worst-case all-small-circuit-YES selective anti-checker; (3) source-length-oblivious parity blocks + CHMY generator-range language; (4) iterate range-language back into ordinary MCSP. Built/falsified (1)/(2), constructed exact image (3), rejected unsupported iteration (4).

## A. Adaptive full-sweep counterexample to extrapolating k-wise probe bounds

Set N=2^n, 2<=k<=2^(n-3), d=ceil(log2 k). Uniform GF(2^n) polynomials of degree <k, followed by nonzero binary trace, yield k-wise-independent N-bit truth tables, each of circuit size O(kn^2). Every such Boolean function has algebraic degree <=d because x^(2^j) is F2-linear and deg_Bool(trace(x^m)) <= wt_2(m). Therefore every affine (d+1)-cube has XOR zero.

Choose three disjoint (d+1)-cubes C0,C1,C2. One one-way full source sweep saves f(0), selects C_(f(0)), computes parities on selected cube and C2, and emits 1 iff both vanish. An n-bit index counter, one selector and two parity bits suffice: O(log N) mutable space and O(N polylog N) time. The polynomial YES ensemble is accepted with probability 1. Under U_N, conditioned on f(0), the two disjoint cube parities are independent fair bits: acceptance exactly 1/4, advantage 3/4.

**Falsifier:** f=1[x=1] has O(n)-gate circuit but fails this test. Thus this construction is NOT worst-case MCSP promise-pure and DOES NOT distinguish CHMY's genuine local PRG. It proves the prior ADAPTIVEKWISE7 source-probe indistinguishability cannot be generalized to a continuously stateful full sweep using only source space bounds.

## B. Positive distributional parity-range quotient, not ordinary MCSP

Fix rational 1/2<nu<1 and alpha=1/nu-1. The j-th source-independent, *online* block has planned length ell_j=2^floor(alpha floor(log2(j+1))); emit its parity upon completion and the final partial block at the input endmarker. This source-length-oblivious schedule has b(N)=Theta(N^nu) nonempty blocks. A one-tape source transducer uses O(log N) space, O(N polylog N) time and outputs each parity immediately. To encode without advance knowledge of n, emit data bit v as 0v, then terminal delimiter 11 and self-delimiting n footer; output length L=2b+O(log N).

For ANY G_N:{0,1}^k->{0,1}^N with k<b, define **the actual one-way serialized string** Enc_n(v)=0v_1 0v_2 ... 0v_b 11 SD(n), with SD(n) a self-delimiting footer. Let L_(G,R)={Enc_n(R_N(G_N(z))):n>=1, z in {0,1}^{k(n)}}. Its index is in the FOOTER, not a 1^n HEADER; this avoids requiring the streamer to know N in advance. Reject malformed encodings. Disjoint block supports make R_N(U_N) uniform on b parity bits. The generator has <=2^k possible compressed outputs. Thus YES probability=1 and uniform-source NO soundness error <=2^(k-b). Genuine lossiness is achieved; target is generator-range membership, NOT MCSP/Gap-MCSP or a low-rank HASHIMAGE_t witness language.

Use CHMY Corollary 22: for fixed nu in (1/2,1), take t_N=N^(2nu)exp(-2sqrt(log N)), seed k_N=O_tilde(sqrt(t_N))=o(N^nu), and the local PRG fooling time t_N one-tape RTMs to error 1/6 (no oracle, or explicitly bounded short oracle queries). Then b>=4k eventually. If a uniform bounded-error one-way-input/one-work-tape decider B recognized the indexed range language in time L^(2-delta), composing it lazily with the O(log N)-space one-way parity producer via the neighboring-cache work-tape overlay (STREAMFUSION11, independent review pending) costs O((N polylog N+L^(2-delta)) polylog N)=N^(max(1,nu(2-delta))+o(1))<t_N. Its PRG-vs-uniform advantage is >=1-2e-(1-e)2^(k-b)>1/6 for e<=1/3, contradicting CHMY. Hence **conditional on the declared one-tape overlay formalization**, this indexed range language has no randomized same-model O(L^(2-delta)) algorithm, for any fixed delta>0.

Its natural seed witness has length k=L^(1-o(1)); if G is uniformly polynomial-time evaluable, the indexed target is in NP with a fixed exponent for fixed nu, but CHMY locality alone is not an NP-verifier proof. P=NP may yield an exponent K>=2, which does not conflict with the transported near-quadratic lower bound. This is not an MCSP threshold map, not a beta_j->0 cascade, and does not amplify g(beta)/beta.

## Finite controls (standard-library Python)

GF(16) trace-polynomial ensembles: all 256, 4096 and 65536 coefficient tuples for k=2,3,4 respectively passed cube-parity identities. One-cube adaptive detectors accepted exactly 32768/65536 uniform 16-bit sources. Two-cube adaptive test at k=2 accepted all 256 polynomial seeds and exactly 16384/65536 uniform sources, rejecting the O(n)-gate point-function YES. Toy NON-CHMY generator N=64,k=5: length-known b=16 parity image has exactly 32/65536 outputs; all 65536 output syndromes were inverted and 10000 streaming comparisons passed. Actual length-oblivious dyadic schedule N=64,alpha=1/3 produced b=36 blocks, 32 toy image words, and 6000 successful constructed target-syndrome preimages. No actual CHMY generator was computationally sampled. No failed tests. These verify finite identities ONLY.

**Next:** Formal independent review of cache one-work-tape model; explicit CHMY generator uniform evaluation; genuine all-YES selective anti-checker; typed reduction from indexed compressed range language to ordinary MCSP without losing promises or increasing the normalized witness threshold. No valid rho>lambda, no cofinal slope divergence. P versus NP OPEN.

Primary references: CHMY STACS 2021 DOI 10.4230/LIPIcs.STACS.2021.23 (ECCC revision https://eccc.weizmann.ac.il/report/2020/103/revision/1/download/); Forbes-Kelley FOCS 2018 DOI 10.1109/FOCS.2018.00093; Oliveira-Pich-Santhanam Theory of Computing 2021.

END_VERIFICATION_SENTINEL::THRES_DUALTRACKS16::P_VS_NP_OPEN
