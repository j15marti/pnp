# PUBLICSEED-PLOTKIN14 | 2026-10-18 19:49 KST

Status: Exact restricted-model coding theorem; P versus NP OPEN.

PROPOSE > SEARCH > BUILD: Read newest Threshold Descent HASHIMAGE-SATURATION9, Clock Gate CLOCKSEED9, Resource Direct Sum CORESEARCH8, Magnification Red Team STREAM-NO10 and DISTANCE-OVERLAP9, plus main notes LOSSY_PROMISE_CASCADE6, PARTIAL_SAMPLE_WEDGE7, PROMISE_CASCADE_FIXEDPOINT8, K_ELIMINATION_TRANSFER4, SOURCEQUERY_SYNTHESIS10 and root main.tex. Primary references: Carter-Wegman 1979, Naor-Naor 1993, Cheraghchi et al. STACS 2021, Oliveira-Pich-Santhanam 2021, and classical Plotkin bound.

THEOREM. Let a public, source-independent seed select an exact collision-two-universal hash from N-bit source strings to b-bit digests. Suppose at most R seed outcomes. Then 2^N <= 2 R (2^b-1). Hence the seed must occupy at least N-b-1 bits. An explicitly serialized public seed plus digest costs at least N-1 bits, so this cannot be a self-contained shrinking first stage.

PROOF. Center the one-hot output indicator in each seed block, weighted by square roots of seed probabilities. The 2^N normalized input vectors live in dimension at most R(2^b-1), have unit norm, and pairwise nonpositive dot products by exact two-universality. Their Gram matrix G satisfies trace(G)=2^N and trace(G^2)<=2*2^N, using u^2<=-u for all off-diagonal u in [-1,0]. Eigenvalue Cauchy-Schwarz implies rank G >= 2^(N-1), proving the claim.

SHARPNESS. For b=1, write a source as (a,v) with v an (N-1)-bit vector; choose random (N-1)-bit s and output a XOR parity(s AND v). Every pair collides with probability 0 or 1/2. Exact exhaustive audits for N=2 through 6 agree, across 6,28,120,496,2016 message pairs.

SCOPE. Does not prohibit approximate universality, source-adaptive seed choice, restricted source domains, external uncounted public coins, or nonlinear transforms. Small-bias hashing may use short seeds because its collision guarantee has slack. HASH-COFINAL-ERASURE12 also needs high collision entropy, not established for actual CHMY outputs. Report does not establish a model-preserving MCSP lower-bound transfer.

DAG: ESTABLISHED, scoped seed length coding bound and existing source/interpolation barriers. CONDITIONAL, cofinal K-elimination and distributional-pushforward implication. OPEN, source-selective YES guard, same one-tape fusion, jointly NP/PH-low target and slope amplification rho>lambda. RETIRED, exact public-universal hash with explicitly serialized seeds as a cofinally shrinking target. P versus NP OPEN.

NEXT: STREAMING-DISTRIBUTIONAL-SELECTOR13 with near-linear one-work-tape source scan, honest seed accounting, and one jointly uniform NP/PH classifier, evaluated on actual CHMY generator versus uniform.
