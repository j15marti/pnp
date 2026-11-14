# TMR-3/026: Length-oblivious one-way MCSP padding forces linear source retention

**Date:** November 14, 2026, 11:30 PST (America/Los_Angeles). **Role:** TMR-3 Time-Space Tradeoffs. **New claim LENGTHBLIND26:** elementary **CANDIDATE/RESTRICTED** symbolic theorem, independent TMR-1/TMR-5 review OPEN. Finite V8 and independent native CPython checks are **COMPUTATIONAL**. Neither ordinary MCSP hardness nor P versus NP is resolved. No schedules modified.

## 1. What is genuinely new

TMR-1/024 proved that adding ignored circuit variables preserves *minimum gate count* at the **same integer threshold**; TMR-1/025 extended the identity to normalized approximation distance. TMR-4/026 and TMR-5/022 proved one-way, append-only-output memory frontiers for **fixed-length truth-table coordinate permutations**. TMR-3/025 simulated a polynomial-processor ring through explicit physical source/port charges. This run proves a DIFFERENT frontier: even the *identity-order, contiguous-repetition* padding operation requires linear source retention **when the amount of padding depends on an unknown source length and the original input head is irreversible**. This is an *interlength prefix ambiguity* theorem, not a permutation argument or a time lower bound.

### Exact input and output model

Fix one total deterministic, uniform, finite-control transducer D, over **all** binary source lengths N=2^n with n>=2. It has one one-way, locally moving, read-only source tape initially positioned at its first bit and with an endmarker after the last bit; w>=1 fixed locally moving two-way writable work tapes of fixed alphabet size G>=2; q fixed control states; and a **write-only, ordered append-only binary output** whose prior contents cannot be reread or used as scratch. One transition can read/advance source, move/write work heads, and append at most one output bit. All these steps and all visited work cells are paid. The machine is **not** initially handed n or N as advice, a header, or an external clock. It must emit the entire specified output and halt correctly for every admissible truth table at every allowed length.

The output is the ignored-low-variable extension

$$
E_{t(n)}(x)=x_0^{R_n}x_1^{R_n}\cdots x_{N-1}^{R_n},
\qquad R_n=2^{t(n)}, \quad M=N R_n=2^{n+t(n)}.
$$

The notation x_i^{R_n} means the bit x_i repeated consecutively R_n times. This is the standard lexicographic truth table for the Boolean function g(u,z)=f(u), with t dummy variables z in the **low-order assignment-index coordinates**. Consequently, in the fixed fan-in-two AND/OR/NOT circuit basis with free constants and size counting gates, CC(g)=CC(f), as already established in TMR-1/024. **This does not map unequal circuit-size thresholds unless their actual integer values match.**

Let S_D(N) be the *maximum*, over all valid N-bit sources, of the number of distinct writable work cells visited over all work tapes during the entire actual run. The same D is used at all lengths.

## 2. New LENGTHBLIND26 theorem

Assume that for every sufficiently large n there is some n'>n with R_{n'}>R_n; in particular, t(n)=ceil(a n) for any fixed a>0 satisfies this condition. Then every such correct D obeys, at every such N=2^n,

$$
\boxed{
2^{N-2}\le (R_n+1)\,q\,(2S_D(N)+3)^{3w}\,G^{S_D(N)}.
}
$$

If t(n)=O(n), so R_n=N^{O(1)}, this implies

$$
\boxed{
S_D(N)=\Omega(N).
}
$$

More precisely, for a fixed G>=2 and w,q and sufficiently large N, the inequality gives

$$
S_D(N)\ge (1/\log_2 G-o(1))\,N
$$

unless S_D(N)>N already, in which case the bound is automatic. The leading coefficient is only a counting consequence of the particular work-cell convention; no optimal machine construction is claimed.

### Proof

Fix n and any n'>n with R_{n'}>R_n. Consider all 2^{N-2} short source tables

$$
x=01v,\qquad v\in\{0,1\}^{N-2}.
$$

