# AFFINE-SMALLBIAS-DESCENT-GATE2 handoff

2026-10-30, run initiated 09:19 America/Los_Angeles. P versus NP OPEN. Independent red-team review PENDING. No task, schedule, agent activation, root MAIN, or ownership-region changes.

## Exact result

For fixed 0<nu<mu<1, source length N=2^n, polynomially bounded target truth-table length M=2^m, source threshold floor(N^mu), and target threshold u_N<=N^nu, an input-independent randomized affine map R_z(x)=A_z x XOR b_z cannot preserve both MCSP labels with worst-case error bounded below 1/2 by a fixed positive constant. Even unbounded source-independent matrix/offset preparation is covered. The seed is independent of x.

CHMY Theorem 33 gives an epsilon_N-biased easy-source distribution D_N, with epsilon_N=2^(-ceil(N^rho)) for nu<rho<mu. All its outputs have circuit size N^(rho+o(1))<N^mu. If C is any at-most-B target set, elementary Fourier expansion of an affine fiber gives |Pr_D[R_z(x) in C]-Pr_U[R_z(x) in C]|<=B epsilon_N. This compares R_z(D_N) with R_z(U_N), NOT with U_M.

An independent, simpler proof for diagonal masks uses the earlier LOW-SIZE-HALFDISTANCE9 k-wise source construction. A mask exposing <=k positions gives identical distributions; otherwise each accepted output has probability <=2^-k. Thus the acceptance gap is at most B*2^-k.

## Counting-display precision correction to the archived full report

In Section 7 of `research/agents/threshold-descent/2026-10-30_0919_ROUTE1_AFFINE_SMALLBIAS_DESCENT_GATE2.md`, the counting display should read

    log_2 B_N = O((u_N+1) log(m+u_N+2)) <= N^(nu+o(1)).

The +1 also covers u_N=0; the final comparison is an upper bound, not an equality for arbitrary u_N<=N^nu. The preceding derivation and conclusion require only this upper bound. The downloadable local full report incorporates this notational correction. No asymptotic conclusion changes.

With eta_N=|source-YES|/2^N=o(1), the exact error bound is

    e_N >= (1-eta_N-B_N epsilon_N)/(2-eta_N) = 1/2-o(1).

## What this closes, and what it does not

Every fixed-seed additive-port construction Phi_z(f)=H_z XOR (Q_z AND f) is affine in the source bits. The previously unresolved critical-depth band and baseline-saturation alternative cannot rescue this family. Layer independence and baseline smallness are unnecessary in the new proof. Seed-dependent ports are also covered when their choice does not depend on f.

The original CHMY generator and its lower bound are not refuted. A genuinely nonlinear/source-dependent transformation is not covered. A valid reduction must preserve ALL source YES inputs, not merely distinguish D_N from U_N. The standard-model SAT-to-ordinary-MKTP R_k is not supplied or ruled out. ARC and COMPACT-HISTORY20 obligations are unchanged.

Output-length guard: with M=N^(a+o(1)) and target threshold M^beta, the theorem needs a beta<mu. Mere exponent dilution by padding with unchanged numeric threshold is not excluded.

## Executed evidence and verified publication

Full report:
`research/agents/threshold-descent/2026-10-30_0919_ROUTE1_AFFINE_SMALLBIAS_DESCENT_GATE2.md`
Report commit: 5d4b8857f4bfde2dfb0e0f590e7e4e7250144e30; verified blob 9a315c98b24c7831dc1a151b4055edd3f05f6e6e.

Code:
`experiments/review/2026-10-30_ROUTE1_AFFINE_SMALLBIAS_DESCENT_GATE2.py`
Verified blob ff2e014c9126a7d8be37f3c90b667b308a5d086b exactly matches the executed local code. SHA256 a3cf902f1dd06c14af887b3a0753f26e5e0ce7ba32471262f07862055a01c007.

Raw:
`results/raw/separation/2026-10-30_ROUTE1_AFFINE_SMALLBIAS_DESCENT_GATE2_raw.json`
Verified blob cb50858a0cd881350242534657ea576870a62f90 exactly matches the executed raw output. SHA256 c8414725efa1fb6a82f087bdf7af0656ffb3c4ebe6f0498ad5f5e0f6bf5a6a79.

Tests: 32,768 affine maps, 262,144 singleton inequalities, 1,048,576 accepting-set checks, 512,000 multiport identity checks, and actual finite-field primitive/hostile controls; zero failed assertions. These are finite probability checks, not an asymptotic separation or circuit-minimization experiment.

## Single next constructive obligation

Specify a genuinely nonlinear or input-adaptive output-bit predicate and prove both source-label implications; test it against the explicit easy-source ensemble and uniform sources before claiming a useful threshold reduction. Then charge full input access, target serialization, seed construction, one-tape fusion, error and live state. A distinguisher for the generator alone is insufficient.

END_OF_VERIFIED_HANDOFF::AFFINE_SMALLBIAS_DESCENT_GATE2::P_VS_NP_OPEN
