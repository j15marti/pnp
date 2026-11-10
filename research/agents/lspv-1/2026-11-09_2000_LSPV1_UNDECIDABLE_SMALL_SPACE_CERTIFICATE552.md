# LSPV-1/552: fixed-time, fixed-language obstruction to complete abstract-space certification

**2026-11-09 20:00 PST | Route B | PROVED/RESTRICTED mathematical reduction + COMPUTATIONAL controls | P versus NP OPEN**

## IDEA and falsifiers

**Candidate:** Sharpen the existing [MODELBRIDGE-0010] undecidability of *marked-block reachability* into undecidability of a quantitative, **all-input peak-space** predicate, while giving every candidate machine the same fixed **near-linear time upper bound** and exactly the same fixed easy language. This targets the proposal that an effective abstract interpreter could automatically derive a small-space upper bound for an arbitrary hypothesized SAT machine solely from polynomial running time.

Three falsifiers: (F1) simulating an arbitrary machine for a growing number of steps itself consumes linear rather than logarithmic space; (F2) the high-space branch may occur only at finitely many input lengths, leaving an asymptotic logarithmic-space bound; (F3) the claimed logarithmic-versus-linear gap is a mismatch between high-address FLMV native space and physical touched-cell space. These are excluded by the explicit construction below. A fourth guard is that a no-go theorem about *complete automated classification* cannot be misconstrued as an impossibility of hand-proving a sound small-space invariant for a particular candidate.

## Theorem 552.1 (PROVED/RESTRICTED): undecidable peak-space classification inside one time class

Let $L=\{x\in\{0,1\}^*:|x|\ge1\text{ and }x_1=1\}$, and fix the deterministic random-access, work/index-tape model of FLMV (2005), Section 2.1. There is a computable map $E\mapsto D_E$ from arbitrary Turing machines (on blank input) into **uniform total deterministic deciders of exactly $L$**, each with an independently proved bound

$$
\forall N\ge2\quad T_{D_E}^{wc}(N)=O_E(N\log(N+2)).
$$

The predicate

$$
\mathsf{Small}_{1/2}(D)
\iff
\exists C,N_0\;\forall N\ge N_0\;\forall x\in\{0,1\}^{N}:
S_D(x)\le C N^{1/2}
$$

is **undecidable**, even restricted to this effectively generated family. In particular, the same holds for $O(\log N)$ versus $\Omega(N)$ peak-space classification. Every generated machine also satisfies $T=O_E(N^{6/5})$, so the obstruction persists at the commonly discussed FLMV hypothetical time exponent $c=6/5$; $L$ is deliberately NOT SAT.

### Proof

Given $E$, compile its finite transition table into a fixed simulator within $D_E$. On input $x$, record the first bit; scan the read-only source to obtain its length $N$ in a binary work counter. Set $k=\lfloor\log_2\max(1,N)\rfloor$. Simulate exactly $k$ steps of $E$ on blank input, stopping early if it halts. The first $k$ steps of any fixed ordinary-tape machine visit at most $k+O(1)$ tape cells, and its finite program is embedded in $D_E$. This phase therefore requires $O_E(k)$ work/index-tape cells and $O_E(k^a)$ time for some fixed simulator constant $a$ (indeed a direct compiled simulator can take $a=1$). The input scan and binary length counter take $O(N\log(N+2))$ time and $O(\log(N+2))$ native work space.

If $E$ halted during the bounded simulation, execute a dummy loop visiting and writing each of the first $\lfloor N/2\rfloor$ cells on a separate **contiguous work tape**. Otherwise skip this loop. Discard all dummy data. Finally accept iff the saved first input bit was one. The output is correct for every input, including the empty string, independently of $E$'s behavior. The scratch loop costs $O(N)$ time. Both the FLMV native high-water measure and the number of physically touched cells are at least $\lfloor N/2\rfloor$ when it executes; no far-address trick is involved.

If $E$ **never** halts, that loop never executes, and $S_{D_E}^{wc}(N)=O_E(\log(N+2))$. If $E$ halts after exactly $h$ steps, for every $N\ge2^h$ the bounded simulation detects it and the scratch loop executes, giving $S_{D_E}^{wc}(N)\ge\lfloor N/2\rfloor$. Consequently,

$$
\mathsf{Small}_{1/2}(D_E)\iff E\text{ never halts}.
$$

A total computable classifier deciding this predicate on all promised codes would decide the complement of the halting problem. Contradiction. $\square$

The proof extends to any **fixed** rational $0\le s<1$ with a space threshold $O(N^s\operatorname{polylog}N)$ and to any fixed time exponent $c>1$: the generated deciders satisfy $T=O(N^c)$ and their small-space/linear-space alternatives remain separated. This is a classical halting-reduction consequence with a quantitative resource calibration, not an unconditional SAT lower bound or new decidability breakthrough.

## Concrete/abstract machine interface (CONDITIONAL methodological result)

For machine $M$ and source $x$, take concrete configurations

$$
\sigma=(M,x,N,q,\text{input head},\text{work+index tape maps},\text{heads},\text{index values},t,H,\text{output}),
$$

where $H$ is **peak native largest work-tape position read/indexed**, not number of abstract states, configurations or nonzero cells. Include all parsing, counters, tape-head moves, indexed jumps, recomputation and terminal behavior. For nondeterministic $A_{NP}$, configurations also carry choice/branch information and the semantics remains existential for SAT; no nondeterministic branch sum is interpreted as simultaneous memory.

