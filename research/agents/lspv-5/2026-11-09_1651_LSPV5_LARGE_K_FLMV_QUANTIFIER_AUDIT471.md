# LSPV-5/471: large-$k$ FLMV quantifier and abstract-space audit

**November 9, 2026, 16:51 PST | Independent Proof Red Team | CONDITIONAL exact recurrence theorem + COMPUTATIONAL controls | P versus NP OPEN**

**Affected tracker evidence:** new [P2-L5-471], refining [P2-A2] and [P2-A3]. [P1-01], [P1-03], [P1-04], [P2-A2], [P2-D1], [P2-C3], [P2-B1] and [P2-B2] remain OPEN.

## IDEA, quantifiers and falsifiers

**Initial hypothesis.** If the exact same-machine transformation postulated by open node [P2-A2] is effective and recursively applicable, then every hypothetical uniform total deterministic polynomial SAT decider with fixed finite exponents $(t_0,s_0)$ reaches the strict FLMV-forbidden region after finitely many rounds, even when the exponents are very large. The number of rounds may depend on the fixed algorithm, but not on input length.

The exact prefix is

$$
\forall A\ \forall t_0,s_0<\infty\;
\bigl[H(A,t_0,s_0)\wedge \text{[P2-A2]}
\Rightarrow \exists r<\infty\;C(\Phi^r(A))\bigr],
$$

not $\exists r\,\forall A$. Here $H$ includes uniformity, total SAT/UNSAT/malformed correctness and simultaneous same-machine exponent bounds, while $C$ is the strict FLMV contradiction.

Falsifiers fixed before search:

1. the closed-form recurrence fails because the max branches change;
2. the boundary $\beta(t)>1/2$ has been solved with the wrong polarity;
3. one finite $r$ works for unbounded initial exponents;
4. the abstract recurrence has been mistaken for a proved concrete machine transformer, or nondeterministic witness verification has leaked into deterministic UNSAT.

F1 and F2 were rejected symbolically and by two implementations. F3 is false by an explicit all-$r$ counterfamily. F4 remains the load-bearing OPEN blocker and therefore prevents any separation claim.

## SEARCH and corpus reconciliation

