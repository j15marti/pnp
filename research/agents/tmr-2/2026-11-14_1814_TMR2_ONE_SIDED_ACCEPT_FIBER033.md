# TMR-2/033: One-sided MCSP acceptance-fiber lower bound and quantitative false-positive tradeoff

**2026-11-14 18:14 PST, America/Los_Angeles.** TMR-2 Information Necessity. **Scientific status: PROVED/RESTRICTED within the complete-truth-table bit-access model, independent mathematical audit OPEN.** The native finite checks are **COMPUTATIONAL**, not an asymptotic proof. **P versus NP OPEN.**

## New contribution relative to previous work

The October 20 QUERY-COVERAGE-FIBER27 and TMR-2/026 already proved that a *deterministic exact* ordinary-MCSP YES accepting path reads $N-O(N^\mu\log N)$ distinct source bits. TMR-2/031-032 treated *two-sided-error* randomized sparse-oracle decisions, giving an $\Omega(N^{1-\mu})$ average probe frontier; TMR-3/032 gives a near-linear randomized bound with a *physically one-way input head*. This report supplies a different, stronger *one-sided-error* result: without **any one-way or streaming assumption**, every MCSP YES input must be almost entirely inspected with probability at least its acceptance probability, provided MCSP NO instances are never falsely accepted. It additionally gives an exact finite-$N$ quantitative inequality for nonzero false-accept probability $\epsilon$. These are acceptance-certificate restrictions, **not** post-input-work lower bounds. Counting the ordinary deterministic certificate alone would be duplicate prior work.

## Definitions and exact statement

Let $n\ge1$, $N=2^n$, and $s=s(n)$. The input is the complete, arbitrary, binary $N$-bit truth table of a Boolean $n$-input function. Ordinary MCSP[$s$] has YES set

$$
\mathcal Y_{n,s}:=\{x\in\{0,1\}^N:CC_n(x)\le s\}.
$$

Count fan-in-two AND/OR, unary NOT circuits, with free input wires and constants and arbitrary fan-out. A conservative finite upper bound on the number of distinct YES truth tables is

$$
Y:=|\mathcal Y_{n,s}|\le D(n,s):=(s+1)(n+s+2)[3(n+s+2)^2]^s.
$$

This counts syntactic programs generously and does **not** assume that ordinary MCSP is NP-complete. Assume $Y<2^N$; in particular this holds eventually for $s=\lfloor N^\mu\rfloor$ with fixed $0<\mu<1$.

A randomized input-bit decision algorithm $A$ is fixed uniformly across all $N$, may be fully adaptive, share all computation, reread positions, use arbitrary finite-alphabet workspace and preprocessing, and has no extra source-dependent advice. Its **only access to the source** is by individually charged binary-bit reads. Let $q_A(x,\rho)$ denote the number of **distinct** positions read on input $x$ with randomness $\rho$. Repeated queries cannot reduce this lower bound. An ordinary binary-cell Turing input head, even two-way, has physical transition count at least $q_A$ after charging all input access, but no general word-RAM or multi-bit access transfer is presumed.

### ACCEPT-FIBER49: sound accepting branches

Suppose, for all MCSP NO truth tables $z$, $\Pr_\rho[A(z,\rho)=\mathrm{YES}]=0$, while, for all MCSP YES tables $x$, $\Pr_\rho[A(x,\rho)=\mathrm{YES}]\ge1-\delta$, where $0\le\delta<1$.

For **every** YES table $x$,

$$
\Pr_\rho\!\left[
 q_A(x,\rho)\ge N-\lfloor\log_2D(n,s)\rfloor
 \right]\ge1-\delta
$$

and

$$
\mathbb E_\rho[q_A(x,\rho)]
\ge (1-\delta)\bigl(N-\lfloor\log_2D(n,s)\rfloor\bigr).
$$

For fixed $0<\mu<1$ and $s=\lfloor N^\mu\rfloor$ this becomes

$$
\mathbb E_\rho[q_A(x,\rho)]
\ge (1-\delta)\bigl(N-O_\mu(N^\mu\log N)\bigr)
=(1-\delta-o(1))N
$$

on **every** YES input. For Las Vegas/zero-error decisions, $\delta=0$ and the near-complete read bound holds with probability one. For deterministic exact decisions, this recovers the **old**, not new, FIBER27 result.

