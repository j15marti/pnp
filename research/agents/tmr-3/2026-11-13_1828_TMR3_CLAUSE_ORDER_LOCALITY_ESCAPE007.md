# TMR-3/007: Clause-order locality defeats a semantic transfer of the one-head equality tradeoff

**Date:** 2026-11-13 18:28 PST (America/Los_Angeles). **Role:** NEW TMR-3 Time-Space Tradeoffs. **Scientific status:** exact source-reordering identity and charged uniform machine construction CANDIDATE pending independent TMR-5/TMR-1 review; finite execution COMPUTATIONAL; unrestricted 3-SAT superpolynomial lower bound and P versus NP OPEN.

## 1. New theorem candidate: same formula, different source geometry

TMR-3/002's previously proposed one-sequential-input-head crossing theorem concerns the GROUPED binary equality 3-CNF source $E_n(a,b)$ and yields, on some SAT diagonal, a same-trace product $T_A(S_A+1)=\Omega_A(L_n n)$. It explicitly depends on source order. This run constructs the **interleaved source** $I_n(a,b)$, obtained only by permuting entire original four-clause blocks. It preserves the unordered original 3-CNF exactly, including all signed clauses, identifiers, variables, number of clauses, and encoded bit length.

One fixed finite total deterministic all-input-correct 3-SAT machine $D$ with **one ordinary locally moving read-only input head** (NO indexed access or second head) has on EVERY interleaved member

$$
T_D(I_n(a,b))=O(L_n),\qquad S_D(I_n(a,b))=O(\log(L_n+2)).
$$

Thus, on one and the same execution,

$$
\frac{T_D(I_n(a,b))(S_D(I_n(a,b))+1)}{L_n n}
=O\!\left(\frac{\log L_n}{n}\right)\longrightarrow0.
$$

**Consequence:** Any proposed $\Omega(L_n n)$ time-space product applying to every ordering of these same unordered formulas, or following merely from their semantic answer, variable-clause incidence graph, or number of alternatives, is false. **This is NOT a counterexample to TMR-3/002's explicitly GROUPED encoding and one-head model.** The old proof relies on source cuts separating two banks. It cannot simply be transferred to the reordered source.

## 2. Exact binary source and SAT semantics

For $n\ge1$ and $a,b\in\{0,1\}^n$, use the original strict proper-3CNF binary grammar, with unary header $1^{5n}0\,1^{8n}0$, one sign bit plus $w_n=\max(1,\lceil\log_2(5n)\rceil)$ variable-ID bits per literal, and $8n$ complete 3-clauses. Set

$$
h_n=13n+2,\qquad g_n=12(w_n+1),\qquad
L_n=h_n+2ng_n=\Theta(n\log(n+1)).
$$

Let $B_i^0(a_i)$ be the original four-clause unit-forcing block on variable IDs $(i,n+2i,n+2i+1)$ and $B_i^1(b_i)$ the one on $(i,3n+2i,3n+2i+1)$. Each enumerates the four combinations of the last two literal signs in lexicographic order. Its first literal has uniform sign bit $1-a_i$ or $1-b_i$. The original source writes the $n$ first-bank blocks, then all $n$ second-bank blocks.

The new source writes, after the IDENTICAL header,

$$
I_n(a,b)=H_n\prod_{i=0}^{n-1}
\bigl(B_i^0(a_i)\,B_i^1(b_i)\bigr).
$$

It is a literal clause-record permutation of $E_n(a,b)$, not an auxiliary-variable reencoding. Each four-clause block forces $x_i$ to its designated bit: if the common first literal were false, one of the four clauses would be false regardless of its two auxiliary values. Hence both the grouped and interleaved binary sources encode the **same Boolean formula** and both are SAT exactly when $a=b$.

## 3. Fully paid fixed one-head machine

Fix one finite deterministic multitape program $D$ serving ALL binary lengths. Its input is read-only with ONE head that can only stay or move to an adjacent cell per transition; finitely many ordinary writable tapes, finite control and alphabet. All head positions, writable buffers, unary and binary counters, ID arithmetic, output and all input movements are charged.

(1) Scan the unary $5n,8n$ header locally, validate exact counts, maintain $O(\log L)$-bit counters. A least-significant-bit-first counter uses amortized $O(1)$ paid work-head moves per unary character, even with carries. Compute $w_n$ in charged logarithmic-size registers.

(2) For $i=0,\ldots,n-1$, read and authenticate first the four original $B_i^0$ clauses and then the adjacent four $B_i^1$ clauses. Compute their expected original variable identifiers using paid increments and $O(\log L)$-bit arithmetic. Compare every source sign and ID bit in exact order. For each of $O(n)$ constant-count literal records, generation, bit comparison and work-head positioning cost $O(w_n)$ physical steps. Hence total verification cost $O(nw_n)=O(L_n)$.

(3) Preserve only one first-bank sign bit while parsing its adjacent second-bank block. Add any inequality to a single mismatch flag, then discard that bit. There is NO $n$-bit bank cache, oracle, parallel access or algebraic subroutine.

(4) Authenticate the terminal endmarker. If all bytes exactly match this family, output SAT iff no mismatch, otherwise UNSAT. On ANY failed fast-path authentication, rewind the source head by paid local moves and run one fixed total, correct exhaustive parser and 3-SAT solver. It handles every other proper CNF and malformed source. Its worst-case exponential time is allowed OFF the family; it supplies both-label correctness and all-length totality.

On a valid fast-path source the input head advances across precisely $L_n$ source bits and observes the endmarker. All other physical work is $O(L_n)$; peak live work cells are $O(\log L_n)$. A standard finite-tape transition-table elaboration is not yet written, so the all-$n$ result is a **symbolically proved construction awaiting peer review**, not a native physical machine experiment.

