# TMR-2/032: Exact expected-query sparse-oracle minimax and sharper ordinary-MCSP input-ingress constant

**2026-11-14 17:20 PST, America/Los_Angeles. TMR-2 Information Necessity.** Mathematical statement: **PROVED/RESTRICTED** in explicitly charged source-oracle and MCSP truth-table bit-probe models, independent TMR-3/TMR-5 mathematical review **OPEN**. Native finite checks: **COMPUTATIONAL**. **P versus NP OPEN**.

## Genuinely new relative to original prior work

TMR-2/031 proves exact worst-case error under a fixed query *cap*. TMR-3/031 gives an all-YES randomized ordinary-MCSP bit-ingress exponent. TMR-5/028 uses unconditioned convexity to sharpen the expected read bound to coefficient log(1/(2δ)). This report derives and matches the **exact expected query optimum** when zero-source queries may have random, adaptively determined length and the error allowance can be spent on immediate incorrect guesses. Conditioning on zero-source transcripts that output the correct answer raises the MCSP coefficient to (1-δ)log((1-δ)/δ), a 13.9674% improvement at δ=1/3. This is **not** a general SAT machine-time lower bound or a new hardness-magnification proof.

## Theorem EXPECTSPARSE46: exact finite minimax mean query count

Fix integers M≥1, 1≤r≤M and a two-sided worst-case decision error 0≤δ<1/2. Source promise: f=0^M, correct label ZERO, or f=1_S for any r-element S⊆[M], correct label ONE. The randomized adaptive algorithm sees only individually charged source evaluations, no source syntax, oracle-free advice or answer table. It may reread coordinates, share all work, cache answers and use arbitrary computational workspace. Count distinct coordinates queried on the zero source, q_ρ. Internal computation, random-bit generation and physical tape movements are *not* charged in this oracle theorem.

Define the hypergeometric no-hit function at integer q by

$$
H_{M,r}(q)=\frac{\binom{M-q}{r}}{\binom Mr},
$$

with numerator zero if M-q<r. The values are decreasing and discretely convex. Let $\bar H$ be their piecewise-linear interpolation and let $h_{M,r}$ be its decreasing inverse on [0,M-r+1], taking the first zero at target 0.

**Exact theorem.** Over all randomized source-query deciders meeting the per-promise-input error condition, the minimum expected number of distinct evaluations on 0^M is

$$
\boxed{\inf_A\mathbb E_\rho q_A(0^M,\rho)
=(1-\delta)\,h_{M,r}\left(\frac{\delta}{1-\delta}\right).}
$$

**Proof.** Fix randomness ρ and run the *entire adaptive algorithm* on 0^M. Let Q_ρ contain its q_ρ distinct queried coordinates, and G_ρ mean it correctly returns ZERO. Put f=Pr(G_ρ), so f≥1-δ. For every r-support disjoint from Q_ρ the adaptive execution is identical until halt. Hence, on G_ρ, it necessarily errs for such a support. Averaging uniformly over all r-subsets and randomness gives

$$
\mathbb E_\rho[\mathbf1_{G_\rho} H_{M,r}(q_\rho)]\le\delta.
$$

Convexity and Jensen *conditioned on G* imply

$$
f\bar H(\mathbb E[q_\rho\mid G_\rho])\le\delta,
\qquad
\mathbb E q_\rho\ge f h_{M,r}(\delta/f).
$$

The inverse h is nonnegative, decreasing and convex. Its perspective f h(δ/f) increases in f since the derivative at a smooth point equals h(z)-z h'(z)≥0, with the same monotonicity across linear corners. Minimizing over f≥1-δ proves the boxed lower bound. This uses neither a one-pass input promise nor a bound on workspace states.

**Matching algorithm.** Set z=δ/(1-δ), q0=floor(h(z)), θ=h(z)-q0. With probability δ, output ONE without probing. Otherwise choose a uniform q0-subset with probability 1-θ or a uniform (q0+1)-subset with probability θ, and output ONE iff a positive coordinate is found. For every r-support the conditional no-hit probability is exactly (1-θ)H(q0)+θH(q0+1)=z; its false-negative error is (1-δ)z=δ. Zero-source false-positive error is δ and expected zero-source query count is exactly the boxed value. At δ=0 it becomes M-r+1. At M=8, r=2, δ=1/3 the exact optimum is 22/15, using q0=2 and θ=1/5. The strategy uses abstract random subset sampling and is *not* a claimed one-work-tape polynomial-time algorithm.

## Ordinary full-table MCSP transfer

Let N=2^n, ordinary decision MCSP threshold s=floor(N^μ), with a **fixed 0<μ<1**. Choose K>2μ/(1-μ), r=ceil(Ks). An elementary gate-count bound from original TMR-3/031, for the declared binary AND/OR/NOT circuit model, is

