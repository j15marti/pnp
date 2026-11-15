# TMR-5/028: Local-head indexed-MCSP circuit bound and sparse-query tail audit

**Timestamp:** 2026-11-14 16:50 PST, America/Los_Angeles. **Owner:** TMR-5 Machine Bottleneck Redteam. **Status:** LOCALHEAD44 and TAIL44 are **PROVED/RESTRICTED at the stated symbolic models, independent TMR-1/TMR-4/TMR-2 review OPEN**. Independently executed finite tests are **COMPUTATIONAL**. P versus NP remains **OPEN**.

## 1. New relative to TMR-5/027 and peers

TMR-5/027 reported the condition $a\mu>2d$ for polynomial-output-length ratios $N=L^{a+o(1)}$ and indexed evaluator time $t=L^{d+o(1)}$, relying on TMR-4/031's explicit bound $CC_n(Y)\le K_E(L+n+t+2)^2$. **That particular displayed bound alone establishes the stated threshold condition only for $a\mu>2\max(1,d)$**, not $a\mu>2d$ when $0\le d<1$. This is a genuine missing algebraic inference, not an explicit counterexample to the conclusion.

**New repair LOCALHEAD44:** In the original standard fixed finite-alphabet Turing-machine model with conventional, left-initialized, locally moving input heads and no free pointer relocation, only the $O(t)$ cells accessible within $t$ transitions need representation. A direct all-transition circuit simulation yields the stronger bound

$$
\boxed{CC_n(Y_{E,F,n})\le K_E(t_{E,F,n}+2)^2.}
$$

Consequently $a\mu>2d$ **is validated in this explicit local-head model, including $d<1$**. The correction must not be transferred to random-access source queries, advice or a prepositioned head without paying for its positioning. A RAM capable of obtaining arbitrary $F[i]$ in unit time does not satisfy this theorem's physical-access hypothesis.

**New independent TMR-3/031 audit TAIL44:** Its constant-factor sparse-flip counting proof survives symbolic review in the charged point-bit oracle model. Beyond its expectation inequality, the exact no-hit hypergeometric probability and discrete convexity give a tail bound and a larger explicit asymptotic expectation coefficient for fixed error $\delta\in(0,1/2)$. This is an advance in a **restricted input-acquisition model**, not additional computational work and not a one-work-tape $N^{1.01}$ lower bound.

## 2. Fully charged locality theorem

**Input and uniformity.** Fix one deterministic total finite-alphabet multitape transducer $E$, one finite program for all source strings $F$ and all index lengths $n$. The ordinary uncompressed source word $F\in\{0,1\}^L$ and the $n$-bit index $i$ are placed in a conventional explicitly delimited layout on a fixed number of tapes; each input head starts at a designated fixed left-origin cell, and every head moves at most one cell in one transition. All work tapes start blank, and there is no free precomputed table, advice, source-dependent initial head position, or random-access instruction. A fixed bounded number of initial tracks/tapes and ordinary local delimiters are permitted. Both malformed-input handling and all preprocessing are executed by the same machine. Let $t=\max_i T_E(F,i)$, with $Y[i]=E(F,i)$ and $N=2^n$.

**LOCALHEAD44 lemma.** There exists $K_E>0$, depending only on $E$ and its tape convention, such that for every $F,n$,

$$
CC_n(Y)\le K_E(t+2)^2
$$

for the exact ordinary binary fan-in AND/OR/NOT circuit model with named input wires, free constants and fanout.

**Proof.** Consider each physical tape head during any of the at most $t$ transitions. Starting at its fixed left-origin cell, it cannot visit a tape position beyond distance $t$, regardless of what $F$ and $i$ contain. Its first $t+1$ relevant tape cells suffice; the rest are physically unobservable. On an input tape, the initial content of each represented cell is either a constant bit of the now fixed source $F$, a named index-input bit $i_j$, an ordinary constant delimiter/endmarker or a blank symbol. Source constants and index wires need no source-length-sized circuit; whether a delimiter lies inside this short prefix is hardwired for each $(F,n)$. All fixed work tapes need at most $O(t+1)$ writable cells. The total number of represented cells over the fixed number of tapes is $O_E(t+1)$.

At every one of $t$ synchronous Boolean circuit layers, use head-indicator wires and cell-symbol indicators to select each scanned symbol by an OR of $O_E(t+1)$ terms, apply the *fixed* finite transition table, conditionally update each represented cell, and shift each head indicator by one. This costs $O_E(t+1)$ gates per layer. Pad early halts with an absorbing terminal state and use its exact output wire. Initialization and terminal selection cost $O_E(t+1)$. All actual transitions, including tape reversals, input rereads, work-memory changes and recomputation, are simulated. Thus the total circuit size is at most $K_E(t+2)^2$. The circuit is nonuniform in the fixed parameter $F,n$ but **does not** grant any free computational step to the uniform evaluator $E$. QED.

