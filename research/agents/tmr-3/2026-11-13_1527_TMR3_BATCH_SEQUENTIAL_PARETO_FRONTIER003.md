# TMR-3 / BATCHED-SEQUENTIAL-PARETO-FRONTIER003

**Date:** November 13, 2026, 15:27 PST (America/Los_Angeles).
**Owner:** NEW TMR-3 Time-Space Tradeoffs, j15marti/pnp main.
**Status:** CANDIDATE symbolic upper construction pending TMR-5 independent review; finite source emulator COMPUTATIONAL; earlier TMR-3/002 lower bound PROVED/RESTRICTED after independent TMR-5 review. P versus NP OPEN.

## 1. Exact increment and quantifiers

**New candidate TMR3-BS3 (intermediate resource frontier).** Let $E_n(a,b)$ be the existing explicitly encoded TMR-2 original proper 3-CNF family, $a,b\in\{0,1\}^n$, with $E_n(a,b)\in SAT$ iff $a=b$, $N=5n$, $M=8n$, $w=\max(1,\lceil\log_2(5n)\rceil)$, $g_n=12(1+w)$ and

$$
L_n=13n+2+24n(1+w)=\Theta(n\log(n+1)).
$$

Let $\sigma(n)$ be a *single fixed*, deterministically computable integer schedule for all $n$, with $\lceil c\log_2(n+2)\rceil\le\sigma(n)\le n$ for sufficiently large $n$. Assume the schedule can be evaluated from a binary $n$ in $O(L_n)$ ordinary multitape transitions and $O(\log(L_n+2))$ visited writable cells. Examples are $\sigma(n)=\lceil\log_2(n+2)\rceil$, $\sigma(n)=\lceil n^{p/q}\rceil$ for any fixed rational $0<p/q\le1$, and $\sigma(n)=n$.

There exists ONE fixed, total, correct deterministic multitape 3-SAT decider $B_\sigma$ (one physically sequential, freely reversing read-only source head, fixed finite alphabets and work tapes) such that **on every** valid family member $E_n(a,b)$,

$$
T_{B_\sigma}(E_n(a,b))
  =O_\sigma\!\left(L_n\left\lceil\frac{n}{\sigma(n)}\right\rceil\right),
\qquad
S_{B_\sigma}(E_n(a,b))=O_\sigma(\sigma(n)+\log L_n)=O_\sigma(\sigma(n)).
\tag{BS3}
$$

The time includes authentication, full physical source scans, rewinds, counters, work-head motions, buffer resets, and output. Space includes the batch buffer, counters, indices, parser, flags and all live work tapes. The read-only input tape is not counted as writable space but access is paid.

**Combined with previously independently reviewed TMR-3/002:** Every fixed correct sequential-input-head machine $A$ has on some **single satisfiable** family member of every sufficiently large $n$ the bound

$$
T_A(F)(S_A(F)+1)\ge c_A L_n n.
\tag{TW2}
$$

Therefore, any fixed uniform $A$ whose actual work space on every $E_n(a,a)$ is at most $D_A\sigma(n)$ has on at least one such diagonal source

$$
T_A(E_n(a,a))=\Omega_A\!\left(\frac{L_n n}{\sigma(n)}\right).
\tag{BS3-LB}
$$

Here the actual *same-input* $S_A(F)$ from TW2 is upper bounded by the explicitly assumed family-wide space cap. No time from another input is borrowed. The construction $B_\sigma$ attains this time scale on every family member, with a workspace cap of order $\sigma(n)$. Thus the **sequential-source equality-family tradeoff is tight, up to fixed constants, across the full logarithmic-to-linear workspace range**, not only at TMR-2's $\sigma=n$ endpoint. Constants may depend on the fixed machine and fixed schedule, never on n.

This is a statement about one recognizable EASY 3-CNF family and the physical source-head topology, not about general SAT complexity or all models.

## 2. Explicit single-machine algorithm

1. On arbitrary binary input $x$, run a complete, streaming authentication of the exact TMR-2 $E_n(a,b)$ grammar. Verify $1^{5n}0\,1^{8n}0$, total declared length, all $8n$ ordered proper three-variable clauses, all four signed unit-gadget rows per block, their fixed expected variable IDs and sign equalities, and the right endmarker. Stream expected IDs/counters with $O(\log L_n)$ cells. A malformed or non-family string takes the separate, paid correct general parser and exhaustive SAT fallback. Thus $B_\sigma$ is fixed, total and correct on ALL binary inputs without a promise.
2. For authenticated members compute the fixed $\sigma(n)$, rewind the physical source head, then iterate chunk starts $h=0,\sigma,2\sigma,\ldots$ until $h\ge n$. The current chunk has $r=\min(\sigma,n-h)$ pair indices.
3. During one physical left-to-right traversal of the whole $L_n$-bit source, retain ONLY the $r$ first-literal signs from first-bank blocks $h,\ldots,h+r-1$ in successive buffer cells. Before the second bank, rewind that buffer head by at most $r$ cells. During the same traversal compare the corresponding second-bank block signs sequentially with the retained signs, accumulating a mismatch flag in finite control.
4. Physically rewind the input head (at most $L_n$ steps) for the next chunk. When all $\lceil n/\sigma\rceil$ chunks finish, accept iff the mismatch flag remains false. In any family member, equality of these $n$ sign pairs is **exactly** satisfiability.

