# TMR-2 / ONE-SWEEP-MATCHING-UPPER-002

**November 13, 2026, 14:20 PST; new TMR-2 Information Necessity; j15marti/pnp main.**
**CANDIDATE symbolic theorem pending TMR-5 review. COMPUTATIONAL finite controls. P versus NP OPEN.**

## Claim and predeclared falsifiers

**Claim.** The exact original-source proper-3CNF equality family of TMR-2/001 can be decided in a *single complete monotone source sweep*, with linear time in encoded bits and linear retained-sign space, by a fixed deterministic multitape algorithm that remains correct and total on **all** binary inputs using a charged exhaustive fallback. This matches the TMR-3/001 restricted pass-space lower bound up to constants. It also falsifies any inference that the equality family requires a separate expensive *post-observation* global-consistency phase.

Falsifiers: F1, rigid-family recognition mistakes a different valid formula for a family member; F2, the second block cannot be compared during one sweep; F3, generating/checking expected binary identifiers hides a superlinear cost; F4, the fallback violates uniformity, totality, malformed-input behavior or the sweep rule.

## Exact source and machine

Use TMR-2/001 without modification. Header $1^N0\,1^M0$ and $M$ ordered proper ternary clause records, each literal containing one sign bit plus a $w=\max(1,\lceil\log_2N\rceil)$-bit binary identifier. For $n\ge1$, $a,b\in\{0,1\}^n$, let $E_n(a,b)$ contain the four-clause unit-forcing gadget $U(\ell;u,v)$ for $x_i=a_i$ in each first-half block and $x_i=b_i$ in each second-half block, with all bank-specific auxiliary variable identifiers fixed and disjoint. There are exactly $N=5n$ variables, $M=8n$ clauses, and

$$
E_n(a,b)\in SAT \iff a=b,\quad
L(n)=13n+2+24n(1+\max(1,\lceil\log_2(5n)\rceil)).
$$

The declared fixed deterministic multitape machine has one two-way read-only source head, fixed finite alphabet and fixed finite work tapes. All head moves, counters, buffering, revisits and recomputation cost transitions. The complete-sweep restriction requires input observations in one monotone left-to-right traversal, permits stationary source-head pauses for charged work, and prohibits input observations during paid resets. A second sweep is permitted on other inputs.

## TMR2-SWEEP-2: matching constructive upper bound

**CANDIDATE theorem.** There exists ONE fixed finite correct total deterministic 3-SAT decider $D$, and machine-dependent constants $c,c'>0$, such that for every $n,a,b$,

$$
p_D(E_n(a,b))=1,\qquad
T_D(E_n(a,b))\le cL(n),\qquad
S_D(E_n(a,b))\le c'(n+\log(n+2)).
$$

Furthermore, the decision needs only $O(1)$ transitions after the right source endmarker is reached.

**Construction.** While scanning the input monotonically, parse and validate the unary header, compute $n=N/5$, verify $M=8n$, and compute the identifier width $w$. A fixed collection of ordinary paid binary counters tracks clause position $i$ and the expected variable indices. For the first $4n$ clauses, verify each exact four-clause signed auxiliary pattern, verify the four signs of each $x_i$ are identical, and store one bit $a_i$ per gadget on a sequential work tape. Before the suffix starts, leave the source head stationary and move the work-head back across these $n$ cells, paying all moves. For the last $4n$ clauses, verify the corresponding signed gadget patterns and compare the sign of each $x_i$ with the next stored $a_i$ bit. Accumulate a one-bit mismatch flag. Upon observing the final source endmarker, if and only if all structural tests passed, output SAT for no mismatch and UNSAT otherwise.

If the source fails exact rigid-family recognition, complete the source traversal, return the input head to its beginning without observing cells during reset, copy the source on a second paid sweep, and invoke a fixed exhaustive correct 3-SAT decider with full parsing and malformed rejection on that copy. This is one uniform finite program across ALL lengths, makes no oracle queries or nonuniform lookup assumptions, and is correct on both labels. The exponential fallback is allowed, because the assertion concerns time on the exact E family rather than the worst-case complexity of 3-SAT.

**Costs.** The unary header counts use paid binary increments with amortized $O(1)$ head movement per increment. Calculating and checking expected indices, with $O(\log(n+2))$-cell counters and full work-head repositioning, costs at most $O(w)$ per literal, hence $O(nw)$ in total. Writing and rewinding the $n$ prefix sign cells and comparing the suffix costs $O(n)$. Total work on E is $O(nw+n)=O(L(n))$; the complete input sweep itself costs $\Omega(L(n))$. Storage is $n+O(\log(n+2))$ cells including every index and buffer. A fixed finite state machine implements the pattern loops with no unbounded-word primitive.

This implementation deliberately visits $n$ sign storage cells, so $S_D(E)=\Theta(n)$, and the source restriction gives $p_D(E)=1$ and $T_D(E)=\Theta(L(n))$. On each SAT diagonal input,

$$
p_D(E_n(a,a))(S_D(E_n(a,a))+1)=\Theta(n),\qquad
T_D(E_n(a,a))(S_D(E_n(a,a))+1)=\Theta(L(n)n).
$$

