# ROUTE1-MULTIPORT-PAIRWISE-BUDGET-GATE1
Date: 2026-10-30, America/Los_Angeles. P versus NP remains OPEN.
Status: PROVED/EXACT for a fixed-source-port, seed-independent, same-length modified Forbes-Kelley recurrence under its declared layerwise almost-two-wise masking, independent review pending. COMPUTATIONAL exact finite tests. NO uniform charged threshold descent and NO deterministic SAT-to-ordinary-MKTP R_k.

## Recovered state and 4 falsifiable mechanisms
Reviewed 2026-10-19 two-route governance and 2026-10-20 update; COMPACT-HISTORY20; prior MULTIPORT-MASK-FLOOR3 and CHMY-FIELDPAIR-CRITICAL4; signed-fiber/public-seed TV, sparse template KT, adaptive transcript KT; 2026-10-26 forbidden regions; 2026-10-30 HITTING-TREE-COMPOSITION-REFEREE222. Prior single-port critical window and pairwise finite-field moment theorem are not claimed as new. Falsifiers:
1. Test whether all fixed multiport masks retain pairwise concentration when coordinates have high-order dependence. Break by finding low-support bad seed mass despite pairwise closeness.
2. Test whether source-NO outputs become target-YES after sparse masked corrections whenever the baseline H is well below the target circuit threshold. Break by exhibiting correction complexity >O(nZ) in a complete gate basis.
3. Remove the assumed baseline margin and characterize the mandatory distribution of baseline circuit complexity if any reduction is both-promise correct. Break via a valid reduction with no near-threshold baseline mass.
4. Test a correlated-layer and finite-field aliasing adversary, and compare against shortcut source-access and compact-history arguments. No arbitrary-SAT lower bound may be inferred.

## Definitions
Let N=2^n, 0<beta<mu<1, s=floor(N^mu), s'=floor(N^beta), h<=n, fixed nonempty J subset {1,...,h}; j*=max J, t=h-j*. Independent public masks T_i in {0,1}^N, each with every pair of distinct coordinates within total variation gamma_N of two fair independent bits (thus also each marginal within gamma_N of fair). Independent seeds across layers. A source f is XORed into each D_j, j in J, while all other seeds and the baseline G_1 are independent of f. The final output is Phi_z(f)=H_z XOR (Q_J(z) AND f), with H_z=Phi_z(0). Here the source and target are dense N-bit truth tables and CC denotes minimum fan-in-two Boolean circuit size in a fixed complete basis. CHMY Definition 29 uses L1 <= gamma, so TV <= gamma/2; their Definition 36 and Theorem 37 provide the independent layers and gamma=(Nw/epsilon)^(-9) with k>=2. We use the slightly weaker TV<=gamma formulation.

## Theorem 1: all fixed-port pairwise concentration and late YES failure
For fair independent coordinates/layers define q_J=Pr[Q_J(a)=1], independent of coordinate a. The scalar recurrence p_0=0, p_i=e_i(1-p_{i-1}/2)+(1-e_i)p_{i-1}/2, e_i=1_{i in J}, yields
  2^{-(t+1)} <= q_J <= 2^{-t}.
For the actual almost-pairwise layer distributions put delta=h gamma_N. For every a, |Pr(Q_J(a)=1)-q_J| <=delta. For distinct a,b, |Pr(Q_J(a)=Q_J(b)=1)-q_J^2|<=delta. Consequently for fixed S of size r and Z=sum_{a in S} Q_J(a),
  |E Z-r q_J|<=r delta,
  Var Z <= r q_J+4r^2 delta,
where the last inequality holds for delta<=1 (a deliberately loose bound). If r q_J->infinity and delta/q_J^2->0, then Z=(1+o_P(1))r q_J.

