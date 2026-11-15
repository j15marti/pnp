# TMR-2/031: Exact randomized minimax for fully shared sparse evaluation oracles

**2026-11-14 16:18 PST (America/Los_Angeles). TMR-2 Information Necessity.**
**Mathematics:** PROVED/RESTRICTED elementary symbolic argument, independent TMR-4/TMR-5 review OPEN.
**Testing:** COMPUTATIONAL exact exhaustive hosted-V8 execution. **P versus NP OPEN.**

## New contribution versus prior work

TMR-2/029 provided an adaptive singleton Hamming-distance bound with global preprocessing and independently restarted output-bit routines; it already noted that a fully shared deterministic singleton decider must inspect all M source coordinates on its zero path. TMR-2/030 generalized the restarted-output Hamming bound to r-sparse sources. This report newly establishes the **exact randomized worst-case minimax error and query threshold for a fully shared, arbitrary-adaptive one-bit decision algorithm**, without restarting between output coordinates. This is a *query-only* result, not an MCSP one-tape or SAT time lower bound.

## Prior original-work ledger and hostile controls

| Original artifact | Status and role |
| --- | --- |
| research/agents/tmr-2/2026-11-14_1417_TMR2_SHARED_ORACLE_PREPROCESS032.md; experiments/tmr/tmr2_shared_oracle032.py; results/raw/tmr/2026-11-14_1417_TMR2_SHARED_ORACLE032_RAW.json | PRIOR PROVED/RESTRICTED singleton reference-distance bound and deterministic full-sharing observation. |
| research/agents/tmr-2/2026-11-14_1521_TMR2_RSPARSE_HYPERGEOMETRIC_QUERY030.md; experiments/tmr/tmr2_sparse_hypergeo038.py; results/raw/tmr/2026-11-14_1521_TMR2_RSPARSE_HYPERGEO038_RAW.json | PRIOR PROVED/RESTRICTED r-sparse per-output restarted distance theorem. Original report, executed code and raw output consulted. |
| research/agents/tmr-4/2026-11-14_1336_TMR4_ORACLE_LOCALITY_GAP_MASK029.md; research/agents/tmr-5/2026-11-14_1350_TMR5_MCSP_SYNTAX_CERTIFICATE_REVIEW025.md | Original query-locality construction and concrete **FALSIFIED/RETIRED unrestricted syntax-transfer inference** using easy proper 3-CNF clause signs. |
| research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex; research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex | Historical crossing sequences, tape and portfolio effects: restricted input-access models, not arbitrary uniform SAT machine lower bounds. |
| research/agents/tmr-4/2026-11-14_1537_TMR4_INDEXABLE_LIFT_FIREWALL031.md; research/agents/tmr-5/2026-11-14_1552_TMR5_DEGREE_WINDOW_CONSTRUCTOR_REVIEW027.md | Prior restricted syntax-aware indexed-circuit and degree-window compiler barriers. |
| research/agents/tmr-5/2026-11-14_0858_TMR5_GF4_CANCELLATION_MOMENT_TRACE020.md; comments/grok-4.7/2026-10-21/2026-10-21_0013_GROK_REVIEW.tex | Compact GF(4)/Walsh/moment/semantic-certificate controls; no full machine hardness transfer. |

Historical Horn, 2-SAT, Gaussian-elimination XOR/Tseitin, bounded-treewidth, disjoint-product, auxiliary-variable, renaming, input-reread, cache/recompute, padding, signed/hypergraph, and native-checker failures remain retained and are not promoted into machine lower bounds.

## Model

Fix integers $M\ge 1$, $1\le r\le M$, $0\le q\le M$. The source is an oracle $f:[M]\to\{0,1\}$. Promise inputs are $f_0=0^M$ with correct answer ZERO, or $f_S=1_S$ for any unknown $r$-subset $S$ with correct answer ONE. A randomized algorithm queries **only this source oracle**, receiving no formula syntax, truth-table advice or independent source-dependent preprocessing. It has arbitrary local computation, arbitrary shared memory, adaptive queries and caching. Its zero-source transcript uses at most $q$ distinct source evaluations on every random-coin outcome; the matching upper algorithm uses at most $q$ on every promised input. This theorem imposes no physical tape, uniform-runtime or space budget.

Define $U=U_{M,r}(q)$ and $e^*=e^*(M,r,q)$ by

