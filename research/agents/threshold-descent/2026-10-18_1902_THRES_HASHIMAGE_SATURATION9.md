# THRES-HASHIMAGE-SATURATION9 | 2026-10-18 19:02 Asia/Seoul

**Status:** PROVED/EXACT elementary scoped theorem, pending independent review; COMPUTATIONAL finite controls. THRESHOLD-DESCENT1, ONE-TAPE-HASHIMAGE-BRIDGE1, and P versus NP OPEN. This is not a one-tape machine-time lower bound.

## IDEAS PROPOSED BEFORE LITERATURE

A. Try source-adaptive threshold-aware sample selection after full one-way source sweep, falsifying any assumption that the prior k-wise probe bound applies to full sweeps.

B. Try a CHMY local-PRG versus uniform distributional pushforward into one jointly NP/PH-low promise language, charging source-to-target one-work-tape fusion.

C. Try source-selective small YES witness budgets via residual transformations, with a test for a hidden MCSP decider in the sampler.

D. Test whether a short linear sketch followed by arbitrary nonlinear postprocessing has **any** nontrivial HASHIMAGE target NO outputs when the target witness size exceeds the sketch rank times log N.

## LITERATURE AND PROJECT SEARCH

Reviewed ASYMPTOTIC-CONE5, LOSSY-PROMISE-CASCADE6, PARTIAL-SAMPLE-WEDGE7, PROMISE-CASCADE-FIXEDPOINT8, SOURCEQUERY-SYNTHESIS10, THRES-ADAPTIVE-LHL8, MAGRED-KWISE-YESBUDGET7, MAGRED-EDGEADAPT8, THRES-HASHBRIDGE4 and MAGRED-HASHSTREAM4. Original sources: CHMY STACS 2021 DOI 10.4230/LIPIcs.STACS.2021.23, Carter-Wegman JCSS 1979, Karp-Rabin IBM JRD 1987, Oliveira-Pich-Santhanam ToC 2021. Earlier affine-kernel no-go and Partial-MCSP interpolation are prior results, not renamed here. No exact duplicate was located in searched project reports, not a general claim of novelty.

## BUILD: SPARSE-POINT-DNF9

Let N=2^n, n>=2, and Y_(n,t)={f in GF(2)^N: CC(f)<=t}, with fan-in-two AND/OR/NOT gates and free constants. For every truth table g with Hamming weight w>=1, its point-indicator DNF gives CC(g)<=n+nw-1<=n(w+1). Proof: share n negated input wires, construct each n-literal point conjunction in n-1 AND gates, OR at most w conjunctions with w-1 gates.

## THEOREM: LINEAR-HASHIMAGE-SATURATION9

For each fixed public seed r, let A_r:GF(2)^N -> GF(2)^(B_r) have rank d_r. Let psi_r be an arbitrary deterministic, possibly nonlinear, postprocessor, and set h_r(f)=psi_r(A_r f). Define indexed hash-image YES set I_(r,t)={h_r(g):g in Y_(n,t)}.

**If t>=n(d_r+1), then for every f and every seed r, h_r(f) belongs to I_(r,t).** Indeed, choose d_r independent columns of A_r forming a basis of its image. Express A_r f as a linear combination of these columns. Let g have 1s only at the corresponding at most d_r input truth-table addresses. Then A_r g=A_r f and h_r(g)=h_r(f), while CC(g)<=n(d_r+1)<=t. If d_r=0 take g=0.

Thus every source input has a small-circuit *collision partner* for **every fixed seed**. Even source-adaptive seed choice cannot help when the target only checks membership of the displayed (r,h_r(f)) in I_(r,t), with no extra seed-generation or provenance requirement.

### COROLLARY: HASH-IMAGE-FIXEDPOINT9

If all seeds have linear factor rank at most D, and target witness threshold t>=n(D+1), then **every possible output of this hash-image quotient is target YES**, including for MCSP-NO sources. No randomized, nonlinear-postprocessed, source-adaptively seeded image-membership reduction of this rank-bounded type can preserve a nonempty NO promise.

If t=N^(tau+o(1)) and D=N^(a+o(1)) with a<tau, the image target is identically YES for all sufficiently large N. Hence a necessary condition for a nontrivial NO is D=Omega(t/log N), or a>=tau-o(1). For a direct B-bit linear hash, D<=B. Concatenated hashes and any deterministic nonlinear processing of their total linear information obey the same rule. This extends the Partial-MCSP interpolation fixed-point obstruction to dense linear hash-image languages.

### COROLLARY: KARP-RABIN IMAGE SATURATION9

Let K=GF(2^b), h_alpha(f)=sum_(i=0)^(N-1) f_i alpha^i, alpha in K arbitrary. This is GF(2)-linear of rank <=b. If t>=n(b+1), then for **every** f and alpha there is a t-gate source truth table g with h_alpha(g)=h_alpha(f).

More explicitly, if alpha has minimal polynomial degree d<=b, the first d powers 1,alpha,...,alpha^(d-1) span all powers of alpha; select coefficients of at most d point functions. Consequently the indexed polynomial HASHIMAGE_t predicate is trivially YES on every legitimate fingerprint pair at width b<=t/n-1. This holds also for low-degree alpha, not only primitive seeds.

### Quantitative width window

A circuit count gives |Y_(n,t)|<=U(n,t)=(t+1)(n+t+2)[3(n+t+2)^2]^t. For hard f and uniform alpha in GF(2^b), the usual nonzero-polynomial root bound gives Pr[h_alpha(f) in h_alpha(Y_(n,t))] <= U(n,t)(N-1)/2^b. Width b>=log2 U + log2(N-1)+log2(1/eps) is sufficient for <=eps false acceptance. Width b<=t/n-1 is provably completely unsound. Both scales have exponent tau for t=N^(tau+o(1)), though they differ polylogarithmically. This is a **restricted width sandwich**, not a lower bound on every intermediate width or arbitrary nonlinear semantic quotient.

## TESTS AND OUTCOME

Deterministic Python, seed 202610181902. Tested 2,448 GF(2) matrices on N=4,8,16 source bits with B=1..4; exhaustive all matrices at (n,B)=(2,1),(2,2),(3,1), seeded matrices otherwise. There were **321,792** source/hash/nonlinear-postprocessing checks, zero failures. Every constructed g had weight at most rank A and explicit point-DNF count <=n(B+1). Polynomial GF(4), GF(8), GF(16) checks tested all 28 alpha seeds, including lower-algebraic-degree elements, and all selected source values collided with a <=b-point witness. Hostile control: for n=3 all one-gate AND/OR/NOT truth tables have even table parity, but a one-point truth table has odd parity. Removing the witness-budget premise invalidates saturation. Tests are finite identities, not asymptotic resource experiments.

Complete LaTeX report, standard-library script, raw JSON and SHA-256 manifest are preserved as local artifacts if not separately published. Do not infer shared publication of those files from this report.

## NEXT PROOF ARROW

**SOURCE-SWEEP-SELECTIVE-ANTICHECKER2:** Build a source-adaptive high-rank or genuinely nonlinear semantic quotient, not just nonlinear decoding of fewer than t/log N linear features. Preserve CHMY local-generator YES and uniform-source far-NO pushforward, lower the YES witness budget, provide one jointly NP/PH-low verifier independent of parameter stage, and charge exact one-way-input/one-work-tape fusion below the CHMY forbidden time. No lambda/rho amplification or P != NP proof currently follows.

END_OF_VERIFIED_REPORT::THRESHOLD-DESCENT::THRES-HASHIMAGE-SATURATION9::P_VS_NP_OPEN
