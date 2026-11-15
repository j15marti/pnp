# TMR-2/034: Typical-YES two-sided MCSP bit-probe frontier and a compact-boundary countercontrol

**2026-11-14 19:20 PST (America/Los_Angeles). TMR-2 Information Necessity.** Claim **EDGE-QUANTILE050**. Mathematical status **PROVED/RESTRICTED** (elementary finite-cube deduction, independent TMR-5/TMR-3 review OPEN). Finite native tests **COMPUTATIONAL**. **P versus NP remains OPEN.**

## The actual increment and attribution

Corpus search uncovered **MAGRED-EDGEADAPT8** at `research/agents/magnification-redteam/2026-10-18_1821_MAGRED_EDGEADAPT8.md`. Its Theorem 1 **already** proves the adaptive coupling $Q(f)\ge(1-e_Y-e_N)D_A(f)$ and the **average** hypercube edge bound $\mathbb E_{f\in A}Q(f)\ge(1-e_Y-e_N)(N-\log_2|A|)$. These inequalities are NOT new and must not be reassigned to TMR-2. The October note also checked some small NAND circuit classes whose every YES vertex had all $N$ single-flip neighbors outside YES, but did not claim this held generally.

**Genuinely new relative to that original:** an explicit **quantile / typical-YES corollary**, with asymptotic fractions quantified, independent native exhaustive testing of *all* vertex subsets of two small hypercubes, and a **basis-sensitive actual small-circuit falsifier**: at $n=3$ and size threshold two, the constant-zero table has **zero outgoing one-bit YES/NO edges**, whereas the class average satisfies the isoperimetric theorem. This demonstrates that the typical-YES guarantee cannot simply be upgraded to every YES via singleton flips. It also independently verifies the underlying original EDGEADAPT8 inequality in exact tiny circuit models.

## Input, model, and theorem

Let $n\ge1$, $N=2^n$, $s=\lfloor N^\mu\rfloor$ for fixed $0<\mu<1$, and $\mathcal Y\subseteq\{0,1\}^N$ be the ordinary exact MCSP YES truth tables satisfying $CC_n(x)\le s$. Put $m=|\mathcal Y|$. The circuit basis is a fixed complete finite fan-in-two basis; input wires and constants are free. Conservatively, for AND/OR/NOT gates, a syntactic count from TMR-2/033 gives
$$
1\le m\le D(n,s):=(s+1)(n+s+2)[3(n+s+2)^2]^s,
\qquad \log_2 D(n,s)=O_\mu(N^\mu\log N)=o(N).
$$

Consider **any** randomized adaptive, fixed-program, total, two-sided-error ordinary-MCSP decider $A$ whose only input channel supplies individual, charged bits of the complete explicit $N$-bit table. It may reread, preprocess, share, cache, recompute, or use unlimited finite-alphabet workspace. For every YES and every NO, its error is at most $0\le\delta<1/2$. Let $q_A(x,\rho)$ count **distinct input positions** actually read, not output bits, on random tape $\rho$. Physical time is at least the number of input-bit read events for a single sequentially stepping machine; random-access costs can only increase this charge. For multiple processors, only aggregate source-read work is bounded without a concurrency cap.

For any $t>0$, define the family of YES strings
$$
\mathcal G_t=\left\{x\in\mathcal Y:
|\{i\in[N]: x\oplus e_i\notin\mathcal Y\}|\ge N-t\right\}.
$$
Then
$$
\boxed{
\frac{|\mathcal G_t|}{m}\ge 1-\frac{\log_2m}{t},
\qquad
\forall x\in\mathcal G_t:\quad
\mathbb E_\rho q_A(x,\rho)\ge (1-2\delta)(N-t).
}
\tag{EDGE-QUANTILE050}
$$
When the first expression is negative, read it as the trivial nonnegative lower bound. For $t=\epsilon N$, its failure fraction is at most $\log_2m/(\epsilon N)$. In particular, choose
$$
\epsilon_N=N^{-(1-\mu)/2};
\quad
\frac{|\mathcal G_{\epsilon_NN}|}{m}
\ge1-O_\mu(N^{-(1-\mu)/2}\log N);
\quad
\mathbb E q_A(x,\rho)\ge(1-2\delta)(1-\epsilon_N)N
$$
on every $x$ in that $1-o(1)$ fraction of ordinary MCSP YES strings. **All asymptotics are in full truth-table length $N$, not in SAT description length $L$.**

### Proof (exact finite-dimensional, no unproved resource assumptions)

Draw $X$ uniformly from $\mathcal Y$. For any truth-table coordinate $i$, conditional on the other $N-1$ bits, the fiber of $\mathcal Y$ at $i$ has either one member (then $X_i$ is fixed) or two (then $X_i$ is fair). Consequently
$$
\Pr[X\oplus e_i\in\mathcal Y]
=H(X_i\mid X_{-i}).
$$
Conditioning cannot increase entropy; apply this for each $i$ against the ordinary chain-rule order:
$$
\sum_{i=1}^N H(X_i\mid X_{-i})
\le\sum_{i=1}^N H(X_i\mid X_1,\ldots,X_{i-1})
=H(X)=\log_2m.
$$
Hence the expected number of **internal** one-bit neighbors is at most $\log_2m$. Markov's inequality makes the fraction with more than $t$ internal neighbors at most $\log_2m/t$. Every remaining vertex has at least $N-t$ **external** (opposite-label) neighbors. This is exactly the old edge-isoperimetric/entropy statement plus a new quantile formulation, not a new edge theorem.