$$
U=\frac{\binom{M-q}{r}}{\binom Mr},
\qquad
\boxed{e^*=\frac{U}{1+U}}.
$$

## Theorem RMINIMAX42 (PROVED/RESTRICTED, independent review OPEN)

**The exact minimum worst-case randomized decision error is $e^*$** over the entire promised family, for all $M,r,q$ above. For any $0\le\delta<1/2$, a randomized algorithm with worst-case error at most $\delta$ exists in this source-only model **if and only if**

$$
\boxed{\frac{\binom{M-q}{r}}{\binom Mr}\le\frac{\delta}{1-\delta}.}
$$

In particular, deterministic zero-error decision requires and can achieve exactly

$$
\boxed{q\ge M-r+1.}
$$

### Lower-bound proof

Fix any random coins $\omega$ and run the **entire adaptive algorithm** on $f_0$. Let $Q_\omega$ be its queried-coordinate set, $|Q_\omega|\le q$, and let $a_\omega$ be its final output. Let $\alpha=\Pr_\omega[a_\omega=\mathrm{ONE}]$, its false-positive probability on zero.

For every $r$-subset $S$ disjoint from $Q_\omega$, all adaptive query replies match the zero execution, so the entire shared transcript, terminal state and answer coincide. In particular, when $a_\omega=\mathrm{ZERO}$, these $S$ incur a false negative. For uniformly random $S$,

$$
\Pr[S\cap Q_\omega=\emptyset]
=\frac{\binom{M-|Q_\omega|}{r}}{\binom Mr}
\ge U.
$$

Average the error over $S$ and then over $\omega$. Some $r$-sparse source has error at least $(1-\alpha)U$, while zero itself has error $\alpha$. Therefore

$$
e_{\rm worst}\ge\max\{\alpha,(1-\alpha)U\}
\ge\frac{U}{1+U},
$$

the last inequality obtained by balancing the two affine expressions at $\alpha=U/(1+U)$. No prefix-state indistinguishability beyond **identical actual oracle answers** is assumed, and full sharing does not invalidate the zero-path coupling.

### Matching algorithm

With probability $\alpha=U/(1+U)$ output ONE without querying. Otherwise choose a uniformly random $q$-subset $Q\subseteq[M]$, query its positions and output ONE iff at least one answer is one. Zero-input error is $\alpha$. For every positive $r$-support $S$, error is

$$
(1-\alpha)\frac{\binom{M-r}{q}}{\binom Mq}
=(1-\alpha)\frac{\binom{M-q}{r}}{\binom Mr}
=\alpha.
$$

Thus worst-case error equals $e^*$ for **each** promised source, proving the exact minimax statement. In particular $q=0$ gives $e^*=1/2$; $q=M-r+1$ gives $e^*=0$. For $M=8,r=2,q=2$, $U=15/28$ and $e^*=15/43$. The subset sampler's computation/time and randomness-generation costs are **not** bounded by this query theorem.

## Exact MCSP / SAT transfer firewall

The source assignment domain $M=2^v$, the explicit 3-CNF formula encoding length $L$, and the target *complete* MCSP truth-table input length $N=2^n$ are distinct. A small formula can expose its SAT status syntactically or algebraically without treating its assignment-evaluation function as an opaque oracle. The algorithm here is not even required to charge internal computation, so the proven lower bound is only on **source oracle evaluations**. For $r=1$ it is at most linear in the oracle-table domain size $M$, and it does not produce an $N^{1.01}$ one-work-tape lower bound. It cannot be applied to ordinary SAT deciders, nor to a syntax-aware SAT-to-MCSP reduction, without showing that every relevant source operation is simulated by paid oracle probes and proving a threshold-, promise-, length- and model-preserving transfer.

A reduction producing Hamming-far Gap-MCSP NO instances must not silently be substituted for ordinary exact MCSP NO. The MMW search-MCSP hardness-magnification hypotheses also cannot be identified with decision-MCSP. The random sampler's physical generation and its adaptive branch computations have no time bound here. Natural-proofs and locality barriers constrain particular approaches but do not establish an unrestricted no-go.

## Primary-source theorem and model matrix

