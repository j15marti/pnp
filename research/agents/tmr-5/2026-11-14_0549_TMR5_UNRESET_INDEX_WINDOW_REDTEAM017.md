# TMR-5/017: independent TMR-3/018 audit and unreset delayed-INDEX locality theorem

**Pacific time:** November 14, 2026, 05:49 PST (America/Los_Angeles). **Owner:** TMR-5 Machine Bottleneck Redteam and synthesis. **Status:** TMR-3/018 original restricted proof **INDEPENDENTLY REVIEWED, PROVED/RESTRICTED** under its explicit two-phase and reset hypotheses; new TMR5-UW17 **CANDIDATE/RESTRICTED** pending independent TMR-1/TMR-3 review. Experiment **COMPUTATIONAL**. Unrestricted 3-SAT lower bound **OPEN**.

## 1. Exact original peer audit

Original peer report: `research/agents/tmr-3/2026-11-14_0529_TMR3_POSTPREPROCESS_INDEX_CACHE_BARRIER018.md`; original executable `experiments/tmr/tmr3_postprep_index_cache018.cjs`; original raw evidence `results/raw/tmr/2026-11-14_0529_TMR3_INDEX_CACHE018_RAW.json`.

The original deterministic delayed-INDEX machine preprocesses an arbitrary source $x\in\{0,1\}^L$, uses at most $s$ visited writable cells across $h$ ordinary tapes, physically resets its read-only source head to the left endmarker, and receives an externally delayed, charged index $p$. The correct answer is $x_p$ for every $(x,p)$. Set $M_A(s)=q(2s+3)^{3h}g^s$, where $q$ is the fixed control-state count and $g\ge2$ bounds work alphabet sizes. Tape-head positions, visited intervals, and contents are included. For $L>\lfloor\log_2M_A(s)\rfloor$, choose the first $L-\lfloor\log_2M_A(s)\rfloor-1$ input bits equal across $2^{\lfloor\log_2M_A(s)\rfloor+1}$ suffix completions. More source completions than retained configurations force two inputs to collide. At the same query $p$ where their sources differ, they must diverge by reading a later source position, which requires at least $L-\lfloor\log_2M_A(s)\rfloor$ physical moves from the reset left head. This validates the peer's exact inequality, **under its assumptions**. Its finite program independently checks only $s$-bit sketches and physically tracked prefix reach, not the full arbitrary-machine theorem, as its report correctly states.

There is no deduction for a general SAT solver, which does not receive delayed INDEX requests. An attempt to drop the source-head RESET condition while retaining the almost-$L$ lower bound is false. The next theorem repairs this by retaining the source-head position in the information accounting and charging true physical locality.

## 2. New theorem TMR5-UW17: arbitrary final source-head position

Fix one total uniform deterministic ordinary multitape machine $A$ with one locally moving, read-only $L$-bit original-source head, $h$ writable work tapes, finite alphabet bound $g\ge2$, fixed $q$ control states, and separate externally delayed charged query tape. Preprocess $x$ arbitrarily, including all rereads, compact algebra and recomputation; the index $p\in\{1,\ldots,L\}$ is not available until phase 2. At the phase boundary every pre-query execution has at most $s$ visited writable cells, but the original-source head may park at any input/endmarker position $u(x)\in\{0,\ldots,L+1\}$. Query time includes all physical moves, local reads, output and work; $A$ must return $x_p$ for **every** $(x,p)$.

Let
$$
M_A(s)=q(2s+3)^{3h}g^s,\quad
H_A(L,s)=(L+2)M_A(s),\quad
t_A(L)=\max_{x\in\{0,1\}^L,\,p\in[L]}T_A^{\mathrm{query}}(x,p).
$$
Then for every $L\ge1$,
$$
\boxed{\quad 2^L\le H_A(L,s)2^{2t_A(L)+1}\quad}
$$
and consequently
$$
\boxed{\quad
t_A(L)\ge\max\left\{0,\left\lceil\frac{L-1-\log_2 H_A(L,s)}{2}\right\rceil\right\}.\quad}
\tag{UW17}
$$
Thus **for any fixed $A$**, if its all-source retained-work budget satisfies $s(L)=o(L)$, then
$$
t_A(L)\ge (\tfrac12-o(1))L.
$$
No source-head reset, fixed query coordinate, prescribed sketch, solver template, SAT oracle, or uncharged memory lookup is used.

**Proof.** The fixed-program pre-query writable control/heads/visited-boundaries/contents have at most $M_A(s)$ possible configurations, using the same complete-state overcount as TMR-3/018. Multiply by $L+2$ for the original head position $u$. If every delayed query halts within $t$ transitions, then during any query the source head cannot inspect a bit outside
$$
W_t(u)=\{j\in[L]:|j-u|\le t\}.
$$
There are at most $2t+1$ positions in $W_t(u)$. Encode each original source string $x$ by its actual pre-query complete writable configuration, actual head position $u(x)$, and the bits of $x$ in $W_t(u(x))$, in increasing address order. This encoding must be injective: if distinct $x,y$ had the same triple, their delayed-query runs on the same index $p$ with $x_p\ne y_p$ would begin in identical machine states, receive the same independent query tape and observe only identical source bits for their first $t$ transitions. They would give identical answers or both fail to finish, contradicting the universal exactness and time-bound assumptions. Thus $2^L$ distinct strings inject into at most $(L+2)M_A(s)2^{2t+1}$ encodings, proving the inequality. The asymptotic bound follows from $\log_2M_A(s)=s\log_2g+O_A(\log(s+2))$ and $\log_2(L+2)=o(L)$. Every transition is accounted for by the physical locality radius; this is an all-machine theorem for **the delayed-INDEX interface only**. QED, pending independent mathematical review.

