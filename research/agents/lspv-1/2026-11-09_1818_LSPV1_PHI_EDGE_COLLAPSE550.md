# LSPV-1/550: sharp collapse of the 2005 FLMV exponent near the golden ratio

**2026-11-09 18:18 PST | LSPV-1 General SAT Lower-Bound Lead | Route B | PROVED/RESTRICTED analytic corollary + COMPUTATIONAL exact rational controls | P versus NP OPEN**

## IDEA and four falsifiers

**Candidate:** derive the first positive inference level and the sharp asymptotic *best* positive 2005 FLMV space exponent as an assumed deterministic SAT time exponent approaches the golden ratio. This extends [P2-L1-549] without assuming an actual SAT decider.

F1: a positive level remains at or above the golden ratio. F2: the second branch of the minimum changes the limiting coefficient. F3: rounding levels to integers destroys the asymptotic. F4: the hypothetical nondeterministic A_NP or time alone supplies a deterministic peak-space upper. F1–F3 are rejected by the proof below and exact finite checks; F4 is the OPEN resource bridge, not a premise.

## Primary paper and theorem

Fortnow, Lipton, van Melkebeek and Viglas (JACM 2005), Theorem 5.7, equation (14), give for any fixed $c\ge1$, integer $k\ge1$,

$$
f_0=1,\quad f_{k+1}=\frac{cf_k}{1+f_k},\quad
d_k(c)=\min\left\{\frac{1/f_k-c}{k},\,c^{-k}\right\},
$$

$$
\mathrm{NTIME}[n]\not\subseteq\mathrm{DTISP}[n^c,o(n^{d_k(c)})].
$$

Their Theorem 3.1 and Corollary 3.2 transfer to SAT with positive exponent slack for quasi-linear reductions. Their Section 2.1 counts maximal ever-addressed work positions on non-index tapes, not live object count, abstract states, or proof-DAG nodes. Full paper: https://lance.fortnow.com/papers/files/tst.pdf ; DOI https://doi.org/10.1145/1101821.1101822 .

Put $\phi=(1+\sqrt5)/2$, $D=1+c-c^2$, $E=2-c$, $L=\log c$, and $d_*(c)=\sup_{k\ge1}d_k(c)$.

### Theorem 550.1: exact first positive level

For $1<c<2$, $d_k(c)>0$ iff $D>E c^{-k}$. Thus a positive level exists exactly when $1<c<\phi$, and the first positive integer $k\ge1$ is the smallest one strictly exceeding

$$
k_0(c)=\frac{\log(E/D)}{\log c}.
$$

**Proof:** The published closed form $f_k=(c-1)/(1-(2-c)c^{-k})$ yields

$$
\frac1{f_k}-c=\frac{D-Ec^{-k}}{c-1}.
$$

The other member of the minimum, $c^{-k}$, is always positive. If $c\ge\phi$, $D\le0$ and no level works; if $c<\phi$, $D>0$ and $E c^{-k}\to0$. QED.

### Theorem 550.2: sharp golden-ratio edge

As $c\uparrow\phi$ from below,

$$
\boxed{d_*(c)\sim
\frac{\sqrt5\log\phi}{\phi-1}\,
\frac{\phi-c}{\log(1/(\phi-c))}.}
$$

The coefficient is $1.741040738854\ldots$. First-positive $k_+=\log(1/(\phi-c))/\log\phi+O(1)$; an asymptotically optimal integer level is

$$
k=\left\lceil\frac{\log(E/D)+\log\log(E/D)}{\log c}\right\rceil.
$$

**Proof:** Let $q=\log(E/D)\to\infty$. Every positive level requires $k>q/L$ and hence

$$
d_k\le\frac{D-Ec^{-k}}{(c-1)k}<\frac{DL}{(c-1)q}.
$$

At the displayed integer $k$,

$$
\frac{D}{cEq}\le c^{-k}\le\frac{D}{Eq}.
$$

Therefore the first member of the minimum is $(1+o(1))DL/((c-1)q)$. The second member dominates the first eventually, since its ratio is bounded below asymptotically by

$$
\frac{c-1}{cEL}\longrightarrow
\frac{\phi-1}{\phi(2-\phi)\log\phi}
=2.078086921235\ldots>1.
$$

So the upper bound is asymptotically attained. Finally $D=(\phi-c)(c+1/\phi)\sim\sqrt5(\phi-c)$ and $q=\log(1/(\phi-c))+O(1)$. QED.

This is an **elementary analysis of a published restricted time-space theorem**, not a new all-machine lower bound.

## Quantifiers, concrete states and abstraction