**Layout caveat.** For a single concatenated source/index tape, a head that cannot travel past the source prefix cannot see the index bits, so the output is necessarily independent of unseen index bits. For separate left-aligned tapes the proof above applies directly. If an interface starts a head at a source-dependent distant address or supplies an arbitrary indexed symbol at unit cost, the lemma is not applicable until that interface is physically simulated and paid.

**COROLLARY (repaired degree window).** Let $L\to\infty$, $N=L^{a+o(1)}$ with fixed $a>0$, and $t\le L^{d+o(1)}$ for fixed $d\ge0$. Then $CC_n(Y)\le L^{2d+o(1)}$. For any fixed $\mu>0$ with $a\mu>2d$, all sufficiently large outputs are ordinary $MCSP[\lfloor N^\mu\rfloor]$ YES. In particular, **a polynomial-time output-index algorithm cannot generate MCSP NO** within this window even when it reads source formula syntax, computes compact summaries or branches adaptively. This is an upper bound on the generated target function and not a polynomial-time decision procedure for SAT or an efficient materialization of $N$ bits. For a target MCSP NO table, $t>\sqrt{\lfloor N^\mu\rfloor/K_E}-2$. No SAT lower bound follows without a label-preserving fully paid reduction.

For example $a=1,d=0.3,\mu=0.9$ has $a\mu=0.9>0.6=2d$, but $a\mu<2$; the earlier displayed $K_E(L+n+t)^2$ bound by itself does **not** establish collapse, whereas LOCALHEAD44 does in its stricter machine model. The former algebraic derivation is retired; the **repaired theorem** is retained pending independent review.

## 3. Independently sharpened randomized sparse-query lower bound

Use TMR-3/031's ordinary exact MCSP setting, $N=2^n$, $s=\lfloor N^\mu\rfloor$ with $0<\mu<1$, fixed $K>2\mu/(1-\mu)$ and $r=\lceil Ks\rceil$. The number of circuits with at most $s$ gates is at most

$$
D(n,s)=(s+1)(n+s+2)\big[3(n+s+2)^2\big]^s.
$$

For a fixed YES table $x$, a uniformly random $r$-bit flip $Y=x\oplus1_R$ remains YES with probability at most $\varepsilon_N=\min(1,D(n,s)/\binom Nr)=2^{-\Omega_{\mu,K}(s\log N)}$. This elementary counting statement and TMR-3's $K$ coefficient are independently verified, subject to its fixed circuit basis.

Let a randomized point-bit oracle algorithm decide ordinary MCSP with error at most $\delta<1/2$ on every full truth table. For its random coins $\rho$ and a fixed YES input $x$, let $q_\rho$ count distinct queried source positions. Define

$$
H_{N,r}(q)=\frac{\binom{N-q}{r}}{\binom Nr}
\quad(0\le q\le N),
$$

with zero numerator if $N-q<r$. Conditional on the entire adaptive zero-difference transcript at $x$, the probability that random $R$ misses every queried position is **exactly** $H_{N,r}(q_\rho)$. By same-transcript coupling, random-flip acceptance probability is at least $\mathbb E_\rho H_{N,r}(q_\rho)-\delta$. Since at most $\varepsilon_N$ of flipped targets are YES, acceptance is at most $\delta+(1-\delta)\varepsilon_N$. Hence

$$
\boxed{\mathbb E_\rho H_{N,r}(q_\rho)\le
b_N:=2\delta+(1-\delta)\varepsilon_N.}
$$

This refines TMR-3/031's union-bound expectation estimate, with *no* assumption that the algorithm restarts or discards shared state.

**Distributional tail (new):** For every integer $m$ with $H_{N,r}(m)>0$,

$$
\boxed{\Pr_\rho[q_\rho\le m]\le
\min\{1,b_N/H_{N,r}(m)\}.}
$$

**Mean coefficient (new):** $H_{N,r}(q)$ is decreasing and discretely convex: $\Delta H(q)=-\binom{N-q-1}{r-1}/\binom Nr$ increases with $q$. Let $\overline H$ be its continuous piecewise-linear interpolation. Jensen gives $\overline H(\mathbb E q)\le \mathbb E H(q)\le b_N$ and therefore

$$
\mathbb E q\ge \overline H^{-1}(b_N).
$$

For fixed $0<\delta<1/2$, $r=K N^{\mu+o(1)}=o(N)$ and $\varepsilon_N\to0$, we have $H_{N,r}(cN/r)\to e^{-c}$. Consequently,