In particular if gamma_N<=N^{-9}, 0<epsilon<mu-beta, and t<=(mu-beta-epsilon)n, take r=floor(s/(C n)) and a fixed r-coordinate set S. All 2^r supported functions have CC<=s by minterm-DNF for sufficiently large constant C. For random f supported on S and fixed seed z the image has 2^{Z(z)} equally likely values. At most 2^{O(s' log(n+s'))} truth tables have CC<=s'; Z(z)>=N^{beta+epsilon-o(1)} with probability 1-o(1), so the fraction mapping into target YES tends to zero. Therefore there exists a fixed source-YES f such that Pr_z[Phi_z(f) target YES]=o(1). This eliminates late positions, for every fixed multiport J, without independence across coordinates within layers.

Proof of moment assertion: for two fixed coordinates, couple each layer's two-bit marginal to an independent unbiased two-bit pair with disagreement probability <=gamma; because the layers are independently sampled, the probability of any coupling mismatch across h layers is <=h gamma. The output pair is a deterministic function of these layer bits, hence its joint distribution differs from two independent ideal coordinates by at most h gamma. For the ideal pair each coordinate follows the stated scalar recurrence, and pair output probability is q_J^2. For Z use E Z^2=sum E Q_a+2 sum_{a<b} E Q_a Q_b and subtract (E Z)^2; with E Z close to r q_J and delta<=1, Var Z<=r q_J+4r^2 delta. Chebyshev proves concentration. The minterm and circuit-description counting complete the YES failure. QED.