For each such x, choose any longer source table x'=x0^{2^{n'}-N}; these share **exactly the first N source symbols**. Before D first scans the physical short-source endmarker at position N, the runs on x and x' are identical, because a fixed deterministic one-way-input machine has received exactly the same source observations. The outputs, however, diverge at position R_n+1 in one-based output indexing: E_{t(n)}(x) has a 1 there (the second source bit), while E_{t(n')}(x') has a 0 there (still a repetition of the first source bit). Therefore by the instant immediately before the first read of the short-source endmarker, D has emitted **at most R_n zeros**. It cannot halt before detecting the endmarker either, because the longer continuation would then force an incorrect output length.

At that cut, the source head is at the fixed position N. The emitted write-only prefix is fully specified by its length e in {0,...,R_n}; it contains no information other than e and zeros. Distinct values of v MUST induce distinct pairs (e, complete finite control plus all writable-work configurations), for if two v values gave the same pair, then after observing the identical endmarker both runs would perform identical future transitions and emit the same future output, contradicting the fact that E_{t(n)}(01v) is injective in v.

For each work tape, a locally moving head has visited a contiguous region beginning at its fixed origin, and every current head coordinate belongs to that visited region. With at most S total distinct visited cells, q finite-control states and G work symbols, the number of possible complete work configurations is bounded conservatively by

$$
q(2S+3)^{3w}G^S.
$$

Multiplying by the R_n+1 possible emitted-prefix lengths proves the displayed injection inequality. If R_n=N^{O(1)}, taking logarithms gives N-2 <= log_2(R_n+1)+log_2 q+3w log_2(2S+3)+S log_2 G. For S<=N the first three terms are O(log N); hence S>=N/log_2G-O(log N). If S>N the result is immediate. QED, conditional only on the stated exact physical interface.

## 3. Genuine cheap controls, exact scope of the conclusion

**Fixed padding amount:** If t is a fixed integer independent of source length, one finite transducer can read each bit once and output 2^t copies in finite control, using O(1) writable cells. There is no interlength output divergence. Thus arbitrary repetition does NOT itself force linear work.

**Known n supplied before the table:** A uniform one-work-tape producer can parse a genuine length header, compute R_n, park the input head on the current source bit, and reuse one binary repetition counter, with O(t(n)+log n) visited work cells and at most O(M(t(n)+1)+poly(n)) charged steps. The length header changes the original source interface and must not be imported free into the CHMY model.

**Two-way read-only source:** Without a length header, a transducer can first count source length using O(log N) work cells, rewind the input head, and then stream the output with a binary repetition counter. The one-way lower bound no longer applies. This escape is computationally charged and is not an unconditional SAT algorithm.

**Unrestricted workspace:** Even on the original one-way source interface, a transducer may cache all N bits on its work tape, learn the length, and subsequently generate the entire output. Therefore the theorem excludes *small-space online padding* but does NOT prove a superpolynomial time requirement for padding, much less for arbitrary MCSP deciders.

**Output storage:** The bound assumes a non-readable append-only output; if the output can be reread or rewritten as arbitrary free scratch, it becomes part of writable memory and must be charged. Likewise a preprovided input length, nonuniform per-N program, rewindable input, random indexed port, or uncharged external processor violates a hypothesis. The theorem remains true for any fixed number w of work tapes with a fixed finite alphabet, not a growing processor count without a new accounting theorem.

## 4. Quantitative hardness-magnification firewall

For ordinary MCSP at truth-table length N=2^n and circuit gate threshold s_H approx N^{mu_H}, dummy-variable padding with M=2^{n+t}=N^{rho+o(1)} preserves the integer minimum gate count but only aligns the low threshold s_L approx M^{mu_L} when mu_H=rho mu_L, up to exact threshold rounding. This is PRIOR TMR-1/024 arithmetic; the new result adds the previously missing **interlength streaming-memory** requirement for a length-blind one-way generator.

CHMY, STACS 2021 Theorem 1 (p.23:3): for some sufficiently small constant mu_1>0, excluding deterministic one-work-tape, one-way-read-only-input O(N^{1.01}) time for ordinary MCSP[2^{mu_1 n}] implies P!=NP. Theorem 2 on the same input/work interface excludes two-sided-error randomized O(N^{1.99}) time for MCSP[2^{mu_2 n}] at a **larger** fixed mu_2 close to one. This source/target threshold gap is OPEN; theorem 2 alone does not instantiate theorem 1.

Even if an O(M^{1.01}) *low-threshold* decider and a matching reduction could be sequentially composed in this exact physical model with no additional overhead, the resulting source time guarantee includes N^{1.01rho+o(1)}. To contradict the high-threshold N^{1.99} exclusion by that composition, a necessary exponent slack for this **certified upper-bound scheme** is

$$
1.01\rho<1.99,\quad\text{equivalently}\quad \rho<199/101\approx1.970297.
$$

This is not a theorem that all other reductions or simulators must obey this exponent; and the actual one-tape producer/solver composition may cost MORE. The new Omega(N) padding-workspace cost alone does not imply the missing runtime lower bound.

MMW, STOC 2019 Theorems 1.2 and 1.3, concern **oracle-assisted full search-MCSP** with one-pass poly(s) workspace **and** poly(s) update time; they do not directly lower-bound an ordinary decision MCSP padding transducer. Their oracle costs and query lengths cannot be silently imported. No Gap-MCSP, MKTP, partial or succinct variant was conflated.

## 5. Independent execution and falsification controls

**Actually executed standalone published JS via hosted V8**: experiments/tmr/tmr3_length_blind_padding026.cjs. Exhaustively checked source lengths N=4,8,16 with n'=n+2 and t(n)=ceil(n/2); 16,452 different suffix tables x=01v, 32,904 independently generated short/long padded output strings, exact first divergent bit at R_n+1, and 16,452 distinct post-cut suffixes. Also ran 65,808 fixed-t all-truth-table streaming-positive controls for n=2,3,4. All assertions passed. The full raw structured output is results/raw/tmr/2026-11-14_1130_TMR3_LENGTH_BLIND_PADDING026_V8_RAW.json.

**Separately executed native CPython independent construction, local only**: 16,452 ambiguity cases, 32,904 generated source/extension comparisons, 816 bounded-circuit both-label checks (n=2,3, thresholds 0..2 and t=1), 65,808 fixed-t controls, zero failures in 0.718 seconds. Python script SHA256 cfca3cf85104637f77ca90ad8567eac048478f64c0a9f069977f998043248d44; local raw SHA256 d6811b11de023e984cf3a71e7e84126cb3140599cd48b2005d0e3cfe0d6e3565. These native Python files are **not** claimed as GitHub publications. No native OS Node, physical finite-alphabet transducer compiler, TeX compilation or repository CI was executed. Finite checks remain COMPUTATIONAL, independent of the asymptotic proof.

Cheap-family controls: algebraic GF(2) and Walsh summaries, Horn/2-SAT, bounded-treewidth dynamic programming, products, shared computation, reordering, padding/renaming and recomputation are still legal for general SAT algorithms. Their correctness/performance was NOT tested in this finite output-transducer experiment. No universal SAT lower bound is inferred from the forced buffering of a chosen output representation.

## 6. Previous evidence ledger and exact next review

| Original file or source | Scope in the present argument |
|---|---|
| research/agents/tmr-1/2026-11-14_1010_TMR1_MCSP_EXACT_PADDING_EXPONENT_FIREWALL024.md | PRIOR gate-minimum identity, both-label matching-integer-threshold padding, exponent corridor |
| research/agents/tmr-1/2026-11-14_1110_TMR1_MCSP_APPROXIMATION_PADDING_UNIFORM_MAGNIFICATION025.md | PRIOR normalized approximation-gap identity; distinct promise and conclusion |
| research/agents/tmr-4/2026-11-14_1039_TMR4_MCSP_PERMUTATION_STREAMING_BUFFER026.md | PRIOR fixed-N input/output permutation memory obstruction |
| research/agents/tmr-5/2026-11-14_1050_TMR5_GENERAL_MCSP_PERMUTATION_FRONTIER_AUDIT022.md | PRIOR all-cuts permutation frontier, independent review of TMR-4 |
| research/agents/tmr-3/2026-11-14_1028_TMR3_MCSP_POLY_RING_SERIALIZATION025.md | PRIOR uniform growing-processor network with exact charged round simulation, not this transducer |
| research/main/2026-10-18_ASYMPTOTIC_CONE5.md | PRIOR cofinal slope conditional; no low-threshold lower bound proved |
| research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex | PRIOR one-tape crossing/sequential access lower bounds; no unrestricted SAT transfer |
| CHMY, *One-Tape Turing Machine and Branching Program Lower Bounds for MCSP*, STACS 2021, Theorems 1,2, p.23:3, https://doi.org/10.4230/LIPIcs.STACS.2021.23 | Original N=2^n ordinary decision MCSP one-way-input/one-work-tape model, different circuit thresholds |
| McKay, Murray, Williams, *Weak Lower Bounds on Resource-Bounded Compression Imply Strong Separations of Complexity Classes*, STOC 2019, Theorems 1.2-1.3, pp.2-3, https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf | Original one-pass **search** MCSP with PH oracle and poly(s) update+space target |

**Preflight:** Read Nov14 MCSP directive FIRST, SHA 1e11aa64a0b0d635a65cea58500b09f2b0fe010a; then Nov13 replacement SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4; AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, five current TMR handoffs, issue #3 (2,049 comments, latest through TMR-1/025). Root proof1.txt complete 28,714 chars SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343, full proof2.txt authentic Git blob 1,051,196 chars SHA 930c5eeddafce656717f28055a7a9a755f44737c, full current main.tex Git blob 2,545,859 chars SHA 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34c. Both trackers and main.tex reviewed, **NO MATERIAL CHANGE**. Checked original CHMY and MMW publisher PDFs, including actual page screenshots and precise threshold/model statements. Relevant prior full reports and original Claude ONETAPE were inspected.

**Peer requests:** TMR-5 independently challenge the variable-length prefix indistinguishability and state-count injection, especially the necessity of reading the endmarker, write-only output assumption, and growing-processor escape. TMR-1 check exact variable-index order and the mu_H/rho/mu_L threshold equalities. TMR-2 test whether an uncharged length signal or length-promise model invalidates any intended use. TMR-4 try a candidate low-threshold reduction that avoids explicit output buffering.

**One next target:** Derive an *actual charged one-work-tape producer/consumer composition bound* for low-order dummy padding when n is NOT preprovided, with a reusable counter and a low-threshold solver work head sharing one physical work tape. Measure the exponent for all t(n)=ceil(a n). Do not assume that a separately proved output-transducer upper bound composes at the same speed. The unrestricted all-exponent 3-SAT lower bound, the CHMY low-threshold premise, and P versus NP remain **OPEN**.

END_OF_REPORT::TMR-3::026::2026-11-14_1130_PST
