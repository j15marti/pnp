# TMR-1/024: Exact dummy-variable circuit-size identity and MCSP threshold-transfer corridor

**Pacific time:** November 14, 2026, 10:10 PST. **Owner:** TMR-1 Machine Model Lead. **Status:** CANDIDATE/RESTRICTED symbolic result pending TMR-5 independent audit; finite tests COMPUTATIONAL. **P versus NP remains OPEN.** No scheduled task was altered.

## Preflight, historical ledger, and novelty

Read FIRST the newest [MCSP five-agent directive](https://github.com/j15marti/pnp/blob/main/research/coordination/2026-11-14_MCSP_FIVE_AGENT_REVIEW.md), blob 1e11aa64a0b0d635a65cea58500b09f2b0fe010a, then the November 13 TMR replacement directive, issue #3 through TMR-5/021, both complete proof trackers, authentic full canonical main.tex, AGENTS.md, CODEX.md, pnp-research skill and all five current TMR handoffs. The contents API incorrectly returned blank bodies for proof2 and main.tex; exact Git blob recovery gave 1,051,196 and 2,545,859 characters. Root proof1 is 28,714 characters. No root writes.

The generic warning that padding erodes exponents was ALREADY established in research/main/2026-10-18_ASYMPTOTIC_CONE5.md and research/agents/magnification-redteam/2026-10-18_1137_MAGRED_PROMISESLOPE1.tex. This run adds a precise arbitrary-function **circuit-minimum equality**, an exact both-label normalization for matching integer thresholds, the input-output materialization cutoff, a quantified **199/101** composition corridor in the published CHMY exponent regime, and an explicit CHMY Theorem 3 arbitrary-oracle short-query exclusion. This is a sharper scoped consistency test, not a claim that padding is a new proof technique.

Original evidence retained:

| Original path | Verified scope, not overpromoted |
|---|---|
| research/main/2026-10-18_ASYMPTOTIC_CONE5.md | PRIOR conditional cofinal exponent slope criterion; simple padding loses lower-bound margin |
| research/agents/magnification-redteam/2026-10-18_1137_MAGRED_PROMISESLOPE1.tex | PRIOR exponent erosion and Gap-MCSP promise failure |
| research/agents/threshold-descent/2026-10-18_1204_THRES_ENTROPY1.tex | Restricted representation-counting barrier, not universal reduction impossibility |
| research/agents/magnification-redteam/2026-10-18_1919_MAGRED_STREAM_NO10.md | Actual all-label sampling failure; preserve counterexamples |
| research/agents/threshold-descent/2026-10-30_0919_ROUTE1_AFFINE_SMALLBIAS_DESCENT_GATE2.md | Fixed affine/field-mask descent failure; nonlinear mappings not excluded |
| research/agents/tmr-1/2026-11-14_0908_TMR1_MCSP_PARAMETER_SHELL023.md | Previous circuit-size intermediate-shell counting, used only for fixed exponent gaps |
| research/agents/tmr-2/2026-11-14_0927_TMR2_MCSP_RESIDUAL_WIDTH024.md | Nonuniform prefix residual width ceiling, not fast uniform transitions |
| research/agents/tmr-3/2026-11-14_0936_TMR3_MCSP_FIXED_NETWORK_SERIALIZATION024.md | Fixed-network quadratic one-work-tape simulation, limited source interface |
| research/agents/tmr-4/2026-11-14_0943_TMR4_MCSP_SAT_TRUTHSHELL_FALSIFIER024.md | CNF satisfaction-table image stays ordinary-MCSP YES at a fixed positive exponent; independently checked elementary AND/OR/NOT upper bound |
| research/agents/tmr-5/2026-11-14_0953_TMR5_MCSP_TWO_STATE_UNIFORMIZATION_REVIEW021.md | Diagonal decidable language, nonuniform OBDD width 2 but not in P, not an MCSP bound |
| research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex, 2026-10-28_1326_CLAUDE_TPORT-0001.tex, 2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex | Restricted transport, proof-calculus and direct-product controls; no unrestricted SAT transfer |

## Exact primary theorem matrix

The **original** STACS 2021 19-page CHMY PDF was examined on printed pp. 23:3–23:4, Theorems 1–3. The original McKay–Murray–Williams STOC 2019 PDF was examined on pp. 1–2, Theorems 1.2–1.3. Their assumptions must not be mixed.

| Primary statement | Full input, model, parameter | Hypothesis or conclusion |
|---|---|---|
| CHMY [1], Thm. 1, p. 23:3 | Decision MCSP[2^(mu_l n)], full N=2^n-bit truth table, **deterministic one-way read-only input + one two-way work tape** | There exists a *small* fixed mu_l>0 for which exclusion from DTIME_1[N^1.01] implies **P != NP**. The precise small constant is not established by our padding experiment |
| CHMY [1], Thm. 2, p. 23:3 | Decision MCSP[2^(mu_h n)], full N-bit truth table, **randomized two-sided error**, same input/work tape interface; some different mu_h close to 1 | Unconditionally **not** in BPTIME_1[N^1.99]. It is a different language than the small-threshold magnification input |
| CHMY [1], Thm. 3, p. 23:4 | For each mu in (1/2,1), MCSP[N^mu], one-work-tape/one-way input, any oracle O, query strings N^o(1) | Some delta(mu)>0 excludes BPTIME_1^O[N^(1+delta(mu))]. Not a barrier to polynomial-size queries |
| McKay–Murray–Williams [2], Thm. 1.2, p. 2 | **Search-MCSP^A**, N-bit one-pass truth table; time-constructible s(n)>=n, oracle Sigma_3SAT^A | Oracle algorithm with total time N times ~O(s), ~O(s^2) update, ~O(s) work space, short oracle queries. No free oracle elimination |
| MMW [2], Thm. 1.3, p. 2 | Uniform one-pass **search**-MCSP^A for some A in PH, s(n)>=n | Proving inability to have **both** poly(s) update and poly(s) workspace implies **P != NP** |
| Oliveira–Santhanam [3], ECCC TR18-139 (2018) | MCSP[2^sqrt(n)] average-case formula and separate approximate promise-MCSP settings | Corresponding lower bounds imply NP lacks polynomial formulas or NP not in BPP, not the same model/conclusion |
| Chen et al. [4], ECCC TR19-168 (2019), ITCS 2020 | Magnification/locality with small oracle gates in certain circuit models | A barrier for specified proof techniques, not a blanket impossibility result |

Primary sources: [1] https://doi.org/10.4230/LIPIcs.STACS.2021.23 ; [2] https://doi.org/10.1145/3313276.3316396 ; [3] https://eccc.weizmann.ac.il/report/2018/139/ ; [4] https://eccc.weizmann.ac.il/report/2019/168/ . Ordinary, Gap-, partial, succinct, and search-MCSP, plus MKTP, are distinct unless a fully proved reduction connects them.

## Theorem PAD24-A: exact ignored-variable circuit complexity

Fix the AND/OR/NOT basis (binary AND/OR, unary NOT), unrestricted fanout, with constants 0 and 1 and input wires free, gates charged. Define f on n bits and E_t f on n+t bits by ignoring the final t input bits:

$$
E_t f(x_1,\ldots,x_n,z_1,\ldots,z_t)=f(x_1,\ldots,x_n).
$$

**CANDIDATE/RESTRICTED elementary theorem**, with full proof:

$$
\boxed{\mathrm{CC}_{n+t}(E_t f)=\mathrm{CC}_n(f)}
$$

for every Boolean f, n>=1 and integer t>=0.

**Upper bound:** Any size-s circuit computing f computes E_t f with the same s gates by ignoring z. **Lower bound:** Take a smallest circuit computing E_t f. Fix every z_i=0, propagate constants topologically, and remove any gate which becomes constant or forwards an existing wire. Constant wires are free, so no new gate is needed. The remaining circuit computes f with at most the original gate count. Both inequalities give equality. This is an exact **basis-scoped circuit** fact, not a physical SAT time lower bound.

If the explicit truth-table ordering puts dummy variables last, then each source table bit repeats 2^t times. Thus the target explicit input length is

$$
M=2^{n+t}=N\,2^t=N^{\rho_n},\qquad N=2^n,\quad \rho_n=1+t/n.
$$

## Theorem PAD24-B: exact threshold preservation and the rounding warning

Let high threshold s_h(n)=floor(2^(mu_h n)) and low threshold s_l(n+t)=floor(2^(mu_l(n+t))). If these **integer thresholds are equal at that n**, then PAD24-A proves, for every full source f:

$$
\mathrm{TT}(f)\in\mathrm{MCSP}[s_h]
\quad\Longleftrightarrow\quad
\mathrm{TT}(E_t f)\in\mathrm{MCSP}[s_l].
$$

This genuinely preserves both labels at that length. For mu_h=3/4, mu_l=1/4 and t=2n, thresholds are exactly identical for **every n**, including floors, but M=N^3. For mu_h=4/5, mu_l=2/5 and t=n, M=N^2. These pairs are **arithmetic illustrations only**, not an assertion that the constants in CHMY Theorems 1 and 2 equal these numbers.

If mu_l*(n+t)/n differs from mu_h by a **fixed positive exponent margin** and both exponents are in (0,1), TMR-1/023's existing strict-shell theorem supplies source functions on which ordinary MCSP labels disagree. When thresholds differ only by O(1) integer gate counts, the same theorem does **not** establish a witness at every missing gate count. Thus rounding t without checking actual thresholds is not enough. A length subsequence alone is not a reduction for the full uniform all-length decision language.

## Theorem PAD24-C: fully charged explicit materialization and exponent corridor

Any finite-alphabet algorithm that physically writes an explicit M-bit target must perform at least M output-write transitions even when f is an easy constant function:

$$
T_{\rm materialize}(N)\ge M=N^{\rho_n}.
$$

This applies **only to output materialization**. A virtual target stream needs its own all-input, one-way/one-work-tape simulation proof and must charge all source reads, buffering, repeated bits, state changes, communication and output; it is not an automatically free extra input tape.

Assume **conditionally** a low-parameter solver using at most O(M^a) transitions on every target input and a completely compatible reduction/simulation using at most O(N^b) transitions. The generic worst-case bound is at most O(N^b+N^(a*rho)). With the exact CHMY exponents a=1.01 and the high-hard threshold 1.99, a **strict slack** generic transfer needs

$$
b<1.99,\qquad \rho<\frac{1.99}{1.01}=\frac{199}{101}\approx1.970297.
$$

If rho>1.99, physical materialization **alone** exceeds the relevant source time. If 199/101<rho<=1.99, the bare O(M^1.01) worst-case upper bound does not deliver a contradiction, although the solver might execute faster on a special padded image. Rho=3 gives solver exponent 3.03 and output exponent 3; rho=2 gives 2.02 and output 2; rho=1.5 gives 1.515. The latter arithmetic does **not** establish an actual reduction at CHMY's unknown constants. At equality check the actual O bound, polylogs, model and tape interface rather than imposing strict inequalities as necessary conditions.

This refines, rather than supersedes, the PRIOR padding-slope analysis from October.

## Corollary PAD24-D: already-published short-query exclusion

This is an **explicit specialization of CHMY Theorem 3**, not a new theorem of comparable significance. Fix any mu_h in (1/2,1) and its positive delta(mu_h). An alleged N^(1+delta(mu_h))-time one-way-input/one-work-tape algorithm for high-threshold MCSP that asks **only N^o(1)-bit oracle questions** is prohibited, even if the oracle is a low-threshold MCSP language. Theorem 3 quantifies over **arbitrary** oracles O. Consequently, a near-linear Turing threshold descent using only subpolynomial-length low-MCSP requests is already excluded in that exact model.

**No claim** is made about an N^epsilon-length query for fixed epsilon>0, a non-oracle nonlinear reduction, a different model, or time above the published bound. This and the explicit-output corridor leave a large OPEN middle.

## Executed native computational controls

A newly authored native CPython reproducer, experiments/tmr/tmr1_mcsp_padding024.py, exhaustively enumerates functionally distinct topological AND/OR/NOT gate outputs at the stated budgets, preserving all future reachable functions when duplicate syntactic gates merge.

| Input arity + dummy bits; max gates | Full source truth tables checked | Mismatched minimum-size-or-over-budget class |
|---|---:|---:|
| 1 + 1; 3 | 4 | 0 |
| 2 + 1; 3 | 16 | 0 |
| 3 + 1; 2 | 256 | 0 |
| **Total** | **276** | **0** |

It also checked exact arithmetic fixtures at rho=3, 2, 1.5 with thresholds matched on the selected lengths, no failures. In the two-input, <=3-gate AND/OR/NOT basis control, XOR is not falsely claimed small. Native execution was a short standalone CPython chunk. All finite evidence is **COMPUTATIONAL**. No arbitrary Turing machine, simulator correctness proof, CHMY experiment, other tool's code replay or general SAT decider was executed. The published raw fixture data and executable permit reproduction.

Cheap adversarial classes retained: Horn, 2-SAT, GF(2)/XOR elimination, bounded-treewidth DP, signed-moment summaries, products, sharing, padding, renaming, auxiliary variables, caching and recomputation. They are **not** falsely counted as executed by this script.

## Integrated dependency graph and single next target

**KNOWN** CHMY large-threshold randomized one-work-tape N^1.99 lower bound.

**OPEN arrow A:** genuinely prove low-threshold deterministic one-work-tape N^1.01 exclusion at the small mu_l furnished by CHMY Thm. 1. Then, via the published theorem, P != NP.

**OPEN arrow B:** construct an all-label, all-length, source-dependent **high-to-low** reduction whose target lengths, threshold integers, physical input interface and tape transitions satisfy the actual exponent budget. PAD24-A/B prove an ignored-variable mapping can preserve semantics, but PAD24-C shows why this alone has not transferred the published hard bound. No arbitrary reduction impossibility has been proved.

**OPEN arrow C:** alternatively prove the exact MMW search-MCSP^A one-pass impossibility with **simultaneously** poly(s) memory and poly(s) update, retaining PH oracle and search semantics. A prefix count alone does not suffice.

For arbitrary SAT, the team must still reach the fixed-uniform-decider all-exponent target: for each correct finite total multitape A, each integer k>=1, C>0 and L0, some valid F of encoded bit length |F|>=L0 has T_A(F)>C(|F|+1)^k. Neither a restricted one-tape result nor PAD24 alone is that lower bound. A legitimate general polynomial SAT algorithm would also be a valid alternative end result.

**Next TMR-1 target:** design and try to falsify one non-padding threshold transfer with explicit parameters mu_h, mu_l, rho, exact integer gate thresholds, output realization and source model. **Peer requests:** TMR-4 propose source-sensitive mapping and both-label hostile cases; TMR-3 validate physical one-way input/one-work-tape composition; TMR-2 investigate short-query and compact-summary escapes; **TMR-5 independently check PAD24-A/B, all-length rounding and the 199/101 generic-bound wording** before any proof promotion.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Canonical main.tex reserved for TMR-5; P=NP and P!=NP OPEN.

END_OF_REPORT::TMR1::024::2026-11-14_1010_PST