$$
\boxed{\mathbb E_\rho q_\rho\ge
\big(\log(1/(2\delta))-o(1)\big)\frac Nr.}
$$

For $\delta=1/3$, the leading coefficient is $\log(3/2)\approx0.405465$, strictly greater than TMR-3/031's $1-2\delta=1/3$. Neither statement forces more than a **sublinear** number of input-bit probes when $\mu>0$. Arbitrary polynomial workspace and source access are permitted; unrestricted machine processing remains unbounded and the P versus NP arrow OPEN. The $\delta=0$ deterministic case is addressed by the earlier stronger nearly-all-$N$ certificate-fiber bound, not the displayed logarithm.

## 4. Literature and model/hypothesis matrix

| Source, theorem/page | Exact problem/model/parameter/conclusion and scope |
| --- | --- |
| Cheraghchi, Hirahara, Myrisiotis, Yoshida, STACS 2021, **Thm 1, printed 23:3** [1] | Ordinary explicit truth-table MCSP, $N=2^n$, $s=N^{\mu_1}$ for some **small** fixed $\mu_1>0$; deterministic one-way read-only input plus one two-way writable tape. **Conditional** $\mathrm{MCSP}[s]\notin\mathrm{DTIME}_1[N^{1.01}]\Rightarrow P\ne NP$. Antecedent OPEN. |
| Same, **Thm 2, 23:3** [1] | Ordinary exact MCSP at a **different** $\mu_2$ close to 1; same input/work interface, two-sided bounded-error randomness. **Proved** $\mathrm{MCSP}[N^{\mu_2}]\notin\mathrm{BPTIME}_1[N^{1.99}]$. Does not instantiate $\mu_1$. |
| Same, **Thm 3, 23:4** [1] | For any oracle and $\mu>1/2$, a one-way-input one-work-tape randomized lower bound $N^{1+\mu'}$ when all oracle queries have length $N^{o(1)}$. This limits short-oracle-query techniques, not arbitrary algorithms. |
| McKay, Murray, Williams, STOC 2019, **Thms 1.2-1.3, author PDF pp.2-3** [2] | **Search**-MCSP with $A$-oracle circuits, time-constructible $s(n)\ge n$, full $N=2^n$-bit stream, $\widetilde O(s)$ space and $\widetilde O(s^2)$ per-item update with short $\Sigma_3SAT^A$ queries. Conditional absence of certain deterministic $\operatorname{poly}(s)$-space/update streamers for some $A\in PH$ implies $P\ne NP$. Neither an ordinary decision MCSP nor MKTP result is silently substituted. |
| TMR-4/031 [3] | Uniform deterministic bit indexer, arbitrary source description $F$ of length $L$, full target $N=2^n$; original quadratic bound $K_E(L+n+t+2)^2$. LOCALHEAD44 strengthens it with an additional **explicit standard local-head assumption**. No oracle/advice conversion. |
| TMR-3/031 [4] | Ordinary MCSP positive-power circuit threshold and restricted adaptive point-bit probes, randomized source access. Original count/coupling argument independently reviewed and sharpened above. Not unrestricted SAT time. |

No result is transferred between ordinary MCSP, promised Hamming-Gap-MCSP, succinct/partial MCSP, MKTP, and MMW search-MCSP without a definition-preserving charged proof. No ordinary MCSP NP-completeness is assumed.

## 5. Exact dependencies, route ranking, and retirements

1. **Priority A, direct magnification:** obtain the exact small-$\mu_1$ $N^{1.01}$ deterministic one-work-tape lower bound on ordinary explicit MCSP in the **one-way** input model, then invoke CHMY Theorem 1. Weakest load-bearing premise is presently **OPEN**. High-$\mu_2$ Theorem 2 does not meet the threshold.
2. **Priority B, new low-$\mu$ cost necessity:** prove a cost-sound invariant charging computational transitions *after and between* source probes. LOCALHEAD44 and TAIL44 demonstrate why output-index shortcuts and source-query counts cannot alone provide $N^{1.01}$. A full arbitrary-machine bridge is **OPEN**.
3. **Priority C, restricted machine networks:** TMR-1/030's short header copying gives a plausible all-step symbolic constructor interface, scoped to one guest work head and a length-only constructor. The large-$\mu_2$ network frontier is **RESTRICTED**, and TMR-3/031's deterministic full-source ingress dominates its $N^{0.99}$ event estimate where applicable. No independent general SAT separation.
4. **Retire or restrict:** unproved inference $a\mu>2d$ **from the displayed $K_E(L+n+t)^2$ bound alone** is **FALSIFIED AS A DEDUCTION** for $d<1$, replaced by LOCALHEAD44 on standard TMs. Dummy-variable positive-power padding, direct masked-SAT full tables, naive source-independent oracle compilers and uncharged index-output expansion remain previously retired in their own exact scopes. Expensive specific representations, prescribed pebbling, single-input crossing sequences and repeated SAT product enumeration are not unconditional resource necessities.

## 6. Original corpus, performed tests, and publication discipline

Original project items inspected for this audit: research/agents/tmr-4/2026-11-14_1537_TMR4_INDEXABLE_LIFT_FIREWALL031.md and original reported experiment/raw; research/agents/tmr-5/2026-11-14_1552_TMR5_DEGREE_WINDOW_CONSTRUCTOR_REVIEW027.md; research/agents/tmr-3/2026-11-14_1635_TMR3_SHARP_SPARSE_NETWORK_SOURCE_FRONTIER031.md; research/agents/tmr-1/2026-11-14_1605_TMR1_SHORT_HEADER_CONSTRUCTOR_SIMULATION030.md; research/agents/tmr-2/2026-11-14_1618_TMR2_RANDOM_SHARED_SPARSE_MINIMAX031.md; prior deterministic research/main/2026-10-20_2343_MAIN_QUERY_COVERAGE_FIBER27.md; research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex; research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex; research/agents/tmr-4/2026-11-14_0836_TMR4_MOMENT_CONGRUENCE_AND_QUOTIENT_COUNTEREXAMPLE023.md; comments/grok-4.7/2026-10-21/2026-10-21_0013_GROK_REVIEW.tex. The original reports are evidence and restricted controls, not inferred theorems from chat.

**Independent native CPython source:** experiments/tmr/tmr5_locality_tail_audit044.py. **Exact raw:** results/raw/tmr/2026-11-14_1650_TMR5_LOCALHEAD_TAIL044_RAW.json. Executed on a local native CPython interpreter: 1,680 paired bounded local-head programs/inputs, 13,440 identical all-transition trace comparisons under changes to unvisited distant source suffixes; 78,971 exact rational hypergeometric monotonicity checks, 77,629 discrete convexity checks, 25,524 tail-formula controls, 16 real-exponent grid checks; **zero failures**. This is an **independent reimplementation**, not a replay of the earlier published JS files, and does not compile a general physical TM.

Preflight: read the 2026-11-14 governing MCSP directive FIRST (blob 1e11aa64a0b0d635a65cea58500b09f2b0fe010a), then 2026-11-13 replacement, AGENTS.md, CODEX.md, pnp skill, latest issue #3 through TMR-3/031, five TMR handoffs and relevant original historical sources. Full proof1.txt read, blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343 (28,714 characters). Root proof2.txt contents API returned blank with SHA, so authentic full blob 930c5eeddafce656717f28055a7a9a755f44737c (1,051,196 characters) was separately retrieved. The same recovery obtained the full canonical main.tex blob 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34 (2,545,859 characters). **TRACKERS REVIEWED; NO MATERIAL CHANGE.** The newly strengthened result needs independent peer review before any promotion into root main.tex; this report does not rewrite the historic manuscript or trackers. All five schedules and roles remain unchanged.

**NEXT exact request:** TMR-4 and TMR-1 independently check the local-head gate unrolling, especially the $L$-independent source-cell initialization and any nonstandard input positioning. TMR-2 and TMR-3 check the hypergeometric Jensen/tail step and explore whether an **unavoidable superlinear computation charge** can be added to the same full input trace without assuming a prescribed representation. TMR-5 should attack any proposed source-index interface using an actual charged simulation and an easy algebraic/circuit control.

## Numbered primary sources

[1] Cheraghchi, Hirahara, Myrisiotis and Yoshida, *One-Tape Turing Machine and Branching Program Lower Bounds for MCSP*, STACS 2021, Theorems 1-3, printed pp.23:3-23:4. https://doi.org/10.4230/LIPIcs.STACS.2021.23

[2] McKay, Murray and Williams, *Weak Lower Bounds on Resource-Bounded Compression Imply Strong Separations of Complexity Classes*, STOC 2019, Theorems 1.2-1.3, author manuscript pp.2-3. https://doi.org/10.1145/3313276.3316396

[3] TMR-4/031 original project report, https://github.com/j15marti/pnp/blob/main/research/agents/tmr-4/2026-11-14_1537_TMR4_INDEXABLE_LIFT_FIREWALL031.md

[4] TMR-3/031 original project report, https://github.com/j15marti/pnp/blob/main/research/agents/tmr-3/2026-11-14_1635_TMR3_SHARP_SPARSE_NETWORK_SOURCE_FRONTIER031.md

END_OF_REPORT::TMR5::028::2026-11-14_1650_PST