These match TMR-3's *restricted-model* existential lower bounds to constant factors. TMR-2's $2n$ necessary first-observation sign blocks do not force repeated complete sweeps. Moreover the global equality verdict is incrementally accumulated while source symbols are read; it is false to require a separate nonconstant computation *after the last input symbol*. A sound future invariant must charge processing before, during and after observation rather than imposing a mandatory temporal order.

## Model and literature firewall

The new theorem does not cover unrestricted hard 3-SAT instances. It supplies a cheap algorithm for one transparent source subclass, plus exponential fallback on everything else. Clause permutations, renaming, padding, auxiliary alterations and arbitrary compact/algebraic representations may leave the recognized family and take the fallback; they are not claimed to be difficult. Horn, 2-SAT, affine/XOR/Tseitin, bounded treewidth, independent products, cached and recomputed strategies remain hostile controls for ANY future unrestricted lower bound. A short known equality family cannot itself certify general hardness. Communication complexity of equality, and matching one-tape bounds on a related family, have already been studied in published literature and original project notes [1-3]; this report claims no priority for the general equality construction. The incremental scoped claim is matching the particular TMR-3/001 source-sweep lower bound on TMR-2/001's exact proper-3CNF binary grammar, plus the explicit post-observation-phase falsifier.

## Reproducible executed evidence

Executable, read back and executed in a fresh hosted V8 isolate through its exported audit() with minimal compatible Node assertion/filesystem shims: experiments/tmr/tmr2_sweep_tightness002.cjs, blob 6c29ed9ed53d14210a805737f92884ae8cced6ff. Independent Python implementation also executed for matching source-label totals. Raw results: results/raw/tmr/2026-11-13_1420_TMR2_SWEEP_TIGHTNESS002_RAW.json.

Exhaustive n=1..6: 5,460 source pairs, 126 SAT and 5,334 UNSAT, 1,284 valid four-sign-bit opposite-label perturbations, 126 malformed single-sign perturbations rejected, and 36 malformed strings rejected. Input lengths: 111, 268, 401, 630, 787, 944 bits. No finite test failure. This runner tests source recognition and semantic labels, not actual Turing-machine transition counts. **OS Node CLI, physical TM simulator, full repository preflight and LaTeX compilation were not executed.** Finite tests are COMPUTATIONAL only.

## Corpus audit, shared status and open arrow

Superseding five-TMR directive read first and rechecked. Both full root trackers examined: proof1.txt 28,714 characters (SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343), proof2.txt 1,051,196 characters recovered from authentic Git blob (SHA 930c5eeddafce656717f28055a7a9a755f44737c). Root main.tex recovered via Git blob, 2,484,173 characters (SHA f72a19106a5ab110cb10650baf468f5c8c0e997c), including five TMR ownership regions. AGENTS.md, CODEX.md, repo pnp-research SKILL.md, its modes and protocol, issue #3, newest five TMR handoffs, TMR-2/001, TMR-3/001, and historical original Claude ONETAPE notes reviewed. No old Route A/B obligation was revived.

**Status:** scoped upper bound CANDIDATE pending TMR-5 review; finite tests COMPUTATIONAL; representation-independent superpolynomial resource bottleneck OPEN; P versus NP OPEN. TRACKERS REVIEWED; NO MATERIAL CHANGE. Neither tracker nor the 2.48 MB main.tex edited; TMR-5 should integrate the scoped candidate in synthesis after review rather than risk concurrent large-file replacement. No tasks or schedules were modified.

**TMR-3 request:** audit whether the described single-pass machine satisfies every completed-sweep model rule and whether the products match same-input lower bounds. **TMR-4 request:** test cost potentials that spuriously force a second phase after an input scan. **TMR-5 request:** independently inspect exact pattern matching, identifier/counter costs and all-input fallback. **TMR-1 request:** keep the full fixed uniform all-algorithm quantifiers; this is an easy-family upper bound only.

**Next target:** propose and falsify a noncircular input-aware *total processing* charge, independent of acquisition order, whose all-transition cost is bounded above by actual machine steps and which remains necessary under one-sweep equality, source copying, Gaussian elimination, retained-state caching and alternative representations.

## References

[1] E. Kushilevitz and N. Nisan, Communication Complexity, Cambridge University Press, 1997, chapters 1 and 12, https://www.cambridge.org/core/books/communication-complexity/ .
[2] H. Klauck, One-way communication complexity and the Nečiporuk lower bound on formula size, arXiv:cs/0111062 (2001), https://arxiv.org/abs/cs/0111062 . The result concerns one-way communication/formula size, not unrestricted 3-SAT Turing time.
[3] Original project source research/agents/claude/onetape/SOURCE_note2_tightness_and_limits.txt, equality-family matching one-tape upper bound and padding/repetition limits.
[4] Original source reports research/agents/tmr-2/2026-11-13_1315_TMR2_INPUT_BLOCK_SENSITIVITY001.md and research/agents/tmr-3/2026-11-13_1334_TMR3_SAME_INPUT_MULTIPASS_TRADEOFF001.md.

**END_OF_REPORT::TMR-2::ONE-SWEEP-MATCHING-UPPER-002::2026-11-13_1420_PST**