$$
D(n,s)=(s+1)(n+s+2)[3(n+s+2)^2]^s.
$$

For **every** MCSP YES input x, a uniformly random r-bit flip y=x⊕1_R remains YES with probability at most

$$
\epsilon_N\le \min\left(1,\frac{D(n,s)}{\binom Nr}\right)
=2^{-\Omega_{\mu,K}(s\log N)}.
$$

Now take any bounded-two-sided-error randomized **adaptive bit-query** decider A for ordinary MCSP, sharing all computations and permitting repeated reads. On a fixed YES x, let G_ρ denote correct output YES and let q_ρ be the number of distinct truth-table indices accessed. If the flip set avoids those indices, the adaptive x and y executions have identical histories and outputs. Averaging y and the coins, the probability of accepting y is at most β_N:=δ+(1-δ)ε_N, so

$$
\mathbb E_\rho[\mathbf1_{G_\rho}H_{N,r}(q_\rho)]
\le\beta_N.
$$

The same conditional Jensen and perspective argument yields, for β_N<1-δ,

$$
\boxed{\mathbb E_\rho q_\rho(x)\ge
(1-\delta)\,h_{N,r}\left(\frac{\beta_N}{1-\delta}\right).}
$$

For fixed δ∈(0,1/2), r=Θ(N^μ)=o(N), ε_N→0 and fixed c≥0, the no-hit probability H(cN/r)→exp(-c). Consequently,

$$
\boxed{\mathbb E_\rho q_\rho(x)\ge
\left((1-\delta)\log\frac{1-\delta}{\delta}-o(1)\right)\frac Nr
=\Omega(N^{1-\mu}).}
$$

This applies separately to every YES table and any shared multi-processor source-bit oracle network **if all original source-input accesses, including preprocessing and input distribution, are charged**. It does not require independently restarted output algorithms. A refined tail bound for H(m)>0 is Pr(q≤m)≤min{1,δ+β_N/H(m)}.

At δ=1/3 the new asymptotic coefficient is 0.4620981204, compared with the earlier 0.4054651081, without improving the sublinear exponent. For N=1,048,576, μ=0.30, K=8, r=504, the finite lower estimate is 960.507586 source-bit probes versus 843.031884 under TMR-5/028's weaker unconditioned Jensen. This is **input ingress**, not post-read work, and it is below N, not the N^1.01 needed in a distinct magnification implication.

## Exact primary-source scope ledger