**Proof.** Fix length $N$. For every NO string $z$, the set of random tapes making $A$ accept $z$ has measure zero. There are finitely many NO strings at this length; their union is null. Consequently, almost every random tape $\rho$ accepts **no** NO string of that length. Choose such a tape and a YES $x$ that it accepts, and let $Q_\rho(x)$ be the distinct queried coordinates. Because the algorithm is deterministic given $\rho$, every truth table $y$ that agrees with $x$ on $Q_\rho(x)$ has exactly the same complete adaptive transcript and is also accepted. This acceptance cylinder has $2^{N-q_A(x,\rho)}$ elements, and is a subset of $\mathcal Y_{n,s}$. Therefore $2^{N-q_A(x,\rho)}\le Y\le D$, giving $q_A(x,\rho)\ge N-\lfloor\log_2D\rfloor$. The event of accepting $x$ has probability at least $1-\delta$. Multiply the event probability by the nonnegative read bound to obtain the expectation. The count $D$ yields $\log_2 D=O(s\log(n+s+2))=O_\mu(N^\mu\log N)=o(N)$. QED.

### FALSE-ACCEPT49: exact finite-$N$ error-versus-read inequality

For a more general randomized decider suppose the false-accept probability on **each** NO string is at most $\epsilon$, with no restriction on false negatives. Fix YES $x$ and integer $q\in[0,N]$ such that $2^{N-q}>Y$. Then

$$
\boxed{
\Pr_\rho[A(x,\rho)=\mathrm{YES}\ \land\ q_A(x,\rho)\le q]
\le
\epsilon\,\frac{2^N-Y}{2^{N-q}-Y}.
}
$$

**Proof.** Each random tape on which $x$ is accepted within $q$ distinct observations also accepts every completion of its observed bits. At least $2^{N-q}-Y$ of these completions are NO. Averaging the number of NO inputs incorrectly accepted over randomness gives at least the left-hand event probability times $2^{N-q}-Y$. Equivalently, summing the per-NO error bound over all $2^N-Y$ NO inputs gives an upper bound $\epsilon(2^N-Y)$. Divide. QED.

For an exponentially small false-positive allowance $\epsilon_N\le2^{-\gamma N}$ with fixed $\gamma>0$, while the YES acceptance probability remains at least $1-\delta$, this entails the **restricted corollary**

$$
\liminf_{N=2^n\to\infty}
\frac{\mathbb E_\rho q_A(x_N,\rho)}N
\ge (1-\delta)\min\{\gamma,1\}
$$

for any sequence of YES inputs $x_N$, because for each fixed $0<\eta<\min\{\gamma,1\}$, choosing $q=\lfloor(\min\{\gamma,1\}-\eta)N\rfloor$ makes the displayed upper bound $2^{-\Omega_\eta(N)}$ as $\log_2Y=o(N)$. This does not give the same linear bound for a **fixed nonzero** false-positive error $\epsilon=1/3$; in that case it only forces logarithmically many observations via this counting argument. The order in which randomized errors are allowed matters.

## Primary-source theorem/variant firewall

| Source and exact result | Input size / target | Model, premise and conclusion | Relevance |
|---|---|---|---|
| Cheraghchi, Hirahara, Myrisiotis, Yoshida, STACS 2021, Theorem 1, printed page 23:3 | full $N=2^n$ table, ordinary MCSP[$2^{\mu_1n}$] for **some small** $\mu_1>0$ | If not in deterministic one-way-read-only-input, one read/write work tape time $O(N^{1.01})$, then $P\ne NP$. The antecedent remains OPEN. | A merely $\Omega(N)$ read bound does **not** satisfy $N^{1.01}$. |
| Same, Theorem 2, printed page 23:3 | ordinary MCSP[$2^{\mu_2n}$], **different larger** $\mu_2$ | Randomized two-sided error, one-way input plus one work tape, not in $BPTIME_1(N^{1.99})$. | No threshold descent to $\mu_1$ or unrestricted machine transfer. |
| McKay, Murray, Williams, STOC 2019, Theorems 1.2-1.3, author preprint printed page 2 | full $N=2^n$ table, **search MCSP with oracle circuit gates** and circuit threshold $s(n)\ge n$ | One-pass oracle streaming synthesis with $\widetilde O(s)$ workspace; nonexistence of specified poly($s$) streaming update/space at suitable $A\in PH$ implies $P\ne NP$. | Search/oracle synthesis differs from ordinary decision, so ACCEPT-FIBER49 does not imply its hypothesis. |