Read the complete new governing handoff `research/coordination/2026-11-09_1624_ASSUMED_TIME_DERIVE_SPACE_FLVM_FIVE_ROLE_HANDOFF.md` (blob `644b0d4745f2edeb8718c7e536a7da995b36b36f`), complete root `proof1.txt` (startup blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`) and `proof2.txt` (startup blob `d1dc2364acc563f883bde1324d17d740efda8f81`), the November 2 five-role handoff, `AGENTS.md`, `CODEX.md`, project research protocol and red-team mode. The local preflight failed because the scheduled workspace is not a full checkout; all governing files and root `main.tex` were instead fetched as complete GitHub blobs. Current issue #3 was read through comment `6755610427` after the high-level comments endpoint twice closed its transport; paged GitHub REST readback succeeded.

Actual peers: LSPV-1/548 owner-bound bit-PHP/ER shortcut, LSPV-2/531 source-sign query bound, LSPV-3/544 typed owner/context whole-DAG abstraction, and prior LSPV-5/470 proper-projection precision obstruction. Current Grok `research/agents/grok/2026-10-23_1915_GROK_REWIRE.tex` concerns circuit rewriting and does not provide the missing all-input contraction. Claude WORLD-LEDGER and TPORT files classify alternation-trading scope and explicitly separate decision portfolios from witness search.

Primary literature read for exact scope:

- Fortnow--Lipton--van Melkebeek--Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6), 2005, DOI `10.1145/1101821.1101822`: deterministic random-access SAT time--space lower bounds; a separate conondeterministic regime has different constants.
- Fortnow--van Melkebeek, DIMACS TR 2000-06: explicitly states $b<((a+2)/a^2-a)/2$ for the earlier positive-space tradeoff.
- Williams, *Inductive Time-Space Lower Bounds for SAT and Related Problems*, and Buss--Williams, *Limits on Alternation-Trading Proofs*: the later $2\cos(\pi/7)\approx1.8019$ record concerns $n^{o(1)}$ space and the latter proves a limit of the alternation-trading proof method. It is not a replacement formula for positive $s=1/2$.
- Cousot--Cousot (POPL 1977), D'Silva--Haller--Kroening ACDCL (POPL 2013) and Abstract Satisfaction (POPL 2014): sound abstraction/fixed-point methodology, not a SAT complexity lower bound.

Required repository delta review: `konard/p-vs-np` head `ecedd2b45f1c524d85c00b2da27a9c140025550c` still labels NP $\subseteq$ P unknown and its experiments non-solutions; `blkph0x/p-vs-np-proof-research` head `7dedc73f758dfbdc072e7aa29dfc08505761ebd5` explicitly scopes its method ledger to promised/family results; `meelgroup/frat-xor` head `18cd6bc17af10a9891c10a846ce966166f9fe0dc` is a proof-format/checker corpus, not a machine-space theorem; `openai/math` head `4eaee87548250b2682affda7d05d947c05554bae` supplies no relevant result. No repository changed the FLMV quantifier gap.

## Concrete complete configurations

For fixed binary source $x$ and fixed native random-access machine $M$, a deterministic complete configuration is

$$
\sigma=(M,x,N,q,\mathbf h_I,\mathbf h_W,W,\ell_W,\mathsf{stack},\mathsf{out},\tau,\mathsf{parse},\mathsf{auth}),
$$

where $q$ is the finite control, $\mathbf h_I$ contains read-only input/index heads, $\mathbf h_W$ all work/index heads, $W$ is the exact work-tape store, $\ell_W$ records live allocation and every tape high-water charged by the model, `stack` includes recursive frames and retained child data, `out` is the output state, $\tau$ is real transition count, `parse` includes malformed status, and `auth` binds the exact input and every assumption. The deterministic transition is a partial function completed by explicit HALT/ERROR states. Peak work space is the maximum charged work high-water over the whole trace, not final live bits or the logarithm of a configuration count.

A nondeterministic configuration additionally has a read-only certificate/choice policy and branch-local choice history. Its collecting successor is a set of branch configurations. SAT acceptance is existential over branches; UNSAT requires absence of accepting branches. Joining branch-local facts without their choice contexts is unsound, and this model is not a deterministic UNSAT decider.

## Abstract domain, alpha/gamma and resource polarity

Let $C=\mathcal P(\mathrm{Trace})$ ordered by inclusion. The abstract domain records

$$
a=(\mathsf{machineID},\mathsf{D/N},\mathsf{sourceAuth},\mathsf{correctness},
[t_-,t_+],[s_-,s_+],\mathsf{phaseLedger},\mathsf{contexts}).
$$

$\alpha(X)$ retains exact machine/determinism/source tags and takes sound extrema of real time and all-phase peak space over $X$; $\gamma(a)$ is the set of complete traces consistent with every tag and interval. With larger upper endpoints ordered upward, a sound may transformer satisfies

$$
\alpha(\operatorname{Post}(X))\sqsubseteq F^\#(\alpha(X)).
$$

This supports **upper** resource certification only when every concrete transition, parsing phase, buffer, work-head high-water, recursive frame, recomputation and output is covered. A necessary lower bound such as FLMV has the opposite use: under its exact deterministic same-machine hypotheses, a claimed upper pair $(t,s)$ is impossible when $s<\beta(t)$. Neither a may overapproximation that fails to decide nor configuration cardinality yields a concrete space lower bound. Abstract Satisfaction may organize deduction/abduction/refinement of reachable states, but does not create the missing compiler or convert an NP witness into deterministic UNSAT evidence.

The proposed recurrence

$$
F^\#(t,s)=\left(\max\{11/10,3/5+t/2\},\max\{1/2,s/2\}\right)
$$

is therefore an admissible abstract transformer **only conditional on** a concrete $\Phi$ satisfying the simulation and full-cost inequality. At present it is a target specification, not proved abstract soundness.

## Theorem 471.1: exact boundary above one-half

For $c>0$,

$$
\beta(c)>\frac12
\iff c^3+c^2-c-2<0.
$$

The derivative $3c^2+2c-1$ is positive for $c\ge1$, so the cubic has a unique root $c_\dagger>6/5$ in this range. Exact bisection gives

$$
c_\dagger=1.2055694304005903117\ldots.
$$

Thus $6/5\le c<c_\dagger$ is the interval relevant to a space upper exponent $1/2$. Separately, $\beta(6/5)=23/45=1/2+1/90$.

## Theorem 471.2: finite rounds for each fixed exponent, not uniformly

Assume $t_0\ge6/5$ and $s_0\ge1/2$. The max branches give exactly

$$
t_r=\frac65+\frac{t_0-6/5}{2^r},
\qquad
s_r=\max\left\{\frac12,\frac{s_0}{2^r}\right\}.
$$

Choose $r$ so that

$$
2^r>\frac{t_0-6/5}{c_\dagger-6/5},
\qquad
2^r\ge2s_0.
$$

Then $t_r<c_\dagger$ and $s_r\le1/2<\beta(t_r)$. Hence every fixed finite initial pair reaches the forbidden region after a finite $r=O(\log(t_0+s_0+2))$, **conditional on every concrete iteration being legal**.

There is no uniform finite $r$. Fix any $r$ and take

$$
t_0=\frac65+2^r(c_\dagger-6/5).
$$

Then $t_r=c_\dagger$ and $\beta(t_r)=1/2$, not the strict inequality. Larger $t_0$ stays outside. Similarly $s_0>2^{r-1}$ keeps the space envelope above $1/2$. This explicitly falsifies $\exists r\,\forall(t_0,s_0)$ while preserving $\forall(t_0,s_0)\,\exists r$.

For the user's notation, $O(N^k)$ with $k\to\infty$ is not one P bound if $k=k(N)$ is unbounded. P is the union over machines with some fixed finite exponent. Across that union, the required conditional iteration count is unbounded, but each particular machine has a finite count.

## Theorem 471.3: assumed time does not calculate space

Conditional on any correct deterministic decider $A$ running in $O(N^k\operatorname{polylog}N)$, and any $0<q\le k$, construct $A^{\mathrm{pad}}_q$: on length $N$, sequentially touch and retain $\lfloor N^q\rfloor$ fresh charged work cells, then run $A$. This is uniform, total and language preserving. It has time $O(N^k\operatorname{polylog}N)$ and peak work space at least $\Omega(N^q)$ on the same model. Therefore the same time upper exponent is consistent with many space exponents. The trivial operational upper $S\le O(T)$ (or machine-specific word-bit variant) is not the desired low-space bound. This wrapper does not say a low-space implementation cannot exist; it proves that time alone does not determine it.

## Exact and illustrative controls

Two independent programs agree:

| initial $t_0=s_0=k$ | first conditional forbidden round | $t_r$ | $s_r$ | $\beta(t_r)$ |
|---:|---:|---:|---:|---:|
| 2 | 8 | 1.203125 | 0.5 | 0.504864 |
| 10 | 11 | 1.204297 | 0.5 | 0.502529 |
| 100 | 15 | 1.203015 | 0.5 | 0.505083 |
| 1000 | 18 | 1.203810 | 0.5 | 0.503498 |
| $10^6$ | 28 | 1.203725 | 0.5 | 0.503667 |

Python checked 223 exact-rational assertions; independently authored Node checked 98 floating controls. For all $r=0,\ldots,40$, the counterchoice $t_0=6/5+2^r/100$ gives $t_r=1.21$ and $\beta(t_r)<1/2$.

At the fixed point, the exponent-only comparison is:

| $N$ | $N^{1/2}$ | $N^{23/45}$ | ratio $N^{1/90}$ |
|---:|---:|---:|---:|
| $10^6$ | $10^3$ | $1.1659\cdot10^3$ | 1.1659 |
| $10^{12}$ | $10^6$ | $1.3594\cdot10^6$ | 1.3594 |
| $10^{24}$ | $10^{12}$ | $1.8478\cdot10^{12}$ | 1.8478 |
| $10^{60}$ | $10^{30}$ | $4.6416\cdot10^{30}$ | 4.6416 |

These are not bytes or measured memory. Constants, word size, polylogarithms and the theorem's asymptotic quantifiers remain uninstantiated.

## ITERATE: revised claim and remaining gap

The initial idea survives only in this precise form:

- **CONDITIONAL/PROVED arithmetic:** for each fixed finite exponent pair, recursive recurrence bounds eventually conflict with FLMV; no uniform finite round covers unbounded exponents.
- **FALSIFIED inference:** an assumed polynomial time bound does not calculate $S$, and an NP verifier does not supply deterministic UNSAT or deterministic FLMV premises.
- **OPEN:** [P2-A2] must still provide one effective exponent-oblivious $\Phi$ that maps every fixed uniform total deterministic SAT decider to another such decider, on the exact machine, with both recurrence inequalities and all-phase peak-space accounting, and remains recursively applicable. Constants may depend on the fixed program and selected finite round, but not on input size.

The later $n^{2\cos(\pi/7)-o(1)}$ lower bound for $n^{o(1)}$ space is stronger along the subpolynomial-space axis but does not certify a positive $N^{1/2}$ upper or extend $\beta$ to large $k$. The two results must not be spliced across different space regimes.

## Resources and publication scope

Logical arithmetic: 223 exact Python + 98 independent Node assertions. Evidence bits are the two source files and compact JSON. Search/construction was under one second per program; parsing, repository reads, literature reads, output and publication are separately logged above. Peak experiment memory is ordinary interpreter memory and is not a native FLMV measurement. No historical R_mix341 rule or weight was used or changed. No automation, role, title, schedule, timezone or enabled state was modified.

Code: `experiments/review/lspv5_471_large_k_flmv_recurrence.py`; independent verifier: `experiments/review/verify_lspv5_471_large_k_flmv.mjs`; raw: `results/raw/arc/2026-11-09_1651_LSPV5_471_LARGE_K_FLMV_RAW.json`; handoff: `research/coordination/2026-11-09_1651_LSPV5_LARGE_K_FLMV_QUANTIFIER_HANDOFF471.md`.

**Final status:** actual advance is the exact $\forall(t_0,s_0)\exists r$ theorem, explicit $\neg\exists r\forall(t_0,s_0)$ counterfamily, and time-does-not-determine-space wrapper. The concrete compiler remains OPEN. P versus NP remains OPEN.
