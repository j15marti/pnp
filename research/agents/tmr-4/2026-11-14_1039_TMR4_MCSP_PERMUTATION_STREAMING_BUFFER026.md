# TMR-4/026: exact MCSP symmetry with a one-way streaming-buffer obstruction

**Date:** 2026-11-14 10:39 PST, America/Los_Angeles. **Owner:** TMR-4 Cost-Sound Abstraction. **Status:** TRANS26, complete scoped elementary argument, **CANDIDATE/RESTRICTED pending independent TMR-1/TMR-5 review**. Experiments **COMPUTATIONAL**. **P versus NP remains OPEN.** This is a new physical-interface obstruction and same-threshold label-preserving map, **not** threshold descent or a SAT lower bound.

## 1. The target and what is genuinely new

The current five-agent MCSP directive was read FIRST (main Git blob \`1e11aa64a0b0d635a65cea58500b09f2b0fe010a\`). The 2026-11-13 replacement directive, full proof1.txt (28,714 characters), authentic complete proof2.txt (1,051,196 characters; blob \`930c5eeddafce656717f28055a7a9a755f44737c\`), and authentic complete main.tex (2,545,859 characters; blob \`6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34\`) were recovered. The contents API returns empty bodies for the last two, so the Git **blob** API was used; no root file was modified. AGENTS.md, CODEX.md, pnp skill, issue #3 through TMR-3/025, all current TMR handoffs, and relevant original studies were surveyed.

**New relative to the original corpus:** a simple, full-input, fully invertible MCSP **same-integer-threshold** reduction is proved to require \(\Omega(N)\) *visited writable work cells* in any finite-alphabet one-way-input, append-only-output transducer, even though the underlying circuits are merely variable-renamed and retain EXACT minimum gate count. An explicit two-way-input counteralgorithm uses only \(O(\log N)\) work cells. This isolates a physical transport cost rather than logical MCSP hardness.

PRIOR comparisons, not new discoveries: TMR-1/024 gives exact dummy-variable padding and the 199/101 exponent corridor; TMR-4/024 falsifies the naive SAT satisfaction-truth-table reduction; TMR-2/024 and TMR-5/021 show compact residual representation does not force cheap *uniform* updates; TMR-3/024 and /025 study restricted charged networks. The older \`research/agents/chmy-threshold/2026-10-21_0712_CHMY_FIBER_CANCELLATION34.md\` audits a different fiber-masking/threshold construction. \`research/agents/lspv-4/2026-11-01_0636_LSPV-4_ARC_SORTED_ACCESSOR302.md\` examines a **clause-list sorted accessor**, not the exact standard-order truth-table permutation here. \`research/main/2026-10-21_1248_MAIN_RP_ORBIT_CERTIFICATION_FIREWALL40.md\` separates language invariance from lower bounds. Claude DIRECTPRODUCT-0001/TPORT-0001 remain portfolio and proof-rule restricted; TMR-4/023's full third-order moments remain a semantic, not arbitrary machine-trace, quotient. None supplies an all-machine SAT lower bound.

## 2. Precise models, functions and theorem

Let \(n\ge2\), \(N=2^n\), and the input \(x\in\{0,1\}^N\) be the **standard lexicographic truth table** of an \(n\)-variable Boolean function \(f\). The index \(j\) is represented by its \(n\) assignment bits, with bit 0 the least significant assignment variable. Define the involutive index permutation

$$
P_n(j)=(j\;\mathrm{with\ assignment\ bits}\ 0\ \mathrm{and}\ n-1\ \mathrm{exchanged}).
$$

Define \(y_j=x_{P_n(j)}\); this is the truth table of \(g(z)=f(z_{n-1},z_1,\ldots,z_{n-2},z_0)\), with the obvious interpretation for \(n=2\).

**Exact same-threshold transfer (PROVED algebraically within declared basis, peer pending):** For every truth table \(x\), in the fan-in-two AND/OR, unary NOT, unrestricted fan-out circuit basis with free constants and gate count, \(CC(g)=CC(f)\). Relabel two input wires in either direction without adding gates. Therefore for **every integer** \(s\), the map \(x\mapsto y\) is a total invertible both-label reduction of ordinary \(\mathrm{MCSP}_n[s]\) to itself. It neither changes \(N\) nor converts a large circuit threshold to a smaller one.

A *streaming transducer* here is ONE fixed total deterministic finite-control machine with one locally moving **one-way, read-only source tape** (no rewinds), \(w\ge1\) locally moving read/write work tapes, alphabet \(\Gamma\) of fixed size \(G\ge2\), and an EXTRA append-only, left-to-right write-only binary output tape. Input symbols and all work movement are charged; the output tape is granted FREE storage to make the lower bound stronger but its bits must be emitted **in target order** and cannot be revised. At most one output bit is appended per transition. Each input of length \(N\) must yield the exact full \(N\)-bit permuted table, with both MCSP labels automatically preserved. \(S(N)\) is the maximum **visited writable work cells**, summed across the \(w\) work tapes on all length-\(N\) inputs; the free output tape does not count. Input head starts at the left end and never moves left. No nonuniform advice, external index oracle, free side channel, preloaded source-dependent finite control or random output writes.

**Theorem TRANS26:**

$$
2^{N/2-1}\ \le\ 2q(S(N)+1)^{3w}G^{S(N)},
$$

where \(q\) is the fixed number of control states (in a standard interval-of-visited-cells convention; changing endmarker conventions modifies only the fixed polynomial factor). Consequently,

$$
S(N)\ \ge\ \left(\frac{1}{2\log_2G}-o(1)\right)N.
$$

Thus any such correct exact one-way transducer uses \(\Omega(N)\) visited work cells for this circuit-size-preserving permutation. No *decision-time* superlinear lower bound is asserted.

**Proof.** Put \(m=N/2\). The first two target coordinates are \(P_n(0)=0\) and \(P_n(1)=m\). Fix \(x_0=0\) and all \(x_i=0\) for \(i\ge m\), and vary independently the \(m-1\) bits \(x_1,\ldots,x_{m-1}\). This gives \(2^{m-1}\) sources sharing the **same unread suffix** at the moment just before the input head first reads coordinate \(m\).

Every total correct transducer must eventually read \(x_m\), because its second output bit is \(x_m\) and two inputs differing only there require different output. Before its first read of \(x_m\), it cannot have emitted the second output bit on **any** source: fixing the already-scanned prefix and changing unread \(x_m\) would make that bit wrong. Therefore the already-written output is either the empty prefix or the single fixed bit 0. (The write-head position distinguishes these possibilities.) The input head has the same coordinate \(m\) in every selected computation. All unread source suffixes, from \(m\) onward, are identical.

If two distinct chosen prefixes produced identical finite control, visited work-tape intervals, their symbols, work-head positions, and output head state at that cut, deterministic continuation would produce the **same remaining output**. But the two target strings differ: \(P_n\) is a bijection, and the varied \(x_1,\ldots,x_{m-1}\) all occur somewhere after the first two output bits. Contradiction. The configurations at that cut must therefore be distinct.

Every work tape has a contiguous visited interval containing its initial head coordinate. If the total number of visited cells on every run is \(\le s\), there are at most \((s+1)^2\) interval endpoint choices and at most \(s+1\) current head positions per tape, giving \((s+1)^{3w}\) positional descriptions. For fixed intervals, their total cell-symbol descriptions number at most \(G^s\). Add \(q\) control states and at most two output-prefix lengths. The input head is at the same coordinate \(m\). Hence \(2^{m-1}\le2q(s+1)^{3w}G^s\). If \(s\le N\), take binary logarithms and use \(\log(s+1)=O(\log N)\); if \(s>N\), the stated asymptotic lower bound is automatic. QED.

**Greedy tight buffer abstraction:** After reading \(k\) input bits, write the longest possible target prefix; let its length be \(j(k)\). Exactly \(k-j(k)\) scanned source bits have not been emitted. For this \(P_n\), \(\max_{0\le k\le N}(k-j(k))=m-1\): at \(k=m\), just \(y_0=x_0\) is available, while for \(k=m+r>m\), all target positions \(0,\ldots,r\) have source indices less than \(m+r\). An abstract ideal bit-buffer can therefore achieve peak \(m-1\) stored bits. The physical one-work-tape machine can store the full \(N\)-bit input and materialize output in charged polynomial time, giving \(O(N)\) visited work cells; no claim of optimal *time* follows.

**Two-way-source hostile counterexample:** If source head movement **in both directions** is allowed, one fixed uniform machine can hold a binary output index and input-head coordinate in \(O(n)=O(\log N)\) visited work cells, repeatedly reread original source bit \(x_{P_n(j)}\) for each output \(j\), and append it. Source travel costs \(O(N^2)\) head moves and one-tape binary arithmetic yields a conservative \(O(N^2\operatorname{polylog}N)\) transition bound. Thus the linear workspace bound does NOT transfer to two-way-input multitape SAT machines. Both implementations preserve every output bit and gate-complexity label.

## 3. Exact relation to MCSP magnification

| Source and theorem / regime | Exact input/model/claim | Consequence for TRANS26 |
| --- | --- | --- |
| Cheraghchi, Hirahara, Myrisiotis, Yoshida, STACS 2021, Theorem 1 and publisher abstract, [1] | Explicit \(N=2^n\)-bit ordinary \(\mathrm{MCSP}[N^{\mu_1}]\), deterministic one-way read-only input + one two-way work tape. An \(N^{1.01}\) **lower bound** for appropriately small \(\mu_1\) implies \(P\ne NP\). | TRANS26 provides only a *space* lower bound for a dedicated output transducer, not the requisite MCSP *decision time* bound. |
| Same source, Theorem 2 / publisher abstract, [1] | For a **different larger** \(\mu_2>\mu_1\), bounded-error randomized same-interface one-work-tape ordinary MCSP has an unconditional near-\(N^{1.99}\) time lower bound. | Exact variable relabeling preserves the integer threshold, so it cannot descend from \(\mu_2\) to \(\mu_1\). |
| McKay, Murray, Williams, STOC 2019, Theorems 1.2–1.3 / MIT accepted version, [2] | One-pass **search-MCSP with specified oracle circuits** and simultaneous update-time + space hypotheses has hardness magnification consequences. | Outputting a permuted truth table is not uniform search-MCSP and its \(\Omega(N)\) transport buffer is not a polynomial-in-\(s\) update lower bound. |
| Oliveira, Pich, Santhanam, Theory of Computing 17 (2021), [3] | Circuit lower-bound magnification for *promise Gap-MCSP* using two size thresholds and nonuniform circuits, with conclusions such as \(NP\not\subseteq P/poly\). | No cross-promise or cross-model transfer follows from a plain MCSP table permutation. |

[1] https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.STACS.2021.23 (published 2021-03-10). [2] https://dspace.mit.edu/entities/publication/d47cf035-39ca-4210-91e8-e5e3051d5deb (STOC 2019, accepted manuscript). [3] https://theoryofcomputing.org/articles/v017a011/ (2021-11-30). The exact bounds in this report are proved directly; no imported theorem is used inside TRANS26's proof.

## 4. Actual independently executed finite evidence

Native CPython 3 executed \`experiments/tmr/tmr4_permutation_buffer026.py\` (source SHA256 \`dcc64f552ab7cb7e376ab9639b1cf0e86a5a7de8b800d8e5d7b3d184ef55b7ad\`), output \`results/raw/tmr/2026-11-14_1039_TMR4_PERMUTATION_BUFFER026_RAW.json\` (raw SHA256 \`3f0f8126d0afc3920495393704c6242ef84859f2e1a44b6d6fd48b83a73f1661\`). Circuit grammar: AND/OR/NOT through 2 gates, shared input wires, free constants. For \(n=2,3,4\), all **197,424** truth-table/threshold classifications, including both YES and NO, agree after coordinate permutation; class counts for \(n=4\) are 6/22/90 for gates 0/1/2. For \(n=2,3,4,5\), all **32,906** low-half prefix variations give different future output suffixes, verifying \(2^{N/2-1}\) finite distinct continuations and peak abstract buffering \(N/2-1\). Total 230,330 assertions/checks in the runner, zero failures. Two-way reread proxy explicitly counts input-head movements 5,25,113,481 for \(N=4,8,16,32\); **this is not** a native finite-control TM compiler. No actual generic SAT/MCSP algorithm or physical one-work-tape emulator was executed. Symbolic proof, not finite tests, establishes the unbounded \(n\) conclusion.

**Hostile controls:** (i) input-only variable renaming is cheap *as a circuit description*, not free as an explicit reordered table; (ii) two-way input rereads evade the one-way memory lower bound; (iii) source output in arbitrary index order would invalidate the premise; (iv) preloaded advice/second input head, reusable output storage, or a source-rewriting interface also invalidate the stated model; (v) Horn, 2-SAT, XOR/GF(2), bounded treewidth, products, Walsh-moment and factorized circuit representations remain allowable for general SAT algorithms; this experiment does not implement their specialized solvers. Padding/auxiliary variables do not repair the threshold gap.

## 5. OPEN dependency and concrete next target

The key CHMY arrow remains missing:

$$
\text{large-threshold known one-way-tape lower bound}
\;\not\Rightarrow\;
\text{small-threshold required one-way-tape lower bound}.
$$

TRANS26 is a useful **model-audit falsifier**, not that missing arrow. **Next falsification target:** take one proposed source-dependent low-threshold reduction from TMR-1, explicitly list its target output coordinate dependencies, and determine whether source access/output scheduling impose an unavoidable buffer (one-way) or a paid reread/serialization cost (two-way). Unlike a circuit-description relabeling, prove both YES/NO labels and numerical exponent budget. **TMR-1/TMR-5 peer request:** independently verify the first-read cut, config-count bound, and both-label circuit relabeling; TMR-3 verify the two-way-input low-space replay and serialization charges. TMR-2 should check the relation to prior MCSP continuation/certificate bounds.

Root proof1.txt/proof2.txt and main.tex: **TRACKERS REVIEWED; NO MATERIAL CHANGE**. No universal SAT proof, no MCSP hardness-promotion. The original artifacts remain intact, no task identity or schedule changed. The new theorem remains **CANDIDATE/RESTRICTED** until independent review.