**Actual transition cost.** The source is read and, except for the final pass, physically rewound once per chunk: $O(L_n\lceil n/\sigma\rceil)$ head movements. The shape/record verifier performs at most $O(\log n)$ work per gadget and $O(1)$ amortized work per unary header symbol, totaling $O(L_n)$ steps since $L_n=\Theta(n\log n)$. Each subsequent sweep needs $O(\log n)$ finite-tape work per block for binary index comparisons, plus $O(1)$ amortized work per bit to maintain the small within-block counter. Hence each sweep is $O(L_n)$ actual multitape transitions; head-stay steps are charged. Per-sweep buffer rewind/reset is $O(\sigma)\le O(n)\le O(L_n)$, and the finite final output is charged. The fixed schedule's $O(L_n)$ preparation is included. No unit-cost unbounded arithmetic or random input index lookup is invoked.

**Actual writable space.** One sequential buffer of at most $\sigma$ bits, a constant number of binary counters/indices of $O(\log L_n)$ bits and parser state, together use $O(\sigma+\log L_n)$ visited cells on fixed work tapes. The buffer is **reused**, not duplicated for each chunk. A mismatch flag is one finite-control bit. The source and any fallback implementation are not invoked as free oracles; on actual E-family inputs fallback is never entered. The rejected/non-family branch may use exponential resources without affecting the scoped bound.

For $\sigma(n)=\lceil n^\alpha\rceil$ with any fixed rational $\alpha\in(0,1]$, the family has $S=O(n^\alpha)$ and $T=O(n^{2-\alpha}\log n)$; the lower bound applies to *any* fixed correct machine with a family-wide $O(n^\alpha)$ space cap. At the logarithmic endpoint, $S=O(\log n)$ and $T=O(n^2)$, while at the linear endpoint $S=O(n)$ and $T=O(n\log n)$. Every fixed exponent is polynomial. This does not exclude even one polynomial-time solver for arbitrary SAT, let alone all polynomial exponents.

## 3. Hostile controls and epistemic separation

- **General-source correctness:** A non-member (including a clause reorder, variable renaming, sign inconsistency, extra padding, or malformed header) is *not* falsely classified by the equality fast path. It is routed through a fully paid exhaustive general SAT routine. No fast-path claim is made after arbitrary reencoding.
- **SAT/UNSAT:** Both labels are decided, including $a=b$ and $a\neq b$, without enumerating assignments. Only the $\sigma$ simultaneously live signs are stored, rather than n signs or all potential configurations.
- **Sharing/caching/recomputation:** The buffer is shared and overwritten between chunks; each physical reread/recompute is charged. A full input copy would use $O(L_n)$ writable cells and is not part of this construction.
- **XOR/Tseitin, Horn, 2-SAT, bounded treewidth, disjoint products:** These are easy/alternative fast-path controls for any *putative universal* bottleneck. They do not strengthen the current equality-family theorem. In particular TMR-2/004's affine complete-graph family is polynomially decidable despite exponential solution count and large primal width.
- **Indexed input:** An indexed read-only source head escapes the physical-crossing lower bound. Our construction does not claim otherwise.
- **Quantifiers:** The schedule $\sigma$ and program $B_\sigma$ are fixed *once across all lengths*. The lower-bound hard input may depend on the tested machine and n. No pointwise minimization over different lookup programs, prescribed solver template, oracle, or external advice occurs.

**Status and coverage gap:** The upper construction is a CANDIDATE symbolic proof pending TMR-5 review. The previously reviewed TW2 is PROVED/RESTRICTED, conditional here on its established exact machine and source hypotheses. Together they describe a tight polynomial resource frontier in a restricted access geometry. No representation-independent compulsory global-consistency cost exceeding a polynomial is identified. The general every-A every-k lower-bound obligation and P versus NP remain OPEN.

## 4. Actual executed computational checks

The published zero-dependency JavaScript V8 audit models the canonical source syntax exactly and separately emulates every bit of a full forward scan, each reverse head traversal, and storage of at most one retained sign batch. It is **not** an instruction-level physical multitape machine simulator: host JavaScript loop indices, strings and bit arithmetic are not presented as literal TM resource measurements. The reported forward and rewind counts describe emulated source-head movements, not CPU time.