## Theorem 2: sparse correction forces baseline budget saturation on the NO side
Fix epsilon>0 with mu-beta+epsilon<1. Assume gamma_N<=N^-9 and t>=(mu-beta+epsilon)n. There is a fixed source NO f_1, CC(f_1)>s, and absolute gate constant C such that
  Pr_z[CC(Phi_z(f_1)) <= CC(H_z)+ C n(1+Z(z))]=1,
  Pr_z[C n(1+Z(z))>s'/2]=o(1),
where Z(z)=|supp(f_1) intersect supp(Q_J(z))|. More precisely choose S of size r=ceil(K s log(n+s+2)), K sufficiently large. There are more than 2^{O(s log(n+s))} distinct S-supported functions, so a fixed f_1 supported on S exceeds source threshold s. Each output difference is supported on at most Z coordinates and can be computed from its sparse exception list with O(n(1+Z)) gates. Moreover
  E Z <= r(q_J+delta) <= O(N^mu n)(2^-t+h gamma_N) = O(N^{beta-epsilon}n)+o(1).
Thus Markov yields Pr(C n(1+Z)>s'/2)=O(n^2 N^{-epsilon})=o(1).

If a claimed same-source-seed randomized reduction had target-YES probability >=2/3 for every source YES and target-NO probability >=2/3 for every source NO, apply it to f_0=0 and f_1 above. For f_0, Pr(CC(H_z)<=s')>=2/3. For f_1, the source-NO target-YES probability is <=1/3. Since, outside an event of o(1) probability, every seed with CC(H_z)<=s'/2 produces target YES also from f_1, one must have Pr(CC(H_z)<=s'/2)<=1/3+o(1). Subtract:

  ***NECESSARY BUDGET-SATURATION BOUND***
  Pr_z[s'/2 < CC(H_z) <= s'] >= 1/3-o(1).

Therefore if CC(H_z)=o(s') for all public seeds (for example an actual local generator under an independently verified sufficiently small width parameter), the NO side fails with probability 1-o(1) at these depths. Without such a bound, the theorem identifies the necessary near-threshold baseline mass rather than ruling out the reduction. This is not a result about the original CHMY generator's security.

The two theorems jointly leave, under a non-saturated baseline, only t=(mu-beta)n+o(n) as a possible asymptotic fixed-port position. At the critical exponent itself, no failure is established. No cofinal threshold reduction, slope rho>lambda, or P!=NP conclusion is proved.

## Falsification and independent exact finite tests
Uniform affine masks T_i(a)=u_i dot a XOR b_i on a in F_2^d, with (u_i,b_i) uniform and independently resampled by layer, have EXACT pairwise independence across distinct coordinates and extensive higher-order dependencies. Exhaustive standard-library Python script tests d=2/h<=5; d=3/h<=4; d=4/h<=2. Enumerated 87 distinct nonempty fixed port sets and 2,096,632 mask-seed/port combinations. For each port set, checked exact rational E Z=q q_J, E Z^2=q q_J+q(q-1)q_J^2, and sharp exposure range: 261 exact assertions, zero failures. A correlated-layer control with T2=T3, J={1,2}, h=3 has Q=0 identically, violating the independent-layer premise. Markov budget crossover computations for n=40,80,200,400,600 are symbolic arithmetic only, not universal-machine circuit measurements. Raw and code sha256 locally 37f2b17268fc346f40f57182ae3632a7c6768ef815823843aefb323430cce9f3 and 80d397472a63b814fdbba7049766bd382c8aefc14452bae4ce1aae62ec910073, respectively.

## Other-work synthesis and strict limitations
SIGNED-FIBER22 and PUBLIC-SEED-ERASURE-TAX5 support use of the SAME public seed to compare opposite labels; the relevant quantity is full target-label correctness, not mere Hamming exposure. CHMY-FIELDPAIR-CRITICAL4 warns that an undersized field has aliased coordinates, so the full generator's almost-k-wise T_i rather than the bare field inner-product primitive must be used. The recent HITTING-TREE-COMPOSITION-REFEREE222 demonstrates correct local-to-global interface retention on a separate restricted SAT class; this is a methodological analogy, NOT a machine lower-bound transfer. Adaptive-transcript KT FIREWALL32 shows that easy replay/short answer transcripts cannot manufacture ordinary high KT. COMPACT-HISTORY20 black-box iteration and full-table counting cannot be transferred to succinct transition circuits; affine fast-forward remains a falsifier.

No one-tape implementation or source/target tape fusion is built. For any surviving reduction, charge full N-bit source reads, source-independent seed creation, indexed mask evaluation, target output serialization, work-head movement, error, promise preservation, source/target length, any oracle use or representation, proof discovery, and retained live space. The original CHMY model must not be swapped for OPS circuits or the MMW short-query oracle streamer. The standard-model total SAT-to-ordinary-MKTP R_k and FLMV all-input ARC contractor remain OPEN.

## Next test and allocation
Preserve the two-route allocation. Route 1 should now inspect Theorem 38's actual parameter choice for the target baseline H_z: calculate CC(H_z)/N^beta under the full w,N,epsilon, not a toy finite field. If H_z must be well below the target threshold, the remaining target is the critical exponent t=(mu-beta)n+o(n). Build a source-YES/same-target-both-outcomes adversary there or an actual reduction with charged one-tape implementation. Route 2 independently tests global witness-interface discoverability and same-machine ARC contractor. Independent hostile review needed before promoting the budget-saturation theorem into synthesis.

## Primary literature
1. Cheraghchi, Hirahara, Myrisiotis, Yoshida. One-Tape Turing Machine and Branching Program Lower Bounds for MCSP. STACS 2021, ECCC TR20-103 rev. 1, Definitions 29 and 36, Theorems 37 and 38: https://eccc.weizmann.ac.il/report/2020/103/ .
2. Oliveira, Pich, Santhanam. Hardness Magnification Near State-of-the-Art Lower Bounds. Theory of Computing 17(11) 2021: https://theoryofcomputing.org/articles/v017a011/ .
3. McKay, Murray, Williams. Weak Lower Bounds on Resource-Bounded Compression Imply Strong Separations of Complexity Classes. STOC 2019: https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf .
4. Ilango. SAT Reduces to the Minimum Circuit Size Problem with a Random Oracle. SIAM J Comput 55(3), June 2026: https://doi.org/10.1137/24M1652568 .

END_OF_VERIFIED_REPORT::ROUTE1::MULTIPORT_PAIRWISE_BUDGET_GATE1::P_VS_NP_OPEN