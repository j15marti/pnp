# TMR-1/028: Capped exact circuit minimization, certificate polarity and the MCSP magnification frontier

**Pacific timestamp:** 2026-11-14 13:57 PST (America/Los_Angeles). **Owner:** TMR-1 Machine Model Lead. **Scientific status:** CANDIDATE/RESTRICTED for the one-work-tape compiler and derived exact-value algorithm, pending independent TMR-3/TMR-5 physical review; elementary reduction implications are CONDITIONAL on explicitly hypothesized reductions; finite tests COMPUTATIONAL. **P versus NP: OPEN.**

## 1. State recovery, authorship and novelty

Read FIRST the controlling 2026-11-14 MCSP directive, blob \`1e11aa64a0b0d635a65cea58500b09f2b0fe010a\`, then the 2026-11-13 replacement directive, AGENTS.md, CODEX.md and .codex/skills/pnp-research/SKILL.md. Read current five TMR handoffs and latest issue #3 through TMR-5/025. Root proof1.txt was readable in full at 28,714 characters, blob \`06f7ebc8c2283304a0f5200b518c6e48fa41e343\`. The GitHub Contents response for proof2.txt and root main.tex returned a SHA and empty body; **authentic Git blobs** \`930c5eeddafce656717f28055a7a9a755f44737c\` and \`6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34\` were fetched and checked at **1,051,196** and **2,545,859** characters. Neither file is empty and neither was edited. Repo-scoped preflight script and full LaTeX compilation were not executed in this connector-based run.

| Prior original artifact | Actual scope/status retained |
| --- | --- |
| \`research/agents/tmr-1/2026-11-14_1307_TMR1_MCSP_GROWING_THRESHOLD_ENUMERATION027.md\`, \`experiments/tmr/tmr1_slowthreshold030.py\`, original raw JSON | Previous decision-only upper bound at $s=\Theta(n/\log n)$, $T=N^{1+2\kappa+o(1)}$; physical one-head compiler pending independent audit |
| \`research/agents/tmr-3/2026-11-14_1327_TMR3_MCSP_RAWSCAN_HEADER_BOUND028.md\` and original Python | Independent mobile-scratch idea, raw $N$-bit tape plus small scratch; differently annotated-input low-space claim not a bare-input transfer |
| \`research/agents/tmr-5/2026-11-14_1350_TMR5_MCSP_SYNTAX_CERTIFICATE_REVIEW025.md\` and original Python | Reverse-label polynomial-output conditional $NP=coNP$ and syntax-aware escape from a restricted evaluation-oracle theorem; independently checked mathematically here |
| \`research/agents/tmr-4/2026-11-14_1336_TMR4_ORACLE_LOCALITY_GAP_MASK029.md\` | Adaptive evaluation-oracle Hamming bound excludes general syntax-aware SAT transformations |
| \`research/agents/tmr-2/2026-11-14_1322_TMR2_GROWING_MCSP_PERIODIC_CODE028.md\` | Full YES query requirement on a periodic, positive-growing-threshold subclass with cheap *special-language* computation; not full MCSP |
| \`research/agents/tmr-3/2026-11-14_0936_TMR3_MCSP_FIXED_NETWORK_SERIALIZATION024.md\`; \`research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex\` | Fixed-network and crossing-sequence resource models are restricted; do not confuse tape transport with unrestricted SAT computation |
| \`research/agents/threshold-descent/2026-10-18_1416_THRES_HASHBRIDGE4.tex\`; \`research/main/2026-10-18_ASYMPTOTIC_CONE5.md\` | Existing affine/compact-summary and padding-exponent countercontrols, not positive hardness transfers |

**Genuinely new relative to TMR-1/027:** (a) upgrade the same exhaustive enumerator from one YES/NO decision to the exact **capped minimum gate count**, over an unbounded threshold; (b) formalize a quantitative polynomial-output SAT-reduction consequence with explicit source encoding and runtime exponents, including both label orientations; (c) independently audit the recent TMR-5 certificate direction and the existential $\mu$ quantifier in CHMY. Exact circuit enumeration is elementary prior art, **not** a claimed new complexity-theory discovery. These are positive restricted algorithms and proof-chain firewalls, not a new lower bound.

## 2. Definitions and one-work-tape exact-value lemma (CAPMIN31)

Let $n$ be Boolean input arity, $N=2^n$ the **explicit full-table input length**, $L$ the bit length of an independent encoded 3-CNF source, and $v$ the number of source SAT variables. These quantities are never substituted for each other. Circuits use two-input AND/OR, unary NOT, free constants and input wires, unrestricted fan-out, and count each gate once. Define $CC_n(f)$ as the minimum number of gates and

$$
K_{s(n)}(f)=\min\{CC_n(f),\,s(n)+1\}.
$$

This is an **integer-valued** transduction, not the YES/NO predicate alone. Let $s:\mathbb N\to\mathbb N$ be fixed, total, and uniformly computable from $n$ in $\operatorname{poly}(n+s(n))$ time using a fixed finite machine.

**CAPMIN31 (CANDIDATE/RESTRICTED one-head machine compiler):** Under the same bare-source input and physical mobile-scratch compiler specified in TMR-1/027 and independently supported in TMR-3/028, a single fixed finite deterministic machine with **one-way read-only input and exactly one two-way read/write work tape**, no input-length header, outputs the exact integer $K_{s(n)}(f)$ in binary on every length-$N$ truth table, with

$$
D(n,s)=(s+1)(n+s+2)[3(n+s+2)^2]^s
$$

and charged bounds

$$
T(N)\le N D(n,s(n))\operatorname{poly}(n+s(n)+1)+N\operatorname{poly}(n+1),
$$

$$
S(N)\le O\bigl(N\operatorname{poly}(n+s(n)+1)\bigr).
$$

Reject malformed non-power-of-two input lengths with a fixed convention. No source bit may be revisited on the read-only input, but the work-tape copy can be reread. All head motions, input copying, gate-program construction, indices, enumeration, candidate evaluation, scratch rotation, output encoding and terminal handling are charged. No random access, preloaded lookup, oracle or advice is free.

**Proof.** First copy the complete one-way input to work tape using the TMR-1/027 mobile counter/record compiler. Determine $N$ and $n$, reject malformed lengths, compute $s(n)$. Enumerate all topologically ordered circuits in **nondecreasing gate-count order** from 0 through $s(n)$. The same count $D(n,s)$ upper-bounds all descriptions. For each candidate use a single-work-head, mobile finite-alphabet scratch block to visit every cached input bit, evaluate its finite DAG, and test equality. On the first matching circuit with $j$ gates, write $j$ in binary and halt. If none matches, write $s(n)+1$. Soundness follows since a matching circuit actually computes all $N$ truth-table entries. Completeness follows since every circuit of at most $s(n)$ gates has a description in the enumeration; its first match occurs at the minimum size because the order is by gate count. The final integer output requires only $O(\log(s+2))$ charged cells/steps, within the displayed resource bounds. Exactly the previous work-tape compiler is reused, so this argument adds an output/classification refinement, **not a newly verified finite-state compiler**. QED subject to that explicit physical-machine dependency.

If $s(n)=o(n/\log n)$, then

$$
\log_2 D(n,s(n))=O\bigl(s(n)\log(n+s(n)+2)+\log(n+s(n)+2)\bigr)=o(n),
$$

and thus $T(N)=N^{1+o(1)}$. This includes the specific unbounded, uniformly computable schedule

$$
s(n)=\left\lfloor\frac{n}{\lceil\log_2(n+1)\rceil^2}\right\rfloor.
$$

For $s_\kappa(n)=\lfloor\kappa n/\lceil\log_2(n+1)\rceil\rfloor$ with any fixed rational $\kappa>0$, the TMR-1/027 count gives $T=N^{1+2\kappa+o(1)}$ for this **stronger exact-value output** as well. In particular $\kappa<0.005$ eventually fits the physical $N^{1.01}$ time exponent, subject to peer review of the one-work-tape compiler. **Neither $o(n/\log n)$ nor $\Theta(n/\log n)$ approaches $N^\mu=2^{\mu n}$ for any fixed $\mu>0$.**

This theorem does not assert a poly$(s)$-space one-pass search streamer of the McKay-Murray-Williams type. It caches the full source table.

## 3. New quantitative reduction firewall (POLY-SHELL31)

Consider a hypothetical single fixed uniform polynomial-time total reduction $R$ from all length-$L$ valid 3-CNF encodings to **fully materialized** target tables of length $N(F)=2^{n(F)}\le L^a$, for fixed $a>0$. Assume $R$ computes the associated nonnegative integer target threshold $s(n(F))$ and that for all relevant target arities

$$
0\le s(n)\le \left\lfloor\frac{\kappa n}{\lceil\log_2(n+1)\rceil}\right\rfloor
$$

for one fixed $\kappa>0$ (or a uniformly computable smaller threshold schedule). Assume **exact both-label equivalence** in *either* orientation, not just one-sided implications.

**POLY-SHELL31 (CONDITIONAL implication, elementary proof):** Such an $R$ would give a deterministic, **uniform polynomial-time** algorithm for general 3-SAT. If $R$ has time $O(L^r)$ and target $N\le L^a$ for fixed $r,a$, a conservative derived SAT time is

$$
T_{\mathrm{SAT}}(L)
  \le O(L^r)+L^{a(1+2\kappa)+o(1)}+L^{O(1)}
$$

for the target's ordinary decision algorithm using CAPMIN31. Therefore the hypothesis implies $P=NP$.

**Proof.** Compute the complete $N\le L^a$ target bits using the fixed program $R$. Call the uniform one-work-tape exact classifier on those actual bits. Its time is bounded by $N^{1+2\kappa+o(1)}$. For a reversed label map negate the one-bit outcome; for a forward map use it directly. Both-label correctness of $R$ supplies SAT correctness for *all* valid $F$. The resulting one fixed composition is polynomial in $L$ and handles all lengths. A short table output, a syntactic formula or a compressed circuit name are **not** interchangeable: the premise explicitly requires a complete table in polynomial $L$ output and charges its construction. QED.

This establishes no **unconditional nonexistence** of $R$. If $P=NP$, such an implication is not contradictory. TMR-5/025's independent **general-threshold reverse-label** observation is also correct: if $R$ maps UNSAT to MCSP YES and SAT to NO with $N,s\le\operatorname{poly}(L)$, guessing the small target circuit and verifying all $N$ entries gives $3UNSAT\in NP$, hence **$NP=coNP$**. That certificate argument needs no assumption that the target MCSP slice lies in P. At the present slow threshold, the stronger $P=NP$ consequence holds by the explicit decider. Forward SAT-to-MCSP YES at arbitrary growing $s$ carries no such certificate-orientation obstruction; ordinary MCSP NP-hardness remains an open research question.

For the previously analyzed exact source gadget $h_F(x,u,w)=F(x)\land u\land w$, the full output has $N=2^{v+2}$ bits. Under a polynomial-output promise $N\le L^a$ it can apply only to $v+2\le a\log_2 L$. Such logarithmic-variable SAT instances can already be decided by enumerating $2^v=\operatorname{poly}(L)$ assignments. This clarifies why the cheap gadget does not create a polynomial-output reduction for arbitrary $v=\Theta(L)$.

## 4. Primary-source theorem/hypothesis matrix and quantifier audit

| Original theorem and version | Exact model, input/threshold/promise | Hypothesis and conclusion | Missing arrow |
| --- | --- | --- | --- |
| Cheraghchi, Hirahara, Myrisiotis, Yoshida, **STACS 2021 Theorem 1**, p.23:3, [publisher PDF](https://drops.dagstuhl.de/storage/00lipics/lipics-vol187-stacs2021/LIPIcs.STACS.2021.23/LIPIcs.STACS.2021.23.pdf) | Ordinary exact **decision** MCSP[$2^{\mu_1 n}$] on $N=2^n$ full bits, deterministic one-way read-only input plus exactly one two-way writable work tape | There exists a sufficiently small $\mu_1>0$ such that nonmembership in $\mathrm{DTIME}_1[N^{1.01}]$ implies $P\ne NP$ | No proved low-$\mu_1$ lower bound |
| CHMY **Theorem 2**, same page | Ordinary exact MCSP[$2^{\mu_2 n}$] at some *different, larger* $\mu_2$ close to 1; bounded two-sided-error randomized machine, same input/work-tape interface | Known unconditional $\notin\mathrm{BPTIME}_1[N^{1.99}]$ | Wrong gate threshold for Theorem 1, even though exponent is stronger |
| McKay, Murray, Williams, **STOC 2019 Theorems 1.2 and 1.3**, p.2, [author PDF](https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf) | **Search**-MCSP$^A[s(n)]$ with oracle gates, full $N=2^n$ table, time-constructible $s(n)\ge n$, a one-pass streaming algorithm with $\Sigma_3SAT^A$ short queries, $\widetilde O(s(n))$ space and $\widetilde O(s(n)^2)$ update time | Under specified nonexistence of a poly$(s)$-space/poly$(s)$-update search streamer for some $A\in PH$, infer $P\ne NP$ | Search/oracle/streaming differs from ordinary exact decision and this run's cached-data algorithm |
| Oliveira, Pich, Santhanam, **CCC 2019**, [DOI](https://doi.org/10.4230/LIPIcs.CCC.2019.27) | Gap-MKtP and approximation/circuit families with specific parameters, not automatically ordinary MCSP | Distinct conditional nonuniform separations at matching theorem assumptions | Promise and circuit-family transfer not established |
| Allender, Hirahara, **MFCS 2017**, [DOI](https://doi.org/10.4230/LIPIcs.MFCS.2017.54) | Approximation of MCSP/MKTP, cryptographic one-way-function hypothesis in NP-intermediate statements | Conditional NP-intermediate conclusions, not unconditional 3-SAT lower bounds | Do not treat assumption as proof |
| Chen et al., **ITCS 2020**, [DOI](https://doi.org/10.4230/LIPIcs.ITCS.2020.70) | Short-oracle-query locality techniques for magnification | Technique-specific barrier, not an unconditional algorithmic lower bound | No arbitrary-machine inference |

**Quantifier firewall.** The displayed CHMY Theorem 1 reads literally $\exists\mu>0:\bigl(M_\mu\notin\mathrm{DTIME}_1[N^{1.01}]\Rightarrow P\ne NP\bigr)$, where $M_\mu=\mathrm{MCSP}[N^\mu]$. Its paper explicitly notes the equivalent sufficient assertion $(\forall\mu>0,\ M_\mu\notin\mathrm{DTIME}_1[N^{1.01}])\Rightarrow P\ne NP$. It does **not** license substituting an arbitrary numerically chosen $\mu_0$ into an unspecified existential witness. Exact rounding and gate convention must also match. Our $s(n)$ is $N^{o(1)}$ and cannot witness that positive power. Under $P=NP$, the magnification construction chooses an eligible small $\mu$ depending on polynomial oracle costs; there is no number here supplied by our experiments.

In contrast to the above truth-table size $N$, the team target for arbitrary 3-SAT is: for each fixed total correct uniform multitape $A$, every $k\ge1$, $C>0$, $L_0$, there exists a valid $F$, $|F|\ge L_0$, with $T_A(F)>C(|F|+1)^k$. Nothing in CAPMIN31 or POLY-SHELL31 proves that statement. Same-machine space obeys $S_A(F)\le O(T_A(F))$, but no small-space theorem alone supplies the missing unrestricted lower bound.

## 5. Executed independent checks and hostile controls

Actually executed **native CPython 3** source \`experiments/tmr/tmr1_capmin031.py\`. The program has **two independently implemented circuit-minimum enumerators**: topologically ordered sequences and a gate-by-gate closure of available truth-table functions. These agree on every Boolean truth table for $n=1,2,3$ and gate budgets 0,1,2. Exhaustive class sizes for $n=3$ are **5, 14, 40** at those budgets. Total **1,832 assertions**, zero failures, plus seven large-$n$ integer-log description-bound checks and 156 polynomial-output-versus-variable-count checks. Raw output: \`results/raw/tmr/2026-11-14_1357_TMR1_CAPMIN031_RAW.json\`. No random seed or external libraries.

A first local test mistakenly parsed the displayed bit sequence \`1010\` as the MSB-first integer \`0b1010\`; with our documented least-significant-index-first table convention the actual integer is \`0b0101\`. That initial assertion failed, was corrected explicitly, and **the final code was rerun** with 1,832 checks and no failures. This was an encoding error in the test, not evidence for an additional theorem. The script is not an executed native single-head Turing-machine transition compiler; machine bounds remain symbolic and dependent on physical-peer review. Other hostile controls retained rather than erased: cheap periodic functions, XOR/Gaussian elimination, Horn/2-SAT, bounded treewidth, dummy padding, syntactic SAT distinction, arbitrary sharing, and the full-output-versus-one-bit decision firewall.

**Exact local native evidence SHA256:** source \`dfb69008d8e3a6f480ac82300e51fd77593660f6ccead1a5bc10211c000e4385\`, raw JSON \`771679285b7d54f3b819a92e2a56a897f292796d1abd7f37cea42e30e1c0d130\`. Post-publication GitHub readback must independently verify paths and content; these hashes refer to the actual local executed files.

## 6. Remaining dependency chain, peer review and tracker status

Candidate chain: establish a correct resource-preserving **high-to-low threshold** transfer at an exact positive-power $\mu_1$, or prove the exact low-$\mu_1$ one-work-tape decision lower bound directly [BOTH OPEN]; combine with **CHMY Theorem 1** [KNOWN CONDITIONAL IMPLICATION] to obtain $P\ne NP$. The existing high-$\mu_2$ bound [KNOWN THEOREM] is not a substitute. Alternatively, a complete polynomial-time 3-SAT machine remains a legitimate outcome. CAPMIN31 adds a positive-algorithm control and cannot be promoted to a separation claim.

**Next single target:** derive a length-blind, one-work-tape exact-value or decision candidate architecture at gate budget $s(n)=\omega(n/\log n)$ and determine whether it reaches even an intermediate $s(n)=n^2$ without losing polynomial $N$ time. Request TMR-3 independent physical one-head compiler and EOF verification, TMR-5 formal audit of the exact capped-size and POLY-SHELL31 both-orientation proof, TMR-2 check search/decision streaming scope, TMR-4 test a threshold-changing source-dependent gadget against the reduction/certificate firewall.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** proof1.txt and proof2.txt unchanged; root canonical main.tex remains TMR-5-owned and unchanged. No additional tasks created, restarted or rescheduled.
