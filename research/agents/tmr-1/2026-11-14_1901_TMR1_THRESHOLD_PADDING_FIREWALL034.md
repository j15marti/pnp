# TMR-1/034: MCSP threshold-separation witnesses and the dummy-variable padding exponent firewall

**Date:** November 14, 2026, 19:01 PST (America/Los_Angeles). **Role:** TMR-1 Machine Model Lead. **Claim:** THRESHOLD-PAD050. **Status:** **CANDIDATE/RESTRICTED** pending independent mathematical audit; finite Python checks **COMPUTATIONAL**. **P versus NP remains OPEN**.

## New contribution relative to prior work

TMR-1/032-033 and TMR-3/031 already established sparse-support counting and efficient decoding of high-circuit-complexity truth tables. TMR-5/029 already observed that dummy-variable repetition preserves the exact minimum gate count. **This run combines those separately existing facts to prove a new quantitative firewall for transferring a high-threshold MCSP machine lower bound into CHMY's low-threshold magnification antecedent:**

1. For EVERY fixed `0 < alpha < beta < 1`, the exact ordinary MCSP YES sets at thresholds `floor(N^alpha)` and `floor(N^beta)` differ at the SAME truth-table length `N=2^n` for every sufficiently large `n`. The separating strings can be chosen sparse and have explicit upper circuits of size `O(N^alpha log N)`, but need not be constructible uniformly from `n`.
2. Padding a truth table by dummy variables exactly preserves its gate complexity but enlarges its explicit input length. Under exact exponent matching `a=beta/alpha` (on compatible arities), it gives `N'=N^a`, so **even a hypothetical zero-overhead composition** of an `O((N')^1.01)` low-threshold machine would have source exponent `1.01a`. Such a padding-only argument, based solely on the stated target worst-case time bound, cannot DERIVE a contradiction with a known `N^1.99` high-threshold lower bound when `a > 1.99/1.01 = 199/101`, and materializing the padded table alone costs `Omega(N^a)`. Actual one-work-tape simulation overhead could be larger.

This is a restricted mathematical falsification of an *inference pattern*, not a new 3-SAT or MCSP decision-time lower bound. In particular it does not assert that CHMY's unspecified constants satisfy any numerical ratio.

## Fixed definitions

Write `N=2^n`, and let `CC_n(x)` be the minimum number of gates in an unrestricted-fanout finite Boolean circuit over AND, OR, NOT with fan-in at most two and free inputs/constants computing the complete `N`-bit truth table `x`. Ordinary decision `MCSP[s]` accepts exactly `CC_n(x)<=s`. Its YES class is `Y_mu(N)={x:CC_n(x)<=floor(N^mu)}`; these are NOT the search problem, Gap-MCSP, MKTP or succinct MCSP.

The standard elementary count of functions admitting at most `s` gates is at most
$$
D(n,s)=(s+1)(n+s+2)[3(n+s+2)^2]^s.
$$
The gate convention is fixed throughout. The number `L` of bits encoding an unrelated 3-CNF SAT input plays no role in these truth-table claims.

## Theorem A: strict same-length threshold separation (new combination, peer review OPEN)

For every pair of fixed reals `0<alpha<beta<1` and all sufficiently large integers `n`, there exists an `x_n in {0,1}^N` such that
$$
\lfloor N^\alpha\rfloor < CC_n(x_n)\le \lfloor N^\beta\rfloor.
$$
Hence `Y_alpha(N)` is a PROPER subset of `Y_beta(N)`, for all sufficiently large `N=2^n`.

**Proof.** Fix integer `K>2alpha/(1-alpha)`. Put `s=floor(N^alpha)` and `r=ceil(Ks)`, which is below `N` for large `n`. There are `binom(N,r)` truth tables of Hamming weight exactly `r`. Their count satisfies
$$
\log_2 {N\choose r}\ge r\log_2(N/r)
=(K(1-\alpha)+o(1))sn,
$$
whereas
$$
\log_2 D(n,s)\le (2\alpha+o(1))sn.
$$
The strict choice of `K` therefore guarantees some `r`-sparse `x_n` with `CC_n(x_n)>s`.

Every `r`-sparse function is the OR of its `r` exact-assignment minterms. Share the at most `n` input negations, use `r(n-1)` AND gates to build minterms, and `r-1` OR gates to combine them. For `r>=1`,
$$
CC_n(x_n)\le n+rn-1=O(N^\alpha\log N)=o(N^\beta).
$$
Thus eventually `CC_n(x_n)<=floor(N^beta)`. Both labels at the two parameters have been proved for the *same* table and the same gate basis. QED.

**Falsified implication:** A known high-threshold lower bound cannot be relabeled as a low-threshold lower bound on the same `N` by claiming monotonicity. The sets have distinct membership labels, even though `Y_alpha subset Y_beta`.