## 3. Hostile controls and falsification boundary

**Why reset cannot simply be removed from IC18.** A fixed total two-phase uniform machine can, with $O(\log L)$ writable cells and paid preprocessing, read source length, park its physical source head near the midpoint $u=\lfloor(L+1)/2\rfloor$, and later answer an arbitrary requested bit by moving toward the query coordinate. For every requested $p$, the number of **original source-head movements** in its query phase is at most $\lceil L/2\rceil$; query-index decoding/counter arithmetic is additional charged work, and a standard binary countdown implementation permits total query time $O(L)$, not a claimed $L/2+o(L)$ exact transition count. Thus a reset-free near-$L$ *source-head movement* claim is false; the factor $1/2$ in the geometric lower bound is the correct worst-case locality scale, while exact total-transition constants depend on the physical compiler. This is an explicit legitimate complete-input geometric shortcut, not a spurious abstraction path.

**Full input caching:** $s=L$ permits an injective retained representation and defeats the sublinear-space premise. Arbitrary XOR/GF(2), Horn/2-SAT, bounded-treewidth, products, sharing, auxiliary variables and reencoding can be performed during preprocessing, but none imply a delayed INDEX query is compulsory for SAT. The query-index tape cannot supply an $x$-dependent oracle bit or advice. The local-window proof remains valid against adaptive rereads and changing head location because those behaviors determine the actual post-preprocess state and remain charged. A general polynomial-space SAT algorithm is unexcluded.

**Relation to abstraction:** TMR-4's all-transition cost-sound projection can be used to certify a particular two-phase query machine, but a potential for this port is not an unconditional SAT-time potential. TMR-2/019's valid opposite-label 3-CNF sign sensitivity yields only $\Omega(L)$ physical input visits on a nine-variable linear-time family, again no compulsory semantic-processing exponent.

## 4. Independently executed finite checks

**Native CPython, independently authored, not a wrapper around TMR-3's JS.** Script: `experiments/tmr/tmr5_unreset_window_audit017.py`; raw JSON `results/raw/tmr/2026-11-14_0549_TMR5_UNRESET_WINDOW017_RAW.json`. Executed in one sub-25-second chunk. Lengths $L=4,\ldots,10$; up to four retained sketch bits; four representation sketches (prefix, suffix, XOR stripes, nonlinear XOR); six source-head parking policies (left, right, center, parity-dependent endpoints, first-one, input-dependent quadrant); and observation radii zero through four. Verified **4,080** cases, **840** pigeonhole-forced collision cases, **3,293** actual indistinguishable pairs, and **3,293** distinct opposite-bit queries beyond the observation window. Full-source copy injectivity passed **2,032** controls; centered-head geometry passed **49** positions. **Zero assertions failed.** The Python source, not the peer JavaScript, was executed natively. Host-Python sketches and query-index arithmetic are not charged TM implementations, so finite evidence remains **COMPUTATIONAL**.

## 5. Literature, provenance, and dependency synthesis

Primary references independently checked (exact original models):
1. A. C.-C. Yao, *Some Complexity Questions Related to Distributive Computing*, STOC 1979, DOI https://doi.org/10.1145/800135.804414 . Communication bits exchanged; no automatic transfer to unrestricted 3-SAT Turing machines.
2. P. B. Miltersen, N. Nisan, S. Safra, A. Wigderson, *On Data Structures and Asymmetric Communication Complexity*, JCSS 57(1), 37–49 (1998), DOI https://doi.org/10.1006/jcss.1998.1577 . Cell-probe/asymmetric communication scope, not this exact locally moving physical tape theorem.
3. L. Fortnow, R. Lipton, D. van Melkebeek, A. Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6), 835–865 (2005), DOI https://doi.org/10.1145/1101821.1101822 . Deterministic random-access SAT exclusions only for specified small-space polynomial exponents, not all polynomial workspaces.

**Strongest surviving implication:** complete-state compression plus physical source locality forces a linear worst-case delayed-INDEX query even when the input head is not reset, but only under sublinear retained writable space. **Next missing arrow:** every correct uniform full-input deterministic 3-SAT decider must necessarily perform an expensive post-observation delayed query or equivalent charged semantic processing, while permitting arbitrary polynomial workspace and fully interleaved computation. This arrow is OPEN. Neither P=NP nor P!=NP follows.

**Repository audit:** Replacement directive read first (Git SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4), root proof1.txt completely read, root proof2.txt nonempty 1,051,196-character authentic blob recovered by SHA 930c5eeddafce656717f28055a7a9a755f44737c, root canonical main.tex 2,533,636-character authentic blob read SHA 867c9b7512a51d59a50c479e81dda6c65615026f. AGENTS.md, CODEX.md, pnp-research skill, all five current TMR handoffs, original TMR-3/018 source/raw, TMR-1/019, TMR-2/019, TMR-4/019, prior TMR-5/016, issue #3 through TMR-3/018, historical input-access and checker limitations considered. The superseding directive governs identities and ownership. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** No schedules touched. Main synthesis is TMR-5 owned. The full arbitrary-machine compiler and LaTeX OS toolchain were not executed.

**Peer request:** TMR-1 and TMR-3 independently audit the injectivity proof, including state-count overcount, source locality, variable original head position, the externally delayed query, and the exact half-factor. TMR-2 pursue a semantic SAT analogue. TMR-4 investigate whether every full SAT execution can support any nontrivial input-aware cost-sound potential. Keep new TMR5-UW17 CANDIDATE/RESTRICTED pending peer review and keep P versus NP OPEN.

END_OF_REPORT::TMR-5::017::2026-11-14_0549_PST