| Primary publication and location | Variant, model, threshold, exact implication |
| --- | --- |
| Cheraghchi, Hirahara, Myrisiotis, Yoshida, [STACS 2021 Theorem 1, printed 23:3](https://doi.org/10.4230/LIPIcs.STACS.2021.23) | Full truth table N=2^n, **ordinary exact MCSP** with s=2^(μ1 n) for a sufficiently small positive constant μ1; if deterministic one-way read-only input **plus one two-way work tape** fails O(N^1.01) runtime, then **P≠NP**. CONDITIONAL, premise OPEN. |
| Same paper, Theorem 2, printed 23:3 | For a **different larger μ2** close to one, established randomized two-sided error exclusion from BPTIME_1[N^1.99] at ordinary full-table MCSP threshold 2^(μ2 n). KNOWN THEOREM; cannot substitute μ2 for μ1. |
| McKay, Murray, Williams, [STOC 2019 Theorems 1.2-1.3, original accepted PDF pp.2](https://doi.org/10.1145/3313276.3316396) | Full truth-table **search-MCSP with permitted A-oracle gates**, s(n)≥n, one-pass streaming, poly(s) space and update time and explicit oracle/class assumptions. A lower-bound premise would yield P≠NP. CONDITIONAL; not interchangeable with decision MCSP, MKTP, succinct or partial MCSP. |

Publisher STACS original PDF page 23:3 and MMW original accepted PDF pp.2-3 were directly inspected, including page images. No numerical value for μ1 or cross-variant reduction is invented. No ETH, SETH, cryptographic hardness or natural-proofs assumption occurs in EXPECTSPARSE46.

## Original-work audit and hostile controls

* PRIOR TMR-2/031 report: research/agents/tmr-2/2026-11-14_1618_TMR2_RANDOM_SHARED_SPARSE_MINIMAX031.md, original source experiments/tmr/tmr2_shared_sparse_minimax042.js. Fixed maximum query cap, a distinct optimization objective.
* PRIOR TMR-3/031 report: research/agents/tmr-3/2026-11-14_1635_TMR3_SHARP_SPARSE_NETWORK_SOURCE_FRONTIER031.md, original code experiments/tmr/tmr3_sharp_sparse_network043.js and raw results/raw/tmr/2026-11-14_1635_TMR3_SHARP_SPARSE_NETWORK043_RAW.json. Exact circuit-count finite controls inspected.
* PRIOR TMR-5/028 report: research/agents/tmr-5/2026-11-14_1650_TMR5_LOCALHEAD_AND_SPARSE_TAIL_AUDIT028.md, original code experiments/tmr/tmr5_locality_tail_audit044.py and raw results/raw/tmr/2026-11-14_1650_TMR5_LOCALHEAD_TAIL044_RAW.json. Its Jensen bound is valid but is not optimal for variable-length randomized zero transcripts.
* PRIOR Claude ONETAPE original research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex: crossing-sequence transport also bounds nondeterministic restricted one-tape SAT; does not settle P vs NP.
* FALSIFIED/RETIRED Claude direct-product derandomization premise: research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex. No unconditional hitting-set shortcut is inferred.
* PRIOR TMR-5 syntax forcing: research/agents/tmr-5/2026-11-14_1350_TMR5_MCSP_SYNTAX_CERTIFICATE_REVIEW025.md. Opposite-label proper 3-CNF instances can be distinguished cheaply from explicit signs, invalidating a universal oracle-to-SAT transfer.
* PRIOR TMR-4 cubic Walsh moments and failed degree-two quotient: research/agents/tmr-4/2026-11-14_0836_TMR4_MOMENT_CONGRUENCE_AND_QUOTIENT_COUNTEREXAMPLE023.md. Short polynomial summaries may preserve all clause continuation semantics in the specified compiler.
* Historical semantic-composition/Grok control ledger: research/coordination/2026-11-14_0819_USER_CLAUDE_SEMANTIC_COMPOSITION_REVIEW.md.

A syntactically readable pair of contradictory unit-form triples (z∨z∨z) and (¬z∨¬z∨¬z), plus irrelevant padding, refutes any assertion that the number of source assignments forces that many oracle evaluations by a general solver. Horn, 2-SAT, XOR/Gaussian elimination, bounded treewidth, disjoint products, cache/recompute, variable renaming and unlimited input rereads remain hostile controls. The input formula has L bits, unlike an MCSP truth table of N=2^n bits.

## Actually executed, reproducibility and preflight

**Native CPython** executed the exact source at experiments/tmr/tmr2_expected_sparse_query046.py, with immutable original results at results/raw/tmr/2026-11-14_1720_TMR2_EXPECTED_SPARSE_QUERY046_RAW.json. It performed **6,524 assertions, zero failures**, 325 independently solved SciPy HiGHS linear-program optima, 325 matching strategies, and 132,242 exhaustive small support/query-set operations. Seed 2032046. Native code SHA256 078dd6c34da85856e64ed3e8c7bc2319e84595dd955068bc0c71755b5ab36038; raw SHA256 904907837a8d769a1e85a1534ad45daad460988a21086e1cd0073a01262df975. Native script and raw Git blob hashes are d639a6859ecacf1a0ff8827669806a39e0d8d1e8 and ceea4556c40851b341604bd7bdeca6c7a7779dfb. Finite checks are COMPUTATIONAL. No general one-tape physical machine, full compiler, random-bit runtime, or asymptotic SAT solver was executed.

Read FIRST the controlling Nov14 MCSP directive (blob 1e11aa64...), then Nov13 TMR replacement. Reviewed full root proof1.txt (28,714 characters, blob 06f7ebc8...), authentic full proof2.txt blob (1,051,196 characters, 930c5eed...) and canonical root main.tex blob (2,545,859 characters, 6ac34c5d...), AGENTS.md, CODEX.md, repo pnp-research SKILL.md, all five current TMR handoffs, latest issue #3 through TMR-1/031, and original TMR/Claude/Grok material above. Blank contents API bodies of large root files were recovered through Git blob readback, never reconstructed. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root main.tex belongs to TMR-5 synthesis. No root trackers, root manuscript or scheduled tasks changed.

## Open chain and peer-review request

The user's unrestricted target quantifies **one fixed total uniform deterministic multitape 3-SAT decider A across all lengths**, then every k≥1,C>0,L0, and an adversarial encoded valid F of length L≥L0 with T_A(F)>C(L+1)^k. The current theorem lower-bounds only **distinct source-bit probes in an opaque table** with error δ and is consistent with cheap syntax-aware and compact algebraic computation. A lower bound greater than N on actual post-input work for the exact small-μ1 one-work-tape MCSP model remains OPEN; no P≠NP proof exists here.

**Next target:** propose then falsify or verify a fully charged post-ingress computational invariant that remains necessary with explicit formula syntax, arbitrary input rereads, short GF(2)/Walsh summaries, sharing and recomputation. **TMR-5** please audit the conditional Jensen/perspective argument, exact strategy and ε loss; **TMR-3** audit preprocessor/network ingress charges; **TMR-4** check algebraic and syntax-aware escapes; **TMR-1** check μ1/μ2 and conditional proof-chain scope. Keep the unrestricted transfer OPEN.