For any such $x$ and any external neighbor $y=x\oplus e_i$, couple the entire adaptive computations on $x,y$ using identical random bits. Without querying coordinate $i$, all answers, subsequent addresses, state updates, and final outputs coincide. Both coupled executions cannot simultaneously be correct because their labels differ. Thus
$$
\Pr_\rho[i\text{ queried on }x]
\ge1-\Pr[A(x)\ne\mathrm{YES}]-\Pr[A(y)\ne\mathrm{NO}]
\ge1-2\delta.
$$
Sum over distinct external coordinates to obtain the per-$x$ claim. This counts shared accesses only once and makes no claim that separate output-bit costs add. QED.

## Hostile countercontrol: why 'every YES' does not follow

In an explicit model with free input/constant wires and each gate permitted to implement **any** two-input Boolean operation, exhaustive circuits of at most **two gates** for $n=3$ give exactly **152** distinct YES truth tables out of $2^8=256$. The all-zero table has **all eight** single-bit flips still in this YES class: each is a three-literal minterm implemented with two binary AND-type gates (input negations are included in the truth-table gate basis). Hence its external one-bit boundary is **zero**, not $N-o(N)$. The overall class has mean external degree $3.368421...$ and maximum eight.

This does **not** contradict MAGRED-EDGEADAPT8 or EDGE-QUANTILE050, which are population/quantile statements. Earlier MAGRED NAND-basis tiny tests happened to give degree $N$ at every YES. The basis and gate cost matter at finite $s$, and even for large $s$ the low-complexity constant-zero function admits single-minterm changes with $O(n)$ gates. This example prevents a false generalization from those finite tests. The tiny all-binary-gates experimental basis is distinct from the asymptotic AND/OR/NOT count, and no small-instance statistics are imported as a universal MCSP theorem.

## Relation to TMR-2/033, TMR-5/030, FLMV and CHMY

- **TMR-2/033** proves on **every YES** an almost-$N$ source-read bound for randomized deciders with **no false-positive acceptance**. EDGE-QUANTILE050 instead permits **constant two-sided error** but obtains the near-linear result on a $1-o(1)$ fraction of YES tables, not every YES.
- **TMR-2/032** and **TMR-5/030** prove oracle-source minimax and communicating-network work-depth inequalities. The new transfer uses the complete explicit MCSP table and its Hamming-boundary geometry, not assignment-evaluation oracle access. Aggregated charged source work is $\Omega(N)$ for most YES tables, while network elapsed time requires a cap $K$ on simultaneous source reads to infer $\Omega(N/K)$.
- **CHMY STACS 2021 Theorem 1, printed p.23:3**: for some sufficiently small $\mu_1>0$, ordinary exact MCSP[$2^{\mu_1n}$] outside **deterministic** $\mathrm{DTIME}_1[N^{1.01}]$ (one-way read-only input plus one two-way writable tape) implies **P != NP**. **Theorem 2, same page** proves $\mathrm{BPTIME}_1[N^{1.99}]$ exclusion at a **different high** circuit threshold $\mu_2$, not the small-$\mu_1$ premise. Our lower bound is only input-access exponent **one**, not $1.01$, independent of how many YES tables it applies to.
- **MMW STOC 2019, Theorems 1.2-1.3** concern search MCSP with oracle gates and streaming algorithms using short $\Sigma_3\mathrm{SAT}$-oracle queries. Neither our decision bit-query theorem nor an assumption of ordinary MCSP NP-completeness substitutes for those premises.
- **FLMV JACM 2005** excludes certain *simultaneous* deterministic SAT time/space pairs on indexed random-access machines, with explicit encoded SAT formula bit length $L$. A near-linear information-acquisition lower bound on length-$N$ **MCSP truth tables** neither supplies an all-input SAT resource contraction nor a transfer from $N$ to $L$; the input bits already cost $\Theta(N)$ to stream. Any claimed FLMV contradiction requires a fully charged uniform SAT-machine construction and both-label correctness. This arrow remains **OPEN**.
- No Gap-MCSP, partial-MCSP, succinct-MCSP or MKTP inference: one-bit flips may fall in a promise gap, and their input lengths and computational tasks differ.

## Prior-work ledger and primary source matrix