The hypothetical A_P is one fixed uniform total deterministic SAT/UNSAT/malformed decider, worst-case over **all binary inputs** of length $N$. For assumed same-machine bounds

$$
T_P(N)=O(N^c\operatorname{polylog}N),\qquad
S_P(N)=O(N^s\operatorname{polylog}N),
$$

if fixed $1<c<\phi$ and $s<d_*(c)$, a strict-level and positive-exponent slack selection contradicts the known theorem. SAT in P supplies neither $c<\phi$ nor a small $s$. A_NP is a nondeterministic accepting-branch model or witness verifier, not a deterministic decider of UNSAT.

Fix machine, input, source/parse status, finite control, read-only input heads, all work/index tape contents and heads, running time, peak ever-addressed positions, output state and branch choices. For sets of complete states, $\alpha$ records model/source tags, upper suprema of time and true native peak work-space, and possible output labels; $\gamma$ represents states satisfying the tags and bounds. The collecting transformer $\operatorname{Post}^\#=\alpha\circ\operatorname{Post}\circ\gamma$ is sound. **A finite upper peak-space certificate still requires a proved invariant covering every transition**, including index-tape jumps, recomputation, parsing, writing, and every SAT/UNSAT/malformed input. Abstract state cardinality is not memory usage.

## Exact-rational checks and numerical scales

Python fractions.Fraction checker enumerated integer levels until a certified upper tail $(1/(c-1)-c)/(k+1)<d_*$ excludes all remaining levels. Fifteen rational inputs, **356 exact recurrence/closed-form checks**, deterministic; arithmetic only, no actual SAT algorithm, historical R_mix341 checker or independently verified proof of the primary theorem.

| Assumed $c$ | First positive $k$ | Optimal $k$ | Best $d_*$ |
|---:|---:|---:|---:|
| 1.2 | 1 | 2 | 0.511111111111 |
| 1.6 | 5 | 8 | 0.006393077970 |
| 1.61 | 7 | 10 | 0.002388069859 |
| 1.615 | 9 | 13 | 0.000752693848 |
| 1.617 | 11 | 15 | 0.000219071096 |
| 1.618 | 18 | 23 | 0.000004927236 |
| 1.61803 | 23 | 28 | 0.000000484348 |

At $c=1.61803$, even $N=10^{60}$ gives the exponent-only scale $N^{d_*}\simeq1.000067$, **not** a measured lower bound on bytes. At $c=6/5$, the ratio of exponent-only scales $N^{23/45}$ and $N^{1/2}$ is $N^{1/90}$: 1.1659, 1.3594, 1.8478 and 4.6416 for $N=10^6,10^{12},10^{24},10^{60}$. Constants and polylogs are unknown.

Executable: experiments/arc/lspv1_550_flmv_phi_envelope.py. Raw output: results/raw/arc/2026-11-09_1818_LSPV1_550_FLMV_PHI_RAW.json. Independent LSPV-5 review still pending.

## Source review, tracker ledger and limitations

Read both 2026-11-09 governing handoffs, complete root proof1.txt (startup blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b), complete root proof2.txt (startup blob 7ce6a525cccb870ed8fe77196fad108b2f930267), issue #3, AGENTS.md, CODEX.md, research skill; original reports LSPV-1/549, LSPV-5/471, Grok 2026-11-09 progress, Claude TPORT-0001; external konard/p-vs-np proof-status manifest, blkph0x/p-vs-np-proof-research method ledger and openai/math README, with their scope/trust qualifications. The new asymptotic and admissibility formula refine [P2-L1-549], but do not transfer SAT proof costs to machine resources.

The solver-class space abstraction is CONDITIONAL; [P2-D1], [P2-C3], [P2-B1] fixed-calculus lower-bound work OPEN; [P2-A2], [P2-A3], [P2-B2] unrestricted machine/B3 bridges OPEN; [P1-01], [P1-03], [P1-04] OPEN. Williams' later $c<2\cos(\pi/7)\approx1.80194$ SAT result is separate and does not use this explicit exponent.

Root main.tex read returned empty content for nonempty blob ab8fa88d3fbbf7a3bd69e40429101fb2041a44e1; it was **not overwritten**. A full local project checkout, preflight and native historical checker were unavailable. No automation, inference grammar or weight changes. P versus NP OPEN.

References: FLMV 2005 https://doi.org/10.1145/1101821.1101822 ; Fortnow/van Melkebeek DIMACS 2000-06 https://archive.dimacs.rutgers.edu/TechnicalReports/abstracts/2000/2000-06.html ; Williams 2008 https://eccc.weizmann.ac.il/eccc-reports/2007/TR07-036/index.html .