The same-program, same-input time-space pair does not borrow resources from different machines or use a nonuniform lookup. Unrestricted polynomial workspace remains permitted on general inputs; the construction is an upper countermodel on a defined easy family, NOT a general polynomial 3-SAT algorithm.

## 4. Why the crossing-splice arrow does not transfer

In grouped $E_n$ every second occurrence of an $x_i$ decision is at the distant second bank, and many cuts in the first bank separate a variable-length prefix from its entire partner bank. In interleaved $I_n$, the two blocks for each $i$ are separated by only one block length $g_n$, so one fixed input head reads both consecutively. The grouped cuts and associated $2^j$ two-sided fooling sets no longer correspond to the same physical source locations. A formula-semantic argument cannot charge such input transport without proving an order-independent transfer or the cost of reordering.

Input ordering is part of the exact bit-string instance. The same unordered formula can have different runtime on different legal encodings. This finding leaves open hard inputs depending on $A,k,C,L_0$ under the team quantifiers, and does not rule out any all-input superpolynomial theorem. The general SAT lower-bound arrow remains OPEN.

## 5. Executed code, raw evidence and hostile controls

Executed independent hosted-V8 JavaScript: experiments/tmr/tmr3_interleaved_clause_order007.cjs. Raw results: results/raw/tmr/2026-11-13_1828_TMR3_INTERLEAVED_ORDER007_RAW.json. Both committed to main and byte-for-byte readback verified.

- **1,420 valid sources**, SAT 118, UNSAT 1,302: exhaustive all $a,b$ for $n=1,\ldots,5$ plus seeded $n=8,16,32,64,128,256,512$.
- **1,420 exact whole-source clause-block permutation/length checks** matched grouped and interleaved original sources.
- **7,100 malformed/structural/sign/ID controls rejected**, and **40 independently exhaustive original-CNF truth evaluations** for both encoded orders at $n\le2$.
- Input-local movement proxy: **3,454,956** adjacent source moves, **3,456,376** read events; **3,147,616** literal expected-field bit checks and **14,500** paired-sign comparisons. Maximum original source length **166,402** bits. **Zero failures.**

This is original standalone V8 source-bit execution, not a wrapper around earlier TMR-3 code. It uses host-number arithmetic and strings and does **not** execute the exhaustive fallback or simulate a physical TM transition table. The physical $O(L)$ and $O(\log L)$ charges are symbolic; finite data alone are not an asymptotic proof.

**Falsification controls:** exact output labels on both sides, bitwise original-clause preservation, endmarker, bad header, one-bit altered sign or identifier, shortened/extended encoding, long lengths, and original-CNF brute force. Horn, 2-SAT, high-treewidth Tseitin/GF(2), bounded-treewidth, products, padding, auxiliary variables, caching and recomputation are legal general inputs handled by the correct but potentially slow fallback; their physical fast-path runtimes were NOT tested or asserted.

## 6. Primary literature, inherited results, scope

[1] F. C. Hennie, *One-tape, off-line Turing machine computations*, Information and Control 8 (1965), 553-578, DOI https://doi.org/10.1016/S0019-9958(65)90399-2. Physically sequential crossing sequences, not general SAT lower bounds.

[2] L. Fortnow, R. Lipton, D. van Melkebeek, A. Viglas, *Time-Space Lower Bounds for Satisfiability*, J. ACM 52(6) (2005), 835-865, DOI https://doi.org/10.1145/1101821.1101822, author source https://lance.fortnow.com/papers/files/tst.pdf, Sections 1 and 2.1. They permit paid INDEX jumps (INDEX tape erased after jumps) and prove only excluded simultaneous $n^c$ time and $n^d$ space pairs with $c$ below the golden ratio and a suitable $d>0$. This cannot exclude arbitrary polynomial-space polynomial-time machines.

[3] Exact earlier grouped-source TMR-3/002 report: research/agents/tmr-3/2026-11-13_1434_TMR3_TWOWAY_CROSSING_TRADEOFF002.md. TMR-3/006 two-HEAD local escape: research/agents/tmr-3/2026-11-13_1723_TMR3_TWOHEAD_SEQUENTIAL_PORT_BOUNDARY006.md.

[4] Independent separate easy-family control: TMR-2/007 toroidal cubic Tseitin streaming report, research/agents/tmr-2/2026-11-13_1812_TMR2_TORUS_CUBIC_STREAMING_ESCAPE007.md. It changes graph structure; THIS report changes clause order only.

**Read corpus/safeguards:** authoritative five-TMR directive first and rechecked SHA 47459817e66dccf1f3079e6c724c0fd2643e7bc4. Full proof1.txt 28,714 characters SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343, full authentic proof2.txt Git blob 1,051,196 characters SHA 930c5eeddafce656717f28055a7a9a755f44737c, full main.tex Git blob 2,497,977 characters SHA 4e0dc7a81c3757289e87661b6df29e458cd03daa; standard contents-fetch misleadingly blank for the latter two. Latest issue #3 through TMR-2/007, AGENTS.md, CODEX.md, pnp skill, five current TMR handoffs and original TMR-3/002,/006, TMR-2/007 and TMR-4/006 inspected. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root main.tex left to TMR-5 synthesis, no new main.tex. No scheduled tasks modified.

**One next target:** TMR-5 independently verify the all-length one-head fully paid parser and source order permutation. Find a genuine post-acquisition processing necessity that survives even clause-local interleaving, indexed input, compact GF(2), sharing/recomputation, and arbitrary polynomial workspace. All-exponent general SAT separation remains OPEN.

END_OF_REPORT::TMR3::CLAUSE_ORDER_LOCALITY007::2026-11-13_1828_PST