| Original path/source | Actual established scope; status |
| --- | --- |
| `research/agents/magnification-redteam/2026-10-18_1821_MAGRED_EDGEADAPT8.md` Theorem 1 | **PROVED/RESTRICTED** earlier general adaptive neighbor-coupling and average hypercube entropy inequality. Explicit attribution; no duplicate novelty. |
| `research/main/2026-10-18_PARTIAL_SAMPLE_WEDGE7.md` | **PROVED/RESTRICTED** existing existence of an opposite-label single-flip MCSP pair and nonadaptive sampling barriers. Does not yield typical-YES quantile. |
| `research/agents/tmr-2/2026-11-14_1814_TMR2_ONE_SIDED_ACCEPT_FIBER033.md` | **PROVED/RESTRICTED** previous all-YES one-sided read certificate; no constant two-sided guarantee on all YES. |
| `research/agents/tmr-5/2026-11-14_1850_TMR5_NETWORK_WORK_DEPTH_ORACLE_AUDIT030.md` | **PROVED/RESTRICTED** zero-vs-singleton evaluation-only network $\mathbb E[KT]$; syntax-aware SAT gap explicitly retired. |
| Cheraghchi et al., STACS 2021, [publisher](https://doi.org/10.4230/LIPIcs.STACS.2021.23), Theorems 1-2 p.23:3 | **KNOWN THEOREM** exact MCSP on complete length-$N=2^n$ tables, one-way input/one work tape; small-$\mu_1$ $N^{1.01}$ hypothesis implies P != NP; proved randomized $N^{1.99}$ lower bound at larger $\mu_2$. |
| McKay, Murray, Williams, STOC 2019, [author PDF](https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf), Theorems 1.2-1.3 | **KNOWN THEOREM** search-MCSP with oracle gates, one-pass streaming/oracle update, not arbitrary exact-decision MCSP or source-evaluation SAT. |
| Fortnow, Lipton, van Melkebeek, Viglas, JACM 2005, [author PDF](https://lance.fortnow.com/papers/files/tst.pdf), Cor.5.8 | **KNOWN THEOREM** deterministic SAT joint time/space exclusion in an indexed random-access machine model, not an MCSP input query theorem. |
| Ellis, Keller, Lifshitz, JCTA 2019, [DOI](https://doi.org/10.1016/j.jcta.2018.12.001) | **KNOWN THEOREM** classical hypercube edge-isoperimetric inequality and refinements; the elementary entropy derivation is self-contained above. |

Original evidence in older TMR Walsh/moment (`research/agents/tmr-2/2026-11-14_0823_TMR2_MAXSAT_WALSH_SIGN_ROBUSTNESS022.md`), Claude ONETAPE/TPORT, and LSPV-3/615 genuine false-checker counterexample remains restricted or falsified at original scope. No inference from them to MCSP decision lower bounds is introduced.

## Actually executed test and immutable evidence

Native CPython on the exact source `experiments/tmr/tmr2_edge_boundary_audit050.py` produced `results/raw/tmr/2026-11-14_1915_TMR2_EDGE_BOUNDARY050_RAW.json`: **66,479 assertions, zero failures**. Exhausted **all 255 nonempty induced subgraphs** of the 3-dimensional hypercube and **all 65,535** of the 4-dimensional hypercube, checking the edge inequality. Separately exhaustively enumerated all 0/1-gate Boolean functions for $n=2,3,4$ (YES counts **16,38,70** with unrestricted binary gate truth tables) and 0/1/2-gate functions for $n=3$ (YES count **152**), with exact neighbor degrees. Independently checked a simple randomized mixture proxy at $\delta=1/3$. **Tests do not simulate a compiled Turing machine and do not establish asymptotics.** Exact CPython local file source Git blob `8ee44ed7f31647e307840fea4c3d5d129390afbf`; raw JSON Git blob `6fbc8ba7387e50246a73198602dae46ae17bf60d` if identical after publication readback.

## Preflight, root status, and next target

Read controlling Nov14 MCSP directive **FIRST**, SHA `1e11aa64a0b0d635a65cea58500b09f2b0fe010a`, then Nov13 replacement, AGENTS.md, CODEX.md, repository skill, all current TMR handoffs, latest issue #3, original TMR and historical exact reports, primary CHMY/MMW PDFs and their source theorem pages. Root `proof1.txt` fully read (28,714 chars, SHA `06f7ebc8c2283304a0f5200b518c6e48fa41e343`); `proof2.txt` recovered from authentic Git blob (1,051,196 chars, SHA `930c5eeddafce656717f28055a7a9a755f44737c`); canonical `main.tex` recovered from authentic Git blob (2,545,859 chars, SHA `6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34`). **TRACKERS REVIEWED; NO MATERIAL CHANGE.** No root main.tex edit, no scheduled-agent mutation.

**Next target and peer request:** TMR-5 independently check the quantile deduction and the $n=3,s=2$ zero-boundary counterexample against exactly the stated binary-gate basis; TMR-3 verify aggregate bit-acquisition work versus network elapsed-time claims; TMR-1 verify low-$\mu_1$ parameter and no mixing of full truth-table $N$ with succinct SAT source $L$; TMR-4 attempt a syntax-aware, charged, both-label bridge before treating the quantile information bound as an MCSP hardness-magnification premise. **Unrestricted post-ingress computational lower bound $N^{1.01}$ at small $\mu_1$ remains OPEN; P versus NP remains OPEN.**

END_OF_REPORT::TMR2::034::2026-11-14_1920_PST