Deterministic V8 run: all $4^n$ ordered pairs for n=1..5, totaling 1,364 exhaustive signed formulas, plus 120 deterministic seeded pairs for n=6,8,16,32,64,128. Each case checks multiple batch sizes including 1, logarithmic, half-width and full n; 6,008 batch decisions. Cases: 92 SAT and 1,392 UNSAT. There were 40,428 passed assertions, 4,452 malformed controls and 1,484 single-gadget sign corruptions rejected, zero failures. The emulated passes visited 210,294,700 forward source bits and charged 198,630,820 reverse moves. Source lengths at n=1..5 were 111, 268, 401, 630, 787 bits; max n=128 had L=35,458 bits. Seed: 0x31f7d509. No external network, native OS Node, physical TM emulator, LaTeX compilation, full repository preflight or validator was executed.

**Reproducer:** [experiments/tmr/tmr3_batch_frontier003.cjs](https://github.com/j15marti/pnp/blob/main/experiments/tmr/tmr3_batch_frontier003.cjs), blob 25c36eb3a9daf2d1197b4e3419c863390692afff.
**Raw results:** [results/raw/tmr/2026-11-13_1527_TMR3_BATCH_FRONTIER003_RAW.json](https://github.com/j15marti/pnp/blob/main/results/raw/tmr/2026-11-13_1527_TMR3_BATCH_FRONTIER003_RAW.json), blob 672425942fd73eefef8c4dc1e4bce9e25212de73.

## 5. Original sources and prior work

[1] F. C. Hennie, *One-Tape, Off-Line Turing Machine Computations*, Information and Control 8 (1965), 553-578, https://doi.org/10.1016/S0019-9958(65)90399-2. Primary original checked: restricted one-tape off-line model, crossing sequences, tight transport bounds. His model is NOT the same as this fixed work-tape/off-line-input model. No theorem transferred without the separate TMR-3/002 proof.

[2] L. Fortnow, R. Lipton, D. van Melkebeek, A. Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6) (2005), 835-865, https://doi.org/10.1145/1101821.1101822. Primary author-hosted text checked, Theorem 1.1: for each fixed $c<(\sqrt5+1)/2$ there is a $d>0$ such that a deterministic **random-access** TM cannot decide SAT in simultaneously $n^c$ time and $n^d$ space. That simultaneous small-space exclusion permits arbitrary larger polynomial space and cannot be used to infer general P != NP or our sequential-head bound.

[3] Project original prior art, LSPV-5/167 (2026-10-26), research/agents/lspv-5/2026-10-26_1648_LSPV-5_CROSSING_AVERAGE_QUANTIFIERS167.tex, exact22 gap family and same-input averaging; Claude ONETAPE-0001 (2026-10-28), research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex, prior matching $O(nL)$ endpoint and two-way model scope.

[4] Independently reviewed TMR-3/002 (2026-11-13), research/agents/tmr-3/2026-11-13_1434_TMR3_TWOWAY_CROSSING_TRADEOFF002.md, original E-family full-configuration crossing bound, TMR-5/002 independent audit research/agents/tmr-5/2026-11-13_1452_TMR5_TEMPORAL_DEFERRAL_AND_CROSSING_REVIEW002.md.

[5] TMR-2/002 and /004 (2026-11-13), research/agents/tmr-2/2026-11-13_1420_TMR2_ONE_SWEEP_MATCHING_UPPER002.md and research/agents/tmr-2/2026-11-13_1512_TMR2_CLIQUE_TSEITIN_COMPRESSION004.md. TMR-2/002 is the $\sigma=n$ endpoint; the new contribution is the *entire intermediate paid batch frontier*, not discovery of communication/crossing bounds or a general SAT algorithm.

**Corpus and state:** Superseding TMR directive read first and rechecked; root proof1.txt and full 1,051,196-byte proof2.txt recovered from original Git blob; root 2,487,713-character main.tex recovered from original Git blob; current issue #3 and all five current handoffs, AGENTS.md, CODEX.md, repo SKILL, original TMR-3/001/002, TMR-2/002/004, TMR-5/002, historical LSPV-5/167, Claude ONETAPE-0001, and LSPV-4/460 examined. Older contradictory role-ownership directions are superseded, not reactivated.

**Root:** TRACKERS REVIEWED; NO MATERIAL CHANGE. No change to proof1.txt or proof2.txt because no unrestricted proof arrow has closed. TMR-3 region is available in root main.tex but newly derived upper construction awaits TMR-5 review; the manuscript is intentionally left unchanged. No scheduled task or agent changed.

**Next precise independent target:** TMR-5 should audit the streaming authentication cost on a fixed finite multitape machine, especially the $O(L_n)$ counter/identifier bookkeeping and buffer-head reset, and independently verify the matched worst-case family-wide cap with TMR-3/002. Then test whether any stronger global-consistency tradeoff can survive algebraic fast paths and indexed input without assuming a particular SAT representation.

END_OF_VERIFIED_REPORT::TMR3_BATCH_FRONTIER003::2026-11-13_1527_PST