## Theorem B: exact dummy-variable padding and quantitative cost (known equality, new threshold audit)

Let `n' >= n` and define `P_{n,n'}(x)` as the truth table of `g(z_1,...,z_{n'-n},u_1,...,u_n)=f(u_1,...,u_n)`. Under lexicographic order with the dummy arguments first, the table simply repeats `x` exactly `2^{n'-n}` times. Then
$$
CC_{n'}(P_{n,n'}(x))=CC_n(x).
$$
**Proof:** The circuit for `f` ignores the dummy inputs, showing `<=`. Conversely, fixing the dummy wires to zero in any circuit for `g` and propagating constants cannot increase its number of gates, showing `>=`. Both claims use the same circuit basis.

Fix threshold exponents `beta>alpha>0` and suppose `a=beta/alpha` is rational and the source arities are restricted to infinitely many `n` for which `n'=an` is an integer. Then `N'=2^{n'}=N^a` and
$$
\lfloor (N')^\alpha\rfloor=\lfloor N^\beta\rfloor.
$$
Consequently, on these *compatible lengths* there is an **exact many-one reduction** from the beta-threshold decision problem to the alpha-threshold decision problem by explicit truth-table repetition. It writes `N'` bits, so incurs `Omega(N')=Omega(N^a)` output work (and can be implemented in polynomial `N'` time). This is a polynomial-time reduction in the *source truth-table length* `N`, NOT a near-linear model-preserving reduction between CHMY one-work-tape decision machines. For incompatible lengths, rounding `n'` shifts thresholds and **requires a separate promise/threshold argument**; none is asserted here.

If a low-alpha decider on `N'` input uses `O((N')^{1.01})` time, then the arithmetic cost of **even the idealized** padding-plus-decider composition is `O(N^{a}+N^{1.01a})=O(N^{1.01a})`. To conflict with exclusion from `DTIME_1[N^{1.99}]` this would need `1.01a<=1.99` in the no-overhead fiction; at equality `a=199/101` an ideal exact `O(N^1.99)` composition would itself contradict the cited lower bound, but any polylogarithmic or larger simulation overhead can defeat that edge case. Exact same-model costs must be proved. For `a>199/101`, that black-box target worst-case bound alone is too weak to derive a contradiction from the known 1.99 exclusion. A different algorithm exploiting the restricted image of the padding map could conceivably run faster; none is supplied. This is a **firewall on this specific padded composition**, not a theorem forbidding other reductions. The contrapositive must not be claimed as an actual one-tape hardness transfer: materializing, buffering, repeating source access and simulating a one-work-tape target while retaining the source on a single work tape can add cost.

## Primary-source theorem matrix and exact remaining arrow

| Source and location | Input / problem, threshold / promise | Exact model and result | Relation |
| --- | --- | --- | --- |
| Cheraghchi, Hirahara, Myrisiotis, Yoshida, **STACS 2021 Theorem 1, p. 23:3** (publisher DOI 10.4230/LIPIcs.STACS.2021.23) | Ordinary exact MCSP, full `N=2^n` truth table, `s(n)=2^(mu_1 n)` for an existential small fixed `mu_1>0` | Uniform deterministic TM with **one one-way read-only input tape and one two-way writable work tape**; conditional: `MCSP[s] notin DTIME_1[N^1.01] => P!=NP`. Neither endpoint has been established by this project. | **OPEN** low-threshold superlinear decision lower bound. |
| Same, **Theorem 2, p. 23:3** | Ordinary exact MCSP, full `N=2^n` table, `s(n)=2^(mu_2 n)` for some larger `mu_2` close to 1 | Randomized two-sided error, one-way read-only input plus one work tape; **KNOWN** `MCSP[s] notin BPTIME_1[N^1.99]`. | Does not fulfill Thm 1 because `mu_2` differs from `mu_1`; deterministic 1.99 exclusion follows only at its own threshold. |
| McKay, Murray, Williams, **STOC 2019 Theorems 1.2-1.3**, author accepted PDF pp. 2-3 | Search-MCSP with oracle gates, explicit `N=2^n` input and size `s(n)>=n` | Efficient one-pass streaming synthesis using short `Sigma_3 SAT^A` oracle calls, and conditional nonexistence of a suitable `poly(s)`-space/update search streamer implies `P!=NP` for an appropriate `A in PH`. | SEARCH, oracle and threshold assumptions cannot be silently replaced with this report's ordinary decision padding. |
| TMR-1/032 and earlier circuit-counting argument, original report path below | Exact ordinary MCSP and `r`-sparse full tables; nonuniform circuits | Combinatorial `D(n,s)` count; no uniform hard-table finder | Used in Theorem A, without claiming discovery of circuit counting. |

**Primary original:** https://drops.dagstuhl.de/storage/00lipics/lipics-vol187-stacs2021/LIPIcs.STACS.2021.23/LIPIcs.STACS.2021.23.pdf; printed p. 23:3 inspected as an image. MMW accepted author paper: https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf . Oliveira, Pich, Santhanam and Chen et al. locality-barrier literature concerns additional models and variants, with no theorem imported into A/B. The latter's metadata can be found at https://arxiv.org/abs/1911.08297. Do not transfer MCSP to Gap-MCSP, partial/succinct MCSP, or MKTP without a specified proven reduction.

## Original project evidence, controls and limitations

| Original path | Authentic scope / status |
| --- | --- |
| `research/agents/tmr-1/2026-11-14_1805_TMR1_SPARSE_NO_BOUNDARY032.md` and its `experiments/tmr/tmr1_sparse_frontier048.py` / raw | Previous sparse count and indexed/generator equality-boundary; **CANDIDATE/RESTRICTED**, counting ingredient reused. |
| `research/agents/tmr-1/2026-11-14_1810_TMR1_LINEAR_SPARSE_STREAM_DECODER033.md` and original code/raw | Prior one-work-tape-with-extra-output-port `O(N)` sparse decoder; **CANDIDATE/RESTRICTED**, independent review OPEN. Not used as a machine-model theorem here. |
| `research/agents/tmr-5/2026-11-14_1750_TMR5_POLYREPEAT_STREAMING_AMORTIZATION_AUDIT029.md` | Previous exact dummy-variable gate-preservation and output sharing; **CANDIDATE/RESTRICTED**, equality independently rederived. |
| `research/main/2026-10-19_1748_MAIN_SPARSE_COSPARSE_ESCAPE1.tex` | Earlier sparse/co-sparse minterm compiler, not general search-MCSP hardness. |
| `research/agents/tmr-4/2026-11-14_1838_TMR4_GLOBAL_ORACLE_SHARED_TRACE_BARRIER034.md` and `research/agents/tmr-5/2026-11-14_1850_TMR5_NETWORK_WORK_DEPTH_ORACLE_AUDIT030.md` | Oracle-only global shared query/work-depth lower bounds; syntax-aware proper 3-CNF control falsifies unrestricted transfer. |
| `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` and `research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex` | Historical physical-head/portfolio limitations, not cross-threshold MCSP decision theorems. |
| Original LSPV/Grok/Walsh and checker counterexamples | Compact algebra, cached computation and genuine cheap accepted runs remain permitted. Neither A nor B assumes all 3-SAT solvers enumerate assignments, materialize sparse descriptions, or use a fixed proof calculus. |

## Executed finite controls and publication

Exact native Python 3 file: `experiments/tmr/tmr1_threshold_padding_audit050.py`; raw output: `results/raw/tmr/2026-11-14_1901_TMR1_THRESHOLD_PAD050_RAW.json`. **1,642 assertions, zero failures**. All 16 two-input and 256 three-input truth tables had unchanged <=1/<=2-gate membership under one-dummy-variable repetition. Two-input NAND has gate cost exactly 2, separating thresholds 1 and 2, and its four-arity padding matches the high threshold with low parameter. Exhaustive small support minterm evaluations and exact numerical asymptotic margins at `n=16,24,32,40,48,64,80` passed. Numeric tests never prove the asymptotic theorem or a finite-state TM implementation. No physical one-work-tape simulator, full test suite or LaTeX compilation was run.

Preflight: read controlling Nov. 14 MCSP directive first, Nov. 13 TMR replacement, AGENTS.md, CODEX.md, repository skill, all five latest TMR handoffs, issue #3 through TMR-5/030, original TMR-1/032-033, TMR-4/034, TMR-5/029, older sparse/Claude and the original CHMY theorem image. Both full proof trackers recovered, including the authentic 1,051,196-character `proof2.txt` Git blob `930c5eeddafce656717f28055a7a9a755f44737c`; `proof1.txt` blob `06f7ebc8c2283304a0f5200b518c6e48fa41e343`, 28,714 characters; canonical `main.tex` authentic Git blob `6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34`, 2,545,859 characters. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root main.tex is TMR-5-owned; not modified. Existing tasks and schedules untouched.

**One next target / peer-review request:** TMR-5 independently verify the strict-inclusion counting proof and high/low threshold inequality; TMR-3 audit whether ANY explicit padding can preserve the CHMY `DTIME_1` one-work-tape exponent; TMR-4 test a genuinely syntax-aware both-label reduction that avoids simple output replication and respects thresholds; TMR-2 test whether a decision certificate yields more than input-length work. The weakest unresolved load-bearing arrow remains an `N^1.01` decision-time exclusion for ordinary MCSP at the specific small parameter of CHMY Theorem 1, with a valid one-work-tape model transfer.

**P versus NP remains OPEN.**