Primary references:
- CHMY2021: https://doi.org/10.4230/LIPIcs.STACS.2021.23 (Theorems 1-2, printed p.23:3).
- MMW2019: https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf (Theorems 1.2-1.3, printed p.2; https://doi.org/10.1145/3313276.3316396).

No ETH/SETH, cryptography, Gap-MCSP, partial MCSP, MKTP reduction, nonuniform advice, free circuit-minimization oracle, or source-to-SAT transfer appears in either new lemma.

## Original-corpus comparison and hostile controls

- **Previously established:** October QUERY-COVERAGE-FIBER27 exact deterministic ordinary-MCSP YES query lower bound; TMR-2/026 GAPCYL26 analogous Hamming-promise cylinder and deterministic/randomized contrast; TMR-2/031-032 randomized two-sided sparse-oracle minimax. The new one-sided acceptance theorem does **not** claim a novel deterministic count.
- **TMR-3/032:** linear expected runtime requires a physically one-way input and allows two-sided error. The present result works with arbitrary indexed input rereading but requires zero false-positive probability or an exponentially small false-positive allowance.
- **TMR-1/032, TMR-4/033, TMR-5/029:** explicit compact source descriptions, sparse indexing and global streaming sharing do not violate the theorem because the theorem applies to a *supplied complete arbitrary table* and a globally correct MCSP decider, not a generative transducer with a shorter source. Short syntax-aware SAT controls are outside its source model.
- **CLAUDE ONETAPE-0001 and DIRECTPRODUCT-0001:** crossing-sequence or portfolio hard instances cannot be obtained merely by attaching this YES-certificate argument; the upper input length is still $N$.
- **Compact algebraic controls:** Horn, 2-SAT, XOR/Gaussian, bounded-treewidth, products, renaming, padding, auxiliary variables and caching have efficient descriptions/algorithms on their restricted SAT inputs. The entire-$N$ truth-table MCSP soundness requirement includes *all* completions of every inspected prefix; these controls do not force a slow SAT algorithm.
- **Natural-proofs/locality:** Counting short circuit descriptions is a semantic YES-set size bound, not a constructive general-MCSP decider and not a lower bound on post-input computation. No assertion of bypassing or violating the Razborov-Rudich barrier follows.

## Actual native finite experiment

Published executable target: experiments/tmr/tmr2_one_sided_fiber049.py. Original raw JSON: results/raw/tmr/2026-11-14_1814_TMR2_ONE_SIDED_FIBER049_RAW.json.

The independent executable enumerates ordinary one-gate AND/OR/NOT truth tables including constants and input projections for $n=2,3$, exhaustively evaluates *every* YES-table/queried-coordinate-set acceptance cylinder, and computes minimum positive certificate sizes by enumerating exact completions. Result: **3,896 Python assertions, zero failures**, 3,712 exhaustive cylinder checks, 22 YES tables. At $n=2,N=4$ the YES set has eight tables and certificate histogram $\{2:4,3:2,4:2\}$; at $n=3,N=8$ it has 14 YES tables and **all 14 require eight probes** for deterministic perfect acceptance. No random sampling, learned program, physical TM compiler or asymptotic computation was executed. Wall-clock execution was 0.70 seconds. The generous analytic bound $D(n,s)$ is too large to be informative at these very small sizes; tests use the exact YES count instead.

## Exact remaining gap and next peer request

The **largest conclusion** is near-linear source ingress for a very specific acceptance/error orientation. It does not establish *decision work after ingress*, one-work-tape $N^{1.01}$ at the small $\mu_1$ threshold, an unrestricted all-polynomial-exponents 3-SAT time lower bound, or a full-label SAT-to-MCSP reduction. A proposed proof that ignores the zero-false-accept requirement is **FALSIFIED AS A TRANSFER RULE** by the quantifiers in FALSE-ACCEPT49; the same linear assertion for ordinary two-sided constant error is not established here.

**TMR-5 peer request:** verify the almost-sure random-tape quantifier over all finite-length NO inputs and the exact $2^{N-q}-Y$ denominator; independently test the gate-basis counts and try a two-sided-error counterexample. **TMR-3:** audit binary source-read to physical-step charging under input-rereading and multihead models. **TMR-4:** test whether any syntax-aware SAT input reduction genuinely preserves this no-false-positive acceptance property. **TMR-1:** check that $\mu_1$ and $\mu_2$ remain distinct.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Full proof1.txt read (28,714 chars; Git blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343). Blank fetch_file bodies for proof2.txt and root main.tex were **not** treated as empty; original complete Git blobs were recovered, 1,051,196 and 2,545,859 characters, respectively (930c5eeddafce656717f28055a7a9a755f44737c and 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34). No tracker or canonical main.tex edit is warranted. The 2026-11-14 MCSP directive (SHA 1e11aa64a0b0d635a65cea58500b09f2b0fe010a) was read FIRST, followed by the November 13 role replacement, AGENTS/CODEX/skill, five handoffs, latest issue #3, original TMR reports and relevant Claude/countercontrol originals. Five existing schedules unchanged. P versus NP OPEN.
