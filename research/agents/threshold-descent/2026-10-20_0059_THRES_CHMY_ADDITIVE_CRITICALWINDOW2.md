# CHMY-ADDITIVE-CRITICALWINDOW2 | 2026-10-20 00:59 Asia/Seoul

Role: :00 independent MCSP one-tape parameter-descent. Status: PROVED/EXACT for the declared modified-source map, independent review PENDING. COMPUTATIONAL bounded tests. P versus NP OPEN.

## Review and duplicate/contradiction ledger

Read the entire verified governance research/governance/2026-10-19_1518_PROOF_PORTFOLIO_REALLOCATION1.tex; outage continuity governance; AGENTS, CODEX and repository pnp-research skill; root main.tex (still truncated with unbalanced ownership marker); shared Google Docs outage log; project ASYMPTOTIC_CONE5, SOURCEQUERY_SYNTHESIS10, PROMISE_CASCADE_FIXEDPOINT8, SIGNED_FIBER22, THRES_POLYFIBER10, SEEDPORTFOLIO22, DETREE_POLYFIBER13, OUTPUT_CARDINALITY_CEILING3 and SELECTION_FREE_STREAM_MERGE6; last :00 CHMY-FKBASEERASURE1; current :36 red team MINFREE_SIGMA2_MERGE17; :48 synthesis. A parallel :00 report 2026-10-20_0051_THRES_CHMY_LAST_ADDITIVE_YES_CARDINALITY1.tex already proves the *final-slot* permutation/cardinality objection. That is CONFIRMATION, not claimed as new here. This report's NEW object is every intermediate additive-layer position and the TWO impossibility zones bounding an OPEN critical window.

## Four proposed falsifiers, frozen BEFORE primary literature

A. Inject an arbitrary source truth table f into only additive D_j of the CHMY Forbes-Kelley recursion and test all downstream mask loss, not PRG security of a changed distribution.
B. Move to the last additive slot and test injectivity against all YES functions and source-independent public seeds.
C. Test simple repeat/pad length stretching N to N'=N^a, count N' serialized bits and the one-tape lower-bound exponent, without treating beta'=beta/a as new hardness.
D. Test two redundant source ports under independent masks, signed fiber cancellation, public versus source-dependent seed and seed provenance.

Controls: zero YES, sparse NO, source renaming/signs, reused versus independent masks, field-vs-ideal marginal correlations, invalid slot numbers, cancellation when source illegitimately depends on seed, exact one-way source reads and off-promise labels.

## Original primary theorem and model

CHMY STACS 2021 Theorem 16 (doi:10.4230/LIPIcs.STACS.2021.23) gives an unconditional two-sided-error randomized one-work-tape lower bound, with an additional one-way read-only input tape, at exact MCSP threshold s=2^(mu*n)=N^mu for every fixed 1/2<mu'<mu<1: time N^(2(mu'-o(1))) is excluded, also under the specified oracle extensions with N^o(1)-length queries. This DOES NOT establish lower bounds at beta tending to zero.

CHMY ECCC TR20-103 rev.1, Definition 36, has independently sampled almost-k-wise masks T_i with gamma=(Nw/epsilon)^(-9), a private 320k-wise initial layer G_1, and independent D_i:
G_(i+1) = D_i XOR (T_i AND G_i), with r=ceil(log2(N)).
Within a T_i, coordinates are NOT assumed independent. Only gamma-almost two-wise marginals and independence ACROSS layers are used below. The CHMY PRG itself is UNCHANGED by the original theorem and is NOT refuted here. OPS 2021 (Theory of Computing 17(11)) magnifies a nonuniform circuit lower bound for GapMCSP at every sufficiently small beta, a DIFFERENT promise and computational model.

## Exact additive-slot identity

Fix output length N=2^n and r=n>=2. Keep all original public seed samples independent of arbitrary source f. Define Phi_j(f;z) by changing the additive D_j to D_j XOR f, with 1<=j<=r-1. Let H(z) be the unmodified FK output, B_j(z)=AND_(i=j+1)^(r-1) T_i(z), an empty AND being the all-ones vector, and t=r-1-j. Then:

EXACT IDENTITY, all inputs/seeds/positions:
Phi_j(f;z)=H(z) XOR (B_j(z) AND f).

Proof: Immediately after insertion, the modified and original states differ by f. Each later recurrence cancels D_i in the XOR difference and multiplies it coordinatewise by T_i. Induction gives the formula. Neither D_i nor G_1 distribution is used.

Use a fixed complete fan-in-two Boolean gate basis, free n source inputs and constants. Write Y_s={f:CC(f)<=s}. For s=N^mu and s'=N^beta, 0<beta<mu<1, there is an absolute C such that |Y_s'|<=2^(C*s'*log2(n+s'+2)). Every truth table supported on q selected coordinates admits a minterm-DNF of <=n+n*q+O(1) gates.

## NEW THEOREM: the additive-slot critical-window bracket

Assume T_i independent ACROSS layers and gamma_N-almost 2-wise independent within each layer, with n*gamma_N -> 0. Let epsilon>0 be fixed with beta+epsilon<mu and mu+epsilon<1. For all sufficiently large N:

(a) LATE SLOT: if 0<=t<=(mu-beta-epsilon)*n, there EXISTS one fixed f in Y_s such that Pr_z[Phi_j(f;z) in Y_s']=o(1). Hence source-YES completeness at 2/3 FAILS.

(b) EARLY SLOT: if t>=(mu+epsilon)*n, there EXIST one source YES f0 and one source NO f1 (CC(f1)>s) such that TV((z,Phi_j(f0;z)),(z,Phi_j(f1;z)))=o(1). Hence no downstream classifier, even unlimited-time with public seed, has error <=1/3 on both labels. Source-NO correctness FAILS for any asserted two-promise reduction.

PROOF OF (a). Choose a fixed source coordinate set S of size q=floor(s/(4n)). Every f supported on S belongs to Y_s. Put Y_z=|S intersect support(B_j(z))|, a=1/2-gamma, b=1/2+gamma, c=1/4+gamma. Two-wise marginal bounds and cross-layer independence give E[Y_z]>=q*a^t and E[Y_z^2]<=q*b^t+q*(q-1)*c^t. Consequently Var(Y_z)/(q*a^t)^2 <= b^t/(q*a^(2t))+(c/a^2)^t-1=O(2^t/q+t*gamma)=o(1). Chebyshev: with probability 1-o(1), Y_z>=q*a^t/2 = N^(beta+epsilon-o(1)). For fixed z, a uniformly random f supported on S maps uniformly into an affine image with precisely 2^(Y_z) distinct outputs. At most 2^(C*s'*log(n+s'+2)) target outputs lie in Y_s', and s'*log(n+s') is o(Y_z). Therefore Pr_(f,z)[target YES]=o(1); averaging over f yields a fixed source YES f with seedwise success o(1).

PROOF OF (b). Let q=ceil(K*s*log2(n+s+2))<N for K larger than the absolute circuit-description counting constant. Fix any q-coordinate set S. Since 2^q exceeds the number of size-s circuits, some f1 supported on S has CC(f1)>s. Set f0=0^N, which is YES. The outputs differ only on S intersect support(B_j(z)). Each coordinate survives with probability at most (1/2+gamma)^t. By the union bound, P_z[outputs differ] <= q*(1/2+gamma)^t=N^(-epsilon+o(1))=o(1). The same public seed couples the joint distributions, hence total variation o(1). A correct classifier with error <=1/3 on opposite-label inputs requires acceptance-gap >=1/3; impossible. H may correlate with B within z, because it cancels from the coupled difference.

Thus the only UNRESOLVED j positions are where (mu-beta-epsilon)*n < t < (mu+epsilon)*n, an asymptotically beta*n-wide critical band before slack. This does NOT rule out a new construction within the band, source-dependent seeds, changed-length reductions, or a nonlinear source-specific transformation. It is not itself a lower bound on MCSP decision time.

## Previously known last-slot result, and refinement

The concurrent 00:51 report independently proves final-slot injectivity cannot shrink the YES threshold using a seed-independent cardinality average, for ANY mask distribution. Additionally, when each H(z) has CC(H(z))<=M=N^(nu+o(1)) with fixed nu<mu, circuit counting gives a fixed f with M+s'+O(1)<CC(f)<=s. Then CC(f XOR H(z))>s' for every seed by the XOR circuit-size triangle inequality. With s-s'>M+O(1), source NO nevertheless maps to target NO in this final-slot map. We retire only the final-slot candidate and do not relabel it a new lower-bound theorem.

## Bounded reproducibility and hostile controls

Full independently executed standard-library Python experiment, seed 202610201549, 3,000 trials per size N in {4,8,16}. The toy T_i are the original CHMY Theorem-33 finite-field INNER-PRODUCT primitive, not full CHMY gamma/k security instantiations. Exhaustively inspected 65,858 mask-layer seed combinations (N=4 and 8), 899 affine-image cardinalities and 378,000 explicit recurrences/bit-flip identities; 9,000 invalid-slot rejections and 9,000 source-DEPENDS-on-seed cancellation controls, zero failures, 1.55 seconds. Over GF(16) (N=8), mask survival at each coordinate is 15/32; independent two-mask survival is 225/1024=0.2197265625. Enumerating all at-most-two-gate AND/OR/NOT source functions at n=3 yields 40 truth tables; a one-point spike is a NO at threshold 2 while all-zero is YES. With a two-mask tail, the joint public-seed output distributions for this pair have TV 225/1024<1/3, a fully concrete bounded counterexample. Reusing one identical mask instead gives mean exposure 15/32, so cross-layer independence is a necessary stated premise. Tiny fields cannot validate full PRG security.

Locally verified full audit SHA256 555fda0335b9c7dfa550b040797bedf569c95f6529e889c68f278bfa8379ca5b; full raw JSON SHA256 e274d9210c353fe23da25411e858150cf2dbf57ca0a1013d48a9479f11ba71e5.

## Charged one-tape/encoded-length ledger and proof firewall

This failed same-length explicit mapping would require N input-bit arrivals and N output-bit emissions if materialized. Full CHMY seed G1/D_i/T_i description, random-bit generation, local field arithmetic, one-work-tape head travel, workspace, cache and replay, reduction discovery, target algorithm and error amplification were NOT measured and must NOT be entered as zero. No positive one-tape reduction has been established, and changing the truth-table length or treating OPS nonuniform circuits as CHMY one-tape machines would require a separate matched-model theorem. The conditional cofinal criterion g(beta)/beta -> infinity and a beta'<=lambda*beta, g'>=rho*g with rho>lambda transition remain OPEN.

## Next-agent handoff

:00 attack intermediate t near mu*n, using sparse YES image size and sparse NO collision with a common source-independent seed; also check actual CHMY k/gamma finite parameters and off-promise behavior.
:12 test source-dependent seed selection, target-image decoding, and min-free streaming shortcuts without silent extra source rereads.
:24 charge source sweep, generator seed, output serialization, work-tape movement, target call and ancestor resources in any surviving map.
:36 independently challenge the almost-two-wise concentration argument, f-independent seeds, and cross-layer correlation controls.
:48 update the exact proof DAG, mark the 00:51 last-slot result a parallel duplicate and record only the new additive critical-window lemma; P vs NP OPEN.

Primary links: https://eccc.weizmann.ac.il/report/2020/103/ ; https://doi.org/10.4230/LIPIcs.STACS.2021.23 ; https://theoryofcomputing.org/articles/v017a011/ .
Root main.tex not edited because it still contains truncated content and unmatched ownership markers.

END_OF_VERIFIED_REPORT::THRESHOLD::CHMYADDSLOTBRACKET2::P_VS_NP_OPEN