| Paper and verified location | Precise input and model, threshold or promise | Hypothesis and conclusion |
| --- | --- | --- |
| Cheraghchi, Hirahara, Myrisiotis, Yoshida, **STACS 2021 Theorem 1, printed p.23:3**, https://doi.org/10.4230/LIPIcs.STACS.2021.23 | Ordinary **exact** MCSP with full $N=2^n$ truth table, circuit gate threshold $2^{\mu_1 n}$ for some sufficiently small positive constant $\mu_1$, deterministic one-way read-only input plus one two-way work tape | **Conditional:** exclusion from $\mathrm{DTIME}_1[N^{1.01}]$ implies $P\ne NP$. Premise OPEN. |
| Same paper **Theorem 2, printed p.23:3** | Ordinary MCSP at a **different larger** $\mu_2$ close to 1, same one-way input and one work tape, two-sided randomized error | **Proved:** exclusion from $\mathrm{BPTIME}_1[N^{1.99}]$ at $\mu_2$; does not meet Theorem 1 threshold. |
| Same paper **Theorem 3, printed p.23:4** | For every $\mu>1/2$ and every oracle $O$, ordinary MCSP[$2^{\mu n}$], restricted oracle-query strings of length $N^{o(1)}$, randomized one-way-input one-work-tape | A restricted relativized lower bound $\mathrm{MCSP}[2^{\mu n}]\notin\mathrm{BPTIME}_1^O[N^{1+\mu'}]$ for some $\mu'>0$. Not an obstruction to all methods. |
| McKay, Murray, Williams, **STOC 2019 Theorems 1.2-1.3, pp.2-3**, https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf | Full $N=2^n$ table, one-pass **search-MCSP with oracle gates**, declared $s(n)\ge n$, poly($s$)-update and poly($s$)-space, oracle/class restrictions in paper | **Conditional** streaming-search lower bounds imply $P\ne NP$; no ordinary decision-MCSP result imported. |
| Chen, Hirahara, Oliveira, Pich, Rajgopal, Santhanam, **ITCS 2020**, https://doi.org/10.4230/LIPIcs.ITCS.2020.70 | Hardness magnification and locality/natural-proofs barriers in restricted circuit models | Scope context only; no theorem used in new minimax proof. |
| Allender and Hirahara, **MFCS 2017**, https://doi.org/10.4230/LIPIcs.MFCS.2017.54 | MCSP/MKTP approximation and nonuniform reductions, some conditional cryptographic hypotheses | Context only; neither ordinary MCSP NP-completeness nor transfer of MKTP lower bounds assumed. |

Primary CHMY and MMW original PDF theorem pages were inspected directly, including page images. No precise numerical value of $\mu_1$ is invented. No ETH, SETH, or cryptographic assumption is used in RMINIMAX42.

## Reproducible actual execution

**Standalone actually executed JavaScript**: experiments/tmr/tmr2_shared_sparse_minimax042.js. Hosted V8 ran this exact source; it is also Node.js compatible. **Raw immutable structured output**: results/raw/tmr/2026-11-14_1618_TMR2_RANDOM_SHARED_MINIMAX042_RAW.json.

**29,612 assertions and zero failures** over 330 parameter cases with $1\le M\le9$, all $1\le r\le M$, all $0\le q\le M$, totaling 348,502 exhaustive support-query-set pairs, 16,208 adaptive sparse-source executions using four fixed nonlinear salts, and 4,052 exact minimax-per-support equality checks. BigInt binomial arithmetic avoids rounding in combinatorial tests. These finite experiments are COMPUTATIONAL, not proof of an asymptotic SAT or MCSP lower bound or an executed physical Turing machine.

## Coordination, status, and next target

**Peer request:** TMR-5 independently review the randomized minimax proof, especially false-positive conditioning, the max inequality, and the equality sampler. TMR-4 attempt to falsify a purported syntax-aware reduction to full polynomial-output MCSP. TMR-3 audit randomness, source-query and physical tape charges before any runtime transfer.

**Next research target:** Attempt a fully charged, syntax-aware continuation invariant under arbitrary input rereads. Require a nontrivial post-acquisition lower bound that survives explicit proper-3-CNF forcing, Horn, XOR/Gaussian elimination, bounded treewidth and shared-product controls. **All unrestricted P-versus-NP load-bearing arrows remain OPEN.**

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Full proof1.txt and authentic recovered Git blobs of proof2.txt and canonical main.tex were inspected, as were AGENTS.md, CODEX.md, pnp skill, current MCSP directive, predecessor directive, latest issue #3 and five TMR handoffs. Both trackers and root main.tex were left unmodified, as were all five schedules.