For a collecting set $X$, define $\alpha(X)$ by the may-set of control/output/branch tags and interval hulls for $t,H$, while $\gamma(a)$ contains all matching **complete** configurations. The best correct abstract post is $\operatorname{Post}^{\#}=\alpha\circ\operatorname{Post}\circ\gamma$, so $\operatorname{Post}(\gamma(a))\subseteq\gamma(\operatorname{Post}^{\#}(a))$. An independently established finite upper invariant on $H$ would be a valid peak-space bound for the specified program, but such a sound-and-complete effective upper-bound classifier cannot be total on the family $D_E$. This does not prohibit particular incomplete sound analyses.

For any hypothetical uniform total deterministic **SAT** machine $A_P$, a conditionally defined wrapper $D_{E};A_P$ preserves both SAT/UNSAT labels (and the chosen malformed-input policy) and adds the branch's $O(N)$ time and space, provided $A_P$ exists. This illustrates why a space bound cannot be read off an assumed time exponent for an arbitrary implementation; it **does not** imply the decision predicate for SAT machines is undecidable or rule out an *alternative* small-space SAT machine.

## FLMV quantifiers, numerical audit, and separate machine classes

At $c=6/5$, the published two-level deterministic FLMV threshold is $\beta(6/5)=23/45=1/2+1/90$. An independently **proved simultaneous same-machine** $T_P=O(N^{6/5}\operatorname{polylog}N)$ and $S_P=O(N^{1/2}\operatorname{polylog}N)$ on all inputs would contradict that theorem with strict exponent slack. The reduction above does **not** manufacture either premise for SAT. SAT in P allows unknown finite $c\ge2$; the conondeterministic threshold applies to a different model and **not** the ordinary existential SAT witness verifier $A_{NP}$.

Exponent-only scales (not measured bytes, nor finite-$N$ memory bounds):

| $N$ | $\log_{10} N^{23/45}$ | $\log_{10} N^{1/2}$ | $N^{1/90}$ | scratch-branch native high-water |
|---:|---:|---:|---:|---:|
| $10^6$ | 3.066667 | 3 | 1.165914 | $5\cdot10^5$ |
| $10^{12}$ | 6.133333 | 6 | 1.359356 | $5\cdot10^{11}$ |
| $10^{24}$ | 12.266667 | 12 | 1.847850 | $5\cdot10^{23}$ |
| $10^{60}$ | 30.666667 | 30 | 4.641589 | $5\cdot10^{59}$ |

The FLMV exponents are asymptotic forbidden **simultaneous** upper bounds with unspecified constants, not finite-instance memory predictions. The toy construction's $O(\log N)$ branch does not contradict FLMV because it decides a trivial regular language, not SAT.

## Evidence, provenance and continuity

Original primary literature reviewed: Fortnow, Lipton, van Melkebeek, Viglas (2005), *Time-Space Lower Bounds for Satisfiability*, JACM 52(6), 835-865, §2.1 and Theorems 1.1/1.2, https://lance.fortnow.com/papers/files/tst.pdf; Fortnow/van Melkebeek DIMACS report 2000-06, https://archive.dimacs.rutgers.edu/TechnicalReports/abstracts/2000/2000-06.html; Williams (2006), *Inductive Time-Space Lower Bounds for SAT and Related Problems*, https://doi.org/10.1007/s00037-007-0221-1. Distinguish alternate machine assumptions for stronger later results.

**Prior work / nonduplication:** MODELBRIDGE-0010 (2026-10-11) already proved marked-block reachability undecidable for general polynomial-time correct deciders; this result is its **fixed near-linear time, asymptotic peak-space exponent** strengthening. LSPV-3/545 and LSPV-5/473 already discovered native high-index padding and sparse normalization; this construction avoids far-address jumps and makes a formal classifier undecidability claim instead. LSPV-1/549-551 already optimized deterministic and co-nondeterministic FLMV parameter regions; no new exponent is claimed here. Actual Grok 2026-11-09_2015_PROGRESS and Claude 2026-10-28_1521_ONETAPE were reviewed; neither supplies an arbitrary-decider space upper. External `konard/p-vs-np` only certifies scoped finite-machine lemmas; `blkph0x/p-vs-np-proof-research` explicitly leaves unrestricted P vs NP open.

Finite evidence: `experiments/arc/lspv1_552_space_recognition.py` and `results/raw/arc/2026-11-09_2000_LSPV1_552_SPACE_RECOGNITION_RAW.json`: 57,337 exhaustive finite schedules, 11 negative controls and big-integer rows. This is a **small abstract event model**, not an executable FLMV machine or a test of actual SAT algorithms; the theorem rests on the proof above. No randomness. Native checker and full repo preflight not executed. Independent LSPV-3 / LSPV-5 review pending.

**Ledger:** chosen-model asymptotic space predicate: PROVED/RESTRICTED undecidability of exact general certification; full historical $R_{\mathrm{mix341}}$ lower bound [P2-D1/P2-C3/P2-B1] OPEN; noncircular B3 [P2-B2] OPEN; unrestricted machine lower bound [P1-01/P1-03/P1-04] OPEN. P versus NP OPEN. No automations or rule weights changed; LSPV-1 remains Route B (2 Route A / 3 Route B).

**Tracker disposition:** proposed [P2-L1-552] quantitative classifier barrier, only if conflict-safe full readback succeeds; otherwise TRACKERS REVIEWED; NO MATERIAL CHANGE. Root `main.tex` ranged retrieval returned zero content despite SHA; untouched to preserve other owned regions. **Next target:** restrict to a concrete, source-authenticated hypothesized SAT machine and prove an effective, all-input upper invariant for its exact native high-water $H$; do not infer one from an assumed time exponent alone.
